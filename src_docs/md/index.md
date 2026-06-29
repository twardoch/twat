<!-- this_file: src_docs/md/index.md -->
# twat

`twat` does nothing on its own. Install plugins, and they snap into place.

It is a minimal plugin **host**: a zero-config namespace that discovers
`twat-*` packages through standard Python entry points, loads them on demand,
and dispatches their CLIs through one command.

```python
import twat

# `pip install twat-fs` registered itself as the "fs" plugin
files = twat.fs.list_directory(".")

# `pip install twat-cache` registered as "cache"
@twat.cache.memoize()
def expensive():
    ...
```

```bash
pip install twat            # the empty host
pip install twat-fs twat-os # plugins snap in
twat --list                 # fs  os
twat fs list /tmp           # dispatch to the fs plugin
```

## Why a host?

Each tool stays a small, independently versioned package you install only when
you need it. The host adds the connective tissue: a shared namespace
(`twat.<plugin>`), a single dispatcher (`twat <plugin> …`), shell completion
for every installed command, and health checks — without importing a single
plugin until you actually use it.

## Where to next

- **[Architecture](01-architecture.md)** — how entry points turn `twat.fs`
  into a live module, with a diagram of the load path.
- **[Writing a plugin](02-plugin-authoring.md)** — the one line of config that
  makes any package a `twat` plugin.
- **[CLI & shell completion](03-cli-and-completions.md)** — `--list`,
  `--available`, `--doctor`, and `twat-<TAB>` setup per shell.
- **[The plugins](04-plugins.md)** — the full table of `twat-*` packages.
