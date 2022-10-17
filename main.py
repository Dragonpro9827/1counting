import discord
from discord.ext import commands,tasks
import datetime
import psycopg2
import os
import time
import json
from difflib import SequenceMatcher
import asyncio
import datetime
import calendar
from datetime import timedelta
from datetime import date
import math
token = os.environ["token"]
thing = os.environ["DATABASE_URL"]
database=psycopg2.connect(thing,sslmode='require')
c=database.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS ulb
             (time DATE primary key,
             list json)''')
c.execute('''CREATE TABLE IF NOT EXISTS lb
             (time DATE primary key,
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
async def daily(ctx, mode="lb"):
  eg = {"lb": "lb", "ulb": "ulb"}
  today = datetime.datetime.now()
  date = f"{today.year}-{today.month}-{today.day}"
  try:
    mode = eg[mode]
  except:
    return
  today = datetime.datetime.now()
  yesterday = str(today - timedelta(days=1))[0:11]
  c.execute(f"select list from {mode} where time=%s", (date,))
  data = c.fetchone()[0]
  c.execute(f"select list from {mode} where time=%s", (yesterday,))
  data_yesterday = c.fetchone()[0]
  data_dict = {}
  for length in range(1, len(data)):
    counter=0
    for x in data[str(length)]:
      num = int((x[2]).replace(",", ""))
      num_yesterday = int((((data_yesterday[str(length)])[counter])[2]).replace(",", ""))
      ye = ((int(num)-int(num_yesterday)))
      data_dict[(x[1])] = ye
      counter+=1
  data_dict = sorted(data_dict.items(), key=lambda item: item[1], reverse=True)
  counter = 0
  send=""
  for i in data_dict:
    print(i)
    send+=f"**{i}** {data_dict[i]}"
  embed=discord.Embed(title=f"Top 10 Daily {mode}", description=send, color=0xf1f3e1)
  embed.set_footer(text="-help | May vary depending on time logged\n\n")
  await ctx.channel.send(embed=embed)
	
@bot.command()
async def finduser(ctx, name="", date=None):
  channel = ctx.channel.id
  if name == "":
    return
  if date == None:
    today = datetime.datetime.now()
    date = f"{today.year}-{today.month}-{today.day}"
  elif len(date) != 10:
    return
  c.execute("select list from ulb where time=%s", (date,))
  data= c.fetchone()[0]
  a={}
  for x in data:
    for i in data[x]:
      server = (i[1])[1:-2]
      if "#" in name:
        if server == name:
          embed=discord.Embed(title=f"**{(i[1])[:-2]}**'s Stats in `{date}`", description=f"**Score:** {i[2]}\n**Rank:** {i[0]}", color=0x9DD2AA)
          embed.set_footer(text="-help | May vary depending on time logged\n\n")
          await ctx.channel.send(embed=embed)
          return
      else:
        s = SequenceMatcher(None, (server[1:-2]), name)
        a[s.ratio()] = [((i[1])[:-2]), (i[2]), (i[0])]
  key = max(a.keys())
  i = a[key]
  embed=discord.Embed(title=f"**{(i[0])}**'s Stats in `{date}`", description=f"**Score:** {i[1]}\n**Rank:** {i[2]}", color=0x73AADF)
  embed.set_footer(text="-find LIST gives shortcuts!| May vary depending on time logged\n\n")
  await ctx.channel.send(embed=embed)
  #await ctx.channel.send("Couldn't find the server you are looking for")
    
    
@bot.command()
async def find(ctx, name="", date=None):
  channel = ctx.channel.id
  eg = {"cho": "𝓣𝓱𝓮 𝓒𝓸𝓾𝓷𝓽𝓲𝓷𝓰 𝓕𝓪𝓶𝓲𝓵𝔂™", "countaholics": "𝕮𝖔𝖚𝖓𝖙𝖆𝖍𝖔𝖑𝖎𝖈𝖘", "jake": "Jake & Oscar's Counting Paradise", "cu": "CU - Contadores Unidos", "ziggy": "The USSR Ziggy Express", "korland": "Delicious Korland", "maggies": "Maggie's Cat's", "catgirls": "Communist Catgirls"}
  if name == "list":
    send=""
    for i in eg:
      send+=f"**{i}** - {eg[i]}\n"
    embed=discord.Embed(title="**List of shortcuts**", description=send, color=0x73AADF)
    await ctx.channel.send(embed=embed)  
    return
  if name == "a":
    return
  try:
    name = eg[name]
  except:
    pass
  if date == None:
    today = datetime.datetime.now()
    date = f"{today.year}-{today.month}-{today.day}"
  elif len(date) != 10:
    return
  c.execute("select list from lb where time=%s", (date,))
  data= c.fetchone()[0]
  a={}
  for x in data:
    for i in data[x]:
      server = (i[1])
      s = SequenceMatcher(None, (server[1:-2]), name)
      a[s.ratio()] = [((i[1])[:-2]), (i[2]), (i[0])]
  key = max(a.keys())
  i = a[key]
  embed=discord.Embed(title=f"**{(i[0])}**'s Stats in `{date}`", description=f"**Score:** {i[1]}\n**Rank:** {i[2]}", color=0x73AADF)
  embed.set_footer(text="-find LIST gives shortcuts!| May vary depending on time logged\n\n")
  await ctx.channel.send(embed=embed)
  #await ctx.channel.send("Couldn't find the server you are looking for")
  
@bot.command()
async def help(ctx):
  embed=discord.Embed(title=f"Need Help? Saul Goodman", description="Bot collects data from every server its in from the +1 commands sent", color=0x50C878)
  embed.add_field(name="History Commands", value="**-ulb**  *{Page: 1-125}* *{Date: 2022-10-10}* Get User leaderboards back in time\n**-lb** *{Page: 1-125}* *{Date: 2022-10-10}* Get Server leaderboards back in time", inline=True)
  embed.add_field(name="Present Statistics", value="**-finduser** *{Name: Christian230102#2391}* Find a specific user and see their current score and rankings, as well as in the past activity\n**-find** *{Server Name: MilkMania}* Find a specific server and see their current score and rankings, as well as in the past activity\n", inline=True)
  channel = ctx.channel.id
  await ctx.channel.send(embed=embed)
@bot.command()
async def ulb(ctx, page=1, date=None):
    channel = ctx.channel.id
    if date == None:
      today = datetime.datetime.now()
      date = f"{today.year}-{today.month}-{today.day}"
    if len(date)== 7:
      c.execute("select time, list from ulb")
      data= c.fetchall()
      send = ""
      days = calendar.monthrange(int(date[0:4]), int(date[5:7]))[1]
      for x in range(0, days):
        for i in data:
          remade = f"{date[0:4]}-{date[5:7]}-{x}"
          if str(i[0]) == (remade):
            send+=f"{remade}: {len(i[1])}\n"
      embed=discord.Embed(title=f"Amount of pages in {date}", description=send, color=0x2B9678)
      embed.set_footer(text="-help | May vary depending on time logged\n\n")
      await ctx.channel.send(embed=embed)
      return
    try:
      today = datetime.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]))
      yesterday = str(today - timedelta(days=1))[0:11]
      c.execute("select list from ulb where time=%s", (date,))
      data = c.fetchone()[0]
    except:
      await ctx.channel.send("Data in this time period wasn't collected | `-ulb {page} {time}`")
      return
    try:
      c.execute("select list from ulb where time=%s", (yesterday,))
      data_yest = c.fetchone()[0]
      data_yesterday = data_yest[str(page)]
      no=True
    except:
      no=False
      pass
    try:
      data = data[str(page)]
      send = ""
      counter = 0
      for i in data:
        if no == True:
          if i[1] == (data_yesterday[counter])[1]:
            today_count, yesterday_count = int((i[2]).replace(",", "")), int(((data_yesterday[counter])[2]).replace(",", ""))
            send+=f"**{i[0]}** {i[1]} **{i[2]}** `[+{today_count-yesterday_count}]`\n"
          else:
            for key in data_yest:
              for x in (data_yest[key]):
                if x[1] == i[1]:
                  today_count, yesterday_count = int((x[2]).replace(",", "")), int(((i)[2]).replace(",", ""))
                  e = int(x[0].replace("#",""))-int(i[0].replace("#",""))
                  if e < 0:
                    e = f"↓{int(e*-1)}"
                  else:
                    e = f"↑{e}"
                  send+=f"**{i[0]}** {i[1]} **{i[2]}** `[+{yesterday_count-today_count}] {e}`\n"
                  break
        else:
          send+=f"**{i[0]}** {i[1]} **{i[2]}**\n"
        counter+=1
      embed=discord.Embed(title=f"*TOP USERS* in {date}", description=send, color=0x2B9678)
      embed.set_footer(text="-help | May vary depending on time logged\n\n")
      await ctx.channel.send(embed=embed)
    except:
      await ctx.channel.send("Page data wasnt collected | `-ulb {page} {time}`")
      return
