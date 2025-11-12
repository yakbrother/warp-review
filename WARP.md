# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This repository contains two orchestration systems:

### 1. Original: Tech Company Orchestrator (Ollama-based)
Simulates a tech company workflow (Product Management → Design → Engineering → Testing → Security → DevOps) using locally hosted Ollama models. Agents communicate via directed graph (NetworkX) to generate code, specifications, and documentation.

### 2. Warp Review (Warp-native)
**Primary tool for this repository.** Specialized pre-PR review workflow for Warp's Agent Mode:
- **PRStatus**: Analyze branch and changed files
- **TestCoverage**: Identify test gaps and requirements
- **Accessibility**: WCAG 2.1 compliance review
- **FinalChecks**: Comprehensive pre-submission checklist

Designed for interactive use with Warp's Agent Mode.

## Essential Commands

### Warp Review (Primary)
```bash
# Install CLI (optional but recommended)
./install.sh

# Run PR review workflow
warp-review run
# or: python pr_review_orchestrator.py

# Quick commands
warp-review status                  # Check branch and changes
warp-review agent test              # Generate specific agent prompt
warp-review view final              # View final checklist
warp-review clean                   # Clean review directory

# View generated prompts
cat .pr_review/prstatus_prompt.txt
warp-review view test --prompt      # Or use CLI

# View analysis results
warp-review view final
cat .pr_review/finalchecks_output.txt
```

### Original Ollama Orchestrator
```bash
# Install dependencies
pip install -r requirements.txt

# Verify Ollama is running (required for original version)
curl http://localhost:11434/api/generate

# Run the orchestrator with initial_prompt.json
python main.py

# View outputs
cat output.txt          # Intermediate outputs after each agent
cat final_output.txt    # Final comprehensive output
```

### Development
```bash
# No tests are currently defined in this project

# Check Python syntax
python -m py_compile main.py
python -m py_compile agents/*.py
```

## Architecture

### Core Components

**main.py**: Entry point that orchestrates the agent workflow
- Reads `initial_prompt.json` (structure: `{message, code, readme}`)
- Creates a directed graph of agents using NetworkX
- Processes prompts through agents in topological order
- Writes intermediate results to `output.txt` and final results to `final_output.txt`
- Supports iterative refinement (default: 1 iteration, configurable via `max_iterations`)

**agents/**: Directory containing specialized agent implementations
- `base_agent.py`: Base class with shared Ollama endpoint configuration
- `config.py`: Centralized model configuration (`DEFAULT_MODEL`)
- Agent implementations: `product_management.py`, `design.py`, `engineering.py`, `testing.py`, `security.py`, `devops.py`, `final_agent.py`

### Agent Workflow (Directed Graph)
```
ProductManagement → Design → Engineering → Testing → Security → DevOps → Final
```

Each agent:
1. Receives a prompt dict with `{message, code, readme}`
2. Sends specialized prompts to Ollama API at `http://localhost:11434/api/generate`
3. Appends its output to the `message` field
4. Returns enhanced prompt dict to the next agent

**FinalAgent** differs: it evaluates completeness and returns a boolean instead of continuing the chain.

### Agent Design Pattern

All agents inherit from `BaseAgent` and follow this pattern:
```python
def process(self, message, code="", readme=""):
    # 1. Convert message to string (handles dict/string input)
    # 2. Build specialized prompt for Ollama
    # 3. POST to Ollama endpoint with model from config
    # 4. Append response to message
    # 5. Return {message, code, readme} dict
```

### Data Flow

1. `initial_prompt.json` → JSON dict loaded
2. Each agent enhances the `message` field by appending its specialized output
3. `code` and `readme` fields flow through unchanged (available for agents to populate)
4. After each agent: write to `output.txt`
5. After all agents: write to `final_output.txt`

## Key Configuration

### Changing the Ollama Model
Edit `agents/config.py`:
```python
class ModelConfig:
    DEFAULT_MODEL = "qwq"  # Change to any Ollama model name
```

### Adjusting Agent Workflow
Modify the graph edges in `main.py`:
```python
G.add_edges_from([
    ('ProductManagement', 'Design'),
    # Add, remove, or reorder edges here
])
```

### Iteration Control
Modify `max_iterations` in `main.py` to allow more refinement passes through the agent pipeline.

## Dependencies

- **networkx**: Directed graph management for agent workflow
- **requests**: HTTP communication with Ollama API
- **json**: Parsing initial_prompt.json

## Critical Requirements

- **Ollama must be running locally** on port 11434 with the configured model available
- `initial_prompt.json` must exist in project root with valid JSON structure
- All agent files must inherit from `BaseAgent` and implement `process()` method

## Common Operations

### Adding a New Agent
1. Create `agents/new_agent.py` inheriting from `BaseAgent`
2. Implement `process(self, message, code="", readme="")` method
3. Import in `main.py`
4. Add to `agents` dict in `main()`
5. Add edges to graph to define its position in workflow

### Customizing Agent Prompts
Each agent's prompt is in its `process()` method. Modify the prompt string in the `data["prompt"]` field to change agent behavior.

### Debugging Agent Issues
- Check Ollama is running: `curl http://localhost:11434/api/generate`
- Verify model exists: `ollama list` 
- Check `output.txt` to see which agent last executed successfully
- Agent errors are caught and printed to console with agent name
