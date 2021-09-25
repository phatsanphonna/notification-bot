import os
import discord
from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Client is online!')

    @commands.command()
    @commands.is_owner()
    async def reload(self, _):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.client.unload_extension(f'cogs.{filename[:-3]}')
                self.client.load_extension(f'cogs.{filename[:-3]}')
                print(f'cogs.{filename[:-3]} reloaded!')

    @commands.command()
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send('Logout!')
        await self.client.logout()


def setup(client):
    client.add_cog(Owner(client))
