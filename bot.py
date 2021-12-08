# bot.py
import os
from TopPlays import TopPlays
from RecentPlays import RecentPlays
from UserProfile import UserProfile
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

help_command = commands.DefaultHelpCommand(
    no_category='User Commands'
)

bot = commands.Bot(command_prefix='!', help_command=help_command)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(help="Displays a user's top play by performance points, along with all other relevant information about the score", brief="Displays a user's top play by performance points")
async def top(ctx, *playerName):
    playerName = ' '.join(playerName)
    topPlay = TopPlays(playerName)
    info = topPlay.getTotalInfo()
    embed = discord.Embed(title=f'{info["artist"]}: {info["songName"]} [{info["diffName"]}] {info["stars"]}{"★"} +{info["mods"]}',
                          description=f'**{info["score"]}** | **{info["acc"]}%** | **{info["threehundred"]}/{info["hundred"]}/{info["fifty"]}/{info["miss"]}** |  **{info["pp"]}**',
                          url=info["map_url"], color=0xD8B400)
    embed.set_author(
        name=f'Top play for {info["username"]}:', url=info["user_url"])
    embed.set_thumbnail(url=info["bg"])
    await ctx.send(embed=embed)

# get recent play


@bot.command(help="Displays a user's most recent play in the last 24 hours, along with all other relevant information about the score", brief="Displays a user's most recent play in the last 24 hours")
async def recent(ctx, *playerName):

    playerName = ' '.join(playerName)
    recentPlay = RecentPlays(playerName)

    info = recentPlay.getTotalInfo()
    if info["exists"] == True:
        embed = discord.Embed(title=f'{info["artist"]}: {info["songName"]} [{info["diffName"]}] {info["stars"]}{"★"} +{info["mods"]}',
                              description=f'**{info["score"]}** | **{info["acc"]}%** | **{info["threehundred"]}/{info["hundred"]}/{info["fifty"]}/{info["miss"]}** |  **{info["pp"]}**',
                              url=info["map_url"], color=0x5FE100)
        embed.set_author(
            name=f'Recent play for {info["username"]}:', url=info["user_url"])
        embed.set_thumbnail(url=info["bg"])

    else:
        embed = discord.Embed(
            title=f'{info["username"]} has not submitted any scores in the last 24 hours.')
    await ctx.send(embed=embed)


@bot.command(help="Displays detailed information about a user's osu! profile, including top 5 plays by performance points", brief="Displays a user's osu! profile, including all relevant information")
async def profile(ctx, *playerName):
    playerName = ' '.join(playerName)
    profile = UserProfile(playerName)
    info = profile.getTotalInfo()

    if info["exists"] == True:

        embed = discord.Embed(title=f'{info["username"]}', description=f'**Level {info["level"]}**',
                              url=info["userUrl"], color=0xCF0000)
        embed.set_author(
            name=f'osu! User Information')
        embed.add_field(name='Global Rank',
                        value=f'{info["rank"]}', inline=True)
        embed.add_field(name='PP     ', value=f'{info["pp"]}', inline=True)
        embed.add_field(name='Accuracy',
                        value=f'{info["profileAcc"]}%', inline=True)
        embed.set_thumbnail(url=info["profilePic"])

        embed.add_field(name='Ranked Score',
                        value=f'{info["rankedScore"]}', inline=True)
        embed.add_field(name='Play Count',
                        value=f'{info["playCount"]}', inline=True)
        embed.add_field(name='Play Time',
                        value=f'{info["playTime"]} hrs', inline=True)

        embed.add_field(name="\u200b",
                        value="**Top Plays:**", inline=False)

        # getting top 5 plays for user similar to how they are displayed on the osu! website

        for i in range(1, 6):
            topPlay = TopPlays(playerName, i)
            info = topPlay.getTotalInfo()
            tempString = f'**{info["artist"]}: {info["songName"]} [{info["diffName"]}] {info["stars"]}{"★"} +{info["mods"]}**'
            embed.add_field(name=f'{i}.',
                            value=f'[{tempString}]({info["map_url"]})', inline=False)
            tempString = f'**{info["score"]}** | **{info["acc"]}%** | **{info["threehundred"]}/{info["hundred"]}/{info["fifty"]}/{info["miss"]}** |  **{info["pp"]}**'
            embed.add_field(name=f'\n{tempString}',
                            value="\u200b", inline=False)

    else:
        embed = discord.Embed(title=f'That user does not exist.')
    await ctx.send(embed=embed)


bot.run(TOKEN)
