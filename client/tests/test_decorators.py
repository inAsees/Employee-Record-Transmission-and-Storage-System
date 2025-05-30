import pytest
import asyncio
from client.middleware.decorators import log_execution_time, retry_on_failure


@pytest.mark.asyncio
async def test_log_execution_time_decorator(caplog):
    @log_execution_time
    async def dummy_func():
        await asyncio.sleep(0.1)
        return "done"

    result = await dummy_func()
    assert result == "done"
    assert any("dummy_func executed in" in msg for msg in caplog.text.splitlines())


@pytest.mark.asyncio
async def test_retry_on_failure_success():
    calls = []

    @retry_on_failure(retries=2)
    async def test_func():
        calls.append(1)
        return "success"

    result = await test_func()
    assert result == "success"
    assert len(calls) == 1


@pytest.mark.asyncio
async def test_retry_on_failure_with_retries():
    calls = []

    @retry_on_failure(retries=3)
    async def test_func():
        calls.append(1)
        if len(calls) < 3:
            raise ValueError("fail")
        return "ok"

    result = await test_func()
    assert result == "ok"
    assert len(calls) == 3
