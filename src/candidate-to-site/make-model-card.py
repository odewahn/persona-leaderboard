import requests
import os
import argparse
import json
import yaml
import jinja2

CANDIDATE_PATH = f"{os.getcwd()}/../../candidates"
EVALUATIONS_PATH = f"{os.getcwd()}/../../evaluations"
SITE_PATH = f"{os.getcwd()}/../../docs"


def load_file(file_path):
    # load the file and return its content
    with open(file_path, "r") as file:
        content = file.read()
    return content


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

questions = load_file("../questions.txt")
# convert quetions to a list
questions = questions.split("\n")

evaluation = []
sum_burrows = 0.0
sum_andreww = 0.0

for idx, q in enumerate(questions):
    answer = load_file(f"{CANDIDATE_PATH}/{model_name}/answer-{idx}.txt")
    eval = load_file(f"{EVALUATIONS_PATH}/{model_name}/answer-{idx}.txt.eval.json")
    # convert eval to json
    eval = json.loads(eval)
    sum_burrows += eval["burrows_delta"]["score"]
    sum_andreww += eval["andreww_model"]["score"]
    evaluation.append({"question": q, "answer": answer, "eval": eval})


system_prompt = load_file(f"{CANDIDATE_PATH}/{model_name}/system.txt")
config = load_file(f"{CANDIDATE_PATH}/{model_name}/config.yaml")
config = yaml.safe_load(config)


data = {
    "model_name": model_name,
    "system_prompt": system_prompt,
    "config": config,
    "scores": {
        "burrows_delta": sum_burrows / len(questions),
        "andreww_model": sum_andreww / len(questions),
    },
    "evaluation": evaluation,
}

# Save the data to a JSON file for debugging purposes
with open(f"{SITE_PATH}/{model_name}.json", "w") as f:
    json.dump(data, f, indent=4)

# Now generate the model card using Jinja2
template_loader = jinja2.FileSystemLoader(searchpath="./")
template_env = jinja2.Environment(loader=template_loader)
template_file = "model_card_template.jinja"
template = template_env.get_template(template_file)

# Render the template with the data
model_card = template.render(data)
# Save the model card to a file
with open(f"{SITE_PATH}/{model_name}.md", "w") as f:
    f.write(model_card)
