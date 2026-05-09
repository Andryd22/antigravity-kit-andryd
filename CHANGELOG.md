# Changelog

All notable changes to the Antigravity Kit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.1.0] - 2026-05-10

### Added

- **New Agents (5)**:
    - `api-designer` — REST, GraphQL, OpenAPI, tRPC contract-first API design
    - `ai-ml-engineer` — LLM integration, RAG pipelines, prompt engineering, AI app development
    - `data-engineer` — ETL/ELT pipelines, dbt, Airflow, data warehousing
    - `embedded-engineer` — Arduino, ESP32, STM32, FreeRTOS, IoT sensors
    - `latex-specialist` — Academic LaTeX chapter generation and project auditing
- **New Skills (9)**:
    - `nestjs-expert` — NestJS modules, DI, guards, interceptors
    - `prisma-expert` — Prisma ORM schema design, migrations, performance
    - `typescript-expert` — Advanced type-level programming, generics, branded types
    - `docker-expert` — Multi-stage builds, Docker Compose, security hardening
    - `prompt-engineering` — LLM prompts, RAG architecture, embedding strategies
    - `data-engineering` — Pipeline patterns, orchestration, data quality
    - `embedded-systems` — MCU, RTOS, MQTT, sensors, power management
    - `latex_tutor` — University-level LaTeX chapter generation from slides
    - `latex_review` — Comprehensive LaTeX project audit and QA
- **New Scripts (2)**:
    - `dependency_analyzer.py` — npm/pip dependency vulnerability scanning
    - `bundle_analyzer.py` — Bundle size analysis, chunk inspection, duplicate detection
- **New File**: `.agent/tasks/lessons.md` — Pattern capture template for agent learning

### Changed

- **Architecture Overhaul (Phase 1)**:
    - Consolidated agent routing into `intelligent-routing/SKILL.md` as single source of truth
    - Trimmed `GEMINI.md` from 273 to ~148 lines, delegated routing with `always_on` rule
    - Removed duplicate agent selection matrices from `orchestrate.md` and `orchestrator.md`
    - Standardized all agent frontmatters to consistent format
- **Quality Enhancement (Phase 2)**:
    - Added concrete EXAMPLE blocks to 7 thin agents with real input/output scenarios
    - Added domain-specific "Never Invent" anti-hallucination guards to all agents
    - Added Review Checklist sections to agents missing them
    - Reduced agent↔skill redundancy in 3 high-overlap pairs (devops, database, frontend)
- **Documentation**:
    - Updated `AGENT_FLOW.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, `README.md`
    - All counts and agent/skill tables updated

### Fixed

- Fixed `debugger.md` missing tools array (was empty `[]`)
- Fixed `explorer-agent.md` invalid tool names (`ViewCodeItem`, `FindByName`)
- Fixed `code-archaeologist.md` missing `Bash` tool
- Fixed phantom skill references in `ARCHITECTURE.md` (`react-best-practices` → `nextjs-react-expert`)

## [2.0.2] - 2026-02-04
- **New Skills**:
    - `rust-pro` - Master Rust 1.75+ 
- **Agent Workflows**:
    - Updated `orchestrate.md` fix output turkish


## [2.0.1] - 2026-01-26

### Added

- **Agent Flow Documentation**: New comprehensive workflow documentation
    - Added `.agent/AGENT_FLOW.md` - Complete agent flow architecture guide
    - Documented Agent Routing Checklist (mandatory steps before code/design work)
    - Documented Socratic Gate Protocol for requirement clarification
    - Added Cross-Skill References pattern documentation
- **New Skills**:
    - `react-best-practices` - Consolidated Next.js and React expertise
    - `web-design-guidelines` - Professional web design standards and patterns

### Changed

- **Skill Consolidation**: Merged `nextjs-best-practices` and `react-patterns` into unified `react-best-practices` skill
- **Architecture Updates**:
    - Enhanced `.agent/ARCHITECTURE.md` with improved flow diagrams
    - Updated `.agent/rules/GEMINI.md` with Agent Routing Checklist
- **Agent Updates**:
    - Updated `frontend-specialist.md` with new skill references
    - Updated `qa-automation-engineer.md` with enhanced testing workflows
- **Frontend Design Skill**: Enhanced `frontend-design/SKILL.md` with cross-references to `web-design-guidelines`

### Removed

- Deprecated `nextjs-best-practices` skill (consolidated into `react-best-practices`)
- Deprecated `react-patterns` skill (consolidated into `react-best-practices`)

### Fixed

- **Agent Flow Accuracy**: Corrected misleading terminology in AGENT_FLOW.md
    - Changed "Parallel Execution" → "Sequential Multi-Domain Execution"
    - Changed "Integration Layer" → "Code Coherence" with accurate description
    - Added reality notes about AI's sequential processing vs. simulated multi-agent behavior
    - Clarified that scripts require user approval (not auto-executed)

## [2.0.0] - Unreleased

### Initial Release

- Initial release of Antigravity Kit
- 20 specialized AI agents
- 37 domain-specific skills
- 11 workflow slash commands
- CLI tool for easy installation and updates
- Comprehensive documentation and architecture guide

[Unreleased]: https://github.com/vudovn/antigravity-kit/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/vudovn/antigravity-kit/releases/tag/v2.0.0
