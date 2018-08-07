import config
import telebot
import json
import requests
import threading
from time import sleep
proxies = {
          'http': 'https://188.40.166.43:1080',
          'https': 'https://54.39.46.86:3128',
          }
telebot.apihelper.proxy = {"https": "socks5://tgproxy:fuckrkn@tp.grishka.me:1080"}
bot = telebot.TeleBot(config.token)
with open("data.txt") as file:
    file = file.read()
    file = file.replace("'", '"')
    data = json.loads(file)
def looking():
    while True:
        for message_chat_id, (tags, last) in data.items():
            url = "https://trixiebooru.org/search.json?q={0}&key=y7xogXKu9obph4qx5_7K".format(tags)
            js = requests.get(url, proxies=proxies).json()
            i = 0
            while js['search'][i]['id'] > last:
                i += 1
                if i == 11:
                    break
            i -= 1
            if i == -1:
                continue
            for k in range(i, -1, -1):
                bot.send_message(int(message_chat_id), js['search'][k]['representations']['large'])
            last = js['search'][0]['id']
            data.update({str(message_chat_id): [tags, last]})
            with open("data.txt", "w") as file:
                file.write(str(data))
        sleep(10)
t1 = threading.Thread(target=looking)
t1.start()
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo(message):
    if message.text == "/start":
        bot.send_message(message.chat.id, "Введите комбинацию тегов, за которой вы хотите следить, например safe, twilight sparkle {0}".format(message.chat.id))
    else:
        tags = message.text.replace(", ", ",")
        tags = tags.replace(" ", "+")
        tags = tags.replace("&", "%26")
        url = "https://trixiebooru.org/search.json?q={0}&key=y7xogXKu9obph4qx5_7K".format(tags)
        js = requests.get(url, proxies=proxies).json()
        last = js['search'][0]['id']
        bot.send_message(message.chat.id, "Теперь вы будете получать уведомления, когда выйдут новые арты с точно такими же тегами. Проверьте, правильно ли вы ввели теги: https://trixiebooru.org/search?q={0}".format(tags))
        data.update({str(message.chat.id): [tags, last]})
        with open("data.txt", "w") as file:
            file.write(str(data))
if __name__ == '__main__':
    bot.polling(none_stop=True)