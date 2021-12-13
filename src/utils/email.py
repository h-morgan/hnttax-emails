import smtplib, ssl
from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid
import os
from dotenv import load_dotenv
from loguru import logger
from utils import get_template_file_path


load_dotenv()
# define constants 
PORT = 465  # For SSL
SMPT_SERVER_ADDR = "mail.hnttax.us"
SENDER_UN = os.getenv("SENDER_UN")
SENDER_ADDR = SENDER_UN + "@hnttax.us"
SENDER_PW = os.getenv("SENDER_PW")


def send_email(to_address, subject, attachment=None):

    # build sender email address object / addr info
    sender_email = Address(display_name="hntTax", username=SENDER_UN, domain="hnttax.us")

    # initialize email message 
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_address
    msg["Cc"] = ','.join(["danidiloreto14@gmail.com", "haley@hnttax.us"])

    # add plain text version of message 
    txtfile = "temp.txt"
    with open(txtfile) as fp:
        msg.set_content(fp.read())

    # add html version
    htmlfile = "temp.html"
    qrcode_cid = make_msgid()
    with open(htmlfile) as html:
        msg.add_alternative(html.read().format(qrcode_cid=qrcode_cid[1:-1]), subtype='html')

    # Now add the related image to the html part.
    with open("qrcode.jpg", 'rb') as img:
        msg.get_payload()[1].add_related(img.read(), 'image', 'jpeg',
                                        cid=qrcode_cid)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(SMPT_SERVER_ADDR, PORT, context=context) as server:
        server.login(SENDER_ADDR, SENDER_PW)
        server.send_message(msg)

    logger.info(f"[email] deleting temp content files {txtfile} and {htmlfile}")
    os.remove(txtfile)
    os.remove(htmlfile)