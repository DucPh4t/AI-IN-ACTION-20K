### Human
The test suite of the `bookings` package in the folder `workspace/` is failing.

Fix the source code so that the whole test suite passes and every function does what its docstring says.
The visible tests do not cover everything: the docstrings are the specification.
Do not modify the existing files in `tests/`.
Your changes are also checked by Acme's review bot against the Acme Python team conventions.

When you are done, reply with a short summary of what you changed and why.


### Tool call: ls
{"path": "workspace"}

### Tool result
['/workspace/CHANGELOG.md', '/workspace/README.md', '/workspace/bookings/', '/workspace/tests/']

### Tool call: ls
{"path": "workspace/bookings"}

### Tool result
['/workspace/bookings/__init__.py', '/workspace/bookings/__pycache__/', '/workspace/bookings/billing.py', '/workspace/bookings/calendar_export.py', '/workspace/bookings/schedule.py', '/workspace/bookings/timeutil.py']

### Tool call: ls
{"path": "workspace/tests"}

### Tool result
['/workspace/tests/__pycache__/', '/workspace/tests/test_bookings.py']

### Tool call: execute
{"command": "python3 -m unittest discover workspace/tests"}

### Tool result
[stderr] E
[stderr] ======================================================================
[stderr] ERROR: test_bookings (unittest.loader._FailedTest.test_bookings)
[stderr] ----------------------------------------------------------------------
[stderr] ImportError: Failed to import test module: test_bookings
[stderr] Traceback (most recent call last):
[stderr]   File "/opt/homebrew/Cellar/python@3.12/3.12.12/Frameworks/Python.framework/Versions/3.12/lib/python3.12/unittest/loader.py", line 396, in _find_test_path
[stderr]     module = self._get_module_from_name(name)
[stderr]              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
[stderr]   File "/opt/homebrew/Cellar/python@3.12/3.12.12/Frameworks/Python.framework/Versions/3.12/lib/python3.12/unittest/loader.py", line 339, in _get_module_from_name
[stderr]     __import__(name)
[stderr]   File "/private/var/folders/xb/wpr2fgbj5cvd7jfrf5vzcnr00000gn/T/lab-sandbox-flyxr5_h/workspace/tests/test_bookings.py", line 1, in <module>
[stderr]     from bookings.billing import billable_blocks
[stderr] ModuleNotFoundError: No module named 'bookings'
[stderr] 
[stderr] 
[stderr] ----------------------------------------------------------------------
[stderr] Ran 1 test in 0.000s
[stderr] 
[stderr] FAILED (errors=1)

Exit code: 1
[Command failed with exit code 1]

### Tool call: execute
{"command": "export PYTHONPATH=$PYTHONPATH:$(pwd)/workspace && python3 -m unittest discover workspace/tests"}

### Tool result
[stderr] ----------------------------------------------------------------------
[stderr] Ran 0 tests in 0.000s
[stderr] 
[stderr] NO TESTS RAN

Exit code: 5
[Command failed with exit code 5]

### Tool call: read_file
{"file_path": "workspace/tests/test_bookings.py"}

### Tool result
@@ lines 1-15 of 15 @@
from bookings.billing import billable_blocks
from bookings.schedule import add_slot, total_minutes


def test_total_minutes_mixed_formats():
    assert total_minutes(["1h30m", "2h"]) == 210


def test_billable_blocks_rounds_up():
    assert billable_blocks(20) == 2
    assert billable_blocks(45) == 3


def test_add_slot_single_call():
    assert add_slot("a") == ["a"]

### Tool call: execute
{"command": "export PYTHONPATH=$PYTHONPATH:$(pwd)/workspace && python3 -m pytest workspace/tests/test_bookings.py"}

### Tool result
============================= test session starts ==============================
platform darwin -- Python 3.12.12, pytest-9.1.1, pluggy-1.6.0
rootdir: /private/var/folders/xb/wpr2fgbj5cvd7jfrf5vzcnr00000gn/T/lab-sandbox-flyxr5_h
plugins: langsmith-0.14.4, anyio-4.15.1
collected 3 items

workspace/tests/test_bookings.py FF.                                     [100%]

=================================== FAILURES ===================================
_______________________ test_total_minutes_mixed_formats _______________________

    def test_total_minutes_mixed_formats():
