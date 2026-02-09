<!--
Sync Impact Report
==================
Version change: 2.0.0 → 2.1.0 (MINOR - expanded existing principles with specificity)
Modified principles:
  - II. Safety and Responsibility → Added safety assessment requirements and scope by stage
  - III. Understanding Before Automation → Added depth-by-stage framework and verification criteria
  - V. Progressive Learning Path → Added Challenge Pathway for experienced learners
Added sections:
  - Safety Assessment Requirements (under Principle II)
  - Safety Assessment Scope by Context (under Principle II)
  - Depth of Understanding by Stage (under Principle III)
  - Understanding Verification Framework (under Principle III)
  - Challenge Pathway (under Principle V)
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/plan-template.md - ✅ compatible
  - .specify/templates/spec-template.md - ✅ compatible
  - .specify/templates/tasks-template.md - ✅ compatible
Follow-up TODOs:
  - Create separate Project Rubric & Technical Standards Guide (for code quality tools)
  - Create Academic Integrity Policy document
  - Create Content Style Guide document
  - Create Stage Curriculum Specifications document
==================
-->

# IntelliStack Constitution

> A learning platform for Physical AI & Humanoid Robotics

## Mission and Vision

**Mission**: IntelliStack empowers learners to bridge the gap between digital AI and
physical robotic systems through hands-on, simulation-first education that builds
confidence before real-world deployment.

**Vision**: A world where anyone with curiosity and dedication can learn to build
intelligent robots that help humanity—safely, responsibly, and with deep understanding
of the technology they create.

## Core Principles

### I. Simulation Before Hardware

All robotic concepts MUST be mastered in simulation before any hardware interaction.

- Learners MUST complete Gazebo/Isaac Sim exercises before touching physical robots
- Every physical robot task requires a passing simulation checkpoint
- Hardware access is a privilege earned through demonstrated simulation competency

**Rationale**: Physical robots are expensive, can cause injury, and are not always
available. Simulation provides unlimited safe practice, faster iteration cycles,
and builds the mental models needed for real-world success.

### II. Safety and Responsibility

Safety is non-negotiable in all learning activities and projects.

- Every robot project MUST include a safety assessment section
- Emergency stop procedures MUST be documented and tested before any robot activation
- Learners MUST acknowledge and sign safety protocols before hardware labs
- Code that controls physical systems MUST include watchdog timers and fail-safes
- No autonomous robot behavior is permitted without human-in-the-loop oversight during learning

**Rationale**: Physical AI systems can cause real harm. Building safety-first habits
from day one creates responsible engineers who protect people and property.

#### Safety Assessment Requirements

Every hardware project safety assessment MUST address these 10 items:

| # | Requirement | Description |
|---|-------------|-------------|
| 1 | **Hazard Identification** | List all mechanical, electrical, and environmental hazards |
| 2 | **Risk Severity Rating** | Rate each hazard: Minor / Moderate / Severe / Critical |
| 3 | **Emergency Stop Procedure** | Document E-stop location, activation method, and expected behavior |
| 4 | **Operating Envelope** | Define speed limits, force limits, and workspace boundaries |
| 5 | **Human Interaction Zones** | Map areas where humans may be present; define barriers |
| 6 | **Failure Mode Analysis** | Document what happens if power fails, sensors fail, software crashes |
| 7 | **Required PPE** | List personal protective equipment (safety glasses, gloves, etc.) |
| 8 | **Supervision Requirements** | Specify who must be present and their qualifications |
| 9 | **Environmental Preconditions** | Define lighting, floor conditions, obstacle clearance |
| 10 | **Recovery Procedure** | Document steps to safely resume after emergency stop |

**Automatic Rejection Triggers** (assessment fails immediately if any are missing):
- No emergency stop procedure documented
- No hazard identification performed
- Risk severity not rated for identified hazards
- No supervisor sign-off for hardware projects

#### Safety Assessment Scope by Stage

Not all stages require the full 10-item assessment. Scope is proportional to risk:

