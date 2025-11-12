#!/usr/bin/env python3
"""
PR Review Orchestrator for Warp

Forked from: https://github.com/kliewerdaniel/orchestrator-ollama
Original concept: Multi-agent orchestration using directed graphs

This fork specializes in pre-PR review workflow:
1. PR Status & Change Analysis
2. Test Coverage Review
3. Accessibility Compliance (WCAG 2.1)
4. Final Checks & Recommendations

Designed to run interactively in Warp's Agent Mode.
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime


class PRReviewOrchestrator:
    """
    Orchestrates PR review workflow through specialized agents.
    Generates prompts for Warp's Agent Mode to process.
    """
    
    def __init__(self, project_dir="."):
        self.project_dir = Path(project_dir)
        self.review_dir = self.project_dir / ".pr_review"
        self.review_dir.mkdir(exist_ok=True)
        
        self.agents = [
            'PRStatus',
            'TestCoverage',
            'Accessibility',
            'FinalChecks'
        ]
        
    def get_git_branch(self):
        """Get current git branch"""
        try:
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True,
                text=True,
                cwd=self.project_dir
            )
            return result.stdout.strip()
        except Exception as e:
            print(f"Error getting git branch: {e}")
            return None
    
    def get_git_diff(self):
        """Get diff against main/master branch"""
        try:
            # Try main first, then master
            for base_branch in ['main', 'master']:
                result = subprocess.run(
                    ['git', 'diff', f'{base_branch}...HEAD'],
                    capture_output=True,
                    text=True,
                    cwd=self.project_dir
                )
                if result.returncode == 0 and result.stdout:
                    return result.stdout
            return None
        except Exception as e:
            print(f"Error getting git diff: {e}")
            return None
    
    def get_changed_files(self):
        """Get list of changed files"""
        try:
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'HEAD', 'origin/main'],
                capture_output=True,
                text=True,
                cwd=self.project_dir
            )
            if result.returncode != 0:
                # Try master if main doesn't exist
                result = subprocess.run(
                    ['git', 'diff', '--name-only', 'HEAD', 'origin/master'],
                    capture_output=True,
                    text=True,
                    cwd=self.project_dir
                )
            return result.stdout.strip().split('\n') if result.stdout else []
        except Exception as e:
            print(f"Error getting changed files: {e}")
            return []
    
    def save_agent_output(self, agent_name, output):
        """Save agent output"""
        output_file = self.review_dir / f"{agent_name.lower()}_output.json"
        with open(output_file, 'w') as f:
            json.dump({
                'agent': agent_name,
                'timestamp': datetime.now().isoformat(),
                'output': output
            }, f, indent=2)
    
    def load_agent_output(self, agent_name):
        """Load previous agent output"""
        output_file = self.review_dir / f"{agent_name.lower()}_output.json"
        if output_file.exists():
            with open(output_file, 'r') as f:
                return json.load(f)
        return None
    
    def generate_pr_status_prompt(self):
        """Generate PR Status Check prompt"""
        branch = self.get_git_branch()
        changed_files = self.get_changed_files()
        
        return f"""# PR Status Check

**Current Branch:** {branch}

**Changed Files:**
{chr(10).join(f'- {f}' for f in changed_files) if changed_files else '(Unable to detect changes)'}

## Your Task

1. **Check if a PR exists** for branch `{branch}`
   - Use: `gh pr view` or `gh pr list --head {branch}`
   - If no PR exists, ask if the user wants to create one

2. **Summarize the scope of changes:**
   - How many files modified?
   - What types of changes? (features, fixes, refactoring, docs)
   - Which areas of the codebase are affected?

3. **Identify the change categories:**
   - New functionality
   - Modified functionality  
   - Bug fixes
   - UI/UX changes
   - Documentation only
   - Configuration changes

4. **Output your findings** to: {self.review_dir}/prstatus_output.txt

Include:
- PR URL (if exists) or recommendation to create one
- Files changed count and breakdown
- Summary of what changed and why (based on commits/diff)
- Risk assessment (low/medium/high complexity)
"""
    
    def generate_test_coverage_prompt(self):
        """Generate Test Coverage Analysis prompt"""
        pr_status = self.load_agent_output('PRStatus')
        context = pr_status['output'] if pr_status else "See .pr_review/prstatus_output.txt"
        
        return f"""# Test Coverage Analysis

**Previous Analysis:**
{context}

## Your Task

Analyze the PR changes and identify test coverage gaps:

### 1. Review Changed Code
For each changed file, identify:
- **New functionality** that requires unit tests
- **Modified functionality** where existing tests need updates  
- **Edge cases and error handling** that should be tested
- **Integration points** that may need integration tests

### 2. For Each Gap, Provide:
```
File: [path/to/file]
Function/Method: [name]
Test Type: [unit/integration/e2e]
Test Location: [path/to/test/file]

What to Test:
- [Specific behavior or functionality]
- [Edge cases to cover]
- [Error conditions to handle]

Why Important:
- [Risk if untested]
- [Impact on system]
```

### 3. Prioritization
Rank test gaps by priority:
- **Critical:** Core functionality, user-facing features, security-sensitive code
- **Important:** Business logic, data transformations, API integrations
- **Nice-to-have:** Helper functions, formatting, minor utilities

### 4. Output
Save your findings to: {self.review_dir}/testcoverage_output.txt

