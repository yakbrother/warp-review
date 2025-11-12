# Contributing to Warp Review

Thank you for considering contributing to Warp Review! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/warp-review.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit with clear messages
7. Push and create a Pull Request

## Development Setup

```bash
# Clone the repo
git clone https://github.com/yakbrother/warp-review.git
cd warp-review

# Install dependencies
pip install -r requirements.txt

# Install CLI for testing
./install.sh

# Test the CLI
warp-review status
```

## Code Style

This project follows these coding standards:

- **Python**: PEP 8 style guide
- **Clear naming**: Descriptive variable and function names
- **Documentation**: Docstrings for all functions and classes
- **Comments**: Explain why, not what
- **Type hints**: Use where beneficial

## Testing

Before submitting a PR:

```bash
# Check Python syntax
python -m py_compile pr_review_orchestrator.py
python -m py_compile warp-review

# Test CLI commands
warp-review --help
warp-review status
```

## What to Contribute

### Priority Areas

1. **New Agents** - Add specialized review agents
   - Performance analysis
   - API contract validation
   - Documentation completeness
   - Database migration safety

2. **CLI Improvements**
   - Additional commands
   - Better output formatting
   - Progress indicators
   - Config file support

3. **Integration** - Connect with other tools
   - GitHub Actions workflow
   - GitLab CI integration
   - Pre-commit hooks
   - IDE plugins

4. **Documentation**
   - Tutorial videos
   - Example projects
   - Best practices guide
   - Troubleshooting tips

### Agent Development

To add a new agent:

1. Add agent to `PRReviewOrchestrator.agents` list
2. Create `generate_<agent>_prompt()` method
3. Define what the agent should analyze
4. Update documentation

Example:
```python
def generate_performance_prompt(self):
    """Generate Performance Analysis prompt"""
    prev_output = self.load_agent_output('Engineering')
    context = prev_output['output'] if prev_output else ""
    
    return f"""# Performance Analysis

Context:
{context}

Analyze for:
- Time complexity of algorithms
- Memory usage patterns
- Database query optimization
- Caching opportunities
"""
```

## Pull Request Guidelines

### PR Title Format

Use conventional commits format:
- `feat: Add performance analysis agent`
- `fix: Correct git diff handling for renamed files`
- `docs: Update CLI usage guide`
- `refactor: Simplify agent prompt generation`
- `test: Add CLI integration tests`

### PR Description

Include:
1. **What** - What does this PR do?
2. **Why** - Why is this change needed?
3. **How** - How does it work?
4. **Testing** - How was it tested?
5. **Screenshots** - If UI changes

### Review Process

1. Automated checks must pass
2. Code review by maintainer
3. Address feedback
4. Approval and merge

## Coding Principles

Follow the project's core principles:

1. **Accessibility-first** - Always consider WCAG 2.1
2. **Test-focused** - Code should be testable
3. **Clear communication** - Prompts should be specific
4. **User-friendly** - CLI should be intuitive

## Communication

- **Issues**: For bug reports and feature requests
- **Discussions**: For questions and ideas
- **PRs**: For code contributions

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Welcome newcomers

## Questions?

- Check [README.md](README.md) for project overview
- Review [CLI_USAGE.md](CLI_USAGE.md) for CLI details
- Look at existing agents for examples
- Open an issue if stuck

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Acknowledgments

This project is a fork of [orchestrator-ollama](https://github.com/kliewerdaniel/orchestrator-ollama). Contributions should respect the original project's concepts and architecture.

---

Thank you for contributing to Warp Review! 🎉
