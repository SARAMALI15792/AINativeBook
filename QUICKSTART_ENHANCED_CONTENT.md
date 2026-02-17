# Enhanced Content Structure - Quick Start Guide

## Overview

Sprint 1 (Foundation) is complete! The IntelliStack platform now has comprehensive infrastructure for:
- 📚 Deep-dive structured content with hierarchical organization
- 🎯 Personalization engine adapting to user preferences
- 🌍 Urdu translation with GPT-4 and caching
- 💻 Interactive code blocks with secure execution
- 📊 Analytics tracking for content effectiveness

## Quick Start

### 1. Apply Database Migration

```bash
cd intellistack/backend
alembic upgrade head
```

This creates:
- 6 new tables (ContentHierarchy, ContentVariant, ContentSummary, InteractiveCodeBlock, ContentEngagement, ContentEffectiveness)
- 5 new enum types
- 8 new columns on existing Content table

### 2. Install Dependencies

```bash
pip install python-frontmatter
```

### 3. Test the API

Start the backend server:
```bash
cd intellistack/backend
uvicorn src.main:app --reload
```

Test endpoints:
```bash
# Get personalized content
curl http://localhost:8000/api/v1/content/{content_id}?personalized=true

# List content variants
curl http://localhost:8000/api/v1/content/{content_id}/variants

# Execute code
curl -X POST http://localhost:8000/api/v1/content/code/execute \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"Hello\")", "language": "python", "environment": "pyodide"}'
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Content Delivery Flow                    │
└─────────────────────────────────────────────────────────────┘

User Request
    ↓
┌───────────────────┐
│  Enhanced Routes  │  GET /api/v1/content/{id}?personalized=true
└────────┬──────────┘
         ↓
┌───────────────────┐
│ Personalization   │  • Get user profile
│    Service        │  • Determine complexity level
└────────┬──────────┘  • Select appropriate variant
         ↓
┌───────────────────┐
│  Content Variant  │  • Simplified / Standard / Advanced
│    Selection      │  • English / Urdu
└────────┬──────────┘
         ↓
┌───────────────────┐
│   Translation     │  • Check cache (30 days)
│    Service        │  • GPT-4 translation if needed
└────────┬──────────┘  • Preserve code blocks
         ↓
┌───────────────────┐
│  Summary Service  │  • Auto-generated summaries
│                   │  • Key concepts extraction
└────────┬──────────┘  • Learning objectives
         ↓
┌───────────────────┐
│ Interactive Code  │  • Executable code blocks
│     Blocks        │  • Pyodide (browser) / Docker (server)
└────────┬──────────┘  • Security sandboxing
         ↓
Response with personalized, translated content + summaries + code blocks
```

## Database Schema

```
Content (existing)
├── has_summary: bool
├── has_interactive_code: bool
├── difficulty_level: enum
├── estimated_reading_time: int
├── prerequisites: jsonb
├── related_content: jsonb
├── tags: jsonb
└── keywords: jsonb

ContentHierarchy (new)
├── parent_id → ContentHierarchy
├── content_id → Content
├── hierarchy_type: enum (stage/chapter/section/subsection)
├── order_index: int
├── depth_level: int
└── breadcrumb_path: jsonb

ContentVariant (new)
├── content_id → Content
├── variant_type: enum (simplified/standard/advanced/language)
├── language_code: str (en/ur)
├── complexity_level: enum
├── mdx_path: str
├── content_json: jsonb
├── word_count: int
├── translated_by: str
└── translation_quality_score: float

ContentSummary (new)
├── content_id → Content
├── summary_type: enum (brief/detailed/key_points)
├── language_code: str
├── summary_text: text
├── key_concepts: jsonb
├── learning_objectives: jsonb
├── prerequisites: jsonb
└── auto_generated: bool

InteractiveCodeBlock (new)
├── content_id → Content
├── code_language: str
├── code_content: text
├── execution_environment: enum (pyodide/docker/wasm)
├── is_editable: bool
├── timeout_seconds: int
├── allowed_imports: jsonb
└── blocked_functions: jsonb

ContentEngagement (new)
├── user_id → User
├── content_id → Content
├── variant_id → ContentVariant
├── time_spent_seconds: int
├── scroll_depth_percent: int
├── code_blocks_executed: int
└── completed: bool

ContentEffectiveness (new)
├── content_id → Content
├── total_views: int
├── completion_rate: float
├── avg_quiz_score: float
├── common_struggles: jsonb
└── language_distribution: jsonb
```

