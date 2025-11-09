from __future__ import annotations
import time
from typing import Callable, Optional, List, Dict
from urllib.parse import urljoin, urlparse, parse_qsl, urlencode, urlunparse
import pandas as pd
import requests
import requests_cache
from bs4 import BeautifulSoup

# Base listing page that contains a paginated table of hockey teams and stats.
BASE_URL = "https://www.scrapethissite.com/pages/forms/"

def make_session(cache_name: str = "scrapethissite_cache", expire_after: int = 24 * 3600) -> requests.Session:
    """
    Create an HTTP session with transparent caching.
    """
    sess = requests_cache.CachedSession(
        cache_name=cache_name,
        backend="sqlite",
        expire_after=expire_after,
        allowable_methods=("GET",),
    )
    return sess


def _ensure_query_param(url: str, key: str, value: str | int) -> str:
    """
    Ensure that a given query parameter exists on the URL, setting or overriding it.
    """
    u = urlparse(url)
    q = dict(parse_qsl(u.query))
    q[key] = str(value)
    return urlunparse(u._replace(query=urlencode(q, doseq=True)))


def _detect_target_table(soup: BeautifulSoup):
    """
    Find the target table on the page.
    """
    for tbl in soup.select("table"):
        # Try thead headers first; fall back to first row headers
        ths = [th.get_text(" ", strip=True).lower() for th in tbl.select("thead th")] or \
              [th.get_text(" ", strip=True).lower() for th in (tbl.find("tr") or []).select("th")]
        if any("team" in h for h in ths) and any("year" in h for h in ths):
            return tbl
    return None


def _parse_table(table) -> List[Dict[str, str]]:
    """
    Convert an HTML table element into a list of row dicts.
    """
    # Extract headers
    header_cells = table.select("thead th")
    if not header_cells:
        first_tr = table.find("tr")
        header_cells = first_tr.find_all("th") if first_tr else []
    headers = [h.get_text(" ", strip=True) for h in header_cells]

    # Extract rows
    rows = []
    for tr in table.select("tbody tr") or table.find_all("tr")[1:]:
        tds = tr.find_all("td")
        if not tds:
            continue
        cells = [td.get_text(" ", strip=True) for td in tds]

        # Zip with headers (pad/trim to match header length)
        if len(cells) < len(headers):
            cells += [""] * (len(headers) - len(cells))
        cells = cells[:len(headers)]
        rows.append(dict(zip(headers, cells)))
    return rows


def _coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names and coerce types for numeric analysis.
    """
    # Map original headers to stable column names
    rename_map = {
        "Team Name": "team",
        "Year": "year",
        "Wins": "wins",
        "Losses": "losses",
        "OT Losses": "ot_losses",
        "Win %": "win_pct",
        "Goals For (GF)": "goals_for",
        "Goals Against (GA)": "goals_against",
        "+ / -": "plus_minus",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # Convert integer-like fields to nullable integers
    for c in ["year", "wins", "losses", "ot_losses", "goals_for", "goals_against", "plus_minus"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")

    # Convert 'win_pct' from strings to numeric 55.3
    if "win_pct" in df.columns:
        df["win_pct"] = pd.to_numeric(
            df["win_pct"].astype(str).str.replace("%", "", regex=False),
            errors="coerce"
        )

    # Clean team names
    if "team" in df.columns:
        df["team"] = df["team"].astype(str).str.strip()

    # Reorder columns to canonical order, append any extras at the end
    order = ["team", "year", "wins", "losses", "ot_losses", "win_pct", "goals_for", "goals_against", "plus_minus"]
    cols = [c for c in order if c in df.columns] + [c for c in df.columns if c not in order]
    return df[cols].reset_index(drop=True)


def _find_next_url(soup: BeautifulSoup, current_url: str, per_page: int) -> Optional[str]:
    """
    Identify the URL for the next page in pagination and preserve per_page.
    """
    # Look for a pagination link with label "»", "Next", or "›"
    next_href = None
    for a in soup.select("ul.pagination a"):
        label = (a.get_text(strip=True) or "")
        if label in {"»", "Next", "›"}:
            next_href = a.get("href")
            break
    if not next_href:
        return None

    # Build absolute URL from possibly relative href
    next_url = urljoin(BASE_URL, next_href)

    # Keep per_page consistent
    if "per_page=" not in next_url:
        next_url = _ensure_query_param(next_url, "per_page", per_page)
    return next_url


def scrape_all_pages(
    per_page: int = 100,
    max_pages: Optional[int] = None,
    delay_sec: float = 0.1,
    session: Optional[requests.Session] = None,
    progress_cb: Optional[Callable[[int, Optional[int]], None]] = None, 
) -> pd.DataFrame:
    """
    Scrape the paginated hockey teams table into a single pandas DataFrame.
    """
    sess = session or make_session()
    url = _ensure_query_param(BASE_URL, "per_page", per_page)

    pages_done = 0
    all_rows: List[Dict[str, str]] = []

    while url:
        # Fetch page
        resp = sess.get(url, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Detect and parse the main table
        table = _detect_target_table(soup)
        if table:
            all_rows.extend(_parse_table(table))

        # Progress bookkeeping
        pages_done += 1
        if progress_cb:
            progress_cb(pages_done, max_pages)

        # Stop if reached page cap
        if max_pages and pages_done >= max_pages:
            break

        # Move to next page; if none, exit loop
        url = _find_next_url(soup, url, per_page)

        # Be polite to the server
        if delay_sec:
            time.sleep(delay_sec)

    if not all_rows:
        return pd.DataFrame()

    df = pd.DataFrame.from_records(all_rows)
    return _coerce_types(df)