FROM python:3.12 AS image

RUN apt-get update && apt-get install libgl1 -y

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["/bin/sh", "./cmd.sh"]
