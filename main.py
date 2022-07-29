import discord
from discord.ext import commands
import datetime
import os
import time
import asyncio
from datetime import timedelta
import math
token = os.environ["token"]
guild = 635976654111506446
intents = discord.Intents.default()
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix="-", intents=intents)
bot.remove_command('help')
x = 0
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")


@bot.listen()
async def on_message(message):
    if message.channel.id==993517852558626916 and message.author.id != 1002517551764488223:
        channel = message.channel.id
        count = message.content.split(" ")[0]
        if count.isnumeric():
            if int(count) % 100 == 0:
                await message.add_reaction(emoji='💯')
            if count[::-1] == count:
                await message.add_reaction(emoji='↔️')
    if message.author.id == 510016054391734273 and message.channel.id == 993517852558626916:
        o = bot.get_guild(guild)
        if "You have used **1** of your saves. You have **0" in message.content or "You have used **1** guild save! There are **0" in message.content:
            user = int(message.content.split("**")
                       [0].split(" ")[1].replace("<@", "").replace(">", ""))
            memb = await o.fetch_member(user)
            await memb.remove_roles(discord.utils.get(o.roles, name="Certified Pro Gamer"))
            await message.channel.send(f"You can no longer count in this channel, <@{user}>. Run `c!user` in bot commands when you get a save, and I will give you the permission back.")
    if message.author.id == 510016054391734273:
        try:
            o = bot.get_guild(635976654111506446)
            user = o.get_member_named((message.embeds)[0].title)
            a = ((message.embeds)[0].fields)[0].value
            a = a.split("\n")
            perc = float(a[0].split(" ")[2].replace("*", "").replace("%", ""))
            total = int(a[3].split(" ")[1].replace("*", "").replace(",", ""))
            save = float(a[4].split("**")[1].split("/")[0])
            if perc >= 98.5 and total >= 1000 and save >= 1:
                await user.add_roles(discord.utils.get(o.roles, name="Certified Pro Gamer"))
                await message.add_reaction(emoji='☑️')
            else:
                await user.remove_roles(discord.utils.get(o.roles, name="Certified Pro Gamer"))
                await message.add_reaction(emoji='❌')
        except Exception as e:
            print(e)
            pass

@bot.command()
async def startrun(ctx):
    global x
    if ctx.channel.id == 993517852558626916 and x == 0:
        channel = ctx.channel.id
        o = bot.get_guild(63597665411150644)
        timex = (datetime.datetime.now()+timedelta(minutes=60)).timestamp()
        await ctx.send(f"Setting inside timer for <t:{int(timex)}:R>")
        x = 1
        while x == 1:
            await asyncio.sleep(5) 
            await ctx.channel.set_permissions(discord.utils.get(o.roles,name="Certified Pro Gamer"), send_messages=False)
            timex = (datetime.datetime.now()+timedelta(minutes=10)).timestamp()
            await ctx.send(f"Sleepy Period Until <t:{int(timex)}:R>")
            await asyncio.sleep(5) 
            x = 0
        await ctx.send("**Run over** please do `-startrun` to restart the timer")
        await ctx.channel.set_permissions(discord.utils.get(o.roles,name="Certified Pro Gamer"), send_messages=True)
@bot.command()
async def cancel(ctx):
    global x
    await ctx.send("Cancelled Run")
    x = 0

@bot.command() 
async def wrong(ctx, incorrect=0, percentage=0.0):
  perc=round(percentage,3)
  c=math.ceil(incorrect/(1-perc/100+0.000005))
  if perc>100:
      await ctx.send("you can't have more than 100% accuracy nerd")
  elif perc<0:
      await ctx.send("you can't have less than 0% accuracy nerd")
  else:
      await ctx.send(f"You need {c} counts to get {perc}% accuracy with {incorrect} incorrect counts")
        
        
bot.run(token)
