import discord
import discord.utils
import time
from tools import (get_zealy_api_data, logger, subdomain, x_api_key,
                   nft_drop_quest_id, discord_bot_key)

intents = discord.Intents.default()
intents.members = True # enable the members intent

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    print(f"Connected to {len(client.guilds)} guild(s):")
    for guild in client.guilds:
        print(f"- {guild.name} (ID: {guild.id})")
    await get_nft_winners()


async def give_role(member_id):
    role_id = 1083679827489476688  # The role ID
    guild_id = 397872799483428865 # replace with the actual guild ID
    guild = client.get_guild(guild_id)
    role = guild.get_role(role_id)
    members_with_role = role.members
    logger.debug(f"Total members with Arr role {len(members_with_role)}")
    if role is None:
        logger.error(f"Role with ID {role_id} not found in guild with ID {guild_id}")
        return
    logger.debug(f"{member_id} id in function")
    member = guild.get_member(int(member_id))
    if member is None:
        logger.error(f"Member with ID {member_id} not found in guild with ID {guild_id}")
        return

    if role in member.roles:
        logger.info(f"Member {member_id} already has role {role.name}")
        return

    await member.add_roles(role)
    logger.info(f"Role '{role.name}' given to member {member_id}")

async def get_nft_winners():
    """
    This function retrieves the list of the winners of the NFT airdrop by
    querying the Zealy API with a specific quest ID and status.
    Returns a list of user IDs who completed the NFT airdrop quest successfully.

    Args:
    None

    Returns:
    list: A list of user IDs who successfully completed the NFT airdrop quest.

    Example:
    >>> get_nft_winners()
    [123, 456, 789]
    """
    logger.info("Get the list of the NFT winners")
    status = "success"
    nft_airdrop_quest_completers = get_zealy_api_data(
        subdomain,
        x_api_key,
        nft_drop_quest_id,
        status
        )
    nft_airdrop_user_ids = []
    for item in nft_airdrop_quest_completers['data']:
        nft_airdrop_user_id = item['user']['discordId']
        nft_airdrop_user_ids.append(nft_airdrop_user_id)
    logger.debug("nft_airdrop_user_ids %s", nft_airdrop_user_ids)
        # Find the specific role by its name or ID
    for discord_user in nft_airdrop_user_ids:
        logger.debug(f"Discord user id {discord_user}")
        logger.debug(f"Total airdrop users {len(nft_airdrop_user_ids)}")
        await give_role(discord_user)
    return nft_airdrop_user_ids



client.run(discord_bot_key)
