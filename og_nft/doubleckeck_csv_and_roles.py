import discord
import csv
import time

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

# Role list
# EOY: 1050341998927806525
# Repechage: 1028946896464658453
# Recipient: 1026401649272557641
specific_role_id = 1026401649272557641 # Replace with the ID of your specific role

@client.event
async def on_ready():
    # Find the specific role by its ID
    specific_role = discord.utils.get(client.guilds[0].roles, id=specific_role_id)
    
    # Get all members with the specific role
    members_with_role = specific_role.members
    
    # Print the IDs of all members with the specific role
    in_the_role = []
    for member in members_with_role:
        in_the_role.append(member.id)
    print(in_the_role)
    
    # Print the number of members with the specific role
    print(len(members_with_role))
    
    # Open the CSV file and read its contents
    with open('members.csv', 'r') as f:
        reader = csv.DictReader(f)
        not_in_the_role = []
        member_ids_in_csv = {int(row['User ID']) for row in reader}
        for row in reader:
            # Check if the member ID is in the dictionary
            member_id = int(row['User ID'])
            
            # Check if the member is in the specific role
            if any(member.id == member_id for member in members_with_role):
                print(f"Member {member_id} is in the CSV file and has the specific role")
            else:
                name = row['Name'] if 'Name' in row else "Unknown"
                print(f"Member {member_id} {name} is in the CSV file but does NOT have the specific role")
                not_in_the_role.append((member_id, name))

        # Loop through members in the specific role
        not_in_csv_set = []
        for member in members_with_role:
            if member.id not in member_ids_in_csv:
                not_in_csv_set.append((member.id, member))


        # Print the list of members in the role but not in the CSV file
        print(f"Members in the CSV file but not in the role: {len(not_in_the_role)}")

        for member_id, name in not_in_csv_set:
            member = client.get_user(member_id)
            if member:
                mention = member.mention
                message = f"{mention} is in the role '{specific_role.name}' but is NOT in the CSV file"
                print(message)
                # Send a message to a specific channel with the mention
                # Channel list
                # EOY: 1050348395832815656
                # Repechage: 1028946709612613682
                # Recipient: 1028938533450297344
                channel = client.get_channel(1028938533450297344) # Replace with the ID of your channel 

                await channel.send(f"Hello {mention}, please submit your SMR address to receive the OG NFT.\nNot doing so will make you uneligible for the airdrop and your NFT will be burned.")
                # print("not in the csv", mention)
                time.sleep(5)
            else:
                print(f"Could not find user with ID {member_id}")
            
client.run(TOKEN)
