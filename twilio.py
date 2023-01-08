
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'ACbc0f23c43da565de1eab3768f418c0de'
auth_token = 'cf3881be0fcc23f7e53b7652ae63d961'
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body='This is the ship that made the Kessel Run in fourteen parsecs?',
         from_= '+44 1793 540747',
         to= '+41775205787'
     )

print(message.sid)