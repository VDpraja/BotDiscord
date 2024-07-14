import discord
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv
import os
import aiosqlite
from tools.youtube import check_new_video

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
OWNER_ID = int(os.getenv('OWNER_ID'))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

DATABASE = 'youtube_channels.db'

async def init_db():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS channels (guild_id INTEGER PRIMARY KEY, channel_id TEXT, notify_channel_id INTEGER)"
        )
        await db.commit()

@bot.event
async def on_ready():
    await init_db()
    await tree.sync()
    print(f'Logged in as {bot.user.name}')
    check_youtube_channel.start()

@tasks.loop(minutes=10)
async def check_youtube_channel():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT guild_id, channel_id, notify_channel_id FROM channels") as cursor:
            async for row in cursor:
                guild_id, youtube_channel_id, notify_channel_id = row
                video_info = check_new_video(YOUTUBE_API_KEY, youtube_channel_id)
                if video_info:
                    guild = bot.get_guild(guild_id)
                    if guild:
                        channel = guild.get_channel(notify_channel_id)
                        if channel:
                            embed = discord.Embed(
                                title=f"📢 {video_info['title']} 📢",
                                description="Don't forget to Like, Comment, and Subscribe!",
                                color=discord.Color.blue()
                            )
                            embed.add_field(name="Watch Now", value=video_info['video_url'])
                            embed.set_thumbnail(url=video_info['thumbnail_url'])
                            await channel.send(embed=embed)

@tree.command(name="setchannel", description="Set the YouTube channel to monitor")
@app_commands.describe(channel_id="The YouTube channel ID to monitor", notify_channel="The channel where notifications will be sent")
async def setchannel(interaction: discord.Interaction, channel_id: str, notify_channel: discord.TextChannel):
    if interaction.user.id != OWNER_ID and interaction.user.id != interaction.guild.owner_id:
        embed = discord.Embed(
            title="⛔ Permission Denied ⛔",
            description="You do not have permission to use this command.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            "INSERT OR REPLACE INTO channels (guild_id, channel_id, notify_channel_id) VALUES (?, ?, ?)",
            (interaction.guild.id, channel_id, notify_channel.id)
        )
        await db.commit()

    embed = discord.Embed(
        title="✅ Channel Set ✅",
        description=f"The YouTube channel to monitor: {channel_id}\nNotifications will be sent to: {notify_channel.mention}",
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)

@tree.command(name="listchannel", description="Get the current YouTube channel being monitored")
async def listchannel(interaction: discord.Interaction):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT channel_id, notify_channel_id FROM channels WHERE guild_id = ?", (interaction.guild.id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                channel_id, notify_channel_id = row
                notify_channel = interaction.guild.get_channel(notify_channel_id)
                embed = discord.Embed(
                    title="📋 Monitored YouTube Channel 📋",
                    description=f"The current YouTube channel being monitored is: {channel_id}\nNotifications will be sent to: {notify_channel.mention}",
                    color=discord.Color.blue()
                )
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(
                    title="⚠ No Channel Set ⚠",
                    description="No YouTube channel is currently being monitored.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed)

bot.run(TOKEN)
