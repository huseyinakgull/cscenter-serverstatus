from discord_webhook import DiscordWebhook, DiscordEmbed
import requests

webhook_url = ''
EmbedBaslik = "quecytest" 
ipadresi = ''

oyuncu_url = f"https://cs.center/api/{ipadresi}/27015/GetPlayerInfo"
oyuncu_cevap = requests.get(oyuncu_url)

sunucu_url = f"https://cs.center/api/{ipadresi}/27015/GetServerInfo"
sunucu_cevap = requests.get(sunucu_url)

if oyuncu_cevap.status_code == 200 and sunucu_cevap.status_code == 200:
    oyuncu_veri = oyuncu_cevap.json()
    if oyuncu_veri.get("success") == "true":
        oyuncu_bilgi = oyuncu_veri.get("data")[0]
        oyuncu_embed = DiscordEmbed(title="Oyuncu Bilgileri", color=0x00ff00)
        for oyuncu in oyuncu_bilgi:
            oyuncu_adi = oyuncu["Name"]
            oyuncu_fragman = oyuncu["Frags"]
            oyuncu_sure = oyuncu["TimeF"]
            oyuncu_embed.add_embed_field(name=oyuncu_adi, value=f"Frags: {oyuncu_fragman}, Süre: {oyuncu_sure}", inline=False)

    sunucu_veri = sunucu_cevap.json()
    if sunucu_veri.get("success") == "true":
        sunucu_bilgi = sunucu_veri.get("data")
        sunucu_bilgi = sunucu_bilgi.get("0")

        sunucu_adi = sunucu_bilgi.get("HostName")
        harita_adi = sunucu_bilgi.get("Map")
        oyuncu_sayisi = sunucu_bilgi.get("Players")
        maks_oyuncu_sayisi = sunucu_bilgi.get("MaxPlayers")

        sunucu_embed = DiscordEmbed(title="Sunucu Bilgileri", color=0x00ff00)
        sunucu_embed.add_embed_field(name="Sunucu Adı", value=sunucu_adi)
        sunucu_embed.add_embed_field(name="Harita Adı", value=harita_adi)
        sunucu_embed.add_embed_field(name="Oyuncu Sayısı", value=f"{oyuncu_sayisi}/{maks_oyuncu_sayisi}")

    final_embed = DiscordEmbed(title=EmbedBaslik, color=0x00ff00)
    final_embed.add_embed_field(name="Sunucu Bilgileri", value="Sunucu Bilgileri:", inline=False)
    final_embed.add_embed_field(name="Sunucu Adı", value=sunucu_adi)
    final_embed.add_embed_field(name="Harita Adı", value=harita_adi)
    final_embed.add_embed_field(name="Oyuncu Sayısı", value=f"{oyuncu_sayisi}/{maks_oyuncu_sayisi}")
    final_embed.add_embed_field(name="Oyuncu Bilgileri", value="Oyuncu Bilgileri:", inline=False)
    for oyuncu in oyuncu_bilgi:
        oyuncu_adi = oyuncu["Name"]
        oyuncu_fragman = oyuncu["Frags"]
        oyuncu_sure = oyuncu["TimeF"]
        final_embed.add_embed_field(name=oyuncu_adi, value=f"Frags: {oyuncu_fragman}, Süre: {oyuncu_sure}", inline=False)
    webhook = DiscordWebhook(url=webhook_url)
    webhook.add_embed(final_embed)
    webhook.execute()

else:
    print("Sayfa yüklenemedi. HTTP Durum Kodu (OyuncuBilgi):", oyuncu_cevap.status_code)
    print("Sayfa yüklenemedi. HTTP Durum Kodu (SunucuBilgi):", sunucu_cevap.status_code)
