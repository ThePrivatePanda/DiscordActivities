import nextcord
from nextcord.utils import utcnow
from nextcord import Status
import config

status_dict = {
    "dnd": Status.dnd,
    "idle": Status.idle,
    "online": Status.online,
    "offline": Status.offline,
}


client = nextcord.Client(
    status=status_dict.get(config.status, Status.dnd),
    activity=nextcord.Game(name=config.activity),
    help_command=None,
)


@client.event
async def on_ready():
    print("Online")


@client.slash_command(
    name="invite",
    description="Get an invite link to invite me to a server.",
)
async def invite(interaction):
    await interaction.response.send_message(
        f"https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=2251673024&scope=bot%20applications.commands"
    )


@client.slash_command(
    name="helpme",
    description="Recieve some help about me",
)
async def help(interaction: nextcord.Interaction):
    emb = nextcord.Embed(title="Help command", colour=nextcord.Colour.blue())
    emb.add_field(
        name="Command `play`:",
        value=f"""
1) `Poker:`
-  Play Poker! 

2) `Chess in the park:`
- Play Chess!

3) `Doodle Crew:`
- Basically skribbl.io

4) `Letter Tile:`
- A game like scrabble! 

5) `Spellcast:`
- A unique game, play it and see!

6) `Awkword:`
- A unique game, play it and see!

7) `Youtube Together:`
- Everyone can access, i.e. add/remove video, play/pause etc.

8) `Watch Together:`
- Only host can access, host can share or hand over the \"remote\".

9) `Checkers in the park:`
- Play Checkers! 

10) `Wordsnacks:`
-  A unique discord VC Game, try it out!

11) `Betrayal.io:`
-  The VC version of the web version.

12) `Fishington.io:`
- The VC version of the web version.

""",
    )
    emb.add_field(
        name="__Usage:__",
        value=f"Join a voice channel and type out the command `/play`\nSelect the game you want to play from the **dropdown** and **click on the link the bot responds with**.",
        inline=False,
    )
    emb.add_field(
        name="Command `invite`:",
        value="Just run `/invite` to get a link to invite me to a server",
    )
    emb.set_footer(icon_url=interaction.user.display_avatar.url)
    emb.set_thumbnail(url=client.user.avatar.url)
    emb.timestamp = utcnow()
    await interaction.response.send_message(embed=emb, ephemeral=True)


async def make(user, game):
    invite = await user.voice.channel.create_invite(
        reason="Play game",
        unique=False,
        target_type=nextcord.InviteTarget.embedded_application,
        target_application_id=game,
    )
    return invite.url


@client.slash_command(
    name="playgame",
    description="Play a game!",
)
async def play_(
    interaction: nextcord.Interaction,
    game: str = nextcord.SlashOption(
        name="game",
        choices={
            "Poker": "755827207812677713",
            "Chess in the park": "832012774040141894",
            "Doodle Crew": "878067389634314250",
            "Letter Tile": "879863686565621790",
            "Spellcast": "852509694341283871",
            "Awkword": "879863881349087252",
            "Youtube Together": "755600276941176913",
            "Watch Together": "880218394199220334",
            "Checkers in the park": "832013003968348200",
            "Wordsnacks": "879863976006127627",
            "Betryal.io": "773336526917861400",
            "Fishington.io": "814288819477020702",
        },
        description="Choose the game you wish to play!",
    ),
):
    if not interaction.user.voice:
        return await interaction.response.send_message(
            "Connect to a voice channel.", ephemeral=True
        )
    return await interaction.response.send_message(
        await make(interaction.user, int(game)), ephemeral=False
    )


client.run(config.token)
