# pylint: disable=C0103, C0116, C0301, W1401, W0702, C0111, W1203, E0401, W0613, W0611, C0104, W0201, W0105, W0621, W0603, W0718, W0612
'''
########
Cartographer v0.1
########
'''

import json
import discord
from discord.ext import commands

EXPLORER_ROLE_ID = 1135984735584256130
CARTOGRAPHER_ROLE_ID = 1134900047419555880
PAYLOAD_MESSAGE_ID = 1137815682491351081


file_path = "data/resources.json"


try:
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
except FileNotFoundError as e:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"Error opening file: {e}")


#Adding existing resource coordinates to resources.json file
@commands.command()
async def coordadd(ctx, *, item_name_coordinates):
    await ctx.message.delete()

    # Check if the user has the required role
    cartographer_role = discord.utils.get(ctx.guild.roles, id=CARTOGRAPHER_ROLE_ID)
    if cartographer_role not in ctx.author.roles:
        await ctx.send("You don't have permission to use this command.", delete_after=5)
        return

    # Separate the item name and coordinates using the last occurrence of space
    last_space_index = item_name_coordinates.rindex(' ')
    item_name = item_name_coordinates[:last_space_index]
    coordinates_str = item_name_coordinates[last_space_index+1:]

    # Split the coordinates by commas and strip spaces from each value
    lat_lng = [coord.strip() for coord in coordinates_str.strip('()').split(',')]

    if len(lat_lng) == 2:
        try:
            lat, lng = map(float, lat_lng)
        except ValueError:
            await ctx.send("Invalid coordinates format.", delete_after=5)
            return

        # Convert the item name to lowercase (or uppercase) for case-insensitive comparison
        item_name = item_name.lower()

        # Check if the item name exists in the list (using case-insensitive comparison)
        item_to_add = next((item for item in data if item['name'].lower() == item_name), None)

        if not item_to_add:
            await ctx.send(f"The item '{item_name}' does not exist in the list.", delete_after=5)
            return

        # Add the new location to the 'locations' array
        item_to_add['locations'].append({"lat": lat, "lng": lng})

        # Write the updated data back to the JSON file
        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=2)

        await ctx.send(f"New location for '{item_name}' has been added: ({lat:.3f}, {lng:.3f})", delete_after=5)

    else:
        await ctx.send("Invalid coordinates format. Use (xxx.xxx, xxx.xxx) format.", delete_after=5)



# Removing existing resource coordinates from resources.json file
@commands.command()
async def coordrem(ctx, *, item_name_coordinates):
    await ctx.message.delete()

    # Check if the user has the required role
    cartographer_role = discord.utils.get(ctx.guild.roles, id=CARTOGRAPHER_ROLE_ID)
    if cartographer_role not in ctx.author.roles:
        await ctx.send("You don't have permission to use this command.", delete_after=5)
        return

    # Separate the item name and coordinates using the last occurrence of space
    last_space_index = item_name_coordinates.rindex(' ')
    item_name = item_name_coordinates[:last_space_index]
    coordinates_str = item_name_coordinates[last_space_index+1:]

    # Split the coordinates by commas and strip spaces from each value
    lat_lng = [coord.strip() for coord in coordinates_str.strip('()').split(',')]

    if len(lat_lng) == 2:
        try:
            lat, lng = map(float, lat_lng)
        except ValueError:
            await ctx.send("Invalid coordinates format.", delete_after=5)
            return

        # Convert the item name to lowercase (or uppercase) for case-insensitive comparison
        item_name = item_name.lower()

        # Check if the item name exists in the list (using case-insensitive comparison)
        item_to_remove = next((item for item in data if item['name'].lower() == item_name), None)

        if not item_to_remove:
            await ctx.send(f"The item '{item_name}' does not exist in the list.", delete_after=5)
            return

        # Check if the location exists in the 'locations' array for the item
        location_to_remove = next((loc for loc in item_to_remove['locations'] if loc['lat'] == lat and loc['lng'] == lng), None)

        if not location_to_remove:
            await ctx.send(f"The location ({lat:.3f}, {lng:.3f}) does not exist for '{item_name}'.", delete_after=5)
            return

        # Remove the location from the 'locations' array
        item_to_remove['locations'].remove(location_to_remove)

        # Write the updated data back to the JSON file
        with open(file_path, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=2)

        await ctx.send(f"Location ({lat:.3f}, {lng:.3f}) has been removed from '{item_name}'.", delete_after=5)
    else:
        await ctx.send("Invalid coordinates format. Use (xxx.xxx, xxx.xxx) format.", delete_after=5)



