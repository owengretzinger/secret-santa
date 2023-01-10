import discord
import secret_santa as ss
from discord.ext import commands



async def user_not_participating_in_different_server(ctx):
    if str(ctx.author) in ss.global_participants:
        if ctx.guild.id != ss.global_participants[str(ctx.author)]:
            await ctx.send(
                "you\'re already participating in a different server... this is ILLEGAL as this would break dm commands."
                f" either make sure to end the game in the other server, or just make a new account and join with that one.")
            return False
    return True


async def has_admin_perms(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        return True
    if ctx.message.author.guild_permissions.administrator:
        return True
    else:
        await ctx.send("oops! you either dont have admin perms, loser.")
        return False


async def is_in_dm(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        return True
    else:
        await ctx.send("man did you really ask that in front of the whole server? slide in my DMs rn")
        return False
async def not_in_dm(ctx):
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        return True
    else:
        await ctx.send("stop tryna slide in my DMs man, that command can only be used in a server")
        return False


def is_started(ctx):
    guild_id = -1
    filename = ""
    try:
        filename = f"{ctx.guild.id}/state_{ctx.guild.id}.txt"
    except:
        try:
            guild_id = ss.get_user_server_id(ctx.author)
            filename = f"{guild_id}/state_{guild_id}.txt"
        except:
            try:
                guild_id = ss.get_user_server_id(ctx.author)
                filename = f"{guild_id}/state_{guild_id}.txt"
            except:
                return False
    finally:
        if guild_id == -1:
            return False
        try:
            with open(filename, "r") as r:
                states = r.readline().split(",")
                return states[0].split("=")[1] == "True"
        except Exception as e:
            raise e
async def have_started(ctx):
    if is_started(ctx):
        return True
    else:
        await ctx.send(
                "oops! you never started secret santa. maybe try growing a few more brain cells then try that button again LOL")
        return False
async def not_started(ctx):
    if not is_started(ctx):
        return True
    else:
        await ctx.send("oops! a game has already been started, idiot")
        return False


def are_names_drawn(ctx):
    guild_id = -1
    filename = ""
    try:
        filename = f"{ctx.guild.id}/state_{ctx.guild.id}.txt"
    except:
        try:
            guild_id = ss.get_user_server_id(ctx.author)
            filename = f"{guild_id}/state_{guild_id}.txt"
        except:
            try:
                guild_id = ss.get_user_server_id(ctx.author)
                filename = f"{guild_id}/state_{guild_id}.txt"
            except:
                return False
    finally:
        if guild_id == -1:
            return False
        try:
            with open(filename, "r") as r:
                states = r.readline().split(",")
                return states[1].split("=")[1] == "True"
        except Exception as e:
            raise e
async def have_drawn_names(ctx):
    if are_names_drawn(ctx.author):
        return True
    else:
        await ctx.send("names havent even been drawn yet how you tryna do that 😂😂😂")
        return False
async def not_drawn_names(ctx):
    if not are_names_drawn(ctx.author):
        return True
    else:
        await ctx.send("oops! names have already been drawn, idiot.")
        return False


async def time_to_wait_error_checks(ctx, time_to_wait):
    if time_to_wait is None:
        await ctx.send("if i sent the message right away, your person could look at the list of online people and "
                       "narrow down who could have them!\ntry that command again but do ```!addmore [time_to_wait]```"
                       "where time_to_wait is how long i should wait in minutes before sending the message.")
        return
    try:
        time_to_wait = float(time_to_wait)
    except:
        await ctx.send(
            f"yeah? you want me to wait {time_to_wait} minutes? ya lemme convert that to a number real quick "
            f"(*maybe consider not making my job a nightmare next time.*)")
        return
    return time_to_wait

class conditions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def state(self, ctx):
        await ctx.send(f"started: {is_started(ctx.author)}, names drawn: {are_names_drawn(ctx.author)}")

def setup(bot):
    bot.add_cog(conditions(bot))