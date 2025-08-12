from webNEWs import web_news
import json
from Bot_tel import dev_pirate_crypto


# num = int(input("Enter the number of news items to fetch: "))
# a = web_news("https://www.investing.com/crypto/bitcoin")
# res = a.run(number=num)
# print("Telegram Bot Runed ! ")
b = dev_pirate_crypto('8492375819:AAEr8cbQEIMqacxzW5JS6mSjEGGAWH_ReYk')
b.run()