Include:
- Total gaps identified
- Breakdown by priority
- Specific test requirements for each gap
- Suggested test approach (mocking, fixtures, test data needed)
"""
    
    def generate_accessibility_prompt(self):
        """Generate Accessibility Review prompt"""
        test_coverage = self.load_agent_output('TestCoverage')
        context = test_coverage['output'] if test_coverage else "See .pr_review/testcoverage_output.txt"
        
        return f"""# Accessibility Review (WCAG 2.1)

**Previous Analysis:**
{context}

## Your Task

**Only perform this review if UI changes were detected.**

If no UI changes, simply note: "No UI changes detected - skipping accessibility review"

### For UI Changes, Check:

#### 1. Semantic HTML
- Are proper HTML5 semantic elements used? (nav, main, article, section, etc.)
- Are headings in logical order (h1 → h2 → h3)?
- Are lists, buttons, and links using correct elements?

#### 2. ARIA Attributes
- Are ARIA labels provided where needed?
- Are roles, states, and properties correctly used?
- Are live regions configured for dynamic content?

#### 3. Keyboard Navigation
- Are all interactive elements keyboard accessible?
- Is focus order logical?
- Are focus indicators visible?
- Can modals/dialogs be closed with Escape?

#### 4. Color Contrast
- Does text meet WCAG 2.1 AA contrast ratios?
  - Normal text: 4.5:1
  - Large text: 3:1
- Are colors not the only means of conveying information?

#### 5. Focus Management
- Is focus trapped in modals?
- Does focus return appropriately after interactions?
- Are focus outlines visible and clear?

### Output
Save to: {self.review_dir}/accessibility_output.txt

For each issue found:
```
File: [path]
Line: [line number]
Issue: [description]
WCAG Criterion: [e.g., 1.3.1, 2.1.1, etc.]
Severity: [Critical/Important/Minor]
Recommendation: [how to fix]
```

Also suggest accessibility tests if needed (e.g., axe-core, jest-axe).
"""
    
    def generate_final_checks_prompt(self):
        """Generate Final Checks prompt"""
        # Gather all previous outputs
        outputs = []
        for agent in ['PRStatus', 'TestCoverage', 'Accessibility']:
            output = self.load_agent_output(agent)
            if output:
                outputs.append(f"### {agent} ###\n{output['output']}")
        
        all_context = "\n\n".join(outputs)
        
        return f"""# Final Pre-PR Checks

**All Previous Analysis:**
{all_context}

## Your Task

Provide a comprehensive pre-PR checklist and recommendations:

### 1. Test Status Summary
- How many test gaps were identified?
- How many have been addressed?
- Are there any critical gaps remaining?

**Ask the user:** "Would you like me to create the remaining tests one at a time?"

### 2. Accessibility Status
- Were any WCAG issues found?
- Have they been addressed?
- Are accessibility tests in place?

### 3. Code Quality Reminders
Check that the user has:
- [ ] Run linter (what command?)
- [ ] Run formatter (what command?)
- [ ] Run full test suite (what command?)
- [ ] Updated documentation if needed
- [ ] Reviewed commit messages for clarity

### 4. PR Readiness Assessment
Rate the PR readiness:
- **Ready to submit** - All checks passed, tests created, no blockers
- **Minor fixes needed** - Small issues to address
- **Significant work needed** - Test gaps or accessibility issues remain

### 5. Action Items
Provide a numbered list of remaining tasks before PR submission.

### 6. Suggested PR Description Template
Generate a PR description including:
- What changed and why
- Testing performed
- Accessibility considerations (if applicable)
- Screenshots (if UI changes)
- Breaking changes (if any)

### Output
Save to: {self.review_dir}/finalchecks_output.txt

End with: "Ready to submit PR? (y/n)"
"""
    
    def run_review(self):
        """Run the PR review workflow"""
        print("=== PR Review Orchestrator ===")
        print(f"Branch: {self.get_git_branch()}")
        print(f"Review directory: {self.review_dir}\n")
        print("=" * 60)
        
        prompts = {
            'PRStatus': self.generate_pr_status_prompt(),
            'TestCoverage': self.generate_test_coverage_prompt(),
            'Accessibility': self.generate_accessibility_prompt(),
            'FinalChecks': self.generate_final_checks_prompt()
        }
        
        for agent_name in self.agents:
            print(f"\n### {agent_name} Agent ###\n")
            
            prompt = prompts[agent_name]
            prompt_file = self.review_dir / f"{agent_name.lower()}_prompt.txt"
            
            with open(prompt_file, 'w') as f:
                f.write(prompt)
            
            print(f"Prompt saved to: {prompt_file}")
            print("\nNext steps:")
            print(f"1. Read prompt: cat {prompt_file}")
            print("2. Process through Warp Agent Mode")
            print(f"3. Save output to: {self.review_dir}/{agent_name.lower()}_output.txt")
            print("\nPress Enter when ready to continue...")
            
            input()
            
            # Load output if exists
            output_file = self.review_dir / f"{agent_name.lower()}_output.txt"
            if output_file.exists():
                with open(output_file, 'r') as f:
                    output = f.read()
                self.save_agent_output(agent_name, output)
                print("✓ Output loaded")
            else:
                print("⚠ No output file found, continuing...")
        
        print("\n" + "=" * 60)
        print("\n✨ PR Review Complete!")
        print(f"\nAll analysis saved in: {self.review_dir}")
        print(f"\nFinal checklist: {self.review_dir}/finalchecks_output.txt")


def main():
    orchestrator = PRReviewOrchestrator()
    orchestrator.run_review()


if __name__ == "__main__":
    main()
