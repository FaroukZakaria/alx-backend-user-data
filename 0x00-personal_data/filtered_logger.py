#!/usr/bin/env python3
"""
Logging an obfuscated message
"""

import re
import logging
import os
import mysql.connector


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = self.filter_message(record.msg)
        return super().format(record)

    def filter_message(self, message: str) -> str:
        return filter_datum(
            self.fields, self.REDACTION,
            message, self.SEPARATOR)


def filter_datum(fields, redaction, message, separator):
    """
    Filters datum and returns logged message
    """
    return re.sub(f"({'|'.join(fields)})", redaction, message)

PII_FIELDS = ("name", "email", "phone", "ssn", "password")

def get_logger() -> logging.Logger:
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    connector = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )

    return connector