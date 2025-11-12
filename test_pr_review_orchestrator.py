#!/usr/bin/env python3
"""
Tests for PR Review Orchestrator

Run with: python -m pytest test_pr_review_orchestrator.py -v
Or: python test_pr_review_orchestrator.py
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import subprocess
import json

from pr_review_orchestrator import PRReviewOrchestrator


class TestPRReviewOrchestrator(unittest.TestCase):
    """Test PRReviewOrchestrator functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.orchestrator = PRReviewOrchestrator(self.test_dir)
    
    def tearDown(self):
        """Clean up test fixtures"""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def test_init(self):
        """Test orchestrator initialization"""
        self.assertIsNotNone(self.orchestrator)
        self.assertEqual(self.orchestrator.project_dir, Path(self.test_dir))
        self.assertEqual(len(self.orchestrator.agents), 4)
        self.assertIn('PRStatus', self.orchestrator.agents)
        self.assertIn('TestCoverage', self.orchestrator.agents)
        self.assertIn('Accessibility', self.orchestrator.agents)
        self.assertIn('FinalChecks', self.orchestrator.agents)
    
    def test_review_directory_created(self):
        """Test that review directory is created"""
        self.assertTrue(self.orchestrator.review_dir.exists())
        self.assertTrue(self.orchestrator.review_dir.is_dir())
    
    def test_save_and_load_agent_output(self):
        """Test saving and loading agent outputs"""
        test_output = "Test output content"
        agent_name = "TestAgent"
        
        # Save output
        self.orchestrator.save_agent_output(agent_name, test_output)
        
        # Load output
        loaded = self.orchestrator.load_agent_output(agent_name)
        
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded['agent'], agent_name)
        self.assertEqual(loaded['output'], test_output)
        self.assertIn('timestamp', loaded)
    
    def test_load_nonexistent_agent_output(self):
        """Test loading output for agent that hasn't run"""
        result = self.orchestrator.load_agent_output('NonexistentAgent')
        self.assertIsNone(result)
    
    def test_generate_pr_status_prompt(self):
        """Test PRStatus prompt generation"""
        prompt = self.orchestrator.generate_pr_status_prompt()
        
        self.assertIsInstance(prompt, str)
        self.assertIn('PR Status Check', prompt)
        self.assertIn('Current Branch', prompt)
        self.assertIn('Changed Files', prompt)
    
    def test_generate_test_coverage_prompt(self):
        """Test TestCoverage prompt generation"""
        prompt = self.orchestrator.generate_test_coverage_prompt()
        
        self.assertIsInstance(prompt, str)
        self.assertIn('Test Coverage Analysis', prompt)
        self.assertIn('Review Changed Code', prompt)
        self.assertIn('edge cases', prompt.lower())
    
    def test_generate_accessibility_prompt(self):
        """Test Accessibility prompt generation"""
        prompt = self.orchestrator.generate_accessibility_prompt()
        
        self.assertIsInstance(prompt, str)
        self.assertIn('Accessibility Review', prompt)
        self.assertIn('WCAG 2.1', prompt)
        self.assertIn('Semantic HTML', prompt)
    
    def test_generate_final_checks_prompt(self):
        """Test FinalChecks prompt generation"""
        prompt = self.orchestrator.generate_final_checks_prompt()
        
        self.assertIsInstance(prompt, str)
        self.assertIn('Final Pre-PR Checks', prompt)
        self.assertIn('Test Status Summary', prompt)
        self.assertIn('PR Readiness Assessment', prompt)
    
    def test_final_checks_uses_previous_outputs(self):
        """Test that FinalChecks prompt includes previous agent outputs"""
        # Save some agent outputs
        self.orchestrator.save_agent_output('PRStatus', 'PR status output')
        self.orchestrator.save_agent_output('TestCoverage', 'Test coverage output')
        
        prompt = self.orchestrator.generate_final_checks_prompt()
        
        self.assertIn('PRStatus', prompt)
        self.assertIn('TestCoverage', prompt)
        self.assertIn('PR status output', prompt)
        self.assertIn('Test coverage output', prompt)


