# Agent-Guided Learning Workflow Design

## Status

Approved in conversation on 2026-07-10.

This specification defines how Codex and the user collaborate on the Trading Mentor Agent project.

It governs the repository instructions, project skill, session continuity, learning workflow, documentation, and commit behavior.

The product roadmap will be redesigned only after this workflow is implemented and verified.

## Context

The project has two connected goals.

It should become a trustworthy personal trading mentor that helps the user understand market information and make informed decisions.

It should also become a recruiter-quality demonstration of agentic engineering that the user can explain and defend.

The user can read Python, understands asynchronous programming and APIs at a high level, and knows the basic Red-Green-Refactor testing cycle.

The main learning goal is architectural judgment, including boundaries, state, orchestration, persistence, failure handling, evaluation, observability, and trade-offs.

The user starts a fresh Codex conversation for each IDE session to avoid carrying unnecessary context.

The repository therefore needs compact, durable, and authoritative session state.

## Goals

- Make the user responsible for consequential architectural decisions.
- Use a Socratic workflow in which the user reasons before Codex recommends or implements.
- Let Codex handle routine implementation details after the architectural direction is approved.
- Preserve fast startup across fresh conversations without rereading historical logs.
- Record durable decisions, genuine lessons, and factual session history in separate places.
- Keep normal verification deterministic and isolate live external-service evaluations.
- Produce verified atomic commits automatically.
- Keep repository content in English for professional presentation.
- Prevent trading recommendations when required evidence is missing or stale.

## Non-Goals

- Quiz the user about routine syntax, formatting, or mechanical implementation details.
- Preserve a framework solely because it already exists in the repository.
- Optimize for multiple users before the personal single-user product requires it.
- Make the session workflow portable to coding agents other than Codex.
- Load the entire project history into every fresh conversation.
- Treat prompts as sufficient enforcement for financial safety requirements.

## Instruction Architecture

The workflow uses three responsibility layers.

### Root `AGENTS.md`

The root instruction file is the stable project constitution.

It defines the product purpose, user authority, engineering standards, financial-safety invariants, verification expectations, documentation map, and commit rules.

It must remain concise because Codex loads it as durable repository guidance.

### Project Skill

The repository-scoped skill lives at `.agents/skills/trading-mentor-session/`.

The skill owns the repeatable session procedure, including orientation, Socratic decision gates, implementation handoff, explanation, session closure, and logging.

The skill is implicitly available for development, architecture, planning, debugging, and implementation work in this repository.

The skill should be instruction-focused and should add scripts only when deterministic automation is proven necessary.

### Project Documentation

Documentation stores mutable state and historical evidence.

Instructions describe how to work, while documentation records what is currently true and why prior decisions were made.

## Session Lifecycle

### Session Start

Codex reads `docs/CURRENT_STATE.md`, the active milestone in `docs/ROADMAP.md`, recent Git status, and only relevant architectural decision records.

Codex opens with the current product state, the last verified milestone, known risks or unfinished work, and the recommended next architectural decision.

Historical session logs are not required startup reading.

### Consequential Decisions

Codex asks the user to propose an approach before presenting its own recommendation.

Codex evaluates the reasoning directly, identifies missing trade-offs or unsupported assumptions, and asks focused follow-up questions until the choice is defensible.

Codex may supply technical evidence and alternatives, but the user makes the final consequential decision.

Consequential decisions include orchestration, state ownership, persistence, provider boundaries, data contracts, safety policy, deployment, observability, and evaluation strategy.

Routine implementation choices remain Codex's responsibility unless they expose a meaningful architectural trade-off.

Durable decisions receive lightweight architectural decision records.

### Implementation

After the user approves the direction, Codex defines the smallest coherent product slice and its test contract.

Codex implements the slice autonomously using Red-Green-Refactor for behavior changes.

Normal tests remain deterministic.

Tests that call Gemini, market-data providers, Telegram, or cloud services are explicitly marked and run only as intentional milestone evaluations.

After verification, Codex explains how the implementation realizes the user's decision and discloses lower-level trade-offs it resolved autonomously.

