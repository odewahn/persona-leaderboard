Generate automated persona benchmarks.

To install when using `uv`:

- clone the repo
- `uv pip install -e .`

# To add a benchmark

THIS IS UGLY RIGHT NOW, BUT IT WORKS

Initialize a new benchmark project:

```bash
cd src/candidate-to-site
python init.py my-new-model
```

This will create new directories in the `candidates` and `evaluations` folders. You can then add your model inofmation to the `candidates` folder:

- Edit the `config.yaml` to specifiy the description, model name, and any tools it uses.
- Put the system prompt you used in the file `system.txt`
- Add the answers to the questions in a file like `answer-<question_number>.txt`, where `question_number` starts at zero and is the number of the question (0-19). So, you should have 20 files named `answer-0.txt`, `answer-1.txt`, ..., `answer-19.txt`.

Once you've completed the setup, you can evaluate the model by running the evaluation script:

```bash
cd src/candidate-to-site
python evaluate.py ../../candidates/my-new-model
```

This will drop 20 evaluations into the `evaluations` folder, one for each question.

Finally, generate the index page for the model by running:

```bash
cd src/candidate-to-site
python make-model-card.py ../../candidates/my-new-model
```