# Add bulk existing resources to resources.json file
@commands.command()
async def addbulk(ctx: commands.Context, *, items: str):
    # Check if the user has the required role
    cartographer_role = discord.utils.get(ctx.guild.roles, id=CARTOGRAPHER_ROLE_ID)
    if cartographer_role not in ctx.author.roles:
        await ctx.send("You don't have permission to use this command.\nPlease sign up to be a cartographer.", delete_after=5)
        return

    # Split the input into lines to handle multiple items
    items_list = items.splitlines()

    for item_data in items_list:
        # Separate the item name and coordinates using the last occurrence of space
        last_space_index = item_data.rindex(' ')
        item_name = item_data[:last_space_index]
        coordinates_str = item_data[last_space_index + 1:]

        # Split the coordinates by commas
        coordinates = coordinates_str.strip('()').split(',')

        if len(coordinates) == 2:
            lat_lng = [coord.strip() for coord in coordinates]
            try:
                lat, lng = map(float, lat_lng)
            except ValueError:
                await ctx.send(f"Invalid coordinates format for '{item_name}'. Skipping...", delete_after=5)
                continue

            # Convert the item name to lowercase (or uppercase) for case-insensitive comparison
            item_name = item_name.lower()

            # Check if the item name exists in the list (using case-insensitive comparison)
            item_to_add = next((item for item in data if item['name'].lower() == item_name), None)

            if not item_to_add:
                await ctx.send(f"The item '{item_name}' does not exist in the list. Skipping...", delete_after=5)
                continue

            # Add the new location to the 'locations' array
            item_to_add['locations'].append({"lat": lat, "lng": lng})

            # Write the updated data back to the JSON file
            with open(file_path, 'w', encoding="utf-8") as file:
                json.dump(data, file, indent=2)

            await ctx.send(f"New location for '{item_name}' has been added: ({lat:.3f}, {lng:.3f})", delete_after=10)
        else:
            await ctx.send(f"Invalid coordinates format for '{item_name}'. Skipping...", delete_after=5)



# Path to the players.json file
player_path = "data/players.json"

