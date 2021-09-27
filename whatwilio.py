from twilio.rest import Client

# client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
client = Client()
ls = [8278687203, 9887997335, 8278686334, 7014336436, 8955641112]

# this is the Twilio sandbox testing number
from_whatsapp_number='whatsapp:+14155238886'

for x in ls:
    # replace this number with your own WhatsApp Messaging number
    to_whatsapp_number = f'whatsapp:+91{x}'
    client.messages.create(body='Ahoy, world!',
                           from_=from_whatsapp_number,
                           to=to_whatsapp_number)