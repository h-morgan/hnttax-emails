from abc import abstractclassmethod, abstractstaticmethod
from loguru import logger
from sqlalchemy import select
from abc import abstractstaticmethod
from db.hntdb import hnt_db_engine as hnt_db
from db.hntdb import hnt_metadata



class BaseFetcher:
    """
    Abstract class used as base for CSV and Schc exporters
    """

    DB_TABLE_NAME = None

    batch_size = None

    def __init__(self, batch_size=100):
        self.batch_size = batch_size

    def _prep_select_stmt(self, status, id, max_id):
        """
        Prepares select statement used to query the hnttax db for
        entries to send emails for
        """
        table = hnt_metadata.tables[self.DB_TABLE_NAME]
        all_statuses_to_send = ["processed", "error", "empty"]

        # prepare base select statement, in batches, ordered by id
        select_stmt = select([table]).limit(self.batch_size)

        # if given an id, process just that id:
        if id:
            select_stmt = select_stmt.where(table.c.id == id)
        
        # if given a status, only get db entries with this status
        elif status == "all":
            select_stmt = select_stmt.where(table.c.status in all_statuses_to_send)
        
        elif status is not None:
            select_stmt = select_stmt.where(table.c.status == status)
        
        select_stmt = select_stmt.order_by(table.c.id)

        # if given a max id, filter select stmt to only include ids > max_id
        if max_id is not None:
            select_stmt = select_stmt.where(table.c.id > max_id)

        return select_stmt

    def _get_rows_batch(self, status, id):
        """
        Query the Wordpress db in batches of self.batch_size, yield whole batch,
        determine max entry_id of the batch, continue process
        """
        
        if id:
            logger.info(f"[{self.DB_TABLE_NAME}] getting id {id} from HNTTAX db")

        else:
            logger.info(f"[{self.DB_TABLE_NAME}] getting batches of {self.batch_size} from HNTTAX db")
        
        max_id = None
        while True:
            select_stmt = self._prep_select_stmt(status, id, max_id=max_id)
            rows = hnt_db.execute(select_stmt).fetchall()

            if not rows:
                logger.info(f"[{self.DB_TABLE_NAME}] end of retrieval of data rows from HNTTAX db")
                break

            logger.info(f"[{self.DB_TABLE_NAME}] retrieved {len(rows)} row(s) of data from HNTTAX db")
            yield rows

            # get max entry_id value given last set of rows
            ids = []
            for row in rows:
                ids.append(row.id)

            max_id = max(ids)

    def _get_rows(self, status, id):
        """
        Calls _get_rows_batch and yields rows one by one
        """
        for rows in self._get_rows_batch(status, id):
            for row in rows:
                yield row

    def get_items(self, status=None, id=None):
        """
        Call get rows method to get rows where
        request_type = "csv" or "schc" --> the table to query
        status = None (when running for specific id) or "success", "error", "empty"
        """
        for row in self._get_rows(status, id):
            yield self._transform_item(row)

    @abstractstaticmethod
    def _transform_item(row):
        pass

