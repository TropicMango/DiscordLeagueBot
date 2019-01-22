import discord
import asyncio
import random
import time
import math
from discord.ext import commands
from DiscordLeague import LolChampList, dataManager

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='n~', description=description)
bot.remove_command("help")

cs = 0
arr = [0, 0, 0]
select = ''
clearing_id = ''
challenge_id = ''
invader = ''
latest_channel = ''
stun_list = []
clear_scaling = 0.6


async def summon_minions():
    global cs
    global arr
    global invader
    invade_val = random.randrange(30, 60)
    i = 0
    while True:
        await asyncio.sleep(random.randrange(5, 30))
        i += 1

        if clearing_id == '':
            arr[random.randrange(len(arr))] += 1
            cs += 1
            await bot.change_presence(game=discord.Game(name='Neeko sees {} minions'.format(cs)))

        if i == invade_val:
            i = 0
            if latest_channel == '':
                continue
            invader = LolChampList.generate()
            if random.random() > 0.7:
                invader += '_{}'.format(random.randrange(0, LolChampList.get_skins(invader)))
            else:
                invader += '_0'
            embed = discord.Embed()
            embed.color = 0xe0ff2f
            embed.title = "Oh no we got a invader!"
            embed.description = "use n~c <champion> to challenge him"
            embed.set_image(url="https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{}.jpg".format(invader))
            print("https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{}.jpg".format(invader))
            await bot.send_message(latest_channel, embed=embed)
            invade_val = random.randrange(120, 300)


@bot.event
async def on_ready():  # when ready it prints the username, id, and starts the summoning process
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name='Not being Neeko~'))
    await summon_minions()


@bot.command()
async def minions():
    global cs
    await bot.say('Neeko sees {} minions'.format(cs))


@bot.command(pass_context=True)
async def ping(ctx):
    await bot.say('Neeko thinks <@!{}> talks too much'.format(ctx.message.author.id))
    t = await bot.say('Pong!')
    ms = (t.timestamp - ctx.message.timestamp).total_seconds() * 1000
    await bot.edit_message(t, new_content='Pong! Took: {}ms'.format(int(ms)))


@bot.command(pass_context=True)
async def start(ctx):
    embed = discord.Embed(discription="welcome to the rift", color=0x71f442)
    embed.add_field(name="Welcome to the Rift {}".format(str(ctx.message.author)[:-5]),
                    value="Neeko is joyful to accompany you", inline=False)
    embed.add_field(name="How to Start", value="use n~pick <champion> to select your champion")
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def pick(ctx):
    if dataManager.started(ctx.message.author.id):
        await bot.say('Sorry you already picked a champion')
        return

    global select
    msg_cont = ctx.message.content[7:]
    hover_champ = LolChampList.includes(msg_cont)

    if ctx.message.author.id != select.split('|')[0] and select != '':
        await bot.say('Uh... Some one else is picking right now, Neeko will get to you shortly~')
        return
    if hover_champ is not False:
        embed = discord.Embed(discription="pick your champ", color=0x71f442)
        embed.set_image(url="https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{}_0.jpg".format(hover_champ))
        embed.add_field(name="{} has been selected".format(hover_champ),
                        value="use n~lock or n~pick to lock in or switch")
        await bot.say(embed=embed)

        await bot.say("<@!{}> is hovering {}".format(ctx.message.author.id, hover_champ))
        select = ctx.message.author.id + '|' + hover_champ
        if str(hover_champ).lower() == 'neeko':
            await bot.say('Neeko is best decision :hearts:')
    else:
        await bot.say("Sorry Neeko don't don't know anyone named {}".format(msg_cont))


