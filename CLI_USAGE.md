# Warp Review CLI Usage

The `warp-review` CLI provides convenient commands for running PR reviews.

## Installation

```bash
# From the warp-review directory
./install.sh
```

This creates a symlink in `~/.local/bin/warp-review` so you can run it from anywhere.

If `~/.local/bin` is not in your PATH, add this to your `~/.zshrc`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Commands

### `warp-review run`

Run the full PR review workflow interactively.

```bash
warp-review run

# Or from a different directory
warp-review run -d ~/projects/my-app
```

This is equivalent to running `python pr_review_orchestrator.py`.

### `warp-review status`

Check the current branch and changed files.

```bash
warp-review status
```

Example output:
```
Branch: feature/new-component
Changed files: 5

Files:
  - src/components/Button.tsx
  - src/components/Button.test.tsx
  - src/styles/button.css
  - docs/components.md
  - package.json

Existing review found: 2 agent(s) completed
```

### `warp-review agent <name>`

Generate a prompt for a specific agent without running the full workflow.

```bash
# Generate PRStatus prompt
warp-review agent prstatus

# Generate and display TestCoverage prompt
warp-review agent test --show

# Shortcuts available
warp-review agent pr        # PRStatus
warp-review agent test      # TestCoverage
warp-review agent a11y      # Accessibility
warp-review agent final     # FinalChecks
```

### `warp-review view <agent>`

View an agent's output or prompt.

```bash
# View FinalChecks output
warp-review view final

# View TestCoverage prompt
warp-review view test --prompt

# View any agent
warp-review view prstatus
warp-review view accessibility
```

### `warp-review clean`

Clean up the `.pr_review/` directory.

```bash
warp-review clean
```

Useful for starting fresh or removing old review data.

## Examples

### Quick Status Check

```bash
warp-review status
```

### Generate Single Agent Prompt

```bash
# Just need test coverage analysis
warp-review agent test --show
```

### View Previous Review

```bash
# Check what the final checklist said
warp-review view final
```

### Full Workflow

```bash
# Run complete review
warp-review run

# For each agent:
# 1. Process prompt through Warp Agent Mode
# 2. Save output to .pr_review/<agent>_output.txt
# 3. Press Enter to continue

# View final results
warp-review view final
```

### Review Different Project

```bash
cd ~
warp-review status -d ~/projects/my-app
warp-review run -d ~/projects/my-app
```

## Agent Names

Use any of these formats:

| Full Name | Shortcuts |
|-----------|-----------|
| prstatus | pr |
| testcoverage | test |
| accessibility | a11y, access |
| finalchecks | final |

## Workflow Integration

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-push

warp-review status
read -p "Run PR review? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    warp-review run
fi
```

### Alias in ~/.zshrc

```bash
alias wr='warp-review'
alias wrs='warp-review status'
alias wrr='warp-review run'
```

Then use:
```bash
wr status
wrr  # Run review
```

## Tips

- Run `warp-review status` before starting work to see what changed
- Use `warp-review agent <name>` to regenerate specific prompts after making changes
- `warp-review view final` is quick way to check your PR checklist
- Use `warp-review clean` before running a fresh review
