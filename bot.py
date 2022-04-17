# bot.py
import os
import discord
import random
import time
import string
import datetime
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get


load_dotenv()

TOKEN=os.getenv('DISCORD_TOKEN')

TEST=False
if TEST:
    alert_channels=[930167379080663071]
    #bot test
else:
    my_file=open("channels.txt", "r")
    content=my_file.read()
    alert_channels=content.split(",")
    alert_channels=[int(i) for i in alert_channels]
    my_file.close()
    my_file=open("ping_servers.txt", "r")
    content=my_file.read()
    role_pings=content.split(",")
    role_pings=[int(i) for i in role_pings]
    my_file.close()
    my_file=open("everyone_ping.txt", "r")
    content=my_file.read()
    everyone_servers=content.split(",")
    everyone_servers=[int(i) for i in everyone_servers]
    my_file.close()
    my_file=open("no_ping.txt", "r")
    content=my_file.read()
    no_ping=content.split(",")
    no_ping=[int(i) for i in no_ping]
    my_file.close()

    #bot test

bot = commands.Bot(command_prefix='#')

@bot.event
async def on_ready():
    print('Bot is ready to be used')
# after it is ready do it
    for guild in bot.guilds:
        print(guild)
        print(guild.id)

@bot.command(name='subscribe')
@commands.has_role('Yurei')
async def sub(ctx, type, channel:discord.TextChannel=None, ping:discord.Role=None):
    if(type==('r' or 'R')):
        file=open("ping_servers.txt", "a")
        string=","+str(ping.id)
        file.write(string)
        file.close()
        file=open("channels.txt", "a")
        string=","+str(channel.id)
        file.write(string)
        file.close()
    elif(type==('n' or 'N')):
        file=open("no_ping.txt", "a")
        string=","+str(channel.id)
        file.write(string)
        file.close()
    elif(type==('e' or 'E')):
        file=open("everyone_ping.txt", "a")
        string=","+str(channel.id)
        file.write(string)
        file.close()

@bot.command(name='unsubscribe')
@commands.has_role('Yurei')
async def unsub(ctx, type, channel:discord.TextChannel=None, ping:discord.Role=None):
    remove_channel=str(channel.id)
    #remove_channel="'"+remove_channel+"'"
    print(remove_channel)
    if(type==('r' or 'R')):
        remove_ping=str(ping.id)
        file=open("ping_servers.txt", "r")
        ps=file.read()
        file.close()
        new_string=",".join([i for i in ps.split(",") if i!= remove_ping])
        file=open("ping_servers.txt", "w")
        file.truncate(0)
        file.write(new_string)
        file.close()
        file=open("channels.txt", "r")
        ps=file.read()
        file.close()
        file=open("channels.txt", "w")
        file.truncate(0)
        new_string=",".join([i for i in ps.split(",") if i!= remove_channel])
        file.write(new_string)
        file.close()
    elif(type==('n' or 'N')):
        file=open("no_ping.txt", "r")
        ps=file.read()
        file.close()
        new_string=",".join([i for i in ps.split(",") if i!= remove_channel])
        file=open("no_ping.txt", "w")
        file.truncate(0)
        file.write(new_string)
        file.close()
    elif(type==('e' or 'E')):
        file=open("everyone_ping.txt", "r")
        ps=file.read()
        file.close()
        new_string=",".join([i for i in ps.split(",") if i!= remove_channel])
        print([i for i in ps.split(",")])
        print([i for i in ps.split(",") if i!=remove_channel])
        print(new_string)
        file=open("everyone_ping.txt", "w")
        file.truncate(0)
        file.write(new_string)
        file.close()

@bot.command(name='buy')
@commands.has_role('Yurei')
async def buy_order(ctx, date, ticker, strikeCP, price, stoploss, image=None):
    embed=discord.Embed(title="Buy", description=date+" "+ticker+" "+strikeCP+" @"+price+"\n"+"SL: "+stoploss, color=0x00FF00)
    if(image!=None):
        embed.set_image(url=image)
    for guilds in bot.guilds:
        for channel in guilds.channels:
            if(channel.id in alert_channels):
                role_id=role_pings[alert_channels.index(channel.id)]
                role=get(guilds.roles, id=role_id)
                await channel.send(role.mention, embed=embed)
            elif(channel.id in everyone_servers):
                await channel.send(ctx.message.guild.default_role, embed=embed)
            elif(channel.id in no_ping):
                await channel.send(embed=embed)
   
@bot.command(name='sell')
@commands.has_role('Yurei')
async def sell_order(ctx, date, ticker, strikeCP, price, perc,image=None):
    embed=discord.Embed(title="Sell "+perc+"%", description=date+" "+ticker+" "+strikeCP+" @"+price, color=0xFF5733)
    if(image!=None):
        embed.set_image(url=image)
    for guilds in bot.guilds:
        for channel in guilds.channels:
            if(channel.id in alert_channels):
                role_id=role_pings[alert_channels.index(channel.id)]
                role=get(guilds.roles, id=role_id)
                await channel.send(role.mention, embed=embed)
            elif(channel.id in everyone_servers):
                await channel.send(ctx.message.guild.default_role, embed=embed)
            elif(channel.id in no_ping):
                await channel.send(embed=embed)

