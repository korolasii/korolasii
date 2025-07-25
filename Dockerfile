FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r req.txt

CMD ["python", "main.py"]