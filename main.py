import discord
from discord.ext import commands,tasks
import datetime
import psycopg2
import os
import time
import json
import asyncio
import datetime
from datetime import timedelta
import math
token = os.environ["token"]
thing = os.environ["DATABASE_URL"]
database=psycopg2.connect(thing,sslmode='require')
c=database.cursor()
c.execute("DROP TABLE ULB")
database.commit()
c.execute('''CREATE TABLE IF NOT EXISTS ulb
             (time text primary key,
             list json)''')
database.commit()
guild = 635976654111506446
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-", intents=intents)
bot.remove_command('help')
x = True
time = 0
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")

@bot.command()
async def ulb(ctx, time=None, page=1):
    c.execute("SELECT time, list FROM ulb")
    all = c.fetchall()
    channel = ctx.channel.id
    await ctx.channel.send(all)
@bot.listen()
async def on_message(message):
    channel = message.channel.id
    try:
      if message.author.id == 510016054391734273:
          if "HIGH SCORE" in (message.embeds[0].title) or "TOP USER" in (message.embeds[0].title):
            data, new_data = (message.embeds[0].description).split("\n"), []
            footer =  (message.embeds[0].footer.text).replace("c!help | Page ", "")
            for i in data:
                new_data.append(i.split("**"))
            b = [[i for i in item if i != ''] for item in new_data]
            data = [item for item in b if item != []]
            date2 = (str(message.created_at)[0:10])
            if "TOP USER" in (message.embeds[0].title):
              try:
                c.execute("select list from ulb where time=%s", (date,))
                dict_ = c.fetchone()[0]
              except:
                dict_ = {}
              dict_[footer] = data
              dict_ = json.dumps(dict_)
              date2 = json.dumps(date2)
              c.execute("insert into ulb (time, list) values (%s, %s) on conflict (time) do update set list=%s", (date2, dict_, dict_))
              database.commit()
    except Exception as e:
      print(e)
      pass
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
    global time
    x = True
    if ctx.channel.id == 993517852558626916 and x == True:
        channel = ctx.channel.id
        o = bot.get_guild(635976654111506446)
        timex = (datetime.datetime.now()+timedelta(minutes=60)).timestamp()
        time = timex
        await ctx.send(f"Setting inside timer for <t:{int(timex)}:R>")
        while x == True:
            await asyncio.sleep(3600) 
            await ctx.channel.set_permissions(discord.utils.get(o.roles,name="Certified Pro Gamer"), send_messages=False)
            timex = (datetime.datetime.now()+timedelta(minutes=10)).timestamp()
            await ctx.send(f"Sleepy Period Until <t:{int(timex)}:R>")
            await asyncio.sleep(600) 
            x = False
        await ctx.send("**Run over** please do `-startrun` to restart the timer")
        await ctx.channel.set_permissions(discord.utils.get(o.roles,name="Certified Pro Gamer"), send_messages=True)
@bot.command()
async def cancel(ctx):
    global x
    x = False
    await ctx.send("Cancelled Run")
@bot.command()
async def run(ctx):
    global time
    await ctx.send(f"<t:{int(time)}:R>")
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
