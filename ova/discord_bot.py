#!/usr/bin/env python3

import os
import json
import logging
import pkg_resources

import discord
from discord.ext.tasks import loop

from available import get_next_available

log = logging.getLogger(__name__)

LOCATIONS = pkg_resources.resource_filename('ova', 'locations.json')

with open(LOCATIONS) as f:
    locations = json.load(f)


TOKEN = os.environ['DISCORD_TOKEN']
OTTAWA_CHANNEL = os.environ['DISCORD_OTTAWA_CHANNEL_ID']

client = discord.Client()

next_available = {}


def format_message(msg):
    msg = f'> Location: `{msg["location"]}`, Next Available Date: `{msg["next_available"]}`\n'
    msg += '> Book at: https://vaccine.covaxonbooking.ca/manage'
    return msg


@loop(seconds=60*10)
async def get_next_available_date():
    log.info('Getting next available date.')

    await client.wait_until_ready()

    channel = client.get_channel(int(OTTAWA_CHANNEL))

    for loc in locations:
        new_available = get_next_available(location=loc)
        if new_available is None:
            continue

        log.info(new_available)
        if loc in next_available:
            if new_available['next_available'] != next_available[loc]:
                try:
                    formatted_message = format_message(new_available)
                    if formatted_message is not None:
                        await channel.send(formatted_message)
                    next_available[loc] = new_available['next_available']
                except Exception as e:
                    log.error(f'Failed to send message. Error: {e}.')
        else:
            try:
                formatted_message = format_message(new_available)
                if formatted_message is not None:
                    await channel.send(formatted_message)
                next_available[loc] = new_available['next_available']
            except Exception as e:
                log.error(f'Failed to send message. Error: {e}.')


@client.event
async def on_ready():
    log.info('Logged in as')
    log.info(client.user.name)
    log.info(client.user.id)


get_next_available_date.start()

client.run(TOKEN)
