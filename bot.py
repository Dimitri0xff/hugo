import argparse
import logging

import discord

from bot import bot_main

if __name__ == '__main__':
    client = discord.Client()


@client.event
async def on_ready():
    logger = logging.getLogger(__name__)
    logger.info('Logged in as ' + client.user.name)


@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        await client.send_message(message.channel, 'Hello')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Discord bot')
    #parser.add_argument('integers', metavar='t', nargs='?', help='Specify ..')

    args = parser.parse_args()

    bot_main.run(client, args)
