import smtplib, ssl
import getpass
import re
from email.mime.text import MIMEText

def iterate(x, y, z):
    x = list(x)
    for a, b in enumerate(x):
        if b == y:
            x[a] = z
    return ''.join(x)

def change(x):
    x = iterate(x, ".", "[.]")
    x = iterate(x, "?", "[?]")
    x = iterate(x, "*", "[*]")
    x = iterate(x, "+", "[+]")
    return x

# Get information from user, When asked for message, type STOP in all caps to end the message.
x= input('What email are you using?  ')
sender_email = choose(x)
receiver_email = input('Who are you sending it to?  ')
password = getpass.getpass(prompt = 'What is your password?  ')
subject = input('What is the subject?  ')
print('\nType your message here:\n')
lines = []
while True:
    line = input()
    if line == 'STOP':
        break
    else:
        lines.append(line)
message = '<br>'.join(lines)

lust = re.findall(r"https?://www[.]\w+[.]\w+/*\S+", message)
last = re.findall(r">\s\S+\s<", message)

a = message
for i, j in zip(lust, last):
    a = re.sub(change('<' + i + j[1:]), "<a href='{}'>{}</a>".format(i[0:-1], j[2:-2]), a)

message = MIMEText(a, 'html')
message['Subject'] = subject
message['From'] = sender_email
message['To'] = receiver_email

context = ssl.create_default_context()
def send_email(email, password, receiver,  body):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as server:
        server.login(email, password)
        server.sendmail(email, receiver, body.as_string())

send_email(sender_email, password, receiver_email, message)
