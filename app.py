import os, sys
from flask import Flask,request
from keys import token
from pymessenger import Bot
from utils import wit_response
from weather import weather_be


app = Flask(__name__)
VERIFY_TOKEN='token_initialized'
PAGE_ACCESS_TOKEN=token

bot=Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
    # webhook verification
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
        if request.args.get('hub.verify_token') ==VERIFY_TOKEN:
            return 'Verification token missmatch', 403
        return request.args['hub.challenge'], 200
    return 'Verified', 200


@app.route('/', methods=['POST'])
def webhook():
    data=request.get_json()
    log(data)

    if data['object']=='page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                sender_id=messaging_event['sender']['id']
                recipient_id=messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text=messaging_event['message']['text']
                    else:
                        messaging_text='Not Found'

                    if 'weather' in messaging_text.lower():
                        city_name,time=wit_response(messaging_text)

                        if city_name!=None:
                            if time!=None:
                                temp,scheduled=weather_be(city_name,time)
                                temp="{:.2f}".format(temp)
                                response=str(temp)+' Degree Celsius'+' Scheduled at '+scheduled
                            else:
                                response='Mention "today" or "tomorrow" in your sentence'
                        else:
                            response='Please mention which place you are searching for'

                    else:
                        response="Sorry, I can only talk about weathers. Try mentioning weather in your sentence"

                    bot.send_text_message(sender_id,response)


    return 'ok',200

def log(message):
    print(message)
    sys.stdout.flush()

if __name__ == '__main__':
    app.run(debug = True,port= 80)
