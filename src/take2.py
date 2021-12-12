import smtplib, ssl
from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid


port = 465  # For SSL
password = "kyleAlta1093"
sender_addr = "team@hnttax.us"
sender_email = Address(display_name="hntTax", username="team", domain="hnttax.us")
smtp_server_addr = "mail.hnttax.us"

receiver_email = ["haley@hnttax.us", "haleymorgan3264@gmail.com"]

msg = EmailMessage()
msg["Subject"] = "testing hnttax automated email"
msg["From"] = sender_email
msg["To"] = ', '.join(receiver_email)

# Add plain text version of message contents
textfile = "response.txt"
with open(textfile) as fp:
    msg.set_content(fp.read())

# add html version - complete with QR code image attachemt
hmtl_file = "response.html"
qrcode_cid = make_msgid()
with open(hmtl_file) as html:
    msg.add_alternative(html.read().format(qrcode_cid=qrcode_cid[1:-1]), subtype='html')


# Now add the related image to the html part.
with open("qrcode.jpg", 'rb') as img:
    msg.get_payload()[1].add_related(img.read(), 'image', 'jpeg',
                                     cid=qrcode_cid)

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server_addr, port, context=context) as server:
    server.login(sender_addr, password)
    
    server.send_message(msg)