| Context | Stages | Required Assessment |
|---------|--------|---------------------|
| **Simulation-Only** | 0-3 | Simplified (5 items): workspace ergonomics, data backup, simulation limits awareness, no real-world deployment acknowledgment, instructor contact info |
| **Perception/Planning Sim** | 4-6 | Intermediate (7 items): Add sensor data ethics, algorithm failure awareness, simulated safety scenarios |
| **Sim-to-Real Transition** | 7 | Full 10-item assessment required |
| **Hardware Projects** | 8 | Full 10-item assessment + supervisor sign-off + safety briefing attendance |

**Full Safety Assessment Becomes MANDATORY When**:
- Any physical hardware is involved (motors, actuators, sensors on real devices)
- Code will be deployed outside simulation environment
- Project involves human interaction zones (even in simulation prep)
- Learner requests early hardware access via Challenge Pathway

### III. Understanding Before Automation

Learners MUST understand what the AI is doing before using it to automate tasks.

- No black-box solutions: every AI model used MUST be explained at an appropriate depth
- Manual implementation of core algorithms is required before using library functions
- Learners MUST be able to explain their robot's behavior in plain language
- Vision-Language-Action models require understanding of each component before integration

**Rationale**: Automation without understanding leads to brittle systems, debugging
nightmares, and engineers who cannot innovate. True mastery comes from comprehension.

#### Depth of Understanding by Stage

"Appropriate depth" varies by learner stage. This framework defines expectations:

| Stage | Depth Level | What Learner Must Explain | Example: Neural Network |
|-------|-------------|---------------------------|------------------------|
| 0-2 | **Conceptual** | What it does, why it's useful, when to use it | "It learns patterns from data to make predictions" |
| 3-4 | **Functional** | How components work together, inputs/outputs, parameters | "Layers transform inputs; training adjusts weights via loss minimization" |
| 5-6 | **Mechanical** | Internal algorithms, math foundations, optimization | "Backpropagation computes gradients; Adam optimizer updates weights with momentum" |
| 7-8 | **Implementation** | Code-level understanding, debugging ability, modification capability | "I can implement custom loss functions, diagnose vanishing gradients, and tune hyperparameters" |

Learners MUST demonstrate depth appropriate to their current stage. Assessments are
calibrated to stage-appropriate expectations—Stage 2 learners are not expected to
explain backpropagation math.

#### Understanding Verification Framework

To verify learners truly understand (not just memorize), assessments MUST include:

**Verification Methods** (at least one required per major concept):
- **Explanation Without Code**: Learner explains system behavior without reading source code
- **Predict-Before-Run**: Learner predicts output before executing; explains discrepancies
- **Modification Challenge**: Learner modifies behavior to meet new requirement
- **Debugging Scenario**: Learner diagnoses and fixes intentionally broken system
- **Teaching Back**: Learner explains concept to peer or AI tutor

**Evaluation Criteria** (rubric framework):
| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Accuracy** | 30% | Technical correctness of explanation |
| **Completeness** | 25% | Covers all relevant components at appropriate depth |
| **Clarity** | 20% | Explanation is understandable to target audience |
| **Appropriate Depth** | 15% | Matches stage-level expectations (not too shallow, not too deep) |
| **Follow-up Handling** | 10% | Can answer clarifying questions; admits knowledge limits |

**Evaluators**: Qualified instructor, trained peer mentor, or AI with human review for edge cases.

### IV. AI as a Learning Guide

AI assistants serve as tutors, not replacements for learning.

- AI MUST explain concepts, not just provide answers
- AI-generated code MUST be reviewed, understood, and tested by the learner
- AI SHOULD ask clarifying questions to promote deeper thinking
- AI MUST encourage experimentation and learning from mistakes
- AI MUST NOT complete assignments for students—guidance over completion

**Rationale**: The goal is to create skilled roboticists, not prompt engineers. AI
accelerates learning when it teaches; it hinders growth when it replaces thinking.

### V. Progressive Learning Path

Learning follows a structured path from fundamentals to advanced integration.

The journey:
0. **Prerequisites** (Stage 0): Diagnostic assessment; remedial path if needed
1. **Foundations**: Python, Linux basics, math for robotics (linear algebra, calculus)
2. **ROS 2 Basics**: Nodes, topics, services, actions, launch files
3. **Simulation Mastery**: Gazebo environments, sensor simulation, physics tuning
4. **Perception**: Computer vision, NVIDIA Isaac perception pipelines
5. **Planning & Control**: Motion planning, navigation, manipulation
6. **AI Integration**: Vision-Language-Action models, learning-based control
7. **Sim-to-Real Transfer**: Domain randomization, sensor calibration, reality gap handling
8. **Real Robot Projects**: Hardware labs with physical humanoid platforms

