<p align="center">
  <h1 align="center">🤖 devmate</h1>
  <p align="center"><strong>Your AI Dev Companion in the Terminal</strong></p>
  <p align="center">Smart commits, code review, shell translation, test generation, docs & refactoring — all powered by AI.</p>
</p>

<p align="center">
  <a href="https://pypi.org/project/devmate-cli/"><img src="https://img.shields.io/pypi/v/devmate-cli?color=blue" alt="PyPI"></a>
  <a href="https://pypi.org/project/devmate-cli/"><img src="https://img.shields.io/pypi/pyversions/devmate-cli" alt="Python"></a>
  <a href="https://github.com/0xsteve-00/devmate-cli/blob/main/LICENSE"><img src="https://img.shields.io/github/license/0xsteve-00/devmate-cli" alt="License"></a>
</p>

---

## ✨ Features

| Command | Description |
|---------|-------------|
| `devmate commit` | 📝 AI-generated commit messages from your diff |
| `devmate shell` | ⚡ Natural language → shell commands |
| `devmate review` | 🔍 AI code review with severity ratings |
| `devmate explain` | 💡 Explain any code file in plain language |
| `devmate test` | 🧪 Auto-generate pytest unit tests |
| `devmate doc` | 📄 Auto-generate docstrings & documentation |
| `devmate refactor` | ♻️ Get refactoring suggestions with before/after |

---

### 📝 `devmate commit` — AI Commit Messages

```bash
$ devmate commit
╭──────── 📝 Commit Message ────────╮
│ feat(auth): add JWT token refresh  │
│ endpoint                           │
╰────────────────────────────────────╯
What do you want to do? [commit/edit/regenerate/cancel]:
```

### ⚡ `devmate shell` — Natural Language → Shell

```bash
$ devmate shell "find all Python files modified in the last 24 hours"
╭──────────── ⚡ Command ────────────╮
│ find . -name "*.py" -mtime -1      │
╰────────────────────────────────────╯
What do you want to do? [run/copy/explain/cancel]:
```

### 🔍 `devmate review` — AI Code Review

```bash
$ devmate review                    # review staged changes
$ devmate review src/app.py         # review specific file
```

### 💡 `devmate explain` — Understand Any Code

```bash
$ devmate explain src/auth.py
$ devmate explain utils.py -f parse_config   # specific function
```

### 🧪 `devmate test` — Generate Unit Tests

```bash
$ devmate test src/utils.py                   # auto-save to tests/
$ devmate test app.py -o tests/test_app.py    # custom output
```

### 📄 `devmate doc` — Generate Documentation

```bash
$ devmate doc src/utils.py                    # overwrite with docstrings
$ devmate doc app.py -o app_documented.py     # save to new file
```

### ♻️ `devmate refactor` — Refactoring Suggestions

```bash
$ devmate refactor src/app.py
```

---

## 🚀 Installation

```bash
pip install devmate-cli
```

### Set up your API key

```bash
# Option 1: Environment variable (recommended)
export OPENAI_API_KEY=sk-...

# Option 2: Config file
devmate init --global
# Then edit ~/.devmate.yaml
```

### Supported AI Providers

devmate uses [litellm](https://github.com/BerriAI/litellm) under the hood, supporting 100+ models:

| Provider | Model Example | Env Variable |
|----------|--------------|--------------|
| OpenAI | `gpt-4o-mini` | `OPENAI_API_KEY` |
| Anthropic | `claude-sonnet-4-20250514` | `ANTHROPIC_API_KEY` |
| Groq | `groq/llama3-70b-8192` | `GROQ_API_KEY` |
| Ollama (local) | `ollama/llama3` | — (free!) |

---

## 📖 Full Usage

```bash
# Commit
devmate commit                    # from staged changes
devmate commit --all              # stage everything first
devmate commit -s simple          # simple | conventional | detailed

# Shell
devmate shell "compress all images"
devmate shell -e "show disk usage"   # auto-execute

# Review
devmate review                    # staged changes
devmate review src/app.py         # specific files

# Explain
devmate explain src/auth.py
devmate explain utils.py -f my_function

# Test
devmate test src/utils.py
devmate test app.py -o tests/test_app.py

# Doc
devmate doc src/utils.py
devmate doc app.py -o app_doc.py

# Refactor
devmate refactor src/app.py

# Config
devmate init                      # local config
devmate init --global             # global config
```

### `.devmate.yaml`

```yaml
api_key: sk-...
model: gpt-4o-mini

commit:
  style: conventional    # conventional | simple | detailed
  language: en
  max_length: 72

shell:
  safety: true           # confirm before dangerous commands
```

---

## 🔒 Safety

- **Dangerous command detection** — `rm -rf`, `mkfs`, etc. trigger a warning
- **No auto-execute by default** — You always review before running
- **API key stays local** — Never stored except in your config or env

---

## 🗺️ Roadmap

- [ ] `devmate chat` — Interactive AI chat in terminal
- [ ] Shell command history & favorites
- [ ] Plugin system
- [ ] Interactive TUI mode
- [ ] VS Code extension

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/awesome`)
3. Make changes & run tests (`pytest`)
4. Submit a PR

---

## 📄 License

MIT © [Achmad Yosifa](https://github.com/0xsteve-00)

---

<p align="center">
  <sub>Built with ❤️ and AI</sub>
</p>
