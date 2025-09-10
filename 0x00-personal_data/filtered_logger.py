#!/usr/bin/env python
"""
Personal data
"""
import re

def filter_datum(fields, redaction, message, separator):
    """Regex-ing"""
    pattern = rf"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
