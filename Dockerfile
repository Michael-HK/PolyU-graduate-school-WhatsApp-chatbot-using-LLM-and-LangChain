FROM python:latest

# create working dir
WORKDIR /app

#copy the neccesary files into the dir
COPY whatsapp-bot.py /app
COPY data /app/data
COPY .env /app
COPY utils /app/utils
COPY requirments.txt /app/requirements.txt

# update pip for installation
RUN pip install --upgrade pip

# install the required libraries
RUN pip install -r /app/requirements.txt

ENTRYPOINT 8080

# execute the main file
CMD ["python", "/app/whatsapp-bot.py"]
