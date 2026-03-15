from faultsift.scanner import scan_lines
from faultsift.scoring import (
    count_by_category,
    count_by_severity,
    summarize_hits,
     top_hits,
    total_score,
)


def make_hits():
    lines = [
        "all good here" ,
        "kernel panic - not syncing",
        "failed password for root",
        "permission denied",
        "segfault at 0",
    ]
    return scan_lines(lines)


def test_total_score():
    hits = make_hits()
    assert total_score(hits) == 280


def test_count_by_severity():
    hits =  make_hits()
    counts = count_by_severity(hits)

    assert counts["critical"] == 2
    assert counts["medium"] == 2


def test_count_by_category():
    hits = make_hits()
    counts = count_by_category(hits)

    assert counts["kernel panic"] == 1
    assert counts["authentication failure"] == 1
    assert counts["permission issue"] == 1
    assert counts["segfault"] == 1


def test_top_hits_orders_by_score():
    hits = make_hits()
    ranked = top_hits(hits)

    assert ranked[0].category == "kernel panic"
    assert ranked[1].category == "segfault"


def test_summarize_hits():
    hits  = make_hits()
    summary = summarize_hits(hits)

    assert summary.total_hits == 4
    assert summary.total_score == 280
    assert summary.severity_counts["critical"] == 2
    assert summary.category_counts["segfault"] == 1
    assert len(summary.top_hits) ==  4