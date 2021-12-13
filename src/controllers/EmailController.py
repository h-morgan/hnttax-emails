from db.hntdb import hnt_db_engine as hnt_db
from db.hntdb import hnt_metadata
from fetchers.CsvEmailFetcher import CsvEmailFetcher
from loguru import logger
from utils import generate_email_content
from utils.email import send_email


def send_csv_emails(status, db_id):
    # where status can be None, processed, error, empty, or all

    fetcher = CsvEmailFetcher()
    table = fetcher.DB_TABLE_NAME
    
    # this is used to set subject of emails sent
    subject_map = {
        "processed": "hntTax - Your HNT Mining Summary",
        "empty": "hntTax - Your HNT Mining Summary (No Rewards Found)",
        "error": "hntTax - Your HNT Mining Summary (Wallet not Found)"
    }

    # get row(s) from hnttax db for which to send email for
    for item in fetcher.get_items(status=status, id=db_id):
        
        if item['currency'] != "USD":
            logger.error(f"[{fetcher.DB_TABLE_NAME}] non-USD currency ({item['id'], }{item['currency']}) - no automated email support yet, terminating")
        
        else:
            # build hmtl/text file templates
            html = generate_email_content(item['status'], item['wallet'], item['year'], filetype="html")
            text = generate_email_content(item['status'], item['wallet'], item['year'], filetype="txt")
            
            # send email
            logger.info(f"[{fetcher.DB_TABLE_NAME}] sending email to {item['email']} (id {item['id']})")
            send_email(item['email'], subject=subject_map[item['status']])