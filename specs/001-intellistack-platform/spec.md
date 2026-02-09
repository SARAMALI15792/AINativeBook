# Feature Specification: IntelliStack Platform

**Feature Branch**: `001-intellistack-platform`
**Created**: 2026-02-07
**Status**: Draft
**Input**: Comprehensive platform specification for AI-native textbook platform for Physical AI & Humanoid Robotics course

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Student Learning Journey (Priority: P1)

A student progresses through the complete 5-stage learning path from foundational concepts to capstone project, demonstrating mastery at each stage before advancement. The journey follows the "simulation before hardware" principle, ensuring safe, iterative skill development.

**Why this priority**: The student learning experience is the core value proposition of IntelliStack. Without effective student outcomes, the platform has no purpose. This story encompasses the primary user flow that all other features support.

**Independent Test**: Can be fully tested by enrolling a test student, completing all 5 stages with assessments, and verifying certification issuance. Delivers complete educational value as a standalone experience.

**Acceptance Scenarios**:

1. **Given** a new student with no prior robotics experience, **When** they complete the diagnostic assessment, **Then** they receive a personalized learning path recommendation with prerequisite gaps identified.

2. **Given** a student in Stage 2 (ROS 2 Basics), **When** they complete all required exercises and pass the stage assessment with ≥70% score, **Then** Stage 3 content is unlocked and a stage completion badge is issued.

3. **Given** a student attempting Stage 3 content without completing Stage 2, **When** they try to access Stage 3 materials, **Then** they see a clear message explaining prerequisites and their current progress toward unlocking.

4. **Given** a student in any simulation stage (1-4), **When** they request to skip to hardware content, **Then** the system explains the simulation-first requirement and shows their simulation checkpoint status.

5. **Given** a student who has completed all 5 stages and passed the capstone project, **When** they view their profile, **Then** they see the IntelliStack Certificate with all earned badges and a shareable portfolio link.

---

### User Story 2 - Author Content Creation (Priority: P2)

A subject matter expert creates, versions, and publishes course content including lessons, exercises, simulations, and assessments. The authoring system supports AI-assisted content creation while maintaining quality standards and version control.

**Why this priority**: Content quality directly determines student outcomes. Authors need efficient tools to keep material current with rapidly evolving robotics technology. This enables the platform to scale and stay relevant.

**Independent Test**: Can be tested by having an author create a complete lesson module with exercises, submit for review, receive feedback, and publish. Delivers content creation capability independent of other features.

**Acceptance Scenarios**:

1. **Given** an approved author with credentials, **When** they create a new lesson in Stage 3 (Simulation Mastery), **Then** they can add text content, code examples, embedded simulations, and learning objectives using the authoring interface.

2. **Given** an author editing existing content, **When** they save changes, **Then** a new version is created with change history preserved, and the previous version remains accessible.

3. **Given** an author submitting content for review, **When** a reviewer approves the content, **Then** it becomes available to students with appropriate version tagging.

4. **Given** an author creating an assessment, **When** they define questions and rubrics, **Then** the system validates that learning objectives are mapped and provides coverage analysis.

5. **Given** a breaking change in ROS 2 or simulation platform, **When** an author updates affected content, **Then** students currently in that module receive notification of updated materials.

---

### User Story 3 - Institution Administration (Priority: P3)

An institution administrator enrolls students in cohorts, customizes branding, manages instructor access, and monitors learning analytics for their organization. The institution maintains autonomy over their learners while leveraging IntelliStack's platform.

**Why this priority**: Institutional adoption drives sustainable growth and provides structured learning environments. Institutions need control over their cohorts and visibility into outcomes for accreditation and quality assurance.

**Independent Test**: Can be tested by creating an institution account, enrolling a cohort of test students, assigning instructors, and generating analytics reports. Delivers institutional management independent of content authoring.

**Acceptance Scenarios**:

1. **Given** an institution administrator, **When** they create a new cohort for Spring 2026, **Then** they can set enrollment limits, start/end dates, and assign instructors to the cohort.

2. **Given** an institution with enrolled students, **When** an administrator views the dashboard, **Then** they see aggregate progress metrics, completion rates, and at-risk student indicators.

3. **Given** an institution with custom branding requirements, **When** they configure branding settings, **Then** their students see institution logo, colors, and custom welcome messaging.

4. **Given** an instructor assigned to a cohort, **When** they access cohort management, **Then** they can view individual student progress, send announcements, and schedule office hours.

5. **Given** an administrator generating compliance reports, **When** they request a completion report, **Then** they receive detailed data on student progress, time-on-task, and assessment scores suitable for accreditation review.

---

### User Story 4 - AI Tutor Interaction (Priority: P4)

A student receives guided assistance from the AI tutor that promotes understanding without providing direct answers. The AI asks clarifying questions, offers hints, explains concepts, and helps debug code while maintaining the "understanding before automation" principle.

**Why this priority**: The AI tutor differentiates IntelliStack from traditional learning platforms. It embodies the constitution's principle of AI as learning guide, ensuring students develop genuine competency rather than dependency.

**Independent Test**: Can be tested by simulating student-AI conversations across various scenarios (concept explanation, debugging help, hint requests) and verifying pedagogically appropriate responses. Delivers tutoring value independent of other features.

**Acceptance Scenarios**:

1. **Given** a student stuck on a ROS 2 concept, **When** they ask the AI tutor for help, **Then** the tutor asks clarifying questions about what the student has tried and what they understand so far.

2. **Given** a student requesting code to solve an exercise, **When** they ask "give me the code," **Then** the AI tutor declines to provide complete solutions and instead offers to explain the approach or review their attempt.

3. **Given** a student with a bug in their simulation code, **When** they share their code with the AI tutor, **Then** the tutor guides them through systematic debugging (reproduce, isolate, hypothesize) rather than fixing it directly.

