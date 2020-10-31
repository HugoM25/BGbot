from PIL import Image
import requests
import math

def GetImagefromURL(url):
    img = Image.open(requests.get(url, stream=True).raw)
    img = img.convert("RGB")
    return img

def GetPixelList(img,listemoji, discordwidht = 17, lenmax = 10) :
    width, height = img.size
    ratio = width/height
    finalheight = int(discordwidht/ratio)
    img = img.resize((discordwidht,finalheight))
    finalemoji = ""
    for x in range(0, finalheight):
        for y in range(0,discordwidht) :
            r,g,b = img.getpixel((y,x))
            distmin = 10000
            goodindex = 0
            for i in range(0, len(listemoji)):
                rde = int(listemoji[i][1].split(" ")[0])
                gde = int(listemoji[i][1].split(" ")[1])
                bde = int(listemoji[i][1].split(" ")[2])
                dist = Distance(r,g,b,rde,gde,bde)
                if dist < distmin :
                    if len(listemoji[i][0]) < lenmax :
                        goodindex = i

                    distmin = dist
            finalemoji += str(listemoji[goodindex][0])
        finalemoji +="\n"

    return finalemoji

def GetListEmoji(filename):
    emojilist = []
    with open(filename, "r") as f :
        lines = f.readlines()
        for line in lines :
            partsline = line.split(",")
            miniliste = [partsline[0], partsline[2][:-1]]
            emojilist.append(miniliste)
    return emojilist

def Distance(x,y,z,dex, dey, dez) :
    distance = math.sqrt( (dex-x)**2 + (dey-y)**2 + (dez-z)**2 )
    return distance

def MessageEmoji(url) :

    listemoji = GetListEmoji("EmojiList.txt")
    messageemoji = GetPixelList(GetImagefromURL(url), listemoji)
    if len(messageemoji) > 2000:
        messageemoji = GetPixelList(GetImagefromURL(url), listemoji, 14, 8)

    return messageemoji

if __name__ == "__main__" :
    url=''
    listemoji = GetListEmoji("EmojiList.txt")

    messageemoji = GetPixelList(GetImagefromURL(url), listemoji)
    if len(messageemoji)> 2000 :
        messageemoji = GetPixelList(GetImagefromURL(url), listemoji, 14, 10)