@bot.command(name='msg')
@commands.has_role('Yurei')
async def message(ctx, txt, image=None):
    embed=discord.Embed(description=txt, color=0x0112a0)
    if(image!=None):
        embed.set_image(url=image)
    for guilds in bot.guilds:
        for channel in guilds.channels:
            if(channel.id in alert_channels):
                role_id=role_pings[alert_channels.index(channel.id)]
                role=get(guilds.roles, id=role_id)
                await channel.send(role.mention, embed=embed)
            elif(channel.id in everyone_servers):
                await channel.send(ctx.message.guild.default_role, embed=embed)
            elif(channel.id in no_ping):
                await channel.send(embed=embed)

@bot.command(name='trim')
@commands.has_role('Yurei')
async def trim(ctx, ticker, price, perc):
    embed=discord.Embed(description="Trim "+perc+ "%\ of "+ticker+" @"+price, color=0xFF5733)
    for guilds in bot.guilds:
        for channel in guilds.channels:
            if(channel.id in alert_channels):
                role_id=role_pings[alert_channels.index(channel.id)]
                role=get(guilds.roles, id=role_id)
                await channel.send(role.mention, embed=embed)
            elif(channel.id in everyone_servers):
                await channel.send(ctx.message.guild.default_role, embed=embed)
            elif(channel.id in no_ping):
                await channel.send(embed=embed)

@bot.command(name='cut')
@commands.has_role('Yurei')
async def cut(ctx, ticker, price):
    embed=discord.Embed(description="CUT "+ticker+" @"+price, color=0xFF5733)
    for guilds in bot.guilds:
        for channel in guilds.channels:
            if(channel.id in alert_channels):
                role_id=role_pings[alert_channels.index(channel.id)]
                role=get(guilds.roles, id=role_id)
                await channel.send(role.mention, embed=embed)
            elif(channel.id in everyone_servers):
                await channel.send(ctx.message.guild.default_role, embed=embed)
            elif(channel.id in no_ping):
                await channel.send(embed=embed)

@bot.command(name='out')
@commands.has_role('Yurei')
async def cut(ctx, ticker, price):
    embed=discord.Embed(description="All out "+ticker+" @"+price, color=0xFF5733)
    for guilds in bot.guilds:
        for channel in guilds.channels:
            if(channel.id in alert_channels):
                role_id=role_pings[alert_channels.index(channel.id)]
                role=get(guilds.roles, id=role_id)
                await channel.send(role.mention, embed=embed)
            elif(channel.id in everyone_servers):
                await channel.send(ctx.message.guild.default_role, embed=embed)
            elif(channel.id in no_ping):
                await channel.send(embed=embed)


@bot.command(name='ospread')
@commands.has_role('Yurei')
async def message(ctx, type, exp, ticker, buy, sell, price, risk):
    txt=""
    txt+="**BTO** "+buy+"\n"
    txt+="**STO** "+sell+"\n"
    txt+="Entry price: "+price+"\n"
    txt+="Risk level: "+risk+"/10"
    embed=discord.Embed(title="Open "+type+" spread for "+exp+" "+ticker, description=txt, color=0x00FF00)
    for guilds in bot.guilds:
        for channel in guilds.channels:
            if(channel.id in alert_channels):
                role_id=role_pings[alert_channels.index(channel.id)]
                role=get(guilds.roles, id=role_id)
                await channel.send(role.mention, embed=embed)
            elif(channel.id in everyone_servers):
                await channel.send(ctx.message.guild.default_role, embed=embed)
            elif(channel.id in no_ping):
                await channel.send(embed=embed)

@bot.command(name='cspread')
@commands.has_role('Yurei')
async def message (ctx, exp, ticker, spread, price):
    txt="Exit price: "+price
    embed=discord.Embed(title="Close spread for "+exp+" "+ticker+ " "+spread, description=txt, color=0xFF5733)
    for guilds in bot.guilds:
        for channel in guilds.channels:
            if(channel.id in alert_channels):
                role_id=role_pings[alert_channels.index(channel.id)]
                role=get(guilds.roles, id=role_id)
                await channel.send(role.mention, embed=embed)
            elif(channel.id in everyone_servers):
                await channel.send(ctx.message.guild.default_role, embed=embed)
            elif(channel.id in no_ping):
                await channel.send(embed=embed)

