from webNEWs import web_news
from run_just_bot import dev_pirate_crypto_nonenews
import json
from Bot_tel import dev_pirate_crypto


print("how mod bot run ?")
mod = input("1 - with news\n2 - without news\n3 - run BTC Get news\n  enter mod: ")
if mod == "1":
    num = int(input("Enter the number of news items to fetch: "))
    a = web_news("https://www.investing.com/crypto/bitcoin")
    res = a.run_BTC(number=num+1)
    print("Telegram Bot Runed ! ")
    b = dev_pirate_crypto('8492375819:AAEr8cbQEIMqacxzW5JS6mSjEGGAWH_ReYk')
    b.run()
elif mod == "2":
    print("Telegram Bot Runed ! ")
    b = dev_pirate_crypto_nonenews('8492375819:AAEr8cbQEIMqacxzW5JS6mSjEGGAWH_ReYk')
    b.run()
elif mod == "3":
    num = int(input("Enter the number of news items to fetch: "))
    a = web_news("https://www.investing.com/crypto/bitcoin")
    res = a.run_BTC(number=num+1)