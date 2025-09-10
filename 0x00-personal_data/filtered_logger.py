#!/usr/bin/env python
"""
Personal data
"""
import re
import logging

def filter_datum(fields, redaction, message, separator):
    """Regex-ing"""
    pattern = rf"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super().__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError
