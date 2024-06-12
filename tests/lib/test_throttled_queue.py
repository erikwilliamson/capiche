# Standard Library Imports
import time

# 3rd-Party Imports
import pytest
import requests

# Application-Local Imports
from capiche.lib import CallbackHandler, ThrottledQueue


def simple_callback(response: requests.Response) -> str:
    return f"RESPONSE: {response}"


def simple_request_no_args_no_return() -> None:
    pass


def simple_request_no_args_with_static_return() -> str:
    return "1"


def simple_request_that_returns_single_arg(num: int) -> int:
    return num


class TestThrottledQueue:
    def test_instantiation(self):
        tq = ThrottledQueue(
            max_rate=5,
            window=5,
            cache_age=30,
            callback=CallbackHandler[requests.Response](callback=simple_callback),
            max_queue_size=2,
        )
        assert (
            repr(tq) == "ThrottledQueue(max_rate=5, window=5, callback=simple_callback, max_queue_size=2, cache_age=30"
        )

    def test_queueing_request(self):
        tq = ThrottledQueue(
            max_rate=1,
            window=1,
            cache_age=30,
            callback=CallbackHandler[requests.Response](callback=simple_callback),
            max_queue_size=None,
        )

        tq.queue_request(method=simple_callback)
        assert tq.queued_requests == 1

    def test_is_empty(self):
        tq = ThrottledQueue(
            max_rate=1,
            window=1,
            cache_age=30,
            callback=CallbackHandler[requests.Response](callback=simple_callback),
            max_queue_size=None,
        )

        assert tq.is_empty is True

    def test_is_full(self):
        tq = ThrottledQueue(
            max_rate=1,
            window=1,
            cache_age=30,
            callback=CallbackHandler[requests.Response](callback=simple_callback),
            max_queue_size=2,
        )

        tq.queue_request(method=simple_callback)
        tq.queue_request(method=simple_callback)

        assert tq.queued_requests == 2
        assert tq.is_full is True

    def test_rate(self):
        tq = ThrottledQueue(
            max_rate=1,
            window=1,
            cache_age=30,
            callback=CallbackHandler[requests.Response](callback=simple_callback),
            max_queue_size=2,
        )

        tq.queue_request(method=simple_request_no_args_no_return)

        # since we haven't started processing, the rate should be 0
        assert tq.rate == 0

        tq.start()

        time.sleep(0.1)  # Give it a sec to complete...

        assert tq.rate == 1


class TestCache:
    def test_cache_no_args(self):
        tq = ThrottledQueue(
            max_rate=10,
            window=1,
            cache_age=30,
            callback=CallbackHandler[requests.Response](callback=simple_callback),
            max_queue_size=2,
        )

        tq.queue_request(method=simple_request_no_args_with_static_return, use_cache=True)

        tq.start()

        assert tq.cache.keys() == {"simple_request_no_args_with_static_returnNoneNone"}

    @pytest.mark.wip
    def test_cache_no_args_with_cache_hit(self):
        tq = ThrottledQueue(
            max_rate=10,
            window=30,
            cache_age=30,
            callback=CallbackHandler[requests.Response](callback=simple_callback),
            max_queue_size=2,
        )

        # Initial request with an empty cache
        tq.queue_request(method=simple_request_no_args_with_static_return, use_cache=True)

        # Subsequent identical call should have a cache hit
        tq.queue_request(method=simple_request_no_args_with_static_return, use_cache=True)

        tq.start()

        time.sleep(0.1)
        # print("\n\n\n", tq.completed_api_call_times, "\n\n\n")

        assert len(tq.completed_api_call_times) == 1

    def test_cache_with_named_args_with_cache_hit(self):
        tq = ThrottledQueue(
            max_rate=10,
            window=1,
            cache_age=30,
            callback=CallbackHandler[requests.Response](callback=simple_callback),
            max_queue_size=2,
        )

        tq.start()

        tq.queue_request(method=simple_request_that_returns_single_arg, kwargs={"num": 1}, use_cache=True)

        time.sleep(0.1)

        assert len(tq.completed_api_call_times) == 1

        time.sleep(0.1)

        tq.queue_request(method=simple_request_that_returns_single_arg, kwargs={"num": 2}, use_cache=True)

        time.sleep(0.1)

        assert len(tq.completed_api_call_times) == 2
