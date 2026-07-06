#!/usr/bin/env python3
"""Run gitcheck-style activity scan for every day in a month; write one file per day."""

import argparse
import calendar
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR / "work"
DEFAULT_AUTHOR = r"Max Huiskes\|max.huiskes"
SKIP_DIRS = frozenset({"vendor", "contrib"})
COMMIT_RE = re.compile(
    r"^([0-9a-f]{7,40})\s+.*?\s+(\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}:\d{2}\s+"
)


def find_git_repos(parent_dir: Path) -> list[Path]:
    repos = []
    for dirpath, dirnames, _ in os.walk(parent_dir):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        if ".git" in dirnames:
            repos.append(Path(dirpath))
            dirnames.remove(".git")
    return sorted(repos)


def git_author() -> str:
    try:
        out = subprocess.run(
            ["git", "config", "--get", "user.name"],
            capture_output=True,
            text=True,
            check=False,
        )
        name = out.stdout.strip()
        if name:
            return name
    except OSError:
        pass
    return DEFAULT_AUTHOR


def fetch_repo(repo_dir: Path) -> None:
    subprocess.run(
        ["git", "fetch", "--all", "--quiet"],
        cwd=repo_dir,
        capture_output=True,
        check=False,
    )


def month_log(repo_dir: Path, author: str, start: date, end: date) -> str:
    result = subprocess.run(
        [
            "git",
            "log",
            "--all",
            f"--author={author}",
            "--regexp-ignore-case",
            f"--since={start.isoformat()} 00:00:00",
            f"--until={end.isoformat()} 23:59:59",
            "--decorate=short",
            "--format=%h %d %ad %s",
            "--date=format-local:%Y-%m-%d %H:%M:%S",
            "--shortstat",
        ],
        cwd=repo_dir,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip()


def split_log_by_day(raw: str) -> dict[date, list[str]]:
    by_day: dict[date, list[str]] = defaultdict(list)
    if not raw:
        return by_day

    blocks = re.split(r"\n(?=[0-9a-f]{7,40}\s)", raw)
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        match = COMMIT_RE.match(block)
        if not match:
            continue
        day = date.fromisoformat(match.group(2))
        by_day[day].append(block)

    return by_day


def collect_month(
    repos: list[Path], author: str, days: list[date], do_fetch: bool
) -> dict[date, list[str]]:
    start, end = days[0], days[-1]
    day_sections: dict[date, list[str]] = defaultdict(list)
    valid_days = set(days)

    for i, repo in enumerate(repos, 1):
        print(f"[{i}/{len(repos)}] {repo}", flush=True)
        if do_fetch:
            fetch_repo(repo)
        raw = month_log(repo, author, start, end)
        for day, commits in split_log_by_day(raw).items():
            if day not in valid_days:
                continue
            day_sections[day].append(f"## {repo}\n\n" + "\n\n".join(commits))

    return day_sections


def days_in_month(year: int, month: int) -> list[date]:
    _, last = calendar.monthrange(year, month)
    return [date(year, month, d) for d in range(1, last + 1)]


def parse_month(value: str) -> tuple[int, int]:
    try:
        year_s, month_s = value.split("-", 1)
        year, month = int(year_s), int(month_s)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "month must be YYYY-MM (e.g. 2026-03)"
        ) from exc
    if not 1 <= month <= 12:
        raise argparse.ArgumentTypeError("month must be 01-12")
    return year, month


def main() -> int:
    today = date.today()
    parser = argparse.ArgumentParser(
        description="Log git activity by day for a whole month into git/work/"
    )
    parser.add_argument(
        "month",
        nargs="?",
        type=parse_month,
        default=(today.year, today.month),
        help="YYYY-MM (default: current month)",
    )
    parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        default=Path.home() / "Desktop",
        help="parent directory to scan for repos (default: ~/Desktop)",
    )
    parser.add_argument(
        "author",
        nargs="?",
        default=None,
        help=f"git --author regex (default: git user.name or {DEFAULT_AUTHOR})",
    )
    parser.add_argument(
        "-f",
        "--fetch",
        action="store_true",
        help="git fetch --all once per repo before checking",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=WORK_DIR,
        help=f"where to write day files (default: {WORK_DIR})",
    )
    args = parser.parse_args()

    year, month = args.month if isinstance(args.month, tuple) else args.month
    parent_dir = args.directory.expanduser().resolve()
    author = args.author or git_author()
    output_dir = args.output_dir.expanduser().resolve()

    if not parent_dir.is_dir():
        print(f"Error: directory not found: {parent_dir}", file=sys.stderr)
        return 1

    repos = find_git_repos(parent_dir)
    if not repos:
        print(f"No git repos found under {parent_dir}", file=sys.stderr)
        return 1

    days = days_in_month(year, month)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Month: {year}-{month:02d}")
    print(f"Scanning: {parent_dir} ({len(repos)} repos)")
    print(f"Author: {author}")
    print(f"Output: {output_dir}")
    print("-" * 54)

    day_sections = collect_month(repos, author, days, args.fetch)
    written = 0
    empty = 0
    day_set = set(days)

    for day in days:
        sections = day_sections.get(day)
        out_path = output_dir / f"{day.isoformat()}.md"
        if sections:
            header = f"# {day.isoformat()}\n\nAuthor filter: {author}\n\n"
            out_path.write_text(header + "\n\n".join(sections) + "\n", encoding="utf-8")
            written += 1
            print(f"{day.isoformat()}: {len(sections)} repo(s)")
        else:
            if out_path.exists():
                out_path.unlink()
            empty += 1

    stray = [d for d in day_sections if d not in day_set]
    if stray:
        print(f"Note: ignored {len(stray)} commit(s) outside month range", file=sys.stderr)

    print("-" * 54)
    print(f"Done. {written} day file(s), {empty} day(s) with no activity.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
