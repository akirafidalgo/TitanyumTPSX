import discord
import asyncio
import json
from mcstatus import MinecraftServer

# Yapılandırmayı yükle
with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config["token"]
GUILD_ID = int(config["guild_id"])
CHANNEL_ID = int(config["channel_id"])
SERVER_IP = config["server_ip"]
CHECK_INTERVAL = int(config.get("check_interval", 120))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

status_message = None  # Global mesaj nesnesi

async def fetch_server_status(ip):
    try:
        server = MinecraftServer.lookup(ip)
        status = server.status()
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

@client.event
async def on_ready():
    global status_message

    print(f"Bot giriş yaptı: {client.user}")
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print("❌ Kanal bulunamadı. Kanal ID'si doğru mu?")
        return

    # İlk mesaj gönderme
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

def create_embed(status):
    if status["online"]:
        description = (
            f"🟢 **Sunucu Çevrimiçi!**\n"
            f"👥 Oyuncular: {status['players_online']} / {status['players_max']}\n"
            f"📶 Gecikme: {status['latency']} ms"
        )
        color = discord.Color.green()
    else:
        description = f"🔴 **Sunucu Kapalı!**\nHata: {status['error']}"
        color = discord.Color.red()

    embed = discord.Embed(
        title=f"Minecraft Sunucu Durumu: `{SERVER_IP}`",
        description=description,
        color=color
    )
    embed.set_footer(text="TitanyumTPSX - Otomatik Sunucu İzleyici")
    return embed

client.run(TOKEN)
