#!/usr/bin/env python3
"""Validate the vitamin D3/K2 review datasets and regenerate derived tables.

The CSV files in ``data/`` are the source of truth. This script checks schema,
arithmetic, enum values and cross-references, computes cost-per-dose metrics, and
renders the Markdown tables used by the documentation.

Usage
-----
    python analysis/build_tables.py           # validate and regenerate
    python analysis/build_tables.py --check   # validate; fail if outputs stale

Only the Python standard library is required (Python 3.10+).
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import sys
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
GEN = ROOT / "docs" / "generated"

CATEGORIES = {"d3", "k2_mk7", "k2_mk4", "k_complex", "combo"}
FORMATS = {"softgel", "capsule", "tablet", "gummy", "liquid", "powder"}
CERTIFICATIONS = {
    "USP Verified",
    "NSF Certified for Sport",
    "NSF/ANSI 173",
    "None documented",
}
DOMAINS = {
    "physiology",
    "deficiency_testing",
    "bone",
    "calcium_regulation",
    "cardiovascular",
    "immune",
    "cancer",
    "metabolic",
    "dosing",
    "safety",
    "interactions",
    "combinations",
    "product_quality",
}
CERTAINTY = {"High", "Moderate", "Low", "Very low", "Not graded"}
EVIDENCE_STATUS = {"Established", "Emerging", "Mixed", "Unsupported"}
VERDICTS = {"Supported", "Partially supported", "Unsupported", "False"}

# Reference daily regimen used to compare cost across product categories.
REF_D3_IU = 2000
REF_MK7_MCG = 100
REF_MK4_MCG = 1000  # a maintenance-scale MK-4 dose; the Japanese drug dose is 45 mg

PRODUCT_COLUMNS = [
    "id",
    "brand",
    "product",
    "category",
    "format",
    "d3_iu",
    "k2_mk7_mcg",
    "k2_mk4_mcg",
    "k1_mcg",
    "servings",
    "price_usd",
    "price_channel",
    "price_date",
    "price_source_url",
    "certification",
    "vegan",
    "notes",
]
EVIDENCE_COLUMNS = [
    "id",
    "domain",
    "question",
    "outcome",
    "population",
    "evidence_type",
    "studies_participants",
    "pooled_effect",
    "effect_measure",
    "ci",
    "certainty",
    "status",
    "source_ids",
    "notes",
]
CLAIM_COLUMNS = ["id", "claim", "category", "verdict", "explanation", "source_ids"]
REFERENCE_COLUMNS = ["id", "authors", "year", "title", "journal", "identifier", "url", "type"]

URL_RE = re.compile(r"^https://\S+$")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{2,70}$")
ROW_ID_RE = re.compile(r"^[EC]\d{2}$")
REF_ID_RE = re.compile(r"^R\d{2}$")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def read_csv(path: Path, columns: list[str], report: Report) -> list[dict[str, str]]:
    if not path.exists():
        report.error(f"{path.relative_to(ROOT)}: file is missing")
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        header = reader.fieldnames or []
        missing = [c for c in columns if c not in header]
        if missing:
            report.error(f"{path.name}: missing columns {missing}")
            return []
        rows = []
        for line, row in enumerate(reader, start=2):
            cleaned = {(k or "").strip(): (v or "").strip() for k, v in row.items()}
            if not cleaned.get("id"):
                report.error(f"{path.name}:{line}: blank id")
                continue
            cleaned["_line"] = str(line)
            rows.append(cleaned)
    if not rows:
        report.error(f"{path.name}: no data rows")
    return rows


def as_float(row: dict[str, str], field: str, report: Report) -> float:
    raw = row.get(field, "")
    try:
        return float(raw)
    except (TypeError, ValueError):
        report.error(f"{row.get('id', '?')}: {field} must be numeric, got {raw!r}")
        return float("nan")


def load_references(report: Report) -> tuple[list[dict[str, str]], set[str]]:
    rows = read_csv(DATA / "references.csv", REFERENCE_COLUMNS, report)
    seen: set[str] = set()
    for row in rows:
        rid = row["id"]
        if not REF_ID_RE.match(rid):
            report.error(f"{rid}: reference id must match R00")
        if rid in seen:
            report.error(f"{rid}: duplicate reference id")
        seen.add(rid)
        if not URL_RE.match(row["url"]):
            report.error(f"{rid}: url must be an https URL")
        if not row["title"] or not row["journal"]:
            report.error(f"{rid}: title and journal are required")
        if not row["year"].isdigit() or not (1900 <= int(row["year"]) <= 2100):
            report.error(f"{rid}: year must be a four-digit year")
    return rows, seen


def load_products(report: Report) -> list[dict[str, object]]:
    rows = read_csv(DATA / "products.csv", PRODUCT_COLUMNS, report)
    seen: set[str] = set()
    products: list[dict[str, object]] = []
    today = dt.date.today()

    for row in rows:
        pid = row["id"]
        if not ID_RE.match(pid):
            report.error(f"{pid}: id must be lowercase slug text")
        if pid in seen:
            report.error(f"{pid}: duplicate product id")
        seen.add(pid)

        if row["category"] not in CATEGORIES:
            report.error(f"{pid}: category {row['category']!r} is not allowed")
        if row["format"] not in FORMATS:
            report.error(f"{pid}: format {row['format']!r} is not allowed")
        if row["certification"] not in CERTIFICATIONS:
            report.error(f"{pid}: certification {row['certification']!r} is not allowed")
        if row["vegan"] not in {"yes", "no"}:
            report.error(f"{pid}: vegan must be yes or no")
        if not URL_RE.match(row["price_source_url"]):
            report.error(f"{pid}: price_source_url must be an https URL")
        try:
            price_date = dt.date.fromisoformat(row["price_date"])
            if price_date > today:
                report.error(f"{pid}: price_date is in the future")
        except ValueError:
            report.error(f"{pid}: price_date must be ISO YYYY-MM-DD")
            price_date = today

        d3 = as_float(row, "d3_iu", report)
        mk7 = as_float(row, "k2_mk7_mcg", report)
        mk4 = as_float(row, "k2_mk4_mcg", report)
        k1 = as_float(row, "k1_mcg", report)
        servings = as_float(row, "servings", report)
        price = as_float(row, "price_usd", report)

        if servings <= 0:
            report.error(f"{pid}: servings must be positive")
        if price <= 1:
            report.error(f"{pid}: price_usd must be greater than 1")
        if d3 < 0 or mk7 < 0 or mk4 < 0 or k1 < 0:
            report.error(f"{pid}: active amounts cannot be negative")
        if not (0 <= d3 <= 50_000):
            report.error(f"{pid}: d3_iu outside plausible range")
        if not (0 <= mk7 <= 2_000):
            report.error(f"{pid}: k2_mk7_mcg outside plausible range")
        if not (0 <= mk4 <= 50_000):
            report.error(f"{pid}: k2_mk4_mcg outside plausible range")

        if row["category"] == "d3" and not (d3 > 0 and mk7 == 0 and mk4 == 0):
            report.error(f"{pid}: d3 products must contain D3 only")
        if row["category"] == "k2_mk7" and not (mk7 > 0 and d3 == 0 and mk4 == 0):
            report.error(f"{pid}: k2_mk7 products must contain MK-7 only")
        if row["category"] == "k2_mk4" and not (mk4 > 0 and d3 == 0 and mk7 == 0):
            report.error(f"{pid}: k2_mk4 products must contain MK-4 only")
        if row["category"] == "combo" and not (d3 > 0 and (mk7 > 0 or mk4 > 0)):
            report.error(f"{pid}: combo products need D3 and a K2 form")
        if row["category"] == "k_complex" and not (mk7 > 0 and mk4 > 0):
            report.error(f"{pid}: k_complex products need MK-7 and MK-4")

        if servings != servings or servings <= 0 or price != price or price <= 0:
            continue

        # Servings required per day to reach the reference regimen. Whichever
        # nutrient is furthest from its reference level governs the dose.
        # MK-4 inside a combination product is ignored for this purpose.
        needs = []
        if d3 > 0:
            needs.append(REF_D3_IU / d3)
        if mk7 > 0:
            needs.append(REF_MK7_MCG / mk7)
        # MK-4 doses are not comparable by mass: retail products supply 45-15 000
        # mcg while Japanese trials used 45 000 mcg. For a standalone MK-4 product
        # the label serving is the only meaningful unit, so one serving is used.
        if row["category"] == "k2_mk4":
            needs = [1.0]
        servings_per_day = max(needs) if needs else 1.0

        cost_per_serving = price / servings
        cost_per_day = cost_per_serving * servings_per_day

        products.append(
            {
                **row,
                "d3": d3,
                "mk7": mk7,
                "mk4": mk4,
                "k1": k1,
                "servings_value": servings,
                "price": price,
                "price_date_value": price_date,
                "cost_per_serving": cost_per_serving,
                "servings_per_day": servings_per_day,
                "cost_per_day": cost_per_day,
                "cost_per_30d": cost_per_day * 30,
                "cost_per_year": cost_per_day * 365,
                "cost_per_1000iu": (
                    price / (d3 * servings) * 1000 if d3 > 0 else None
                ),
                "cost_per_100mcg_mk7": (
                    price / (mk7 * servings) * 100 if mk7 > 0 else None
                ),
            }
        )

    products.sort(key=lambda p: float(p["cost_per_day"]))
    for rank, product in enumerate(products, start=1):
        product["rank"] = rank
    return products


def load_evidence(report: Report, ref_ids: set[str]) -> list[dict[str, str]]:
    rows = read_csv(DATA / "evidence.csv", EVIDENCE_COLUMNS, report)
    seen: set[str] = set()
    for row in rows:
        eid = row["id"]
        if not ROW_ID_RE.match(eid):
            report.error(f"{eid}: evidence id must match E00")
        if eid in seen:
            report.error(f"{eid}: duplicate evidence id")
        seen.add(eid)
        if row["domain"] not in DOMAINS:
            report.error(f"{eid}: unknown domain {row['domain']!r}")
        if row["certainty"] not in CERTAINTY:
            report.error(f"{eid}: unknown certainty {row['certainty']!r}")
        if row["status"] not in EVIDENCE_STATUS:
            report.error(f"{eid}: unknown status {row['status']!r}")
        ids = [s for s in row["source_ids"].split(";") if s]
        if not ids:
            report.error(f"{eid}: at least one source id is required")
        for ref in ids:
            if ref not in ref_ids:
                report.error(f"{eid}: source id {ref} is not in references.csv")
    return rows


def load_claims(report: Report, ref_ids: set[str]) -> list[dict[str, str]]:
    rows = read_csv(DATA / "claims.csv", CLAIM_COLUMNS, report)
    seen: set[str] = set()
    for row in rows:
        cid = row["id"]
        if not ROW_ID_RE.match(cid):
            report.error(f"{cid}: claim id must match C00")
        if cid in seen:
            report.error(f"{cid}: duplicate claim id")
        seen.add(cid)
        if row["verdict"] not in VERDICTS:
            report.error(f"{cid}: unknown verdict {row['verdict']!r}")
        ids = [s for s in row["source_ids"].split(";") if s]
        if not ids:
            report.error(f"{cid}: at least one source id is required")
        for ref in ids:
            if ref not in ref_ids:
                report.error(f"{cid}: source id {ref} is not in references.csv")
    return rows


def money(value: object) -> str:
    return f"${float(value):.2f}"


def actives(p: dict[str, object]) -> str:
    parts = []
    if float(p["d3"]) > 0:
        parts.append(f"{float(p['d3']):,.0f} IU D3")
    if float(p["mk7"]) > 0:
        parts.append(f"{float(p['mk7']):,.0f} mcg MK-7")
    if float(p["mk4"]) > 0:
        parts.append(f"{float(p['mk4']):,.0f} mcg MK-4")
    if float(p["k1"]) > 0:
        parts.append(f"{float(p['k1']):,.0f} mcg K1")
    return " + ".join(parts)


def render_products(products: list[dict[str, object]]) -> str:
    lines = [
        "<!-- Generated by analysis/build_tables.py. Do not edit by hand. -->",
        "",
        "# Brand and product comparison tables",
        "",
        "Prices are US one-time retail snapshots from the source named in",
        "`data/products.csv`. They exclude tax and shipping and will change. The",
        "reference regimen is **2000 IU vitamin D3 and 100 mcg MK-7 per day**;",
        "whichever nutrient is furthest from that level sets how many servings a day",
        "are needed. Standalone MK-4 products are compared at their label serving,",
        "because retail MK-4 doses range from 45 mcg to 15 mg while clinical trials",
        "used 45 mg/day; MK-4 inside a combination is not counted.",
        "",
        f"Products: **{len(products)}**. Snapshot dates: "
        f"{min(p['price_date_value'] for p in products)} to "
        f"{max(p['price_date_value'] for p in products)}.",
        "",
        "## All products ranked by cost per day at the reference regimen",
        "",
        "| Rank | Brand | Product | Type | Actives per serving | Servings | Price | $/serving | $/30 days | $/year | Certification |",
        "| ---: | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for p in products:
        lines.append(
            "| {rank} | {brand} | {product} | {cat} | {act} | {srv} | {price} | {cps} | {c30} | {cy} | {cert} |".format(
                rank=p["rank"],
                brand=p["brand"],
                product=p["product"],
                cat=str(p["category"]).replace("_", " "),
                act=actives(p),
                srv=int(float(p["servings_value"])),
                price=money(p["price"]),
                cps=money(p["cost_per_serving"]),
                c30=money(p["cost_per_30d"]),
                cy=money(p["cost_per_year"]),
                cert=p["certification"],
            )
        )

    d3_only = [p for p in products if p["category"] == "d3"]
    mk7_only = [p for p in products if p["category"] == "k2_mk7"]
    combos = [p for p in products if p["category"] == "combo"]
    kcomplex = [p for p in products if p["category"] == "k_complex"]
    certified = [p for p in products if p["certification"] != "None documented"]

    lines += ["", "## Unit costs within each nutrient", ""]
    lines += [
        "| Brand | Product | Cost per 1000 IU D3 | Cost per 100 mcg MK-7 |",
        "| --- | --- | ---: | ---: |",
    ]
    for p in products:
        if p["cost_per_1000iu"] is None and p["cost_per_100mcg_mk7"] is None:
            continue
        d3_cost = (
            money(p["cost_per_1000iu"]) if p["cost_per_1000iu"] is not None else "-"
        )
        k2_cost = (
            money(p["cost_per_100mcg_mk7"])
            if p["cost_per_100mcg_mk7"] is not None
            else "-"
        )
        lines.append(f"| {p['brand']} | {p['product']} | {d3_cost} | {k2_cost} |")

    lines += ["", "## Value summary", ""]
    lines += [
        "| Metric | Product | $/30 days | $/year |",
        "| --- | --- | ---: | ---: |",
    ]
    cheapest = products[0]
    lines.append(
        f"| Cheapest overall | {cheapest['brand']} {cheapest['product']} | {money(cheapest['cost_per_30d'])} | {money(cheapest['cost_per_year'])} |"
    )
    for label, group in (
        ("Cheapest D3 only", d3_only),
        ("Cheapest MK-7 only", mk7_only),
        ("Cheapest combination", combos),
    ):
        if group:
            best = min(group, key=lambda p: float(p["cost_per_day"]))
            lines.append(
                f"| {label} | {best['brand']} {best['product']} | {money(best['cost_per_30d'])} | {money(best['cost_per_year'])} |"
            )
    certified_d3 = [p for p in certified if p["category"] == "d3"]
    if certified_d3:
        best = min(certified_d3, key=lambda p: float(p["cost_per_day"]))
        lines.append(
            f"| Cheapest certified D3 | {best['brand']} {best['product']} | {money(best['cost_per_30d'])} | {money(best['cost_per_year'])} |"
        )
    certified_k = [p for p in certified if p["category"] in {"k2_mk7", "k_complex"}]
    if certified_k:
        best = min(certified_k, key=lambda p: float(p["cost_per_day"]))
        lines.append(
            f"| Cheapest certified K2 | {best['brand']} {best['product']} | {money(best['cost_per_30d'])} | {money(best['cost_per_year'])} |"
        )
    priciest = products[-1]
    lines.append(
        f"| Most expensive overall | {priciest['brand']} {priciest['product']} | {money(priciest['cost_per_30d'])} | {money(priciest['cost_per_year'])} |"
    )

    lines += ["", "Median cost per 30 days by product type:", ""]
    lines += [
        "| Type | Products | Median $/30 days | Range |",
        "| --- | ---: | ---: | --- |",
    ]
    for label, group in (
        ("D3 only", d3_only),
        ("MK-7 only", mk7_only),
        ("Combination D3 + K2", combos),
        ("Mixed K complex", kcomplex),
    ):
        if group:
            costs = [float(p["cost_per_30d"]) for p in group]
            lines.append(
                f"| {label} | {len(group)} | {money(median(costs))} | {money(min(costs))} - {money(max(costs))} |"
            )

    if d3_only and combos:
        ratio = median([float(p["cost_per_30d"]) for p in combos]) / median(
            [float(p["cost_per_30d"]) for p in d3_only]
        )
        lines += [
            "",
            f"Median combination cost is **{ratio:.1f}x** the median D3-only cost for the "
            "reference regimen. That premium buys a nutrient whose added benefit over D3 "
            "alone is not established for any hard outcome.",
        ]

    lines += [
        "",
        "## Certification status",
        "",
        "Certification verifies identity, potency and contaminant limits. It says nothing",
        "about whether the product works. `None documented` means no public listing was",
        "found for that SKU; some of those brands describe testing that is not independently",
        "verifiable.",
        "",
        "| Brand | Product | Certification | $/30 days |",
        "| --- | --- | --- | ---: |",
    ]
    for p in products:
        if p["certification"] == "None documented":
            continue
        lines.append(
            f"| {p['brand']} | {p['product']} | {p['certification']} | {money(p['cost_per_30d'])} |"
        )

    uncertified = len(products) - len(certified)
    lines += [
        "",
        "## Data quality flags",
        "",
        f"- {uncertified} of {len(products)} products have no public third-party certification listed.",
        f"- {len([p for p in products if p['format'] == 'gummy'])} product is a gummy, the format most prone to potency deviation in independent testing.",
        f"- {len([p for p in products if p['category'] == 'k2_mk4'])} products use MK-4, which needs far larger milligram doses than MK-7.",
        "- Prices are dated snapshots, not live quotes. Re-check the source URL before buying.",
        "- Several brand-store prices were promotional at the time of collection and are labelled as such.",
        "",
    ]
    return "\n".join(lines)


def render_evidence(evidence: list[dict[str, str]]) -> str:
    titles = {
        "physiology": "Forms, absorption and bioavailability",
        "deficiency_testing": "Deficiency, thresholds and blood testing",
        "bone": "Bone health and fracture prevention",
        "calcium_regulation": "Calcium regulation and vascular calcification",
        "cardiovascular": "Cardiovascular outcomes",
        "immune": "Immune function and infection",
        "cancer": "Cancer incidence and mortality",
        "metabolic": "Glycaemic outcomes",
        "dosing": "Dosing strategy",
        "safety": "Safety, toxicity and kidney stones",
        "interactions": "Medication interactions",
        "combinations": "D3 plus K2 combinations",
        "product_quality": "Product quality and labelling",
    }
    lines = [
        "<!-- Generated by analysis/build_tables.py. Do not edit by hand. -->",
        "",
        "# Evidence tables",
        "",
        "Certainty reflects the strength and consistency of the underlying evidence",
        "(GRADE-style judgement), not the size of the effect. `Status` separates",
        "established findings from emerging, mixed and unsupported ones.",
        "",
    ]
    for domain in titles:
        subset = [e for e in evidence if e["domain"] == domain]
        if not subset:
            continue
        lines += [
            f"## {titles[domain]}",
            "",
            "| Question | Outcome | Evidence base | Pooled result | Certainty | Status | Sources |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
        for e in subset:
            effect = e["pooled_effect"]
            if e["ci"]:
                effect = f"{effect} ({e['ci']})"
            base = e["evidence_type"]
            detail = e["studies_participants"]
            if detail and detail.lower() not in base.lower():
                base = f"{base}; {detail}"
            lines.append(
                f"| {e['question']} | {e['outcome']} | {base} | {effect} | {e['certainty']} | {e['status']} | {', '.join(e['source_ids'].split(';'))} |"
            )
        lines.append("")
    return "\n".join(lines)


def render_claims(claims: list[dict[str, str]]) -> str:
    lines = [
        "<!-- Generated by analysis/build_tables.py. Do not edit by hand. -->",
        "",
        "# Claim adjudication table",
        "",
        "Every claim below was checked against the cited evidence. `Partially supported`",
        "means a kernel of truth exists but the claim as commonly stated overstates it.",
        "",
        "| # | Claim | Verdict | What the evidence shows | Sources |",
        "| ---: | --- | --- | --- | --- |",
    ]
    for i, c in enumerate(claims, start=1):
        lines.append(
            f"| {i} | {c['claim']} | **{c['verdict']}** | {c['explanation']} | {', '.join(c['source_ids'].split(';'))} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_references(refs: list[dict[str, str]]) -> str:
    lines = [
        "<!-- Generated by analysis/build_tables.py. Do not edit by hand. -->",
        "",
        "# References",
        "",
        "Identifiers resolve to the publisher record. Where an author list was not",
        "transcribed, the title is given first and the DOI or stable URL identifies the",
        "record. Accessed November 2026.",
        "",
    ]
    for ref in sorted(refs, key=lambda r: r["id"]):
        authors = ref["authors"].strip()
        prefix = f"{authors} " if authors else ""
        identifier = ref["identifier"].strip()
        ident = f" {identifier}." if identifier else ""
        lines.append(
            f"- **[{ref['id']}]** {prefix}({ref['year']}). *{ref['title']}*. {ref['journal']}.{ident} <{ref['url']}>"
        )
    lines.append("")
    return "\n".join(lines)


def check_doc_links(report: Report) -> None:
    candidates = [ROOT / "README.md", ROOT / "CONTRIBUTING.md", ROOT / "CHANGELOG.md"]
    candidates += sorted((ROOT / "docs").rglob("*.md"))
    candidates += sorted((ROOT / "report").rglob("*.md"))
    for path in candidates:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative = target.split("#", 1)[0]
            if not relative:
                continue
            if not (path.parent / relative).exists():
                report.error(f"{path.relative_to(ROOT)}: broken relative link {target!r}")


def write_outputs(outputs: dict[Path, str]) -> None:
    GEN.mkdir(parents=True, exist_ok=True)
    for path, text in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated files are stale")
    args = parser.parse_args()

    report = Report()
    refs, ref_ids = load_references(report)
    products = load_products(report)
    evidence = load_evidence(report, ref_ids)
    claims = load_claims(report, ref_ids)
    check_doc_links(report)

    outputs = {
        GEN / "brand-comparison.md": render_products(products),
        GEN / "evidence-tables.md": render_evidence(evidence),
        GEN / "claims-table.md": render_claims(claims),
        ROOT / "docs" / "references.md": render_references(refs),
    }

    if args.check:
        for path, text in outputs.items():
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                report.error(
                    f"{path.relative_to(ROOT)}: generated output is stale; run python analysis/build_tables.py"
                )
    else:
        write_outputs(outputs)

    print("Vitamin D3/K2 evidence repository validation")
    print(f"  products:   {len(products)}")
    print(f"  evidence:   {len(evidence)} rows")
    print(f"  claims:     {len(claims)} rows")
    print(f"  references: {len(refs)} entries")
    print(f"  warnings:   {len(report.warnings)}")
    print(f"  errors:     {len(report.errors)}")
    for warning in report.warnings:
        print(f"  WARN  {warning}")
    for error in report.errors:
        print(f"  ERROR {error}", file=sys.stderr)
    if report.errors:
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
