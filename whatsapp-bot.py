import copy
import os
import re

from threading import Thread
from time import sleep
from typing import Dict
from typing import List
import openai
import torch
from dotenv import load_dotenv
from flask import Flask
from flask import request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
from utils.func import llm_query, get_tokenizer_model

load_dotenv()
# Twilio settings
client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])
#hugging face settings
auth_token = os.environ["HUGGING_FACE_API_KEY"]

# Define variable to hold llama2 weights naming 
name = "meta-llama/Llama-2-70b-chat-hf"

# Initiate the Flask app
app = Flask(__name__)

def format_activities_text(text: str) -> str:
    """Format the response for better display in WhatsApp"""
    # replace markdown subheadings with bold italics
    text = re.sub(r"###\s*(.+)", r"*_\1_*", text)
    return text

def generate_reply(incoming_message: str, sender_contact: str, receiver_contact: str) -> str:
    """Parse message text and return an appropriate response.
    Args:
        incoming_message:
            Message text
        sender_contact:
            Sender's contact, follows a format 'whatsapp:+<phone number>'
        receiver_contact:
            Receiver's contact (ie, my contact), follows a format 'whatsapp:+<phone number>'

    Returns:
        Response text
    """
    text_message = incoming_message.lower()
    #if ["hi", "how are you", "hey"] in text_message:
    if text_message == "hi" or text_message == "how are you" or text_message == "hey":
       # Return a default message
        return (
            'Hi there! I am Sequi, Ask me any question related to PolyU Taught Programmes \n'
          'Either you are prospective student or current student \n\n'
          'NB: Please avoid asking unrelated question as I will not be of help \n'
        )
    else:
        response = llama_query.query(text_message)
        # format for better whatsapp view
        text_body = format_activities_text(response)
  
    # spliting the text to avoid whatsApp character limit
    # Divide output into 1500 character chunks due to WhatsApp character limit of 1600 chars
    if len(text_body) > 1600:
        text_body = [text_body[i : i + 1500] for i in range(0, len(text_body), 1500)]
    
    for text in text_body:
        client.messages.create(body=text, from_= sender_contact, to=receiver_contact)
        sleep(0.5)
    return
    
@app.route("/")
def hello_world() -> str:
    """Information message"""
    return "WhatsApp bot for PolyU Admission and Academic enquires"

@app.route("/text", methods=["POST"])
def text_reply() -> str:
    """Respond to incoming messages"""
    reply = generate_reply(
        incoming_message=request.form.get("Body"),
        sender_contact=request.form.get("From"),
        receiver_contact=request.form.get("To"),
    )
    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    
    #load the model at the instance of launching the endpoint
    tokenizer, model = get_tokenizer_model()
    llama_query = llm_query()
    app.run(debug=False, host="0.0.0.0", port=port)
