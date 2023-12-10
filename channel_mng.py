#Channel manager Ver.1.0
version = "1.0"

import discord
import argparse
from discord import app_commands
from discord.ext import commands
import traceback

TOKEN_dev    = 'hogehoge12345678'
TOKEN_prod   = 'hogehoge12345678'

Intents = discord.Intents.default()
Intents.members = True
client = discord.Client(activity=discord.Game('Ver.'+version),intents=Intents)
tree   = app_commands.CommandTree(client)


parser = argparse.ArgumentParser()
parser.add_argument('-p','--production',  action='store_true', default=False , help='Use when running in PRODUCTION ENVIRONMENT')
args   = parser.parse_args()

if args.production:
    TOKEN   = TOKEN_prod
    #print('This version is not available in production environment.')
    #exit()
else:
    TOKEN    = TOKEN_dev


print('Please wait, now launching...')

@client.event
async def on_ready():
    await tree.sync()
    print('Channel Management System Ver.' + version)
    print('When you want to operate me, type the command on the Discord message...')


@tree.command(name='create', description='Create a new channel')
@commands.has_permissions(administrator=True)
async def create(interaction: discord.Interaction, name: str, role_read: discord.Role, role_write: discord.Role, category: discord.CategoryChannel):#, \
                 #role_read2:  discord.Role = None, role_read3:  discord.Role = None, role_read4:  discord.Role = None, role_read5:  discord.Role = None, \
                # role_write2: discord.Role = None, role_write3: discord.Role = None, role_write4: discord.Role = None, role_write5: discord.Role = None):

    try:
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
            #interaction.guild.role_read:    discord.PermissionOverwrite(read_messages=True),
            interaction.guild.get_role(role_read.id):    discord.PermissionOverwrite(read_messages=True),
            interaction.guild.get_role(role_write.id):   discord.PermissionOverwrite(send_messages=True),
            interaction.guild.me:           discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        if category is None:
            category = interaction.channel.category

        await interaction.guild.create_text_channel(name, overwrites=overwrites, category=category)
        await interaction.response.send_message(f'Created a new channel: {name}')
    except:
        await interaction.response.send_message('Failed to create a new channel \n' + traceback.format_exc())

@tree.command(name='delete', description='Delete a channel')
@commands.has_permissions(administrator=True)
async def delete(interaction: discord.Interaction, channel: discord.TextChannel):
    try:
        await channel.delete()
        await interaction.response.send_message(f'Deleted a channel: {channel.name}')
    except:
        await interaction.response.send_message('Failed to delete a channel \n' + traceback.format_exc())

client.run(TOKEN)


