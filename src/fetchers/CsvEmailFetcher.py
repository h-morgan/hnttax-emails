from fetchers.BaseFetcher import BaseFetcher


class CsvEmailFetcher(BaseFetcher):
    """
    Abstract class used as base for CSV and Schc exporters
    """

    DB_TABLE_NAME = "hnt_csv_requests"

    @staticmethod
    def _transform_item(row):
        # get status, id (for filename and updates), year, wallet, email
        row_id = row.id
        status = row.status
        email = row.email
        year = row.year
        wallet = row.wallet
        currency = row.local_currency

        return {
            "id": row_id,
            "status": status,
            "email": email,
            "year": year,
            "wallet": wallet,
            "currency": currency
        }