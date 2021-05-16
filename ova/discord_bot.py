#!/usr/bin/env python3

import os
import json
import logging
import pkg_resources

from discord.ext.tasks import loop
from discord.ext import commands

from available import get_next_available

log = logging.getLogger(__name__)

LOCATIONS = pkg_resources.resource_filename('ova', 'locations.json')

with open(LOCATIONS) as f:
    locations = json.load(f)


TOKEN = os.environ['DISCORD_TOKEN']
OTTAWA_CHANNEL = os.environ['DISCORD_OTTAWA_CHANNEL_ID']

bot = commands.Bot(command_prefix='$')

next_available = {}


@bot.command(
    help='Get next available booking dates.'
)
async def get_next(ctx):
    log.info('Getting next available date.')
    for loc in locations:
        log.info(f'Fetching dates for : {loc}.')
        new_available = get_next_available(location=loc)
        if new_available is None:
            continue

        log.info(new_available)
        try:
            formatted_message = format_message(new_available)
            if formatted_message is not None:
                await ctx.send(formatted_message)
            next_available[loc] = new_available['next_available']
        except Exception as e:
            log.error(f'Failed to send message. Error: {e}.')


def format_message(msg):
    log.info('Formatting msg.')
    message = f'> Location: `{msg["location"]}`\n'
    message += f'> Next Available Date: `{msg["next_available"]}`\n'
    message += '> Book at: https://vaccine.covaxonbooking.ca/manage'
    return message


@bot.command(
    help='Pause the alerting.'
)
async def pause(ctx):
    log.info(f'Pausing alerting due to request from: {ctx.author}.')
    get_next_available_date.cancel()


@bot.command(
    help='Starting alerts.'
)
async def start(ctx):
    log.info(f'Starting alerts due to request from: {ctx.author}.')
    get_next_available_date.start()


@loop(seconds=60*5)
async def get_next_available_date():
    log.info('Getting next available date.')

    await bot.wait_until_ready()

    channel = bot.get_channel(int(OTTAWA_CHANNEL))

    for loc in locations:
        log.info(f'Fetching dates for: {loc}.')
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


@bot.event
async def on_ready():
    log.info('Logged in as')
    log.info(bot.user.name)
    log.info(bot.user.id)


get_next_available_date.start()

bot.run(TOKEN)
