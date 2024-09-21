import asyncio

from ENTER_ZION_Chat.enterzion import joke, check_name, check_rat, delete_chat, clear_chat, refresh_msg, header, chat_msgs, online_users, specify_the_path, add_sounds, add_user, \
    select, TEXT, input, radio, input_group, actions, toast, put_progressbar, set_progressbar, put_markdown, put_scrollable, put_button, put_buttons, put_scope, run_async, run_js, \
    start_server

path = r"D:\Python\Progects\online_chat\sounds"
specify_the_path(path)
sounds = {
    "Аджара-Гуджю": "adjara-gudju.mp3",
    "Бабабой": "bababooey-sound-effect.mp3",
    "Бръэ": "brue.mp3",
    "Да ладно!": "daladna.mp3",
    "Вот это прикол...": "vot-eto-prikol1.mp3",
    "Давай прыгай ...!": "davay-pryigay.mp3",
}

add_sounds(sounds)


async def main():
    # вставляем HTML код, который отвечает за хедер со школой и стилями
    await header()

    # регистрация пользователя
    nickname = await input("Как вас зовут",
                           required=True,
                           placeholder="Напиши сюда своё имя, я хочу с тобой познакомиться =)",
                           validate=check_name,
                           type=TEXT)
    # просто прикольный прогрес бар
    put_progressbar(name="progressbar", init=0.2, auto_close=True)

    # Выбор звука
    user_sound = await select("Выберите ваш личный звук для отправки сообщений\n"
                              "Только давай что-то приличное, а то я столько уже всего наслушался...",
                              value=[key for key in sounds], options=[key for key in sounds])

    # Смотрим какой звук выбрал пользователь
    sound = sounds[user_sound]
    set_progressbar(name="progressbar", value=0.5)
    await asyncio.sleep(0.5)

    # проверка на крысу
    await radio("Ты же никому не расскажешь о нашей тайной переписке?",
                options=["Я никому ничего не расскажу, честно",
                         "Я всё покажу маме и меня побьют за это в школе, потому что мои одноклассники знают мой IP адрес и уже выехали за мной"],
                onchange=check_rat,
                # Проверка на крысу
                validate=lambda answer: "Мы тут не уважаем таких -_-" if answer != "Я никому ничего не расскажу, честно" else None)
    set_progressbar("progressbar", value=0.6)
    await asyncio.sleep(0.2)
    set_progressbar("progressbar", value=0.8)
    await asyncio.sleep(0.3)
    set_progressbar("progressbar", value=1)
    await asyncio.sleep(0.5)

    put_markdown("## 🤠 Добро пожаловать в онлайн чат!\nЗдесь можно общаться с друзьями и одноклассниками!")

    # Окошко для сообщений
    put_scrollable(put_scope("chat"), height=300, keep_bottom=True)

    # прикрепляем к пользователю выбранный звук
    # online_users[nickname] = sound
    add_user(nickname, sound)
    # Добавляем в список сообщение о присоединении и косвенно обновляем сообщения у других пользователей
    chat_msgs.append(('📢', f'`{nickname}` присоединился к чату!', online_users[nickname]))

    put_markdown(f'📢 `{nickname}` присоединился к чату', scope="chat")

    # Запускаем асинхронный таск, чтобы у пользователя обновлялись сообщения
    refresh_task = run_async(refresh_msg(nickname))

    # Запускаем асинхронный таск, который позволяет удалять переписку
    clear_chat_task = run_async(clear_chat())

    # за визуализацию удаления отвечает delete_chat, а за его отчистку clear_chat() (она была запущена асинхронно для проверки чата на пустоту)
    put_button("Удалить переписку😏", onclick=lambda: delete_chat("alarm.mp3", "puk.mp3", "windows-xp-shutdown.mp3", "windows-xp-startup.mp3"))

    # Создаём поле ввода сообщения (если сделать без while True, то можно будет ввести сообщение лишь раз
    while True:
        data = await input_group("💭 Новое сообщение", [
            # валидация joke позволяет не отправить сообщение (можно убрать)
            input(placeholder="Текст сообщения ...", name="msg", validate=lambda m: joke("brue.mp3")),
            actions(name="cmd", buttons=["Отправить",
                                         {
                                             'label': "Выйти из чата",
                                             'type': 'cancel'
                                         }
                                         ])
            # Проверка сообщения на пустоту
        ], validate=lambda m: ('msg', "Введите текст сообщения!") if m["cmd"] == "Отправить" and not m['msg'] else None)

        # если пользователь вышел из чата, то брейкаем
        if data is None:
            break

        # появление сообщения на экране
        put_markdown(f"`{nickname}`: {data['msg']}", scope="chat")

        # отправка сообщения всем пользователям
        chat_msgs.append((nickname, data['msg'], online_users[nickname]))

    # Ну и если мы вышли из цикла (разлогинились), то завершаем таски на отслеживание новых сообщений и удаления чата
    refresh_task.close()
    clear_chat_task.close()

    # удаление пользователя
    del online_users[nickname]
    toast("Вы вышли из чата!")
    # Высвечиваем у себя, что пользователь вышел
    put_markdown(f'📢 Пользователь `{nickname}` покинул чат!', scope="chat")

    # Высвечиваем у всех, что пользователь вышел
    chat_msgs.append(('📢', f'Пользователь `{nickname}` покинул чат!'))

    put_buttons(['Перезайти'], onclick=lambda btn: run_js('window.location.reload()'))


if __name__ == "__main__":
    start_server(main, debug=True, port=5000)