class TestGitIntegration(unittest.TestCase):
    """Test git integration features"""
    
    def setUp(self):
        """Set up git test repository"""
        self.test_dir = tempfile.mkdtemp()
        self.orchestrator = PRReviewOrchestrator(self.test_dir)
        
        # Initialize git repo
        subprocess.run(['git', 'init'], cwd=self.test_dir, capture_output=True)
        subprocess.run(
            ['git', 'config', 'user.email', 'test@example.com'],
            cwd=self.test_dir,
            capture_output=True
        )
        subprocess.run(
            ['git', 'config', 'user.name', 'Test User'],
            cwd=self.test_dir,
            capture_output=True
        )
        subprocess.run(
            ['git', 'checkout', '-b', 'test-branch'],
            cwd=self.test_dir,
            capture_output=True
        )
    
    def tearDown(self):
        """Clean up test repository"""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def test_get_git_branch(self):
        """Test getting current git branch"""
        branch = self.orchestrator.get_git_branch()
        self.assertEqual(branch, 'test-branch')
    
    def test_get_changed_files_empty(self):
        """Test getting changed files when none exist"""
        files = self.orchestrator.get_changed_files()
        # May be empty or have an empty string depending on git state
        self.assertIsInstance(files, list)


class TestPromptContentQuality(unittest.TestCase):
    """Test that prompts contain expected quality indicators"""
    
    def setUp(self):
        """Set up orchestrator"""
        self.test_dir = tempfile.mkdtemp()
        self.orchestrator = PRReviewOrchestrator(self.test_dir)
    
    def tearDown(self):
        """Clean up"""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def test_pr_status_prompt_specificity(self):
        """Test PRStatus prompt has specific instructions"""
        prompt = self.orchestrator.generate_pr_status_prompt()
        
        # Should have specific file paths
        self.assertIn(str(self.orchestrator.review_dir), prompt)
        self.assertIn('prstatus_output.txt', prompt)
        
        # Should have concrete deliverables
        self.assertIn('PR URL', prompt)
        self.assertIn('Risk assessment', prompt)
    
    def test_test_coverage_prompt_structure(self):
        """Test TestCoverage prompt has structured format"""
        prompt = self.orchestrator.generate_test_coverage_prompt()
        
        # Should have clear sections
        self.assertIn('### 1.', prompt)
        self.assertIn('### 2.', prompt)
        self.assertIn('### 3.', prompt)
        
        # Should specify priorities
        self.assertIn('Critical', prompt)
        self.assertIn('Important', prompt)
    
    def test_accessibility_prompt_wcag_criteria(self):
        """Test Accessibility prompt references WCAG criteria"""
        prompt = self.orchestrator.generate_accessibility_prompt()
        
        # Should reference specific WCAG elements
        self.assertIn('4.5:1', prompt)  # Contrast ratio
        self.assertIn('3:1', prompt)    # Large text contrast
        self.assertIn('ARIA', prompt)
        self.assertIn('keyboard', prompt.lower())
    
    def test_prompts_save_to_correct_locations(self):
        """Test all prompts reference correct output locations"""
        prompts = {
            'PRStatus': self.orchestrator.generate_pr_status_prompt(),
            'TestCoverage': self.orchestrator.generate_test_coverage_prompt(),
            'Accessibility': self.orchestrator.generate_accessibility_prompt(),
            'FinalChecks': self.orchestrator.generate_final_checks_prompt()
        }
        
        for agent_name, prompt in prompts.items():
            expected_file = f"{agent_name.lower()}_output.txt"
            self.assertIn(expected_file, prompt.lower(),
                         f"{agent_name} prompt should reference {expected_file}")


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def test_orchestrator_with_nonexistent_directory(self):
        """Test creating orchestrator requires parent directory to exist"""
        test_path = Path(tempfile.gettempdir()) / 'nonexistent_test_dir'
        
        # Ensure it doesn't exist
        if test_path.exists():
            shutil.rmtree(test_path)
        
        # Create the parent directory first (orchestrator only creates .pr_review)
        test_path.mkdir(parents=True, exist_ok=True)
        
        orchestrator = PRReviewOrchestrator(str(test_path))
        
        # Review directory should be created
        self.assertTrue(orchestrator.review_dir.exists())
        
        # Cleanup
        if test_path.exists():
            shutil.rmtree(test_path)
    
    def test_multiple_save_load_cycles(self):
        """Test multiple save/load cycles work correctly"""
        test_dir = tempfile.mkdtemp()
        orchestrator = PRReviewOrchestrator(test_dir)
        
        # Save multiple times
        for i in range(3):
            orchestrator.save_agent_output('TestAgent', f'Output {i}')
        
        # Load should get the last one
        result = orchestrator.load_agent_output('TestAgent')
        self.assertEqual(result['output'], 'Output 2')
        
        # Cleanup
        shutil.rmtree(test_dir)


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPRReviewOrchestrator))
    suite.addTests(loader.loadTestsFromTestCase(TestGitIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestPromptContentQuality))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
