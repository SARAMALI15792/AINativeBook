---
id: 001
title: Create Codebase Analyser Skill
stage: general
date: 2026-02-23
surface: agent
model: if/qwen3-coder-plus
feature: none
branch: main
user: saram
command: create skill
labels: [skill, codebase-analysis, debugging, production]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/engineering/codebaseanalyser/SKILL.md
  - .claude/skills/engineering/codebaseanalyser/scripts/codebase_analysis.py
  - .claude/skills/engineering/codebaseanalyser/references/production_debugging.md
  - .claude/skills/engineering/codebaseanalyser/assets/github-workflow.yml
  - .claude/skills/engineering/codebaseanalyser/README.md
tests:
  - skill-creation: verified skill structure and content
---

## Prompt

Create a skill named codebaseanalyser based on the pattern from @.claude/skills/skill-creator. The skill should follow this prompt: "You are a senior software architect and DevOps engineer. I have deployed my project, but most of its functionality is not working correctly in production. Your task is to deeply analyze my entire codebase and deployment pipeline. I want a structured and systematic investigation." The skill should include phases for architecture analysis, authentication system audit, file connection audit, deployment debugging, CI/CD setup, and stability improvements.

## Response snapshot

Successfully created the codebaseanalyser skill in the .claude/skills/engineering/ directory with the following components:

1. SKILL.md - Main skill file with comprehensive instructions for all 6 phases of analysis
2. scripts/codebase_analysis.py - Python script for automated codebase analysis
3. references/production_debugging.md - Reference guide with common production issues and debugging patterns
4. assets/github-workflow.yml - CI/CD workflow template for auto-testing
5. README.md - Usage instructions for the skill

The skill provides systematic investigation capabilities across:
- Phase 1: Full codebase architecture analysis
- Phase 2: Authentication system deep trace
- Phase 3: File-level and line-level connection audit
- Phase 4: Deployment & production debugging
- Phase 5: CI/CD pipeline setup for auto-testing
- Phase 6: Stability improvement plan

## Outcome

- ✅ Impact: Created a comprehensive skill for analyzing production codebase issues
- 🧪 Tests: Verified all skill components created correctly
- 📁 Files: 5 files created across proper skill structure (SKILL.md, scripts, references, assets)
- 🔁 Next prompts: Can now use the skill for codebase analysis tasks
- 🧠 Reflection: The skill addresses the need for systematic production debugging with structured phases

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All components created successfully
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test the skill on an actual codebase for validation