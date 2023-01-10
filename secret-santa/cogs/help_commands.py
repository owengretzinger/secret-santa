import asyncio
import json
import discord
from discord.ext import commands


def get_prefix(message):
    with open("prefixes.json", "r") as r:
        prefixes = json.load(r)

    try:
        if str(message.guild.id) in prefixes:
            return prefixes[str(message.guild.id)]
        else:
            return "!"
    except:
        return "!"

class help_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name="help")
    async def help(self, ctx):

        number_emojis = ["1\N{variation selector-16}\N{combining enclosing keycap}",
                         "2\N{variation selector-16}\N{combining enclosing keycap}",
                         "3\N{variation selector-16}\N{combining enclosing keycap}"]

        desc = "**react to see a specific section**\n"
        desc += f'**\n{number_emojis[0]} - admin commands**\ncommands that can only be used in a server where you\'re an admin\n'
        desc += f'**\n{number_emojis[1]} - dm commands**\ncommands that can only be used in in my dms ;)\n'
        desc += f'**\n{number_emojis[2]} - miscellaneous commands**\ncommands that anyone can use\n'

        embed = discord.Embed(colour=discord.Colour.from_rgb(250, 250, 250), timestamp=ctx.message.created_at,
                              description=desc)
        embed.set_author(name='Help', icon_url=ctx.author.avatar_url)
        message = await ctx.send(embed=embed)

        await message.add_reaction(number_emojis[0])
        await message.add_reaction(number_emojis[1])
        await message.add_reaction(number_emojis[2])

        def check(_reaction, _user):
            return _user == ctx.author and str(_reaction.emoji) in number_emojis

        try:
            _reaction, _user = await self.bot.wait_for('reaction_add', timeout=15, check=check)
        except asyncio.TimeoutError:
            await message.edit(content="your request has timed out.", embed=None)
            return
        else:
            if str(_reaction.emoji) == number_emojis[0]:
                await admin_help(ctx, message)
            elif str(_reaction.emoji) == number_emojis[1]:
                await dm_help(ctx, message)
            elif str(_reaction.emoji) == number_emojis[2]:
                await misc_help(ctx, message)


async def admin_help(ctx, message):
    prefix = get_prefix(ctx)
    desc = "**these commands can only be used in a server where you're an admin:**\n"
    desc += f'**\n{prefix}start**\nstarts a new secret santa. ' \
            'to use this command you must be an admin, and secret santa cannot already be ongoing. ' \
            'this will prompt me to ping everyone with a message to react to in order to join.\n'
    desc += f'\n**{prefix}draw**\nthis will randomly generate who everyone gets. ' \
            'it will dm everyone who is participating, and will also send a message to the main chat ' \
            'pinging everyone and listing those who are participating.\n'
    desc += f'\n**{prefix}end**\nresets the whole thing. it will get you to confirm by reacting to a message so that you don\'t ' \
            'accidentally mess everything up. only the admin who initiates the command will be the one who\'s reaction counts.\n'
    desc += f'\n**{prefix}prefix [new_prefix]**\nchange the bot command prefix to anything you\'d like.\n'
    desc += f'\n**{prefix}changechannel**\nchanges the default channel i will send messages to as a result of dm commands. ' \
            f'see the help section for dm commands for more information'

    embed = discord.Embed(colour=discord.Colour.from_rgb(250, 250, 250), timestamp=ctx.message.created_at,
                          description=desc)
    embed.set_author(name='Admin Commands', icon_url=ctx.author.avatar_url)
    await message.edit(embed=embed)


async def dm_help(ctx, message):
    prefix = get_prefix(ctx)
    desc = "**you must slide in my dms to use these commands 😉 (also, names must already have been drawn):**\n"
    desc += f'\n**{prefix}whodoihave**\nin case you had dms off initially or for whatever reason, dm me this command ' \
            'and i will send you who you have again.\n'
    desc += f'\n**{prefix}addmore [time_to_wait]**\nif the person who you have hasn\'t added enough to their wish list then dming me this ' \
            'command will prompt me to ping them in the specified channel (see help > admin commands) telling them to add more. ' \
            'put a space, then an amount of time in minutes for the bot to wait before sending the message, up to 1440 (24 hours). ' \
            'this way, the person you have won\'t be able to look at the list of people online to narrow down who has them. ' \
            'all of this is so that you can request they add more anonymously, thereby protecting your identity 🕵\n'
    desc += f'\n**{prefix}adddetail [time_to_wait]**\nsame thing as !addmore, but will tell them that their list is too vague instead. ' \
            'use this if your person isn\'t being specific enough for you to make a confident purchase.'

    embed = discord.Embed(colour=discord.Colour.from_rgb(250, 250, 250), timestamp=ctx.message.created_at,
                          description=desc)
    embed.set_author(name='DM Commands', icon_url=ctx.author.avatar_url)
    await message.edit(embed=embed)


async def misc_help(ctx, message):
    prefix = get_prefix(ctx)
    desc = "**other commands that anyone can use:**\n"
    desc += f'\n**{prefix}rules**\nshows a description of how i was designed to facilitate secret santa, and how you can best use me!\n'
    desc += f'\n**{prefix}participants**\nif you\'re too lazy to find the message listing the participants, you can use this to see that\n'
    desc += f'\n**contains: prefix**\nif you type the word "prefix" anywhere in a sentence i will respond and tell you what my prefix is ' \
            f'("{prefix}" currently). for example, type "what the heck is this bot\'s prefix again?"\n'

    embed = discord.Embed(colour=discord.Colour.from_rgb(250, 250, 250), timestamp=ctx.message.created_at,
                          description=desc)
    embed.set_author(name='Miscellaneous Commands', icon_url=ctx.author.avatar_url)
    await message.edit(embed=embed)


def setup(bot):
    bot.add_cog(help_commands(bot))