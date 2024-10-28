FROM python:3.13.0-slim-bullseye

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./
CMD ["python", "-m", "schedule"]