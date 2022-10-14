import discord
from discord.ext import commands,tasks
import datetime
import psycopg2
import os
import time
import json
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
async def ulb(ctx, date=None, page=1):
    channel = ctx.channel.id
    if len(date)== 7:
      c.execute("select time, list from ulb")
      data= c.fetchall()
      print(date[5:0])
      send = ""
      days = calendar.monthrange(int(date[0:4]), int(date[5:7]))[1]
      for x in range(0, days):
        for i in data:
          remade = f"{date[0:4]}-{date[5:7]}-{x}"
          if str(i[0]) == (remade):
            send+=f"{remade}: {len(i[1])}\n"
      embed=discord.Embed(title=f"Amount of pages in {date}", description=send, color=0x301934)
      await ctx.channel.send(embed=embed)
      return
    try:
      today = datetime.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]))
      yesterday = str(today - timedelta(days=1))[0:11]
      print(yesterday)
      c.execute("select list from ulb where time=%s", (date,))
      data = c.fetchone()[0]
    except:
      await ctx.channel.send("Data in this time period wasn't collected :(")
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
                  send+=f"**{i[0]}** {i[1]} **{i[2]}** `[+{yesterday_count-today_count} ↑{e}]`\n"
                  break
        else:
          send+=f"**{i[0]}** {i[1]} **{i[2]}**\n"
        counter+=1
      embed=discord.Embed(title=f"*TOP USERS* in {date}", description=send, color=0x301934)
      await ctx.channel.send(embed=embed)
    except:
      await ctx.channel.send("Page data wasnt collected :(")
      return
@bot.command()
async def lb(ctx, date=None, page=1):
    channel = ctx.channel.id
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
      embed=discord.Embed(title=f"Amount of pages in {date}", description=send, color=0x301934)
      await ctx.channel.send(embed=embed)
      return
    try:
      c.execute("select list from lb where time=%s", (date,))
      data = c.fetchone()[0]
    except:
      await ctx.channel.send("Data in this time period wasn't collected :(")
      return
    try:
      data = data[str(page)]
      send = ""
      for i in data:
        send+=f"**{i[0]}** {i[1]} **{i[2]}**\n"
      embed=discord.Embed(title=f"*HIGH SCORES* in {date}", description=send, color=0x301934)
      await ctx.channel.send(embed=embed)
    except:
      await ctx.channel.send("Page data wasnt collected :(")
      return
  
@bot.listen()
async def on_message(message):
    channel = message.channel.id
    try:
      if message.author.id == 510016054391734273:
          if "HIGH SCORE" == (message.embeds[0].title) or "TOP USER" == (message.embeds[0].title):
            data, new_data = (message.embeds[0].description).split("\n"), []
            footer =  (message.embeds[0].footer.text).replace("c!help | Page ", "")
            for i in data:
                new_data.append(i.split("**"))
            b = [[i for i in item if i != ''] for item in new_data]
            data = [item for item in b if item != []]
            date2 = (str(message.created_at)[0:10])
            if "TOP USER" == (message.embeds[0].title):
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
            if "HIGH SCORE" == (message.embeds[0].title):
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
