from collections import Counter
from dataclasses import dataclass

from faultsift.scanner import ScanHit


# Holds the overall results after scanning a file or list of lines
@dataclass
class ScanSummary:
    total_hits: int
    total_score: int
    severity_counts: dict[str, int]
    category_counts: dict[str, int]
    top_hits: list[ScanHit]


# Add up all scores from every hit
def total_score(hits: list[ScanHit]) -> int:
    return sum(hit.score for hit in hits)


# Count how many hits landed in each severity bucket
def count_by_severity(hits: list[ScanHit]) -> dict[str, int]:
    counts = Counter(hit.severity for hit in hits)
    return dict(counts)


# Count how many hits appeared in each category
def count_by_category(hits: list[ScanHit]) -> dict[str, int]:
    counts = Counter(hit.category for hit in hits)
    return dict(counts)


# Sort hits by score first, then by line number, and keep the top few
def top_hits(hits: list[ScanHit], limit: int = 5) -> list[ScanHit]:
    ranked_hits = sorted(hits, key=lambda hit: (-hit.score, hit.line_number))
    return ranked_hits[:limit]


# Build one summary object that the reporter can print nicely
def summarize_hits(hits: list[ScanHit], limit: int = 5) -> ScanSummary:
    return ScanSummary(
        total_hits=len(hits),
        total_score=total_score(hits),
        severity_counts=count_by_severity(hits),
        category_counts=count_by_category(hits),
        top_hits=top_hits(hits, limit),
    )