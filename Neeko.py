import discord
import time
import asyncio
import random
from discord.ext import commands


description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='n~', description=description)


cs = 0
arr = [0, 0, 0]


async def summon_minions():
    global cs
    global arr
    while True:
        await bot.change_presence(game=discord.Game(name='Neeko sees {} minions'.format(cs)))
        await asyncio.sleep(random.randrange(10, 11))
        arr[random.randrange(len(arr))] += 1
        cs += 1


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    # await bot.change_presence(game=discord.Game(name='Not Being Neeko~'))
    await summon_minions()


@bot.command(pass_context=True)
async def minions(ctx):
    await bot.say('Neeko sees.....'.format(str(ctx.message.author)[:-5]))
    t = await bot.say('Pong!')
    ms = (t.timestamp - ctx.message.timestamp).total_seconds() * 1000
    await bot.edit_message(t, new_content='Pong! Took: {}ms'.format(int(ms)))


@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say('Neeko thinks {} talks too much'.format(str(ctx.message.author)[:-5]))
    t = await bot.say('Pong!')
    ms = (t.timestamp - ctx.message.timestamp).total_seconds() * 1000
    await bot.edit_message(t, new_content='Pong! Took: {}ms'.format(int(ms)))


@bot.command(pass_context=True)
async def start(ctx):
    embed = discord.Embed(discription="welcome to the rift", color=0x71f442)
    embed.add_field(name="Welcome to the Rift {}".format(str(ctx.message.author)[:-5]),
                    value="Neeko is joyful to accompany you", inline=False)
    embed.add_field(name="How to Start", value="use n~pick <champion> to select your champion (caps required)")
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def pick(ctx):
    hover_champ = ctx.message.content[7:]
    embed = discord.Embed(discription="pick your champ", color=0x71f442)
    embed.set_image(url="https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{}_0.jpg".format(hover_champ))
    embed.add_field(name="{} has been selected".format(hover_champ),
                    value="use n~confirm or n~pick to confirm or switch")
    await bot.say(embed=embed)
    if str(hover_champ).lower() == 'neeko':
        await bot.say('Neeko is best decision :hearts:')





bot.run('NTM0OTg5MTE4NzkxMjIxMjQ4.DyBn7g.q8t70y3DtaZLNw1HKCmQfY2t3Zk')
