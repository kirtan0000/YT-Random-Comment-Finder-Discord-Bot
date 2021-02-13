import discord
import os
import config
import validators
import googleapiclient.discovery
import random
import re

client = discord.Client()
yt = googleapiclient.discovery.build(
    'youtube', 'v3', developerKey=config.YT_API_KEY)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


def findData(link):
    try:
        if len(link.split(" ")) > 1 and validators.url(link.split(" ")[1]):
            video_id = link.split(" ")[1].rsplit(
                '/', 1)[-1].split("?")[1].split("=")[1]
            request = yt.commentThreads().list(
                part="id,snippet",
                maxResults=200,
                videoId=video_id
            )
            res = request.execute()['items']
            randComment = re.sub('<(a|/a).*?>', "", re.sub('<br*?>', '\n',  re.sub('</br*?>', '\n', res[random.randint(
                0, len(res))]["snippet"]["topLevelComment"]["snippet"]["textDisplay"]))).replace("&#39;", "'")
            randCommentAuthor = res[random.randint(
                0, len(res))]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
            endResult = '"{}" - {}'.format(randComment, randCommentAuthor)
            return endResult
        else:
            return "Please enter a valid link."
    except Exception:
        return "An error occured."


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '!help':
        await message.channel.send('Commands:\n\n!find <youtube video url>\n  - Select a random comment from the given youtube video.')
    elif message.content.startswith('!find'):
        await message.channel.send(findData(message.content))
    else:
        await message.channel.send("Command '{}' not found! Type '!help' for a list of commands.".format(message.content))


client.run(config.TOKEN)
