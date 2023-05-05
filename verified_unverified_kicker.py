import discord
import asyncio
from tools import discord_bot_key

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)    

unverified_role_name = "Unverified"
unverified_role_id = 1085941733302468630
verified_role_id = 411189981223059467

@client.event
async def on_ready():
    # Find the specific role by its name or ID
    specific_role = discord.utils.get(client.guilds[0].roles, name=unverified_role_name) or client.guilds[0].get_role(unverified_role_id)
    
    # Get all members with the specific role
    members_with_role = specific_role.members

    # Wait for 30 seconds for each member with the specific role and kick them
    for member in members_with_role:
        print(member.id)
        if discord.utils.get(member.roles, id=verified_role_id): # has Turing test passed
            # Member has verfied role, remove unverified role if present
            if discord.utils.get(member.roles, id=unverified_role_id):
                await member.remove_roles(client.guilds[0].get_role(unverified_role_id))
        else:
            # Member does not have verified role, kick them
            await asyncio.sleep(5)
            await member.kick(reason="Verification not completed, please join again and verify your account. https://discord.gg/iota \n It is not possible to continue with the quests on Zealy without verification.")
            print(member, "kicked", member.id)

client.run(discord_bot_key)
