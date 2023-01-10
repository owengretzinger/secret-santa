import json
import csv
import asyncio
import random
import os
import discord
from discord.ext import commands
import secret_santa as ss
import conditions as c


async def sendDMs(participants_list):
    matches = {}

    # drawing names
    all_people = participants_list.copy()
    for participant in participants_list:
        person = get_name(participant, all_people)
        if person == "impossible":
            matches = await sendDMs(participants_list)
            return matches

        all_people.remove(person)
        print(f"{participant.name} got {person.name}")
        # if we are down to the last person and the only possible person they could get is themself, restart

        matches[str(participant)] = person

    # sending DMs
    for participant in participants_list:
        await sendDM(participant, matches[str(participant)])

    return matches

async def sendDM(santa, victim):
    message = "you are "
    message += f"{victim.name}"
    if victim.display_name != victim.name:
        message += f"/{victim.display_name}"
    message += "'s secret santa!"
    # let them know about commands i'll add later
    await santa.send(message)

def get_name(user, choices):
    person = random.choice(choices)
    if person is user:
        if len(choices) == 1:
            print("the only option for the last person is themself. restarting name draw.")
            return "impossible"
        person = get_name(user, choices)
    return person

def save_matches_to_file(guild_id, matches):
    guild_id = str(guild_id)
    filename = f"{guild_id}/TOP_SECRET_{guild_id}.txt"
    with open(filename, "w", newline="") as w:
        writer = csv.writer(w)
        writer.writerow(["santa", "their victim"])
        for person in matches:
            match = matches[person]
            writer.writerow([person, match])

