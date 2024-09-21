Этот чат разработан специально для школы [ENTERZION](https://enterzion.io/)

В основе лежит библиотека PyWebIo


## Для запуска main.py нужно написать в консоль:
    python3 -m venv venv
## Запуск виртуального окружения на Windows:
    python3 .\venv\Scripts\activate
## Запуск виртуального окружения Linux:
    python3 venv/bin/activate

## Установка библиотеки PyWebIO в виртуальное окружение
    pip3 install -U pywebio



[Дока PyWebIO](https://pywebio.readthedocs.io/en/latest/guide.html#)

> Что это такое?
> **PyWebIO** — это библиотека на Python, разработанная для создания веб-приложений с интерактивным пользовательским интерфейсом, не требуя глубоких знаний в веб-разработке. Она позволяет разработчикам быстро создавать веб-приложения и прототипы, используя простые команды Python.

### Основные характеристики PyWebIO:

1. **Интерактивность**: PyWebIO предоставляет средства для получения ввода от пользователя и отображения вывода в виде текстов, графиков и других элементов интерфейса.

2. **Отсутствие необходимости в HTML/CSS**: Вы можете сосредоточиться на логике вашего приложения без необходимости разбираться в HTML и CSS, что делает его удобным для новичков.

3. **Поддержка различных интерфейсов**: PyWebIO позволяет создавать интерфейсы, которые могут работать на мобильных устройствах, что делает его подходящим для различных платформ.

4. **Гибкость**: Вы можете интегрировать PyWebIO с другими фреймворками и библиотеками Python, такими как Flask или FastAPI, для расширенной функциональности.

5. **Простота использования**: PyWebIO имеет дружелюбный API и предоставляет понятные функции для работы с формами, полями ввода, текстом и графиками. PyWebIO — это отличное решение для быстроразвивающихся приложений, требующих минимальной настройки и немедленного взаимодействия с пользователями. Это делает его идеальным инструментом для обучения, создания прототипов и разработки простых веб-приложений.

### Пример использования PyWebIO

Вот простой пример, как использовать PyWebIO для создания интерактивного ввода:

```python
from pywebio import start_server
from pywebio import input, output

def main():
    name = input.input("Как вас зовут?")
    output.put_text(f"Привет, {name}!")

if __name__ == '__main__':
    start_server(main, port=8080)

```

Это приложение запрашивает имя пользователя и приветствует его. Всего несколькими строками кода вы можете создать интерактивное веб-приложение!

## Что можно пощупать в input?
## Подключение
`from pywebio.input import *`
### Select
```python
selector = select('Заголовок', value=['вариант 1', 'вариант 2'], options=['вариант 1', 'вариант 2'])
# value=что будет принимать значение selector, options=список отображений)
print(selector)
```

### Input
```python
# Password input
input("ЗАГОЛОВОК", type=ТИП_ПОЛЯ)
```

### Textarea
```python
# Multi-line text input
text = textarea('ЗАГОЛОВОК', rows=РАЗМЕР_ОКНА_В_СТРОКАХ, placeholder='ИЗНАЧАЛЬНЫЙ ТЕКСТ')
```

### Валидация

## Функции валидации
> Если возвращено `None`, то валидация успешно пройдена, в противном случае вылезет ошибка


## Важно!
> `validate` принимает именно название функции, а не её вызов, поэтому, если нужно передать в `validate` функцию с параметрами, то мы будем использовать `lambda`


```python
def check_age(p):  # return None when the check passes, otherwise return the error message
    if p < 10:
        return 'Too young!!'
    if p > 60:
        return 'Too old!!'

age = input("How old are you?", type=NUMBER, validate=check_age)
```

### Редактор кода

### Редактор
> Можно использовать параметр `code` в [pywebio.input.textarea()](https://pywebio.readthedocs.io/en/latest/input.html#pywebio.input.textarea "pywebio.input.textarea"), чтобы сделать редактор

```python
code = textarea('Code Edit', code={
    'mode': "python",
    'theme': 'darcula',
}, value='import something\n# Write your python code')
```
### Input Group

```python
data = input_group("Basic info",[
  input('Input your name', name='name'),
  input('Input your age', name='age', type=NUMBER, validate=check_age)
])
put_text(data['name'], data['age'])
```



## Что можно пощупать в output?

### Подключение
> `from pywebio.output import *`
### Отправка текста

```python
put_text('hello').style('color: red; font-size: 20px')
```
### Отправка файла
```python
put_file('hello_word.txt', b'hello word!')
```

### Оповещение
```python
# Show a notification message
toast('New message 🔔')
```

### Всплывающее окно
```python
# Show a PopUp
popup('popup title', 'popup text content')
```

### Окошко с текстом

## `put_scope`
> По сути, это `div`, в который можно что-то запихивать
>


### `put_scrollable`
> Создаём описание `scope`:
> `Размер и тд`

### Создание `scope`
```python
# Окошко для сообщений  
put_scrollable(put_scope("chat"), height=300, keep_bottom=True)

```


### `Важно`
> Можно и без `put_scrollable`

### Добавление текста в `scope`
```python
put_markdown(f'📢 `{nickname}` присоединился к чату', scope="chat")
```
### Очистка `scope`
```python
clear("название_scope")
```




## Из оставшегося


### `run_async`
> `from pywebio.session import run_async`
> Запускает код асинхронно. После его выполнения нужно завершать асинхронный таск

```python
clear_chat_task = run_async(clear_chat())
# здесь какой-то код
clear_chat_task.close()
```

### `run_js`
> `from pywebio.session import run_js`
> Запускает `JavaScript` код

```python
put_buttons(['Перезайти'], onclick=lambda btn: run_js('window.location.reload()'))
```

### `put_audio`
> `from pywebio_battery import put_audio`
> Отправляет в браузер `audio` файл
> - 1 параметр - бинарное представление файла
> - 2 параметр - запускать ли автоматически

```python
put_audio(open("audio.mp3", "rb").read(), autoplay=True)
```