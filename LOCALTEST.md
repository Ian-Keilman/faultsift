# Local Testing Notes

These are the local PowerShell checks I used while building FaultSift.

## Environment check

```powershell
python --version

Expected on my machine:

Python 3.10.2
Rule checks

Check that a filesystem read-only style error matches the right rule:

python -c "from faultsift.rules import best_match; print(best_match('EXT4-fs error remounting filesystem read-only'))"

Expected shape of output:

LogRule(category='filesystem read-only', severity='critical', score=88, ...)

Check that a DNS resolution issue matches the right rule:

python -c "from faultsift.rules import best_match; print(best_match('temporary failure in name resolution'))"

Expected shape of output:

LogRule(category='dns failure', severity='low', score=30, ...)

Check that a kernel panic line matches the right rule:

python -c "from faultsift.rules import best_match; print(best_match('kernel panic - not syncing'))"

Expected shape of output:

LogRule(category='kernel panic', severity='critical', score=100, ...)
Scanner checks

Check that only suspicious lines become hits:

python -c "from faultsift.scanner import scan_lines; lines=['all good here','kernel panic - not syncing','failed password for root']; print(scan_lines(lines))"

Expected shape of output:

[ScanHit(line_number=2, raw_line='kernel panic - not syncing', category='kernel panic', severity='critical', score=100), ScanHit(line_number=3, raw_line='failed password for root', category='authentication failure', severity='medium', score=50)]
Scoring checks

Check that hits are summarized correctly:

python -c "from faultsift.scanner import scan_lines; from faultsift.scoring import summarize_hits; lines=['all good here','kernel panic - not syncing','failed password for root','permission denied','segfault at 0']; hits=scan_lines(lines); print(summarize_hits(hits))"

Expected output:

ScanSummary(total_hits=4, total_score=280, severity_counts={'critical': 2, 'medium': 2}, category_counts={'kernel panic': 1, 'authentication failure': 1, 'permission issue': 1, 'segfault': 1}, top_hits=[ScanHit(line_number=2, raw_line='kernel panic - not syncing', category='kernel panic', severity='critical', score=100), ScanHit(line_number=5, raw_line='segfault at 0', category='segfault', severity='critical', score=90), ScanHit(line_number=3, raw_line='failed password for root', category='authentication failure', severity='medium', score=50), ScanHit(line_number=4, raw_line='permission denied', category='permission issue', severity='medium', score=40)])
Reporter checks

Check that the plain-text report renders correctly:

python -c "from faultsift.scanner import scan_lines; from faultsift.scoring import summarize_hits; from faultsift.reporter import render_summary; lines=['all good here','kernel panic - not syncing','failed password for root','permission denied','segfault at 0']; hits=scan_lines(lines); summary=summarize_hits(hits); print(render_summary(summary))"

Expected output:

FaultSift Report
========================================
Total hits: 4
Total score: 280

Severity counts:
  - critical: 2
  - medium: 2

Category counts:
  - authentication failure: 1
  - kernel panic: 1
  - permission issue: 1
  - segfault: 1

Top hits:
  line 2 | critical | kernel panic | kernel panic - not syncing
  line 5 | critical | segfault | segfault at 0
  line 3 | medium | authentication failure | failed password for root
  line 4 | medium | permission issue | permission denied
CLI demo check

Run the built-in demo command:

python -m faultsift.cli demo

Expected output:

FaultSift Report
========================================
Total hits: 4
Total score: 280

Severity counts:
  - critical: 2
  - medium: 2

Category counts:
  - authentication failure: 1
  - kernel panic: 1
  - permission issue: 1
  - segfault: 1

Top hits:
  line 4 | critical | kernel panic | kernel panic - not syncing
  line 5 | critical | segfault | segfault at 0
  line 2 | medium | authentication failure | failed password for root
  line 3 | medium | permission issue | permission denied
Sample log creation

Create a sample log file in PowerShell:

@"
system boot ok
failed password for root
permission denied
kernel panic - not syncing
segfault at 0
"@ | Set-Content sample.log
CLI file analysis check

Analyze the sample log:

python -m faultsift.cli analyze sample.log

Expected output:

FaultSift Report
========================================
Total hits: 4
Total score: 280

Severity counts:
  - critical: 2
  - medium: 2

Category counts:
  - authentication failure: 1
  - kernel panic: 1
  - permission issue: 1
  - segfault: 1

Top hits:
  line 4 | critical | kernel panic | kernel panic - not syncing
  line 5 | critical | segfault | segfault at 0
  line 2 | medium | authentication failure | failed password for root
  line 3 | medium | permission issue | permission denied
Pytest check

Run pytest:

pytest

Current output on my machine:

============================================================================================= test session starts ==============================================================================================
platform win32 -- Python 3.10.2, pytest-9.0.2, pluggy-1.6.0
rootdir: (removing address for obvious reasons)
configfile: pyproject.toml
testpaths: tests
collected 0 items

============================================================================================ no tests ran in 0.02s =============================================================================================
# Local Testing Notes

These are the local PowerShell checks I used while building FaultSift.

## Environment check

```powershell
python --version

