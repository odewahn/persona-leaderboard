import requests
import json

URL = "http://localhost:8000/api/blocks"
FN = "out.json"

# Grab the data from the API
response = requests.get(URL)
if response.status_code == 200:
    data = response.json()

# output the "content" field of each block into a list
sample_content = [block["content"] for block in data["blocks"]]

# write the sample content to a file as a json array
with open(FN, "w") as f:
    json.dump(sample_content, f, indent=4)
