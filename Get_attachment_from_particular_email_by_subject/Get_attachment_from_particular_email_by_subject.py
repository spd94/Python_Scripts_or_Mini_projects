'''
This script intended to work with gmail accounts which have authorized imap access to gmail.(https://support.google.com/mail/answer/7126229?hl=en) 
Just for running this script change ur gmail settings and after that revert back to default settings.
==========================
IMPORTANT
*This script assume that u have email account with imap access,let say "abc@gmail.com"
*From which u want to download the all "attachments from" one particular sender id,let say "xyz@gmail.com"
*And "store/Download it" into paticular directory with name according to email subject.
*Do changes in script according to comments. 
==========================
'''
import imaplib
import base64
import os
import email
import re

mail = imaplib.IMAP4_SSL('imap.gmail.com',993) #This is required to connect to gmail imap server according to there docs.
mail.login('abc@gmail.com','passwd') #enter ur email and password
mail.list()

mail.select("inbox") 

result, data = mail.search(None, '(FROM "xyz@gmail.com ")' ) #enter from which sender email id u want to download attachments.

ids = data[0] 
mail_ids = data[0]
id_list = mail_ids.split()

for num in data[0].split():
    typ, data = mail.fetch(num, '(RFC822)' )
    raw_email = data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)

    for part in email_message.walk():        
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            subject=str(email_message).split("Subject:",1)[1].split("\nTo:",1)[0]
            subject=re.sub(r'[^\w]', '_', subject)
            directory="/Users/spd94/Documents/"+subject #Here give ur local machine directory path(mine is /Users/spd1994/Documents/,change it), where u want to store attachments in folder named by email subject
            if not os.path.exists(directory):
                os.makedirs(directory)
            filePath = os.path.join(directory, fileName)
            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
            subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
            print('Downloaded "{file}" from email titled "{subject}" with UID {uid}.'.format(file=fileName, subject=subject, uid=num.decode('utf-8')))
			