Expected on my machine:

Python 3.10.2
Rule checks

Check that a filesystem read-only style error matches the right rule:

python -c "from faultsift.rules import best_match; print(best_match('EXT4-fs error remounting filesystem read-only'))"

Expected shape of output:

LogRule(category='filesystem read-only', severity='critical', score=88, ...)

Check that a DNS resolution issue matches the right rule:

python -c "from faultsift.rules import best_match; print(best_match('temporary failure in name resolution'))"

Expected shape of output:

LogRule(category='dns failure', severity='low', score=30, ...)

Check that a kernel panic line matches the right rule:

python -c "from faultsift.rules import best_match; print(best_match('kernel panic - not syncing'))"

Expected shape of output:

LogRule(category='kernel panic', severity='critical', score=100, ...)
Scanner checks

Check that only suspicious lines become hits:

python -c "from faultsift.scanner import scan_lines; lines=['all good here','kernel panic - not syncing','failed password for root']; print(scan_lines(lines))"

Expected shape of output:

[ScanHit(line_number=2, raw_line='kernel panic - not syncing', category='kernel panic', severity='critical', score=100), ScanHit(line_number=3, raw_line='failed password for root', category='authentication failure', severity='medium', score=50)]
Scoring checks

Check that hits are summarized correctly:

python -c "from faultsift.scanner import scan_lines; from faultsift.scoring import summarize_hits; lines=['all good here','kernel panic - not syncing','failed password for root','permission denied','segfault at 0']; hits=scan_lines(lines); print(summarize_hits(hits))"

Expected output:

ScanSummary(total_hits=4, total_score=280, severity_counts={'critical': 2, 'medium': 2}, category_counts={'kernel panic': 1, 'authentication failure': 1, 'permission issue': 1, 'segfault': 1}, top_hits=[ScanHit(line_number=2, raw_line='kernel panic - not syncing', category='kernel panic', severity='critical', score=100), ScanHit(line_number=5, raw_line='segfault at 0', category='segfault', severity='critical', score=90), ScanHit(line_number=3, raw_line='failed password for root', category='authentication failure', severity='medium', score=50), ScanHit(line_number=4, raw_line='permission denied', category='permission issue', severity='medium', score=40)])
Reporter checks

Check that the plain-text report renders correctly:

python -c "from faultsift.scanner import scan_lines; from faultsift.scoring import summarize_hits; from faultsift.reporter import render_summary; lines=['all good here','kernel panic - not syncing','failed password for root','permission denied','segfault at 0']; hits=scan_lines(lines); summary=summarize_hits(hits); print(render_summary(summary))"

Expected output:

FaultSift Report
========================================
Total hits: 4
Total score: 280

Severity counts:
  - critical: 2
  - medium: 2

Category counts:
  - authentication failure: 1
  - kernel panic: 1
  - permission issue: 1
  - segfault: 1

Top hits:
  line 2 | critical | kernel panic | kernel panic - not syncing
  line 5 | critical | segfault | segfault at 0
  line 3 | medium | authentication failure | failed password for root
  line 4 | medium | permission issue | permission denied
CLI demo check

Run the built-in demo command:

python -m faultsift.cli demo

Expected output:

FaultSift Report
========================================
Total hits: 4
Total score: 280

Severity counts:
  - critical: 2
  - medium: 2

Category counts:
  - authentication failure: 1
  - kernel panic: 1
  - permission issue: 1
  - segfault: 1

Top hits:
  line 4 | critical | kernel panic | kernel panic - not syncing
  line 5 | critical | segfault | segfault at 0
  line 2 | medium | authentication failure | failed password for root
  line 3 | medium | permission issue | permission denied
Sample log creation

Create a sample log file in PowerShell:

@"
system boot ok
failed password for root
permission denied
kernel panic - not syncing
segfault at 0
"@ | Set-Content sample.log
CLI file analysis check

Analyze the sample log:

python -m faultsift.cli analyze sample.log

Expected output:

FaultSift Report
========================================
Total hits: 4
Total score: 280

Severity counts:
  - critical: 2
  - medium: 2

Category counts:
  - authentication failure: 1
  - kernel panic: 1
  - permission issue: 1
  - segfault: 1

Top hits:
  line 4 | critical | kernel panic | kernel panic - not syncing
  line 5 | critical | segfault | segfault at 0
  line 2 | medium | authentication failure | failed password for root
  line 3 | medium | permission issue | permission denied
Pytest check

Run pytest:

pytest

Current output on my machine:

============================================================================================= test session starts ==============================================================================================
platform win32 -- Python 3.10.2, pytest-9.0.2, pluggy-1.6.0
rootdir: (my address would be here)
configfile: pyproject.toml
testpaths: tests
collected 0 items

============================================================================================ no tests ran in 0.02s =============================================================================================
