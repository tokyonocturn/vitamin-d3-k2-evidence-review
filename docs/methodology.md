# Methodology

## 1. Questions and scope

This review asks six practical questions:

1. What do vitamin D3 and vitamin K2 do physiologically, and which forms are
   absorbed and used differently?
2. What benefits are established by controlled human evidence for bone health,
   calcium regulation, immune function, cardiovascular outcomes, cancer, and
   mortality?
3. Does combining D3 with K2 produce benefits beyond D3 alone?
4. How should 25(OH)D be interpreted, what thresholds and intakes apply, and
   where does toxicity begin?
5. Which medications and conditions make supplementation unsafe?
6. Across real products, which forms, brands, and certifications offer the best
   quality and value per effective dose?

The unit of analysis is **oral vitamin D and vitamin K supplementation in
humans**, with a primary focus on cholecalciferol and menaquinone-7 because those
are the forms used in most trials and sold in most products.

## 2. Evidence sources

Searches were run in November 2026 across PubMed/PMC, journal publisher sites
(NEJM, BMJ, JAMA, Lancet Diabetes & Endocrinology, JCEM, Osteoporosis
International, Circulation, JACC, Journal of Thrombosis and Haemostasis,
Nutrients, American Journal of Clinical Nutrition), guideline bodies (Endocrine
Society, USPSTF, IOM/NASEM, NIH Office of Dietary Supplements), and the reference
lists of recent systematic reviews.

Additional sources:

- Certifier documentation (USP, NSF, Informed Sport).
- Independent laboratory testing and market surveys (ConsumerLab, peer-reviewed
  analytical chemistry studies).
- Brand storefronts and one independent price tracker for price snapshots.

Search terms combined `vitamin D`, `cholecalciferol`, `25-hydroxyvitamin D`,
`vitamin D2`, `ergocalciferol`, `calcifediol`, `vitamin K`, `menaquinone`,
`MK-4`, `MK-7`, `phylloquinone`, `osteocalcin`, `matrix Gla protein`,
`fracture`, `bone mineral density`, `falls`, `respiratory infection`,
`autoimmune`, `cancer`, `cardiovascular`, `calcification`, `mortality`,
`deficiency`, `toxicity`, `hypercalcemia`, `nephrolithiasis`, `warfarin`,
`acenocoumarol`, `DOAC`, `bioavailability`, `half-life`, `all-trans`,
`certification`, `contamination`, and `cost`.

## 3. Inclusion and exclusion

**Included**

- Randomised controlled trials in humans.
- Systematic reviews and meta-analyses of RCTs, including individual-participant
  data analyses.
- Clinical practice guidelines and government evidence reviews for thresholds,
  intakes, and upper limits.
- Pharmacokinetic studies for absorption and half-life.
- Independent laboratory testing and peer-reviewed product surveys for quality.
- Certifier programme documentation for what a seal verifies.

**Excluded from efficacy conclusions**

- Animal-only studies (used only to explain mechanism).
- Uncontrolled case reports, conference abstracts without data, and vendor blogs.
- Observational studies used as proof of causation (retained only to describe
  hypotheses or prevalence).
- Multi-ingredient products when the question is about a single nutrient.

No language other than English was searched. There was no publication-date
cut-off; foundational physiology is retained, while efficacy and safety claims
prioritise 2015–2026 syntheses.

## 4. Evidence grading

Each row in [`data/evidence.csv`](../data/evidence.csv) has two independent axes.

**Certainty** (GRADE-style):

| Level | Meaning |
| --- | --- |
| High | Further research is unlikely to change confidence in the estimate. |
| Moderate | Further research may change the estimate or the conclusion. |
| Low | Further research is likely to change the estimate. |
| Very low | The estimate is very uncertain. |

**Status**:

| Status | Meaning |
| --- | --- |
| Established | Multiple consistent RCTs or a meta-analysis, plausible mechanism, no serious unresolved contradiction. |
| Emerging | Human data exist but samples are small, results inconsistent, or certainty is very low. |
| Mixed | Direction depends on outcome, population, dose, or dosing schedule. |
| Unsupported | Claim is marketed or repeated but controlled human evidence does not support it. |

Certainty and importance are separate. A pooled 0.3% BMD difference can be
statistically robust and clinically irrelevant.

### Handling contradictions

Where syntheses disagreed, both estimates are reported and the disagreement is
explained rather than averaged. Examples:

- **Fracture prevention.** VITAL and D-Health found no benefit from vitamin D
  alone, while Cochrane found a hip-fracture benefit for calcium plus vitamin D.
  The difference is population: institutionalised and deficient versus replete
  community-dwelling adults. Both are reported.
- **Vitamin K2 and bone.** Knapen 2013 found less bone loss with 180 mcg MK-7,
  while Rønn 2020 found no BMD difference with 375 mcg MK-7 on a background of
  vitamin D and calcium. The second trial is larger and better controlled; both
  are reported with the discrepancy stated.
