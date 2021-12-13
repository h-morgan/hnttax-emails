from dotenv.main import load_dotenv
from db.hntdb import hnt_db_engine as hnt_db
from db.hntdb import hnt_metadata
from fetchers.CsvEmailFetcher import CsvEmailFetcher
from loguru import logger
from utils import generate_email_content, get_csv_from_aws
from utils.email import send_email


def send_csv_emails(status, db_id):
    # where status can be None, processed, error, empty, or all

    fetcher = CsvEmailFetcher()
    table = hnt_metadata.tables[fetcher.DB_TABLE_NAME]
    
    # this is used to set subject of emails sent
    subject_map = {
        "processed": "hntTax - Your HNT Mining Summary",
        "empty": "hntTax - Your HNT Mining Summary (No Rewards Found)",
        "error": "hntTax - Your HNT Mining Summary (Wallet not Found)"
    }

    # get row(s) from hnttax db for which to send email for
    for item in fetcher.get_items(status=status, id=db_id):

        if item['status'] == "sent":
            logger.warning(f"[{fetcher.DB_TABLE_NAME}] retrieved already-sent row, skipping: id {item['id']}")
            continue
        
        if item['currency'] != "USD":
            logger.error(f"[{fetcher.DB_TABLE_NAME}] non-USD currency ({item['id'], }{item['currency']}) - no automated email support yet, terminating")
        
        else:
            # build hmtl/text file templates
            html = generate_email_content(item['status'], item['wallet'], item['year'], filetype="html")
            text = generate_email_content(item['status'], item['wallet'], item['year'], filetype="txt")

            # build filename to retrieve csv rewards from aws
            s3_file = f"csv_summary/{item['year']}/{item['id']}_{item['year']}_{item['wallet'][0:7]}.csv"
            local_csv = get_csv_from_aws(s3_file)

            # send email
            logger.info(f"[{fetcher.DB_TABLE_NAME}] sending email to {item['email']} (id {item['id']})")
            send_email(item['email'], subject=subject_map[item['status']], attachment=local_csv)

            # once email has been sent, update the "status" in the db
            update_status = table.update().where(table.c.id == int(item['id'])).values(status="sent")
            hnt_db.execute(update_status)

            logger.info(f"[{fetcher.DB_TABLE_NAME}] email sent for id {item['id']}, status updated in db")

    logger.info(f"[{fetcher.DB_TABLE_NAME}] DONE - csv emails sent")