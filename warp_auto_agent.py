#!/usr/bin/env python3
"""
Automated Warp Agent Processor

Generates agent prompts and instructions for running through Warp Agent Mode.
Can be used to batch-process all agents or run them one at a time.
"""

import json
import sys
from pathlib import Path
from datetime import datetime


class WarpAgentProcessor:
    """Generates specialized prompts for Warp Agent Mode processing"""
    
    def __init__(self, workflow_dir=".warp_workflow"):
        self.workflow_dir = Path(workflow_dir)
        self.workflow_dir.mkdir(exist_ok=True)
        
    def get_agent_context(self, agent_name):
        """Load previous agent outputs for context"""
        context_files = {
            'Design': 'product_management_output.txt',
            'Engineering': 'design_output.txt',
            'Testing': 'engineering_output.txt',
            'Security': 'testing_output.txt',
            'DevOps': 'security_output.txt',
            'Final': 'devops_output.txt'
        }
        
        if agent_name not in context_files:
            return None
            
        context_file = self.workflow_dir / context_files[agent_name]
        if context_file.exists():
            with open(context_file, 'r') as f:
                return f.read()
        return None
    
    def generate_agent_prompt(self, agent_name, initial_message, include_context=True):
        """Generate a prompt for a specific agent"""
        
        if agent_name == "ProductManagement":
            return f"""Act as an experienced product manager. Expand on this idea:

{initial_message}

Create comprehensive product requirements including:
- User personas
- User stories with acceptance criteria  
- Feature prioritization (MoSCoW)
- Success metrics and KPIs
- Timeline recommendations"""

        elif agent_name == "Design":
            context = self.get_agent_context('Design') if include_context else initial_message
            return f"""Act as a UI/UX designer. Create design specifications:

Context:
{context or initial_message}

Provide:
- User flows
- Wireframe descriptions
- Component library specs
- Design system (colors, typography)
- Accessibility guidelines"""

        elif agent_name == "Engineering":
            context = self.get_agent_context('Engineering') if include_context else initial_message
            return f"""Act as a senior software engineer. Create technical specs:

Context:
{context or initial_message}

Provide:
- System architecture
- Technology stack recommendations
- Database schema
- API specifications
- Development setup"""

        elif agent_name == "Testing":
            context = self.get_agent_context('Testing') if include_context else initial_message
            return f"""Act as a QA engineer. Create testing strategy:

Context:
{context or initial_message}

Provide:
- Test pyramid strategy
- Critical test scenarios
- Testing tools recommendations
- Automation approach
- Performance criteria"""

        elif agent_name == "Security":
            context = self.get_agent_context('Security') if include_context else initial_message
            return f"""Act as a security engineer. Provide security analysis:

Context:
{context or initial_message}

Provide:
- Threat model (STRIDE)
- Auth/authz strategy
- Data encryption requirements
- Security testing approach
- Compliance considerations"""

        elif agent_name == "DevOps":
            context = self.get_agent_context('DevOps') if include_context else initial_message
            return f"""Act as a DevOps engineer. Create infrastructure specs:

Context:
{context or initial_message}

Provide:
- Infrastructure architecture
- CI/CD pipeline design
- Containerization strategy
- Monitoring and logging
- Scaling strategy"""

        elif agent_name == "Final":
            # Gather all outputs
            outputs = []
            for agent in ['ProductManagement', 'Design', 'Engineering', 'Testing', 'Security', 'DevOps']:
                output_file = self.workflow_dir / f"{agent.lower()}_output.txt"
                if output_file.exists():
                    with open(output_file, 'r') as f:
                        outputs.append(f"### {agent} ###\n{f.read()}")
            
            all_context = "\n\n".join(outputs)
            return f"""Act as a technical project manager. Provide comprehensive project summary:

All Agent Outputs:
{all_context}

Provide:
- Executive summary
- Completeness assessment
- Integration points
- Risk assessment
- Next steps
- Team structure recommendations
- Timeline estimate"""

        return ""

    def generate_all_prompts(self, initial_prompt_file="initial_prompt.json"):
        """Generate prompts for all agents"""
        
        # Load initial prompt
        with open(initial_prompt_file, 'r') as f:
            initial_data = json.load(f)
            initial_message = initial_data.get('message', '')
        
        agents = ['ProductManagement', 'Design', 'Engineering', 'Testing', 'Security', 'DevOps', 'Final']
        
        print(f"Generating prompts for all agents...")
        print(f"Initial message: {initial_message}\n")
        
        for agent in agents:
            prompt = self.generate_agent_prompt(agent, initial_message)
            prompt_file = self.workflow_dir / f"{agent.lower()}_prompt.txt"
            
            with open(prompt_file, 'w') as f:
                f.write(prompt)
            
            print(f"✓ Generated: {prompt_file}")
        
        print(f"\nAll prompts generated in: {self.workflow_dir}")
        print("\nNext steps:")
        print("1. Run each prompt through Warp Agent Mode")
        print("2. Save outputs to corresponding *_output.txt files")
        print("3. Use the output files as context for subsequent agents")

    def print_workflow_instructions(self):
        """Print detailed workflow instructions"""
        print("""
=== Warp-Native Orchestrator Workflow ===

This workflow uses Warp's Agent Mode to process specialized agent prompts.

WORKFLOW STEPS:

1. Generate prompts:
   python warp_auto_agent.py generate

2. For each agent (in order):
   a. Read the prompt from .warp_workflow/{agent}_prompt.txt
   b. Run it in Warp Agent Mode
   c. Copy the response
   d. Save to .warp_workflow/{agent}_output.txt

3. Agent order:
   ProductManagement → Design → Engineering → Testing → Security → DevOps → Final

4. Each agent uses the previous agent's output as context

EXAMPLE USAGE:

# In Warp Agent Mode, paste prompt:
cat .warp_workflow/productmanagement_prompt.txt

# Save response to:
# .warp_workflow/productmanagement_output.txt

# Repeat for each agent

TIPS:
- Process agents in order for best results
- Each output becomes context for the next agent
- The Final agent consolidates all outputs
- Save all outputs for reference
""")


def main():
    """Main CLI interface"""
    processor = WarpAgentProcessor()
    
    if len(sys.argv) < 2:
        print("Usage: python warp_auto_agent.py [generate|help]")
        print("\nCommands:")
        print("  generate  - Generate all agent prompts")
        print("  help      - Show detailed workflow instructions")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "generate":
        processor.generate_all_prompts()
    elif command == "help":
        processor.print_workflow_instructions()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
