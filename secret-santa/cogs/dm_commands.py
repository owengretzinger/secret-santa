import asyncio
import discord
from discord.ext import commands
import secret_santa as ss
import conditions as c
import admin_commands


async def addcommand(ctx, time_to_wait, message):
    time_to_wait = await c.time_to_wait_error_checks(ctx, time_to_wait)
    if time_to_wait is None:
        return

    victim = ss.get_victim(ctx.author)
    if victim is None:
        await ctx.send("theres been a terrible mistake. i couldnt find who you have.")
        return

    channel = await ss.find_channel(ctx)
    if channel is None:
        return

    timer = float(time_to_wait)
    if timer > 1440:
        await ctx.send("maybe choose a value less than a day haha")
        return

    sent_message = await ctx.send(f"got it. waiting {timer:.1f} more minutes until i send the message!")
    while timer > 0:
        await asyncio.sleep(6)
        timer -= 0.1
        await sent_message.edit(content=f"got it. waiting {timer:.1f} more minutes until i send the message!")

    await channel.send(f"{victim.mention} {message}")
    await sent_message.edit(content=f"message sent!")

class events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(c.have_started)
    @commands.check(c.have_drawn_names)
    @commands.check(c.is_in_dm)
    async def whodoihave(self, ctx):
        victim = ss.get_victim(ctx.author)
        if victim is None:
            await ctx.send("theres been a terrible mistake. i couldnt find who you have.")
            return
        await admin_commands.sendDM(ctx, victim)
    @whodoihave.error
    async def whodoihave_error(self, ctx, error):
        pass

    @commands.command()
    @commands.check(c.have_started)
    @commands.check(c.have_drawn_names)
    @commands.check(c.is_in_dm)
    async def addmore(self, ctx, time_to_wait=None):
        await addcommand(ctx, time_to_wait, "put more stuff on your list please 🙂")
    @addmore.error
    async def addmore_error(self, ctx, error):
        pass

    @commands.command()
    @commands.check(c.have_started)
    @commands.check(c.have_drawn_names)
    @commands.check(c.is_in_dm)
    async def adddetail(self, ctx, time_to_wait=None):
        await addcommand(ctx, time_to_wait, "bro fix ur list dude, it's too vague")
    @addmore.error
    async def addmore_error(self, ctx, error):
        pass

def setup(bot):
    bot.add_cog(events(bot))