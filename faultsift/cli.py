#
#
#


from pathlib import Path

import typer

from faultsift.reporter import render_summary
from faultsift.scanner import scan_lines
from faultsift.scoring import summarize_hits

app = typer.Typer()


@app.command()
def analyze(path: str, top: int = 5):
    file_path = Path(path)

    if not file_path.exists():
        typer.echo(f"File not found: {file_path}")
        raise typer.Exit(code=1)

    if not file_path.is_file():
        typer.echo(f"Not a file: {file_path}")
        raise typer.Exit(code=1)

    try:
        text = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = file_path.read_text(encoding="utf-8", errors="ignore")

    lines = text.splitlines()
    hits = scan_lines(lines)
    summary = summarize_hits(hits, limit=top)

    typer.echo(render_summary(summary))


@app.command()
def demo():
    lines = [
        "system boot ok",
        "failed password for root",
        "permission denied",
        "kernel panic - not syncing",
        "segfault at 0",
    ]

    hits = scan_lines(lines)
    summary = summarize_hits(hits)
    typer.echo(render_summary(summary))


if __name__ == "__main__":
    app()