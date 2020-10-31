import discord
import Emojiimage
import json
import random
import os

class Bot(discord.Client):
    def __init__(self):
        super().__init__()

    async def on_ready(self):
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("-----------")

    async def on_message(self, message):
        botcommand = "!bgbot "

        if (message.author == self.user):
            if message.content.startswith("[POLL] ") :
                await message.add_reaction("👍")
                await message.add_reaction("👎")


        #Permet de connaître les commandes du bot
        if (message.content.startswith(botcommand + "help")):
            Messagehelp = "Bonjour, je suis bgbot, pour apprendre à mieux me connaître voici mes différentes commandes :"+ "\n"
            Messagehelp += "------Utile------\n"
            Messagehelp += "**!bgbot poll [Votre texte du sondage]**\n"
            Messagehelp += "*Permet de créer des sondages.*\n"
            Messagehelp += "------Divers------\n"
            Messagehelp += "**!bgbot blague**\n"
            Messagehelp += "*je ne suis pas l'auteur de ces blagues, elles peuvent donc être très nulles.*\n"
            Messagehelp += "**!bgbot emojimage [Le lien de votre image ou alors en pièce jointe]**\n"
            Messagehelp += "*Encore en bêta mais est censé changer votre image en emoji.*"
            await message.channel.send(Messagehelp)


        #Fonction image to emojimage-------------------------------------------------------------------------------------
        if (message.content.startswith(botcommand + "emojimage")):
            if (len(message.attachments) > 0):
                print(message.attachments[0].url)
                await message.channel.send(Emojiimage.MessageEmoji(str(message.attachments[0].url)))
            else :
                await message.channel.send("[ERROR] No image to transform")

        #Permet de faire des polls---------------------------------------------------------------------------------------
        if (message.content.startswith(botcommand + "poll")):
            messageparts = message.content.split(" ")
            pollmessage = ""
            for i in range(2, len(messageparts)):
                pollmessage += str(messageparts[i] + " ")

            await message.channel.send( "[POLL] " + pollmessage)

        if (message.content.startswith(botcommand + "blague")):
            message_blague = ""
            with open("blagues.json", encoding="utf-8")as f:
                jsonData = json.load(f)
                randomblague = random.randint(0,len(jsonData))
                message_blague = str(jsonData[randomblague]["joke"])+ " " +  str(jsonData[randomblague]["answer"])
            await message.channel.send(message_blague)


if __name__ == "__main__" :
    bot = Bot()
    bot.run(os.environ["DISCORD_TOKEN"])
