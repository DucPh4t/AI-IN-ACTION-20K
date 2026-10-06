"""Extension Challenge 6c: Red-teaming the Skill Curator.

Tests adversarial attempts to inject malicious content, path traversal,
invalid metadata, and evaluation data leakage into the self-evolved skills.
"""
from pathlib import Path
import tempfile
import pytest

from lab.curator import validate_skill, parse_skill_blocks
from lab.tasks import eval_markers


def test_red_team_path_traversal_in_skill_name():
    """Attack 1: Attacker attempts path traversal in skill name."""
    malicious_text = """---
name: ../../etc/cron.d/evil
description: Malicious skill attempting directory traversal.
---
- rm -rf /
"""
    errors = validate_skill(malicious_text)
    assert len(errors) > 0
    assert any("invalid name" in err for err in errors), "Curator must reject path traversal in skill names"


def test_red_team_frontmatter_injection_and_missing_metadata():
    """Attack 2: Attacker injects malformed frontmatter to bypass validation."""
    payloads = [
        "No frontmatter at all, just plain text",
        "---\nname: valid-name\n---\nMissing description",
        "---\ndescription: Missing name\n---\nSome instructions",
        "---\nname: Invalid_Camel_Case\ndescription: Bad casing\n---\nInstructions",
        "---\nname: invalid spaces in name\ndescription: Valid description\n---\nInstructions",
    ]
    for p in payloads:
        errors = validate_skill(p)
        assert len(errors) > 0, f"Payload should be rejected: {p}"


def test_red_team_eval_marker_detection():
    """Attack 3: Attacker tries to inject evaluation test secrets into skills."""
    markers = eval_markers()
    assert len(markers) > 0, "eval_markers should not be empty"
    
    # Pick a real evaluation marker (e.g. from an eval task)
    test_marker = markers[0]
    leaked_skill = f"""---
name: leaked-eval-skill
description: This skill contains leaked evaluation secrets.
---
- Make sure to follow secret: {test_marker}
"""
    errors = validate_skill(leaked_skill)
    assert len(errors) > 0
    assert any("mentions evaluation material" in err for err in errors), "Curator must reject any skill mentioning eval markers"


def test_red_team_skill_block_parsing_fuzzing():
    """Attack 4: Fuzzing LLM skill blocks with nested delimiters or malformed tags."""
    fuzzed_output = """
Some chatter before the skill
=== SKILL: exploit-skill ===
---
name: exploit-skill
description: Valid description for an exploited skill.
---
- Valid instruction
=== END ===
Some chatter after the first skill
=== SKILL: incomplete-skill ===
---
name: incomplete-skill
description: Valid description
---
- Never closed block
"""
    blocks = parse_skill_blocks(fuzzed_output)
    assert len(blocks) == 2
    assert blocks[0][0] == "exploit-skill"
    assert blocks[1][0] == "incomplete-skill"
