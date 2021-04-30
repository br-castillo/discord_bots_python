import discord
from discord.ext import commands, tasks
import datetime
from ruamel.yaml import YAML
import os
import requests
import bs4
import logging
import random
from itertools import cycle
import asyncio
import re

yaml = YAML()

with open("./config.yml", "r", encoding = "utf-8") as file:
	config = yaml.load(file)

# client = discord.Client()
client = commands.Bot(command_prefix = config["Prefix"], 
                   description = "Buzzy Bot", 
                   case_insensitive=True)

'''
Bot Properties being read from Config.yml
'''

# Channel ID's
log_channel_id = config["Log Channel ID"]
main_channel_id = config["Main Channel ID"]

# Embedded Message Colors
client.embed_green = discord.Color.from_rgb(37, 225, 45)
client.embed_red = discord.Color.from_rgb(255, 0, 0)
client.embed_white = discord.Color.from_rgb(255, 255, 255)
client.embed_black = discord.Color.from_rgb( 0, 0, 0)
client.embed_lightblue = discord.Color.from_rgb(0, 175, 225)

# Embedded Message Properties
client.footer_text = config["Embed Settings"]["Footer"]["Text"]
client.newspaper_icon = config["Embed Settings"]["Footer"]["Icon URL"]

# Playing Status and Command Prefix setup
client.prefix = config["Prefix"]
client.playing_status = config["Playing Status"].format(prefix = client.prefix)

client.TOKEN = os.getenv(config["Bot Token Variable Name"])
token = client.TOKEN

'''
Bot event on start-up
'''

@client.event
async def on_ready():
    print(f"I am logged in as {client.user} and connected to Discord! ID: {client.user.id}")

    game = discord.Game(name = "==help")
    await client.change_presence(activity = game)
    
    embed = discord.Embed(
    	title = f"{client.user.name} Online!" , 
    	color = client.embed_green ,
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        )

    embed.set_footer(
        text = client.footer_text,
        icon_url = client.newspaper_icon)

    print('-----')
    client.log_channel = client.get_channel(log_channel_id)
    await client.log_channel.send(embed = embed)

'''
Restart Command
'''

@client.command(name = "restart" , aliases = ["r"], help = "Restarts the bot.")
async def restart(ctx):
    embed = discord.Embed(
        title = f"{client.user.name} Restarting!" ,
        color = client.embed_white , 
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        )

    embed.set_author(
        name = ctx.author.name ,
        icon_url = ctx.author.avatar_url
        )

    embed.set_footer(
        text = client.footer_text,
        icon_url = client.newspaper_icon
        )

    await client.log_channel.send(embed = embed)
    await ctx.message.add_reaction("✅")
    await client.close()

'''@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))'''

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('==hello'):
        await message.channel.send('Hello!')

client.run(#discord token here)