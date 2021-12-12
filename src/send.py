import click
from loguru import logger
from datetime import datetime


@click.command()
@click.option("--request", '-r', default="csv", type=click.Choice(["csv", "schc"]))
@click.option("--status", '-s', default='id', type=click.Choice(["success", "empty", "error", "id"]))
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

    # TODO: buildout functionality to bulk send emails for specific statuses
    if status in ("success", "empty", "error"):
        logger.warning(f"[{service_name}] bulk email by status is not yet supported, terminating")
        return     

    # if the service requested is to process for an id, and no id is passed, log error
    if status == "id" and id is None:
        logger.error(f"[{service_name}] you must pass an id for the db row to create/send an email for")

    elif status == "id" and id:
        logger.info(f"[{service_name}] generating email for {request} request, id {id} in db table")

    
    else:
        logger.warn("Incompatible service requested. Please fetch csv, schc, or both.")


if __name__ == "__main__":

    run()