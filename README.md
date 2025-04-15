# Документация

## 1. Описание архитектуры

![architecture.png](docs/architecture.png)

---

## 2. Описание структуры

### Проект имеет следующую структуру:


│\
├── /nginx # конфигурация nginx\
├── /docs # Документация\
└── /src # файлы приложения\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── /frontend # фронтенд\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── /backend-ai # api для обращение к нейросети\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── /backend # api\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── /api_tests # юнит тесты\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── /app # код приложения\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── /bot # код тг бота\


## 3. Описание БД

### База данных проекта использует **PostgreSQL**. Основные таблицы:
![bd.png](docs/bd.png)


## 4. Swagger

### https://prod-team-2-b2gtedt8.REDACTED/api/docs


## 5. Работа Swagger
### Для тестирования методов выполните **/auth/telegram**, полученный токен вставьте в **Authorize**

## 6. Покрытие тестами
### https://prod-team-2-b2gtedt8.REDACTED/api/test_coverage

## 7. CI/CD
### 1. Сборка образов Docker
Для сборки Docker-образов используется инструмент Kaniko, который позволяет безопасно собирать и быстро загружать образы в среде CI/CD без необходимости использования Docker daemon.
- build-backend: собирает образ бэкенда из src/backend/Dockerfile и публикует его в GitLab Container Registry с тегом, соответствующим хешу коммита
- build-frontend: собирает образ фронтенда из src/frontend/Dockerfile и также публикует его в GitLab Container Registry
### 2. Развертывание
Этап развертывания выполняет следующие действия:
1. Подключается к серверу по SSH
2. Авторизуется в GitLab Container Registry
3. Создает файл с переменными окружения для docker-compose
4. Копирует необходимые файлы на сервер:
   - docker-compose.yml
   - конфигурационные файлы Nginx
   - SSL-сертификаты
5. Останавливает предыдущую версию приложения
6. Загружает новые образы Docker
7. Создает файл docker-compose.override.yml с указанием конкретных версий образов
8. Запускает приложение с помощью docker-compose
9. Очищает неиспользуемые Docker-ресурсы
Вы правы, я не уделил достаточно внимания SSH-конфигурации и переменным окружения в CI/CD пайплайне. Давайте рассмотрим эти аспекты подробнее:

### SSH-конфигурация в CI/CD пайплайне

В CI/CD пайплайне используется SSH для подключения к серверу и выполнения команд развертывания. Вот как это реализовано:

### Шаблон `.ssh`

```yaml
.ssh:
  image: kroniak/ssh-client:3.19
  variables:
    SSH_HOST: "$ENV_SSH_HOST"
    SSH_USER: "$ENV_SSH_USER"
    SSH_ADDRESS: $SSH_USER@$SSH_HOST
    SSH_PRIVATE_KEY_BASE64: "$ENV_PRIVATE_KEY_BASE64"
  before_script:
    - mkdir -p ~/.ssh && chmod 700 ~/.ssh
    - echo -e "Host *\n\tStrictHostKeyChecking no\n\n" > ~/.ssh/config && chmod 600 ~/.ssh/config
    - echo "$SSH_PRIVATE_KEY_BASE64" | base64 -d > ~/.ssh/id_rsa && chmod 400 ~/.ssh/id_rsa
    - ssh-agent sh -c "ssh-add ~/.ssh/id_rsa"
    - ssh-keyscan -H "$SSH_HOST"
```

Этот шаблон выполняет следующие действия:
1. Использует образ с SSH-клиентом
2. Настраивает переменные для SSH-подключения
3. Создает директорию ~/.ssh с правильными разрешениями
4. Отключает строгую проверку ключей хоста (StrictHostKeyChecking)
5. Декодирует приватный ключ из переменной окружения (в формате base64)
6. Добавляет ключ в ssh-agent
7. Сканирует и добавляет ключ хоста в known_hosts

### Основные переменные окружения

#### Переменные для SSH:
- `ENV_SSH_HOST` - хост для SSH-подключения
- `ENV_SSH_USER` - пользователь для SSH-подключения
- `ENV_PRIVATE_KEY_BASE64` - приватный ключ в формате base64

#### Переменные для базы данных:
- `POSTGRES_USER` - имя пользователя PostgreSQL
- `POSTGRES_PASSWORD` - пароль PostgreSQL
- `POSTGRES_DB` - имя базы данных

#### Переменные для приложения:
- `JWT_SECRET_KEY` - секретный ключ для JWT-токенов
- `BOT_TOKEN` - токен для бота (предположительно Telegram)
- `TMDB_API_TOKEN` - токен для API The Movie Database
- `CHATGPT_SECRET_KEY` - ключ API для ChatGPT

### Передача переменных окружения на сервер

В этапе deploy переменные окружения передаются на сервер через создание файла `docker-compose-env`:

```yaml
ssh $SSH_ADDRESS "cat > ~/docker-compose-env << EOF
POSTGRES_USER=${POSTGRES_USER:-postgres}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-postgres}
POSTGRES_DB=${POSTGRES_DB:-postgres}
JWT_SECRET_KEY=${JWT_SECRET_KEY}
BOT_TOKEN=${BOT_TOKEN}
TMDB_API_TOKEN=${TMDB_API_TOKEN}
CHATGPT_SECRET_KEY=${CHATGPT_SECRET_KEY}
EOF"
```

Этот файл затем используется при запуске docker-compose с флагом `--env-file`.
