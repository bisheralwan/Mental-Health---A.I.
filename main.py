import discord
import os
import requests  #allows code to make an HTTP request to get data from the API
import json  #the API returns JSON
import random
from replit import db

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "miserable", "bitter", "mournful"]

f_encouragements = [
    "You’re making a big change, and I’m so proud of you!",
    "Sending some good vibes and happy thoughts your way.",
    "I’m so sorry you’re going through this, but this too shall pass."
]

starter_words = ["Hello", "Hey", "Greetings"]

starter_words_bot = ["Hey!", "What's up?", "What's going on?"]

db["responding"] = True

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " \n- " + json_data[0]['a']
    return quote


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    msg = message.content
    if message.author == client.user:
        return

    if any(word in msg for word in starter_words):
        await message.channel.send(random.choice(starter_words_bot))

    if msg.startswith('Inspire me'):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
        options = f_encouragements
        if "encouragements" in db.keys():
            options += db["encouragements"]

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))

    if msg.startswith("Add"):
        encouraging_message = msg.split("Add ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send(
            "Thanks for teaching me some new inspirational pieces, what would I do without you?"
        )

    if msg.startswith("Respond"):
        db["responding"] = True
        await message.channel.send("Hey, I'm here!")
        await message.channel.send(random.choice(f_encouragements))
    if msg.startswith("Stop"):
        db["responding"] = False
        await message.channel.send(
            "Go ahead and rant, I'll sit back and listen (:")


client.run(os.getenv('KEY'))
