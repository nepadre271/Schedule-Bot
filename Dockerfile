FROM python:3.13.0-slim-bullseye

WORKDIR /app

RUN apt update

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./
EXPOSE 8000
ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD ["python", "-m", "bot"]