# Load player data from players.json
def load_player_data():
    try:
        with open(player_path, 'r', encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as e:
        print(f"File not found: {player_path}")
        return []
    except Exception as e:
        print(f"Error opening file: {e}")
        return []

# Save player data to players.json
def save_player_data(data):
    try:
        with open(player_path, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=2)
    except Exception as e:
        print(f"Error saving data: {e}")


# Add player locations to Player file
@commands.command()
async def playeradd(ctx, player_name, *, coordinates_str):
    await ctx.message.delete()
    # Check if the user has the required role
    cartographer_role = discord.utils.get(ctx.guild.roles, id=CARTOGRAPHER_ROLE_ID)
    if cartographer_role not in ctx.author.roles:
        await ctx.send("You don't have permission to use this command.", delete_after=5)
        return

    # Load player data
    data = load_player_data()

    # Convert the player_name to lowercase (or uppercase) for case-insensitive comparison
    player_name = player_name.lower()

    # Check if the player_name exists in the list (using case-insensitive comparison)
    player_data = next((p for p in data if p['name'].lower() == player_name), None)

    # If player doesn't exist, create a new entry
    if not player_data:
        player_data = {
            'name': player_name, 
            'category': 'Players',
            'locations': []}
        data.append(player_data)

    # Split the coordinates by commas and strip spaces from each value
    lat_lng = [coord.strip() for coord in coordinates_str.strip('()').split(',')]

    if len(lat_lng) == 2:
        try:
            lat, lng = map(float, lat_lng)
        except ValueError:
            await ctx.send("Invalid coordinates format.", delete_after=5)
            return

        # Add the new location to the 'locations' array
        player_data['locations'].append({"lat": lat, "lng": lng})

        # Save player data
        save_player_data(data)

        await ctx.send(f"New location for '{player_name}' has been added: ({lat:.3f}, {lng:.3f})", delete_after=5)
    else:
        await ctx.send("Invalid coordinates format. Use (xxx.xxx, xxx.xxx) format.", delete_after=5)



# Remove player locations from Player file
@commands.command()
async def playerrem(ctx, player_name, *, coordinates_str):
    await ctx.message.delete()
    # Check if the user has the required role
    cartographer_role = discord.utils.get(ctx.guild.roles, id=CARTOGRAPHER_ROLE_ID)
    if cartographer_role not in ctx.author.roles:
        await ctx.send("You don't have permission to use this command.", delete_after=5)
        return

    # Load player data
    data = load_player_data()

    # Convert the player_name to lowercase (or uppercase) for case-insensitive comparison
    player_name = player_name.lower()

    # Check if the player_name exists in the list (using case-insensitive comparison)
    player_data = next((p for p in data if p['name'].lower() == player_name), None)

    if not player_data:
        await ctx.send(f"The player '{player_name}' does not exist in the list.", delete_after=5)
        return

    # Split the coordinates by commas and strip spaces from each value
    lat_lng = [coord.strip() for coord in coordinates_str.strip('()').split(',')]

    if len(lat_lng) == 2:
        try:
            lat, lng = map(float, lat_lng)
        except ValueError:
            await ctx.send("Invalid coordinates format.", delete_after=5)
            return

        # Check if the location exists in the 'locations' array for the player
        location_to_remove = next((loc for loc in player_data['locations'] if loc['lat'] == lat and loc['lng'] == lng), None)

        if not location_to_remove:
            await ctx.send(f"The location ({lat:.3f}, {lng:.3f}) does not exist for '{player_name}'.", delete_after=5)
            return

        # Remove the location from the 'locations' array
        player_data['locations'].remove(location_to_remove)

        # Save player data
        save_player_data(data)

        await ctx.send(f"Location ({lat:.3f}, {lng:.3f}) has been removed from '{player_name}'.", delete_after=5)
    else:
        await ctx.send("Invalid coordinates format. Use (xxx.xxx, xxx.xxx) format.", delete_after=5)



# Add bulk players to player file
@commands.command()
async def playerbulk(ctx: commands.Context, *, items: str):
    # Check if the user has the required role
    cartographer_role = discord.utils.get(ctx.guild.roles, id=CARTOGRAPHER_ROLE_ID)
    if cartographer_role not in ctx.author.roles:
        await ctx.send("You don't have permission to use this command.\nPlease sign up to be a cartographer.", delete_after=5)
        return

    # Load player data
    data = load_player_data()

    # Split the input into lines to handle multiple items
    items_list = items.splitlines()

    for item_data in items_list:
        # Separate the player_name and coordinates using the last occurrence of space
        last_space_index = item_data.rindex(' ')
        player_name = item_data[:last_space_index]
        coordinates_str = item_data[last_space_index + 1:]

        # Convert the player_name to lowercase (or uppercase) for case-insensitive comparison
        player_name = player_name.lower()

        # Check if the player_name exists in the list (using case-insensitive comparison)
        player_data = next((p for p in data if p['name'].lower() == player_name), None)

        # If player doesn't exist, create a new entry
        if not player_data:
            player_data = {
                'name': player_name,
                'category': 'Players',
                'locations': []
            }
            data.append(player_data)

        # Split the coordinates by commas and strip spaces from each value
        lat_lng = [coord.strip() for coord in coordinates_str.strip('()').split(',')]

        if len(lat_lng) == 2:
            try:
                lat, lng = map(float, lat_lng)
            except ValueError:
                await ctx.send(f"Invalid coordinates format for '{player_name}'. Skipping...", delete_after=5)
                continue

            # Add the new location to the 'locations' array
            player_data['locations'].append({"lat": lat, "lng": lng})

            # Save player data
            save_player_data(data)

            await ctx.send(f"New location for '{player_name}' has been added: ({lat:.3f}, {lng:.3f})", delete_after=10)
        else:
            await ctx.send(f"Invalid coordinates format for '{player_name}'. Skipping...", delete_after=5)



# Adding a new base resource to resources.json file
@commands.command()
async def rscadd(ctx, *, input_data):
    await ctx.message.delete()

    # Check if the user has the required role
    cartographer_role = discord.utils.get(ctx.guild.roles, id=CARTOGRAPHER_ROLE_ID)
    if cartographer_role not in ctx.author.roles:
        await ctx.send("You don't have permission to use this command.", delete_after=5)
        return

    # Split input_data into item name and category
    try:
        item_name, category = map(str.strip, input_data.split(','))
    except ValueError:
        await ctx.send("Invalid input format. Use: <item_name>, <category>", delete_after=5)
        return

    # Convert the item name to lowercase for case-insensitive comparison
    item_name = item_name.lower()

    # Check if the item name already exists in the list
    existing_item = next((item for item in data if item['name'].lower() == item_name), None)

    if existing_item:
        await ctx.send(f"The item '{item_name}' already exists in the list.", delete_after=5)
        return

    # Add the new item to the data list
    new_item = {
        "name": item_name,
        "category": category,
        "locations": []
    }
    data.append(new_item)

    # Write the updated data back to the JSON file
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    await ctx.send(f"New item '{item_name}' with category '{category}' has been added to the list.", delete_after=5)


async def setup(bot):
    bot.add_command(coordadd)
    bot.add_command(coordrem)
    bot.add_command(addbulk)
    bot.add_command(playeradd)
    bot.add_command(playerrem)
    bot.add_command(playerbulk)
    bot.add_command(rscadd)
