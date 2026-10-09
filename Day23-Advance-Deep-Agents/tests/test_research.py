from research import slugify, summarize
from collections import namedtuple

FakeMessage = namedtuple("FakeMessage", ["tool_calls", "usage_metadata"])

def test_slugify():
    assert slugify("survey about world model") == "survey-about-world-model"
    assert slugify("../../x") == "x"
    assert slugify("") == "topic"
    assert slugify("!@#$") == "topic"
    long_topic = "a" * 100
    assert len(slugify(long_topic)) <= 60

def test_summarize():
    msg1 = FakeMessage(
        tool_calls=[{"name": "write_todos"}, {"name": "task"}],
        usage_metadata={"input_tokens": 100, "output_tokens": 50}
    )
    msg2 = FakeMessage(
        tool_calls=[{"name": "task"}, {"name": "execute"}],
        usage_metadata={"input_tokens": 150, "output_tokens": 70}
    )
    res = summarize([msg1, msg2], 12.345, "test-model")
    assert res["model"] == "test-model"
    assert res["elapsed_s"] == 12.3
    assert res["subagent_calls"] == 2
    assert res["tool_calls"]["task"] == 2
    assert res["tool_calls"]["write_todos"] == 1
    assert res["tool_calls"]["execute"] == 1
    assert res["tokens"]["input"] == 250
    assert res["tokens"]["output"] == 120
