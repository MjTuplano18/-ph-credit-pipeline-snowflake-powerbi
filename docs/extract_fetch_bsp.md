<!--
FILE: extract_fetch_bsp.md
PURPOSE: Explain the BSP extractor script behavior and usage
PHASE: 2
DEPENDS ON: extract/fetch_bsp.py and optional BSP_API_URL
OUTPUTS: Guidance for running the extractor and validating output
-->

# BSP Extractor

## Why We Pull BSP Data

Collections risk rises when macro conditions tighten. BSP policy rates affect loan pricing (especially variable-rate borrowers), while inflation pressures borrower cash flow. In a real collections team at SP Madrid, these signals help decide which segments to prioritize when the economy is stressed.

## What We Are Building

We are creating a small macro dataset that can be joined to loans by time period. This dataset is intentionally small but reliable, so we can enrich the lending data without blocking the pipeline when the BSP API is down.

## Recommended Indicators

Start with these two because they are core to default risk and easy to explain:

- **Policy rate** (BSP overnight rate or policy rate) to represent credit tightening.
- **Inflation rate** (CPI) to represent cost-of-living pressure.

Optional later additions:

- **Lending rates** (bank lending rate or lending rate for commercial loans).
- **Unemployment rate** if available in the BSP portal (macro stress proxy).

## If BSP Has No Public API

If BSP does not expose an API for these series, we can use a reliable public macro API as a proxy and document the choice. A common option is the World Bank API, which provides PH inflation data with no API key required.

Example (World Bank inflation, Philippines):

```
https://api.worldbank.org/v2/country/PH/indicator/FP.CPI.TOTL.ZG?format=json
```

This returns annual inflation rates. The extractor normalizes this into `rate_period` and `inflation_rate` and sets `policy_rate` to `None` when policy rate is not provided.

## How To Find the BSP API Endpoint

1. Go to the BSP Open Data portal.
2. Search for the indicator name (for example, "policy rate" or "inflation rate").
3. Open the dataset and look for the "API" or "Download" section.
4. Copy the JSON API URL and confirm it returns data as either:
   - a list of records, or
   - a dict with a `data` array.

If the endpoint requires an API key, store it in `.env` and we can add headers in the script later.

## How To Configure the Script

Add the endpoint to your local `.env` (never commit this file):

```
BSP_API_URL=https://<your-bsp-endpoint>
```

The template placeholder is in [.env.example](.env.example) so you remember the variable name.

## How To Run

```
& .\.venv\Scripts\python.exe .\extract\fetch_bsp.py
```

## What Good Output Looks Like

- A DataFrame with `ingested_at` filled in.
- `bsp_fallback_reason` is `None` when live data is used.
- Columns contain time and indicator values (names depend on the BSP dataset).

## Code Walkthrough (What Each Part Does)

### API Request

```
response = requests.get(api_url, timeout=timeout)
response.raise_for_status()
```

This calls the BSP endpoint and throws an error if the response is not successful, which triggers fallback behavior.

### Payload Shape Handling

```
if isinstance(payload, dict) and "data" in payload:
    records = payload["data"]
elif isinstance(payload, list):
    records = payload
```

This supports the two most common API response shapes: a list of records or a dict with a `data` list.

### Fallback Data

```
df = pd.DataFrame([
    {"rate_period": "2023-Q4", "policy_rate": 6.5, "inflation_rate": 4.0},
    {"rate_period": "2024-Q1", "policy_rate": 6.5, "inflation_rate": 3.7},
])
```

This ensures the script still returns a valid DataFrame even if the API fails, so downstream steps never block.
