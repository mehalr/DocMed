

from twilio.rest import Client
from decouple import config 
 
account_sid = config('ACC_SID')
auth_token = config('AUTH_TOKEN')
client = Client(account_sid, auth_token) 

def send_message(mesg):
    message = client.messages.create( 
                                  from_='whatsapp:+14155238886',  
                                  body= mesg,  
                                  to= config('NUMBER')
                              ) 
     
    print(message.sid)


