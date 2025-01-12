# Use a lightweight Python image
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir PyGithub

CMD ["python", "repo_creator.py"]
