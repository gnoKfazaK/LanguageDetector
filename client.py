import threading
import time
import json
import redis
import telepot

from telepot.loop import MessageLoop
from TimeBasedCache import TimeBasedCache



PROMPT = False 
API_TOKEN = "IAmNotGoingToLeakMyTokenLOL"
HOST = 'localhost'
PORT = 6379
TTL = 90 # Time-To-Live in cache is 90 seconds

# Create Redis connection
r = redis.Redis(host= HOST, port=PORT)

cache = TimeBasedCache(TTL)

def prompt_user():
    while True:
        text = input('Input a text or a sentence:\n')
        chat_id = 12345678
        message = {
            "text": text,
            "chat_id": chat_id
        }
        r.lpush("text", json.dumps(message)) # Submit message to download queue
        time.sleep(1)
    
# Function to listen for predictions
def listen_predictions():
    while True:
    # Listen for message from prediction queue
        message = r.blpop("prediction")
        data = json.loads(message[1])
        lang = data['lang']
        confidence = round(float(data['prob']) * 100)
        print(f'The language is {lang}  ({confidence})')
        print(f'Chat_id: {data['chat_id']}')

def user_input(msg):
    print('+' * 40)
    print('Client')
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == "text":
        content = msg["text"]
        print(f'Text:\n{content}\n')
        print(f'Chat_id: {chat_id}\n')
        # print('Cahche:', cache.cache)
        if cache.exists(content):
            print("Cache")
            reply = cache.get(content)
            cache.put(content, reply)
            bot.sendMessage(chat_id, reply)
            print(reply, f'chat_id: {chat_id}')
            print('-' * 40)

        else:    
            message = {
                    "text": content,
                    "chat_id": chat_id
                }
            r.lpush("text", json.dumps(message))

def reply_user():
    while True:
        message = r.blpop("prediction")
        data = json.loads(message[1])
        lang = data['lang']
        confidence = round(float(data['prob']) * 100)
        chat_id = data['chat_id']
        reply = f'The language is {lang}  ({confidence})'
        cache.put(data['text'], reply)
        bot.sendMessage(chat_id, reply)
        print(reply, f'chat_id: {chat_id}')
        print('-' * 40)


# Cannot receive message when the function cannot receive redis.blpop('prediction')
def handle(msg):
    """
    A function that will be invoked when a message is recevied by the bot.
    """
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == "text":
        content = msg["text"]
        print(content)
        message = {
                "text": content,
                "chat_id": chat_id
            }
        r.lpush("text", json.dumps(message))
        message = r.blpop("prediction")
        data = json.loads(message[1])
        lang = data['lang']
        confidence = round(float(data['prob']) * 100)
        reply = f'The language is {lang}  ({confidence})'
        bot.sendMessage(chat_id, reply)
        print(f'The language is {lang}  ({confidence})')




def main():
    if not PROMPT:
        print("Bot starting")
        MessageLoop(bot, user_input).run_as_thread()
        reply_user_thread = threading.Thread(target=reply_user)
        reply_user_thread.start()
    
    if PROMPT:
        prompt_thread = threading.Thread(target=prompt_user)
        prediction_thread = threading.Thread(target=listen_predictions)
        prompt_thread.start()
        prediction_thread.start()
        


# Create and start threads
if __name__ == "__main__":
    bot = telepot.Bot(API_TOKEN)
    main()
    while True:

        time.sleep(10)
    