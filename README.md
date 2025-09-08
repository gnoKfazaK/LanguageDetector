# LanguageDetector
## The main function of my program is to detect the language of the user input. 
The program mainly runs on 2 scripts, client.py and server.py. For the script client.py mainly 
for the connection between the telegram bot and for caching. The script server.py is for 
running the server that detects the language of the user’s input. And send it back to 
client.py.  
The messages are passed between threads by using Redis as a queue. So, the client.py can 
still receive user’s input even when the server.py had yet to respond. 
## Install libraries
```pip install threading time json redis telepot lingua-language-detector```
## Run the client side script
```python ./client.py```

## Run the server side script
```python ./server.py```
### You can run the LinguaDetection.py seperatly. (Not nessicary)
```python LinguaDetection.py```
# System architecture
<img width="637" height="489" alt="SystemArchitecture" src="https://github.com/user-attachments/assets/38f93082-53ab-4203-8435-85316e0af4b7" />

# Telegram Example
<img width="761" height="583" alt="Telegram bot photo" src="https://github.com/user-attachments/assets/fa1538fa-27fc-48f2-97db-35ca67ec68e7" />
