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

## 🎯 What is devmate?

**devmate** is a CLI tool that brings AI directly into your development workflow — no browser, no copy-pasting into ChatGPT, no context switching.

Instead of leaving your terminal to ask AI for help, devmate gives you **8 commands** that handle the most common AI-assisted tasks right where you code:

- **Tired of writing "fix stuff" commits?** → `devmate commit` analyzes your diff and generates proper conventional commit messages.
- **Can't remember the `find` or `tar` syntax?** → `devmate shell "find large files"` gives you the exact command.
- **Want a second pair of eyes on your code?** → `devmate review` catches bugs, security issues, and anti-patterns before you push.
- **Onboarding onto a new codebase?** → `devmate explain src/auth.py` breaks down what the code does in plain language.
- **Hate writing tests?** → `devmate test src/utils.py` generates ready-to-run pytest tests with edge cases covered.
- **Undocumented code everywhere?** → `devmate doc src/app.py` adds Google-style docstrings to every function.
- **Code smells but not sure where?** → `devmate refactor src/app.py` gives before/after suggestions with impact ratings.

All of this works with **100+ AI models** (OpenAI, Anthropic, Groq, Ollama) — including free local models.

---

## ✨ Commands

| Command | What It Does |
|---------|-------------|
| `devmate commit` | 📝 Reads your `git diff`, generates a meaningful commit message (conventional/simple/detailed), lets you commit, edit, or regenerate |
| `devmate shell` | ⚡ Converts plain English (or any language) to the exact shell command you need, with optional auto-execute and safety checks |
| `devmate review` | 🔍 Reviews your staged changes or specific files for bugs, security issues, performance problems, and best practice violations |
| `devmate explain` | 💡 Explains a code file (or a specific function) in plain language — great for unfamiliar codebases |
| `devmate test` | 🧪 Generates comprehensive pytest unit tests with happy paths, edge cases, error handling, and mocking |
| `devmate doc` | 📄 Adds Google-style docstrings to all public classes and functions in a file |
| `devmate refactor` | ♻️ Analyzes code and suggests refactoring improvements with before/after code, rated by impact |
| `devmate init` | ⚙️ Creates a `.devmate.yaml` config file for your project or globally |

---

## 🚀 Quick Start

```bash
# Install
pip install devmate-cli

# Set your API key
export OPENAI_API_KEY=sk-...

# Start using
devmate commit --all          # AI commit message
devmate shell "list open ports"   # natural language → command
devmate review src/app.py     # AI code review
```

---

## 📖 Usage Examples

### 📝 Commit — Never write "fix stuff" again

```bash
$ devmate commit
╭──────── 📝 Commit Message ────────╮
│ feat(auth): add JWT token refresh  │
│ endpoint                           │
│                                    │
│ - Add /auth/refresh POST endpoint  │
│ - Implement token rotation logic   │
│ - Add 7-day refresh token expiry   │
╰────────────────────────────────────╯
What do you want to do? [commit/edit/regenerate/cancel]:
```

```bash
devmate commit                    # from staged changes
devmate commit --all              # stage everything first
devmate commit -s simple          # simple | conventional | detailed
```

### ⚡ Shell — Stop Googling commands

```bash
$ devmate shell "find all Python files modified in the last 24 hours"
╭──────────── ⚡ Command ────────────╮
│ find . -name "*.py" -mtime -1      │
╰────────────────────────────────────╯
What do you want to do? [run/copy/explain/cancel]:
```

```bash
devmate shell "compress all images"
devmate shell -e "show disk usage"       # auto-execute
devmate shell "cari file lebih dari 100mb"   # works in any language!
```

### 🔍 Review — Catch bugs before they ship

```bash
$ devmate review                    # review staged changes
$ devmate review src/app.py         # review a specific file

# Output: severity-rated feedback
# 🔴 Critical: SQL injection in line 42
# 🟡 Warning: Unused variable `temp` in line 15
# 🟢 Suggestion: Consider using list comprehension
# ✅ Good: Error handling is solid
```

### 💡 Explain — Understand any codebase fast

```bash
$ devmate explain src/auth.py
$ devmate explain utils.py -f parse_config   # explain one function
```

### 🧪 Test — Auto-generate pytest tests

```bash
$ devmate test src/utils.py                   # saves to tests/test_utils.py
$ devmate test app.py -o tests/test_app.py    # custom output path
```

### 📄 Doc — Add docstrings everywhere

```bash
$ devmate doc src/utils.py                    # overwrite with docstrings
$ devmate doc app.py -o app_documented.py     # save to a new file
```

### ♻️ Refactor — Improve code quality

```bash
$ devmate refactor src/app.py

# Output: rated suggestions with before/after code
# 🔴 High Impact: Extract duplicated auth logic into decorator
# 🟡 Medium: Replace nested ifs with early returns
# 🟢 Low: Use f-strings instead of .format()
```

---

## ⚙️ Configuration

```bash
devmate init                      # create .devmate.yaml (local)
devmate init --global             # create ~/.devmate.yaml (global)
```

### `.devmate.yaml`

```yaml
# API key (or use environment variables)
api_key: sk-...

# AI model (any litellm-supported model)
model: gpt-4o-mini

# Commit settings
commit:
  style: conventional   # conventional | simple | detailed
  language: en          # commit message language
  max_length: 72        # subject line max length

# Shell settings
shell:
  safety: true          # confirm before dangerous commands
```

### Supported Providers

| Provider | Model Example | Env Variable |
|----------|--------------|--------------|
| OpenAI | `gpt-4o-mini` | `OPENAI_API_KEY` |
| Anthropic | `claude-sonnet-4-20250514` | `ANTHROPIC_API_KEY` |
| Groq | `groq/llama3-70b-8192` | `GROQ_API_KEY` |
| Ollama (local) | `ollama/llama3` | — (free!) |
| + 100 more via [litellm](https://github.com/BerriAI/litellm) | | |

---

## 🔒 Safety

- **Dangerous command detection** — `rm -rf`, `mkfs`, `dd`, etc. trigger a warning
- **No auto-execute by default** — You always review commands before running
- **API keys stay local** — Only stored in your env or config file, never sent anywhere except your chosen AI provider

---

## 🗺️ Roadmap

- [ ] `devmate chat` — Interactive AI chat in terminal
- [ ] Shell command history & favorites
- [ ] Plugin system for custom commands
- [ ] Interactive TUI mode
- [ ] VS Code extension

---

## 🤝 Contributing

Contributions welcome! Open an issue or submit a PR.

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/awesome`)
3. Make changes & run tests (`pytest`)
4. Submit a PR

---

## 📄 License

MIT License

---

## ⭐ Support

If you find devmate useful, give it a star! It helps others discover the project and motivates us to keep improving.

<p align="center">
  <a href="https://github.com/0xsteve-00/devmate-cli/stargazers">
    <img src="https://img.shields.io/github/stars/0xsteve-00/devmate-cli?style=social" alt="GitHub Stars">
  </a>
</p>

<p align="center">
  <a href="https://github.com/0xsteve-00/devmate-cli">⭐ Star devmate on GitHub</a>
</p>

---

<p align="center">
  <sub>Built with ❤️ and AI</sub>
</p>
