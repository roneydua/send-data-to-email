#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   send_email.py
@Time    :   2024/09/13 10:10:29
@Author  :   Roney D. Silva
@Contact :   roneyddasilva@gmail.com
'''

import smtplib
import threading
import zipfile
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep

# Email details

from_addr = "roneyddasilva.temp@gmail.com"
password = "jyun hfwy uild lppa"
to_addr = "roneyddasilva@gmail.com"
smtp_server = "smtp.gmail.com"
acc_file = "CoolTerm Capture (acc.stc) 2024-09-12 11-14-26-130.txt"
source_file = "CoolTerm Capture (source.stc) 2024-09-12 11-14-34-896.txt"
# attachment1 = "CoolTerm Capture (acc.stc) 2024-09-12 11-14-26-130_to_send.txt"
# attachment2 = "CoolTerm Capture (source.stc) 2024-09-12 11-14-34-896_to_send.txt"
attachment1 = "CoolTerm Capture (acc.stc) 2024-09-12 11-14-26-130.zip"
attachment2 = "CoolTerm Capture (source.stc) 2024-09-12 11-14-34-896.zip"


def send_email_thead():
    while 1:
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        subject = "thermal chamber test" + current_time
        body = "."

        # Attachments
        # shutil.copy2(acc_file,attachment1)
        # shutil.copy2(source_file,attachment2)
        with zipfile.ZipFile(
            attachment1, "w", compression=zipfile.ZIP_LZMA, compresslevel=9
        ) as myzip1:
            myzip1.write(acc_file)
        with zipfile.ZipFile(
            attachment2, "w", compression=zipfile.ZIP_LZMA, compresslevel=9
        ) as myzip1:
            myzip1.write(source_file)

        # Open files and create file-like objects
        fp1 = open(attachment1, "rb")
        fp2 = open(attachment2, "rb")

        # Construct email message
        msg = MIMEMultipart()
        msg["From"] = from_addr
        msg["To"] = to_addr
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Add attachments
        msg.attach(MIMEApplication(fp1.read(), Name=attachment1))
        msg.attach(MIMEApplication(fp2.read(), Name=attachment2))

        # Send email
        try:
            with smtplib.SMTP(smtp_server, 587) as server:
                server.starttls()
                server.login(from_addr, password)
                server.sendmail(from_addr, to_addr, msg.as_string())
            # Close file objects
            fp1.close()
            fp2.close()
            print("send data on " + current_time)
        except:
            pass
        sleep(60*60*3)


def status_thread():
    while 1:
        print("I'm running "+datetime.now().strftime("%Y%m%d_%H%M%S"))
        sleep(30)


def main():
    # make treadings
    t1 = threading.Thread(target=send_email_thead)
    t2 = threading.Thread(target=status_thread)
    # start
    t1.start()
    t2.start()
    # keep
    t1.join()
    t2.join()


if __name__ == "__main__":
    main()
