FROM python:3.13
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app ./app
EXPOSE 8000

RUN useradd appuser
USER appuser

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]