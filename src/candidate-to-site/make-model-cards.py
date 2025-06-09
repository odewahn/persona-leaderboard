import requests
import os
import argparse
import json
import yaml
import jinja2

MKDOCS_YAML_FN = f"{os.getcwd()}/../../mkdocs.yml"
CANDIDATE_PATH = f"{os.getcwd()}/../../candidates"
EVALUATIONS_PATH = f"{os.getcwd()}/../../evaluations"
SITE_PATH = f"{os.getcwd()}/../../docs"

# Prepare the Jinja2 template environment
template_loader = jinja2.FileSystemLoader(searchpath="./")
template_env = jinja2.Environment(loader=template_loader)
template_file = "model_card_template.jinja"
template = template_env.get_template(template_file)


def load_file(file_path):
    # load the file and return its content
    with open(file_path, "r") as file:
        content = file.read()
    return content


def gather_data(questions, model_name):
    # This function is a placeholder for any additional data gathering logic
    # that might be needed in the future.
    evaluation = []
    sum_burrows = 0.0
    sum_andreww = 0.0
    all_burrows = []
    all_andreww = []

    for idx, q in enumerate(questions):
        answer = load_file(f"{CANDIDATE_PATH}/{model_name}/answer-{idx}.txt")
        eval = load_file(f"{EVALUATIONS_PATH}/{model_name}/answer-{idx}.txt.eval.json")
        # convert eval to json
        eval = json.loads(eval)
        eval["burrows_delta"]["score"] = round(eval["burrows_delta"]["score"], 4)
        eval["andreww_model"]["score"] = round(eval["andreww_model"]["score"], 4)
        sum_burrows += eval["burrows_delta"]["score"]
        sum_andreww += eval["andreww_model"]["score"]
        all_burrows.append(eval["burrows_delta"]["score"])
        all_andreww.append(eval["andreww_model"]["score"])
        evaluation.append({"question": q, "answer": answer, "eval": eval})

    system_prompt = load_file(f"{CANDIDATE_PATH}/{model_name}/system.txt")
    config = load_file(f"{CANDIDATE_PATH}/{model_name}/config.yaml")
    config = yaml.safe_load(config)

    # compute the median of the scores
    if len(all_burrows) > 0:
        all_burrows.sort()
        median_burrows = all_burrows[len(all_burrows) // 2]
    else:
        median_burrows = 0.0

    if len(all_andreww) > 0:
        all_andreww.sort()
        median_andreww = all_andreww[len(all_andreww) // 2]
    else:
        median_andreww = 0.0

    data = {
        "model_name": model_name,
        "system_prompt": system_prompt,
        "config": config,
        "scores": {
            "burrows_delta": round(sum_burrows / len(questions), 4),
            "andreww_model": round(sum_andreww / len(questions), 4),
            "median_burrows_delta": median_burrows,
            "median_andreww_model": median_andreww,
        },
        "evaluation": evaluation,
    }
    return data


candidates = os.listdir(CANDIDATE_PATH)
questions = load_file("../questions.txt").split("\n")

score_summary = []
for candidate in candidates:
    print(f"Processing candidate: {candidate}")
    # gather data for the candidate
    data = gather_data(questions, candidate)

    # comput the final score summary
    for s in data["evaluation"]:
        score_summary.append(
            {
                "model_name": data["model_name"],
                "question": s["question"],
                "burrows_delta": s["eval"]["burrows_delta"]["score"],
                "andreww_model": s["eval"]["andreww_model"]["score"],
            }
        )

    # Save the data to a JSON file for debugging purposes
    with open(f"{SITE_PATH}/{candidate}.json", "w") as f:
        json.dump(data, f, indent=4)

    # Render the template with the data
    model_card = template.render(data)

    # Save the model card to a file
    with open(f"{SITE_PATH}/{candidate}.md", "w") as f:
        f.write(model_card)

# write the score summary as a csv
import csv

with open(f"{SITE_PATH}/score_summary.csv", "w", newline="") as csvfile:
    fieldnames = ["model_name", "question", "burrows_delta", "andreww_model"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in score_summary:
        writer.writerow(row)
