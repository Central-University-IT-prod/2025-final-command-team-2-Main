FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y supervisor && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

RUN mkdir -p /var/log/app

RUN echo '[supervisord]\n\
nodaemon=true\n\
logfile=/var/log/app/supervisord.log\n\
\n\
[program:flask]\n\
command=/bin/bash -c "if [ ! -d \"migrations\" ]; then flask db init; fi && flask db migrate -m \"Auto-generated migration\" && flask db upgrade && python run.py --no-reload"\n\
directory=/app\n\
stdout_logfile=/var/log/app/flask.log\n\
stderr_logfile=/var/log/app/flask-error.log\n\
\n\
[program:bot]\n\
command=python bot/run.py\n\
directory=/app\n\
stdout_logfile=/var/log/app/bot.log\n\
stderr_logfile=/var/log/app/bot-error.log' > /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord"]