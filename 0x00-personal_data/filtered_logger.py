#!/usr/bin/env python3
"""Module to return the log message obfuscated"""
import re


def filter_datum(fields, redaction, message, separator):
    """Returns the log message obfuscated"""
    return re.sub(fr'({"|".join(fields)})=[^{separator}]+',
                  lambda field: f'{field.group(1)}={redaction}', message)
