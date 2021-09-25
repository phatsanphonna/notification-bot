import discord
from discord.ext import commands


class Client(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="DM me to get started! also Slash Commands are available."
            )
        )


def setup(client):
    client.add_cog(Client(client))
