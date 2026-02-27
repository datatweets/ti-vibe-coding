# Review Code Quality

Review the staged or recently changed files in this project for:

1. **PEP 8 / ruff compliance** — flag any style or lint issues
2. **Type hints** — ensure all public function signatures have type annotations
3. **Docstrings** — verify Google-style docstrings on all public functions
4. **Test coverage** — identify any new public functions that are missing tests
5. **CLAUDE.md alignment** — check that changes respect the coding standards in CLAUDE.md

Output a short bullet-point summary: what looks good, what needs attention.
Run `ruff check src/ tests/` and report results before giving your summary.
