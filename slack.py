import random
import threading

import time

from config import c

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from optimiser import get_drugs_and_genes, optimise_template, refine_email

# Initialize your app with your token and signing secret
app = App(token=c["slack_bot_token"])


def get_random_response():
    responses = [
        "Drafting your email masterpiece now! 🎨",
        "Starting to compose the perfect email for you... 📝",
        "Putting my wordsmith skills to work on your email... ✍️",
        "Let me roll up my sleeves and begin writing your email... 🧵",
        "Initiating the email-writing process just for you... 🖋️",
        "Now weaving together the right words for your email... 🧶",
        "Working on crafting a well-structured email for you... 🗂️",
        "Getting down to business and writing your email... 💼",
        "Starting the creative process to write your email... 🌈",
        "I'm on it! Just beginning to draft your email... ⏳",
        "Allow me a moment to start constructing your email... 🏗️",
        "Hold tight! I'm writing the best email for you now... 🎢",
        "Beginning to formulate a well-written email for you... 🧪",
        "Now piecing together your professionally crafted email... 🧩",
        "Kicking off the email writing process right away! 🏁",
        "Just starting to put pen to paper for your email... 🖊️",
        "Beginning my journey to craft the perfect email for you... 🧭",
        "Now launching the process of composing your email... 🛫",
        "Starting to explore my writing skills for your email... 🏞️",
        "Initiating the hunt for the best words for your email... 🐾",
        "Setting off to create a well-written email for you... ⛵",
        "Just beginning my investigation to draft your email... 🕵️",
        "Commencing the creative process for your email... 🌄",
        "Now diving into the task of writing your email... 🏊",
        "Starting my mission to craft the most effective email... 🚁",
        "Just initiating the process of composing your email... 🎢",
        "Ready, set, write! Crafting your email now... 🚦",
        "Now beginning to navigate the art of writing your email... 🗺️",
        "Setting sail on my journey to write your email... ⛵",
        "Starting to probe my writing talents for your email... 🌌",
        "Now launching my quest to create your perfect email... 🚀",
        "Embarking on my mission to write the best email for you... 🚂",
        "Initiating the expedition to draft your ideal email... 🏜️",
        "Commencing the quest for the ultimate email content... 🏰",
        "Just starting to sift through my ideas for your email... 🏗️",
        "Now entering the writing mode to craft your email... 🚪",
        "Initiating the operation to create the ideal email... 🎯",
        "Kicking off the process of writing your perfect email... ⚽",
        "Launching my investigation to compose your email... 🚀",
        "Beginning my search for the most fitting words for your email... 🌠",
        "Ready to roll! Starting to write your email now... 🚴",
        "Jumping into action to draft the perfect email for you... 🤸",
        "Setting out on my mission to craft your ideal email... 🚶‍♀️",
        "Now initiating the process of writing your email... 🕰️",
        "Just starting to assemble the best email for you... 🧩",
    ]
    return random.choice(responses)


# Listen for messages in the Slack channel
@app.event("app_mention")
def command_handler(body, say):
    handle_message(body, say, "app_mention")


# Listen for direct messages
@app.event("message")
def dm_handler(body, say):
    print("got handle DM")
    event = body.get("event", {})
    channel_type = event.get("channel_type")

    if channel_type == "im":
        handle_message(body, say, "message")


def handle_message(body, say, type):
    # Extract the message text from the event payload
    print("got handle message")
    query = body["event"]["text"]

    company = query

    say(get_random_response())

    # You can add any additional filtering or conditions to respond to specific messages here.
    d = get_drugs_and_genes(company)

    email = optimise_template(company, d)

    refined_email = refine_email(email)

    # Reply in Slack with the message.
    say(refined_email)


def start_slack_bot():
    handler = SocketModeHandler(app, c["slack_app_token"])
    handler.start()


# Start the Slack bot in a separate thread
bot_thread = threading.Thread(target=start_slack_bot, daemon=True)
bot_thread.start()

# Keep the main thread running
while True:
    time.sleep(10)  # Sleep for 10 seconds