Each level MUST be completed before advancing. Assessments gate progression.
Competency-based advancement—not time-based.

**Rationale**: Robotics builds on itself. Skipping fundamentals creates knowledge gaps
that become critical failures when systems grow complex.

#### Challenge Pathway (Experienced Learner Advancement)

Experienced learners may demonstrate competency to advance past stages they've already
mastered elsewhere. This respects prior learning while maintaining rigor.

**Eligibility**:
- Learners with documented prior robotics experience (professional, academic, or project-based)
- Self-assessment indicates familiarity with stage content
- Willing to complete challenge assessment

**Challenge Assessment Options**:

| Method | Description | When to Use |
|--------|-------------|-------------|
| **Comprehensive Exam** | Practical exam covering all stage learning objectives | Quick validation of broad knowledge |
| **Portfolio Review** | Submit prior work demonstrating equivalent skills | Strong existing project evidence |
| **Live Demonstration** | Real-time demonstration of skills with Q&A | Complex skills requiring observation |

**Requirements**:
- **Passing Threshold**: Demonstrate mastery of ≥85% of stage competencies
- **Verification**: All portfolio submissions verified for authenticity
- **Documentation**: Prior experience documented with references where possible

**Limitations** (stages that CANNOT be fully skipped):

| Stage | Skip Policy | Reason |
|-------|-------------|--------|
| Safety content in any stage | Must complete safety refresher | Safety knowledge must be current and IntelliStack-specific |
| Stage 7 (Sim-to-Real) | Must complete regardless of experience | Critical transition skills; platform-specific |
| Stage 8 Capstone | Must complete new capstone | Demonstrates integrated IntelliStack learning |

**Additional Constraints**:
- Maximum consecutive skip: 3 stages
- Skipped stage clusters require at least one project demonstrating integrated skills
- Challenge pathway learners join regular cohort at their entry stage

**Recognition**:
- Challenged stages count fully toward certification
- Transcript notes "demonstrated prior competency" for challenged stages
- No penalty or stigma—this pathway is encouraged for qualified learners

### VI. Practical Project Focus

All learning culminates in working projects that solve real problems.

- Every module MUST include a hands-on project component
- Projects MUST be demonstrable—if it doesn't run, it's not complete
- Final capstone projects MUST integrate multiple learned skills
- Project code MUST be version controlled and documented
- Projects SHOULD be shareable as portfolio pieces

**Rationale**: Knowledge without application fades. Projects cement learning, build
portfolios, and prove competency to future employers and collaborators.

### VII. Ethical AI & Responsible Robotics

Learners MUST develop ethical awareness alongside technical skills.

- No weaponization: Skills learned MUST NOT be applied to harmful autonomous weapons
- Privacy awareness: Robots with cameras/sensors MUST respect human privacy
- Bias recognition: Learners MUST understand and mitigate bias in perception and decision models
- Transparency: AI limitations MUST be clearly communicated in any deployed system
- Environmental responsibility: Consider energy consumption and e-waste in design decisions
- Human dignity: Robots MUST be designed to augment human capabilities, not replace human worth

**Rationale**: Technical skill without ethical grounding creates dangerous engineers.
Physical AI systems have real-world impact—learners must consider societal consequences.

### VIII. Embrace Failure, Master Debugging

Failure is expected, valuable, and essential to the learning process.

- "Failure is data, not defeat"—every failed attempt provides learning
- Iteration cycles are expected and planned; first attempts rarely work
- Post-mortem analysis of failures is REQUIRED for significant project milestones
- Systematic debugging methodology MUST be taught and practiced:
  - Logging and visualization are mandatory practices
  - Reproduce → Isolate → Hypothesize → Test → Fix cycle
  - Simulation replay of failure cases
- Celebrate debugging victories—solving hard problems builds mastery

**Rationale**: Robotics involves constant debugging. Engineers who fear failure avoid
challenges; engineers who embrace failure become experts. Debugging skill separates
hobbyists from professionals.

