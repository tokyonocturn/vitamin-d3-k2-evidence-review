# Contributing

This repository is a source-linked evidence review. Corrections and additions are
welcome, but the bar is evidence, not opinion.

## Reporting a correction

Open an issue with:

1. the exact claim or row (file, ID, quoted text);
2. the source that contradicts it (DOI, PMID, or stable URL);
3. the proposed replacement text or value;
4. whether the error affects the report, a generated table, or both.

Do not edit generated files in `docs/generated/` or `docs/references.md` by hand.
They are rebuilt from the CSVs.

## Adding or changing data

### Products

Add a row to `data/products.csv` and follow the schema in
`data/data-dictionary.md`.

Requirements:

- a real `price_source_url` that resolves to the page used;
- an ISO `price_date`;
- one-time retail price in USD, excluding tax, shipping, subscription, and coupons;
- `price_channel` that accurately describes the source, including whether the price
  was promotional;
- certification only when a public listing or the certifier's documentation
  supports it; otherwise `None documented`;
- a note explaining any unusual serving size, format, or pack.

Do not add affiliate links, referral codes, or prices from marketplaces with no
lot traceability unless the product is only sold there, and say so in `notes`.

### Evidence

Add a row to `data/evidence.csv` with:

- one question and one outcome per row;
- the design and sample size;
- the pooled effect in the units used by the source, plus the confidence interval
  where reported;
- a certainty grade and a status that follow the scheme in the data dictionary;
- at least one existing reference ID.

Do not average across syntheses yourself. If two syntheses disagree, add separate
rows and explain the discrepancy in `notes`, as the fracture and K2 bone rows do.

### Claims

Add a row to `data/claims.csv` only if the claim is publicly circulating and can be
adjudicated against cited evidence. Use `Partially supported` when a kernel of truth
is overstated, not as a diplomatic default.

### References

Add a row to `data/references.csv` with a DOI or stable URL. Prefer the publisher
record over a news article. Do not cite a secondary summary for a numerical claim
when the primary record is available.

## Validation

```bash
python analysis/build_tables.py           # validate + regenerate
python analysis/build_tables.py --check   # fail if outputs are stale
```

The build fails on:

- missing columns or invalid categorical values;
- duplicate IDs or IDs that do not match the expected pattern;
- dangling evidence/claim to reference links;
- implausible active-ingredient amounts or price arithmetic;
- broken relative Markdown links;
- generated tables that do not match the data.

CI runs `--check` on every push and pull request.

## Style

- British or American spelling is acceptable, but be consistent within a file.
- Report effect sizes with units and confidence intervals.
- Separate statistical significance from practical importance.
- Say "not supported" rather than "proven false" unless the evidence is decisive.
- No brand promotion. Mentioning a product is not an endorsement.
- Keep the medical disclaimer intact.
- Do not describe a surrogate endpoint (BMD, coronary calcium, dp-ucMGP) as if it
  were a clinical outcome.

## Commits

Use a short imperative subject and a body explaining the evidence change:

```
data: correct Nature Made K2 pack size to 30 softgels

The brand page lists a 30-count bottle, not 60. Re-ran the generator;
no other rows change.
```
