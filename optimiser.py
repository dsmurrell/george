import openai
import json
from config import c
import os
import glob

openai.api_key = c["openai_key"]

from termcolor import colored

model = "gpt-4"


def check_description(file):
    messages = [
        {
            "role": "system",
            "content": "You rate projects for their relevance to some criteria.",
        },
        {
            "role": "user",
            "content": f"""
For this project description, can you score it for each of the following from 1 to 10.

- Whether it relates to population genomics
- Whether it relates to precision medicine
- Whether it involes patients

Then, can you add up the scores and give me the total score?

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
    if i > 10:
        exit()
