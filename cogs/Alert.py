import discord
from discord.ext import commands, tasks
from datetime import datetime
import aiohttp
import time
from discord_slash import cog_ext, SlashContext

import os
from dotenv import load_dotenv

load_dotenv()

API_URL = str(os.getenv('API_URL'))
url = API_URL + 'private'


class Alert(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.alert_loop.start()

    async def _setalert(self, ctx):
        author = ctx.author_id if isinstance(ctx, SlashContext) else ctx.author.id

        await ctx.send('ใส่เวลาที่ต้องการแจ้งเตือน ในรูปแบบ ค.ศ. ตามดังนี้ `dd/mm/yyyy HH:MM` (20/09/2021 21:10)')
        set_time = await self.client.wait_for(
            'message',
            check=lambda m: m.author == ctx.author and m.channel == ctx.channel
        )
        try:
            converted_time = datetime.strptime(set_time.content, '%d/%m/%Y %H:%M')
            converted_time = round(converted_time.timestamp() * 1000)
        except ValueError:
            return await ctx.send('โปรดใส่เวลาให้ถูกต้อง!')

        await ctx.send('ใส่หัวข้อที่ต้องการแจ้งเตือน')
        subject = await self.client.wait_for(
            'message',
            check=lambda m: m.author == ctx.author and m.channel == ctx.channel
        )

        await ctx.send('ใส่คำอธิบายที่ต้องการ ไม่มีให้ใส่ -')
        notes = await self.client.wait_for(
            'message',
            check=lambda m: m.author == ctx.author and m.channel == ctx.channel
        )

        embed = discord.Embed(
            title='ข้อมูลพวกนี้ถูกต้องหรือไม่',
            description='ถ้าถูกต้องให้พิมพ์ `Yes` หรือ ไม่ถูกต้อง/ต้องการแก้ไข ให้พิมพ์ `No`',
            colour=discord.Colour.orange()
        )
        embed.add_field(name='หัวข้อ', value=subject.content)
        embed.add_field(name='เวลา', value=set_time.content)
        embed.add_field(name='คำอธิบาย', value=notes.content, inline=False)

        await ctx.send(embed=embed)
        confirmation = await self.client.wait_for(
            'message',
            check=lambda m: m.author == ctx.author and m.channel == ctx.channel
        )

        send_data = {
            "subject": subject.content,
            "notes": notes.content,
            "time": converted_time,
            "avatarurl": str(ctx.author.avatar_url),
            "username": str(ctx.author)
        }
        print(send_data)

        if confirmation.content.lower() == 'yes':
            s_time = time.time()
            msg = await ctx.send(':arrows_counterclockwise: ระบบกำลังดำเนินการ โปรดรอสักครู่...')

            async with aiohttp.ClientSession() as session:
                async with session.post(f'{url}/{author}', data=send_data) as res:
                    process_time = round((time.time() - s_time) * 1000)
                    await msg.edit(
                        content=f':white_check_mark: ระบบดำเนินการเสร็จสิ้นแล้ว ({process_time} ms)')

        elif confirmation.content.lower() == 'no':
            await ctx.send('คุณได้ทำการยกเลิกการตั้งค่าเรียบร้อยแล้ว')
        else:
            await ctx.send('คุณทำรายการไม่ถูกต้อง โปรดลองใหม่อีกครั้ง')

    async def _getalert(self, ctx):
        author = ctx.author_id if isinstance(ctx, SlashContext) else ctx.author.id

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{url}/{author}') as res:
                data = await res.json()
                print(data)
                msg = ''

                for d in data:
                    msg += f'{d["subject"]} - {d["notes"]} ({d["_id"]})\n'

                embed = discord.Embed(
                    title=f'คุณมีการแจ้งเตือนเหลืออยู่ {len(data)} ครั้ง',
                    description=msg,
                    colour=discord.Colour.blue()
                )

                await ctx.send(embed=embed)

    async def _deletealert(self, ctx, _id):
        author = ctx.author_id if isinstance(ctx, SlashContext) else ctx.author.id

        s_time = time.time()
        msg = await ctx.send(':arrows_counterclockwise: ระบบกำลังดำเนินการ โปรดรอสักครู่...')

        async with aiohttp.ClientSession() as session:
            async with session.delete(f'{url}/{author}?id={_id}'):
                process_time = round((time.time() - s_time) * 1000)
                await msg.edit(
                    content=f':white_check_mark: ระบบดำเนินการเสร็จสิ้นแล้ว ({process_time} ms)')

    @tasks.loop(seconds=60)
    async def alert_loop(self):
        print(datetime.now())

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{url}?time={round(time.time() * 1000)}') as res:
                data = await res.json()

                if data is not None:
                    for d in data:
                        d['time'] = datetime.fromtimestamp(d['time'] / 1000.0)
                        print(d)

                        if d['time'] <= datetime.now():
                            channel = self.client.get_user(int(d['userid']))
                            embed = discord.Embed(
                                title=d['subject'],
                                description=d['notes'],
                                colour=discord.Colour.green()
                            )
                            embed.set_footer(text=d['time'].strftime('%d/%m/%Y %H:%M'), icon_url=channel.avatar_url)

                            await channel.send(embed=embed)

                            async with session.delete(f'{url}/{int(d["userid"])}?id={d["_id"]}'):
                                print('Event deleted!')

    @commands.dm_only()
    @commands.command(aliases=['alert'])
    async def setalert(self, ctx):
        await self._setalert(ctx)

    @cog_ext.cog_slash(name='alert', description='สร้างการแจ้งเตือน')
    async def set_alert_slash(self, ctx: SlashContext):
        await self._setalert(ctx)

    @commands.command(aliases=['getalert', 'seealert'])
    async def get_alert(self, ctx):
        await self._getalert(ctx)

    @cog_ext.cog_slash(name='seealert', description='ดูที่ตั้งค่าแจ้งเตือนทั้งหมด')
    async def get_alert_slash(self, ctx: SlashContext):
        await self._getalert(ctx)

    @commands.command(aliases=['removealert'])
    async def delete_alert(self, ctx, _id: str):
        await self._deletealert(ctx, _id)

    @cog_ext.cog_slash(name='deletealert', description='ลบการแจ้งเตือน')
    async def delete_alert_slash(self, ctx: SlashContext, _id: str):
        await self._deletealert(ctx, _id)


def setup(client):
    client.add_cog(Alert(client))
