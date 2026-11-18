# Changelog

All notable changes to the datasets, generated tables, and report are recorded here.
The format follows Keep a Changelog; versions use semantic versioning.

## [1.0.0] - 2026-11-18

### Added

- Comprehensive scientific report covering physiology, forms, absorption,
  bioavailability, bone health, calcium regulation, immune function,
  cardiovascular claims, cancer, mortality, glycaemic outcomes, blood testing,
  thresholds, dosing, toxicity, kidney stones, medication interactions, D3+K2
  combinations, special populations, product quality, and cost.
- `data/products.csv`: 20 products priced 2026-11-18, normalised to cost per
  30 days at a reference regimen of 2000 IU D3 and 100 mcg MK-7.
- `data/evidence.csv`: 49 graded evidence rows across thirteen domains.
- `data/claims.csv`: 34 claims adjudicated as supported, partially supported,
  unsupported, or false.
- `data/references.csv`: 65 references with DOI, PMID, or stable URL.
- `analysis/build_tables.py`: schema validation, cost model, generated Markdown,
  relative-link checking, and a `--check` mode for CI.
- GitHub Actions workflow that validates the datasets on every push.
- Practical safety guide, dosing guide, formulation and absorption review, and
  brand comparison.

### Notes

- Prices are US one-time retail snapshots and exclude tax and shipping. Several
  brand-store prices were promotional and are labelled as such.
- No new laboratory testing was commissioned; potency and contamination
  conclusions rely on published independent testing and peer-reviewed analytical
  studies.
- The review is AI-assisted and has not been peer reviewed. See
  `docs/methodology.md`.

## Correction policy

Substantive corrections are recorded here with the date, the affected row or claim,
and the source that justified the change. Generated tables are never edited by hand;
they are rebuilt from the CSVs and verified in CI.
