import os, random, threading, aiohttp, time, requests, asyncio, discord, httpx, socket, socks, cloudscraper, logging, ssl, hashlib
from datetime import datetime, timedelta
from discord.ext import commands
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from stem import Signal
from stem.control import Controller
from dotenv import load_dotenv

TOKEN = ""
PROXY_FILE = "proxies.txt"
CHANNEL_NAME = ""
THREAD_COUNT = 100
DURATION_MINUTES = 3

GQL_HEADERS = {
    "Accept": "application/vnd.twitchtv.v5+json",
    "Client-ID": "xejf7gte39bqsf915a9p8ja2nqxfrj",
    "Authorization": "OAuth 9cercg1ssunppf0lvmndvmpokxtyzi",
    "Content-Type": "text/plain;charset=UTF-8"
}

USHER_HEADERS = {
    "Accept": "application/x-mpegURL, application/vnd.apple.mpegurl, application/json, text/plain",
    "Sec-Fetch-Mode": "cors"
}

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def load_proxies():
    if not os.path.exists(PROXY_FILE):
        raise FileNotFoundError(f"Proxy file {PROXY_FILE} not found")
    
    with open(PROXY_FILE, 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    
    if not proxies:
        raise ValueError("No proxies found in the proxy file")
    
    return proxies

def substring(text, start, end, start_index=0, comparison=None, default=None):
    try:
        start_pos = text.index(start, start_index) + len(start)
        end_pos = text.index(end, start_pos)
        return text[start_pos:end_pos]
    except ValueError:
        return default or ""
    

def send_view_request(proxy, channel_name):
    try:
        USER_AGENT_POOL = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
            "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 13; SM-G781B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.5; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Mozilla/5.0 (X11; Linux i686; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPod touch; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-F936B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-F721B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-A336B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-M536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-M336B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-X906B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-X700B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-X500B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-X300B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Safari/537.36"
        ]

        proxies = {
            "http": proxy,
            "https": proxy
        }
        
        session = requests.Session()
        session.proxies = proxies
        session.timeout = 50

        selected_user_agent = random.choice(USER_AGENT_POOL)

        GQL_HEADERS_ENHANCED = {
            "Accept": "application/vnd.twitchtv.v5+json",
            "Client-ID": "xejf7gte39bqsf915a9p8ja2nqxfrj",
            "Authorization": "OAuth 9cercg1ssunppf0lvmndvmpokxtyzi",
            "Content-Type": "text/plain;charset=UTF-8",
            "User-Agent": selected_user_agent,
            "Origin": "https://www.twitch.tv",
            "Referer": f"https://www.twitch.tv/{channel_name}",
            "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "X-Device-Id": "".join(random.choices("abcdef0123456789", k=32)),
            "X-Request-Id": "".join(random.choices("abcdef0123456789", k=32)),
            "X-Forwarded-For": ".".join()(str, (random.randint(1, 255) for _ in range(4)))
        }

        gql_payload = {
            "operationName": "PlaybackAccessToken_Template",
            "query": """query PlaybackAccessToken_Template($login: String!, $isLive: Boolean!, $vodID: ID!, $isVod: Boolean!, $playerType: String!) {
                streamPlaybackAccessToken(channelName: $login, params: {platform: "web", playerBackend: "mediaplayer", playerType: $playerType}) @include(if: $isLive) {
                    value
                    signature
                    __typename
                }
                videoPlaybackAccessToken(id: $vodID, params: {platform: "web", playerBackend: "mediaplayer", playerType: $playerType}) @include(if: $isVod) {
                    value
                    signature
                    __typename
                }
            }""",
            "variables": {
                "isLive": True,
                "login": channel_name,
                "isVod": False,
                "vodID": "",
                "playerType": "site"
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "0828119ded1c13477966434e15800ff57ddacf13ba1911c129dc2200705b0712"
                }
            }
        }
        
        response = session.post(
            "https://gql.twitch.tv/gql",
            json=gql_payload,
            headers=GQL_HEADERS_ENHANCED
        )
        response_data = response.json()
        
        value = substring(str(response_data), 'value":"', '","signature').replace("\\", "").replace("u0026", "\\u0026").replace("+", "%2B").replace(":", "%3A").replace(",", "%2C").replace("[", "%5B").replace("]", "%5D").replace("'", "%27")
        signature = substring(str(response_data), 'signature":"', '","__typename')
        
        if not value or not signature:
            print(f"Failed to get token/signature with proxy {proxy}")
            return
        
        USHER_HEADERS_ENHANCED = {
            "Accept": "application/x-mpegURL, application/vnd.apple.mpegurl, application/json, text/plain",
            "Sec-Fetch-Mode": "cors",
            "User-Agent": selected_user_agent,
            "Origin": "https://www.twitch.tv",
            "Referer": f"https://www.twitch.tv/{channel_name}",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "DNT": "1",
            "Sec-GPC": "1",
            "X-Player-Type": "site",
            "X-Player-Version": "1.10.0",
            "X-Forwarded-For": ".".join()(str, (random.randint(1, 255) for _ in range(4)))
        }
        
        usher_url = f"https://usher.ttvnw.net/api/channel/hls/{channel_name}.m3u8?allow_source=true&fast_bread=true&p=8220969&play_session_id=4b8aff3033c5df69b141ca7678327fb4&player_backend=mediaplayer&playlist_include_framerate=true&reassignments_supported=true&sig={signature}&supported_codecs=avc1&token={value}&cdm=wv&player_version=1.10.0"
        
        usher_response = session.get(usher_url, headers=USHER_HEADERS_ENHANCED)
        usher_content = usher_response.text
        
        video_weaver_base = substring(usher_content, "https://video-weaver", ".m3u8")
        if not video_weaver_base:
            print(f"Failed to parse video-weaver URL with proxy {proxy}")
            return
            
        video_weaver_url = f"https://video-weaver{video_weaver_base}.m3u8"
        weaver_response = session.get(video_weaver_url, headers=USHER_HEADERS_ENHANCED)
        weaver_content = weaver_response.text
        
        edge_url = substring(weaver_content, "#EXT-X-TWITCH-PREFETCH:", ".ts") + ".ts"
        if not edge_url:
            print(f"Failed to parse edge URL with proxy {proxy}")
            return
            
        FINAL_HEADERS = {
            **USHER_HEADERS_ENHANCED,
            "Accept": "*/*",
            "Host": edge_url.split("/")[2],
            "Range": "bytes=0-1024",
            "X-Requested-With": "XMLHttpRequest",
            "X-Forwarded-Proto": "https",
            "TE": "trailers"
        }
        
        EXTRA_POWER_HEADERS = {
            "Sec-Ch-Ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Ch-Ua-Full-Version": '"123.0.6312.58"',
            "Sec-Ch-Ua-Arch": '"x86"',
            "Sec-Ch-Ua-Bitness": '"64"',
            "Sec-Ch-Ua-Model": '""',
            "Sec-Ch-Ua-Platform-Version": '"15.0.0"',
    
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Proto": "https",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Host": "www.twitch.tv",
            "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
            "X-Real-IP": f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
            "X-Client-Version": "1.10.0",
            "X-Device-Id": f"{random.randint(1000000000000000, 9999999999999999)}",
            "X-Request-Id": f"{random.randint(1000000000000000, 9999999999999999)}",
    
            "X-Client-Request-Id": f"REQ-{random.randint(1000000000000000, 9999999999999999)}",
            "X-Client-Session-Id": f"SESS-{random.randint(1000000000000000, 9999999999999999)}",
            "X-Client-Connection-Id": f"CONN-{random.randint(1000000000000000, 9999999999999999)}",
            "X-Twitch-Client-Version": "1.10.0",
            "X-Twitch-Client-Request-Id": f"TWITCH-REQ-{random.randint(1000000000000000, 9999999999999999)}",
    
            "Save-Data": "off",
            "DNT": "1",
            "Priority": "u=1, i",
            "Device-Memory": "8",
            "Downlink": "10",
            "ECT": "4g",
            "RTT": "50",
            "Viewport-Width": "1920",
            "Width": "1920",
    
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,fr;q=0.8,de;q=0.7",
            "Accept-CH": "Sec-CH-UA-Arch, Sec-CH-UA-Bitness, Sec-CH-UA-Model, Sec-CH-UA-Platform-Version",
    
            "Alt-Svc": 'h3=":443"; ma=86400, h3-29=":443"; ma=86400',
            "Early-Data": "1",
    
            "X-Twitch-Locale": "en-US",
            "X-Twitch-Timezone": "UTC",
            "X-Twitch-Client-Device-Id": f"DEV-{random.randint(1000000000000000, 9999999999999999)}",
            "X-Twitch-Client-Advertising-Id": f"ADV-{random.randint(1000000000000000, 9999999999999999)}"
        }

        session.head(edge_url, headers=FINAL_HEADERS)
        print(f"Successfully sent view with proxy {proxy}")
        
    except Exception as e:
        print(f"Error with proxy {proxy}: {str(e)}")

