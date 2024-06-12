from capiche.lib.constants import THREAD_SLEEP_TIME, DEFAULT_CACHE_DURATION

class TestConstants:
    def test_constants(self):
        assert THREAD_SLEEP_TIME == 0.1
        assert DEFAULT_CACHE_DURATION == 60 * 60
