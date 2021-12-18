import click
from loguru import logger
from datetime import datetime

from sqlalchemy.sql.operators import is_distinct_from
from controllers.EmailController import send_csv_emails 


@click.command()
@click.option("--request", '-r', default="csv", type=click.Choice(["csv", "schc"]))
@click.option("--status", '-s', default="all", type=click.Choice(["processed", "empty", "error", "all"]))
@click.option("--id", default=None, help="the id for the row in the hnttax db to create/send an email for")
def run(request, status, id):

    # set service name for logging
    service_name = "email-cli"
    
    # set now datetime
    now = datetime.utcnow()

    # TODO: buildout sched c email functionality
    if request == 'schc':
        logger.warning(f"[{service_name}] schedule c emailing is not yet supported, terminating")
        return

    elif request == "csv":
        logger.info(f"[{service_name}] csv request emails - preparing to send")

        # TODO: buildout functionality to bulk send emails for specific statuses
        if status in ("empty", "error", "all") and id is None:
            logger.warning(f"[{service_name}] bulk email by status is not yet supported, terminating")  

        if id:
            logger.info(f"[{service_name}] sending email for db id: {id}")
            send_csv_emails(status, id)
        
        else:
            logger.info(f"[{service_name}] sending email for csv db rows with status: {status}")
            send_csv_emails(status, id)


if __name__ == "__main__":

    run()