FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000
# RUN python
# CMD tail -f /dev/null
CMD ["streamlit", "run", "src/main.py", "--server.port=8000", "--server.address=0.0.0.0"]
