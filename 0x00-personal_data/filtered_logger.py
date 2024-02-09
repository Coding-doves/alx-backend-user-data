#!/usr/bin/env python3
''' filter_datum '''
import re
import logging
from logging import StreamHandler
from typing import List
import csv
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    ''' filter '''
    return re.sub(r'(?<=^|\{0})[^{1}]+(?={0}|$)'.format(separator, separator),
                  redaction, message)


def get_db() -> mysql.connector.connection.MySQLConnection:
    ''' connect to db '''
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    dbname = os.getenv("PERSONAL_DATA_DB_NAME")

    if not dbname:
        raise ValueError(
            "Database name not provided in environment variable "
            "PERSONAL_DATA_DB_NAME"
        )

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=dbname
    )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        ''' initialize '''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        ''' format '''
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.getMessage(),
            self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    ''' logger '''
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def main():
    ''' entry point '''
    logger = get_logger()
    db_connection = get_db()
    cursor = db_connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    for row in rows:
        filtered_row = {key: "***" if key in [
                "name",
                "email",
                "phone",
                "ssn",
                "password"] else value for key, value in row.items()}
        logger.info(filtered_row)

    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()
