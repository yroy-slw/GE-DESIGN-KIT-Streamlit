"""
Smoke test - verify every data-testid ge_design_kit's CSS depends on
still exists in the installed Streamlit version's bundled frontend.

Why this exists: ge_design_kit styles Streamlit's NATIVE widgets by
targeting [data-testid="..."] selectors. It's the least-bad option
available (see README "Pièges à connaître", data-testid identifies
Streamlit's own widget type, and there's no other stable hook for
native-widget structure/state, only for the leaf checkmark/thumb which
come from React Aria). But it's still an internal Streamlit convention,
not a public API Streamlit can rename these between versions with no
changelog entry, and the breakage is SILENT: nothing throws, the CSS
rule just stops matching. This happened for real during development —
"stLogo" became "stSidebarLogo"/"stHeaderLogo" at some point, and the
topbar quietly started rendering underneath a stray re-injected logo
until someone noticed by eye.

This test doesn't render a real page (no browser dependency), it
greps Streamlit's own bundled frontend JS for each testid string the
kit's CSS actually selects on, extracted straight from ge_design_kit's
source so this test can't silently drift from what the CSS really
depends on. If Streamlit ever drops or renames one, this fails loudly
at `pip install -r requirements.txt` / CI time instead of the kit
losing styling with no error anywhere.
"""

import re
from pathlib import Path

import pytest

KIT_DIR = Path(__file__).parent.parent / "ge_design_kit"
_TESTID_PATTERN = re.compile(r'data-testid="([a-zA-Z0-9_-]+)"')

# Testids Streamlit builds by string interpolation
# (`data-testid={\`prefix${suffix}\`}`) rather than as one literal
# string in its source — grepping the bundle for the FULL name would
# always fail even though the prefix (the actually-stable part) is
# genuinely present. Verified live against Streamlit 1.62's DOM before
# adding each entry (ErrorElement.*.js:
# `data-testid":`stAlertContent${i}`` for the 4 below) — don't add one
# without the same live check, and re-verify after a Streamlit bump.
_DYNAMIC_TESTID_PREFIXES = {
    "stAlertContentInfo": "stAlertContent",
    "stAlertContentSuccess": "stAlertContent",
    "stAlertContentWarning": "stAlertContent",
    "stAlertContentError": "stAlertContent",
}


def _extract_testids_from_kit() -> set[str]:
    testids: set[str] = set()
    for py_file in KIT_DIR.glob("*.py"):
        testids.update(_TESTID_PATTERN.findall(py_file.read_text(encoding="utf-8")))
    return testids


def _streamlit_static_js_dir() -> Path:
    import streamlit

    return Path(streamlit.__file__).parent / "static" / "static" / "js"


def test_ge_design_kit_imports_cleanly():
    """Baseline: the package itself must import without raising."""
    import ge_design_kit  # noqa: F401


@pytest.fixture(scope="module")
def bundled_js_text() -> str:
    """
    Concatenate every bundled frontend JS file once per test run —
    grepping ~100 files once per testid separately would be needlessly
    slow and the file list doesn't change mid-run.
    """
    js_dir = _streamlit_static_js_dir()
    assert js_dir.is_dir(), (
        f"Streamlit static JS directory not found: {js_dir} — "
        "is streamlit actually installed in this environment?"
    )
    chunks = [
        js_file.read_text(encoding="utf-8", errors="ignore")
        for js_file in js_dir.glob("*.js")
    ]
    assert chunks, f"No .js files found under {js_dir} — Streamlit install looks broken."
    return "\n".join(chunks)


@pytest.mark.parametrize("testid", sorted(_extract_testids_from_kit()))
def test_testid_still_exists_in_streamlit_bundle(testid: str, bundled_js_text: str):
    """
    ge_design_kit's CSS targets [data-testid="{testid}"] somewhere in
    the codebase — fails if the installed Streamlit version no longer
    ships that literal (or its stable dynamic prefix, cf.
    _DYNAMIC_TESTID_PREFIXES) anywhere in its frontend bundle.
    """
    needle = _DYNAMIC_TESTID_PREFIXES.get(testid, testid)
    assert needle in bundled_js_text, (
        f'data-testid="{testid}" not found anywhere in the installed Streamlit '
        f"frontend bundle (searched for {needle!r}). ge_design_kit's CSS "
        f"relies on this string — either this Streamlit version "
        f"renamed/removed it, or the wrong Streamlit version is installed. "
        f"grep ge_design_kit/*.py for \"{testid}\" to find every rule that "
        f"needs re-verifying against the browser inspector."
    )
