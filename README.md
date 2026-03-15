# FaultSift

FaultSift is a small command-line tool for digging through Linux logs and surfacing more important lines.

Simply put: point it at a log file or a folder of logs, let it scan for suspicious patterns like authentication failures, crashes, timeouts, permission issues, and disk problems, then get back a clean summary of what needs attention.

I figured that it would be cool to do something security related, after having been focused on mostly backend or frontend SWE.
Cybersecurity is an industry that would be really cool to be a part of.

I wanted one project in my portfolio that felt a little more systems-oriented and a little less like a CRUD web app. This seemed like a good way to practice building a real CLI, handling messy text data, and writing something that feels useful for debugging, operations, or security triage. Pay attention, internship recruiters.

## What it aims to do

- Scans either one log file or a whole directory
- Can pick out suspicious or important lines
- Shows group findings by type and severity
- Will give higher priority to more serious issues
- Prints a readable terminal summary
- Export results to JSON on command

## Stack

- Python
- Typer
- Rich
- pytest

## Planned usage

```bash
python -m faultsift.cli scan ./sample_logs
python -m faultsift.cli scan ./sample_logs --json-out outputs/report.json
python -m faultsift.cli scan ./sample_logs --keyword timeout --min-severity medium