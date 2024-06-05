import discord
import os
import random
from dotenv import load_dotenv
from discord.ext import commands
from ec2_metadata import ec2_metadata

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

load_dotenv()
token = str(os.getenv('yapper_token'))
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
  print("logged in as a bot {0.user}".format(client))

playGame = False
gameQuestionAsked = False

print(f'This is my ec2 metadata for my region: {ec2_metadata.region}')
print(f'This is my ec2 metadata for my instance: {ec2_metadata.instance_id}')

@client.event
async def on_message(message):
  username = str(message.author)
  channel = str(message.channel)
  userMessage = str(message.content)

  print(f'Message {userMessage} by {username} in {channel}')

  if message.author == client.user:
    return
  
  if channel == "random":
    global playGame
    global gameQuestionAsked

    if userMessage.lower() == "hello" or userMessage.lower() == "hi":
      await message.channel.send(f'Hello there {username}')
      await message.channel.send('Would you like to play a game of Rock, Paper, Scissors?')
      gameQuestionAsked = True
      return
    if userMessage.lower() == "bye":
      await message.channel.send(f'See you later, {username}')

    if gameQuestionAsked:
      if userMessage.lower() == "yes":
        playGame = True
        await message.channel.send("Please enter rock, paper, or scissors.")
      elif userMessage.lower() != "yes" :
        playGame = False
        await message.channel.send("Say 'hi' to me if you want to play later.")
      gameQuestionAsked = False
  
    if playGame:
      choices = ["rock","paper","scissors"]
      userMessage = userMessage.lower()
      botChoice = random.choice(choices)

      if userMessage == botChoice:
        await message.channel.send("Its a tie!")
        playGame = False

      elif userMessage == "rock":
        if botChoice == "paper":
          await message.channel.send("I won!")
          playGame = False
        else :
          await message.channel.send("You won this time.")
          playGame = False

      elif userMessage == "paper":
        if botChoice == "scissors":
          await message.channel.send("I won!")
          playGame = False
        else :
          await message.channel.send("You won this time.")
          playGame = False
      
      elif userMessage == "scissors":
        if botChoice == "rock4":
          await message.channel.send("I won!")
          playGame = False
        else :
          await message.channel.send("You won this time.")
          playGame = False
      else :
        print("here")

      if not playGame:
        await message.channel.send("Would you like to play again?")
        gameQuestionAsked = True


@client.command()
async def ping(ctx):
  await ctx.send('Pong!')

client.run(token)