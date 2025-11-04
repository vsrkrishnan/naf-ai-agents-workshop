# GitHub Codespaces - LangGraph Workshop

Your cloud-based development environment for the LangGraph workshop is ready!

## ✅ What's Installed

- Python 3.11 with `uv` package manager
- All workshop dependencies (LangGraph, Jupyter, etc.)
- Virtual environment at `.venv/` (auto-activated)
- VS Code extensions for Python and Jupyter
- Git configured with notebook output stripping

## 🚀 Quickstart (2 minutes)

### Step 1: Configure API Key

```bash
# Copy template
cp .env.template .env

# Open in editor
code .env
```

Add your Anthropic API key:

```bash
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE
```

Save the file (Cmd+S / Ctrl+S).

### Step 2: Test Your Setup

```bash
make test-foundations-1
```

✅ If you see `✅ Foundations 01 complete`, you're ready!

## 📚 Workshop Notebooks

### Foundations Series (Generic LangGraph)

Located in: `notebooks/foundations/`

| Notebook | Time | Topics |
|----------|------|--------|
| 01 | 45 min | State & Graphs |
| 02 | 50 min | Conversational Agents |
| 03 | 55 min | Tools & ReAct |
| 04 | 60 min | Advanced Patterns |

### Firewall Workshop (PAN-OS Automation)

Located in: `notebooks/firewall_workshop/`

**Note**: All notebooks work in **mock mode** (no PAN-OS device needed).

| Notebook | Topics |
|----------|--------|
| 01 | Firewall State Workflows |
| 02 | Conversational Assistant |
| 03 | Tools & Security Audit |
| 04 | Production Patterns |

## 🛠️ Useful Commands

```bash
# Test individual notebooks
make test-foundations-1
make test-foundations-2
make test-firewall-1

# Test entire series
make test-foundations
make test-firewall

# Clean outputs
make clean

# See all commands
make help
```

## 🆘 Troubleshooting

**API Key Issues:**

```bash
# Check .env file exists
ls -la .env

# Verify key is set
cat .env | grep ANTHROPIC
```

**Module Not Found:**

- Rebuild container: Cmd/Ctrl+Shift+P → "Codespaces: Rebuild Container"

**Notebook Kernel Issues:**

- Select kernel: Click kernel name in top-right → Choose `.venv` Python

## 🎯 Next Steps

1. ✅ Configure `.env` with API key
2. ✅ Test setup: `make test-foundations-1`
3. 📖 Open `notebooks/foundations/01_state_and_graphs.ipynb`
4. 🎓 Work through notebooks in order

Happy learning! 🚀