4. **Given** a student who has demonstrated understanding of a concept, **When** they request code assistance, **Then** the AI tutor provides more direct help, recognizing their competency level.

5. **Given** a student asking about content beyond their current stage, **When** they inquire about Stage 5 topics while in Stage 2, **Then** the AI tutor explains the progressive learning path and redirects to current stage focus.

---

### User Story 5 - Community Collaboration (Priority: P5)

Students engage with peers through forums, study groups, peer review of projects, and mentorship connections. The community fosters collaborative learning while maintaining academic integrity and constructive discourse.

**Why this priority**: Community learning accelerates outcomes and builds professional networks. Peer interaction reinforces learning and prepares students for collaborative robotics team environments. Lower priority because core learning can occur without it.

**Independent Test**: Can be tested by creating forum posts, forming study groups, submitting projects for peer review, and matching mentors with mentees. Delivers community value as an enhancement to individual learning.

**Acceptance Scenarios**:

1. **Given** a student in Stage 3, **When** they post a question in the Stage 3 forum, **Then** peers and mentors in Stage 3+ can respond, and the student receives notification of replies.

2. **Given** a student creating a study group, **When** they invite classmates, **Then** the group gets a shared space for discussions, resource sharing, and scheduled video sessions.

3. **Given** a student submitting a project for peer review, **When** two peers complete their reviews using the provided rubric, **Then** the student receives aggregated feedback with specific improvement suggestions.

4. **Given** an advanced student (Stage 5+) opting into mentorship, **When** a Stage 1 student requests a mentor, **Then** the system suggests compatible matches based on interests and availability.

5. **Given** a community member violating conduct guidelines, **When** a moderator reviews the report, **Then** appropriate action is taken and the reporter receives notification of resolution.

---

### User Story 6 - RAG Chatbot Interaction (Priority: P3.5)

A student asks questions about textbook content and receives AI-generated answers with citations to specific chapters and sections. Students can highlight text and ask context-specific questions, with responses streaming in real-time for an interactive experience.

**Why this priority**: The RAG chatbot significantly enhances learning by providing instant, contextual answers grounded in course materials. It bridges the gap between static content and interactive tutoring, enabling deeper engagement with material. Positioned between institution administration (P3) and AI tutor (P4) because it directly supports learning but doesn't replace the pedagogical AI tutor.

**Independent Test**: Can be tested by submitting questions about various chapters, verifying citation accuracy, testing text selection queries, and measuring response streaming behavior. Delivers contextual search value independent of other features.

**Acceptance Scenarios**:

1. **Given** a student reading Stage 2 content, **When** they ask "How do ROS 2 topics differ from services?", **Then** they receive an answer with citations referencing the specific chapter and section where this is explained.

2. **Given** a student highlighting a code example in the textbook, **When** they ask "What does this line do?", **Then** the AI answers specifically about the selected text with context from surrounding content.

3. **Given** a student submitting a question, **When** the AI begins generating a response, **Then** the answer streams in real-time (character-by-character or chunk-based) rather than appearing all at once.

4. **Given** a student in Stage 3 with Stage 4 content locked, **When** they ask a question that would be answered by Stage 4 material, **Then** the system only searches accessible content and indicates if the full answer may be in later stages.

5. **Given** a student receiving an unsatisfactory RAG answer, **When** they indicate the answer didn't help, **Then** they are offered the option to escalate to the AI tutor or flag for instructor review.

---

### Edge Cases

- **Prerequisite Conflict**: What happens when curriculum updates change prerequisites for a stage a student has already started?
  - System allows completion of current stage; new prerequisites apply only to future enrollments.

- **Assessment Integrity Violation**: How does the system handle suspected cheating or plagiarism?
  - Automated similarity detection flags submissions; instructor review required before any action; student notified and given opportunity to respond.

- **Simulation Environment Failure**: What happens when cloud simulation resources are unavailable?
  - Graceful degradation to offline content; progress syncs when connection restores; students notified of affected features.

- **Institution Mid-Term Changes**: How does the system handle an institution changing cohort settings during active term?
  - Changes apply to new enrollments; existing students continue under original settings unless explicitly migrated.

- **AI Tutor Misuse Attempts**: What happens when a student persistently tries to extract direct answers?
  - Escalating guardrails: polite redirects → explanation of learning philosophy → temporary cooldown → instructor notification.

- **Experienced Learner Challenge Failure**: What happens if a challenge pathway assessment reveals gaps?
  - Detailed gap analysis provided; student placed at appropriate stage; partial credit for demonstrated competencies.

---

## Requirements *(mandatory)*

### Functional Requirements

#### Learning Management (FR-001 to FR-015)

- **FR-001**: System MUST enforce prerequisite completion before allowing access to subsequent stage content.

- **FR-002**: System MUST provide diagnostic assessment at enrollment to identify prerequisite gaps and recommend Stage 0 remediation if needed.

- **FR-003**: System MUST track learner progress at granular level (lesson, exercise, assessment) and persist across sessions.

- **FR-004**: System MUST support competency-based advancement where learners progress upon demonstrated mastery, not time elapsed.

- **FR-005**: System MUST issue digital badges for stage completion that are verifiable and shareable.

- **FR-006**: System MUST support both self-paced learning and cohort-based learning with deadlines.

- **FR-007**: System MUST provide estimated time-to-completion for each stage as guidance (not requirement).

- **FR-008**: System MUST allow learners to revisit completed content without affecting progress tracking.

- **FR-009**: System MUST notify learners of content updates in stages they have completed or are currently in.

- **FR-010**: System MUST support the Challenge Pathway allowing experienced learners to demonstrate competency and skip up to 3 consecutive Course Stages (excluding Course Stages 4 and 5, which map to constitution stages 6-8).

- **FR-011**: System MUST enforce safety content completion regardless of Challenge Pathway eligibility.

