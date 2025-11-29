import smtplib
from email.mime.text import MIMEText

def send_email(to, subject, body):
    sender = "your@gmail.com"
    pwd = "YOUR_APP_PASSWORD"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender, pwd)
    server.sendmail(sender, [to], msg.as_string())
    server.quit()
