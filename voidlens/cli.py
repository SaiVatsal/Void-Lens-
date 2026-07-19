"""
VoidLens CLI — cybersecurity-inspired terminal interface.

Matrix green-on-black themed command-line application built with Typer and Rich.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.text import Text
from rich import box

from voidlens import __version__
from voidlens.constants import BANNER, Status, ScanType, Theme, STATUS_STYLE_MAP
from voidlens.core.models import ScanResult
from voidlens.core.runner import scan_username, scan_email, scan_batch
from voidlens.core.formatter import export
from voidlens.core.report import build_summary
from voidlens.core.logger import setup_logger

app = typer.Typer(
    name="voidlens",
    help="Peer into the digital void — OSINT & Digital Footprint Intelligence Suite",
    no_args_is_help=True,
    rich_markup_mode="rich",
    add_completion=False,
)

console = Console(highlight=False)


def _print_banner() -> None:
    """Display the VoidLens ASCII banner."""
    console.print(BANNER.format(version=__version__))


def _print_results_table(result: ScanResult, verbose: bool = False) -> None:
    """Print scan results as a styled Rich table."""
    table = Table(
        box=box.SIMPLE_HEAVY,
        border_style="green",
        header_style="bold bright_green",
        title=f"[bold bright_green]◈ {result.scan_type.value.upper()}: {result.query}[/]",
        title_style="bold bright_green",
        pad_edge=True,
    )
    table.add_column("Site", style="bright_green", min_width=20)
    table.add_column("Status", min_width=12)
    if verbose:
        table.add_column("URL", style="bright_cyan", max_width=50)
        table.add_column("Time", style="dim green", justify="right")
        table.add_column("Code", style="dim green", justify="right")
        table.add_column("Reason", style="dim white", max_width=30)

    for site in sorted(result.results, key=lambda s: s.site):
        style = STATUS_STYLE_MAP.get(site.status, "white")
        status_text = Text(site.status.value, style=style)
        row = [site.site, status_text]
        if verbose:
            row.extend([
                site.url,
                f"{site.response_time:.2f}s",
                str(site.status_code),
                site.reason,
            ])
        table.add_row(*row)

    console.print(table)


def _print_summary(result: ScanResult) -> None:
    """Print scan summary panel."""
    summary = build_summary([result])
    panel_text = (
        f"[bright_green]◈ Scanned:[/] {summary.total_sites}  "
        f"[bright_green]◈ Found:[/] {summary.total_found}  "
        f"[dim white]◈ Not Found:[/] {summary.total_not_found}  "
        f"[yellow]◈ Unknown:[/] {summary.total_unknown}  "
        f"[red]◈ Errors:[/] {summary.total_errors}  "
        f"[dim green]◈ Elapsed:[/] {result.elapsed}s"
    )
    console.print(Panel(panel_text, border_style="green", title="[bold bright_green]Summary[/]"))


async def _run_scan(
    usernames: list[str],
    emails: list[str],
    categories: list[str] | None,
    modules: list[str] | None,
    verbose: bool,
    concurrency: int,
    timeout: int,
    proxy_file: str | None,
    json_out: str | None,
    csv_out: str | None,
    html_out: str | None,
    md_out: str | None,
    xml_out: str | None,
    sarif_out: str | None,
) -> None:
    """Execute the scan pipeline."""
    all_results: list[ScanResult] = []

    total_tasks = len(usernames) + len(emails)

    with Progress(
        SpinnerColumn(style="bright_green"),
        TextColumn("[bright_green]{task.description}[/]"),
        BarColumn(bar_width=30, complete_style="bright_green", finished_style="green"),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Scanning...", total=total_tasks)

        for username in usernames:
            result = await scan_username(
                username, categories=categories, modules=modules,
                concurrency=concurrency, timeout=timeout, proxy_file=proxy_file,
            )
            all_results.append(result)
            progress.advance(task)

        for email in emails:
            result = await scan_email(
                email, categories=categories, modules=modules,
                concurrency=concurrency, timeout=timeout, proxy_file=proxy_file,
            )
            all_results.append(result)
            progress.advance(task)

    # Display results
    for result in all_results:
        _print_results_table(result, verbose=verbose)
        _print_summary(result)

    # Export
    exports = {
        "json": json_out, "csv": csv_out, "html": html_out,
        "md": md_out, "xml": xml_out, "sarif": sarif_out,
    }
    for fmt, path in exports.items():
        if path:
            export(all_results, path, fmt)
            console.print(f"[bright_green]◈ Exported {fmt.upper()}:[/] {path}")


def _load_file(path: str) -> list[str]:
    """Load queries from a text file (one per line)."""
    filepath = Path(path)
    if not filepath.exists():
        console.print(f"[red]Error:[/] File not found: {path}")
        raise typer.Exit(1)
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


@app.command()
def scan(
    username: Optional[str] = typer.Option(None, "-u", "--username", help="Username to scan"),
    email: Optional[str] = typer.Option(None, "-e", "--email", help="Email to scan"),
    username_file: Optional[str] = typer.Option(None, "-uf", "--username-file", help="File with usernames"),
    email_file: Optional[str] = typer.Option(None, "-ef", "--email-file", help="File with emails"),
    category: Optional[list[str]] = typer.Option(None, "-c", "--category", help="Filter by category"),
    module: Optional[list[str]] = typer.Option(None, "-m", "--module", help="Run specific modules"),
    verbose: bool = typer.Option(False, "-v", "--verbose", help="Verbose output"),
    concurrency: int = typer.Option(100, "--concurrency", help="Max concurrent requests"),
    timeout: int = typer.Option(5, "--timeout", help="Request timeout (seconds)"),
    proxy_file: Optional[str] = typer.Option(None, "-P", "--proxy", help="Proxy list file"),
    json_out: Optional[str] = typer.Option(None, "--json", help="Export JSON report"),
    csv_out: Optional[str] = typer.Option(None, "--csv", help="Export CSV report"),
    html_out: Optional[str] = typer.Option(None, "--html", help="Export HTML report"),
    md_out: Optional[str] = typer.Option(None, "--md", help="Export Markdown report"),
    xml_out: Optional[str] = typer.Option(None, "--xml", help="Export XML report"),
    sarif_out: Optional[str] = typer.Option(None, "--sarif", help="Export SARIF report"),
) -> None:
    """Scan usernames and emails across the digital void."""
    _print_banner()
    setup_logger(verbose=verbose)

    usernames: list[str] = []
    emails: list[str] = []

    if username:
        usernames.append(username)
    if username_file:
        usernames.extend(_load_file(username_file))
    if email:
        emails.append(email)
    if email_file:
        emails.extend(_load_file(email_file))

    if not usernames and not emails:
        console.print("[red]Error:[/] Provide at least one username (-u) or email (-e)")
        raise typer.Exit(1)

    asyncio.run(_run_scan(
        usernames=usernames, emails=emails,
        categories=category, modules=module,
        verbose=verbose, concurrency=concurrency, timeout=timeout,
        proxy_file=proxy_file, json_out=json_out, csv_out=csv_out,
        html_out=html_out, md_out=md_out, xml_out=xml_out, sarif_out=sarif_out,
    ))


@app.command()
def version() -> None:
    """Show VoidLens version."""
    console.print(f"[bright_green]VoidLens[/] v{__version__}")


@app.command()
def update() -> None:
    """Check for updates and upgrade."""
    import subprocess
    console.print("[bright_green]Checking for updates...[/]")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "voidlens"],
            capture_output=True, text=True,
        )
        if "Successfully installed" in result.stdout:
            console.print("[bright_green]◈ Updated successfully![/]")
        else:
            console.print("[dim green]Already up to date.[/]")
    except Exception as exc:
        console.print(f"[red]Update failed:[/] {exc}")


if __name__ == "__main__":
    app()
