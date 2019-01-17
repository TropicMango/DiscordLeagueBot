import discord
import time
import asyncio
import random
from discord.ext import commands
from DiscordLeague import LolChampList


description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='n~', description=description)


cs = 50
arr = [0, 0, 0]
select = ''
clearing = ''


async def summon_minions():
    global cs
    global arr
    while True:
        await asyncio.sleep(random.randrange(10, 11))
        arr[random.randrange(len(arr))] += 1
        cs += 1
        await bot.change_presence(game=discord.Game(name='Neeko sees {} minions'.format(cs)))


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name='Neeko sees no minions'))
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
    global select
    msg_cont = ctx.message.content[7:]
    hover_champ = LolChampList.includes(msg_cont)

    if str(ctx.message.author) != select.split('|')[0] and select != '':
        await bot.say('Uh... Some one else is picking right now, Neeko will get to you shortly~')
        return
    if hover_champ is not False:
        embed = discord.Embed(discription="pick your champ", color=0x71f442)
        embed.set_image(url="https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{}_0.jpg".format(hover_champ))
        embed.add_field(name="{} has been selected".format(hover_champ),
                        value="use n~lock or n~pick to lock in or switch")
        await bot.say(embed=embed)

        await bot.say("<@!{}> is hovering ".format(ctx.message.author.id) + hover_champ)
        select = str(ctx.message.author) + '|' + hover_champ
        print(select)
        if str(hover_champ).lower() == 'neeko':
            await bot.say('Neeko is best decision :hearts:')
    else:
        await bot.say("Sorry Neeko don't don't know anyone named {}".format(msg_cont))


@bot.command(pass_context=True)
async def lock(ctx):
    global select
    if str(ctx.message.author) != select.split('|')[0] and select != '':
        await bot.say('Uh... Some one else is picking right now, Neeko will get to you shortly~')
        return
    await bot.say('Okie~')
    await bot.say("<@!{}> locked in ".format(ctx.message.author.id) + select.split('|')[1])
    embed = discord.Embed()
    embed.title = select.split('|')[1] + " joined " + select.split('|')[0][:-5] + "'s crew"
    await bot.say(embed=embed)
    if select.split('|')[1] == 'Neeko':
        await bot.say("Neeko is joyful to be with you")
    select = ''


@bot.command(pass_context=True)
async def clear(ctx):
    global clearing
    if clearing != '':
        await bot.say("there is someone clearing right now\n you can stop them then steal the cs with <n~steal>")
        return
    clearing = ctx.message.author
    await bot.change_presence(game=discord.Game(name='Neeko sees people clearing minions'))
    player = '<@!{}>'.format(ctx.message.author.id)
    clear_msg = await bot.say(player + " is now clearing the minions~")
    await asyncio.sleep(3)
    my_cs = 0
    global cs
    while cs > 0 and clearing == ctx.message.author:
        my_cs += 1
        cs -= 1
        await bot.edit_message(clear_msg, player + " cleared {} minions\n{} minions left".format(my_cs, cs))
        print(my_cs)
        await asyncio.sleep(1)  # change this to stat check
    await bot.say(player + " earned {} gold for clearing~".format(my_cs*12))
    if cs == 0:
        clearing = ''
    return


@bot.command(pass_context=True)
async def steal(ctx):
    author = ctx.message.author
    if clearing == '' or clearing == author:
        await bot.say("Neeko don't see what's there to steal")
    else:
        old_player = '<@!{}>'.format(clearing.id)
        new_player = '<@!{}>'.format(ctx.message.author.id)
        await bot.say("Oh! {} stopped {} from clearing the minions\nuse n~clear to finish the wave".format(new_player, old_player))


bot.run('NTM0OTg5MTE4NzkxMjIxMjQ4.DyBn7g.q8t70y3DtaZLNw1HKCmQfY2t3Zk')
