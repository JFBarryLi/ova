#!/usr/bin/env python3

import os

import aiohttp
import discord
from discord.ext.tasks import loop

from available import get_next_available

TOKEN = os.environ['DISCORD_TOKEN']
CHANNEL = os.environ['DISCORD_CHANNEL_ID']

client = discord.Client()

next_available_date = ''


@loop(seconds=15)
async def get_next_available_date():
    global next_available_date

    await client.wait_until_ready()

    channel = client.get_channel(int(CHANNEL))

    new_available_date = get_next_available()
    print(new_available_date)
    if new_available_date != next_available_date:
        await channel.send(new_available_date)
        next_available_date = new_available_date


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------')


get_next_available_date.start()

client.run(TOKEN)
