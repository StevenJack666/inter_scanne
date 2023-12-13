FROM python:3.7

# 给我们要传的参数一个初始值
ENV PARAMS=""
WORKDIR /app

COPY ../../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ../.. .

CMD "python" "vcrawl.py" $PARAMS