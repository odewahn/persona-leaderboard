# This has to be run after the make-model-cards.py script
import os
import json
import jinja2


CANDIDATE_PATH = f"{os.getcwd()}/../../candidates"
EVALUATIONS_PATH = f"{os.getcwd()}/../../evaluations"
SITE_PATH = f"{os.getcwd()}/../../docs"

# Prepare the Jinja2 template environment
template_loader = jinja2.FileSystemLoader(searchpath="./")
template_env = jinja2.Environment(loader=template_loader)
template_file = "group-by-question.jinja"
template = template_env.get_template(template_file)


def load_file(file_path):
    # load the file and return its content
    with open(file_path, "r") as file:
        content = file.read()
    return content


candidates = os.listdir(EVALUATIONS_PATH)
questions = load_file("../questions.txt").split("\n")

out = []
for idx, q in enumerate(questions):
    answers = []
    print(f"Processing question {idx}: {q}")
    for candidate in candidates:
        data = json.loads(load_file(f"{SITE_PATH}/{candidate}.json"))
        answers.append(
            {
                "candidate": candidate,
                "answer": data["evaluation"][idx]["answer"],
                "eval": data["evaluation"][idx]["eval"],
            }
        )
    out.append(
        {
            "question": q,
            "candidates": sorted(
                answers, key=lambda x: x["eval"]["andreww_model"]["score"], reverse=True
            ),
        }
    )

# write the output to a file
output_file = f"{SITE_PATH}/grouped-by-question.json"
with open(output_file, "w") as file:
    file.write(json.dumps(out, indent=4, ensure_ascii=False))

# render each answer in the template and write to a file
for idx, q in enumerate(out):
    rendered = template.render(q)
    output_file = f"{SITE_PATH}/question-{idx}.md"
    with open(output_file, "w") as file:
        file.write(rendered)
    print(f"Written {output_file}")
    print(f"Processed question {idx + 1}/{len(out)}")
