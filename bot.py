import os
import time

import discord
from datetime import datetime
from discord.ext import commands
from discord_slash import SlashCommand

from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(
    command_prefix=';', intents=discord.Intents.all(),
    description='DM me to get started! also Slash Commands are available.',
    case_insensitive=True,
)
slash = SlashCommand(client, override_type=True, sync_on_cog_reload=True)


def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
            print(f'cogs.{filename[:-3]} loaded!')


def run():
    dts = datetime.now().second
    print(dts)

    if dts != 0:
        time.sleep(1)
        run()
    else:
        @slash.slash(name='ping')
        async def ping(ctx):
            await ctx.send('Pong!')

        load_cogs()
        client.run(os.getenv('TOKEN'))


if __name__ == '__main__':
    run()
