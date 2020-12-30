import os, requests
import pandas as pd
from bs4 import BeautifulSoup
from requests import get
from discord_webhook import DiscordWebhook

# Webhook settings
url_wb = os.environ.get('DISCORD_WH')

# Data for the scrap
urls = ["https://medium.com/@coinbaseblog", "https://1inch-exchange.medium.com"]

# Open old database file
path = "/home/pi/OpenAlpha/db.xlsx"
df = pd.read_excel(path)

# Check every url
for url in urls:
	response = get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	
	# Check the class before running the code. It might change from blog to blog
	news_list = soup.find_all(class_ = 'dn br')

	# Empty list
	updated_list = []

	for news in news_list:
		article_text = news.text
		article_link = news.get('href')

		# Check if the main domain is missing in the href
		if ("http" not in article_link):
			article_link = url + article_link

		if (article_text not in df.values):
			msg = article_text + '\n' + article_link
			updated_list.append([article_text, article_link])
			try:
				print(article_text)
			except:
				print(article_text.encode('utf-8'))

			# Send message to Discord server
			webhook = DiscordWebhook(url=url_wb, content=msg)
			response = webhook.execute()

	# Export updated news to Excel
	cols = ['Text', 'Link']
	df = df.append(pd.DataFrame(updated_list, columns=cols), ignore_index = True)
	df.to_excel(path, index = False)

