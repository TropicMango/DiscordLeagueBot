import discord
import asyncio
import random
from discord.ext import commands
from DiscordLeague import LolChampList, dataManager

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='n~', description=description)


cs = 0
arr = [0, 0, 0]
select = ''
clearing_id = ''
challenge_id = ''
invader = ''
latest_channel = ''


async def summon_minions():
    global cs
    global arr
    global invader
    invade_val = random.randrange(60, 300)
    i = 0
    while True:
        await asyncio.sleep(random.randrange(5, 30))
        i += 1

        if clearing_id == '':
            arr[random.randrange(len(arr))] += 1
            cs += 1
            await bot.change_presence(game=discord.Game(name='Neeko sees {} minions'.format(cs)))

        if i == invade_val:
            await asyncio.sleep(random.randrange(600, 1200))
            invader = LolChampList.generate()
            if random.random() > 0.7:
                invader += '_{}'.format(random.randrange(1, LolChampList.get_skins(invader)))
            else:
                invader += '_0'
            embed = discord.Embed()
            embed.title = "Oh no we got a invader!"
            embed.description = "use n~c <champion> to challenge him"
            embed.set_image(url="https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{}.jpg".format(invader))
            print("https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{}.jpg".format(invader))
            await bot.send_message(latest_channel, embed=embed)
            invade_val = random.randrange(60, 300)




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
        await bot.say("there is someone clearing right now\n you can stop them then steal the cs with <n~steal>")
        return
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
        await asyncio.sleep(1)  # change this to stat check
    dataManager.add_gold(ctx.message.author.id, my_cs * 5)
    await bot.say("{} earned {} gold for clearing~".format(player, my_cs*5))

    if cs == 0:
        await bot.change_presence(game=discord.Game(name='Neeko no minions'))
        clearing_id = ''
    return


@bot.command(pass_context=True)
async def steal(ctx):
    global clearing_id
    author_id = ctx.message.author.id
    if clearing_id == '' or clearing_id == author_id:
        await bot.say("Neeko don't see what's there to steal")
    else:
        old_player = '<@!{}>'.format(clearing_id)
        new_player = '<@!{}>'.format(author_id)
        await bot.say("Oh! {} stopped {} from clearing the minions\n"
                      "use n~clear to finish the wave".format(new_player, old_player))
        clearing_id = ''


@bot.command(pass_context=True)
async def c(ctx):
    if invader == '':
        await bot.say("Currently no challengers")
        return
    if invader.split('_')[0].lower() != ''.join(list(filter(str.isalnum, ctx.message.content.split(' ')[1]))):
        await bot.say("Not the right champion")
        return
    await bot.say("Neeko doesn't know how fighting works yet...")
    await bot.say("But they join your team~")
    embed = discord.Embed()
    embed.title = '{} decided to join your team! (not really)'.format(invader.split('_')[0])
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
async def champ(ctx):
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
    await bot.say('<@!{}> selected {} as their MVP'.format(
        ctx.message.author.id, dataManager.change_mvp(ctx.message.author.id, ctx.message.content.split(' ')[1])))


@bot.command(pass_context=True)
async def info(ctx):
    my_champ = dataManager.get_my_champ(ctx.message.author.id)
    embed = discord.Embed()
    embed.set_image(url="https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{}.jpg".format(my_champ[0]))
    embed.title = str(ctx.message.author)[:-5] + "'s MVP: {}".format(my_champ[0].split('_')[0])
    embed.description = my_champ[1]
    await bot.say(embed=embed)


@bot.event
async def on_message(message):
    global latest_channel
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
#     global latest_channel
#     latest_channel = ctx.message.channel
#     await summon_champion()

bot.run('NTM0OTg5MTE4NzkxMjIxMjQ4.DyBn7g.q8t70y3DtaZLNw1HKCmQfY2t3Zk')