### Session End

Codex refreshes `docs/CURRENT_STATE.md` automatically.

Codex appends a dated session record, updates roadmap progress, and records only genuine reusable knowledge in `docs/LESSONS_LEARNED.md`.

Codex creates one or more verified atomic commits for coherent milestones.

Codex does not mix unrelated cleanup, features, and documentation decisions in one commit.

Unrelated user changes and unverified work remain uncommitted and are recorded clearly in the session handoff.

## Documentation Model

The authoritative documentation structure is:

```text
docs/
  CURRENT_STATE.md
  ROADMAP.md
  LESSONS_LEARNED.md
  decisions/
    ADR-0001-<decision>.md
  sessions/
    YYYY-MM-DD-<sequence>.md
  specs/
    YYYY-MM-DD-<topic>-design.md
  legacy/
    implementation_plan.md
    NOTES.md
```

`CURRENT_STATE.md` is a compact startup snapshot that is overwritten after each session.

`ROADMAP.md` is the only authoritative forward plan.

`sessions/` contains factual historical records that are not required startup context.

`decisions/` contains durable choices, alternatives, trade-offs, and consequences.

`LESSONS_LEARNED.md` contains curated reusable knowledge rather than progress notes.

`legacy/` contains explicitly historical material that no longer directs future work.

`specs/` contains approved designs written before implementation.

The existing implementation plan and notes move into `legacy/` and receive clear historical labels.

## Product and Technology Principles

The project uses a balanced curriculum model.

Architecture must earn its place, while meaningful opportunities to learn agentic engineering should remain visible and deliberate.

LangGraph, Gemini, Telegram, and JSON are starting points rather than permanent constraints.

Replacing an existing technology requires evidence, trade-off analysis, and a durable decision record when the consequences extend beyond the session.

The provisional deployment direction is a request-based Google Cloud Run service using Telegram webhooks and scale-to-zero behavior.

The target operating cost is zero under normal personal usage, with billing safeguards and constrained scaling.

Persistent storage remains a future architectural decision because Cloud Run's local filesystem is disposable.

## Trading Safety Invariant

The system may explain data, teach concepts, produce conditional scenarios, and provide direct recommendations only as evidence quality increases.

Direct recommendations require fresh and complete market data, portfolio context, and explicit risk controls.

If required evidence is missing or stale, the system must state the limitation and withhold the recommendation.

This invariant must be enforced by application logic and evaluation, not only by an LLM prompt.

## Skill Validation

The project skill follows a Red-Green-Refactor validation cycle for process documentation.

Before the skill is written, fresh agents are tested without it against pressure scenarios that tempt them to skip user reasoning, session orientation, verification, logging, atomic commits, or trading-safety gates.

Observed baseline failures determine the minimal skill content.

The same scenarios are rerun with the skill available.

Any new rationalizations or missed workflow steps are corrected and retested.

The skill structure is validated with the skill-authoring validation tool before adoption.

## Migration

The existing `.agents/AGENTS.md` is replaced by the tracked root `AGENTS.md`.

The existing `interactive-learning` and `knowledge-logging` skills are removed after their useful rules are incorporated into `trading-mentor-session`.

The `.agents` directory is removed from `.gitignore` so repository-scoped skills are versioned and available after a fresh clone.

The old plan and notes are preserved under `docs/legacy/`.

The new product roadmap is created only after the instruction system and session skill are verified.

## Acceptance Criteria

- A fresh Codex conversation can orient itself from compact current documentation.
- Codex asks the user to reason before consequential architectural implementation.
- Codex critiques weak reasoning directly and records durable decisions.
- Routine implementation proceeds autonomously after approval.
- Deterministic tests remain separate from live external-service evaluations.
- Session state, history, lessons, and decisions have distinct authoritative locations.
- The new skill passes baseline pressure scenarios that fail without it.
- The root instructions and project skill are tracked in Git.
- Verified milestones produce atomic commits automatically.
- The product roadmap clearly supersedes the legacy implementation plan.