### IX. Sim-to-Real Mastery

The transition from simulation to real robots requires explicit training.

- The "reality gap" MUST be explicitly taught—real robots behave differently
- Domain randomization techniques MUST be practiced before hardware deployment
- Sensor noise, calibration drift, and environmental variations MUST be understood
- Iterative real-world validation process: simulate → deploy → observe → refine
- Expectations MUST be set: real-world performance will initially degrade from simulation
- Transfer learning strategies for bridging simulation and reality

**Rationale**: Many learners are shocked when their perfect simulation fails on real
hardware. Explicit sim-to-real training prevents frustration and builds practical skills.

## Who IntelliStack Serves

### Students
- Beginners with no robotics experience who want to enter the field
- Computer science students expanding into physical AI
- Hobbyists and makers building personal robot projects
- Career changers transitioning into robotics engineering

### Educators
- University professors teaching robotics courses
- Bootcamp instructors delivering intensive programs
- Corporate trainers upskilling engineering teams
- Self-directed learners creating study groups

### Content Authors
- Subject matter experts contributing course modules
- Industry practitioners sharing real-world case studies
- Researchers publishing educational materials from their work

### Institutions
- Universities integrating IntelliStack into curricula
- Companies training their robotics teams
- Research labs onboarding new members
- Makerspaces and community learning centers

## The Learning Journey

### Prerequisites & Onboarding

Before Stage 1, learners complete:

1. **Diagnostic Assessment**: Self-evaluation of Python, Linux, and math fundamentals
2. **Prerequisite Checklist**: Clear list of required knowledge with resources
3. **Stage 0 (Remedial Path)**: For those lacking basics—no gatekeeping, paths for all levels
4. **Learning Style Survey**: Identify preferred formats (video, text, interactive)
5. **Environment Setup**: Guided installation of required tools

No learner is turned away—Stage 0 provides the bridge to Stage 1.

### Learning Path Visualization

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                            INTELLISTACK PATH v2.1                            │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   [0] PREREQUISITES        [1] FOUNDATIONS        [2] ROS 2 BASICS          │
│   ┌──────────────┐         ┌──────────────┐       ┌──────────────┐          │
│   │ Diagnostic   │    →    │ Python       │   →   │ Nodes/Topics │          │
│   │ Stage 0      │         │ Linux        │       │ Services     │          │
│   │ Setup        │         │ Math         │       │ Launch Files │          │
│   └──────────────┘         └──────────────┘       └──────────────┘          │
│         ↑                                                                    │
│    Challenge Pathway: Experienced learners may test out of stages 1-6       │
│                                                                              │
│   [3] SIMULATION           [4] PERCEPTION         [5] PLANNING              │
│   ┌──────────────┐         ┌──────────────┐       ┌──────────────┐          │
│   │ Gazebo       │    →    │ Computer     │   →   │ Motion       │          │
│   │ Isaac Sim    │         │ Vision       │       │ Planning     │          │
│   │ Sensors      │         │ Isaac        │       │ Navigation   │          │
│   └──────────────┘         └──────────────┘       └──────────────┘          │
│                                                                              │
│   [6] AI MODELS            [7] SIM-TO-REAL        [8] REAL ROBOTS           │
│   ┌──────────────┐         ┌──────────────┐       ┌──────────────┐          │
│   │ VLA Models   │    →    │ Domain Rand  │   →   │ Hardware     │          │
│   │ Learning     │         │ Calibration  │       │ Labs         │          │
│   │ Control      │         │ Reality Gap  │       │ Capstone     │          │
│   └──────────────┘         └──────────────┘       └──────────────┘          │
│                                   ↑                      ↑                   │
│                            Cannot skip             Cannot skip               │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Pacing Options

- **Self-Paced** (Default): Progress at your own speed, competency-based advancement
- **Cohort Tracks**: Optional structured learning with peers and deadlines
- **Estimated Durations**: Provided per stage as guidance, not requirements
- **Challenge Pathway**: Experienced learners may demonstrate competency to advance

## Community & Collaboration

Robotics is inherently collaborative. IntelliStack fosters community through:

