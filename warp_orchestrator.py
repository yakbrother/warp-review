#!/usr/bin/env python3
"""
Warp-Native Tech Company Orchestrator

This orchestrator leverages Warp's Agent Mode to process prompts through
specialized agents interactively. Instead of making API calls, it generates
prompts for the user to run through Warp's Agent Mode.
"""

import json
import os
from pathlib import Path
from datetime import datetime
import networkx as nx


class WarpOrchestrator:
    """
    Orchestrates multi-agent workflow using Warp's Agent Mode.
    Generates specialized prompts for each agent that the user runs through Warp.
    """
    
    def __init__(self, project_dir="."):
        self.project_dir = Path(project_dir)
        self.workflow_dir = self.project_dir / ".warp_workflow"
        self.workflow_dir.mkdir(exist_ok=True)
        
        # Agent configuration
        self.agents = [
            'ProductManagement',
            'Design', 
            'Engineering',
            'Testing',
            'Security',
            'DevOps',
            'Final'
        ]
        
        # Create directed graph
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(self.agents)
        self.graph.add_edges_from([
            ('ProductManagement', 'Design'),
            ('Design', 'Engineering'),
            ('Engineering', 'Testing'),
            ('Testing', 'Security'),
            ('Security', 'DevOps'),
            ('DevOps', 'Final')
        ])
    
    def load_initial_prompt(self):
        """Load the initial prompt from initial_prompt.json"""
        prompt_file = self.project_dir / "initial_prompt.json"
        
        if not prompt_file.exists():
            print(f"Error: {prompt_file} not found")
            return None
            
        with open(prompt_file, 'r') as f:
            return json.load(f)
    
    def save_agent_output(self, agent_name, output):
        """Save output from an agent to workflow directory"""
        output_file = self.workflow_dir / f"{agent_name.lower()}_output.json"
        
        with open(output_file, 'w') as f:
            json.dump({
                'agent': agent_name,
                'timestamp': datetime.now().isoformat(),
                'output': output
            }, f, indent=2)
    
    def load_agent_output(self, agent_name):
        """Load output from a previous agent"""
        output_file = self.workflow_dir / f"{agent_name.lower()}_output.json"
        
        if not output_file.exists():
            return None
            
        with open(output_file, 'r') as f:
            return json.load(f)
    
    def get_agent_prompt(self, agent_name, context):
        """Generate a specialized prompt for Warp Agent Mode"""
        prompts = {
            'ProductManagement': self._product_management_prompt(context),
            'Design': self._design_prompt(context),
            'Engineering': self._engineering_prompt(context),
            'Testing': self._testing_prompt(context),
            'Security': self._security_prompt(context),
            'DevOps': self._devops_prompt(context),
            'Final': self._final_prompt(context)
        }
        
        return prompts.get(agent_name, "")
    
    def _product_management_prompt(self, context):
        message = context.get('message', '')
        return f"""Act as an experienced product manager. Expand on this idea with comprehensive product requirements:

Initial Idea: {message}

Provide:
- User personas and key stakeholders
- Detailed user stories with acceptance criteria
- Feature prioritization (MoSCoW method)
- Success metrics and KPIs
- Technical and business constraints
- Timeline and milestone recommendations

Save your response to: {self.workflow_dir}/product_management_output.txt"""
    
    def _design_prompt(self, context):
        prev_output = self.load_agent_output('ProductManagement')
        requirements = prev_output['output'] if prev_output else context.get('message', '')
        
        return f"""Act as a UI/UX designer. Create comprehensive design specifications based on these requirements:

Requirements:
{requirements}

Provide:
- User flow diagrams (describe the flows)
- High-level wireframe descriptions for key screens
- Component library specification
- Design system guidelines (colors, typography, spacing)
- Accessibility considerations
- Mobile/responsive design approach

Save your response to: {self.workflow_dir}/design_output.txt"""
    
    def _engineering_prompt(self, context):
        prev_output = self.load_agent_output('Design')
        design_specs = prev_output['output'] if prev_output else context.get('message', '')
        
        return f"""Act as a senior software engineer. Create technical implementation specifications:

Design Specifications:
{design_specs}

Provide:
- System architecture diagram (describe components)
- Technology stack recommendations with justification
- Database schema design
- API endpoint specifications
- Key algorithms and data structures
- Code organization and module structure
- Development environment setup
- Third-party integrations needed

Save your response to: {self.workflow_dir}/engineering_output.txt"""
    
    def _testing_prompt(self, context):
        prev_output = self.load_agent_output('Engineering')
        tech_specs = prev_output['output'] if prev_output else context.get('message', '')
        
        return f"""Act as a QA engineer. Create a comprehensive testing strategy:

Technical Specifications:
{tech_specs}

Provide:
- Test pyramid strategy (unit, integration, e2e percentages)
- Critical test scenarios with test cases
- Testing tools and frameworks recommendation
- Automated testing approach
- Performance testing criteria
- Browser/device compatibility matrix
- Bug tracking and reporting process

Save your response to: {self.workflow_dir}/testing_output.txt"""
    
    def _security_prompt(self, context):
        prev_output = self.load_agent_output('Testing')
        test_specs = prev_output['output'] if prev_output else context.get('message', '')
        
        return f"""Act as a security engineer. Perform security analysis and provide recommendations:

System Context:
{test_specs}

Provide:
- Security threat model (STRIDE analysis)
- Authentication and authorization strategy
- Data encryption requirements (at rest and in transit)
- Input validation and sanitization requirements
- Security headers and CORS configuration
- Dependency vulnerability scanning approach
- Security testing recommendations
- Compliance considerations (GDPR, SOC2, etc.)

Save your response to: {self.workflow_dir}/security_output.txt"""
    
    def _devops_prompt(self, context):
        prev_output = self.load_agent_output('Security')
        security_specs = prev_output['output'] if prev_output else context.get('message', '')
        
        return f"""Act as a DevOps engineer. Create deployment and infrastructure specifications:

Security Requirements:
{security_specs}

Provide:
- Infrastructure architecture (cloud provider, services)
- CI/CD pipeline design
- Containerization strategy (Docker/Kubernetes)
- Environment configuration (dev, staging, prod)
- Monitoring and logging setup
- Backup and disaster recovery plan
- Scaling strategy
- Cost optimization recommendations

Save your response to: {self.workflow_dir}/devops_output.txt"""
    
    def _final_prompt(self, context):
        # Gather all agent outputs
        outputs = []
        for agent in self.agents[:-1]:  # Exclude 'Final'
            output = self.load_agent_output(agent)
            if output:
                outputs.append(f"\n### {agent} Output ###\n{output['output']}")
        
        all_outputs = "\n".join(outputs)
        
        return f"""Act as a technical project manager. Review all agent outputs and provide a comprehensive project summary:

All Agent Outputs:
{all_outputs}

Provide:
- Executive summary
- Completeness assessment (what's covered, what's missing)
- Integration points between components
- Risk assessment and mitigation strategies
- Next steps and action items
- Recommended team structure and roles
- Estimated timeline and resources

Save your response to: {self.workflow_dir}/final_output.txt"""
    
    def run_interactive_workflow(self):
        """Run the workflow interactively through Warp"""
        print("=== Warp-Native Tech Company Orchestrator ===\n")
        
        # Load initial prompt
        initial_context = self.load_initial_prompt()
        if not initial_context:
            return
        
        print(f"Initial prompt loaded: {initial_context['message']}\n")
        print(f"Workflow directory: {self.workflow_dir}\n")
        print("=" * 60)
        
        # Process each agent in topological order
        for agent_name in nx.topological_sort(self.graph):
            print(f"\n### {agent_name} Agent ###\n")
            
            # Generate the prompt
            prompt = self.get_agent_prompt(agent_name, initial_context)
            
            # Save prompt to file
            prompt_file = self.workflow_dir / f"{agent_name.lower()}_prompt.txt"
            with open(prompt_file, 'w') as f:
                f.write(prompt)
            
            print(f"Prompt saved to: {prompt_file}")
            print("\nTo process this agent:")
            print(f"1. Copy the prompt from: {prompt_file}")
            print("2. Run it through Warp's Agent Mode")
            print(f"3. Save the output to: {self.workflow_dir}/{agent_name.lower()}_output.txt")
            print("4. Press Enter when ready to continue to next agent...")
            
            # Wait for user
            input()
            
            # Try to load the output
            output_file = self.workflow_dir / f"{agent_name.lower()}_output.txt"
            if output_file.exists():
                with open(output_file, 'r') as f:
                    output = f.read()
                self.save_agent_output(agent_name, output)
                print(f"✓ Output loaded successfully")
            else:
                print(f"⚠ Warning: Output file not found at {output_file}")
                print("Continuing anyway...")
        
        print("\n" + "=" * 60)
        print("\n✨ Workflow complete!")
        print(f"\nAll outputs saved in: {self.workflow_dir}")
        print("\nTo generate a consolidated report, check:")
        print(f"  {self.workflow_dir}/final_output.txt")


def main():
    """Main entry point"""
    orchestrator = WarpOrchestrator()
    orchestrator.run_interactive_workflow()


if __name__ == "__main__":
    main()
