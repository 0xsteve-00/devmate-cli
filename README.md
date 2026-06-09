<p align="center">
  <h1 align="center">🤖 devmate</h1>
  <p align="center"><strong>Your AI Dev Companion in the Terminal</strong></p>
  <p align="center">Smart commit messages & natural language shell commands — powered by AI.</p>
</p>

<p align="center">
  <a href="https://pypi.org/project/devmate-cli/"><img src="https://img.shields.io/pypi/v/devmate-cli?color=blue" alt="PyPI"></a>
  <a href="https://pypi.org/project/devmate-cli/"><img src="https://img.shields.io/pypi/pyversions/devmate-cli" alt="Python"></a>
  <a href="https://github.com/achmadyosifa/devmate-cli/blob/main/LICENSE"><img src="https://img.shields.io/github/license/achmadyosifa/devmate-cli" alt="License"></a>
</p>

---

## ✨ Features

### 📝 `devmate commit` — AI Commit Messages
Automatically generate meaningful commit messages from your `git diff`. No more "fix stuff" commits.

```bash
$ devmate commit
```

```
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

### ⚡ `devmate shell` — Natural Language → Shell Commands
Describe what you want in plain English (or any language), get the exact command.

```bash
$ devmate shell "find all Python files modified in the last 24 hours"
```

```
╭──────────── ⚡ Command ────────────╮
│ find . -name "*.py" -mtime -1      │
╰────────────────────────────────────╯
What do you want to do? [run/copy/explain/cancel]:
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

devmate uses [litellm](https://github.com/BerriAI/litellm) under the hood, so it supports 100+ models:

| Provider | Model Example | Env Variable |
|----------|--------------|--------------|
| OpenAI | `gpt-4o-mini` | `OPENAI_API_KEY` |
| Anthropic | `claude-sonnet-4-20250514` | `ANTHROPIC_API_KEY` |
| Groq | `groq/llama3-70b-8192` | `GROQ_API_KEY` |
| Ollama (local) | `ollama/llama3` | — (free!) |
| And many more... | | |

---

## 📖 Usage

### Commit Messages

```bash
# Generate from staged changes
devmate commit

# Stage everything and commit
devmate commit --all

# Use a specific style
devmate commit --style simple
devmate commit --style conventional   # (default)
devmate commit --style detailed
```

### Shell Commands

```bash
# Translate to command (interactive)
devmate shell "compress all images in current folder"

# Translate and execute immediately
devmate shell -e "show top 10 largest files"

# Works in any language!
devmate shell "cari file lebih dari 100mb"
```

### Configuration

```bash
# Create config file
devmate init           # in current directory
devmate init --global  # in home directory (~/.devmate.yaml)
```

#### `.devmate.yaml`

```yaml
# API key (or use environment variables)
api_key: sk-...

# AI model
model: gpt-4o-mini

# Commit settings
commit:
  style: conventional   # conventional | simple | detailed
  language: en
  max_length: 72

# Shell settings
shell:
  safety: true          # confirm before dangerous commands
  os_context: true      # send OS info for better commands
```

---

## 🔒 Safety

- **Dangerous command detection**: Commands like `rm -rf`, `mkfs`, etc. trigger a warning
- **No auto-execute by default**: You always see the command before running it
- **Your API key stays local**: Never stored anywhere except your config or env

---

## 🗺️ Roadmap

- [ ] `devmate review` — AI code review before push
- [ ] `devmate explain <file>` — Explain any code file
- [ ] `devmate test` — Generate unit tests
- [ ] Shell command history & favorites
- [ ] Plugin system
- [ ] Interactive TUI mode

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/awesome`)
3. Make your changes
4. Run tests (`pytest`)
5. Submit a PR

---

## 📄 License

MIT © [Achmad Yosifa](https://github.com/achmadyosifa)

---

<p align="center">
  <sub>Built with ❤️ and AI</sub>
</p>
