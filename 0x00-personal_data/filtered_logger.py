#!/usr/bin/env python3
''' filter_datum '''
import re
import logging


def filter_datum(fields, redaction, message, separator):
    return re.sub(r'(?<=^|\{0})[^{1}]+(?={0}|$)'.format(separator, separator), redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError
