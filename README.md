# Задача

Спроектировать и разработать API для системы опросов пользователей.

**Функционал для администратора системы:**

- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

**Функционал для пользователей системы:**

- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

**Использовать следующие технологии:** Django 2.2.10, Django REST framework.

**Результат выполнения задачи:**
- исходный код приложения в github (только на github, публичный репозиторий)
- инструкция по разворачиванию приложения (в docker или локально)
- документация по API

# Инструкция по разворачиванию приложения локально

1. Клонируйте репозиторий: 

    `git clone https://github.com/Ankzy/drf_polls_api.git`
2. Установите необходимые библиотеки:

    `pip install -r requirements.txt`
3. Перейдите в папку с проектом и примените миграции:

    `cd polls`
 
    `python manage.py migrate --run-syncdb`
4. Создайте администратора:
    
    `python manage.py createsuperuser`
5. Запустите локальный сервер:
 
    `python manage.py runserver`
 
Приложение будет доступно локально по адресу http://127.0.0.1:8000/.

# Документация по API

**Функционал для администратора системы:**

Панель управления администратора доступна локально по адресу http://127.0.0.1:8000/admin/. 
Авторизуйтесь, используя данные superuser. Администратору доступно создание, редактирование 
и удаление опросов, вопросов и вариантов ответов для них.

**Функционал для пользователя системы:**

**_1. Получение списка активных опросов_.**

http://127.0.0.1:8000/api/polls/ (GET-запрос)

Пример полученного ответа: [get_polls](get_polls.json)


**_2. Прохождение опросов_.**

http://127.0.0.1:8000/api/answers/ (POST-запрос)

В теле запроса передается список ответов.

**Поля ответа на вопрос:**
1. poll - id опроса.
2. user - id пользователя.
3. question - id вопроса.
4. choice_id - id варианта ответа. Для вопросов с выбором нескольких вариантов (MULT) передается
список id. Для вопросов с выбором одного варианта (SNGL) - просто id (integer). Для текстовых 
вопросов null.
5. text - текст ответа. Заполняется для текстового типа вопроса, для вопросов с вариантами ответа
null.

Пример тела запроса: [post_answers](post_answers.json)
 

**_3. Получение пройденных пользователем опросов с детализацией по ответам по ID пользователя_.**

http://127.0.0.1:8000/api/completed-polls/<user_id>/ (GET-запрос)

Пример полученного ответа для user_id=1: [get_results](get_results.json) 
