#!/usr/bin/env python3
''' filter_datum '''
import re
import logging
from logging import StreamHandler
from filtered_formatter import RedactingFormatter
import csv


def filter_datum(fields, redaction, message, separator):
    return re.sub(r'(?<=^|\{0})[^{1}]+(?={0}|$)'.format(separator, separator), redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields
        
    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)


PII_FIELDS = ("name", "email", "phone", "address", "credit_card")

def get_logger():
    ''' logger '''
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger
