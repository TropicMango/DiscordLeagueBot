import discord
import asyncio
from Discord import Image
from Discord import webtest
from Discord import LolLineFetcher

client = discord.Client()
trading = False


def collect_image(message):
    get_url = Image.search_cat()
    embed = discord.Embed()
    embed.set_image(url=get_url)
    msg = client.send_message(message.channel, embed=embed)
    return msg


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    # await client.send_message(message.channel, 'Done sleeping')


@client.event
async def on_message(message):
    global trading
    if message.author.bot:
        return
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith("!champ"):
        await client.send_message(message.channel, LolLineFetcher.gen_champ())
        await client.send_message(message.channel, LolLineFetcher.hint())
    elif message.content.startswith("!hint"):
        for x in range(int_cast(message.content)):
            await client.send_message(message.channel, LolLineFetcher.hint())
    elif message.content.startswith("!answer"):
        await client.send_message(message.channel, LolLineFetcher.answer(name_cast(message.content)))
    elif message.content.startswith('!search'):
        item = message.content.replace("!search ", "")
        link = webtest.search_things(item)
        await client.send_message(message.channel, link)
    elif message.content.startswith('!sleep'):
        message_s = message.content
        time = int_cast(message_s)

        tmp = await client.send_message(message.channel, 'sleeping for {}'.format(time))
        while time > 0:
            time -= 1
            await asyncio.sleep(1)
            await client.edit_message(tmp, 'sleeping for {}'.format(time))
        await client.edit_message(tmp, 'Done sleeping')
    elif message.content.startswith('!spam'):
        message_s = message.content
        time = int_cast(message_s)

        await client.send_message(message.channel, 'spamming {} messages'.format(time))
        while time > 1:
            time -= 1
            await asyncio.sleep(1)
            await client.send_message(message.channel, 'spamming {} more messages'.format(time))
        await client.send_message(message.channel, 'spam complete'.format(time))
    elif 'is stupid' in message.content:
        await asyncio.sleep(0.4)
        await client.send_message(message.channel, 'agreed')
    elif message.content.lower().startswith('cat'):
        message_s = message.content
        time = int_cast(message_s)
        if time > 20:
            await client.send_message(message.channel, 'Error Value Over 20')
        else:
            for x in range(time):
                await collect_image(message)
                await asyncio.sleep(1)
    elif 'cat' in message.content.lower() and not 'catch' in message.content.lower():
        await collect_image(message)
    elif message.content.lower().startswith('skaarl'):
        await client.send_message(message.channel, "I'm a lizard!")
    elif 'skaarl' in message.content.lower():
        await client.send_message(message.channel, 'Skaarl is a lizard')
    elif 'bird' in message.content.lower():
        await client.send_message(message.channel, 'Skaarl is not a bird')
    elif 'ping' in message.content.lower():
        await client.send_message(message.channel, 'pong')


def int_cast(string):
    try:
        return int(string.split(' ')[1])
    except ValueError:
        return 1
    except IndexError:
        return 1


def name_cast(string):
    try:
        return string.split(' ')[1]
    except ValueError:
        return ""
    except IndexError:
        return ""


client.run('NDc5ODA3NzQ0NDkzNDg2MDkw.DwwT3A.LnAqJ7LNQdz9lhaAS9c0PmcySSA')
