from wit import Wit

access_token="4PJYEITMZSNF7Q7UJLJCANJ7NNPFLN4K"

client =Wit(access_token=access_token)

def wit_response(message_text):
    resp =client.message(message_text)
    time=None
    city_name=None



    entities=resp['entities']
    for entity in entities:
        if entity=='wit$location:location':
            city_name=resp['entities'][entity][0]['body']
        if entity=='wit$datetime:datetime':
            time=resp['entities'][entity][0]['value'].split('T')[0]

    return city_name,time
