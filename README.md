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

### Install the CLI (optional but recommended)

```bash
./install.sh
```

This creates a symlink to `~/.local/bin/warp-review` so you can run it from anywhere.

### Usage

```bash
# Run the full review
warp-review run
# or: python pr_review_orchestrator.py

# Check PR status
warp-review status

# Generate specific agent prompt
warp-review agent test

# View results
warp-review view final
```

See [QUICKSTART_PR_REVIEW.md](QUICKSTART_PR_REVIEW.md) for detailed instructions.

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

```bash
# 1. Make your changes
git checkout -b feature/new-component
# ... make changes ...
git commit -m "Add new component"

# 2. Run Warp Review
python pr_review_orchestrator.py

# 3. Process agents through Warp
# Each agent generates a specialized prompt
# You process it through Warp Agent Mode
# Save the analysis for the next agent

# 4. Address findings
# - Add missing tests
# - Fix accessibility issues
# - Update documentation

# 5. Submit PR with generated description
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
