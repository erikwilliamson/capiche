# Application-Local Imports
from capiche.lib.constants import DEFAULT_CACHE_DURATION, THREAD_SLEEP_TIME


class TestConstants:
    def test_constants(self):
        assert THREAD_SLEEP_TIME == 0.1
        assert DEFAULT_CACHE_DURATION == 60 * 60
