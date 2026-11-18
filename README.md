# Vitamin D3 and Vitamin K2: An Independent Evidence Review and Product Database

A source-linked review of cholecalciferol and menaquinone supplements — what they
do, what they do not do, how to dose them, who should avoid them, and what 20 real
products cost per effective daily dose. Every quantitative claim traces to a
reference, and every table is generated from the CSV datasets in [`data/`](data/).

**No brand funding, affiliate links, or sponsorship.** Prices were collected in
November 2026 and will change.

---

## Bottom line

**Vitamin D3 is a real nutrient with a narrow, well-defined clinical job. Vitamin
K2 is a plausible mechanism in search of an outcome.** The evidence that K2 adds
anything to D3 — the entire premise of the fastest-growing segment of the
supplement market — does not hold up.

| Question | Answer | Confidence |
| --- | --- | --- |
| Does D3 prevent fractures in healthy adults? | **No.** VITAL found HR 0.98 for total fractures and 1.01 for hip fractures in 25,871 adults over 5.3 years, with no effect modification by baseline 25(OH)D [R06]. | High |
| Does D3 prevent fractures in anyone? | **Yes, narrowly.** Calcium plus vitamin D reduced hip fracture (RR 0.84) in older, largely institutionalised populations [R19]. D3 alone did not. | Moderate |
| Does D3 prevent cancer or heart disease? | **No.** Cancer incidence HR 0.96 and major cardiovascular events HR 0.97 in VITAL [R05]. | High |
| Does D3 reduce cancer death? | **Slightly.** Cancer mortality RR 0.87 across five trials and 1,591 cancer deaths, driven by daily dosing [R16]. | Moderate |
| Does D3 prevent colds? | **Weakly, if at all.** The 2017 individual-participant analysis found OR 0.88 [R13]; the larger 2025 aggregate analysis found OR 0.94 (p=0.057) with publication bias [R14]. | Moderate |
| Does D3 prevent autoimmune disease? | **Only while you take it.** HR 0.78 during the trial, HR 0.98 two years after it stopped [R07; R08]. | Moderate |
| Which form of D? | **D3.** It raises total 25(OH)D about 40% more than D2 at the same dose [R43]. | Moderate |
| How much D3? | **600–800 IU/day** meets requirements; **800–2000 IU/day** is a reasonable supplemental range; **4000 IU/day** is the tolerable upper limit [R01]. | High |
| Is D3 toxic? | **Rarely.** Toxicity is unusual below 25(OH)D of 150 ng/mL and follows sustained intakes above 10,000 IU/day [R40; R54]. | Moderate |
| Does K2 build bone? | **Unclear.** One 3-year MK-7 trial found less bone loss [R23]; a better-powered 3-year trial found no BMD difference at all [R24]. | Low |
| Does K2 clear arteries? | **Not demonstrated.** Coronary calcium improved slightly in pooled small trials [R36], but the largest dedicated trials were neutral [R30; R32]. | Low |
| Is D3 + K2 better than D3 alone? | **Not established.** No trial shows a hard-outcome benefit, and the one positive bone trial used an activated vitamin D analogue, not cholecalciferol [R28; R24; R25]. | Low |
| Is K2 safe with warfarin? | **No.** MK-7 at 45 mcg/day lowered INR by 20–37%, and 10 mcg was clinically relevant in some people [R37]. | Moderate |
| Best value D3? | **NOW 2000 IU, 240 softgels at $13.59** — **$0.03 per 1000 IU**, about **$21 per year** at 2000 IU/day. | Price snapshot |
| Best value K2? | **Horbaach MK-7 100 mcg, 250 softgels at $15.49** — **$1.86 per 30 days**. No public certification. | Price snapshot |
| What does the K2 premium buy? | Nothing proven. Median D3+K2 combination cost is **4.5×** the median D3-only cost for the same reference regimen. | Price snapshot |

The full argument, including where each claim comes from and where it breaks
down, is in the [scientific report](report/vitamin-d3-k2-scientific-report.md).

---

## The five findings that matter

1. **The fracture story is about deficiency, not about supplements.** Vitamin D
   prevents rickets and osteomalacia, and it helps people who are deficient or
   institutionalised. In replete community-dwelling adults, it does not prevent
   fractures, and the largest trial found no benefit even in participants with
   25(OH)D below 12 ng/mL [R06].

2. **Dose shape matters more than dose size.** Daily or weekly low-dose vitamin D
   is associated with fewer falls and fewer respiratory infections; bolus dosing
   is not, and an annual 500,000 IU dose increased falls and fractures [R17;
   R61]. "More vitamin D" is not a monotonic good.

3. **K2's human outcome evidence is thin and contradictory.** The mechanism is
   real — MK-7 carboxylates osteocalcin and matrix Gla protein [R18; R30]. The
   outcomes are not: bone density trials disagree, vascular calcification trials
   are mostly null, and no trial has been powered for fractures or cardiac events.

4. **The D3+K2 combination is a marketing construct.** The trials that tested it
   directly either found no added benefit over D3 plus calcium [R24; R25] or used
   a prescription vitamin D analogue that is not sold as a supplement [R28].

5. **Product quality varies, and certification is the only cheap hedge.** Two of
   26 vitamin D products in one independent review contained nearly twice their
   labelled dose [R46]; a 2013 analysis found 52–135% of expected potency across
   brands, while the USP-verified manufacturer measured 101.7% [R48].

---

## What is in this repository

