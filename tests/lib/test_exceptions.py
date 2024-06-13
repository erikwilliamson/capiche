# Standard Library Imports
import time

# 3rd-Party Imports
import pytest
import requests

# Application-Local Imports
from capiche.lib import CallbackHandler, ThrottledQueue
from capiche.lib.exceptions import MessageException

def simple_callback(response: requests.Response) -> str:
    return f"RESPONSE: {response}"


def simple_request_no_args_no_return() -> None:
    pass


def simple_request_no_args_with_static_return() -> str:
    return "1"


def simple_request_that_returns_single_arg(num: int) -> int:
    return num


class TestMessageException:
    def test_instantiation(self):
        message = "this is a test"
        try:
            raise MessageException(message=message)
        except MessageException as exc:
            assert str(exc) == message
