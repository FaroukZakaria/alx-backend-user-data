#!/usr/bin/env python3
"""
Logging an obfuscated message
"""

import re

def filter_datum(fields, redaction, message, separator):
    return re.sub(f"({'|'.join(fields)})", redaction, message)