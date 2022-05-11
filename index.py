import json

import discord
import discord.ext

import connect4
import monkeytype

botOn = True
client = discord.Client(command_prefix="/", intents=discord.Intents.all())

### OPENING bot_config.json ###
bot_config_file = open('config/bot_config.json', "r")
bot_config = json.load(bot_config_file)
bot_config_file.close()

### OPENING server_data.json ###
server_data_file = open('config/server_data.json', "r")
server_data = json.load(server_data_file)
server_data_file.close()

### OPENING user_data.json ###
user_data_file = open('config/user_data.json', "r")
user_data = json.load(user_data_file)
user_data_file.close()

### CREATING HELP COMMAND EMBED ###
helptxt = open('config/help.txt')
general_help_embed = discord.Embed(title=(bot_config["name"] + " Help Menu"), description=helptxt.read().replace("!prefix!", bot_config["prefix"]))
helptxt.close()

### OTHER GLOBAL VARIABLES ###
congames = []

### STARTUP LISTENER ###
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(bot_config)

### MESSAGE LISTENER ###
@client.event
async def on_message(message: discord.Message):
    ## BOT MESSAGE CANCELER ##
    if message.author == client.user:
        return

    ## USER COMMAND ##
    if message.content.startswith(bot_config["prefix"]):
        respondChannel = message.channel
        args = message.content.split()

        # shutdown command #
        if message.content.startswith(bot_config["prefix"] + 'shutdown'):
            # check if user is the bot owner
            if not (message.author.id == bot_config["botownerid"]):
                await respondChannel.send("Only the bot owner can use this command. Your userID is " + str(message.author.id) + ".")
                return
            
            botOn = False
            await respondChannel.send(embed=discord.Embed(title=bot_config["name"] + " is shuting down."))
            await client.close()
                

        # help command #
        elif message.content.startswith(bot_config["prefix"]+'help'):
            await respondChannel.send(embed=general_help_embed)

        # invitelink command #
        elif message.content.startswith(bot_config["prefix"]+'invitelink'):
            await respondChannel.send("https://discord.com/api/oauth2/authorize?client_id="+str(client.user.id)+"&permissions=8&scope=bot")

        # connect4 command #
        elif message.content.startswith(bot_config["prefix"]+'connect4'):
            gameMessage = await message.channel.send(embed=discord.Embed(title=message.author.name + " wants to play Connect4!",
                                                                 description="React to this message with a :thumbsup: to play!"))
            await gameMessage.add_reaction("👍")
            congames.append(connect4.connect4game(
                message.author.id, message.author.name, message.author, gameMessage.id))
        
        # monkeytypemanual command #
        elif message.content.startswith(bot_config["prefix"]+'monkeytypemanual'):
            # implement me
            f = open("config/monkeyTypeManual.txt", "r")
            await respondChannel.send(embed=discord.Embed(title="MonkeyType Module Manual", description=f.read().replace("!prefix!", bot_config['prefix'])))
            f.close()

        # setapekey command #
        elif message.content.startswith(bot_config["prefix"]+'setapekey'):
            userid = str(message.author.id)
            if len(args) != 2:
                await respondChannel.send("ERROR: Setapekey takes 1 option. Please refer to " + bot_config['prefix'] + "help")
                return
            
            # making spot in user_data
            if not (userid in user_data):
                user_data[userid] = {}
            if not ('monkeytype' in user_data[userid]):
                user_data[userid]['monkeytype'] = {}
            user_data[userid]['monkeytype']['apekey'] = args[1]
            
            await message.delete()

            user_data_file = open('config/user_data.json', "w")
            json.dump(user_data, user_data_file)
            user_data_file.close()

            await respondChannel.send("SUCCESS: Your apekey was set!")

        # monkeytypestats command #
        elif message.content.startswith(bot_config["prefix"]+'monkeytypestats'):
            # create default params
            userToLookup = str(message.author.id)
            mode = 'time'

            # parse args for options
            for i in range(len(args)):
                if args[i] == '--u':
                    try:
                        if args[i+1].startswith("<@"):
                            userToLookup = args[i+1][2:len(args[i+1]) - 1]
                        else:
                            userToLookup = args[i+1]
                    except:
                        await respondChannel.send("ERROR: --u must be followed by a user")
                        return
                elif args[i] == '--m':
                    try:
                        args[i+1] = args[i+1].lower()
                        modes = ['time','words']
                        if args[i+1] in modes:
                            mode = args[i+1]
                        else:
                            await respondChannel.send("ERROR: " + args[i+1] + " isn't a valid mode.\nOptions for mode are: time, words")
                            return
                    except:
                        await respondChannel.send("ERROR: --m must be followed by a mode\nOptions for mode are: time, words")
                        return
            
            # get user's apekey from user data
            apekey = ""
            if (not (userToLookup in user_data)) or (not ('monkeytype' in user_data[userToLookup])) or not ('apekey' in user_data[userToLookup]['monkeytype']):
                await respondChannel.send("ERROR: Seems that <@" + userToLookup + "> has not setup their ApeKey. Please refer to " + bot_config['prefix'] + "monkeytypemanual.")
                return
            apekey = user_data[userToLookup]['monkeytype']['apekey']
            
            # get stats and desired bests
            response = monkeytype.createStatsEmbedDescription(apekey, userToLookup, mode)
            if response == None:
                await respondChannel.send("ERROR: Failed to get data from MonkeyType API. Make sure the user's ApeKey is correct. Refer to " + bot_config['prefix'] + "monkeytypemanual for help.")
                return
            await respondChannel.send(embed=discord.Embed(description=response, image="https://dslv9ilpbe7p1.cloudfront.net/O9hOWcdog0uBs9vrAG2s5g_store_logo_image.png"))

        # monkeytypelast command #
        elif message.content.startswith(bot_config["prefix"]+'monkeytypelast'):
            # create default params
            userToLookup = str(message.author.id)

            # parse args for options
            for i in range(len(args)):
                if args[i] == '--u':
                    try:
                        if args[i+1].startswith("<@"):
                            userToLookup = args[i+1][2:len(args[i+1]) - 1]
                        else:
                            userToLookup = args[i+1]
                    except:
                        await respondChannel.send("ERROR: --u must be followed by a user")
                        return
            
            # get user's apekey from user data
            apekey = ""
            if (not (userToLookup in user_data)) or (not ('monkeytype' in user_data[userToLookup])) or not ('apekey' in user_data[userToLookup]['monkeytype']):
                await respondChannel.send("ERROR: Seems that <@" + userToLookup + "> has not setup their ApeKey. Please refer to " + bot_config['prefix'] + "monkeytypemanual.")
                return
            apekey = user_data[userToLookup]['monkeytype']['apekey']
            
            # get stats and desired bests
            response = monkeytype.createLastEmbedDescription(apekey, userToLookup)
            if response == None:
                await respondChannel.send("ERROR: Failed to get data from MonkeyType API. Make sure the user's ApeKey is correct. Refer to " + bot_config['prefix'] + "monkeytypemanual for help.")
                return
            await respondChannel.send(embed=discord.Embed(description=response, image="https://dslv9ilpbe7p1.cloudfront.net/O9hOWcdog0uBs9vrAG2s5g_store_logo_image.png"))

        # unknown command#
        else:
            await respondChannel.send("ERROR: Unknown command. Please refer to " + bot_config['prefix'] + "help")

