"""commit-provenance - live demo (Streamlit Community Cloud).

Reads the committed readiness report under reports/*.jsonl and shows the v0.1
data-report slice: which required artifacts are present, which are missing, the
readiness score, and the repository surfaces counted. No network, no secrets -
runs entirely off the committed report.

Deploy: Streamlit Community Cloud -> New app -> repo AthenaTheOwl/commit-provenance,
branch main, main file streamlit_app.py.
"""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

REPO = Path(__file__).resolve().parent
REPORTS = REPO / "reports"


def load_report() -> tuple[dict | None, str]:
    files = sorted(REPORTS.glob("*.jsonl"))
    if not files:
        return None, ""
    latest = files[-1]
    lines = [line for line in latest.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        return None, latest.stem
    return json.loads(lines[-1]), latest.stem


st.set_page_config(page_title="commit-provenance - repo readiness", layout="wide")
st.title("commit-provenance")
st.caption(
    "v0.1 data-report slice: which readiness artifacts are present in the repo, "
    "which are still missing, and the surfaces counted. reads the committed "
    "reports/*.jsonl directly."
)

report, stem = load_report()
if report is None:
    st.warning("no report found under reports/*.jsonl")
    st.stop()

repo = report.get("repository", {})
artifacts: dict[str, bool] = report.get("artifacts", {})
score = report.get("score", {})
counts = report.get("counts", {})

present = score.get("required_artifacts_present", sum(1 for v in artifacts.values() if v))
total = score.get("required_artifacts_total", len(artifacts) or 1)
missing_sections = report.get("missing_status_sections", [])
pct = (present / total * 100) if total else 0.0

st.subheader(
    f"{repo.get('name', '?')} @ {repo.get('head', '?')} "
    f"(branch {repo.get('branch', '?')}) - report {stem}"
)

c1, c2, c3 = st.columns(3)
c1.metric("required artifacts present", f"{present}/{total}")
c2.metric("readiness", f"{pct:.0f}%")
c3.metric(
    "status sections missing",
    len(missing_sections),
    help="STATUS.md sections required by the report (Current state / Known limits / Next feature queue)",
)

only_missing = st.checkbox("show only missing artifacts", value=False)

rows = [
    {"artifact": name, "status": "present" if ok else "MISSING"}
    for name, ok in artifacts.items()
    if (not only_missing) or (not ok)
]
# ranked: missing first, then present, each alphabetical.
rows.sort(key=lambda r: (r["status"] == "present", r["artifact"]))

st.dataframe(rows, use_container_width=True, hide_index=True)

st.markdown("**repository surfaces**")
s1, s2, s3, s4 = st.columns(4)
s1.metric("docs", counts.get("docs", 0))
s2.metric("spec files", counts.get("spec_files", 0))
s3.metric("tests", counts.get("tests", 0))
s4.metric("jsonl reports", counts.get("jsonl_reports", 0))

missing = sorted(name for name, ok in artifacts.items() if not ok)
if missing:
    st.info(
        f"**biggest gap:** {len(missing)} required artifact(s) absent - "
        f"first to fix: `{missing[0]}`. readiness {pct:.0f}%."
    )
else:
    st.info(
        f"**biggest gap:** none - all {total} required artifacts present, readiness {pct:.0f}%. "
        "the next surface is the signed emit/verify flow specified under specs/0001."
    )

st.caption(
    "v0.1 reports artifact readiness; the signing + hook flow is specified but not built. "
    "the report model + scoring live in `commit_provenance/`; this page reads the committed "
    "`reports/*.jsonl`. repo: github.com/AthenaTheOwl/commit-provenance"
)

# ----------------------------------------------------------------------------
# interactive: score your OWN repo against the real readiness engine.
# this drives the actual validator in commit_provenance.scoring - the same
# functions the `git-provenance report` command uses. nothing is hardcoded:
# the artifact checklist and your pasted STATUS.md are fed to
# parse_status_sections / missing_status_sections / score_report live.
# ----------------------------------------------------------------------------
from commit_provenance.scoring import (  # noqa: E402
    REQUIRED_ARTIFACTS,
    REQUIRED_STATUS_SECTIONS,
    missing_status_sections,
    parse_status_sections,
    score_report,
)

st.divider()
st.header("check your own repo against the readiness engine")
st.caption(
    "this is not a lookup. you describe a repo - which required artifacts exist, and your "
    "STATUS.md text - and the page runs the real validator "
    "(`commit_provenance.scoring.parse_status_sections`, `missing_status_sections`, "
    "`score_report`) on it live. flip a checkbox or edit the status and the score recomputes."
)

# pre-fill the checklist from the committed report so the example starts honest.
prefill = report.get("artifacts", {})

left, right = st.columns([3, 4])

with left:
    st.markdown("**which required artifacts does your repo have?**")
    st.caption("pre-filled from the committed report; uncheck any to see readiness drop.")
    user_presence: dict[str, bool] = {}
    for name in REQUIRED_ARTIFACTS:
        default = bool(prefill.get(name, True))
        user_presence[name] = st.checkbox(name, value=default, key=f"art::{name}")

with right:
    st.markdown("**paste your STATUS.md** (the engine looks for `## ` section headers)")
    default_status = (
        "## Current state\n- v0.1 ships a runnable report command.\n\n"
        "## Known limits\n- no signed records yet.\n\n"
        "## Next feature queue\n- add Ed25519 signing.\n"
    )
    status_text = st.text_area(
        "STATUS.md",
        value=default_status,
        height=240,
        label_visibility="collapsed",
    )

# DRIVE THE REAL ENGINE -------------------------------------------------------
parsed_sections = parse_status_sections(status_text)
missing_secs = missing_status_sections(parsed_sections)
live_score = score_report(user_presence, missing_secs)

present_n = live_score["required_artifacts_present"]
total_n = live_score["required_artifacts_total"]
live_pct = (present_n / total_n * 100) if total_n else 0.0

m1, m2, m3 = st.columns(3)
m1.metric("required artifacts present", f"{present_n}/{total_n}")
m2.metric("readiness", f"{live_pct:.0f}%")
m3.metric("status sections missing", live_score["missing_status_sections"])

# WHY: pass/fail with reasons, straight from the engine output.
gate_pass = present_n == total_n and live_score["missing_status_sections"] == 0
if gate_pass:
    st.success(
        f"PASS - all {total_n} required artifacts present and all "
        f"{len(REQUIRED_STATUS_SECTIONS)} STATUS.md sections found. readiness {live_pct:.0f}%."
    )
else:
    reasons = []
    absent = sorted(name for name, ok in user_presence.items() if not ok)
    if absent:
        reasons.append(
            f"{len(absent)} required artifact(s) absent (first: `{absent[0]}`)"
        )
    if missing_secs:
        reasons.append("missing STATUS.md section(s): " + ", ".join(missing_secs))
    st.error("FAIL - " + "; ".join(reasons) + f". readiness {live_pct:.0f}%.")

with st.expander("what the engine parsed from your STATUS.md"):
    st.write(
        {
            "sections found": list(parsed_sections.keys()),
            "required sections": list(REQUIRED_STATUS_SECTIONS),
            "missing sections": missing_secs,
        }
    )
    st.json(
        {
            section: parsed_sections.get(section, [])
            for section in REQUIRED_STATUS_SECTIONS
        }
    )

st.caption(
    "engine: `commit_provenance.scoring` (the same checks `git-provenance report` runs). "
    "no values are hardcoded here - your checklist and status text are scored live."
)
