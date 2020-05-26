import random  # Импорт генератора случайных чисел
from time import sleep  # Импорт  функции задержки
import pandas as pd  # Библиотека для работы с датасетами
import vk_api  # Библиотека для работы с Вконтакте

usd = pd.read_csv('data/dollar.csv')  # Загружаем в память датасет с курсами доллара

eur = pd.read_csv('data/euro.csv')  # Загружаем в память датасет с курсами евро

usddates = usd['Date'].to_numpy()  # Создаем Numpy массив с датами
eurdates = eur['Date'].to_numpy()  # Создаем Numpy массив с датами



class valute(): # Создаем класс
    # Доллар
    def usdcheck():  # Задаем функцию проверки курса доллара
        messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            body = messages["items"][0]["last_message"]["text"]

            # В методе выводим небольшую инструкцию пользователю. 
            text = 'Вы выбрали доллар - Напишите "да", чтобы продолжить или "нет" для отмены'
            vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1, 30000, 1), "message": text})
            while True:
                messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
                if messages["count"] >= 1:
                    id = messages["items"][0]["last_message"]["from_id"]
                    body = messages["items"][0]["last_message"]["text"]

                    # Далее проверяем на наличие команд “да” или “нет”.
                    if "нет" in body.lower():
                        break
                    elif "да" in body.lower():
                        vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1, 30000, 1),
                                                    "message": 'Введите дату в формате дд.мм.гггг самая ранняя дата - 04.11.1992'})
                        while True:
                            messages = vk.method("messages.getConversations",
                                                 {"offset": 0, "count": 20, "filter": "unread"})
                            if messages["count"] >= 1:
                                body = messages["items"][0]["last_message"]["text"]
                                dt = body
                                check = dt in usddates
                                if check == True:
                                    usdval = usd[usd.Date == dt]['USD'].values[0]
                                    usdtext = "Стоимость доллара на " + str(dt) + " составляла " + str(
                                        usdval) + ' руб., вы можете написать "выход", чтобы выйти или ввести другую дату'
                                    vk.method("messages.send",
                                              {"peer_id": id, "random_id": random.randrange(1, 30000, 1),
                                               "message": usdtext})
                                elif "выход" in body.lower():
                                    break
                                else:
                                    vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1, 30000, 1),
                                               "message": 'Выбран выходной день или неверный формат даты, введите другую дату'})
                    elif "выход" in body.lower():
                        break
                    else:
                        vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1, 30000, 1),"message": 'Я вас не понимаю, введите да или нет'})

# Евро
    def eurcheck():  # Задаем функцию проверки курса евро
        messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            body = messages["items"][0]["last_message"]["text"]

            # В методе выводим небольшую инструкцию пользователю. 
            text = 'Вы выбрали евро - Напишите "да", чтобы продолжить или "нет" для отмены'
            vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1, 30000, 1), "message": text})
            while True:
                messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
                if messages["count"] >= 1:
                    id = messages["items"][0]["last_message"]["from_id"]
                    body = messages["items"][0]["last_message"]["text"]

                    # Далее проверяем на наличие команд “да” или “нет”.
                    if "нет" in body.lower():
                        break
                    elif "да" in body.lower():
                        vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1, 30000, 1),
                                                    "message": 'Введите дату в формате дд.мм.гггг, самая ранняя дата - 01.01.1999'})

                        while True:
                            messages = vk.method("messages.getConversations",
                                                 {"offset": 0, "count": 20, "filter": "unread"})
                            if messages["count"] >= 1:
                                body = messages["items"][0]["last_message"]["text"]  # Заносим в память введенную дату
                                dt = body
                                check = dt in eurdates
                                if check == True:
                                    eurval = eur[eur.Date == dt]['EUR'].values[0]
                                    eurtext = "Стоимость евро на " + str(dt) + " составляла " + str(
                                        eurval) + ' руб., вы можете написать "выход", чтобы выйти или ввести другую дату'
                                    vk.method("messages.send",
                                              {"peer_id": id, "random_id": random.randrange(1, 30000, 1),
                                               "message": eurtext})
                                elif "выход" in body.lower():
                                    break
                                else:
                                    vk.method("messages.send",
                                              {"peer_id": id, "random_id": random.randrange(1, 30000, 1),
                                               "message": 'Выбран выходной день или неверный формат даты, введите другую дату'})
                    elif "выход" in body.lower():
                        break

# КЛАСС МЕНЮ
class Menu():
    @staticmethod
    def showMenu():
        menu_array = ['Список команд:',
                      'Доллар - курс доллара',
                      'Евро - курс евро']
        menu = ''
        for i in menu_array:
            menu = menu + i + '\n'
        return menu

# ОСНОВНОЙ КОД БОТА
vk = vk_api.VkApi(token="461066dcdf6ee8921a21626fedd29eec26bbfc204eb8c556aa93ce67175b153f6062acf4df2fcffe586e6")

while True:
    try:
        messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            body = messages["items"][0]["last_message"]["text"]
            if "привет" in body.lower():
                vk.method("messages.send",
                          {"peer_id": id, "random_id": random.randrange(1, 30000, 1), "message": "Привет"})

            # меню
            elif "меню" in body.lower():
                menu = Menu.showMenu()
                vk.method("messages.send", {"peer_id": id, "random_id": random.randrange(1, 30000, 1), "message": menu})

            elif "доллар" in body.lower():
                valute.usdcheck()
                vk.method("messages.send",
                          {"peer_id": id, "random_id": random.randrange(1, 30000, 1), "message": "Вы вышли"})
            elif "евро" in body.lower():
                valute.eurcheck()
                vk.method("messages.send",
                          {"peer_id": id, "random_id": random.randrange(1, 30000, 1), "message": "Вы вышли"})
            else:
                vk.method("messages.send",
                          {"peer_id": id, "random_id": random.randrange(1, 30000, 1), "message": "Я вас не понимаю"})

        sleep(1)
    except Exception as e:
        print("Ошибка")
        sleep(1)