@bot.command(name='strim')
@commands.has_role('Yurei')
async def trim(ctx, exp, ticker, price, number):
    embed=discord.Embed(title="Trim "+exp+" "+ticker+ " spread", description="Sell "+number+" cons"+" @"+price, color=0xFF5733)
    for guilds in bot.guilds:
        for channel in guilds.channels:
            if(channel.id in alert_channels):
                role_id=role_pings[alert_channels.index(channel.id)]
                role=get(guilds.roles, id=role_id)
                await channel.send(role.mention, embed=embed)
            elif(channel.id in everyone_servers):
                await channel.send(ctx.message.guild.default_role, embed=embed)
            elif(channel.id in no_ping):
                await channel.send(embed=embed)

@bot.command(name='rollup')
@commands.has_role('Yurei')
async def rollup(ctx, exp, ticker, p1, p2, p11, p12, price):
    txt=""
    txt+="Roll up "+p1+"/"+p2+" spread to "+p11+"/"+p12+" spread, same expiration\n\n"
    txt+="**New price**: "+price
    embed=discord.Embed(title="Roll up "+exp+" "+ticker+ " spread", description=txt, color=0xFF5733)
    for guilds in bot.guilds:
        for channel in guilds.channels:
            if(channel.id in alert_channels):
                role_id=role_pings[alert_channels.index(channel.id)]
                role=get(guilds.roles, id=role_id)
                await channel.send(role.mention, embed=embed)
            elif(channel.id in everyone_servers):
                await channel.send(ctx.message.guild.default_role, embed=embed)
            elif(channel.id in no_ping):
                await channel.send(embed=embed)

@bot.command(name='watchlist')
@commands.has_role('Yurei')
async def recap(ctx, tickers, COrP, ER):
    txt=""
    ticks=str(tickers).split(',')
    CP=str(COrP).split(',')
    Ers=str(ER).split(',')
    Ers=[int(i)-1 for i in Ers]
    print(Ers)
    for i in range(0, len(ticks)):
        if i in Ers:
            result="***"
            result+=ticks[i]+"***: "
            result+= CP[i]+"\n"
            txt+=result
        else:
            result="**"
            result+=ticks[i]+"**: "
            result+= CP[i]+"\n"
            txt+=result            
    txt+="Italicized tickers are ER/lotto plays"
    end_date = datetime.date.today() + datetime.timedelta(days=1)
    tom = end_date.strftime("%m/%d/%y")
    embed=discord.Embed(title="Watchlist for "+str(tom), description=txt, color=0x0112a0)
    if TEST==True:
        for guilds in bot.guilds:
            for channel in guilds.channels:
                if(channel.id in alert_channels):
                    await channel.send(embed=embed)
    else:
        for guilds in bot.guilds:
            for channel in guilds.channels:
                if(channel.id in alert_channels):
                    role_id=role_pings[alert_channels.index(channel.id)]
                    role=get(guilds.roles, id=role_id)
                    await channel.send(role.mention, embed=embed)
                elif(channel.id in everyone_servers):
                    await channel.send(ctx.message.guild.default_role, embed=embed)
                elif(channel.id in no_ping):
                    await channel.send(embed=embed)

@bot.command(name='recap')
@commands.has_role('Yurei')
async def recap(ctx, tickers, percents):
    tickers=str(tickers)
    ticks=tickers.split(',')
    percents=str(percents)
    percs=percents.split(',')
    rg=[]
    for i in percs:
        if i[0]=='+':
            rg.append('g')
        else:
            rg.append('r')
    embed_string=""
    for i in range(0, len(ticks)):
        #print(i)
        result=""
        result=result+ticks[i]+" "+percs[i]+"% "
        if(rg[i]=='g'):
            result=result+" <:green_circle:930207873961697412>"
        else:
            result=result+" <:red_circle:930208152559956028>"
        result=result+"\n"
        #print(result)
        embed_string=embed_string+result
    total=0
    for i in range(0, len(percs)):
        if rg[i]=='g':
            total=total+int(percs[i][1:])
        else:
            total=total-int(percs[i][1:])
    embed_string=embed_string+"\n \n Total:"+str(total)
    if(total>100):
        embed_string=embed_string+"%<:rocket:930210721655046144>\n"
    avg_gain=round(total/len(percs),2)
    Winrate=round(rg.count('g')/len(rg)*100,2)
    embed_string=embed_string+"\nWinrate="+str(Winrate)+"%\n"+"AvgGain="+str(avg_gain)+ "%"+" per trade"

    today=datetime.today()
    today_date = today.strftime("%m/%d")
    embed=discord.Embed(title= today_date+" recap", description=embed_string)
    for guilds in bot.guilds:
        for channel in guilds.channels:
            if(channel.id in alert_channels):
                role_id=role_pings[alert_channels.index(channel.id)]
                role=get(guilds.roles, id=role_id)
                await channel.send(role.mention, embed=embed)
            elif(channel.id in everyone_servers):
                await channel.send(ctx.message.guild.default_role, embed=embed)
            elif(channel.id in no_ping):
                await channel.send(embed=embed)
    

bot.run(TOKEN)