| Path | Contents |
| --- | --- |
| [`report/vitamin-d3-k2-scientific-report.md`](report/vitamin-d3-k2-scientific-report.md) | Comprehensive report: physiology, forms, absorption, bone, calcium regulation, immune function, cardiovascular claims, cancer, testing, dosing, toxicity, interactions, combinations, populations, products, conclusions. |
| [`docs/methodology.md`](docs/methodology.md) | Search strategy, inclusion rules, grading scheme, cost model, verification, limitations, AI disclosure. |
| [`docs/safety-guide.md`](docs/safety-guide.md) | Practical safety guide: who should avoid supplementation, toxicity, hypercalcemia, kidney stones, medication interactions, red flags. |
| [`docs/dosing-guide.md`](docs/dosing-guide.md) | Dosing by goal and population, correction protocols, timing, missed doses, what to expect. |
| [`docs/forms-and-absorption.md`](docs/forms-and-absorption.md) | D3 vs D2 vs calcifediol; K1 vs MK-4 vs MK-7; oil, powder, lichen, natto; bioavailability evidence. |
| [`docs/brand-comparison.md`](docs/brand-comparison.md) | How to read the product data, value tiers, certification, and buying guidance. |
| [`docs/generated/brand-comparison.md`](docs/generated/brand-comparison.md) | Generated 20-product cost table, unit costs, certification table. |
| [`docs/generated/evidence-tables.md`](docs/generated/evidence-tables.md) | 49 graded evidence rows across thirteen domains. |
| [`docs/generated/claims-table.md`](docs/generated/claims-table.md) | 34 common claims adjudicated as supported, partial, unsupported, or false. |
| [`docs/references.md`](docs/references.md) | 65 references with DOI, PMID, or stable URL. |
| [`data/products.csv`](data/products.csv) | Product database (price, actives, servings, certification, notes). |
| [`data/evidence.csv`](data/evidence.csv) | Evidence table with effect sizes, certainty, and status. |
| [`data/claims.csv`](data/claims.csv) | Claim adjudication dataset. |
| [`data/references.csv`](data/references.csv) | Reference metadata. |
| [`data/data-dictionary.md`](data/data-dictionary.md) | Column definitions and grading scheme. |
| [`analysis/build_tables.py`](analysis/build_tables.py) | Validates the datasets, computes cost metrics, regenerates all tables. |

---

## Reproduce it

Requires Python 3.10+ and no third-party packages.

```bash
python analysis/build_tables.py           # validate + regenerate tables
python analysis/build_tables.py --check   # fail if data or tables are stale
```

The `--check` command runs in CI on every push
([`.github/workflows/validate.yml`](.github/workflows/validate.yml)). It verifies:

- required columns and allowed categorical values;
- unique IDs and resolvable cross-references between evidence, claims, and references;
- plausible active-ingredient amounts and price arithmetic;
- that the generated Markdown is byte-identical to what the data produces.

### Derived cost model

```
servings per day      = max(needed for 2000 IU D3, needed for 100 mcg MK-7)
cost per serving      = price / servings per container
cost per day          = cost per serving x servings per day
cost per 30 days      = cost per day x 30
cost per year         = cost per day x 365
cost per 1000 IU D3   = price x 1000 / (IU per serving x servings)
cost per 100 mcg MK-7 = price x 100 / (mcg per serving x servings)
```

Standalone MK-4 products are compared at their label serving, because retail MK-4
doses range from 45 mcg to 15 mg while clinical trials used 45 mg/day. MK-4 inside
a combination product is not counted toward the reference regimen. This avoids
pretending that a 45 mcg MK-4 capsule is comparable to a 180 mcg MK-7 capsule.

---

## How the evidence was handled

- **Established** findings have multiple consistent RCTs or a meta-analysis, with
  a plausible mechanism and no serious unresolved contradiction.
- **Emerging** findings have human data but small samples, inconsistency, or very
  low certainty.
- **Mixed** means the pooled direction is unclear or depends on outcome.
- **Unsupported** means the claim is marketed or repeated but is not supported by
  controlled human evidence.

Certainty is graded High / Moderate / Low / Very low using GRADE logic. The two
axes are deliberately separate: a real but tiny effect can be *established* and
still be clinically unimportant.

Full details, including how contradictions were resolved, are in
[`docs/methodology.md`](docs/methodology.md).

---

## What this review is not

- **Not medical advice.** Vitamin D and K are nutrients, not treatments. People
  with kidney disease, granulomatous disease, hyperparathyroidism, cancer,
  malabsorption, who take anticoagulants or other interacting drugs, who are
  pregnant or breastfeeding, or who are treating children should talk to a
  clinician.
- **Not a primary laboratory study.** Product-quality conclusions come from
  published independent testing (ConsumerLab, peer-reviewed market surveys) and
  certifier databases; this project did not commission new assays.
- **Not exhaustive.** Twenty products are a purposive sample across price tiers,
  forms, and certifications, not a census of the market.
- **Not free of uncertainty.** Supplement research is partly industry-funded,
  publication bias is measurable, and many trials are small. Effect estimates
  should be read as best current approximations.

### AI-assistance disclosure

This review was assembled with AI assistance under human direction. Every numeric
claim was checked against the cited abstract, table, or dataset; the datasets and
generated tables are machine-validated. It has **not** been peer reviewed. Treat
it as a well-documented starting point, not a substitute for the primary
literature or clinical judgement.

Corrections are welcome: open an issue with the claim, the source, and the
proposed change. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## Citation and license

Citation metadata is in [`CITATION.cff`](CITATION.cff).

- **Text and data:** CC BY 4.0 — share and adapt with attribution.
- **Code:** MIT.

See [`NOTICE`](NOTICE) for the full content-license and medical disclaimer.
