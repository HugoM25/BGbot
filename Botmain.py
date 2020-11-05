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
            Messagehelp += "**!bgbot opendoc [add/show/clear]**\n"
            Messagehelp += "*Gère le fichier commun, tout le monde peut y écrire, parfait pour les sondages !*\n"
            Messagehelp += "------Divers------\n"
            Messagehelp += "**!bgbot blague**\n"
            Messagehelp += "*je ne suis pas l'auteur de ces blagues, elles peuvent donc être très nulles.*\n"
            Messagehelp += "**!bgbot emojimage [Le lien de votre image ou alors en pièce jointe]**\n"
            Messagehelp += "*Encore en bêta mais est censé changer votre image en emoji.*\n"
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

        #Renvoie une blague à l'utilisateur (parfois douteuse, le .json de blague n'est pas de moi)----------------------
        if (message.content.startswith(botcommand + "blague")):
            message_blague = ""
            with open("blagues.json", encoding="utf-8")as f:
                jsonData = json.load(f)
                randomblague = random.randint(0,len(jsonData))
                message_blague = str(jsonData[randomblague]["joke"])+ " " +  str(jsonData[randomblague]["answer"])
            await message.channel.send(message_blague)

        #Permet de gérer un open doc en commun (pratique pour récuperer des avis) --------------------------------------

        #Ajoute un avis au document
        if (message.content.startswith(botcommand + "opendoc add")):
            messagetext = str(message.content)
            messagelist = messagetext.split(" ")
            messagetoadd = ""
            for i in range(3, len(messagelist)):
                messagetoadd += messagelist[i] + " "

            with open("opendoc.txt", "a") as f :
                f.write("------------- " + "\n")
                f.write(messagetoadd)
                f.write("\n" + str(message.author.name) +"\n")

            await message.channel.send(message.author.mention +" Votre texte a bien été enregistré !")

        #Donne le document
        if (message.content.startswith(botcommand + "opendoc show")):
            await message.channel.send("Voici votre document actuel :")
            await message.channel.send(file=discord.File("opendoc.txt"))

        if(message.content.startswith(botcommand+ "opendoc clear") and str(message.author) == "LeCoumik#0882"):
            with open("opendoc.txt", "w") as f:
                f.write("")
            await message.channel.send("Le document a été vidé !")





if __name__ == "__main__" :
    bot = Bot()
    bot.run(os.environ["DISCORD_TOKEN"])
