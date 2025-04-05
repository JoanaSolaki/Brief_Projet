FROM python:3

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "sh", "-c", "python ./scripts/create_db.py && python ./scripts/import_data.py" ]
