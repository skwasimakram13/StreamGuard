## Summary

<!-- 
  Provide a brief, clear description of what this PR changes and why.
  Focus on the "why" — what problem does it solve or what value does it add?
-->

Closes #<!-- issue number, e.g., Closes #42 -->

---

## Type of Change

<!-- Check all that apply -->

- [ ] 🐛 **Bug fix** — non-breaking change that resolves a reported issue
- [ ] ✨ **New feature** — non-breaking addition of new functionality
- [ ] 💥 **Breaking change** — fix or feature that changes existing behavior in a backward-incompatible way
- [ ] 📝 **Documentation** — changes to README, CHANGELOG, CONTRIBUTING, or inline docstrings only
- [ ] 🔧 **Refactor** — internal code restructuring with no observable behavior change
- [ ] ⚡ **Performance** — improvement to speed, memory usage, or API quota efficiency
- [ ] 🔒 **Security fix** — addresses a security vulnerability (ensure you have followed [SECURITY.md](SECURITY.md))
- [ ] 🔨 **Build / CI** — changes to GitHub Actions, installer scripts, or build configuration

---

## What Changed

<!-- 
  Provide a concise but complete description of the changes made:
  - Which files were modified and why
  - Any new dependencies introduced
  - Any configuration or environment changes required
-->

**Files changed:**
- `file.py` — reason for change
- `other_file.py` — reason for change

---

## Testing Done

<!--
  Describe exactly how you tested this change:
  - Did you run `python main.py` end-to-end?
  - Which specific flows did you exercise?
  - Did you test edge cases (no active stream, expired token, empty banned word list, etc.)?
-->

- [ ] Ran `python main.py` locally — app launches without errors
- [ ] Tested the specific flow affected by this change end-to-end
- [ ] Tested relevant edge cases (describe below)

**Edge cases tested:**
<!-- List any specific edge cases you verified -->

---

## Screenshots / Recordings *(required for UI changes)*

<!-- 
  For any change that affects the UI, provide Before / After screenshots or a short screen recording.
  Drag and drop images directly into this text box on GitHub.
-->

| Before | After |
|--------|-------|
| *(screenshot)* | *(screenshot)* |

---

## Contributor Checklist

<!-- All items must be checked before this PR can be reviewed and merged -->

**Code Quality**
- [ ] My code follows the [style guide in `CONTRIBUTING.md`](CONTRIBUTING.md) (PEP 8, type hints, docstrings, `logger.error()`)
- [ ] All `asyncio.get_event_loop()` calls inside `async def` functions have been replaced with `asyncio.get_running_loop()`
- [ ] Error handling uses `logger.error()` — no bare `print()` calls for diagnostics
- [ ] No direct calls to `googleapiclient` from `main.py` — all YouTube API calls go through `youtube_engine.py`

**Security**
- [ ] I have **NOT** committed any credentials, API keys, tokens, or `client_secret.json` files
- [ ] I have **NOT** hardcoded any personal information, account IDs, or YouTube channel IDs
- [ ] No new plaintext credential storage has been introduced

**Documentation**
- [ ] I have updated `CHANGELOG.md` under the `[Unreleased]` section describing this change
- [ ] I have added or updated docstrings for all modified public classes and methods
- [ ] README or other documentation has been updated if the change affects user-facing behavior

**Dependencies**
- [ ] If I added a new `pip` dependency, it is listed in both `requirements.txt` and `pyproject.toml` with an appropriate minimum version bound
- [ ] No unnecessary dependencies have been added

---

## Breaking Changes *(if applicable)*

<!--
  If this is a breaking change, describe:
  - What existing behavior changes
  - What users / developers need to do to migrate
  - Whether any data migration is needed (e.g., settings.json schema changes, database migrations)
-->

N/A

---

## Additional Notes for Reviewers

<!-- Anything else you'd like the reviewer to know: design decisions, known limitations, follow-up issues, etc. -->
