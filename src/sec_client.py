"""Small SEC EDGAR helper.

The offline project does not require this module to run. It is included to show
how the project can be extended with SEC company facts.

Important: SEC requests should include a descriptive User-Agent with your email.
"""

from __future__ import annotations

import requests

AMAZON_CIK = "0001018724"
SEC_COMPANYFACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"


def fetch_companyfacts(cik: str = AMAZON_CIK, user_agent: str | None = None) -> dict:
    """Fetch SEC companyfacts JSON for a company CIK.

    Parameters
    ----------
    cik:
        Ten-digit CIK string. Amazon is 0001018724.
    user_agent:
        Descriptive identifier required by SEC fair-access guidance, e.g.
        "Your Name your.email@example.com".
    """
    if not user_agent:
        raise ValueError("Please provide a SEC-compliant User-Agent with your name and email.")

    url = SEC_COMPANYFACTS_URL.format(cik=cik.zfill(10))
    response = requests.get(url, headers={"User-Agent": user_agent}, timeout=30)
    response.raise_for_status()
    return response.json()