def run_viewer(channel_name, duration_minutes):
    proxies = load_proxies()
    end_time = datetime.now() + timedelta(minutes=duration_minutes)
    
    while datetime.now() < end_time:
        threads = []
        for _ in range(THREAD_COUNT):
            proxy = random.choice(proxies)
            t = threading.Thread(target=send_view_request, args=(proxy, channel_name))
            t.start()
            threads.append(t)
            time.sleep(0.1)
        
        for t in threads:
            t.join()
        
        time.sleep(2)

@bot.command(name='tview')
async def tview(ctx, channel_name: str, duration: int = DURATION_MINUTES):
    required_role = "Premium +"
    if not any(role.name == required_role for role in ctx.author.roles):
        embed = discord.Embed(
            description="You need the {required_role} to use this command!",
            color=0xb589cf
        )
        await ctx.send(embed=embed)
        return

    allowed_channel_id = 112839203821246
    if ctx.channel.id != allowed_channel_id:
        allowed_channel = bot.get_channel(allowed_channel_id)
        embed = discord.Embed(
            description=f"use this command in {allowed_channel.mention}!",
            color=0xb589cf
        )
        await ctx.send(embed=embed)
        return
    
    if duration <= 0 or duration > 120:
        embed = discord.Embed(
            description="on cooldown!",
            color=0xb589cf
        )
        await ctx.send(embed=embed)
        return
    
    global CHANNEL_NAME
    CHANNEL_NAME = channel_name
    
    embed = discord.Embed(
        description=f"➣ Sending {THREAD_COUNT} viewers to {channel_name}",
        color=0xb589cf
    )
    await ctx.send(embed=embed)
    
    log_channel = bot.get_channel("logs_twitch_views")
    if log_channel:
        log_embed = discord.Embed(
            title="👻 Boo View 👻",
            description=f"➣ <@{ctx.author.id}>, Sending viewers.\n\n"
                      f"🔥 **Target streamer channel:**\n"
                      f"{channel_name}\n\n"
                      f"📈 **Threads amount:**\n"
                      f"{THREAD_COUNT}\n\n"
                      f"⏳ **Number of minutes:**\n"
                      f"{DURATION_MINUTES}",
            color=0xb589cf
        )
        log_embed.set_footer(text="Powered by ghostaiotool.com")
        await log_channel.send(embed=log_embed)
    
    threading.Thread(
        target=run_viewer,
        args=(channel_name, duration),
        daemon=True
    ).start()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"Error starting bot: {e}")