- **Respiratory infection.** The 2017 individual-participant meta-analysis found
  OR 0.88, while the 2025 aggregate analysis found OR 0.94 (p=0.057) with
  publication bias. The later, larger analysis is given more weight, and the
  earlier estimate is retained to show the direction of travel.
- **Kidney stones.** Vitamin D alone shows no increased risk in trials, while
  calcium plus vitamin D in WHI showed an increase. The signal is attributed to
  calcium loading and reported as such.

## 5. Product sampling and pricing

### Sampling

Twenty products were selected purposively to cover:

- vitamin D3 at budget, mid, and premium prices;
- multiple pack sizes of the same product, to expose the pack-size effect;
- MK-7 at 100 mcg and 180 mcg, including branded MenaQ7;
- MK-4 at a retail dose and a high-dose liquid;
- single-nutrient and combined products;
- gummy and liquid formats as comparators;
- products with USP Verified, NSF Certified for Sport, NSF/ANSI 173, and no
  documented certification.

This is **not** a random or exhaustive market sample. It is large enough to show
the shape of the market and the cost spread, not to rank every brand.

### Price rules

- US one-time retail price in USD, excluding tax and shipping.
- Brand storefront preferred; one independent price tracker used where a brand
  page did not expose a price.
- Subscription, auto-ship, and coupon prices excluded. Where the brand store was
  itself running a sale, the price is used and labelled `Brand store (sale price)`.
- Each row records `price_date`, `price_channel`, and `price_source_url`.
- All prices were collected on 2026-11-18.

### Cost model

Cost is normalised to a **reference regimen of 2000 IU vitamin D3 and 100 mcg
MK-7 per day**. Whichever nutrient is furthest from that level determines how many
servings are needed, so a 5000 IU product is dosed at 0.4 servings per day.

Standalone MK-4 products are compared at their label serving. Retail MK-4 doses
range from 45 mcg to 15 mg, while clinical trials used 45 mg/day; normalising by
mass would either make a $75 bottle look trivial or a 45 mcg capsule look
worthless. Using the label serving is the least misleading option, and MK-4 inside
a combination product is not counted toward the reference regimen.

Derived fields:

```
servings per day      = max(2000 / IU D3 per serving, 100 / mcg MK-7 per serving)
cost per serving      = price / servings per container
cost per day          = cost per serving x servings per day
cost per 30 days      = cost per day x 30
cost per year         = cost per day x 365
cost per 1000 IU D3   = price x 1000 / (IU per serving x servings)
cost per 100 mcg MK-7 = price x 100 / (mcg per serving x servings)
```

## 6. Verification performed

- **Arithmetic.** Serving counts, price per serving, cost per day, and annual cost
  are recomputed by script; implausible values fail the build.
- **Cross-references.** Every evidence and claim row must point to an existing
  reference ID; the validator fails on dangling citations.
- **Effect sizes.** Each pooled estimate was checked against the abstract, table,
  or results section of the cited record.
- **Certification claims.** Checked against the certifier's public listing or
  programme documentation where available, and recorded as "None documented"
  rather than assumed absent when no listing was found.
- **Contamination and potency claims.** Triangulated across a peer-reviewed
  analytical study, an independent commercial testing programme, and a
  peer-reviewed market survey; where they disagree, the disagreement is stated.
- **Generated output.** CI reruns the generator and fails if the committed tables
  differ from the data.

## 7. Limitations

1. **Single-reviewer, AI-assisted.** No duplicate independent screening or
   extraction. This is the largest methodological limitation.
2. **Paywalls.** Some independent testing detail (ConsumerLab) is member-only;
   only public summaries are cited, which limits product-level specificity.
3. **Publication and funding bias.** Many supplement trials are small and some are
   industry-funded. The respiratory infection literature shows measurable funnel
   plot asymmetry.
4. **Heterogeneity.** Populations, doses, forms, and outcome definitions differ.
   Pooled estimates average across dissimilar studies.
5. **Price volatility.** Prices, pack sizes, and certifications change. The
   dataset is a dated snapshot, not a live price feed.
6. **Certification is not efficacy.** A seal says something about identity and
   contaminants, not about whether the product prevents fractures.
7. **Product sample is purposive.** It illustrates value tiers; it does not
   establish market-wide failure rates.
8. **No new laboratory testing.** Contamination and potency conclusions rely on
   published assays, which may not reflect the current lot of any product.
9. **Generalisation.** Trial populations are mostly older, white adults in North
   America, Europe, and Australasia; dosing in other groups is extrapolated.

## 8. Conflicts of interest and funding

None. No brand paid for inclusion, no affiliate links are used, and no product was
supplied by a manufacturer. The author has no financial interest in any supplement
brand.

## 9. AI-assistance disclosure and corrections

This review was assembled with AI assistance under human direction. Numeric claims
were checked against cited sources, and the datasets are machine-validated. It has
not been peer reviewed. If you find an error, open an issue with the exact claim,
the source, and the correction; substantive corrections will be recorded in
[`CHANGELOG.md`](../CHANGELOG.md).
