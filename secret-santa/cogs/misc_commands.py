import discord
from discord.ext import commands
import secret_santa as ss
import conditions as c
import help_commands


class misc_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(c.have_drawn_names)
    @commands.check(c.have_started)
    async def participants(self, ctx):
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            if await c.user_not_participating_in_different_server(ctx) is not True:
                return

        guild_id = ss.get_user_server_id(ctx.author)
        filename = f"{str(guild_id)}/start_message_id_{str(guild_id)}.txt"
        try:
            with open(filename, "r") as r:
                try:
                    start_message_id = int(r.readline())
                except:
                    await ctx.send(
                        "there has been a terrible error. file data has been corrupted. i have no idea what to do")
                    return
        except:
            await ctx.send("there has been a terrible error. a file containing crucial information could not be found.")
            return

        channel = discord.utils.get(self.bot.get_guild(guild_id).channels, name='general')
        messages = await channel.history(limit=123).flatten()
        cache_msg = discord.utils.find(lambda m: m.id == start_message_id, messages)

        participants_list = []
        message = "\nparticipants:\n"
        for reaction in cache_msg.reactions:
            async for participant in reaction.users():
                if participant == self.bot.user or participant in participants_list:
                    continue
                participants_list.append(participant)
                message += "    - "
                message += f"{participant.name}"
                if participant.display_name != participant.name:
                    message += f"/{participant.display_name}"
                message += "\n"
        await ctx.send(message)
    @participants.error
    async def participants_error(self, ctx, error):
        pass


    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            prefix = help_commands.get_prefix(message)
            if "prefix" in message.content and not message.content.startswith(f"{prefix}prefix") and message.author != self.bot.user:
                await message.channel.send(f"my prefix is {prefix}")
        except Exception as e:
            print("from on_message prefix func: error occured", e)


    @commands.command()
    async def repeat(self, ctx):
        def check(fix_later):
            return True

        await ctx.send("i will repeat the next thing you say back to you")
        message = await self.bot.wait_for('message', check=check)
        await ctx.send(message.content)

    @commands.command()
    async def get_emoji(self, ctx, emoji):
        await ctx.send(emoji)

def setup(bot):
    bot.add_cog(misc_commands(bot))