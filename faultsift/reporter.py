from faultsift.scoring import ScanSummary


#
#
#


def render_summary(summary: ScanSummary) -> str:
    lines = []

    lines.append ("FaultSift Report")
    lines.append("=" * 40)
    lines.append(f"Total hits: {summary.total_hits}")
    lines.append(f"Total score: {summary.total_score}")     
    lines.append("")

    lines.append("Severity counts:")
    if summary.severity_counts:
        for severity, count in sorted(summary.severity_counts.items()):
             lines.append(f"  - {severity}: {count}")
    else:
        lines.append("  - none")
    lines.append("")

    lines.append("Category counts:")
    if summary.category_counts:
        for category, count in sorted(summary.category_counts.items()):
            lines.append(f"  - {category}: {count}")
    else:
        lines.append("  - none")
    lines.append("")

    lines.append("Top hits:")
    if summary.top_hits:
        for hit in summary.top_hits:
            lines.append(
                f"  line {hit.line_number} | {hit.severity} | {hit.category} | {hit.raw_line}"
            )
    else:
        lines.append("  - none")

    return "\n".join(lines) 