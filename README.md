# Warp Review

A Warp-native PR review orchestrator for comprehensive pre-submission code review.

**Forked from:** [orchestrator-ollama](https://github.com/kliewerdaniel/orchestrator-ollama) by @kliewerdaniel

## What is Warp Review?

Warp Review is a multi-agent orchestration system designed to help you review PRs before submission. It analyzes your changes through 4 specialized agents:

1. **PRStatus** - Analyzes your branch and changed files
2. **TestCoverage** - Identifies test gaps and requirements  
3. **Accessibility** - Verifies WCAG 2.1 compliance for UI changes
4. **FinalChecks** - Generates comprehensive pre-submission checklist

## Quick Start

### 1. Install the CLI (one-time setup)

```bash
cd ~/Sites/warp-review  # or wherever you cloned this repo
./install.sh
```

This creates a symlink to `~/.local/bin/warp-review` so you can run it from **any project**.

### 2. Use it on Any Project

```bash
# Go to your project
cd ~/Sites/my-project

# Run warp-review
warp-review run
```

That's it! Warp-review analyzes your current branch and changed files.

### Usage Examples

```bash
# Full review workflow
cd ~/Sites/my-app
warp-review run

# Quick status check
warp-review status

# Generate specific agent
warp-review agent test

# View final checklist
warp-review view final

# Use from anywhere with -d flag
warp-review run -d ~/Sites/another-project
```

See [QUICKSTART_PR_REVIEW.md](QUICKSTART_PR_REVIEW.md) for detailed instructions.

## Works with Any Project

Warp Review is **language and framework agnostic**. It works with:

- ✅ **Any git repository** - Analyzes your branch and changes
- ✅ **Any language** - JavaScript, Python, PHP, Go, Rust, etc.
- ✅ **Any framework** - React, Django, Laravel, Next.js, etc.
- ✅ **Multiple projects** - Use the same CLI everywhere

Just install once, then use it on any project you're working on.

## Why Warp Review?

- **Accessibility-first** - WCAG 2.1 compliance built-in
- **Test-focused** - Identifies gaps before they become issues
- **Interactive** - Work with Warp's Agent Mode for intelligent review
- **Comprehensive** - Covers code quality, testing, and accessibility

## Documentation

- **[CLI_QUICK_REFERENCE.md](CLI_QUICK_REFERENCE.md)** - CLI commands cheat sheet
- **[CLI_USAGE.md](CLI_USAGE.md)** - Detailed CLI usage guide
- **[QUICKSTART_PR_REVIEW.md](QUICKSTART_PR_REVIEW.md)** - Get started in 5 minutes
- **[README_PR_REVIEW.md](README_PR_REVIEW.md)** - Full documentation and workflow
- **[PR_REVIEW_SUMMARY.md](PR_REVIEW_SUMMARY.md)** - What changed from original
- **[WARP.md](WARP.md)** - Warp-specific guidance

## Example Workflow

### On Any Project

```bash
# Navigate to your project (any project!)
cd ~/Sites/my-app

# Create a feature branch
git checkout -b feature/new-component

# Make your changes
# ... code code code ...

# Commit your work
git add .
git commit -m "Add new component"

# Run warp-review
warp-review run

# Follow the prompts for each agent:
# 1. PRStatus - Reviews your changes
# 2. TestCoverage - Identifies test gaps  
# 3. Accessibility - Checks WCAG compliance
# 4. FinalChecks - Comprehensive checklist

# View final results
warp-review view final

# Address any issues found
# - Write missing tests
# - Fix accessibility issues
# - Update documentation

# Submit your PR with confidence!
gh pr create
```

### On Multiple Projects

```bash
# Review different projects without changing directories
warp-review status -d ~/Sites/project-1
warp-review status -d ~/Sites/project-2
warp-review run -d ~/Sites/project-3
```

## Output Structure

```
.pr_review/
├── prstatus_prompt.txt          # Generated prompts
├── prstatus_output.txt          # Your analysis
├── testcoverage_prompt.txt
├── testcoverage_output.txt
├── accessibility_prompt.txt
├── accessibility_output.txt
├── finalchecks_prompt.txt
└── finalchecks_output.txt       # Final checklist
```

## Requirements

- Python 3.8+
- git
- gh CLI (optional, for PR operations)

```bash
pip install -r requirements.txt
```

## Testing

Warp Review includes a comprehensive test suite:

```bash
# Run tests
python test_pr_review_orchestrator.py

# Or with pytest (if installed)
python -m pytest test_pr_review_orchestrator.py -v
```

The test suite covers:
- Orchestrator initialization
- Agent prompt generation
- Git integration
- Save/load functionality
- WCAG 2.1 compliance checks
- Edge cases and error handling

## Philosophy

Warp Review embodies:
- **Accessibility-first development** (WCAG 2.1)
- **Test-driven practices** (comprehensive coverage)
- **Code quality standards** (linting, formatting)
- **Thoughtful reviews** (clear descriptions, no surprises)

## Original Project

This is a specialized fork of [orchestrator-ollama](https://github.com/kliewerdaniel/orchestrator-ollama).

**What changed:**
- Renamed from Orchestrator-Ollama to warp-review
- Adapted for PR review instead of product development
- Uses Warp Agent Mode instead of local Ollama
- Focused on 4 specialized review agents
- Added git integration for real change analysis

The original Ollama-based orchestrator files remain in this repo for reference:
- `README_ORIGINAL.md` - Original project documentation
- `main.py` and `agents/` - Original orchestrator code

## Credits

Original concept and architecture: [orchestrator-ollama](https://github.com/kliewerdaniel/orchestrator-ollama) by @kliewerdaniel

## License

Maintains original license from orchestrator-ollama project.
