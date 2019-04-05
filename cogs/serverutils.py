import discord
from discord.ext import commands

class ServerUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def message_from_link(self, link):
        split_link = link.split("/")
        channel = self.bot.get_channel(int(split_link[-2]))
        message = await self.bot.get_message(channel, int(split_link[-1]))
        return message

    async def add_star(self, message):
        author = message.author
        channel = self.bot.get_channel(483357571756064782)
        description = message.clean_content
        if len(message.clean_content) == 0 and len(message.embeds) > 0 and "description" in message.embeds[0]:
            description += message.embeds[0]["description"]
        embed = discord.Embed(
            description = description,
            timestamp = message.created_at,
            colour = author.colour
        )
        if len(message.embeds) > 0 and message.embeds[0]["type"] == "image":
            embed.set_image(url=message.embeds[0].image.url)
        elif len(message.attachments) > 0:
            embed.set_image(url=message.attachments[0]["url"])
        url = "https://discordapp.com/channels/{0}/{1}/{2}".format(
            str(message.guild.id),
            str(message.channel.id),
            str(message.id)
        )
        embed.set_author(name=author.name + " in #" + message.channel.name, url=url, icon_url=author.avatar_url)
        await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.name == "⭐":
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            await self.add_star(message)

    @commands.command()
    async def star(self, message : message_from_link):
        await self.add_star(message)

