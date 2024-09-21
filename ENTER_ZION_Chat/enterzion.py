import asyncio
import random

from pywebio.input import select, TEXT, input, radio, input_group, actions
from pywebio.output import put_html, toast, put_markdown, clear
from pywebio_battery import put_audio

from pywebio import start_server
from pywebio.output import toast, put_progressbar, set_progressbar, put_markdown, put_scrollable, put_button, put_buttons, put_scope
from pywebio.session import run_async, run_js

path = ""
online_users = dict()
chat_msgs = []
sounds = dict()


def add_sounds(sounds_dict: dict):
    """" Добавляем звуки """
    global sounds, path
    for sound_name, sound in sounds_dict.items():
        sounds[sound_name] = path + "\\" + sound


def specify_the_path(path_to_sounds):
    """ Говорим библиотеке, где лежат файлы со звуком"""
    global path

    path = path_to_sounds


def add_user(nickname, sound):
    """ Добавляем нового пользователя с его звуком отправки сообщений """
    global online_users
    print(path + "/" + sound)
    online_users[nickname] = open(path + "/" + sound, "rb").read()


def check_name(name: str) -> str:
    """ Проверка имени пользователя (имя содержит плохие слова или такой пользователь уже существует """
    bad_words = ["лох"]
    for bad_word in bad_words:
        if bad_word in name.lower():
            return "Ты серьёзно думаешь, что это смешно? 😢"
    if name in online_users.keys():
        return f"То есть ты сейчас попытался выдать себя за {name}?!?!!\nМеня не обмануть -_-"


def joke(joke_sound):
    """ Возможность не отправить сообщение пользователя"""
    number = random.randint(1, 5)
    if number == 1:
        put_audio(open(f"{path}\\{joke_sound}", "rb").read(), autoplay=True)
        return "Ха-Ха-Ха, я тебя надурил и сообщение не отправилось =)"


def check_rat(answer):
    """ Проверка на 'крысу', чтобы пользователь никому не рассказал о переписке """
    if answer == "Я никому ничего не расскажу, честно":
        return toast("Молодец, ты сделал правильный выбор!")
    else:
        return toast("Я даю тебе ещё один шанс осмыслить своё решение 😡")


async def delete_chat(alarm_sound, time_sound, shutdown_sound, startup_sound):
    """ Оповещение об удалении переписки """
    chat_msgs.append(("Система", "О нет... ЧТО ПРОИСХОДИТ?! КТО-ТО СОБИРАЕТСЯ ОЧИЩАТЬ ПЕРЕПИСКУ!!!",
                      open(f"{path}\\{alarm_sound}", "rb").read()
                      ))
    await asyncio.sleep(3)
    chat_msgs.append(("Система", "ВНИМАНИЕ, ПРОИСХОДИТ УДАЛЕНИЕ ПЕРЕПИСКИ",
                      open(f"{path}\\{time_sound}", "rb").read()
                      ))
    await asyncio.sleep(1)
    for i in range(3, 0, -1):
        chat_msgs.append(("Система", f"Переписка будет удалена через {i}...",
                          open(f"{path}\\{time_sound}", "rb").read()
                          ))
        await asyncio.sleep(1)
    await asyncio.sleep(2)

    chat_msgs.append(("Система", "Выключение...",
                      open(f"{path}\\{shutdown_sound}", "rb").read()
                      ))
    await asyncio.sleep(3)

    chat_msgs.append(("Система", "Запуск...",
                      open(f"{path}\\{startup_sound}", "rb").read()
                      ))
    await asyncio.sleep(3)
    clear("chat")
    chat_msgs.clear()
    toast("Сообщения успешно удалены!")


async def header():
    """ Вставляем 'шапку' сайта, то есть лого """

    # вставляем HTML код, который отвечает за хедер с лого
    put_html("""
            <a href="https://enterzion.io/"  target="_blank"><h1 style="justify-content: center"><img style="height:20px" src="https://enterzion.io/static/base_templates/images/logo.svg"></img></h1></a>
    """)

    # вставляем HTML код, в котором есть стили
    put_html("""
          <style>
                body {
                    background-color: white; /* Цвет фона */
                }
                .scrollable-border{
                    background-color: white; /* Цвет фона */
                }
        </style>
    """)


async def clear_chat():
    """ Функция очистки чата (функция delete_chat только оповещает об удалении, а именно здесь происходит удаление чата) """
    global chat_msgs
    while True:
        await asyncio.sleep(0.1)
        if not chat_msgs:
            clear("chat")
            await asyncio.sleep(0.4)


async def refresh_msg(nickname):
    """ Обновление переписки у других пользователей """

    global chat_msgs, path
    last_idx = len(chat_msgs)
    while True:
        await asyncio.sleep(0.1)

        for m in chat_msgs[last_idx:]:
            if m[0] == "Система":
                put_markdown(f"`{m[0]}`: {m[1]}", scope="chat")
                try:
                    put_audio(m[2], autoplay=True)
                except:
                    pass
            elif m[0] != nickname:  # if not a message from current user
                put_markdown(f"`{m[0]}`: {m[1]}", scope="chat")
                try:
                    put_audio(m[2], autoplay=True)
                except:
                    pass

        last_idx = len(chat_msgs)
