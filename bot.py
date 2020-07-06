# CodedBotBy: Desta Adyangga Saputra
#-*- coding: utf-8 -*-
import telebot
import requests
import os
import re
import json
from requests.exceptions import *
from bs4 import BeautifulSoup as bs
from flask import Flask,request
from lib import *

bot = telebot.TeleBot(token)
r = requests.Session()

app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,"📌 Press /help to show information!")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message,'''----{>🤖 Manga Bot 🤖<}----

Use command:

/help - ❓information
/search <mangaName> - 🔎 manga
/download <mangaName> <Chapter> - ⬇️ manga''')

@bot.message_handler(commands=['search'])
def search(message):
	text = message.text
	id = re.findall("'id': (.*?),",str(message))
	id = id[len(id)-1]
	reply = False
	if len(text.split()) == 1:
		bot.reply_to(message,"❌ Please enter manga name! Use: /search <mangaName>")
		return "salah!"
	try:
		nime = text.split(" ")
		del nime[0]
		nim = " ".join(nime)
	except:
		reply = "❌ Please enter manga name! Use: /search <mangaName>"
	data = search_manga(nim)
	if data:
		name = data['name']
		chapter = data['chapter']
		desc = data['desc']
		img = data['img']
		capt = "✅ manga is found!\n\n"+"MangaName: "+name+"\nAll_chapter: "+chapter+"\n\n-------<|Description|>-------\n\n"+desc
		send_Img(id, img, capt=capt)
	else:
		reply = "❌ Maybe manga not found!"
	if reply:
		bot.reply_to(message,reply)

@bot.message_handler(commands=['download'])
def down(message):
	text = message.text
	id = re.findall("'id': (.*?),",str(message))
	id = id[len(id)-1]
	reply = False
	if len(text.split()) == 1:
		bot.reply_to(message,"❌ Please enter manga name! Use: /download <manaName>  <chapter>")
		return "salah!"
	try:
		bot.reply_to(message, "⏱ Please wait........")
		arg = text.split()
		end = len(arg)-1
		chapter = arg[end]
		del arg[end]
		del arg[0]
	except:
		reply = "❌ Please enter manga name! Use: /download <manaName>  <chapter>"

	nimex = " ".join(arg)
	nimexx = search_manga(nimex)
	manga = nimexx['name']
	if nimexx:
		pdf = download(nimexx["name"], chapter)
		send_File(id, pdf, capt="✅ Success Downloading!\n\nManga: "+manga+"\nChapter: "+chapter)
	else:
		reply ="❌ Maybe manga/chapter not found!"
	if reply:
		send_Msg(id, reply)

#####--Uses For Loong Pooling method --#####
#bot.remove_webhook()
#print('bot aktif')
#bot.polling()
############################################

@app.route('/' + token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "oke", 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://yourbotdomain.com/'+api)
    return 'oke',200

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT','5000')),debug=True)

