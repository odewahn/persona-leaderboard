import requests
import os
import argparse
import json
import sys

CANDIDATE_PATH = f"{os.getcwd()}/../../candidates"
EVALUATIONS_PATH = f"{os.getcwd()}/../../evaluations"


def fetch_files(answers_dir):
    # load all files that have the pattern "answers-*.txt" in the answers directory
    files = [
        f
        for f in os.listdir(answers_dir)
        if f.startswith("answer-") and f.endswith(".txt")
    ]
    if not files:
        raise ValueError("No answer files found in the 'answers' directory.")
    return [os.path.join(answers_dir, f) for f in files]


def load_file(file_path):
    # load the file and return its content
    with open(file_path, "r") as file:
        content = file.read()
    return content


def evaluate(content):
    # raise an error if the content is not a string
    if not isinstance(content, str):
        raise ValueError("Content must be a string")

    # Make the API request
    response = requests.post(
        "https://persona-service.platform.gcp.oreilly.review/api/v1/persona-service/metrics",
        headers={"Content-Type": "application/json"},
        json={"content": content},
    )

    # Check if the request was successful
    if response.status_code == 200:
        out = response.json()
        if out["success"] is False:
            raise Exception(f"Error: {out['error']}")
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


# get first argument to use as the answers directory
parser = argparse.ArgumentParser(description="Process answers.")
parser.add_argument(
    "name",
    type=str,
    help="You must provide a name for the evaluation run.",
)
args = parser.parse_args()
print(f"Arguments received: {args}")

print(f"Fetching answer files from directory: {args.name}")
# remove the trailing slash if it exists
if args.name.endswith("/"):
    args.name = args.name[:-1]

# model name is the last argument
model_name = args.name.split("/")[-1]
# if the model name is empty, raise an error
print(f"Model name: {model_name}")


files_dir = f"{CANDIDATE_PATH}/{model_name}/"
print(f"Files directory: {files_dir}")

# Load all the answers files from the specified directory
files = fetch_files(files_dir)
files.sort()
print(f"Files to evaluate: {files}")


for file in files:
    fn = os.path.basename(file)
    eval_fn = f"{EVALUATIONS_PATH}/{model_name}/{fn}.eval.json"
    # If the eval file does not extis, create it
    if not os.path.exists(eval_fn):
        with open(eval_fn, "w") as f:
            print(f"Creating evaluation file: {eval_fn}")
            content = load_file(file)
            print(f"Evaluating file: {file}")
            evaluation = evaluate(content)
            f.write(json.dumps(evaluation, indent=4))
