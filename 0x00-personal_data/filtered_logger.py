#!/usr/bin/env python3
"""Module to return the log message obfuscated"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str):
    """Returns the log message obfuscated"""
    return re.sub(fr'({"|".join(fields)})=[^{separator}]+',
                  lambda field: f'{field.group(1)}={redaction}', message)
