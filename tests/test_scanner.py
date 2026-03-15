#fix pytest discovery

from faultsift.scanner import scan_line, scan_lines


def test_scan_line_returns_hit() :
    hit = scan_line("kernel panic - not syncing\n", 7 )

    assert hit is not None
    assert hit.line_number == 7
    assert hit.raw_line == "kernel panic - not syncing"
    assert hit.category == "kernel panic"
    assert hit.severity == "critical"
    assert hit.score == 100


def test_scan_line_returns_none_for_clean_line():
    hit = scan_line("system boot ok\n", 1)
    assert hit is None


def test_scan_lines_collects_only_matching_lines():
    lines = [
        "all good here",
         "failed password for root",
        "permission denied",
    ]

    hits = scan_lines(lines)

    assert len(hits) == 2
    assert hits[0].line_number == 2
    assert hits[0].category == "authentication failure"
    assert hits[1].line_number == 3
    assert hits[1].category == "permission issue"