#!/usr/bin/env python3
"""
Initialize a new skill following the skill-creator pattern.

Usage:
    python init_skill.py <skill-name> --path <path>

Examples:
    python init_skill.py my-skill --path .claude/skills/authoring/
    python init_skill.py my-skill --path .claude/skills/engineering/
"""

import os
import sys
import argparse
from pathlib import Path


def create_skill_structure(skill_name, skill_path):
    """Create the basic skill structure with required files and directories."""

    # Validate skill name
    if not skill_name.replace('-', '').replace('_', '').isalnum():
        print(f"Error: Skill name '{skill_name}' contains invalid characters. Use only alphanumeric, hyphens, and underscores.")
        return False

    # Create the full skill directory
    full_path = Path(skill_path) / skill_name
    if full_path.exists():
        print(f"Error: Skill directory already exists at {full_path}")
        return False

    # Create the skill structure
    full_path.mkdir(parents=True, exist_ok=True)

    # Create directories
    (full_path / "scripts").mkdir(exist_ok=True)
    (full_path / "references").mkdir(exist_ok=True)
    (full_path / "assets").mkdir(exist_ok=True)

    # Create the main SKILL.md file
    skill_content = f"""---
name: {skill_name}
description: Provide a clear, specific description of what this skill does and when to use it.
---

# {skill_name.replace('-', ' ').replace('_', ' ').title()}

Provide a comprehensive description of the skill's purpose and functionality here.

## When to Use This Skill

This skill should be used when:
- List specific conditions when this skill should be used
- Be as specific as possible about the scenarios
- Include what problems this skill solves

## How to Use This Skill

Provide step-by-step instructions for using this skill:
1. First step
2. Second step
3. Third step

## Resources Available

- Use files in `scripts/` for executable code
- Reference files in `references/` for documentation
- Use files in `assets/` for templates and boilerplate

## Important Guidelines

- Follow imperative/infinitive form writing style
- Be specific and actionable
- Focus on what Claude should do when using this skill
"""

    with open(full_path / "SKILL.md", "w", encoding="utf-8") as f:
        f.write(skill_content)

    # Create an example script
    script_content = '''#!/usr/bin/env python3
"""
Example script for the skill.
"""

def main():
    print("This is an example script for the skill.")
    # Add actual script functionality here


if __name__ == "__main__":
    main()
'''

    with open(full_path / "scripts" / "example_script.py", "w", encoding="utf-8") as f:
        f.write(script_content)

    # Create an example reference
    reference_content = """# Example Reference Document

This is an example reference file that can be loaded when needed to provide additional context to Claude.

## Detailed Information

Provide detailed information that Claude might need to reference when using this skill.
"""

    with open(full_path / "references" / "example_reference.md", "w", encoding="utf-8") as f:
        f.write(reference_content)

    # Create an example asset
    asset_content = """# Example Asset File

This is an example asset file that can be used as a template or for direct inclusion in outputs.
"""

    with open(full_path / "assets" / "example_asset.txt", "w", encoding="utf-8") as f:
        f.write(asset_content)

    # Create README
    readme_content = f"""# {skill_name.replace('-', ' ').replace('_', ' ').title()}

This skill provides functionality for [describe what the skill does].

## Usage

[Explain how to use this skill]

## Resources

- `scripts/` - Contains executable scripts
- `references/` - Contains reference documentation
- `assets/` - Contains template files
"""

    with open(full_path / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"Skill '{skill_name}' successfully created at {full_path}")
    print("\nNext steps:")
    print(f"1. Edit {full_path}/SKILL.md with your specific skill implementation")
    print(f"2. Add relevant scripts to {full_path}/scripts/")
    print(f"3. Add reference materials to {full_path}/references/")
    print(f"4. Add asset templates to {full_path}/assets/")

    return True


def main():
    parser = argparse.ArgumentParser(description='Initialize a new skill following the skill-creator pattern.')
    parser.add_argument('skill_name', help='Name of the skill to create')
    parser.add_argument('--path', required=True, help='Path where the skill should be created (e.g., .claude/skills/authoring/ or .claude/skills/engineering/)')

    args = parser.parse_args()

    # Validate path
    skill_path = Path(args.path)
    if not skill_path.exists():
        print(f"Error: Path '{skill_path}' does not exist.")
        print("Make sure you're using the correct path: .claude/skills/authoring/ or .claude/skills/engineering/")
        return 1

    success = create_skill_structure(args.skill_name, skill_path)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())