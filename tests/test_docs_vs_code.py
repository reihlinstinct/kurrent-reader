"""Two-way docs-vs-code drift check (issue #34).

- Every subcommand and flag in cli.py must appear in the docs, or carry an
  allowlist entry with a reason.
- Every CLI token the docs present as kurrent-reader syntax must exist in
  the code.
- The paths in the README layout section must exist on disk.
- The three version carriers (VERSION, pyproject.toml, __init__.__version__)
  must agree.

Stdlib only, offline; sources are parsed as text so no dependency is needed.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "src" / "kurrent_reader" / "cli.py"
DOC_FILES = sorted(ROOT.glob("*.md"))
ALLOWLIST = ROOT / ".github" / "docs-vs-code-allowlist.txt"

SUB_TOKEN_RE = re.compile(r"[a-z][a-z0-9-]*")
FLAG_TOKEN_RE = re.compile(r"--[a-z][a-z0-9-]*")
DOC_FLAG_RE = re.compile(r"--[a-z][a-z0-9-]*")
DOC_CMD_RE = re.compile(r"kurrent-reader\s+([a-z][a-z0-9-]*)")


def _allowlist() -> dict[str, str]:
    out: dict[str, str] = {}
    if ALLOWLIST.is_file():
        for line in ALLOWLIST.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            token, _, reason = line.partition("#")
            token = token.strip()
            assert reason.strip(), f"allowlist entry without a reason: {line}"
            out[token] = reason.strip()
    return out


def _string_calls(tree: ast.AST, attr: str) -> list[str]:
    """First positional string argument of every `<anything>.attr(...)` call."""
    out = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == attr
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
        ):
            out.append(node.args[0].value)
    return out


def _tokens_from_source(text: str) -> tuple[set[str], set[str]]:
    tree = ast.parse(text)
    subs = {s for s in _string_calls(tree, "add_parser") if SUB_TOKEN_RE.fullmatch(s)}
    flags = {
        f for f in _string_calls(tree, "add_argument") if FLAG_TOKEN_RE.fullmatch(f)
    }
    return subs, flags - {"--help"}


def cli_tokens() -> tuple[set[str], set[str]]:
    return _tokens_from_source(CLI.read_text(encoding="utf-8"))


def test_token_parser_handles_any_quote_style_and_multiline() -> None:
    # Regression for the regex extractor (#36): it only matched double-quoted
    # single-line calls, so a single-quoted flag would pass silently.
    src = (
        "p = sub.add_parser('fix')\n"
        + "p.add_argument(\n"
        + "    '--dry-run',\n"
        + "    action='store_true',\n"
        + ")\n"
    )
    subs, flags = _tokens_from_source(src)
    assert "fix" in subs
    assert "--dry-run" in flags
