import smtplib, ssl
from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid
import os
from dotenv import load_dotenv
from loguru import logger
from utils import get_template_file_path
import mimetypes


load_dotenv()
# define constants 
PORT = 465  # For SSL
SMPT_SERVER_ADDR = "mail.hnttax.us"
SENDER_UN = os.getenv("SENDER_UN")
SENDER_ADDR = SENDER_UN + "@hnttax.us"
SENDER_PW = os.getenv("SENDER_PW")


def send_email(to_address, subject, hotspot_attachment=None, validator_attachment=None):

    # build sender email address object / addr info
    sender_email = Address(display_name="hntTax", username=SENDER_UN, domain="hnttax.us")

    # initialize email message 
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_address
    msg["Cc"] = "team@hnttax.us"

    # add plain text version of message 
    txtfile = "temp.txt"
    with open(txtfile) as fp:
        msg.set_content(fp.read())

    # add html version
    htmlfile = "temp.html"
    qrcode_cid = make_msgid(domain="hnttax.us")
    with open(htmlfile) as html:
        msg.add_alternative(html.read().format(qrcode_cid=qrcode_cid[1:-1]), subtype='html')

    # Now add the related image to the html part.
    with open("qrcode.jpg", 'rb') as img:
        # know the Content-Type of the image
        maintype, subtype = mimetypes.guess_type(img.name)[0].split('/')
        # attach it
        msg.get_payload()[1].add_related(img.read(), maintype=maintype, subtype=subtype, cid=qrcode_cid)

    # add csv attachment to message (if we have one, errors and emptys wont)
    if hotspot_attachment:
        with open(hotspot_attachment, 'rb') as attach:
            content = attach.read()
            msg.add_attachment(content, maintype='application', subtype='csv', filename="hnt_hotspot_rewards.csv")
        
    # add csv attachment to message (if we have one, errors and emptys wont)
    if validator_attachment:
        with open(validator_attachment, 'rb') as attach2:
            content2 = attach2.read()
            msg.add_attachment(content2, maintype='application', subtype='csv', filename="hnt_validator_rewards.csv")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(SMPT_SERVER_ADDR, PORT, context=context) as server:
        server.login(SENDER_ADDR, SENDER_PW)
        server.send_message(msg)

    logger.info(f"[email] deleting temp content files {txtfile} and {htmlfile}")
    os.remove(txtfile)
    os.remove(htmlfile)