FROM python:3-alpine

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# COPY assets ./assets

# print the assets folder content on the console
RUN ls

EXPOSE 8080

CMD ["python", "./main.py"]