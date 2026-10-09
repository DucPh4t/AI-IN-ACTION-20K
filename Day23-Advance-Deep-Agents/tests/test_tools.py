import pytest
from tools import with_retry, RetryableError, arxiv_search, hf_daily_papers, hf_search_papers


def test_with_retry_succeeds_immediately():
    calls = 0
    def fn():
        nonlocal calls
        calls += 1
        return "ok"
    assert with_retry(fn, attempts=3, base=0.01) == "ok"
    assert calls == 1


def test_with_retry_eventual_success():
    calls = 0
    def fn():
        nonlocal calls
        calls += 1
        if calls < 3:
            raise RetryableError("transient", retry_after=0.01)
        return "success"
    assert with_retry(fn, attempts=4, base=0.01) == "success"
    assert calls == 3


def test_with_retry_exhausted():
    calls = 0
    def fn():
        nonlocal calls
        calls += 1
        raise RetryableError("fail", retry_after=0.01)
    with pytest.raises(RetryableError):
        with_retry(fn, attempts=3, base=0.01)
    assert calls == 3


def test_with_retry_non_retryable_error_not_caught():
    calls = 0
    def fn():
        nonlocal calls
        calls += 1
        raise ValueError("programming bug")
    with pytest.raises(ValueError):
        with_retry(fn, attempts=3, base=0.01)
    assert calls == 1