class admin_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(c.not_in_dm)
    @commands.check(c.has_admin_perms)
    async def prefix(self, ctx, *, new_prefix):
        with open("prefixes.json", "r") as r:
            prefixes = json.load(r)

        prefixes[str(ctx.guild.id)] = new_prefix
        await ctx.send(f'new prefix is "{new_prefix}"')

        with open("prefixes.json", "w") as w:
            json.dump(prefixes, w, indent=4)
    @prefix.error
    async def prefix_error(self, ctx, error):
        pass

    @commands.command()
    @commands.check(c.not_in_dm)
    @commands.check(c.has_admin_perms)
    async def changechannel(self, ctx, new_channel_name):
        channel = discord.utils.get(ctx.guild.channels, name=new_channel_name)
        if channel is None:
            await ctx.send(f"channel \"{new_channel_name}\" doesn't exist.")
            return

        channel_preference = {str(ctx.guild.id): new_channel_name}
        filename = f"{ctx.guild.id}/channel_name_{ctx.guild.id}.json"
        with open(filename, "w") as w:
            json.dump(channel_preference, w, indent=4)
        #channel = channel
        await ctx.send(f"success! dm commands such as addmore and adddetail will now go to {new_channel_name}.")
    @changechannel.error
    async def changechannel_error(self, ctx, error):
        pass


    @commands.command()
    @commands.check(c.user_not_participating_in_different_server)
    @commands.check(c.has_admin_perms)
    @commands.check(c.not_in_dm)
    @commands.check(c.not_started)
    async def start(self, ctx):
        start_message = await ctx.send("everyone secret santa has been started! react to this message to join! :santa:")
        await start_message.add_reaction(emoji='🎅')
        await start_message.pin()
        start_message_id = start_message.id

        #s.started = True
        guild_id = str(ctx.guild.id)
        try:
            os.mkdir(guild_id)
        except:
            pass
        filename = f"{guild_id}/state_{guild_id}.txt"
        with open(filename, "w") as w:
            w.write("started=True,names_drawn=False")

        start_message_info = {ctx.channel.name: str(start_message_id)}
        filename = f"{guild_id}/start_message_id_{guild_id}.json"
        with open(filename, "w") as w:
            json.dump(start_message_info, w, indent=4)
    @start.error
    async def start_error(self, ctx, error):
        pass


    @commands.command()
    @commands.check(c.user_not_participating_in_different_server)
    @commands.check(c.has_admin_perms)
    @commands.check(c.not_in_dm)
    @commands.check(c.have_started)
    @commands.check(c.not_drawn_names)
    async def draw(self, ctx):

        try:
            guild_id = ctx.guild.id
            filename = f"{guild_id}/start_message_id_{guild_id}.json"
            with open(filename, "r") as r:
                channel_info = json.load(r)

            channel_name = list(channel_info.keys())[0]
            channel = discord.utils.get(ctx.guild.channels, name=channel_name)
            start_message_id = int(channel_info[channel_name])

            messages = await channel.history(limit=200).flatten()
            cache_msg = discord.utils.find(lambda m: m.id == start_message_id, messages)
            message = "everyone names have been drawn!\nparticipants:\n"
            participants_list = []
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
        except Exception as e:
            await ctx.send("i couldn't find the \"secret santa has been started\" message. either someone deleted it "
                           "or there has been over 200 messages sent since it was."
                           "(this probably means you will have to do !end and restart the whole thing)")
            raise e

        # error messages if < 3 people are participating
        if len(participants_list) == 0:
            await ctx.send("nobody even joined bro are u really trying to break me rn?")
            return
        if len(participants_list) == 1:
            await ctx.send("bro you need more than 1 person to do secret santa r u dumb 😂😂😂")
            return
        if len(participants_list) == 2:
            await ctx.send("really? secret santa with 2 people? that wouldn't be very secret, now would it?")
            return

        # add to global participants (literally)
        for participant in participants_list:
            for global_participant in ss.global_participants:
                if str(participant) == str(global_participant):
                    name = global_participant.split("#")[0]
                    discrim = global_participant.split("#")[1]
                    user = discord.utils.get(self.bot.get_guild(ss.global_participants[global_participant]).members,
                                             name=name, discriminator=discrim)
                    await ctx.send(
                        f"{user.mention} is already playing secret santa in another server. this is ILLEGAL as this would break dm commands."
                        f" either make sure to end the game in the other server, or just make a new account and join with that one.")
                    return
            ss.global_participants[str(participant)] = ctx.guild.id
        with open("global_participants.txt", "w", newline="") as w:
            writer = csv.writer(w)
            writer.writerow(["participant", "guild_id"])
            for participant in ss.global_participants:
                writer.writerow([participant, ss.global_participants[participant]])

        await ctx.send(message)

        matches = await sendDMs(participants_list)
        save_matches_to_file(ctx.guild.id, matches)

        # set state
        guild_id = str(ctx.guild.id)
        filename = f"{guild_id}/state_{guild_id}.txt"
        with open(filename, "w") as w:
            w.write("started=True,names_drawn=True")

        # for participant in participants_list:
        #     print("participant: ", participant)
        # for global_participant in ss.global_participants:
        #     print("global_participant: ", global_participant)
    @draw.error
    async def draw_error(self, ctx, error):
        pass

    @commands.command()
    @commands.check(c.user_not_participating_in_different_server)
    @commands.check(c.has_admin_perms)
    @commands.check(c.not_in_dm)
    async def end(self, ctx):

        message = await ctx.send("are you sure? react to this message with ❌ within the next 10 seconds to confirm.")
        await message.add_reaction(emoji='❌')

        def check(_reaction, _user):
            return _user == ctx.author and str(_reaction.emoji) == '❌'

        try:
            _reaction, _user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(
                "10 seconds is up. if you meant to react but ran out of time, you will have to do !end again.")
            return
        else:
            try:
                with open("global_participants.txt", "r") as r:
                    r.readline()
                    for line in r.readlines():
                        user = line.split(",")[0]
                        ss.global_participants.pop(user)
            except:
                pass
            with open("global_participants.txt", "w", newline="") as w:
                writer = csv.writer(w)
                writer.writerow(["participant", "guild_id"])
                for participant in ss.global_participants:
                    writer.writerow([participant, ss.global_participants[participant]])

            # s.started = False
            # s.names_drawn = False
            guild_id = str(ctx.guild.id)
            filename = f"{guild_id}/state_{guild_id}.txt"
            with open(filename, "w") as w:
                w.write("started=False,names_drawn=False")

            try:
                os.rename(f"{guild_id}/TOP_SECRET_{guild_id}.txt",
                          f"{guild_id}/TOP_SECRET_ARCHIVED_{guild_id}_{random.randrange(0, 1000000)}.txt")
            except:
                try:
                    os.rename(f"{guild_id}/TOP_SECRET_{guild_id}.txt",
                              f"{guild_id}/TOP_SECRET_ARCHIVED_{guild_id}_{random.randrange(0, 1000000)}.txt")
                except:
                    pass

            await ctx.send("ok, secret santa has been fully reset.")
        #await asyncio.sleep(2)

        # cache_msg = discord.utils.get(self.bot.cached_messages, id=message.id)
        # confirm = False
        # for reaction in cache_msg.reactions:
        #     if reaction.emoji != "❌":
        #         continue
        #     async for user in reaction.users():
        #         if user != ctx.author:
        #             continue
        #         confirm = True
    @end.error
    async def end_error(self, ctx, error):
        pass


def setup(bot):
    bot.add_cog(admin_commands(bot))