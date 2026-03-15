from dataclasses import dataclass
from pathlib import Path

from faultsift.rules import best_match


# Stores one line that matched one of the log rules
@dataclass
class ScanHit:
    line_number: int
    raw_line: str
    category: str
    severity: str
    score: int


# Check a single line and return a ScanHit if it matches something
def scan_line(line: str, line_number: int) -> ScanHit | None:
    found_rule = best_match(line)

    if found_rule is None:
        return None

    clean_line = line.rstrip("\n")

    return ScanHit(
        line_number=line_number,
        raw_line=clean_line,
        category=found_rule.category,
        severity=found_rule.severity,
        score=found_rule.score,
    )


# Go through every line and keep only the ones that matched
def scan_lines(lines: list[str]) -> list[ScanHit]:
    found_hits = []

    for line_number, line in enumerate(lines, start=1):
        hit = scan_line(line, line_number)
        if hit is not None:
            found_hits.append(hit)

    return found_hits


# Open a file, read the lines, and scan them
def scan_file(path: str | Path) -> list[ScanHit]:
    file_path = Path(path)

    with file_path.open("r", encoding="utf-8", errors="ignore") as file:
        all_lines = file.readlines()

    return scan_lines(all_lines)