### REACTION LISTENER ###
@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    ## CONNECT 4 ##
    for game in congames:
        # game.printvars()
        if game.messageid == reaction.message.id:
            numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
            # GAME HASN'T STARTED #
            if game.started == False:
                if reaction.emoji == "👍":
                    if user.id != game.player1id:
                        game.player2id = user.id
                        game.player2name = user.name
                        game.player2user = user
                        game.started = True
                        lol = await reaction.message.channel.send(embed=discord.Embed(title=game.player1name + " VS. " + game.player2name + " in Connect4!", description="<@" + str(game.player2id) + "> accepted <@" + str(game.player1id) + ">'s invite for Connect4.\n\n" + game.gametostring() + "\n<@" + str(game.player1id) + ">'s move."))
                        for i in numbers:
                            await lol.add_reaction(i)
                        game.messageid = lol.id
                        await reaction.message.delete()
                    else:
                        await user.send("Wow, can't even get Wumpus to play with you? :'(")
            # GAME IS STARTED #
            else:
                if ((game.curplayer == 1 and user.id == game.player1id) or (game.curplayer == 2 and user.id == game.player2id)):
                    for i in range(len(numbers)):
                        if reaction.emoji == numbers[i]:
                            winner = game.placepiece(i)
                            await reaction.message.delete()
                            if winner != 0:
                                if winner == 1:
                                    await reaction.message.channel.send(embed=discord.Embed(title=game.player1name + " wins!", description="<@" + str(game.player2id) + "> loses. :(\n\n" + game.gametostring()))
                                else:
                                    await reaction.message.channel.send(embed=discord.Embed(title=game.player2name + " wins!", description="<@" + str(game.player1id) + "> loses. :(\n\n" + game.gametostring()))
                                del game
                            else:
                                if game.curplayer == 2:
                                    lol = await reaction.message.channel.send(embed=discord.Embed(title=game.player1name + " VS. " + game.player2name + " in Connect4!", description=game.player1name + " just placed a piece.\n\n" + game.gametostring() + "\n<@" + str(game.player2id) + ">'s move."))
                                else:
                                    lol = await reaction.message.channel.send(embed=discord.Embed(title=game.player1name + " VS. " + game.player2name + " in Connect4!", description=game.player2name + " just placed a piece.\n\n" + game.gametostring() + "\n<@" + str(game.player1id) + ">'s move."))
                                for i in numbers:
                                    await lol.add_reaction(i)
                                game.messageid = lol.id

def runPsiBot():
    while botOn:
        client.run(bot_config["token"])

if __name__ == "__main__":
    runPsiBot()