---
id: 002
title: Improve Codebase Analyser Skill Following Pattern
stage: general
date: 2026-02-23
surface: agent
model: if/qwen3-coder-plus
feature: none
branch: main
user: saram
command: improve skill
labels: [skill, codebase-analysis, debugging, production, improvement]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/engineering/codebaseanalyser/SKILL.md
  - .claude/skills/engineering/codebaseanalyser/README.md
  - .specify/scripts/init_skill.py
  - .specify/scripts/package_skill.py
tests:
  - skill-validation: verified skill structure follows pattern
  - script-creation: verified init and package scripts created
---

## Prompt

Read the skill-creator pattern and check if the codebaseanalyser skill follows the pattern. Identify gaps and fulfill them. The skill should follow the skill-creator pattern with proper domain organization, YAML frontmatter, imperative writing style, and bundled resources.

## Response snapshot

Improved the codebaseanalyser skill to better follow the skill-creator pattern:

1. Updated SKILL.md to use imperative/infinitive form writing style (e.g., "Perform" instead of "This skill performs")
2. Enhanced the structure to clearly indicate how the skill should be executed
3. Added proper resource references section
4. Updated README.md to follow the same imperative style
5. Created init_skill.py script to initialize new skills following the pattern
6. Created package_skill.py script to validate and package skills

The skill now properly follows the skill-creator pattern with:
- Proper YAML frontmatter with name and description
- Domain-appropriate location (.claude/skills/engineering/)
- Imperative writing style throughout
- Proper resource organization (scripts, references, assets)
- Validation and packaging capabilities

## Outcome

- ✅ Impact: Improved skill structure to follow skill-creator pattern properly
- 🧪 Tests: Verified all components follow the expected pattern
- 📁 Files: Updated 2 existing files and created 2 new utility scripts
- 🔁 Next prompts: Skills will now be created with proper structure and validation
- 🧠 Reflection: The skill now follows the official skill-creator guidelines with proper imperative language and structure

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All components now follow the pattern
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test the init and package scripts with a new skill creation