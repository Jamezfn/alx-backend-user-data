#!/usr/bin/env python
"""Regex-ing"""
import re
import logging

def filter_datum(fields, redaction, message, separator):
    """Returns the log message obfuscated"""
    pattern = f"({'|'.join(fields)}=[^{separator}]*)"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)

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
