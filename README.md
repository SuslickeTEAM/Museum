# 🏛️ Музей Боевой Славы

Современное веб-приложение для музея с красивой админ-панелью на Django Unfold и полным Docker setup для production.

## ✨ Особенности

- 🎨 **Django Unfold** - современная админ-панель на Tailwind CSS
- 🐳 **Docker** - полный production setup с PostgreSQL, Nginx, Gunicorn
- 🔒 **Безопасность** - следование Django best practices
- 📱 **Адаптивный дизайн** - работает на всех устройствах
- 🖼️ **Автоматическая оптимизация изображений** - при загрузке
- 🎵 **Аудиогиды** - поддержка аудио для экспонатов
- ⚡ **Production-ready** - готово к развёртыванию

## 🚀 Быстрый старт

### С Docker (рекомендуется)

```bash
# 1. Клонировать репозиторий
git clone https://github.com/SuslickeTEAM/Museum.git
cd Museum

# 2. Скопировать .env файл
cp .env.example .env

# 3. Запустить Docker Compose
docker-compose up -d --build

# 4. Открыть в браузере
# Сайт: http://localhost
# Админка: http://localhost/admin
```

### Локальная разработка

```bash
# 1. Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Скопировать и настроить .env
cp .env.example .env
# Изменить DB_ENGINE на django.db.backends.sqlite3

# 4. Применить миграции
python manage.py migrate

# 5. Создать superuser
python manage.py createsuperuser

# 6. Собрать статику
python manage.py collectstatic --noinput

# 7. Запустить сервер
python manage.py runserver
```

## 🐳 Docker команды

```bash
# Запустить
docker-compose up -d

# Остановить
docker-compose down

# Перезапустить
docker-compose restart

# Посмотреть логи
docker-compose logs -f web

# Пересобрать после изменений
docker-compose up -d --build

# Выполнить команду Django
docker-compose exec web python manage.py <команда>
```

## 📦 Структура проекта

```
Museum/
├── config/              # Настройки Django
│   ├── settings.py      # Основные настройки
│   ├── urls.py          # URL маршруты
│   └── wsgi.py          # WSGI конфигурация
├── Museum/              # Основное приложение
│   ├── models.py        # Модели БД
│   ├── views.py         # Представления
│   ├── admin.py         # Админ-панель
│   ├── forms.py         # Формы
│   └── tests/           # Тесты
├── templates/           # HTML шаблоны
├── static/              # Статические файлы
├── media/               # Загруженные файлы
├── docker-compose.yml   # Docker Compose конфигурация
├── Dockerfile           # Docker образ
├── nginx.conf           # Nginx конфигурация
└── requirements.txt     # Python зависимости
```

## 🗄️ Модели

### Event (События)
- Новости и анонсы музея
- Изображения с автооптимизацией
- Флаг активности

### Category (Категории)
- Организация экспонатов
- SEO-friendly slug
- Порядок отображения
- Счётчик экспонатов

### Exhibit (Экспонаты)
- Название и описание
- Изображение с автооптимизацией
- Аудиогид (опционально)
- Счётчик просмотров
- Флаг "Избранное"

## 🎨 Админ-панель

Django Unfold предоставляет:
- Современный UI на Tailwind CSS
- Тёмная/светлая тема
- Удобная навигация с иконками
- Адаптивный дизайн
- Быстрая работа

**Доступ:** http://localhost/admin

## 🔧 Конфигурация

Основные переменные окружения в `.env`:

```env
# Django
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,yourdomain.com

# Database (PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=museum_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=db
DB_PORT=5432

# Superuser (для автосоздания)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=secure-password

# Обработка изображений
MAX_IMAGE_WIDTH=1920
MAX_IMAGE_HEIGHT=1920
IMAGE_QUALITY=85
```

## 🧪 Тестирование

```bash
# Запустить все тесты
python manage.py test

# С coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 📝 Линтинг

```bash
# Проверка кода
ruff check .

# Автоисправление
ruff check . --fix

# Форматирование
ruff format .
```

## 🚢 Production деплой

1. Обновите `.env` для production:
   - Установите `DJANGO_DEBUG=False`
   - Смените `DJANGO_SECRET_KEY`
   - Обновите `DJANGO_ALLOWED_HOSTS`
   - Используйте надёжные пароли

2. Настройте SSL/TLS (рекомендуется Caddy или Traefik)

3. Запустите:
   ```bash
   docker-compose up -d --build
   ```

4. Настройте резервное копирование PostgreSQL

## 📚 Технологии

- **Django 5.1.2** - веб-фреймворк
- **PostgreSQL 16** - база данных
- **Django Unfold** - админ-панель
- **Nginx** - веб-сервер
- **Gunicorn** - WSGI сервер
- **Docker** - контейнеризация
- **Pillow** - обработка изображений
- **WhiteNoise** - статические файлы

## 🤝 Разработка

```bash
# Создать миграции
python manage.py makemigrations

# Применить миграции
python manage.py migrate

# Создать superuser
python manage.py createsuperuser

# Загрузить тестовые данные
python manage.py populate_db
```

## 📄 Лицензия

MIT License

## 👥 Авторы

SuslickeTEAM

---

🎨 Built with Django Unfold | 🐳 Powered by Docker | ⚡ Production Ready
