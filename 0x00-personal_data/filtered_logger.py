#!/usr/bin/env python3
""""""
import re
from typing import List


def filter_datum(fields: List, redaction: str, message: str, separator: str):
    """Returns the log message obfuscated"""
    return re.sub(fr'({"|".join(fields)})=[^{separator}]+',
                  lambda field: f'{field.group(1)}={redaction}', message)


# TEST CODE:
#
# fields = ["password", "date_of_birth"]
# messages = [
#     "name=egg;email=eggmin@eggsample.com;password=eggcellent;\
# date_of_birth=12/12/1986;",
#     "name=bob;email=bob@dylan.com;password=bobbycool;\
# date_of_birth=03/04/1993;"]

# for message in messages:
#     print(filter_datum(fields, 'xxx', message, ';'))

# OUTPUT:
#
# name=egg;email=eggmin@eggsample.com;password=xxx;date_of_birth=xxx;
# name=bob;email=bob@dylan.com;password=xxx;date_of_birth=xxx;