@bot.command()
async def lb(ctx, page=1, date=None):
    channel = ctx.channel.id
    if date == None:
      today = datetime.datetime.now()
      date = f"{today.year}-{today.month}-{today.day}"
    if len(date)== 7:
      c.execute("select time, list from lb")
      data= c.fetchall()
      print(date[5:0])
      send = ""
      days = calendar.monthrange(int(date[0:4]), int(date[5:7]))[1]
      for x in range(0, days):
        for i in data:
          remade = f"{date[0:4]}-{date[5:7]}-{x}"
          if str(i[0]) == (remade):
            send+=f"{remade}: {len(i[1])}\n"
      embed=discord.Embed(title=f"Amount of pages in {date}", description=send, color=0x15C2BE)
      embed.set_footer(text="-help | May vary depending on time logged\n\n")
      await ctx.channel.send(embed=embed)
      return
    try:
      today = datetime.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]))
      yesterday = str(today - timedelta(days=1))[0:11]
      c.execute("select list from lb where time=%s", (date,))
      data = c.fetchone()[0]
    except:
      await ctx.channel.send("Data in this time period wasn't collected | `-lb {page} {time}`")
      return
    try:
      c.execute("select list from lb where time=%s", (yesterday,))
      data_yest = c.fetchone()[0]
      data_yesterday = data_yest[str(page)]
      no=True
    except:
      no=False
      pass
    try:
      data = data[str(page)]
      send = ""
      counter = 0
      for i in data:
        if no == True:
          if i[1] == (data_yesterday[counter])[1]:
            today_count, yesterday_count = int((i[2]).replace(",", "")), int(((data_yesterday[counter])[2]).replace(",", ""))
            send+=f"**{i[0]}** {i[1]} **{i[2]}** `[+{today_count-yesterday_count}]`\n"
          else:
            for key in data_yest:
              for x in (data_yest[key]):
                if x[1] == i[1]:
                  today_count, yesterday_count = int((x[2]).replace(",", "")), int(((i)[2]).replace(",", ""))
                  e = int(x[0].replace("#",""))-int(i[0].replace("#",""))
                  if e < 0:
                    e = f"↓{int(e*-1)}"
                  else:
                    e = f"↑{e}"
                  send+=f"**{i[0]}** {i[1]} **{i[2]}** `[+{yesterday_count-today_count}] {e}`\n"
                  break
        else:
          send+=f"**{i[0]}** {i[1]} **{i[2]}**\n"
        counter+=1
      embed=discord.Embed(title=f"*HIGH SCORES* in {date}", description=send, color=0x15C2BE)
      embed.set_footer(text="-help | May vary depending on time logged\n\n")
      await ctx.channel.send(embed=embed)
    except:
      await ctx.channel.send("Page data wasnt collected | `-lb {page} {time}`")
      return
  
