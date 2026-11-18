# Data dictionary

All datasets are UTF-8 CSV with a single header row. They are the source of truth
for the report; the Markdown tables under `docs/generated/` are rendered from them
by `analysis/build_tables.py`.

## `products.csv`

| Column | Type | Meaning |
| --- | --- | --- |
| `id` | slug | Stable identifier used in prose and tables. |
| `brand` | text | Brand name as sold. |
| `product` | text | Product name, dose, and pack size. |
| `category` | enum | `d3`, `k2_mk7`, `k2_mk4`, `k_complex`, `combo`. |
| `format` | enum | `softgel`, `capsule`, `tablet`, `gummy`, `liquid`, `powder`. |
| `d3_iu` | number | Vitamin D3 IU per label serving. |
| `k2_mk7_mcg` | number | MK-7 micrograms per label serving. |
| `k2_mk4_mcg` | number | MK-4 micrograms per label serving. |
| `k1_mcg` | number | Vitamin K1 micrograms per label serving. |
| `servings` | integer | Label servings per container. For gummies, this is servings (pairs), not pieces. |
| `price_usd` | number | One-time retail price in US dollars, excluding tax and shipping. |
| `price_channel` | text | `Brand store (list price)`, `Brand store (sale price)`, or `Third-party price check`. |
| `price_date` | ISO date | Date the price was observed. |
| `price_source_url` | https URL | Page used for the price. |
| `certification` | enum | `USP Verified`, `NSF Certified for Sport`, `NSF/ANSI 173`, `None documented`. |
| `vegan` | yes/no | Whether the product is labelled vegan. |
| `notes` | text | Provenance and caveats. |

### Derived fields (not stored in the CSV)

`analysis/build_tables.py` computes:

- `servings_per_day` = max(2000 / IU D3 per serving, 100 / mcg MK-7 per serving),
  except for `k2_mk4`, where it is 1.0
- `cost_per_serving` = price / servings
- `cost_per_day` = cost per serving x servings per day
- `cost_per_30d` = cost per day x 30
- `cost_per_year` = cost per day x 365
- `cost_per_1000iu` = price x 1000 / (IU D3 per serving x servings)
- `cost_per_100mcg_mk7` = price x 100 / (mcg MK-7 per serving x servings)

The reference regimen is **2000 IU D3 and 100 mcg MK-7 daily**. Whichever nutrient
is furthest from that level determines the number of servings. MK-4 inside a
combination product is not counted, and standalone MK-4 is compared at its label
serving, because retail MK-4 doses are not commensurate with the 45 mg/day used in
Japanese trials.

## `evidence.csv`

| Column | Meaning |
| --- | --- |
| `id` | Stable identifier matching `E00`. |
| `domain` | One of `physiology`, `deficiency_testing`, `bone`, `calcium_regulation`, `cardiovascular`, `immune`, `cancer`, `metabolic`, `dosing`, `safety`, `interactions`, `combinations`, `product_quality`. |
| `question` | The practical question being answered. |
| `outcome` | The measured outcome. |
| `population` | Who was studied. |
| `evidence_type` | Design and size of the evidence base. |
| `studies_participants` | Number of studies and participants where reported. |
| `pooled_effect` | The pooled estimate, in the units used by the source. |
| `effect_measure` | Hazard ratio, odds ratio, relative risk, mean difference, prevalence, or qualitative. |
| `ci` | Confidence interval, where reported. |
| `certainty` | GRADE-style certainty: `High`, `Moderate`, `Low`, `Very low`, `Not graded`. |
| `status` | `Established`, `Emerging`, `Mixed`, `Unsupported`. |
| `source_ids` | Semicolon-separated reference IDs from `references.csv`. |
| `notes` | Caveats. |

## `claims.csv`

| Column | Meaning |
| --- | --- |
| `id` | Stable identifier matching `C00`. |
| `claim` | The claim as commonly stated. |
| `category` | Marketing, safety, bone, cardiovascular, immune, cancer, metabolic, dosing, testing, formulation, interactions, combinations, product_quality, nutrition, or general. |
| `verdict` | `Supported`, `Partially supported`, `Unsupported`, `False`. |
| `explanation` | What the evidence actually shows. |
| `source_ids` | Semicolon-separated reference IDs. |

## `references.csv`

| Column | Meaning |
| --- | --- |
| `id` | `R01`-style identifier used in every other dataset. |
| `authors` | Author list or organisation as transcribed; blank when not transcribed. |
| `year` | Publication year. |
| `title` | Article or programme title. |
| `journal` | Journal, publisher, or programme. |
| `identifier` | DOI, PMID/PMC, volume/page, or report number where available. |
| `url` | Stable https link to the record. |
| `type` | Evidence type. |

## Certainty scheme

Certainty is a judgement, not a statistical output. It combines risk of bias,
inconsistency, indirectness, imprecision, and publication bias, following the
logic of GRADE:

- **High**: further research is unlikely to change confidence in the estimate.
- **Moderate**: further research may change the estimate and could change the conclusion.
- **Low**: further research is likely to change the estimate.
- **Very low**: the estimate is very uncertain.

`Status` is separate and describes the state of the claim, not its certainty: a
small effect can be `Established` with `Moderate` certainty, while a plausible
mechanism with only pilot data is `Emerging` with `Very low` certainty.

## Units

- Vitamin D: 1 mcg = 40 IU. 2000 IU = 50 mcg.
- 25(OH)D: ng/mL x 2.496 = nmol/L. 30 ng/mL = 75 nmol/L; 20 ng/mL = 50 nmol/L.
- Vitamin K: micrograms (mcg) for K1 and MK-7; micrograms or milligrams for MK-4,
  as labelled. 1 mg = 1000 mcg.
