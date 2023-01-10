import random
import discord
import asyncio
import csv
import json
import os
from discord.ext import commands


intents = discord.Intents.default()
intents.members = True
intents.guilds = True

async def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or("!")(bot, message)

    with open("prefixes.json", "r") as r:
        prefixes = json.load(r)

    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or("!")(bot, message)

    new_prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(new_prefix)(bot, message)

client = commands.Bot(command_prefix=get_prefix, intents = intents)
client.remove_command('help')

global_participants = {}

@client.event
async def on_ready():
    global global_participants
    print('bot is ready')
    await client.change_presence(activity=discord.Game('delivering presents 🎁'))

    global_participants.clear()
    try:
        with open("global_participants.txt", "r") as r:
            r.readline()
            for line in r.readlines():
                line = line.strip()
                user_info = line.split(",")
                guild_id = int(user_info[1])
                global_participants[user_info[0]] = guild_id
    except:
        pass

    #print(os.path.isdir('./test'))

def get_user_server_id(user):
    global global_participants
    identifier = f"{user.name}#{user.discriminator}"
    if identifier in global_participants:
        return global_participants[identifier]
    else:
        return -1

def get_victim(person):
    guild_id = str(get_user_server_id(person))
    filename = f"{guild_id}/TOP_SECRET_{guild_id}.txt"
    with open(filename, "r") as r:
        r.readline()
        reader = csv.reader(r)
        for line in reader:
            if str(person) != line[0]:
                continue

            victim_file = line[1].split("#")
            victim_name = victim_file[0]
            victim_discrim = victim_file[1]
            victim = discord.utils.get(client.get_guild(get_user_server_id(person)).members, name=victim_name, discriminator=victim_discrim)
            return victim
        return "error"

async def find_channel(ctx):
    guild_id = 0
    try:
        guild_id = ctx.guild.id
    except:
        try:
            guild_id = get_user_server_id(ctx.author)
        except:
            await ctx.send("could not find your server, this is very bad")
    finally:
        filename = f"{guild_id}/channel_name_{guild_id}.json"
        guild = client.get_guild(guild_id)
        try:
            with open(filename, "r") as r:
                channel_name = json.load(r)[str(guild_id)]
                channel = discord.utils.get(guild.channels, name=channel_name)
        except:
            await ctx.send("admins have not specified a channel for these messages to go to; i will send it to \#general")
            channel = discord.utils.get(guild.channels, name='general')
        if channel is None:
            await ctx.send("your server also doesn't have a \#general channel. "
                           "an admin may need to manually set the default channel for me to send messages to by using the **!changechannel** command.")
            return
        return channel

@client.command()
@commands.is_owner()
async def reload(ctx, _cog):
    try:
        client.unload_extension(f"cogs.{_cog}")
        client.load_extension(f"cogs.{_cog}")
        await ctx.send(f"{_cog} was reloaded.")
    except Exception as e:
        print(f"{_cog} could not be reloaded")
        raise e


@client.event
async def on_guild_join(guild):
    channel = discord.utils.get(guild.channels, name='general')
    if channel is None:
        channel = discord.utils.get(guild.channels, name='bot-commands')
    if channel is None:
        channel = guild.channels[0]
    try:
        await channel.send('hey! thanks for adding me to your server - my default prefix is "!". '
                     'to see how secret santa is supposed to be run with me, check out "!rules". '
                     'also, make sure to check out "!help" as well to see all the different commands '
                     'you can use with me. have fun! :)')
    except:
        print("couldnt find da channel ;(")




#called when someone tries to use a command that doesnt exist
# @client.event
# async def on_command_error(ctx, error):
#     await ctx.send(f'{error}. Use !help to see a list of commands.')



for cog in os.listdir("cogs"):
    if cog.endswith(".py") and not cog.startswith("_"):
        try:
            cog = f'cogs.{cog.replace(".py", "")}'
            client.load_extension(cog)
        except Exception as e:
            print(f"{cog} cannot be loaded:")
            raise e

client.run('token')
