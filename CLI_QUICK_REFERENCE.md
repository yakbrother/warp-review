# Warp Review CLI - Quick Reference

## Installation

```bash
./install.sh
```

## Essential Commands

```bash
warp-review run              # Run full review
warp-review status           # Check branch/changes
warp-review agent <name>     # Generate agent prompt
warp-review view <agent>     # View agent output
warp-review clean            # Clean review directory
```

## Agent Shortcuts

| Command | Agent |
|---------|-------|
| `warp-review agent pr` | PRStatus |
| `warp-review agent test` | TestCoverage |
| `warp-review agent a11y` | Accessibility |
| `warp-review agent final` | FinalChecks |

## Common Workflows

### Full Review
```bash
warp-review run
# Process each agent through Warp
warp-review view final
```

### Quick Check
```bash
warp-review status
```

### Specific Agent Only
```bash
warp-review agent test --show
# Process through Warp
# Save to .pr_review/testcoverage_output.txt
warp-review view test
```

### Re-run After Changes
```bash
warp-review clean
warp-review agent test
```

## Flags

```bash
-d, --dir DIR    # Run in different directory
--show           # Display prompt after generating (agent command)
--prompt         # View prompt instead of output (view command)
```

## Examples

```bash
# From different directory
warp-review status -d ~/projects/my-app

# Generate and show prompt
warp-review agent test --show

# View prompt instead of output
warp-review view test --prompt

# Full help
warp-review --help
warp-review agent --help
```

## Aliases (Add to ~/.zshrc)

```bash
alias wr='warp-review'
alias wrs='warp-review status'
alias wrr='warp-review run'
alias wrt='warp-review agent test'
alias wrf='warp-review view final'
```

Then use:
```bash
wrs           # Check status
wrr           # Run review
wrt --show    # Test coverage
wrf           # View final checklist
```
