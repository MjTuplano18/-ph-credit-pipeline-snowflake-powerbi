# FILE: fetch_bsp.py
# PURPOSE: Fetch BSP macroeconomic indicators with a safe fallback
# PHASE: 2
# DEPENDS ON: Optional BSP_API_URL env var
# OUTPUTS: Prints a DataFrame preview and dtypes
import os

import pandas as pd
import requests
from dotenv import load_dotenv


def _normalize_payload(payload: object) -> pd.DataFrame:
    if isinstance(payload, dict) and "data" in payload:
        return pd.DataFrame(payload["data"])

    if isinstance(payload, list):
        # World Bank format: [metadata, data]
        if len(payload) >= 2 and isinstance(payload[1], list):
            records = payload[1]
            df = pd.DataFrame(records)
            if {"date", "value"}.issubset(df.columns):
                df = df.rename(columns={"date": "rate_period", "value": "inflation_rate"})
                df["policy_rate"] = None
                return df[["rate_period", "policy_rate", "inflation_rate"]]

        return pd.DataFrame(payload)

    raise ValueError("Unexpected BSP API payload shape")


def fetch_bsp_rates(api_url: str, timeout: int = 10) -> pd.DataFrame:
    """Fetch BSP indicators from API, fallback to static data on failure."""
    try:
        if not api_url:
            raise ValueError("BSP_API_URL is not set")

        response = requests.get(api_url, timeout=timeout)  # External API call may fail or be slow
        response.raise_for_status()
        payload = response.json()

        df = _normalize_payload(payload)
        df["bsp_fallback_reason"] = None
    except Exception as exc:
        df = pd.DataFrame(
            [
                {"rate_period": "2023-Q4", "policy_rate": 6.5, "inflation_rate": 4.0},
                {"rate_period": "2024-Q1", "policy_rate": 6.5, "inflation_rate": 3.7},
            ]
        )
        df["bsp_fallback_reason"] = str(exc)  # Keep the reason for transparency

    df["ingested_at"] = pd.Timestamp.now("UTC")  # Timestamp for auditability
    return df


def main() -> None:
    load_dotenv()  # Load local environment variables from .env when present
    api_url = os.getenv("BSP_API_URL", "")  # Keep empty by default to force explicit config
    df = fetch_bsp_rates(api_url)

    print("BSP rates preview:")
    print(df.head())
    print("\nDtypes:")
    print(df.dtypes)


if __name__ == "__main__":
    main()
