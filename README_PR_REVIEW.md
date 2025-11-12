# Warp Review

**Forked from:** [orchestrator-ollama](https://github.com/kliewerdaniel/orchestrator-ollama) by @kliewerdaniel

A Warp-native PR review orchestrator that adapts the original multi-agent orchestration concept for pre-PR code review workflow.

## What Changed From Original

The original project simulated a tech company workflow (Product → Design → Engineering → Testing → Security → DevOps) using Ollama models. This fork:

- **Specializes in PR review workflow** instead of product development
- **Integrates with git** to analyze actual code changes
- **Focuses on 4 specialized agents:**
  1. **PRStatus** - Analyze PR and changed files
  2. **TestCoverage** - Identify test gaps and requirements
  3. **Accessibility** - WCAG 2.1 compliance review
  4. **FinalChecks** - Comprehensive pre-submission checklist

- **Designed for Warp Agent Mode** - generates prompts for interactive processing
- **Adheres to accessibility-first development** principles

## Credit

Original concept and architecture: [orchestrator-ollama](https://github.com/kliewerdaniel/orchestrator-ollama)

The directed graph orchestration pattern and agent-based workflow design are from the original project.

## Quick Start

```bash
# Run the PR review orchestrator
python pr_review_orchestrator.py
```

The script will:
1. Analyze your current git branch and changes
2. Generate specialized prompts for each review agent
3. Guide you through processing each agent via Warp
4. Compile a comprehensive pre-PR checklist

## Workflow

### 1. PR Status Check
- Checks if PR exists for current branch
- Analyzes changed files and scope
- Categorizes changes (features, fixes, UI, etc.)
- Provides risk assessment

### 2. Test Coverage Analysis
- Reviews changed code for test gaps
- Identifies:
  - New functionality needing tests
  - Modified functionality needing test updates
  - Edge cases and error handling
  - Integration points
- Prioritizes gaps (Critical/Important/Nice-to-have)
- Provides specific test requirements

### 3. Accessibility Review
- **Only runs if UI changes detected**
- Checks WCAG 2.1 compliance:
  - Semantic HTML
  - ARIA attributes
  - Keyboard navigation
  - Color contrast
  - Focus management
- Suggests accessibility tests (axe-core, jest-axe)

### 4. Final Checks
- Summarizes test status
- Offers to create tests interactively
- Provides code quality checklist:
  - Linter
  - Formatter
  - Test suite
  - Documentation
  - Commit messages
- Generates PR readiness assessment
- Provides action items
- Suggests PR description template

## Requirements

```bash
pip install -r requirements.txt
```

Dependencies:
- Python 3.8+
- git
- gh CLI (optional, for PR operations)

## Output

All analysis is saved in `.pr_review/`:
```
.pr_review/
├── prstatus_prompt.txt
├── prstatus_output.txt
├── testcoverage_prompt.txt
├── testcoverage_output.txt
├── accessibility_prompt.txt
├── accessibility_output.txt
├── finalchecks_prompt.txt
└── finalchecks_output.txt
```

## Usage Tips

1. **Run before creating PR** - catch issues early
2. **Process agents in order** - each builds on previous analysis
3. **Save outputs to txt files** - agents use previous outputs as context
4. **Use in Warp Agent Mode** - designed for interactive review
5. **Iterate as needed** - re-run specific agents after fixes

## Example Workflow

```bash
# 1. Make your code changes
git checkout -b feature/new-component

# 2. Commit changes
git add .
git commit -m "Add new component"

# 3. Run PR review
python pr_review_orchestrator.py

# 4. Process each agent prompt through Warp
# 5. Address identified issues
# 6. Create PR with generated description
```

## Philosophy

This tool embodies:
- **Accessibility-first** development (WCAG 2.1 compliance)
- **Test-driven** practices (comprehensive coverage)
- **Code quality** standards (linting, formatting)
- **Thoughtful PR reviews** (clear descriptions, no surprises)

## Original Project

For the original multi-agent orchestration system with Ollama:
- Repository: https://github.com/kliewerdaniel/orchestrator-ollama
- Use case: Simulating tech company workflow from idea to deployment
- Agents: ProductManagement, Design, Engineering, Testing, Security, DevOps

## License

Maintains original license from orchestrator-ollama project.
