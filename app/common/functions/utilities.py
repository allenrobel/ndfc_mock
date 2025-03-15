import random
import string
from datetime import datetime


def get_datetime() -> datetime:
    """
    We specifically do NOT want to store timezone info
    in the datetime object since we don't need it.  Rather,
    we are treating datetime like a timestamp.
    """
    return datetime.now().replace(tzinfo=None)


def gen_hex(length) -> str:
    """
    Generate a random hex string of length `length`.
    """
    return "".join(random.choice("0123456789ABCDEF") for _ in range(length))


def gen_number(length) -> str:
    """
    Generate a random number of length `length`.
    """
    return "".join(random.choice("0123456789") for _ in range(length))


def gen_string(length) -> str:
    """
    Generate a random alphabetic string of length `length`.
    """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def random_unicast_mac_address() -> str:
    """
    Generate a random unicast MAC address, with an OUI of 00:AA:BB.
    """
    return f"00:AA:BB:{gen_hex(2)}:{gen_hex(2)}:{gen_hex(2)}"


def random_switch_serial_number() -> str:
    """
    # Summary

    Generate a random switch serial number.

    FOX2109PGCS
    """
    return f"FOX{gen_number(4)}{gen_string(4).upper()}"
