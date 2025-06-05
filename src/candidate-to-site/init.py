import cookiecutter
import os
from cookiecutter.main import cookiecutter
import argparse


script_path = os.path.dirname(os.path.realpath(__file__))


# get first argument to use as the answers directory
parser = argparse.ArgumentParser(description="Initialize a new model to evaluate")
parser.add_argument(
    "name",
    type=str,
    help="Model name",
)
args = parser.parse_args()
print(f"Arguments received: {args}")

print(f"Fetching answer files from directory: {args.name}")


cookiecutter(
    os.path.join(script_path, "project_template/"),
    no_input=True,
    extra_context={"name": args.name},
    output_dir="../../candidates",
    overwrite_if_exists=True,
)

# Create the directory in the evaluations folder if it doesn't exist
evaluations_dir = os.path.join(script_path, "../../evaluations", args.name)
if not os.path.exists(evaluations_dir):
    os.makedirs(evaluations_dir)