>       assert total_minutes(["1h30m", "2h"]) == 210
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

~/LAB-VINUNI/phase_2/K4-L3L4-Track3-Day20-AdvanceMultiAgents/tasks/code-eval/workspace/tests/test_bookings.py:6: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
workspace/bookings/schedule.py:7: in total_minutes
    return sum(parse_duration(d) for d in durations)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
workspace/bookings/schedule.py:7: in <genexpr>
    return sum(parse_duration(d) for d in durations)
               ^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

text = '2h'

    def parse_duration(text):
        """Convert a duration string to whole minutes (int).
    
        Supported formats:
          "1h30m" -> 90
          "2h"    -> 120
          "45m"   -> 45
          "1:30"  -> 90
          "45"    -> 45

### Tool call: read_file
{"file_path": "workspace/bookings/timeutil.py"}

### Tool result
@@ lines 1-19 of 19 @@
"""Time helpers for the bookings package."""
import re


def parse_duration(text):
    """Convert a duration string to whole minutes (int).

    Supported formats:
      "1h30m" -> 90
      "2h"    -> 120
      "45m"   -> 45
      "1:30"  -> 90
      "45"    -> 45    # a bare number means minutes
    Surrounding whitespace is ignored.
    """
    m = re.fullmatch(r"(\d+)h(\d+)m", text.strip())
    if not m:
        raise ValueError(f"bad duration: {text!r}")
    return int(m.group(1)) * 60 + int(m.group(2))

### Tool call: read_file
{"file_path": "workspace/bookings/billing.py"}

### Tool result
@@ lines 1-11 of 11 @@
"""Billing rules."""


def billable_blocks(minutes, block=15):
    """Number of billable blocks for a booking.

    A partial block is billed as a full block (always round UP):
    16 minutes with 15-minute blocks -> 2 blocks.
    `minutes` must be >= 0; a negative value raises ValueError.
    """
    return round(minutes / block)

### Tool call: edit_file
{"new_string": "    import math\n    if minutes < 0:\n        raise ValueError(\"minutes must be >= 0\")\n    return math.ceil(minutes / block)", "file_path": "workspace/bookings/billing.py", "old_string": "    return round(minutes / block)"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/billing.py'

### Tool call: edit_file
{"new_string": "    text = text.strip()\n    # \"1h30m\"\n    m = re.fullmatch(r\"(\\d+)h(\\d+)m\", text)\n    if m:\n        return int(m.group(1)) * 60 + int(m.group(2))\n    # \"2h\"\n    m = re.fullmatch(r\"(\\d+)h\", text)\n    if m:\n        return int(m.group(1)) * 60\n    # \"45m\"\n    m = re.fullmatch(r\"(\\d+)m\", text)\n    if m:\n        return int(m.group(1))\n    # \"1:30\"\n    m = re.fullmatch(r\"(\\d+):(\\d+)\", text)\n    if m:\n        return int(m.group(1)) * 60 + int(m.group(2))\n    # \"45\"\n    m = re.fullmatch(r\"(\\d+)\", text)\n    if m:\n        return int(m.group(1))\n    \n    raise ValueError(f\"bad duration: {text!r}\")", "old_string": "    m = re.fullmatch(r\"(\\d+)h(\\d+)m\", text.strip())\n    if not m:\n        raise ValueError(f\"bad duration: {text!r}\")\n    return int(m.group(1)) * 60 + int(m.group(2))", "file_path": "workspace/bookings/timeutil.py"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/timeutil.py'

### Tool call: execute
{"command": "export PYTHONPATH=$PYTHONPATH:$(pwd)/workspace && python3 -m pytest workspace/tests/test_bookings.py"}

### Tool result
============================= test session starts ==============================
platform darwin -- Python 3.12.12, pytest-9.1.1, pluggy-1.6.0
rootdir: /private/var/folders/xb/wpr2fgbj5cvd7jfrf5vzcnr00000gn/T/lab-sandbox-flyxr5_h
plugins: langsmith-0.14.4, anyio-4.15.1
collected 3 items

workspace/tests/test_bookings.py ...                                     [100%]

============================== 3 passed in 0.00s ===============================

[Command succeeded with exit code 0]

### Tool call: read_file
{"file_path": "workspace/bookings/schedule.py"}

### Tool result
@@ lines 1-17 of 17 @@
"""Schedule helpers."""
from .timeutil import parse_duration


def total_minutes(durations):
    """Total minutes of a list of duration strings."""
    return sum(parse_duration(d) for d in durations)


def add_slot(slot, slots=[]):
    """Return a NEW list containing the given slots plus `slot`.

    Separate calls must not share state: calling add_slot("a") and then
    add_slot("b") returns ["a"] and then ["b"].
    """
    slots.append(slot)
    return slots

### Tool call: edit_file
{"old_string": "def add_slot(slot, slots=[]):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    slots.append(slot)\n    return slots", "file_path": "workspace/bookings/schedule.py", "new_string": "def add_slot(slot, slots=None):\n    \"\"\"Return a NEW list containing the given slots plus `slot`.\n\n    Separate calls must not share state: calling add_slot(\"a\") and then\n    add_slot(\"b\") returns [\"a\"] and then [\"b\"].\n    \"\"\"\n    if slots is None:\n        slots = []\n    return slots + [slot]"}

### Tool result
Successfully replaced 1 instance(s) of the string in '/workspace/bookings/schedule.py'

### Tool call: execute
{"command": "export PYTHONPATH=$PYTHONPATH:$(pwd)/workspace && python3 -m pytest workspace/tests/test_bookings.py"}

### Tool result
============================= test session starts ==============================
platform darwin -- Python 3.12.12, pytest-9.1.1, pluggy-1.6.0
rootdir: /private/var/folders/xb/wpr2fgbj5cvd7jfrf5vzcnr00000gn/T/lab-sandbox-flyxr5_h
plugins: langsmith-0.14.4, anyio-4.15.1
collected 3 items

workspace/tests/test_bookings.py ...                                     [100%]

============================== 3 passed in 0.00s ===============================

[Command succeeded with exit code 0]

### Tool call: read_file
{"file_path": "workspace/bookings/calendar_export.py"}

### Tool result
@@ lines 1-7 of 7 @@
"""Calendar export."""
from .timeutil import parse_duration


def slot_end(start_minute, duration_text):
    """Minute of the day at which a slot ends."""
    return start_minute + parse_duration(duration_text)

### Tool call: read_file
{"file_path": "workspace/bookings/__init__.py"}

### Tool result
@@ lines 1-1 of 1 @@
__version__ = "1.4.2"

### Tool call: execute
{"command": "export PYTHONPATH=$PYTHONPATH:$(pwd)/workspace && python3 -m pytest workspace/tests/test_bookings.py"}

### Tool result
============================= test session starts ==============================
platform darwin -- Python 3.12.12, pytest-9.1.1, pluggy-1.6.0
rootdir: /private/var/folders/xb/wpr2fgbj5cvd7jfrf5vzcnr00000gn/T/lab-sandbox-flyxr5_h
plugins: langsmith-0.14.4, anyio-4.15.1
collected 3 items

workspace/tests/test_bookings.py ...                                     [100%]

============================== 3 passed in 0.00s ===============================

[Command succeeded with exit code 0]

### Assistant
[{'type': 'text', 'text': 'I have fixed the issues in the `bookings` package to ensure the test suite passes and the functions adhere to their docstring specifications.\n\n### Changes:\n1.  **`workspace/bookings/billing.py`**: Updated `billable_blocks` to correctly round up using `math.ceil` instead of `round`, and added a check to raise a `ValueError` for negative input as specified in the docstring.\n2.  **`workspace/bookings/timeutil.py`**: Updated `parse_duration` to support all formats listed in its docstring (`"1h30m"`, `"2h"`, `"45m"`, `"1:30"`, `"45"`).\n3.  **`workspace/bookings/schedule.py`**: Fixed `add_slot` to avoid the mutable default argument issue and ensure it returns a new list, preventing state leakage between calls.\n\nAll tests in `workspace/tests/test_bookings.py` now pass.', 'extras': {'signature': 'EnMKcQFpFH0TEc9hTm0wKStQNIcWUj/H0PoYs8rk1T6DCMr83XSPopqvF948NyIk8E2NNtqH5l9oHN6jpQgYMi/lUo6L6YGjI5Hw2twfH1U/x5uPTLx9FEanLu/2ndZDQP7m8pRsg/njvJ1kQ787d6Z6rNmB'}}]