@bot.listen()
async def on_message(message):
    channel = message.channel.id
    try:
      if message.author.id == 510016054391734273:
          if "*HIGH SCORES*" == (message.embeds[0].title) or "*TOP USERS*" == (message.embeds[0].title):
            data, new_data = (message.embeds[0].description).split("\n"), []
            footer =  (message.embeds[0].footer.text).replace("c!help | Page ", "")
            for i in data:
                new_data.append(i.split("**"))
            b = [[i for i in item if i != ''] for item in new_data]
            data = [item for item in b if item != []]
            u = int((data[0][0]).replace("#","").replace(",",""))
            u = (u+9)/10
            print(u)
            if int(u) > 125:
              return
            date2 = (str(message.created_at)[0:10])
            if "*TOP USERS*" == (message.embeds[0].title):
              try:
                c.execute("select list from ulb where time=%s", (date2,))
                dict_ = c.fetchone()[0]
              except:
                dict_ = {}
              dict_[footer] = data
              dict_ = json.dumps(dict_)
              date2 = json.dumps(date2)
              c.execute("insert into ulb (time, list) values (%s, %s) on conflict (time) do update set list=%s", (date2, dict_, dict_))
              database.commit()
            if "*HIGH SCORES*" == (message.embeds[0].title):
              try:
                c.execute("select list from lb where time=%s", (date2,))
                dict_ = c.fetchone()[0]
              except:
                dict_ = {}
              dict_[footer] = data
              dict_ = json.dumps(dict_)
              date2 = json.dumps(date2)
              c.execute("insert into lb (time, list) values (%s, %s) on conflict (time) do update set list=%s", (date2, dict_, dict_))
              database.commit()
    except Exception as e:
      print(e)
      pass
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
