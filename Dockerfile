FROM python:latest

# create working dir
WORKDIR /app

# update pip for installation
RUN pip install --upgrade pip

#copy dependencies and install it
COPY requirments.txt /app/requirements.txt
# install the required libraries
RUN pip install -r /app/requirements.txt

#copy the neccesary files into the dir
COPY .env /app
COPY utils /app/utils
COPY whatsapp-bot.py /app
COPY data /app/data

ENTRYPOINT 8080

# execute the main file
CMD ["python", "/app/whatsapp-bot.py"]