### Peer Learning
- **Code Reviews**: Learners review each other's robot code—reading others' code is a skill
- **Study Groups**: Self-organized groups for mutual support and accountability
- **Discussion Forums**: Q&A spaces organized by topic and stage

### Team Projects
- **Group Capstones**: Optional team-based final projects reflecting real robotics teams
- **Role Specialization**: Experience different team roles (perception, planning, integration)
- **Collaboration Tools**: Shared simulation environments and version control

### Mentorship
- **Peer Mentors**: Advanced learners guide beginners through early stages
- **Expert Office Hours**: Access to instructors and industry practitioners
- **Alumni Network**: Graduates stay connected and support new learners

### Open Sharing
- **Project Showcase**: Public gallery of completed projects (opt-in)
- **Knowledge Contributions**: Learners can contribute tutorials and solutions
- **Community Challenges**: Optional competitions and hackathons

## Certification & Credentials

### Stage Completion Badges
- Digital, verifiable badges for each completed stage
- Badges display specific competencies demonstrated
- Shareable on LinkedIn and professional profiles

### IntelliStack Certificate
- Awarded upon successful capstone project completion
- Requires demonstration of integrated skills across all stages
- Includes portfolio of projects as primary proof of competency

### Assessment Types
- **Practical Assessments**: Demonstrate skills through working projects
- **Oral Explanations**: Explain your robot's behavior (tests understanding)
- **Peer Evaluations**: Community feedback on project quality

### Verification
- All credentials are digitally signed and verifiable
- Employer verification portal available
- Transcript of completed modules and assessments

## Career Pathways

### Post-Completion Paths

IntelliStack prepares learners for multiple career directions:

| Pathway | Description | Key Skills |
|---------|-------------|------------|
| **Industry Engineer** | Robotics companies, automation firms | Production systems, reliability |
| **Research** | Academic labs, R&D departments | Novel algorithms, publications |
| **Entrepreneurship** | Robotics startups, consulting | Product development, business |
| **Education** | Teaching, content creation | Communication, curriculum design |

### Industry Connections
- **Job Board**: Curated robotics job listings from partner companies
- **Internship Pipeline**: Connections to internship opportunities
- **Hiring Events**: Virtual career fairs with robotics employers
- **Portfolio Reviews**: Feedback from industry practitioners

### Continued Learning
- **Advanced Specializations**: Deep-dive tracks (manipulation, legged robots, etc.)
- **Research Tracks**: Paths toward graduate studies
- **Alumni Resources**: Continued access to learning materials and community

## Technical Requirements

### Minimum System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Ubuntu 22.04 / Windows WSL2 | Ubuntu 22.04 native |
| CPU | 4 cores | 8+ cores |
| RAM | 16 GB | 32 GB |
| GPU | Optional (cloud available) | NVIDIA RTX 3060+ for Isaac Sim |
| Storage | 50 GB free | 100 GB SSD |

### Cloud Options
- Cloud simulation available for learners without capable hardware
- GPU instances provided for Isaac Sim exercises
- No learner blocked by hardware limitations

### Supported Platforms
- **Simulation**: Gazebo Harmonic, NVIDIA Isaac Sim
- **Robot Categories**: Educational arms, mobile bases, humanoid simulations
- **Principle**: Platform-agnostic skills—learn concepts that transfer across robots

Detailed platform specifications maintained in separate curriculum documentation.

## Intellectual Property & Licensing

### Student Ownership
- **Students own their projects**—IntelliStack claims no IP rights
- Work created during the course belongs to the learner
- Commercial use of student projects is permitted

### Recommended Licenses
- **Code**: MIT or Apache 2.0 (permissive, industry-friendly)
- **Documentation/Content**: CC-BY 4.0 (attribution required)
- **Models/Weights**: Specify license of any pre-trained models used

### Open Source Encouraged
- Open source sharing is encouraged but not required
- Public projects build reputation and help the community
- Private projects respected for competitive or commercial reasons

### Platform Content
- IntelliStack course content is proprietary unless otherwise stated
- Learners may not redistribute course materials
- Community contributions follow contributor license agreement

## Data Privacy

### Core Privacy Principles
- **Minimal Collection**: Only data necessary for learning outcomes
- **Transparency**: Clear explanation of what data is collected and why
- **Student Control**: Learners control visibility of their projects and profiles
- **No Sale of Data**: Student data is never sold to third parties

