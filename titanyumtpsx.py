import discord
import asyncio
import json
import logging
from mcstatus.server import JavaServer
from discord.ext import commands

logging.getLogger("discord").setLevel(logging.CRITICAL)
print("🔧 Logging into TitanyumTPSX bot...")

with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config["token"]
GUILD_ID = int(config["guild_id"])
CHANNEL_ID = int(config["channel_id"])
SERVER_IP = config["server_ip"]
SERVERNAME = config.get("servername", SERVER_IP)
CHECK_INTERVAL = int(config.get("check_interval", 120))


giris_durum = {
    "yurtici": True,
    "yurtdisi": True
}

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

status_message = None

async def fetch_server_status(ip):
    try:
        server = JavaServer.lookup(ip)
        status = await server.async_status()
        return {
            "online": True,
            "players_online": status.players.online,
            "players_max": status.players.max,
            "latency": round(status.latency, 2)
        }
    except Exception as e:
        return {
            "online": False,
            "error": str(e)
        }

def durum_etiketi(aktif):
    return "✅ Aktif" if aktif else "❌ Pasif"

def create_embed(status):
    giris_bilgi = f"🌍 Yurt İçi: {durum_etiketi(giris_durum['yurtici'])} | Yurt Dışı: {durum_etiketi(giris_durum['yurtdisi'])}"

    if status["online"]:
        description = (
            f"🟢 **Sunucu Çevrimiçi!**\n"
            f"👥 Oyuncular: {status['players_online']} / {status['players_max']}\n"
            f"📶 Gecikme: {status['latency']} ms\n"
            f"{giris_bilgi}"
        )
        color = discord.Color.green()
    else:
        description = (
            f"🔴 **Sunucu Kapalı!**\n"
            f"Hata: {status['error']}\n"
            f"{giris_bilgi}"
        )
        color = discord.Color.red()

    embed = discord.Embed(
        title=f"{SERVERNAME} Sunucu Durumu: ",
        description=description,
        color=color
    )
    embed.set_footer(text="TitanyumTPSX - Otomatik Sunucu İzleyici")
    return embed

@bot.event
async def on_ready():
    global status_message

    print(f"✅ Bot giriş yaptı: {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print("❌ Kanal bulunamadı.")
        return

    try:
        async for msg in channel.history(limit=100):
            if msg.author == bot.user and msg.embeds:
                if msg.embeds[0].title and msg.embeds[0].title.startswith("Minecraft Sunucu Durumu:"):
                    await msg.delete()
    except Exception as e:
        print("❌ Eski mesajları silerken hata:", e)

    status = await fetch_server_status(SERVER_IP)
    embed = create_embed(status)
    status_message = await channel.send(embed=embed)

    while True:
        await asyncio.sleep(CHECK_INTERVAL)
        status = await fetch_server_status(SERVER_IP)
        embed = create_embed(status)
        try:
            await status_message.edit(embed=embed)
        except Exception as e:
            print("❌ Mesaj düzenlenemedi:", e)

@bot.command(name="giris")
async def giris_komutu(ctx, tip: str, durum: str):
    global giris_durum, status_message

    tip = tip.lower()
    durum = durum.lower()

    if tip not in ["yurtici", "yurtdisi"]:
        await ctx.send("❌ Geçersiz giriş tipi! `yurtici` veya `yurtdisi` yaz.")
        return
    if durum not in ["aktif", "pasif"]:
        await ctx.send("❌ Geçersiz durum! `aktif` veya `pasif` yaz.")
        return

    giris_durum[tip] = (durum == "aktif")
    await ctx.send(f"✅ `{tip}` durumu `{durum}` olarak ayarlandı.")

    status = await fetch_server_status(SERVER_IP)
    embed = create_embed(status)
    try:
        await status_message.edit(embed=embed)
    except Exception as e:
        print("❌ Mesaj düzenlenemedi:", e)

bot.run(TOKEN)