@bot.command(pass_context=True)
async def lock(ctx):
    global select
    s_split = select.split('|')
    if ctx.message.author.id != s_split[0] and select != '':
        await bot.say('Uh... Some one else is picking right now, Neeko will get to you shortly~')
        return
    await bot.say('Okie~')
    dataManager.pick_champ(s_split[0], s_split[1])
    await bot.say("<@!{}> locked in ".format(s_split[0], s_split[1]))
    embed = discord.Embed()
    embed.color = 0xe0ff2f
    embed.title = s_split[1] + " joined " + str(ctx.message.author)[:-5] + "'s team"
    await bot.say(embed=embed)
    if select.split('|')[1] == 'Neeko':
        await bot.say("Neeko is joyful to be with you")
    select = ''


@bot.command(pass_context=True)
async def clear(ctx):
    global clearing_id
    if not dataManager.started(ctx.message.author.id):
        await bot.say("Sorry you don't have any champions...")
        return
    if clearing_id != '':
        await bot.say("there is someone clearing right now\n you can stop them with <n~stun>")
        return
    for x in range(len(stun_list)):
        name = stun_list[x]
        if name.startswith(ctx.message.author.id):
            if float(name.split('|')[1]) > time.time():
                await bot.say("Sorry you are stunned right now")
                return
            else:
                stun_list.pop(x)
                continue
    clearing_id = ctx.message.author.id
    await bot.change_presence(game=discord.Game(name='Neeko sees people clearing minions'))
    player = '<@!{}>'.format(clearing_id)
    clear_msg = await bot.say(player + " is now clearing the minions~")
    await asyncio.sleep(3)
    my_cs = 0
    global cs
    print(str(ctx.message.author) + "is now clearing")
    while cs > 0 and clearing_id == ctx.message.author.id:
        my_cs += 1
        cs -= 1
        await bot.edit_message(clear_msg, "{} cleared {} minions\n{} minions left".format(player, my_cs, cs))
        await asyncio.sleep(10 / math.pow(int(dataManager.get_my_strength(ctx.message.author.id)), clear_scaling))

    members = 0
    for user in ctx.message.server.members:
        if user.status != discord.Status.offline and not user.bot:
            members += 1
    await bot.say(dataManager.add_gold(ctx.message.author.id, my_cs, members))
    if cs == 0:
        await bot.change_presence(game=discord.Game(name='Neeko no minions'))
        clearing_id = ''
    return


@bot.command(pass_context=True)
async def stun(ctx):
    global clearing_id
    author_id = ctx.message.author.id
    if clearing_id == '' or clearing_id == author_id:
        await bot.say("Neeko don't see who's there to stun")
    else:
        old_player = '<@!{}>'.format(clearing_id)
        new_player = '<@!{}>'.format(author_id)
        await bot.say("Oh! {} stunned {} for 10 seconds\n"
                      "use n~clear to finish the wave".format(new_player, old_player))
        stun_list.append('{}|{}'.format(clearing_id, time.time() + 10))
        clearing_id = ''


@bot.command(pass_context=True)
async def c(ctx):
    if not dataManager.started(ctx.message.author.id):
        await bot.say("Sorry you don't have any champions...")
        return
    global invader
    if invader == '':
        await bot.say("Currently no challengers")
        return
    if invader.split('_')[0].lower() != ''.join(list(filter(str.isalnum, ctx.message.content.split(' ')[1]))):
        await bot.say("Not the right champion")
        return
    await bot.say("Neeko doesn't know how fighting works yet...")
    await bot.say("But they join your team~")
    dataManager.add_champ(ctx.message.author.id, invader.split('_')[0], invader.split('_')[1])
    embed = discord.Embed()
    embed.color = 0xe0ff2f
    embed.title = '{} decided to join your team!'.format(invader.split('_')[0])
    invader = ''
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def gold(ctx):
    if not dataManager.started(ctx.message.author.id):
        await bot.say("Sorry you don't have any champions...")
        return
    embed = discord.Embed()
    embed.color = 0xe0ff2f
    embed.set_thumbnail(url="http://ddragon.leagueoflegends.com/cdn/5.5.1/img/ui/gold.png")
    embed.title = "{}'s account balance:".format(str(ctx.message.author)[:-5])
    embed.description = "you currently have: {} gold".format(dataManager.get_gold(ctx.message.author.id))
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def team(ctx):
    if not dataManager.started(ctx.message.author.id):
        await bot.say("Sorry you don't have any champions...")
        return
    embed = discord.Embed()
    embed.color = 0xe0ff2f
    # embed.set_thumbnail(url="https://ddragon.leagueoflegends.com/cdn/9.1.1/img/champion/Teemo.png")
    embed.title = "{}'s current team:".format(str(ctx.message.author)[:-5])
    champs = dataManager.get_champs(ctx.message.author.id)
    for stat in champs:
        embed.add_field(name=stat.split('|')[0], value=stat.split('|')[1])
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def mvp(ctx):
    try:
        await bot.say('<@!{}> selected {} as their MVP'.format(
            ctx.message.author.id, dataManager.change_mvp(ctx.message.author.id, ctx.message.content.split(' ')[1])))
        await display_info(ctx)
    except IndexError:
        await bot.say("Sorry but Neeko don't think you entered a champion number...")
    except discord.ext.commands.errors.CommandInvokeError:
        await bot.say("Sorry but Neeko don't think you have a champion of that number...")


