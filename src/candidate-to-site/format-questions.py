# read the questions from the file
with open("../questions.txt", "r") as file:
    questions = file.readlines()

questions = [question.strip() for question in questions if question.strip()]

# Print the header
print("|idx| Question |")
print("|---|----------|")
for idx, q in enumerate(questions):
    print(f"|{idx}| {q} |")  # Print each question in the desired format