## Service APIs

### PersonalizationService

```python
from src.ai.personalization.service import PersonalizationService

service = PersonalizationService(llm_client)

# Get personalized content variant
variant = await service.get_personalized_content(
    content_id="chapter-1",
    user_id="user-123",
    db=db
)

# Generate domain-specific examples
examples = await service.generate_personalized_examples(
    content=content,
    profile=user_profile
)

# Estimate personalized time
time_minutes = await service.estimate_personalized_time(
    content=content,
    profile=user_profile
)
```

### TranslationService

```python
from src.ai.translation.service import TranslationService

service = TranslationService(llm_client)

# Translate content
translated = await service.translate_content(
    content_id="chapter-1",
    content_text="The kernel manages...",
    source_language="en",
    target_language="ur",
    content_type="chapter",
    context="Linux operating systems",
    db=db
)

# Batch translate
results = await service.batch_translate(
    content_items=[
        {"id": "ch1", "text": "...", "type": "chapter"},
        {"id": "ch2", "text": "...", "type": "chapter"}
    ],
    target_language="ur",
    db=db
)
```

### CodeExecutionService

```python
from src.ai.code_execution.service import CodeExecutionService

service = CodeExecutionService()

# Execute code
result = await service.execute_code(
    code="print('Hello, World!')",
    language="python",
    environment="pyodide",
    timeout=30
)

# Validate code
validation = await service.validate_code(
    code="import os; os.system('ls')",
    language="python"
)
# Returns: {"valid": False, "error": "Security violation: import os is not allowed"}
```

### SummaryService

```python
from src.ai.content.summary_service import SummaryService

service = SummaryService(llm_client)

# Generate summary
summary = await service.generate_summary(
    content=content,
    content_text="Full chapter text...",
    summary_type="brief",
    language_code="en",
    db=db
)

# Extract key concepts
concepts = await service.extract_key_concepts(
    content_text="Full chapter text...",
    max_concepts=5
)
```

### ContentSyncService

```python
from src.core.content.sync_service import ContentSyncService
from pathlib import Path

service = ContentSyncService(
    content_directory=Path("intellistack/content/docs")
)

# Scan content directory
content_files = await service.scan_content_directory()

# Sync single file
content = await service.sync_content_to_db(
    content_file=content_files[0],
    stage_id="stage-1",
    db=db
)

# Full sync
stats = await service.full_sync(db=db)
# Returns: {"scanned": 35, "created": 5, "updated": 30, "errors": 0}
```

## Content File Format

Create content files with frontmatter:

```markdown
---
id: 1-1-linux-theory
title: "The Digital Nervous System"
sidebar_label: "1.1 Linux & OS Theory"
description: "Deep dive into Kernel Space, User Space, and the 'Everything is a File' abstraction."
difficulty: intermediate
estimated_time: 45
tags: ["linux", "kernel", "operating-systems"]
learning_objectives:
  - Understand kernel vs user space separation
  - Explain system calls and their role
  - Apply the "everything is a file" concept
prerequisites:
  - Basic programming knowledge
  - Command line familiarity
---

# The Digital Nervous System

<details>
<summary>📋 Chapter Summary</summary>

**Key Concepts**: Kernel space, User space, System calls, File descriptors

**What You'll Learn**:
- Understand the privilege separation in operating systems
- Explain how system calls work
- Apply the "everything is a file" concept to robotics I/O

**Prerequisites**: Basic programming knowledge, familiarity with command line

**Time Estimate**: 45 minutes

</details>

## 1. The Theory of Existence

Content here...

## 2. Interactive Example

```python live
# This code is editable and executable
import sys

