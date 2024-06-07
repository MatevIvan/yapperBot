# import libraries
import discord
import os
import random
from discord.ext import commands
from ec2_metadata import ec2_metadata

#enable necessary intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

#load token from environmental variables on the os
token = str(os.getenv('yapper_token'))
#create the Discord bot
client = commands.Bot(command_prefix="!",intents=intents)

#add an event handler for when the bot is ready
@client.event
async def on_ready():
  #print in console confiming the bot has logged on
  print("logged in as a bot {0.user}".format(client))

#initialize variables for the game
playGame = False
gameQuestionAsked = False

#create an event handler for incomming messages
@client.event
async def on_message(message):
  #this will format the bot's name
  #Bot names have some numbers after #
  username = str(message.author).split("#")[0]

  #This format's usernames to simplify  
  try:
    username = username.split("_")[0]
  except Exception as e:
    pass

  channel = str(message.channel)
  userMessage = str(message.content)

  #logs both the user input and the bot output
  print(f"{username}: '{userMessage}' in {channel}")

  #ignore if the message came from the bot (itself)
  if message.author == client.user:
    return
  
  #check if message is in 'random'
  if channel == "random":
    #Make the global variables usable
    global playGame
    global gameQuestionAsked

    #handle simple greetings
    if userMessage.lower() == "hello" or userMessage.lower() == "hi":
      await message.channel.send(f'Hello there {username}')
      await message.channel.send('Would you like to play a game of Rock, Paper, Scissors?')
      gameQuestionAsked = True
      return
    #handle simple salutation
    if userMessage.lower() == "bye" or userMessage.lower() == "good bye":
      await message.channel.send(f'See you later, {username}')
    #handle request about ec2 information
    if userMessage.lower() == "tell me about my server!":
      await message.channel.send(f'This is my ec2 metadata for my region: {ec2_metadata.region}')
      await message.channel.send(f'This is my ec2 metadata for my instance: {ec2_metadata.instance_id}')

    #checks to see if game question has been asked
    if gameQuestionAsked:
      #if player agrees to play, set playGame to true and state directions
      if userMessage.lower() == "yes":
        playGame = True
        await message.channel.send("Please enter rock, paper, or scissors.")
      #if player answers anything other than 'yes' end the game
      elif userMessage.lower() != "yes" :
        playGame = False
        await message.channel.send("Say 'hi' to me if you want to play later.")
      #set game question to false so that the directions are sent over and over again
      gameQuestionAsked = False
  
    #Handle game logic if player wants to play the game
    if playGame:
      #create array with possible choices and randomly choose one
      choices = ["rock","paper","scissors"]
      botChoice = random.choice(choices)
      userMessage = userMessage.lower()

      #Compare user choices with bot's choices
      #Always set playGame to false because the game ends after one round
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

      #Ask if player wants to play again
      if not playGame:
        await message.channel.send("Would you like to play again?")
        #setting this to true returns the user take to the directions
        gameQuestionAsked = True

#initialize the bot with the provided token
client.run(token)