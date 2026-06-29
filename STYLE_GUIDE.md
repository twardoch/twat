<!-- this_file: STYLE_GUIDE.md -->
# Documentation style guide

How we write prose for `twat` — README, `src_docs/`, docstrings, and release
notes. Two rules carry the rest: **hook fast** and **show, don't gesture**.

## Hook fast

The first line earns the second. Open on the payoff, not the preamble.

- **Yes:** "`twat` does nothing on its own. Install plugins, and they snap into
  place."
- **No:** "This document describes the architecture and usage of the twat
  plugin host system, which is designed to..."

Cut throat-clearing — "In order to", "It should be noted that", "This section
will cover". Enter late, leave early: start in the middle of the useful part and
stop before re-explaining it. The reader's time is the budget.

## Show, don't gesture

Demonstrate with a runnable example before you describe in prose. A command the
reader can paste beats a paragraph about what the command would do.

- **Gesturing:** "The CLI supports listing installed plugins."
- **Showing:**

  ```console
  $ twat --list
  cache
  fs
  ```

Every claim about behaviour should be backed by code, a command, or output — not
an adjective. If you cannot show it, question whether it is true.

## Specifics

- **One idea per paragraph.** If a paragraph turns, split it.
- **Concrete over abstract.** "imports `twat_fs` and caches it in `sys.modules`"
  beats "handles the loading process efficiently".
- **No hype.** Drop "powerful", "seamless", "revolutionary", "blazing-fast".
  State what it does; let the reader judge.
- **Active voice, present tense.** "The host rewrites `sys.argv`", not "`sys.argv`
  is rewritten by the host".
- **Tables for matrices, prose for reasoning.** Use a table when comparing
  options or listing plugins; use sentences when explaining *why*.
- **Diagrams are Mermaid, never images.** Keep them in the repo as text so they
  diff and never go stale.
- **Code blocks are real.** Examples should run as written. Mark shell sessions
  with `console` and a `$` prompt; mark copy-paste commands with `bash`.
- **Honest skepticism over salesmanship.** Name the limitation and the trade-off
  rather than hiding it.

## Docstrings

Same spirit, scaled down. First line is a single imperative summary; then say
*why* and note the cost when it matters (e.g. "imports plugins, so slower than
`iter_plugins`"). Document the failure mode, not just the happy path.
