import altair as alt
import pandas as pd


def _ensure_types(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with numeric columns coerced so charts receive clean types."""
    d = df.copy()
    int_cols = [c for c in ["year", "wins", "losses", "ot_losses", "goals_for", "goals_against", "plus_minus"] if c in d.columns]
    for c in int_cols:
        d[c] = pd.to_numeric(d[c], errors="coerce")
    if "win_pct" in d.columns:
        d["win_pct"] = pd.to_numeric(d["win_pct"], errors="coerce")
    return d


def teams_per_year(df: pd.DataFrame):
    """Build a bar chart counting how many team entries appear in each year."""
    d = _ensure_types(df)
    agg = d.groupby("year", as_index=False).size()

    # Display data in chronological order
    year_domain = list(range(1990, 2012))

    chart = (
        alt.Chart(agg)
        .mark_bar()
        .encode(
            x=alt.X(
                "year:O",
                title="Year",
                sort=year_domain,                     
                scale=alt.Scale(domain=year_domain), 
            ),
            y=alt.Y("size:Q", title="Teams Count"),
            tooltip=[alt.Tooltip("year:O", title="Year"), alt.Tooltip("size:Q", title="Teams")]
        )
        .properties(title="Number of Teams per Year")
    )
    return chart


def avg_wins_per_year(df: pd.DataFrame):
    """Return a line chart showing average wins by season."""
    d = df.copy()
    if "wins" not in d.columns or "year" not in d.columns:
        return alt.LayerChart()

    d["year"] = pd.to_numeric(d["year"], errors="coerce")
    d = d.dropna(subset=["year"])
    agg = d.groupby("year", as_index=False)["wins"].mean()

    chart = (
        alt.Chart(agg)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "year:Q",
                title="Year",
                scale=alt.Scale(domain=[1990, 2011], nice=False),
                # Integer formatting
                axis=alt.Axis(format="d", formatType="number", tickMinStep=1, labelOverlap="greedy"),
            ),
            y=alt.Y("wins:Q", title="Average Wins"),
            tooltip=[
                alt.Tooltip("year:Q", format="d", title="Year"),
                alt.Tooltip("wins:Q", format=".2f", title="Avg Wins"),
            ],
        )
        .properties(title="Average Wins by Year")
    )
    return chart


def top_teams_by_win_pct(df: pd.DataFrame, top_n: int = 10):
    """Produce a bar chart highlighting the top-N teams by peak win percentage."""
    d = _ensure_types(df)
    if "win_pct" not in d.columns:
        return alt.LayerChart()
    # Best season per team (max win %)
    best = d.sort_values(["team", "win_pct"], ascending=[True, False]).dropna(subset=["win_pct"])
    best = best.groupby("team", as_index=False).first().nlargest(top_n, "win_pct")
    chart = (
        alt.Chart(best)
        .mark_bar()
        .encode(
            x=alt.X("win_pct:Q", title="Best Win %"),
            y=alt.Y("team:N", sort="-x", title="Team"),
            color=alt.Color("year:O", title="Year"),
            tooltip=["team:N", "year:O", alt.Tooltip("win_pct:Q", format=".3f", title="Win %")]
        )
        .properties(title=f"Top {top_n} Teams by Best Season Win %")
    )
    return chart


def goals_scatter(df: pd.DataFrame):
    """Plot goals for vs. goals against to contrast offense and defense per season."""
    d = _ensure_types(df)
    if not {"goals_for", "goals_against"}.issubset(d.columns):
        return alt.LayerChart()
    chart = (
        alt.Chart(d)
        .mark_circle(size=60, opacity=0.7)
        .encode(
            x=alt.X("goals_for:Q", title="Goals For (GF)"),
            y=alt.Y("goals_against:Q", title="Goals Against (GA)"),
            color=alt.Color("year:O", title="Year"),
            tooltip=["team:N", "year:O", "wins:Q", "losses:Q", alt.Tooltip("win_pct:Q", format=".3f", title="Win %")]
        )
        .properties(title="Goals For vs Goals Against (by Team Season)")
    )
    return chart


def win_pct_hist(df: pd.DataFrame):
    """Render a histogram summarizing the distribution of win percentages."""
    d = _ensure_types(df)
    if "win_pct" not in d.columns:
        return alt.LayerChart()
    chart = (
        alt.Chart(d.dropna(subset=["win_pct"]))
        .mark_bar(opacity=0.8)
        .encode(
            x=alt.X("win_pct:Q", bin=alt.Bin(maxbins=30), title="Win %"),
            y=alt.Y("count():Q", title="Count"),
            tooltip=[alt.Tooltip("count():Q", title="Count")]
        )
        .properties(title="Distribution of Win % Across Seasons")
    )
    return chart