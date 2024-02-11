# pylint: disable=C0103, C0116, C0301, W1401, W0702, C0111, W1203, E0401, W0613, W0611, C0104, W0201, W0105, W0621, W0603, W0718, W0612
'''
########
Cartographer Extensions - Embeds
########
'''

import json
import discord
from discord.ext import commands


file_path = r"data\resources.json"

try:
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
except FileNotFoundError as e:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"Error opening file: {e}")


explorer_role_message = discord.Embed(title="Explorer Role", description=
'''Anyone can sign up to be an Explorer! All that is asked of you is to explore the world and report resource locations as you discover them. If you are interested in being an explorer, react with ✅ below to be added to the Explorer role and open up additional channels. These channels include:

<#1134898424739799090> Submit existing resource coordinates for documentation (e.g., already in dropdowns) 
<#1135384960388304916> Submit newly discovered resources and coordinates (e.g., not in dropdowns)
<#1134910979990368296> General discussion channel for Explorers

Please note: We are currently documenting **clusters of resource nodes.** For example, we won't mark every blueberry bush but will mark a cluster of blueberry bushes.''', color=0xe5bd87)


welcome_message = discord.Embed(title="Welcome to Pax Dei Maps!", description=
'''If you're interested in exploring the world of Pax Dei, learn where resources can be found, or want to help others along the journey to explore the vast regions, welcome!

Our goal is the chart the lands of Pax Dei, gathering and documenting vital information along the way.

This currently includes resource and inhabitant locations but may expand in the future.

If you are interested in joining us as a cartographer, head to the <#1134897515607629844> channel and grab the Explorer role.''', color=0xe5bd87)

welcome_banner = discord.File("assets/PxD_Banner.gif", filename='banner.gif')


rules = discord.Embed(title="Rules", description=
'''1) Always remain respectful to other people, including our team.
2) Do not use slurs or defamatory language towards other members.
3) Any language that may discriminate against other people based on sex, gender, race, will lead to a ban.
4) Do not threaten anyone.
5) No advertisements without permission.
6) Trolling and/or harassing other members is prohibited.
7) Use English please!
8) Political or religious discussions are prohibited.
9) Do not share illegal or NSFW content.
## Be excellent to each other!''', color=0xe5bd87)



@commands.command()
async def exprole(ctx):
    await ctx.message.delete()
    await ctx.send(embed=explorer_role_message)

@commands.command()
async def ctwelcome(ctx):
    await ctx.message.delete()
    await ctx.send(embed=welcome_message)
    await ctx.send(file=welcome_banner)

@commands.command()
async def ctrules(ctx):
    await ctx.message.delete()
    await ctx.send(embed=rules)

@commands.command()
async def stats(ctx):
    await ctx.message.delete()

    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as e:
        await ctx.send(f"File not found: {file_path}")
        return
    except Exception as e:
        await ctx.send(f"Error opening file: {e}")
        return

    # Calculate statistics
    categories = set()  # Set to store unique categories
    items = set()  # Set to store unique item names
    num_locations_tracked = 0  # Initialize the total locations tracked counter
    category_totals = {}  # Dictionary to store category totals

    for item in data:
        category = item.get("category", "Uncategorized")
        categories.add(category)  # Add the category to the set of unique categories
        item_name = item.get("name", "Unnamed")
        items.add(item_name)  # Add the item name to the set of unique item names
        num_locations_in_item = len(item.get("locations", []))
        num_locations_tracked += num_locations_in_item

        if category not in category_totals:
            category_totals[category] = 0  # Initialize the category total as an integer
        category_totals[category] += num_locations_in_item  # Accumulate the locations

    # Create an embed to display the statistics
    embed = discord.Embed(
        title="Item Statistics",
        color=0x00f2fd,
    )

    # Add TOTALS section
    embed.add_field(name="TOTALS", value=f"Total number of categories: {len(categories)}\nTotal number of items: {len(items)}\nTotal number of locations tracked: {num_locations_tracked}", inline=False)

    # Add CATEGORY TOTALS section
    category_info = "\n".join([f"{category} -- {num_locations}" for category, num_locations in category_totals.items()])
    embed.add_field(name="CATEGORY TOTALS", value=category_info, inline=False)

    await ctx.send(embed=embed)



embed_list = {

    exprole,
    stats,
    ctwelcome,
    ctrules

}

async def setup(bot):
    for i in embed_list:
        bot.add_command(i)
