#Config
prefix = "!!"
token = "Nzc5NjM3NDQwMjkzODk2MTkz.X7jb8g.NEDBhv8SvKTt0ouiuPN76mpvX1c"

from nextcord import embeds
import nextcord
import aiohttp
import json
from nextcord.ext import commands

bot = commands.Bot(command_prefix=prefix, status=nextcord.Status.dnd, activity=nextcord.Game(name=f"{prefix}help"), help_command=None)

app_ids = {
    1 : 755827207812677713,
    2 : 832012774040141894,
    3 : 878067389634314250,
    4 : 879863686565621790,
    5 : 852509694341283871,
    6 : 880218394199220334,
    7 : 832013003968348200,
    8 : 879863976006127627,
    9 : 773336526917861400,
    10 : 814288819477020702
}

def make(t, vcid):
    url = f"https://discord.com/api/v9/channels/{vcid}/invites"
    body = {
        "max_age": 86400,
        "max_uses": 0,
        "target_application_id": app_ids[t.lower()],
        "target_type": 2,
        "temporary": False,
        "validate": None
    }

    auth = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
    }

    code = json.loads((requests.post(url, data = json.dumps(body, separators=(',', ':'), ensure_ascii=True), headers = auth)).text)["code"]
    return f"https://discord.gg/{code}"

@bot.event
async def on_ready():
    print("Online")

@bot.command(name="invite")
async def invite(ctx):
    await ctx.send("https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=19457&scope=bot")

@bot.command(name="help")
async def help(ctx):
    emb = nextcord.Embed(title="Help command")
    print("Recieved command and initiated embed")
    emb.add_field(name="Command `play`:", value=f"""

1) Poker- Aliases:`poker`, `pokernight`
  -  Play Poker! 

2) Chess in the park- Aliases:`chess`, `Chess in the Park`
- Play Chess!

3) Doodle Crew- Aliases: `skribble`, `doodle`, `doodlecrew`, `dc`
    - Basically skribbl.io

4) `Letter Tile`: A game like scrabble! `scrabble` `Letter Tile`, `lt`
5) `Spellcast`:
6) Youtube Together (Everyone can access, i.e. add/remove video, play/pause etc)
7) Watch Together (Only host can access, host can share or hand over the \"remote\")
8) `Checkers in the park`: Play Checkers! `checkers`, `checkersinthepark`
9) `Wordsnacks`: A unique discord VC Game, try it out! `word snacks` `ws`
10) `Betrayal.io`: The VC version of the web version `btrio` `btr` `betrayal`
11) `Fishington.io`: The VC version of the web version `fish` `fishington` `ftio`

Join a voice channel and type out the command `{prefix}play`
Reply with the number corresponding with the game you wish to play.
Click on the link the bot responds with.
""")
    await ctx.send(embed=emb)

@bot.command(name="play")
async def play(ctx, game=None):
    if game is None:
        await ctx.reply('''
    Which game do you want to play?
    1) Poker
    2) Chess in the park
    3) Doodle Crew
    4) Letter Tile
    5) Spellcast
    6) Youtube Together
    7) Checkers in the park
    8) Wordsnacks
    9) Betrayal.io
    10) Fishington.io
    
    Reply with the number corresponding to the game you wish to play. JUST THE NUMBER FOR GODS SAKE.
    ''')
        def check(m):
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
        msg = await bot.wait_for("message", check=check)
    else:
        msg = ctx.message.content

    try:
        if int(msg) < 9: game = int(msg)
    except:
        return await ctx.send('imagine knowing your numbers.')

    voiceChannel = ctx.author.voice.channel
    if voiceChannel is not None:
        await ctx.send(f"Click on this link: {make(game, voiceChannel.id)}")
    else:
        await ctx.send("Connect to a voice channel first")

bot.run(token)
