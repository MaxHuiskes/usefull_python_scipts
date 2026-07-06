# Git activity tools

Scripts to see what you committed across many repos (e.g. everything under `~/Desktop/Workspace`).

Both tools:

- Walk a parent folder and find every `.git` repo
- Skip `vendor/` and `contrib/`
- Filter by author (name or email, case-insensitive)
- Use `git log --all` (all branches)

## gitcheck.sh — one day, terminal output

```bash
cd git
chmod +x gitcheck.sh   # once

./gitcheck.sh 2026-05-18 ~/Desktop/Workspace
./gitcheck.sh 2026-05-18 ~/Desktop/Workspace "max.huiskes"
./gitcheck.sh -f 2026-05-18 ~/Desktop/Workspace
```

| Argument | Default |
|----------|---------|
| date | required (`YYYY-MM-DD`) |
| directory | `.` (current folder) |
| author | `git config user.name`, or `Max Huiskes\|max.huiskes` |

`-f` runs `git fetch --all` in each repo before checking (slower; use if commits are only on remote).

## monthly_work_log.py — whole month, one file per day

Writes markdown to `git/work/YYYY-MM-DD.md` (only days with commits).

```bash
python3 git/monthly_work_log.py 2026-05 ~/Desktop/Workspace
python3 git/monthly_work_log.py 2026-05 ~/Desktop/Workspace "max.huiskes"
python3 git/monthly_work_log.py -f 2026-05 ~/Desktop/Workspace
python3 git/monthly_work_log.py -o ~/Desktop/work-logs 2026-05 ~/Desktop/Workspace
```

| Argument | Default |
|----------|---------|
| month | current month (`YYYY-MM`) |
| directory | `~/Desktop` |
| author | `git config user.name`, or `Max Huiskes\|max.huiskes` |

| Flag | Effect |
|------|--------|
| `-f` / `--fetch` | `git fetch --all` once per repo |
| `-o` / `--output-dir` | output folder (default: `git/work/`) |

Progress prints as `[1/47] /path/to/repo`. Empty days get no file; old files for days with no activity are removed.

## Author filter

Git `--author` is a regex. Examples:

- `max.huiskes` — matches email
- `Max Huiskes` — matches display name
- `Max Huiskes\|max.huiskes` — both (default if no git user.name)

Quote the pattern in the shell when it contains `|`:

```bash
./gitcheck.sh 2026-05-18 ~/Desktop/Workspace "Max Huiskes\|max.huiskes"
```

## Typical workflow

**Today:**

```bash
./git/gitcheck.sh 2026-07-06 ~/Desktop/Workspace
```

**End of month (timesheet / review):**

```bash
python3 git/monthly_work_log.py 2026-06 ~/Desktop/Workspace
```

Output lives in `git/work/`, not under Workspace. Each file lists repo paths and commits for that day.

## Notes

- Scan folder ≠ output folder. `~/Desktop/Workspace` is where repos are read from; results go to `git/work/` unless you pass `-o`.
- No commits for that month/author → no day files (expected).
- Large folders (40+ repos): monthly script is faster than running gitcheck 30 times; `-f` adds time but only fetches each repo once.
