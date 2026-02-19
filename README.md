# IntelliStack Platform

**AI-Native Learning Platform for Physical AI & Humanoid Robotics Education**

This repository contains the IntelliStack platform - an advanced learning management system designed specifically for physical AI and humanoid robotics education.

## Features

- Progressive learning paths (5 stages from Foundations to Capstone)
- AI-powered tutoring with Socratic method
- RAG chatbot with citations and source navigation
- Content authoring tools with versioning
- Institution management with cohorts and analytics
- Community features (coming soon)
- Assessment delivery with rubric-based grading (coming soon)

## Technology Stack

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **ORM:** SQLAlchemy 2.0 (async)
- **Migrations:** Alembic
- **Database:** PostgreSQL (Neon)
- **Vector Store:** Qdrant (for RAG)
- **Cache:** Redis
- **AI/ML:** OpenAI API, LangChain/LangGraph, Cohere (reranking)

### Infrastructure
- **Containerization:** Docker & Docker Compose
- **GPU Support:** NVIDIA Container Toolkit
- **Simulation:** Gazebo, NVIDIA Isaac Sim

## Current Progress

The platform is currently at 74.5% completion (38/51 tasks complete), with the following phases completed:
- Phase 0: Vertical Slice (100%)
- Phase 1: Setup (100%)
- Phase 2: Foundation (100%)
- Phase 3: Student Learning (100%)
- Phase 4: Content Creation (100%)
- Phase 5: Institution Admin (100%)
- Phase 6: RAG Chatbot (100%)

Upcoming phases include:
- Phase 7: AI Tutor (Socratic method, debugging helper, code review)
- Phase 8: Community (Forums, study groups, mentorship)
- Phase 9: Assessment (Quiz delivery, rubric-based grading)
- Phase 10: Personalization (Adaptive content, recommendations)
- Phase 11: Polish (Production readiness, security, docs)

## Contributing

To contribute to this project, please follow the spec-driven development (SDD) methodology outlined in the documentation.