@bot.command(pass_context=True)
async def info(ctx):
    await display_info(ctx)


async def display_info(ctx):
    my_champ = dataManager.get_my_champ(ctx.message.author.id)
    embed = discord.Embed()
    embed.set_image(url="https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{}.jpg".format(my_champ[0]))
    embed.title = str(ctx.message.author)[:-5] + "'s MVP: {}".format(my_champ[0].split('_')[0])
    embed.description = my_champ[1] + '\nClears at {} minions per second' \
        .format(round(1 / (10 / math.pow(int(dataManager.get_my_strength(ctx.message.author.id)), clear_scaling)), 2))
    await bot.say(embed=embed)


@bot.command()
async def shop():
    embed = discord.Embed(color=0x71f442)
    embed.title = 'Hey look Neeko sees the shop~'
    embed.add_field(name='item1', value='does things')
    embed.add_field(name='item2', value='does things')
    embed.add_field(name='item3', value='does things')
    embed.add_field(name='item4', value='does things')
    embed.add_field(name='item5', value='does things')
    embed.add_field(name='item6', value='does things')
    embed.add_field(name='item7', value='does things')
    embed.add_field(name='item8', value='does things')
    embed.add_field(name='item9', value='does things')
    await bot.say(embed=embed)


@bot.command()
async def help():
    embed = discord.Embed()
    embed.title = "Neeko's available commands: "
    embed.description = "n~start: basic information to start the game\n" \
                        "n~clear: clear the minions to earn gold\n" \
                        "n~stun: interrupt someone from clearing so you can clear\n" \
                        "n~team: shows a list of your team\n" \
                        "n~mvp: change the mvp of your team\n" \
                        "n~info: shows information on your mvp\n" \
                        "n~shop: uh... good question XD"
    await bot.say(embed=embed)


@bot.event
async def on_message(message):
    global latest_channel
    if latest_channel == '':
        latest_channel = message.channel
    await bot.process_commands(message)


# ------------------------------------------ Testing Commands ----------------------------------------------

@bot.command(pass_context=True)
async def cheat(ctx):
    await bot.say("good summoners shouldn't cheat like <@!{}>".format(ctx.message.author.id))
    # global cs
    # cs += 10n~clear
    # await bot.say('<@!{}> should be reported for spawning 10 minions'.format(ctx.message.author.id))
    # await bot.change_presence(game=discord.Game(name='Neeko sees {} minions'.format(cs)))


# @bot.command(pass_context=True)
# async def test(ctx):
#     for user in ctx.message.server.members:
#         if user.status != discord.Status.offline and !user.bot:
#             i += 1

bot.run('NTM0OTg5MTE4NzkxMjIxMjQ4.DyBn7g.q8t70y3DtaZLNw1HKCmQfY2t3Zk')