- **FR-012**: System MUST provide clear visualization of learning path progress showing completed, current, and locked stages.

- **FR-013**: System MUST support learning style preferences (video, text, interactive) and surface content in preferred format when available.

- **FR-014**: System MUST generate IntelliStack Certificate upon successful capstone completion with verification capability.

- **FR-015**: System MUST maintain learner portfolio of completed projects accessible for sharing with potential employers.

#### Content & Simulation (FR-016 to FR-025)

- **FR-016**: System MUST integrate with Gazebo simulation environment for Stages 1-4 exercises.

- **FR-017**: System MUST integrate with NVIDIA Isaac Sim for perception and advanced simulation exercises.

- **FR-018**: System MUST support ROS 2 (Humble/Iron) as the primary robotics middleware throughout the curriculum.

- **FR-019**: System MUST provide cloud-based simulation environments for learners without local GPU resources. Individual users have a default quota of 25 hours/month; institutions may negotiate custom quotas.

- **FR-020**: System MUST enforce simulation checkpoint completion before any hardware-related content access.

- **FR-021**: System MUST support embedded interactive simulations within lesson content (not just external links).

- **FR-022**: System MUST allow learners to save, restore, and share simulation states.

- **FR-023**: System MUST provide simulation environments that support domain randomization for sim-to-real transfer training.

- **FR-024**: System MUST include pre-configured robot models (educational arms, mobile bases, humanoid simulations) aligned with curriculum.

- **FR-025**: System MUST track simulation performance metrics (completion time, collision count, success rate) for assessment.

#### AI Components (FR-026 to FR-035)

- **FR-026**: System MUST provide conversational AI tutor accessible throughout the learning experience.

- **FR-027**: AI tutor MUST follow Socratic method—asking questions and providing hints rather than direct answers.

- **FR-028**: AI tutor MUST refuse to provide complete code solutions for exercises; guidance and debugging help are permitted.

- **FR-029**: AI tutor MUST adapt response depth based on learner's demonstrated understanding level (stage-appropriate explanations).

- **FR-030**: AI tutor MUST guide debugging using systematic methodology (reproduce → isolate → hypothesize → test → fix).

- **FR-031**: System MUST provide AI-assisted code review that explains issues and suggests improvements without auto-fixing.

- **FR-032**: System MUST use AI for personalized learning path recommendations based on progress patterns and assessment results.

- **FR-033**: AI components MUST log interactions for quality assurance and continuous improvement (with learner consent). Logs are retained for 30 days, then automatically purged.

- **FR-034**: AI tutor MUST maintain conversation context within a learning session for coherent multi-turn interactions.

- **FR-035**: System MUST provide AI guardrails that escalate to instructor notification after repeated attempts to circumvent learning guidelines.

#### User & Role Management (FR-036 to FR-042)

- **FR-036**: System MUST support distinct user roles: Student, Author, Instructor, Institution Admin, Platform Admin.

- **FR-037**: System MUST support role-based access control where permissions are determined by role assignment.

- **FR-038**: System MUST allow users to have multiple roles (e.g., an Author who is also an Instructor).

- **FR-039**: System MUST support institution-level user management with delegated administration. Users exist in a global identity pool and can be assigned to one or more institutions. Institutions can configure webhook URLs to receive event notifications (enrollments, progress milestones, assessment completions) with automatic retry on delivery failure.

- **FR-040**: System MUST maintain audit trail of role changes and administrative actions.

- **FR-041**: System MUST support account recovery and credential management workflows.

- **FR-042**: System MUST enforce session management with appropriate timeout and concurrent session policies.

#### Assessment System (FR-043 to FR-052)

- **FR-043**: System MUST support multiple assessment types: quizzes, practical projects, peer reviews, oral explanations.

- **FR-044**: System MUST require practical demonstration (working project) as primary assessment method, not just knowledge testing.

- **FR-045**: System MUST support rubric-based assessment with clear criteria visible to learners before submission.

- **FR-046**: System MUST implement the Understanding Verification Framework including: explain-without-code, predict-before-run, modification challenge, debugging scenario, and teaching-back methods.

- **FR-047**: System MUST support automated assessment for objective criteria (code execution, simulation performance) while routing subjective elements to human review.

- **FR-048**: System MUST provide detailed feedback on assessments explaining what was correct, what needs improvement, and how to improve.

- **FR-049**: System MUST support assessment retakes with configurable attempt limits and cooldown periods.

- **FR-050**: System MUST detect potential academic integrity violations through similarity analysis and flag for instructor review.

- **FR-051**: System MUST support peer review assignments with anonymization options and reviewer accountability.

- **FR-052**: System MUST require 10-item safety assessment completion before any hardware project (per constitution requirements).

#### Community Features (FR-053 to FR-058)

- **FR-053**: System MUST provide discussion forums organized by stage and topic with threading support.

- **FR-054**: System MUST support study group creation with shared resources, scheduling, and communication tools.

- **FR-055**: System MUST facilitate peer mentorship matching based on stage progression, interests, and availability.

- **FR-056**: System MUST provide moderation tools for community managers to maintain constructive discourse.

- **FR-057**: System MUST support project showcase where learners can optionally publish completed work.

- **FR-058**: System MUST provide notification system for forum replies, study group activity, and mentorship communications.

#### Quality & Safety (FR-059 to FR-065)

- **FR-059**: System MUST enforce content review workflow before any material is published to learners.

- **FR-060**: System MUST maintain content versioning with rollback capability.

- **FR-061**: System MUST meet accessibility standards allowing screen reader compatibility and keyboard navigation. Loading states use skeleton screens (placeholder shapes matching content layout) to reduce perceived wait time and prevent layout shift.

- **FR-062**: System MUST provide content in multiple formats where feasible (video captions, text alternatives).

