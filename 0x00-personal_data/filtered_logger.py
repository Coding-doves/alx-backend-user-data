#!/usr/bin/env python3
''' filter_datum '''
import re


def filter_datum(fields, redaction, message, separator):
    return re.sub(r'(?<=^|\{0})[^{1}]+(?={0}|$)'.format(separator, separator), redaction, message)
