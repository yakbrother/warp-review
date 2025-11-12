# Coding Standards for Warp Review

This document outlines the coding standards and best practices for contributing to Warp Review.

## Core Principles

### Communication & Code Quality
- Always verify information before presenting it. Do not make assumptions or speculate without clear evidence.
- Make changes file by file and give users a chance to spot mistakes.
- Never use apologies.
- **Always think of accessibility (WCAG 2.2 compliance).**
- Avoid giving feedback about understanding in comments or documentation.

### Code Changes & Documentation
- Don't suggest whitespace changes.
- Don't summarize changes made unless requested.
- Don't use emojis in code documentation or PRs.
- Don't invent changes other than what's explicitly requested.
- Don't remove unrelated code or functionalities.
- Provide all edits in a single chunk instead of multiple-step instructions.
- Always provide links to real files, not context-generated files.

## Code Quality Standards

### Naming & Clarity
- **Prefer descriptive, explicit variable names** over short, ambiguous ones.
- Variables, functions, and classes should reveal their purpose.
- Avoid abbreviations unless universally understood.
- Use meaningful names that explain why something exists and how it's used.

### Architecture & Structure
- Keep functions small and single-purpose.
- Each function should do exactly one thing.
- Prefer composition over inheritance.
- Use early returns to avoid deep nesting.
- Extract complex logic into well-named functions.

### Security (Non-Negotiable)
- Always consider security implications when modifying code.
- **Never commit secrets or API keys.**
- Validate and sanitize all user input.
- Use prepared statements for database queries (N/A for warp-review).
- Implement proper authentication and authorization checks.

### Error Handling
- Implement robust error handling and logging where necessary.
- Handle errors at the beginning of functions (guard clauses).
- Return early for error conditions.
- Use specific exception types, not generic exceptions.
- Log errors with sufficient context.

### Testing (Required)
- **Suggest or include appropriate unit tests** for new or modified code.
- Write tests for business logic and user workflows.
- Test behavior, not implementation details.
- Include edge cases and error scenarios.
- Keep tests maintainable and readable.

### Performance
- When suggesting changes, consider and prioritize code performance.
- Avoid premature optimization - measure first.
- Check for N+1 problems in loops.
- Use appropriate data structures (maps/sets vs arrays).

### Clean Code Practices

#### Constants Over Magic Numbers
- Replace hard-coded values with named constants.
- Use descriptive constant names that explain the value's purpose.
- Keep constants at the top of the file or in a dedicated constants file.

#### Comments & Documentation
- Don't comment on what code does - make code self-documenting.
- Use comments to explain **why** something is done a certain way.
- Document APIs, complex algorithms, and non-obvious side effects.
- Document complex business logic.

#### DRY (Don't Repeat Yourself)
- Extract repeated code into reusable functions.
- Share common logic through proper abstraction.
- Maintain single sources of truth.

#### Code Organization
- Keep related code together.
- Organize code in a logical hierarchy.
- Use consistent file and folder naming conventions.
- Hide implementation details (encapsulation).
- Expose clear interfaces.

## Python-Specific Standards

### Type Hints & Declarations
- Use type hints for function parameters and return values.
- Enable strict type checking where possible.
- Use `typing` module for complex types.

### Code Style
- Follow PEP 8 style guide.
- Use docstrings for all public functions and classes.
- Prefer f-strings over `.format()` or `%` formatting.
- Use list/dict comprehensions where they improve readability.

### Best Practices
- Use `pathlib.Path` instead of `os.path` for file operations.
- Use context managers (`with` statements) for resource management.
- Prefer `subprocess.run()` over deprecated alternatives.
- Use `json.load()`/`json.dump()` for JSON operations.

## Git & Version Control

### Commit Messages
- Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`
- Keep messages under 72 characters.
- Be descriptive: what and why, not how.
- Make small, focused commits.

### Branch Naming
- Use meaningful branch names.
- Follow pattern: `feature/description`, `fix/bug-name`, `docs/what-changed`

## Accessibility Standards

Warp Review is built on accessibility-first principles:

### WCAG 2.2 Compliance
- Use semantic HTML elements where applicable.
- Provide text alternatives for non-text content.
- Ensure sufficient color contrast (4.5:1 for normal text, 3:1 for large text).
- Support keyboard navigation for all interactive elements.
- Maintain proper heading hierarchy.

### Implementation
- Generate prompts that check for accessibility issues.
- Include ARIA labels where needed.
- Focus indicators must be visible.
- Test with accessibility in mind.

## Edge Cases & Validation

### Always Consider
- Handle empty inputs (empty strings, arrays, null, undefined).
- Test boundary values (min/max, overflow, negative numbers, zero).
- Validate special characters in strings.
- Handle timezone issues in date/time operations.
- Check for floating-point precision issues.
- Ensure cross-platform compatibility.

### Assertions
- **Include assertions wherever possible** to validate assumptions.
- Use assertions to catch potential errors early.
- Document why assertions are important for the logic.

## Testing Requirements

### Test Coverage
- Unit tests for all core functionality.
- Integration tests for git operations.
- Edge case tests (null, empty, boundary values).
- Error case tests to verify error handling.

### Test Quality
- Test assertions must be meaningful.
- Mock data should be realistic.
- Test descriptions should clearly explain what's being tested.
- Tests must be deterministic (no flaky tests).
- Tests should be isolated (no dependencies on each other).

## Code Review Checklist

Before submitting code:
- [ ] All tests pass.
- [ ] Code follows style guidelines.
- [ ] No security vulnerabilities.
- [ ] Error handling is comprehensive.
- [ ] Edge cases are handled.
- [ ] Documentation is updated.
- [ ] Commit message is clear.
- [ ] No magic numbers (use named constants).
- [ ] Variable names are descriptive.
- [ ] Functions are small and single-purpose.

## Workflow

### When Implementing Features
1. Clarify requirements if anything is vague.
2. Point out potential issues or better approaches.
3. Write or update tests first (TDD when appropriate).
4. Implement the feature.
5. Run tests and linters.
6. Commit with a clear commit message.

### When Fixing Bugs
1. Understand the root cause before coding.
2. Write a failing test that reproduces the bug.
3. Fix the issue.
4. Verify the test passes.
5. Check for similar issues elsewhere.

## What to Push Back On

Contributors should raise concerns about:
- Security vulnerabilities.
- Accessibility violations.
- Performance red flags.
- Code that will be hard to maintain.
- Missing error handling.
- Breaking changes without migration plan.
- Reinventing the wheel when good libraries exist.

## Project-Specific Rules

### Prompt Generation
- Prompts must be specific and actionable.
- Include concrete deliverables.
- Reference correct file paths.
- Provide structured format.

### Git Integration
- Handle both main and master branches.
- Gracefully handle missing remotes.
- Provide clear error messages.

### CLI Design
- Commands should be intuitive.
- Provide helpful error messages.
- Include examples in help text.
- Support common shortcuts.

## Dependencies

- Avoid adding heavy dependencies without discussion.
- Keep requirements.txt lean.
- Consider if stdlib can do the job.
- Update dependencies regularly but test thoroughly.

## Documentation Standards

- Keep README.md updated.
- Document complex business logic.
- Add docstrings for public APIs.
- Use comments sparingly - code should be self-documenting.
- Update WARP.md when adding new features.

## Final Notes

- **Quality over speed** - get it right.
- **Working code over perfect code** - ship it.
- **User experience matters** - make it intuitive.
- **Accessibility is not optional** - build it in.
- **Security is not negotiable** - validate everything.
- **Testing is required** - prove it works.

---

*These standards are based on industry best practices and adapted for the Warp Review project.*
