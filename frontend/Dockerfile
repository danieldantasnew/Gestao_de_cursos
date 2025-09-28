FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

RUN npm install

EXPOSE 8000

CMD sh -c "python manage.py migrate && npm run watch & python manage.py runserver 0.0.0.0:8000"
