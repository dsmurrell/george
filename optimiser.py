import openai
import json
from config import c
import os
import glob

openai.api_key = c["openai_key"]

from termcolor import colored

model = "gpt-4"
# model = "gpt-3.5-turbo"


def check_description(file):
    messages = [
        {
            "role": "system",
            "content": "You rate projects for their relevance to some criteria.",
        },
        {
            "role": "user",
            "content": f"""
For this project description, can you score it for each of the following criteria from 1 to 10. Can you give respond with the score of each criteria.

- Whether it relates to population genomics
- Whether it relates to precision medicine
- Whether it involes patients

There are a few exclusion criteria, which if met, disqualifies the project from being considered and the total score should be made 0.:

- Relates to cancer

Then, can you add up the scores and give me the total score? If an exclusion is hit then the total score should be zero.

Add the total score in the following format at the end of the response:

"Total score: x"

Project description: {file}
""",
        },
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
    )

    print(colored(file, "yellow"))

    final_response = response["choices"][0]["message"]["content"]

    print(colored(final_response, "green"))


# Set your directory here
directory = "./files"

# Use glob to match the pattern '*.txt'
files = glob.glob(os.path.join(directory, "*.txt"))

for i, file in enumerate(files):
    with open(file, "r") as f:
        text = f.read()
        check_description(text)
    if i > 100:
        exit()
