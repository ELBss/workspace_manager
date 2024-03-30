FROM python:3.12-slim
# RUN apt update \
#     && apt install -y --no-install-recommends \
#     && apt clean \
#     && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN pip install --no-cache-dir -r requirements.txt
COPY  bot/.env /src/bot/
COPY . /src
# ENTRYPOINT [ "python", "bot/bot.py" ]
CMD ["python", "bot/bot.py"]