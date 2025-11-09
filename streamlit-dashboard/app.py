from __future__ import annotations
import io
from typing import Optional
import pandas as pd
import streamlit as st
from scraper import make_session, scrape_all_pages
import charts as charts_mod


st.set_page_config(
    page_title="Scraper Dashboard – Hockey Teams (Forms)",
    layout="wide",
)


def _init_state():
    """Ensure the Streamlit session state holds a placeholder for scraped data."""
    if "data" not in st.session_state:
        st.session_state["data"] = None


def _metrics(df: pd.DataFrame):
    """Render headline metrics summarizing the scraped dataset."""
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Total rows", f"{len(df):,}")
    with col_b:
        st.metric("Distinct teams", f"{df['team'].nunique():,}" if "team" in df.columns else "—")
    with col_c:
        years = df["year"].dropna().astype(int) if "year" in df.columns else pd.Series(dtype=int)
        label = f"{years.min()}–{years.max()}" if not years.empty else "—"
        st.metric("Year range", label)


def main():
    """Drive the Streamlit dashboard flow from scraping trigger to visualization."""
    _init_state()

    st.title("Scraper Dashboard: Hockey Teams (Forms)")
    st.write(
        "This dashboard scrapes the hockey teams dataset from "
        "[Scrape This Site – Hockey Teams: Forms](https://www.scrapethissite.com/pages/forms/) "
        "by following pagination links (»), then visualizes the results."
    )

    
    # Define sidebar controls
    with st.sidebar:
        st.header("Controls")

        pages_to_scrape = st.slider(
            "Pages to scrape",
            min_value=1,
            max_value=25,
            value=6,
            help="Follows the next (») link until this many pages are scraped."
        )

        delay_sec = st.slider(
            "Delay between requests (s)",
            min_value=0.00,
            max_value=0.50,
            value=0.10,
            step=0.05,
            help="Be polite to the site. 0.10–0.20s is reasonable."
        )

        start = st.button("Start scraping", type="primary")

    # Scrape on demand
    if start:
        sess = make_session()
        st.subheader("Scraping status")
        status = st.status("Starting…", expanded=True)
        progress = st.progress(0.0)

        # Update the progress widgets as each page finishes scraping
        def cb(done: int, total: Optional[int]):
            total = total or pages_to_scrape
            progress.progress(min(done / total, 1.0))
            status.update(label=f"Scraping page {done}/{total}…")

        try:
            df = scrape_all_pages(
                max_pages=pages_to_scrape,
                delay_sec=delay_sec,
                session=sess,
                progress_cb=cb,
            )
            if df is None or df.empty:
                status.update(state="error", label="No data scraped. Try increasing pages or per page.")
            else:
                status.update(state="complete", label=f"Done. Scraped {len(df):,} rows.")
                st.session_state["data"] = df
        except Exception as e:
            status.update(state="error", label=f"Scraping failed: {e}")

    # Manage data and charts
    df: Optional[pd.DataFrame] = st.session_state.get("data")
    if df is not None and not df.empty:
        st.subheader("Raw data")

        _metrics(df)

        # Filters
        years = (
            sorted(df["year"].dropna().astype(int).unique().tolist(), reverse=True)
            if "year" in df.columns else []
        )
        filter_cols = st.columns([2, 2, 3])
        with filter_cols[0]:
            year_filter = st.multiselect(
                "Filter by year(s)",
                options=years,
                default=years if years else [],
            )
        with filter_cols[1]:
            team_query = st.text_input("Filter by team name (contains)", value="")
        with filter_cols[2]:
            show_cols = st.multiselect(
                "Columns to display",
                options=df.columns.tolist(),
                default=[c for c in ["team", "year", "wins", "losses", "ot_losses", "win_pct", "goals_for", "goals_against", "plus_minus"] if c in df.columns],
            )

        filtered = df.copy()
        # Apply client-side filters based on sidebar selections.
        if year_filter and "year" in filtered.columns:
            filtered = filtered[filtered["year"].isin(year_filter)]
        if team_query and "team" in filtered.columns:
            filtered = filtered[filtered["team"].str.contains(team_query, case=False, na=False)]
        if show_cols:
            filtered = filtered[show_cols]

        st.dataframe(filtered, use_container_width=True, hide_index=True)

        # Download CSV
        csv_buf = io.StringIO()
        filtered.to_csv(csv_buf, index=False)
        st.download_button(
            label="Download CSV",
            data=csv_buf.getvalue(),
            file_name="hockey_teams_scraped.csv",
            mime="text/csv",
        )

        # Charts
        st.subheader("Charts")
        c1, c2 = st.columns(2)
        with c1:
            st.altair_chart(charts_mod.teams_per_year(df), use_container_width=True)
        with c2:
            st.altair_chart(charts_mod.avg_wins_per_year(df), use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            st.altair_chart(charts_mod.top_teams_by_win_pct(df, top_n=10), use_container_width=True)
        with c4:
            st.altair_chart(charts_mod.goals_scatter(df), use_container_width=True)

        st.altair_chart(charts_mod.win_pct_hist(df), use_container_width=True)

    else:
        st.info("No data yet. Choose the number of pages to scrape, then click Start scraping.")


if __name__ == "__main__":
    main()