- **FR-063**: System MUST enforce safety assessment requirements at stage-appropriate scope (simplified for simulation-only, full 10-item for hardware).

- **FR-064**: System MUST block hardware content access without completed safety prerequisites and safety briefing acknowledgment.

- **FR-065**: System MUST provide emergency contact information and safety resources accessible from any learning context.

#### RAG Chatbot System (FR-066 to FR-080)

- **FR-066**: System MUST allow students to ask questions about any content in the textbook corpus.

- **FR-067**: System MUST provide answers with citations referencing specific chapter and section.

- **FR-068**: System MUST allow students to select/highlight text and ask questions about that selection.

- **FR-069**: System MUST stream responses in real-time (character-by-character or chunk-based).

- **FR-070**: System MUST maintain conversation context across multiple questions in a session.

- **FR-071**: System MUST rank and retrieve relevant content from the corpus using semantic similarity.

- **FR-072**: System MUST indicate confidence level when answering questions.

- **FR-073**: System MUST handle cases where the answer is not in the corpus (acknowledge limitations).

- **FR-074**: System MUST support follow-up questions that reference previous answers.

- **FR-075**: System MUST allow students to view the source passages used to generate answers.

- **FR-076**: System MUST support both broad questions (cross-chapter) and narrow questions (specific section).

- **FR-077**: System MUST handle code-related questions with syntax-aware responses.

- **FR-078**: System MUST respect content access controls (only answer from stages student has unlocked).

- **FR-079**: System MUST log all RAG interactions for quality improvement (with consent).

- **FR-080**: System MUST provide option to escalate to human instructor if RAG answer is unsatisfactory.

#### Enhanced Personalization (FR-081 to FR-090)

- **FR-081**: System MUST collect user background profile (prior experience, learning goals, preferred pace).

- **FR-082**: System MUST provide per-chapter personalization button to generate tailored explanations.

- **FR-083**: System MUST adapt content complexity based on demonstrated user understanding.

- **FR-084**: System MUST support Urdu translation of content on-demand via toggle.

- **FR-085**: System MUST remember personalization preferences across sessions.

- **FR-086**: System MUST generate personalized exercise variations based on user's weak areas.

- **FR-087**: System MUST adjust example domains to match user's stated background (e.g., manufacturing vs research).

- **FR-088**: System MUST provide personalized learning time estimates based on user's pace history.

- **FR-089**: System MUST allow users to reset personalization and start fresh.

- **FR-090**: System MUST respect user privacy preferences for personalization data. Account deletion follows a 30-day soft delete policy: data is marked deleted immediately, user can recover within 30 days, and permanent purge occurs after 30 days.

#### Infrastructure & Deployment (FR-091 to FR-100)

- **FR-091**: System MUST provide setup scripts for local development environment.

- **FR-092**: System MUST support deployment on Ubuntu 22.04 LTS.

- **FR-093**: System MUST support NVIDIA RTX GPU workstations for local simulation.

- **FR-094**: System MUST support NVIDIA Jetson Orin edge devices for edge deployment.

- **FR-095**: System MUST support cloud GPU instances for simulation without local hardware.

- **FR-096**: System MUST provide containerized services for consistent deployment.

- **FR-097**: System MUST document hardware compatibility matrix.

- **FR-098**: System MUST support model export from cloud training to edge deployment.

- **FR-099**: System MUST provide automated CI/CD pipeline for content deployment.

- **FR-100**: System MUST support both staging and production environments.

#### Engineering Quality (FR-101 to FR-110)

- **FR-101**: System MUST implement structured logging for all services.

- **FR-102**: System MUST provide performance monitoring dashboards.

- **FR-103**: System MUST implement graceful error handling with user-friendly messages. When external services (AI, simulation, vector DB) are unavailable, the system degrades gracefully: affected features are disabled, cached content remains accessible, and a status banner informs users of limited functionality.

- **FR-104**: System MUST manage secrets securely (no hardcoded credentials).

- **FR-105**: System MUST scale horizontally to handle increased load.

- **FR-106**: System MUST provide health check endpoints for all services.

- **FR-107**: System MUST implement rate limiting to prevent abuse. Default limit: 60 requests/minute per authenticated user; unauthenticated requests limited to 10/minute.

- **FR-108**: System MUST maintain comprehensive API documentation.

- **FR-109**: System MUST provide database backup and recovery procedures.

- **FR-110**: System MUST implement request tracing for debugging.

#### Platform Deliverables (FR-111 to FR-115)

- **FR-111**: System MUST be deployable from a public repository.

- **FR-112**: System MUST include demo mode showcasing core features (≤90 second walkthrough).

- **FR-113**: System MUST include architecture documentation with component diagrams.

- **FR-114**: System MUST provide reusable agent components for extension.

- **FR-115**: System MUST support automated deployment via documented pipeline.

---

### Key Entities

#### User
Represents any person interacting with IntelliStack. Has profile information, authentication credentials, and role assignments.

**Attributes**:
- Unique identifier
- Profile (name, email, bio, avatar)
- Authentication credentials
- Role assignments (Student, Author, Instructor, Institution Admin, Platform Admin)
- Learning preferences
- Notification settings
- Institution affiliation (optional)

**Relationships**:
- A User may have multiple Roles
- A User (as Student) has one Progress record
- A User (as Student) belongs to zero or more Cohorts
- A User (as Author) creates zero or more Content items
- A User (as Instructor) manages zero or more Cohorts

---

#### Course
Represents the complete Physical AI & Humanoid Robotics curriculum organized into 5 stages with defined learning objectives and prerequisites.

