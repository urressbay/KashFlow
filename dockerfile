FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]


FROM python:3-alpine

WORKDIR /app
RUN apk add --no-cache mariadb-dev pkgconfig gcc musl-dev
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]


