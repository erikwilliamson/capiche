# Application-Local Imports
from capiche.lib import ThrottledRequest


class TestThrottledRequest:
    def test_instantiation(self):
        def test_method():
            pass

        tr = ThrottledRequest(method=test_method, use_cache=True, args=[1], kwargs={"x": 1})

        assert repr(tr) == "ThrottledRequest(method=test_method, args=[1], kwargs={'x': 1}, use_cache=True)"

    def test_cache_key_with_args_and_kwargs(self):
        def test_method():
            pass

        tr = ThrottledRequest(method=test_method, use_cache=True, args=[1], kwargs={"x": 1})

        assert tr.cache_key == "test_method[1]{'x': 1}"

    def test_cache_key_with_args(self):
        def test_method():
            pass

        tr = ThrottledRequest(method=test_method, use_cache=True, args=[1])

        assert tr.cache_key == "test_method[1]None"

    def test_cache_key_with_kwargs(self):
        def test_method():
            pass

        tr = ThrottledRequest(method=test_method, use_cache=True, kwargs={"x": 1})

        assert tr.cache_key == "test_methodNone{'x': 1}"

    def test_cache_key_without_args(self):
        def test_method():
            pass

        tr = ThrottledRequest(method=test_method, use_cache=True)

        assert tr.cache_key == "test_methodNoneNone"
