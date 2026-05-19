FROM python:3.12.12-slim-trixie

ENV PYTHONUNBUFFERED=1

WORKDIR /bot
COPY requirements.txt /bot/
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . /bot

ENTRYPOINT [ "python", "bot.py" ]
