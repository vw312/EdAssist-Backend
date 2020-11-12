FROM python:3.8-slim-buster

RUN mkdir /app
WORKDIR /app

RUN apt update
RUN apt install -y libpq-dev gcc 
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt clean all

RUN useradd -m user

COPY . .

RUN chown -R user:user /app
RUN chmod +x entrypoint.sh
USER user

CMD ./entrypoint.sh