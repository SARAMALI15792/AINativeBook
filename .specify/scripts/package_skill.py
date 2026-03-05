#!/usr/bin/env python3
"""
Package a skill for distribution following the skill-creator pattern.

Usage:
    python package_skill.py <path/to/skill-folder> [output-directory]

Examples:
    python package_skill.py .claude/skills/engineering/my-skill
    python package_skill.py .claude/skills/authoring/my-skill ./dist
"""

import os
import sys
import json
import argparse
import zipfile
from pathlib import Path
import yaml


def validate_skill(skill_path):
    """Validate that the skill meets all requirements."""
    skill_path = Path(skill_path)

    print(f"Validating skill at {skill_path}...")

    # Check if SKILL.md exists
    skill_file = skill_path / "SKILL.md"
    if not skill_file.exists():
        print(f"Error: Missing SKILL.md file in {skill_path}")
        return False

    # Read and validate SKILL.md content
    try:
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for YAML frontmatter
        if not content.startswith('---'):
            print(f"Error: SKILL.md missing YAML frontmatter")
            return False

        # Extract YAML frontmatter
        parts = content.split('---', 2)
        if len(parts) < 3:
            print(f"Error: Invalid YAML frontmatter in SKILL.md")
            return False

        yaml_content = parts[1]
        data = yaml.safe_load(yaml_content)

        # Validate required fields
        if not data.get('name'):
            print(f"Error: Missing 'name' in YAML frontmatter")
            return False

        if not data.get('description'):
            print(f"Error: Missing 'description' in YAML frontmatter")
            return False

        print(f"✓ Skill name: {data['name']}")
        print(f"✓ Description present")

        # Validate description quality (should be specific)
        description = data['description']
        if len(description.strip()) < 10:
            print(f"Warning: Description might be too short")

        if 'placeholder' in description.lower() or 'example' in description.lower():
            print(f"Warning: Description appears to be a placeholder")

        # Check for proper directory structure
        required_dirs = ['scripts', 'references', 'assets']
        for dir_name in required_dirs:
            dir_path = skill_path / dir_name
            if not dir_path.exists():
                print(f"Warning: Missing directory {dir_name} (not required but often used)")
            else:
                print(f"✓ Found directory: {dir_name}")

        print("✓ Skill validation passed")
        return True

    except Exception as e:
        print(f"Error validating SKILL.md: {e}")
        return False


def package_skill(skill_path, output_dir=None):
    """Package the skill into a zip file."""
    skill_path = Path(skill_path)
    skill_name = skill_path.name

    if output_dir is None:
        output_dir = "."

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    zip_path = output_path / f"{skill_name}.zip"

    print(f"Creating package at {zip_path}...")

    # Create zip file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                file_path = Path(root) / file
                # Add file to zip with relative path
                arcname = file_path.relative_to(skill_path.parent)
                zipf.write(file_path, arcname)

    print(f"✓ Skill packaged successfully at {zip_path}")
    return zip_path


def main():
    parser = argparse.ArgumentParser(description='Package a skill following the skill-creator pattern.')
    parser.add_argument('skill_path', help='Path to the skill directory to package')
    parser.add_argument('output_dir', nargs='?', default=None, help='Output directory for the package (optional)')

    args = parser.parse_args()

    skill_path = Path(args.skill_path)
    if not skill_path.exists():
        print(f"Error: Path '{skill_path}' does not exist.")
        return 1

    if not skill_path.is_dir():
        print(f"Error: '{skill_path}' is not a directory.")
        return 1

    # Validate the skill first
    if not validate_skill(skill_path):
        print("Skill validation failed. Please fix the issues before packaging.")
        return 1

    # Package the skill
    try:
        package_path = package_skill(skill_path, args.output_dir)
        print(f"\nSkill '{skill_path.name}' successfully validated and packaged!")
        print(f"Package created at: {package_path}")
        return 0
    except Exception as e:
        print(f"Error packaging skill: {e}")
        return 1


if __name__ == "__main__":
    # Need to install PyYAML for this script to work
    try:
        import yaml
    except ImportError:
        print("This script requires PyYAML. Install it with: pip install PyYAML")
        sys.exit(1)

    sys.exit(main())