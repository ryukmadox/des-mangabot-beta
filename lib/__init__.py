#!/bin/python
#-*- coding: utf-8 -*-
import requests, os, sys, time, re
from bs4 import BeautifulSoup as bs

token = 'TOKENBOT'
api = f"https://api.telegram.org/bot{token}/"

def res(method, data):
	global api
	api_res = api+method
	if requests.get(api_res,params=data):
		return True

def send_Msg(id, text):
	data = {
		'chat_id':id,
		'text':text
	}

	res('sendMessage',data)

def send_File(id, document, capt=False):
	data = {
		'chat_id':id,
		'document':document
	}
	if capt:
		data['caption'] = capt

	res('sendDocument',data)


def send_Img(id, photo, capt=False):
	data = {
		'chat_id':id,
		'photo':photo
	}
	if capt:
		data['caption'] = capt

	res('sendPhoto',data)

def search_manga(nime):
	try:
		c = {}
		data = {
			'post_type':'manga',
			's':nime.replace(' ','+')
		}
		r = requests.post('https://komiku.co.id',data=data).text
		name = re.findall('<a href="https://komiku.co.id/manga/(.*?)/">',r)[0]
		link = requests.get('https://komiku.co.id/manga/'+name).text
		chapter = re.findall('<span>Chapter Baru </span><span>Chapter (.*?)</span>',link)[0]
		b = bs(link, "html.parser")
		desc = b.findAll('p')[1].text.replace('\n','').replace('\t','')
		image = re.findall('<img src="(.*?)" data-src=".*?" class="lazy sd rd">',r)[0].split('?')[0]
		end = image.split('/')[len(image.split('/'))-1]
		#if os.path.exists('images/'+end):
		#	image = 'images/'+end
		#else:
		#	byte = requests.get(image).text
		#	open('images/'+end, 'wb').write(byte.encode('utf-8'))
		#	image = 'images/'+end

		c['name'] = name
		c['chapter'] = chapter
		c['desc'] = desc
		c['img'] = image
		return c
	except:
		return False

def download(nime, chapter):
	try:
		r = requests.get('https://komiku.co.id/manga/'+nime).text
		rgx = re.findall(f'<a href="(.*?)" title=".*? Chapter {chapter}" class="popunder">',r)[0]
		r2 = requests.get(rgx).text
		r3 = requests.get('https://komiku.co.id'+re.findall('<a href="(.*?)" rel="nofollow" target="_blank">Download PDF</a>',r2)[0],allow_redirects=True,timeout=400).text
		r4 = requests.get(re.findall('<iframe src="(.*?)"></iframe>',r3)[0]).text
		pdf_komik = re.findall('<a href="(.*?)" download>',r4)[0]
		return pdf_komik
	except:
		return False
