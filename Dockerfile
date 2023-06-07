FROM python:3.11-slim

WORKDIR /pyrisk-app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app ./app
COPY ./api.json ./

EXPOSE 8001
CMD [ "flask","--app","app.main","run","--host","0.0.0.0","--port","8001"]