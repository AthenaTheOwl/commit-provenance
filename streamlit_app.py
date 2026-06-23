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
