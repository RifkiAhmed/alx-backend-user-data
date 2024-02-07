#!/usr/bin/env python3
"""Module to return the log message obfuscated"""
import logging
import re
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Returns the log message obfuscated"""
    return re.sub(fr'({"|".join(fields)})=[^{separator}]+',
                  lambda field: f'{field.group(1)}={redaction}', message)


def get_logger() -> logging.Logger:
    """Return a Logger object"""
    logger = logging.getLogger("user_data", 20)
    logger.propagate = False
    handler = logging.StreamHandler(RedactingFormatter())
    logger.addHandler(handler)
    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.__fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records"""
        record.msg: str = filter_datum(self.__fields, self.REDACTION,
                                       record.getMessage(), self.SEPARATOR)
        return super().format(record)
