# bot.py
import os
from TopPlays import TopPlays
from RecentPlays import RecentPlays
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command()
async def info(ctx):
    commandList = "!top <username> to get user's top play\n!recent to get user's most recent play within 24 hours"
    await ctx.send(commandList)


@bot.command()
async def top(ctx, *playerName):
    playerName = ' '.join(playerName)
    topPlay = TopPlays(playerName)
    info = topPlay.getTotalInfo()
    embed = discord.Embed(title=f'{info["artist"]}: {info["songName"]} ({info["diffName"]}) {info["stars"]}{"★"} {info["mods"]}',
                          description=f'**{info["score"]}** | **{info["acc"]}%** | **{info["threehundred"]}/{info["hundred"]}/{info["fifty"]}/{info["miss"]}** |  **{info["pp"]}**',
                          url=info["map_url"], color=0xFF5733)
    embed.set_author(
        name=f'Top play for {info["username"]}:', url=info["user_url"])
    embed.set_thumbnail(url=info["bg"])
    await ctx.send(embed=embed)

# get recent play


@bot.command()
async def recent(ctx, *playerName):

    playerName = ' '.join(playerName)
    recentPlay = RecentPlays(playerName)

    info = recentPlay.getTotalInfo()
    if info["exists"] == True:
        embed = discord.Embed(title=f'{info["artist"]}: {info["songName"]} ({info["diffName"]}) {info["stars"]}{"★"} {info["mods"]}',
                              description=f'**{info["score"]}** | **{info["acc"]}%** | **{info["threehundred"]}/{info["hundred"]}/{info["fifty"]}/{info["miss"]}** |  **{info["pp"]}**',
                              url=info["map_url"], color=0xFF5733)
        embed.set_author(
            name=f'Recent play for {info["username"]}:', url=info["user_url"])
        embed.set_thumbnail(url=info["bg"])

    else:
        embed = discord.Embed(
            title=f'{info["username"]} has not submitted any scores in the last 24 hours.')
    await ctx.send(embed=embed)


bot.run(TOKEN)
