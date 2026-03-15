from dataclasses import dataclass, field
from pathlib import Path

#
#

@dataclass
class Finding:
    file_path: Path
    line_number: int
    raw_line: str
    category: str
    severity: str
    score: int


@dataclass
class ScanSummary:
    total_files_scanned: int = 0
    total_lines_scanned: int = 0
    findings: list[Finding] = field(default_factory=list)

    @property
    def total_findings(self) -> int:
        return len(self.findings)
    
    ##