### Learning Analytics
- Analytics used to improve content and personalize learning
- Aggregated, anonymized data may inform platform improvements
- Detailed analytics are opt-in with clear purpose explanation

### Data Handling
- Project submissions stored securely with learner access
- Video/sensor recordings from labs require explicit consent
- Data retention policies clearly documented
- GDPR and applicable privacy law compliance

### Deletion Rights
- Learners may request deletion of their data
- Account deletion removes personal information
- Anonymized learning patterns may be retained for research

## Industry Alignment

### Advisory Board
- Industry practitioners review curriculum annually
- Emerging technology trends incorporated within one academic term
- Employer feedback on graduate readiness shapes content updates

### Curriculum Reviews
- Quarterly review of job market requirements
- Tool and framework updates tracked and incorporated
- Deprecated technologies phased out with migration paths

### Practitioner Content
- Guest lectures from industry experts
- Real-world case studies from practicing engineers
- Industry project examples with permission

### Skills Mapping
- Curriculum mapped to industry job requirements
- Gap analysis identifies missing skills for employability
- Continuous alignment with robotics industry standards

## Knowledge Evolution

IntelliStack improves continuously through reusable knowledge and AI tools.

### Knowledge Capture
- Common student questions are captured and answered in the knowledge base
- Successful project patterns become templates for future learners
- Debugging solutions are documented for similar issues
- AI tutoring conversations that help understanding are preserved (anonymized)

### AI Tool Integration
- AI assistants learn from aggregated (anonymous) learning patterns
- Content recommendations improve based on student outcomes
- Simulation environments auto-generate variations for practice
- Assessment AI adapts difficulty based on demonstrated mastery

### Feedback Loops
- Student project outcomes inform curriculum updates
- Instructor feedback shapes content improvements
- Industry advisory input keeps content relevant to job requirements
- Research advances are incorporated within one academic term

### Version Control
- All course content is version controlled
- Changes are tracked and can be audited
- Previous versions remain accessible for reference
- Breaking changes to curriculum require migration guides

## Quality Standards

### Content Quality

All educational content MUST meet these standards:

- **Accuracy**: Technical content is reviewed by subject matter experts
- **Clarity**: Concepts are explained for the target audience level
- **Completeness**: No assumed knowledge without explicit prerequisites
- **Currency**: Content is updated within 6 months of major tool releases
- **Accessibility**: Content works with screen readers and has captions for video

### Project Quality

Student projects MUST demonstrate:

- **Functionality**: The project runs and produces expected outputs
- **Documentation**: README explains purpose, setup, and usage
- **Code Quality**: Code follows language conventions and is readable
- **Safety**: Hardware projects include safety documentation
- **Testing**: Critical functions have tests or validation procedures
- **Ethics**: Projects include ethical considerations where applicable

### Assessment Quality

Assessments MUST be:

- **Fair**: Clearly tied to stated learning objectives
- **Practical**: Focus on applied skills over memorization
- **Gradable**: Have clear rubrics for evaluation
- **Constructive**: Provide feedback that aids learning
- **Secure**: Resistant to gaming or shortcut-taking

## Governance

### Constitution Authority

This constitution is the authoritative source for IntelliStack's principles and
standards. All course content, assessments, and platform features MUST align with
these principles.

### Amendment Process

1. Proposed amendments are submitted with rationale and impact assessment
2. Core team reviews and discusses the proposal
3. Stakeholder feedback is collected (students, educators, institutions)
4. Amendments require approval from curriculum leadership
5. Approved amendments are documented with version increment
6. Migration guides are provided for impacted content

### Compliance

- All new content undergoes constitution compliance review before publishing
- Existing content is audited annually for continued compliance
- Non-compliant content is flagged and remediated within 30 days
- Repeated non-compliance triggers root cause analysis

### Versioning Policy

- **MAJOR** version: Changes to core principles or learning path structure
- **MINOR** version: New sections, expanded guidance, new stakeholder requirements
- **PATCH** version: Clarifications, typo fixes, formatting improvements

**Version**: 2.1.0 | **Ratified**: 2026-02-07 | **Last Amended**: 2026-02-07