**Attributes**:
- Version identifier
- Stage definitions (0-5 mapping to constitution's 0-8)
- Learning objectives per stage
- Prerequisite relationships
- Estimated duration per stage
- Badge definitions per stage

**Relationships**:
- A Course contains multiple Stages
- A Stage contains multiple Content items
- A Stage has prerequisite Stages
- A Stage defines multiple Assessments

**Stage Mapping** (Course Stages to Constitution stages):

> **Terminology Note**: "Course Stage" refers to the platform's 5-level progression (1-5). "Constitution Stage" refers to the 9-level pedagogical framework (0-8) in the IntelliStack Constitution. This distinction avoids confusion when referencing stage numbers.

| Course Stage | Constitution Stages | Focus |
|--------------|---------------------|-------|
| Course Stage 1: Foundations | 0-1 | Prerequisites, Python, Linux, Math |
| Course Stage 2: ROS 2 & Simulation | 2-3 | ROS 2 Basics, Gazebo, Isaac Sim |
| Course Stage 3: Perception & Planning | 4-5 | Computer Vision, Motion Planning, Navigation |
| Course Stage 4: AI Integration | 6-7 | VLA Models, Sim-to-Real Transfer |
| Course Stage 5: Capstone | 8 | Real Robot Projects, Integration |

---

#### Content
Represents learning materials including lessons, exercises, simulations, and supplementary resources.

**Attributes**:
- Unique identifier
- Content type (lesson, exercise, simulation, resource)
- Title and description
- Learning objectives addressed
- Stage assignment
- Version history
- Author attribution
- Review status (draft, in-review, published, archived)
- Format variants (video, text, interactive)

**Relationships**:
- Content belongs to one Stage
- Content is created by one or more Authors
- Content may have multiple Versions
- Content may embed Simulations
- Content maps to Learning Objectives

---

#### Assessment
Represents evaluation instruments including quizzes, projects, peer reviews, and practical demonstrations.

**Attributes**:
- Unique identifier
- Assessment type (quiz, project, peer-review, demonstration, safety-assessment)
- Title and instructions
- Rubric with criteria and weights
- Learning objectives assessed
- Passing threshold
- Attempt limits and cooldown
- Time limits (if applicable)

**Relationships**:
- Assessment belongs to one or more Stages
- Assessment evaluates specific Learning Objectives
- Assessment generates Submissions from Students
- Assessment may require Peer Reviews

---

#### Progress
Represents a student's advancement through the curriculum including completed content, assessment scores, and earned credentials.

**Attributes**:
- Student reference
- Content completion records (with timestamps)
- Assessment submission history and scores
- Badge achievements
- Current stage
- Cumulative metrics (time-on-task, completion rate)
- Portfolio of completed projects
- Certificate status

**Relationships**:
- Progress belongs to one Student
- Progress tracks completion of multiple Content items
- Progress records multiple Assessment submissions
- Progress earns multiple Badges
- Progress culminates in Certificate (upon capstone completion)

---

#### Community
Represents collaborative spaces including forums, study groups, and mentorship connections.

**Attributes**:
- Forum structure (categories, threads, posts)
- Study group definitions (members, resources, schedule)
- Mentorship pairs (mentor, mentee, status)
- Project showcase entries
- Moderation queue and actions

**Relationships**:
- Forums organized by Stage and Topic
- Study Groups contain multiple Users
- Mentorship connects two Users (mentor role, mentee role)
- Showcase entries link to User portfolios

---

#### RAGContext
Represents a RAG conversation session with retrieved passages and citations for the chatbot system.

**Attributes**:
- Session identifier
- User reference
- Conversation history (questions and answers)
- Retrieved passages with source references
- Active content scope (which chapters/sections accessible)
- Personalization settings active
- Confidence scores for answers
- Citation metadata

**Relationships**:
- RAGContext belongs to one User
- RAGContext references multiple Content items (retrieved passages)
- RAGContext respects Progress (content access controls)
- RAGContext may escalate to AI Tutor or Instructor

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

#### Learning Outcomes

- **SC-001**: 70% of enrolled students complete all 5 stages within 12 months of enrollment.

- **SC-002**: 80% of students who reach Stage 5 successfully complete their capstone project (passing grade on first or second attempt).

- **SC-003**: 85% of students report satisfaction rating of 4+ out of 5 in end-of-stage surveys.

- **SC-004**: Students demonstrate stage-appropriate understanding depth as measured by Understanding Verification Framework assessments (≥70% pass rate on first attempt).

- **SC-005**: Challenge Pathway learners (who test out of stages) perform equivalently to standard-path learners in subsequent stages (no statistically significant performance gap).

#### Platform Performance

- **SC-006**: Platform supports 10,000 concurrent simulation sessions without degradation.

- **SC-007**: Platform maintains 99.5% uptime during academic terms (August-May).

- **SC-008**: Page load times remain under 3 seconds for 95th percentile of requests.

- **SC-009**: AI tutor response time remains under 5 seconds for 95th percentile of queries.

#### Content & Quality

- **SC-010**: Authors publish content updates within 48 hours of significant technology changes (ROS releases, simulation platform updates).

- **SC-011**: 90% of content passes accessibility audit against established standards.

- **SC-012**: Peer review coverage reaches 80% of project submissions (at least 2 reviews per project).

#### Safety & Compliance

- **SC-013**: 100% of students accessing hardware content have completed safety assessments and briefing acknowledgment.

- **SC-014**: Zero safety incidents attributed to inadequate platform safety training.

#### Community & Engagement

- **SC-015**: 60% of students engage with community features (forums, study groups, or mentorship) at least once per month during active learning.

#### RAG Chatbot & Personalization

- **SC-016**: RAG chatbot provides accurate answers with correct citations for 90% of in-corpus questions.

- **SC-017**: Response streaming begins within 1 second of query submission.

- **SC-018**: Per-chapter personalization generates tailored content within 5 seconds.

#### Infrastructure & Deliverables

- **SC-019**: Setup scripts configure development environment successfully in under 30 minutes.

- **SC-020**: Technical documentation covers 100% of public APIs and deployment procedures.

- **SC-021**: Urdu translation produces comprehensible content for 95% of text passages.

---

## Clarifications

### Session 2026-02-07

- Q: How should authentication work across institutions - isolated tenants or shared identity? → A: Global identity + institution assignment (single user pool with users assigned to institution(s))
- Q: How long should AI conversation logs be retained? → A: 30 days (balance of privacy and operational debugging needs)
- Q: What should be the monthly simulation compute quota per user? → A: 25 hours/month (moderate; enough for casual learners)
- Q: What canonical term should be used for the 5-level course progression? → A: "Course Stage" (prefix distinguishes from constitution's 9-level stages)
- Q: What should happen when a user requests account deletion? → A: 30-day soft delete (data marked deleted, purged after 30 days; allows recovery)
- Q: What should be the default API rate limit per authenticated user? → A: 60 requests/minute (standard SaaS baseline)
- Q: What should the user experience be when external services fail? → A: Graceful degradation (disable affected features, show cached content, display status banner)
- Q: What loading pattern should be used for content fetching and async operations? → A: Skeleton screens (gray placeholder shapes matching expected content layout)
- Q: Should IntelliStack provide webhooks for institution event notifications? → A: Webhooks only (push events to institution-configured URLs; retry on failure)

---

## Assumptions

The following informed decisions were made where the original requirements were ambiguous:

1. **Stage Mapping**: The course condenses the constitution's 9 stages (0-8) into 5 stages for practical course delivery. This maintains the progression while fitting typical academic term structures.

2. **Assessment Passing Threshold**: A default of 70% passing threshold is assumed for most assessments, consistent with typical educational standards. This can be configured per assessment.

3. **Challenge Pathway Limits**: Maximum of 3 consecutive stages can be skipped via challenge pathway, balancing respect for prior learning with ensuring foundational coverage.

4. **AI Tutor Guardrails**: Escalation path (redirect → explain → cooldown → instructor notification) is assumed after 5 consecutive attempts to extract direct answers within a session.

5. **Peer Review Requirement**: Projects require 2 peer reviews for completion, balancing thoroughness with reviewer availability.

6. **Badge Portability**: Digital badges use open standards for portability and verification, specific standard selection deferred to implementation.

7. **Cloud Simulation Default**: Cloud simulation is the default for learners; local installation is optional for those with capable hardware.

8. **Content Review Workflow**: Content requires at least one reviewer approval before publication; emergency updates may use expedited single-reviewer process.

9. **Institution Branding Scope**: Institution customization includes logo, primary colors, and welcome messaging; deep structural customization is out of scope.

10. **Mentorship Matching**: Matching is suggestion-based; both parties must accept before mentorship is established.

11. **Urdu Translation Quality**: Urdu translation is AI-generated, not human-verified; quality may vary and users should verify critical content.

12. **Edge Deployment Optional**: Edge deployment (Jetson) is optional; cloud-first approach is the default for most users without local GPU hardware.

13. **Demo Video Source**: Demo video is generated from actual platform interactions, not a separate pre-recorded video; reflects live functionality.

14. **RAG Citation Granularity**: Citations reference chapter and section level; line-level citations are not guaranteed for all content types.

15. **Personalization Data Retention**: User personalization data is retained indefinitely unless explicitly reset by user or deleted per privacy request.

---

## Scope

### In Scope

- Complete 5-stage learning management system with prerequisite enforcement
- Integration with Gazebo and NVIDIA Isaac Sim simulation environments
- ROS 2 curriculum support (Humble/Iron distributions)
- AI conversational tutor with Socratic method guardrails
- AI-assisted code review (non-automatic fixing)
- Personalized learning path recommendations
- Multi-role user management (Student, Author, Instructor, Institution Admin, Platform Admin)
- Institution administration with cohort management and branding
- Assessment system supporting quizzes, projects, peer reviews, and practical demonstrations
- Understanding Verification Framework implementation
- Safety assessment requirements per constitution
- Community features: forums, study groups, peer mentorship, project showcase
- Digital badges and certificate issuance with verification
- Learner portfolio for completed projects
- Challenge Pathway for experienced learner advancement
- Content versioning and review workflow
- Accessibility compliance
- Learning analytics and progress tracking
- RAG chatbot with corpus search, citations, and streaming responses
- Per-chapter personalization and adaptive content complexity
- Language translation (Urdu via AI, expandable to other languages)
- Infrastructure setup automation (local development and cloud deployment)
- Demo mode and video capability for platform showcase
- Engineering quality standards (logging, monitoring, error handling)
- Reusable agent components for platform extension

### Out of Scope

- Physical robot hardware manufacturing or provisioning
- Hardware shipping or logistics
- Third-party LMS integration (Moodle, Canvas, Blackboard connectors)
- Mobile native applications (responsive web is in scope)
- Real-time collaborative coding (pair programming features)
- Job placement services (job board links may be provided, but not placement services)
- Payment processing and e-commerce (handled by separate system)
- Video conferencing (integration with external tools, not native video)
- Human-verified translations (AI translation only; quality may vary)
- Advanced analytics and business intelligence dashboards beyond standard progress reporting
- Custom institution-specific curriculum modifications (standard curriculum with pacing flexibility only)
- Integration with university student information systems (SIS)
- Proctoring services for assessments
- Physical textbook or printed materials production

---

## Constitution Alignment

This specification aligns with the IntelliStack Constitution v2.1.0 as follows:

| Constitution Principle | Specification Alignment |
|------------------------|------------------------|
| **I. Simulation Before Hardware** | FR-020 enforces simulation checkpoint completion; Stage mapping ensures Stages 1-4 are simulation-only; FR-064 blocks hardware access without simulation mastery |
| **II. Safety and Responsibility** | FR-052, FR-063, FR-064, FR-065 implement safety assessment requirements; SC-013, SC-014 measure safety compliance |
| **III. Understanding Before Automation** | FR-027, FR-028 enforce AI tutor Socratic method; FR-046 implements Understanding Verification Framework; AI refuses direct answers |
| **IV. AI as Learning Guide** | FR-026 through FR-035 define AI tutor behavior; FR-029 adapts to learner level; FR-035 provides guardrails with escalation |
| **V. Progressive Learning Path** | FR-001 through FR-012 implement staged progression; FR-010, FR-011 support Challenge Pathway with limitations |
| **VI. Practical Project Focus** | FR-044 requires practical demonstration; FR-015 maintains portfolio; FR-057 enables project showcase |
| **VII. Ethical AI & Responsible Robotics** | Addressed in curriculum content (out of spec scope); safety assessments include ethical considerations |
| **VIII. Embrace Failure, Master Debugging** | FR-030 guides systematic debugging; FR-048, FR-049 support learning from assessment failures |
| **IX. Sim-to-Real Mastery** | FR-023 supports domain randomization; Stage 4 explicitly covers sim-to-real transfer; FR-020 gates hardware access |

---

## Appendix: Learning Stage Details

### Stage 1: Foundations (Constitution Stages 0-1)

**Learning Objectives**:
- Complete diagnostic assessment and address prerequisite gaps
- Demonstrate Python proficiency for robotics applications
- Navigate Linux command line and development environment
- Apply linear algebra and calculus concepts to robotics problems
- Set up development environment with required tools

**Assessment Types**: Diagnostic quiz, coding exercises, environment setup verification

---

### Stage 2: ROS 2 & Simulation (Constitution Stages 2-3)

**Learning Objectives**:
- Create and manage ROS 2 nodes, topics, services, and actions
- Write and execute launch files for multi-node systems
- Build and simulate robots in Gazebo environment
- Configure sensors and physics in simulation
- Debug ROS 2 systems using standard tools

**Assessment Types**: ROS 2 practical projects, simulation exercises, debugging challenges

---

### Stage 3: Perception & Planning (Constitution Stages 4-5)

**Learning Objectives**:
- Implement computer vision pipelines for robot perception
- Use NVIDIA Isaac perception tools and pipelines
- Design motion planning solutions for robot arms
- Implement navigation for mobile robots
- Integrate perception with planning systems

**Assessment Types**: Perception projects, navigation challenges, integrated system demonstrations

---

### Stage 4: AI Integration (Constitution Stages 6-7)

**Learning Objectives**:
- Understand and apply Vision-Language-Action (VLA) models
- Implement learning-based control strategies
- Apply domain randomization techniques
- Calibrate sensors and handle reality gap
- Transfer simulation-trained models to real-world scenarios

**Assessment Types**: VLA integration project, sim-to-real transfer demonstration, domain randomization experiments

---

### Stage 5: Capstone (Constitution Stage 8)

**Learning Objectives**:
- Complete full 10-item safety assessment for hardware project
- Integrate skills from all previous stages into comprehensive project
- Demonstrate working robot system (simulation and/or hardware)
- Document project with portfolio-quality materials
- Present and defend project decisions

**Assessment Types**: Capstone project with safety assessment, oral defense, peer review, portfolio submission

**Requirements**: Safety briefing attendance, supervisor sign-off for hardware components, demonstration of integrated skills

---

## Appendix: Implementation Plan

### Technical Stack

| Attribute | Value |
|-----------|-------|
| **Frontend** | TypeScript, Next.js, Tailwind CSS, ShadCN UI, TanStack Query, Zustand |
| **Backend** | Python 3.11+, FastAPI, SQLAlchemy/SQLModel, Alembic |
| **AI/RAG** | OpenAI Agents SDK, LangGraph, LlamaIndex, Qdrant |
| **Database** | Neon PostgreSQL |
| **Auth** | Better-Auth (client + server SDK) |
| **Async** | Celery/Dramatiq + Redis |
| **Content** | Docusaurus (MDX) |
| **DevOps** | Docker, GitHub Actions, Vercel (frontend), Fly.io (backend) |

---

### System Architecture

```
┌─────────────────┐     ┌─────────────────┐
│  Next.js (Vercel)│     │ Docusaurus MDX  │
│  Frontend        │     │ Content Platform│
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │   FastAPI Gateway     │
         │   + Better-Auth       │
         └───────────┬───────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼───┐  ┌────────▼────────┐  ┌────▼────┐
│ Auth  │  │ Core Services   │  │   AI    │
│Service│  │ • Learning      │  │Services │
│       │  │ • Content       │  │ • RAG   │
│       │  │ • Assessment    │  │ • Tutor │
│       │  │ • Community     │  │ • Pers. │
└───┬───┘  └────────┬────────┘  └────┬────┘
    │               │                │
    └───────────────┼────────────────┘
                    │
    ┌───────────────┼───────────────┐
    │               │               │
┌───▼────┐  ┌──────▼──────┐  ┌─────▼─────┐
│Postgres│  │    Redis    │  │  Qdrant   │
│ (Neon) │  │ Cache+Queue │  │ Vector DB │
└────────┘  └─────────────┘  └───────────┘
```

---

### Service Decomposition

| Service | FRs | Responsibility |
|---------|-----|----------------|
| **Auth** | FR-036–042 | Authentication, RBAC, sessions, audit |
| **Learning** | FR-001–015 | Progress, prerequisites, badges, certificates, challenge pathway |
| **Content** | FR-059–060 | Course/stage/content CRUD, versioning, review workflow |
| **Assessment** | FR-043–052 | Delivery, submissions, rubrics, peer review, similarity |
| **AI Tutor** | FR-026–035 | Socratic tutoring, debugging guidance, code review, guardrails |
| **RAG Chatbot** | FR-066–080 | Retrieval, citation, streaming, context management |
| **Personalization** | FR-081–090 | Profile, content adaptation, translation |
| **Community** | FR-053–058 | Forums, study groups, mentorship, moderation |
| **Simulation** | FR-016–025 | Gazebo/Isaac integration, state management |
| **Analytics** | FR-102, FR-110 | Metrics, dashboards, tracing |

---

### Project Structure

```
intellistack/
├── backend/
│   ├── src/
│   │   ├── main.py
│   │   ├── config/
│   │   ├── core/
│   │   │   ├── auth/
│   │   │   ├── learning/
│   │   │   ├── content/
│   │   │   ├── assessment/
│   │   │   ├── community/
│   │   │   ├── institution/
│   │   │   └── analytics/
│   │   ├── ai/
│   │   │   ├── tutor/
│   │   │   ├── rag/
│   │   │   ├── personalization/
│   │   │   └── shared/
│   │   ├── simulation/
│   │   ├── shared/
│   │   └── tasks/
│   ├── alembic/
│   └── tests/
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/
│   │   │   ├── (dashboard)/
│   │   │   │   ├── learn/
│   │   │   │   ├── assessments/
│   │   │   │   ├── ai/
│   │   │   │   ├── community/
│   │   │   │   └── admin/
│   │   │   └── (institution)/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── stores/
│   │   └── types/
│   └── tests/
│
├── content/                    # Docusaurus MDX
├── docker-compose.yml
└── .github/workflows/
```

---

### Key Data Models

#### Core Entities

- **User** → UserRole → Role → Institution → Cohort
- **Course** → Stage → Content → ContentVersion
- **Assessment** → Submission → Rubric
- **Progress** → Badge → UserBadge → Certificate
- **AIConversation** → AIMessage → RAGRetrieval
- **ForumCategory** → ForumThread → ForumPost
- **StudyGroup** → StudyGroupMember
- **Mentorship** (mentor ↔ mentee)

#### Vector Store (Qdrant)

Collection: `textbook_content`
- Embedding size: 1536 (OpenAI ada-002)
- Payload: content_id, stage_id, chapter, section, text, code_language

---

### AI Pipeline Architecture

#### RAG Pipeline

```
Query → Query Analyzer → Access Control Filter → Hybrid Search (Qdrant)
    → Re-ranking → Context Builder → Response Gen (GPT-4o) → Streaming SSE
    → Citation Formatter
```

#### AI Tutor Guardrails

```
User Request → Classify Intent →
  ├── Concept Question → Generate Socratic Response
  ├── Code Help → Guidance (no solutions)
  ├── Debugging → Systematic: reproduce→isolate→hypothesize→test
  └── Direct Answer Request → Guardrail Check →
        ├── Attempt 1-3: Polite redirect + explain philosophy
        ├── Attempt 4-5: Cooldown + alternatives offered
        └── Attempt 6+: Escalate to instructor
```

---

### Implementation Phases

#### Phase 1: Core Platform (Weeks 1-6)
- Project scaffolding, Docker, CI/CD
- Auth service (Better-Auth, RBAC)
- Content service (CRUD, versioning)
- Learning service (progress, prerequisites)
- Frontend: auth flows, dashboard, content viewer

#### Phase 2: Content & AI (Weeks 7-12)
- RAG pipeline (ingestion, Qdrant, retrieval)
- RAG chatbot UI (streaming, citations)
- AI Tutor (LangGraph agents, Socratic guardrails)
- Assessment service (quizzes, projects, rubrics)
- Content authoring (review workflow)

#### Phase 3: Full Features (Weeks 13-18)
- Community (forums, study groups, mentorship)
- Personalization (profiles, adaptation, Urdu)
- Institution admin (cohorts, branding)
- Simulation layer (Gazebo connector)
- Badges & certificates

#### Phase 4: Polish & Scale (Weeks 19-24)
- Analytics dashboards
- Performance optimization
- Security hardening
- Demo mode (≤90 second walkthrough)
- API documentation

---

### Critical Files

| File | Purpose |
|------|---------|
| `backend/src/config/settings.py` | Pydantic settings, env vars |
| `backend/src/core/auth/service.py` | Better-Auth + RBAC |
| `backend/src/ai/rag/pipelines/query_pipeline.py` | LangGraph RAG orchestration |
| `backend/src/ai/tutor/socratic_guardrails.py` | Guardrail logic (FR-027, FR-028) |
| `frontend/src/app/(dashboard)/learn/content/[id]/page.tsx` | Main content viewer |

---

### Risk Mitigations

| Risk | Mitigation |
|------|------------|
| RAG quality issues | Reranking pipeline, instructor escalation, quality monitoring |
| Simulation complexity | Abstraction layer, cloud-first, defer Isaac Sim |
| AI guardrail bypass | Multi-layer defense, red-teaming, instructor review queue |
| Database scaling | Connection pooling, read replicas, Neon auto-scaling |
| OpenAI rate limits | Response caching, request batching, multiple keys |

---

### ADR Candidates

1. **ADR-001**: Monorepo structure
2. **ADR-002**: Better-Auth vs NextAuth.js
3. **ADR-003**: LangGraph for AI orchestration
4. **ADR-004**: Qdrant for vector storage
5. **ADR-005**: Hybrid content storage (Git + Postgres)
6. **ADR-006**: WebSocket + SSE fallback for streaming
7. **ADR-007**: Cloud-first simulation integration
8. **ADR-008**: On-demand AI translation with caching

---

### Verification Plan

1. **Unit Tests**: pytest (backend), Vitest (frontend)
2. **Integration Tests**: API contract testing with actual DB
3. **E2E Tests**: Playwright for critical user journeys
4. **RAG Quality**: Automated evaluation with test question corpus
5. **Performance**: Load testing for 10k concurrent users (SC-006)
6. **Accessibility**: Automated audit (SC-011)

---

*End of Specification*
