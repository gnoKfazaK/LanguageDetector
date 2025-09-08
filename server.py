import json
from LinguaDetection import TopLang
import redis

# Create Redis connection
r = redis.Redis(host='localhost', port=6379)


# Continuously receive messages from the "image" queue
while True:
    # Receive message from the "image" queue
    print('+' * 40)
    print('Server')
    message = r.brpop("text")
    data = json.loads(message[1])
    # Preprocess the image
    print(f'Text:\n{data['text']}\n\nChat_id:\n{data['chat_id']}')
    lang, prob = TopLang(data['text'])
    if lang is not None:
        # Generate predictions using the model
        # Create the message for the "prediction" queue
        print(f"\nLanguage: {lang} ({prob})")
        
        message = {
            "text": data['text'],
            "lang": lang, 
            "prob": prob, 
            'chat_id': data['chat_id']
        }
        # Submit the message to the "prediction" queue
        r.lpush("prediction", json.dumps(message))
        print('-' * 40)


