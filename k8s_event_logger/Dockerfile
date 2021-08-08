FROM python:3.9-slim-buster

WORKDIR /app
COPY . .
RUN pip -r install requirements.txt

CMD ["python", "src/k8s_asyncio.py"]