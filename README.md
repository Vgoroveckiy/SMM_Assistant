
---

# SMM Assistant

**SMM Assistant** — это веб-приложение на Flask для автоматизации SMM-задач: генерации контента, публикации постов и анализа статистики для групп ВКонтакте с помощью OpenAI и VK API.

## Возможности

- Генерация текстов постов с помощью GPT-4o-mini по заданной теме и тону.
- Генерация изображений для постов через DALL-E (OpenAI).
- Автоматическая публикация постов (с изображением или без) в группу VK.
- Просмотр статистики по постам (лайки, просмотры) и подписчикам группы VK.
- Регистрация и аутентификация пользователей, индивидуальные настройки VK API.

## Основные функции

### Генерация контента
- **Генератор текста:** Использует модель GPT-4o-mini для создания уникального контента на основе заданной темы и тона.
- **Генератор изображений:** Создает изображения, соответствующие генерируемому тексту.

### Публикация в VK
- **Загрузка изображений:** Автоматически загружает созданные изображения на сервер ВКонтакте.
- **Публикация постов:** Отправляет сгенерированный контент и изображение на указанный URL группы.

### Анализ статистики
- **Лайки и просмотры:** Позволяет анализировать метрики вроде количества лайков, комментариев и просмотров.
- **Подписчики:** Предоставляет информацию о численности подписчиков группы.

## Технологии

- **Flask** — веб-фреймворк Python.
- **Flask-WTF, Flask-Bcrypt, Flask-SQLAlchemy** — формы, хэширование паролей, ORM.
- **OpenAI API** — генерация текста и изображений.
- **VK API** — публикация и статистика в ВКонтакте.
- **SQLite** — хранение пользователей и настроек.

## Основные компоненты

- [`app/__init__.py`](app/__init__.py) — создание Flask-приложения, регистрация блюпринтов.
- [`app/auth.py`](app/auth.py) — регистрация, вход, выход, формы пользователей.
- [`app/models.py`](app/models.py) — модель пользователя (SQLAlchemy).
- [`app/smm.py`](app/smm.py) — маршруты для генерации постов, публикации и статистики.
- [`generators/text_gen.py`](generators/text_gen.py) — генерация текста поста через OpenAI GPT.
- [`generators/image_gen.py`](generators/image_gen.py) — генерация изображения через OpenAI DALL-E.
- [`social_publishers/vk_publisher.py`](social_publishers/vk_publisher.py) — публикация постов и загрузка изображений в VK.
- [`social_stats/vk_stats.py`](social_stats/vk_stats.py) — получение статистики и подписчиков VK.

## Структура проекта

```
SMM_Assistant/
│
├── app/
│   ├── __init__.py         # Инициализация Flask-приложения, регистрация блюпринтов
│   ├── auth.py             # Регистрация, вход, выход пользователей (Flask-WTF)
│   ├── forms.py            # Формы для Flask-WTF (если используются)
│   ├── models.py           # Модель пользователя SQLAlchemy
│   ├── smm.py              # Основная бизнес-логика SMM (генерация, публикация, статистика)
│   ├── static/             # Статические файлы (CSS, JS)
│   └── templates/          # HTML-шаблоны (Jinja2)
│
├── generators/
│   ├── image_gen.py        # Генерация изображений через OpenAI DALL-E
│   └── text_gen.py         # Генерация текста постов через OpenAI GPT
│
├── social_publishers/
│   └── vk_publisher.py     # Публикация постов и загрузка изображений в VK
│
├── social_stats/
│   └── vk_stats.py         # Получение статистики и подписчиков VK
│
├── config.py               # Конфигурация приложения (API-ключи и др.)
├── main.py                 # Точка входа, запуск Flask-приложения
├── requirements.txt        # Зависимости Python
├── smm_assistant.service   # (опционально) systemd unit для автозапуска
├── test.py                 # Пример скрипта для тестирования генерации и публикации
├── instance/
│   └── site.db             # SQLite база данных пользователей
└── README.md
```

## Установка и запуск

1. **Клонируйте репозиторий и перейдите в папку проекта:**
   ```sh
   git clone https://github.com/your-repo/smm-manager.git
   cd smm-manager
   ```

2. **Создайте и активируйте виртуальное окружение:**
   ```sh
   python -m venv env
   source env/bin/activate  # Windows: env\Scripts\activate
   ```

3. **Установите зависимости:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Настройте переменные в `config.py`:**
   - Укажите свои ключи OpenAI и VK API, а также ID группы VK.

5. **Инициализируйте базу данных:**
   ```sh
   python
   >>> from app import db, create_app
   >>> app = create_app()
   >>> with app.app_context():
   ...     db.create_all()
   ... 
   ```

6. **Запустите приложение:**
   ```sh
   python main.py
   ```
   По умолчанию приложение будет доступно на [http://localhost:5500](http://localhost:5500).

## Использование

1. Зарегистрируйтесь и войдите в систему.
2. В разделе **Settings** укажите свои VK API ID и VK Group ID.
3. В разделе **Post Generator** задайте тему и тон, при необходимости отметьте генерацию изображения и/или автопубликацию.
4. В разделе **VK Stats** просматривайте статистику по последним постам и подписчикам.


## Пример тестирования

Для быстрой проверки генерации и публикации используйте [`test.py`](test.py):

```python
from generators.text_gen import PostGenerator
from generators.image_gen import ImageGenerator
from social_publishers.vk_publisher import VKPublisher
import config as conf

post_gen = PostGenerator(conf.openai_key, "дружелюбный", "Новости компании")
content = post_gen.generate_post()
img_desc = post_gen.generate_post_image_description()
img_gen = ImageGenerator(conf.openai_key)
img_url = img_gen.generate_image(img_desc)
vk_pub = VKPublisher(conf.vk_api_key, conf.vk_group_id)
vk_pub.publish_post(content, img_url)
```

## Лицензия

Этот проект распространяется под лицензией MIT, см. файл `LICENSE` для подробностей.

---
