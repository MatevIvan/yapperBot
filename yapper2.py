import discord
import os
import random
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

load_dotenv()
token = str(os.getenv('yapper_token'))
print("this is my token: " + token)
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
  print("logged in as a bot {0.user}".format(client))

@client.event
async def on_message(message):
  username = str(message.author)
  channel = str(message.channel)
  userMessage = str(message.content)

  print(f'Message {userMessage} by {username} in {channel}')

  if message.author == client.user:
    return
  
  if channel == "random":
    if userMessage.lower() == "hello" or userMessage.lower() == "hi":
      await message.channel.send(f'Hello there {username}')
      return
    elif userMessage.lower() == "bye":
      await message.channel.send(f'See you later, {username}')
    elif userMessage.lower() == "tell me a joke": 
      jokes = [" Can someone please shed more light on how my lamp got stolen?", 
                     "Why is she called llene? She stands on equal legs.", 
                     "What do you call a gazelle in a lions territory? Denzel."] 
      await message.channel.send(random.choice(jokes)) 
    else :
      await message.channel.send("End of the code")

@client.command()
async def ping(ctx):
  await ctx.send('Pong!')

client.run(token)