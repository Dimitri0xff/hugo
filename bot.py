import discord


client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)


@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        await client.send_message(message.channel, 'Hello')


key_file = open('token.txt')
key = key_file.read()
key_file.close()
client.run(key)