def hello_kernel():
    print("Hello from user space!")
    print(f"Python version: {sys.version}")

hello_kernel()
```

## 3. Deep FAQ

**Q: Why can't user space access hardware directly?**
A: Security and stability...
```

## Security Configuration

### Code Execution Limits

Default security settings in `CodeExecutionService`:

```python
# Resource limits
default_timeout = 30  # seconds
max_output_length = 10000  # characters
default_memory_limit = 128  # MB

# Blocked patterns
dangerous_patterns = [
    "import os",
    "import sys",
    "import subprocess",
    "__import__",
    "eval(",
    "exec(",
    "compile(",
    "open(",
    "file(",
]

# Docker security
docker_flags = [
    "--rm",
    "--network=none",  # No network access
    f"--memory={memory_limit}m",
    "--cpus=0.5",
    f"--timeout={timeout}",
]
```

### API Authentication

All endpoints require authentication:

```python
from src.core.auth.dependencies import get_current_user

@router.get("/{content_id}")
async def get_content(
    content_id: str,
    current_user: User = Depends(get_current_user),  # Required
    db: AsyncSession = Depends(get_db),
):
    # Endpoint logic
```

## Next Steps

### Immediate Actions

1. **Apply Migration**
   ```bash
   cd intellistack/backend
   alembic upgrade head
   ```

2. **Test Services**
   - Run backend server
   - Test personalization endpoint
   - Execute sample code
   - Generate a summary

3. **Review Documentation**
   - Read `ENHANCED_CONTENT_IMPLEMENTATION.md`
   - Review service APIs
   - Check security measures

### Sprint 2: Content Expansion

**Goal:** Create 60+ comprehensive chapters

**Timeline:** Weeks 2-4 (3 weeks)

**Deliverables:**
- Stage 1: 15-20 chapters (Linux, Python, Math, Git, Physics)
- Stage 2: 12-15 chapters (ROS 2, Gazebo, Launch systems)
- Stage 3: 10-12 chapters (Computer vision, SLAM, Sensor fusion)
- Stage 4: 10-12 chapters (ML, Deep learning, RL, LLM integration)
- Stage 5: 8-10 chapters (Capstone project guidance)

**Content Standards:**
- Every chapter has collapsible summary
- Minimum 3 interactive code examples
- Mermaid diagrams for complex concepts
- "Deep FAQ" section
- Cross-linked related chapters

## Troubleshooting

### Migration Issues

```bash
# Check current migration status
alembic current

# View migration history
alembic history

# Rollback if needed
alembic downgrade -1
```

### Service Errors

Check logs with structlog:
```python
import structlog
logger = structlog.get_logger()

# Logs include context
logger.info("content_synced", content_id=content.id, title=content.title)
logger.error("translation_error", error=str(e), content_id=content_id)
```

### Code Execution Failures

Common issues:
- Docker daemon not running → Start Docker Desktop
- Timeout errors → Increase timeout parameter
- Security violations → Check allowed_imports and blocked_functions
- Memory errors → Increase memory_limit_mb

## Resources

- **Implementation Doc:** `ENHANCED_CONTENT_IMPLEMENTATION.md`
- **PHR:** `history/prompts/001-intellistack-platform/001-enhanced-content-implementation.implementation.prompt.md`
- **Migration:** `intellistack/backend/alembic/versions/20260217_enhanced_content_structure.py`
- **Models:** `intellistack/backend/src/core/content/enhanced_models.py`
- **Services:** `intellistack/backend/src/ai/*/service.py`

## Support

For questions or issues:
1. Check `ENHANCED_CONTENT_IMPLEMENTATION.md` for detailed documentation
2. Review service code for implementation details
3. Check logs for error messages
4. Consult PHR for implementation context

---

**Status:** Sprint 1 Complete ✅
**Next:** Sprint 2 - Content Expansion
**Progress:** 15% of total implementation
