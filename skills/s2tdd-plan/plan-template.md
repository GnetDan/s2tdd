<!-- Adapted from github/spec-kit (MIT). -->
# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]

**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/s2tdd-plan` command; its definition describes the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]

**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]

**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]

**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]

**Acceptance tests**: [where they live, e.g. tests/acceptance/ — one per scenario ID (convention: specs/WORKFLOW.md); which scenarios need a live service and become scripted checkpoints (run by the implementer), which few need a person (a verdict on feel or quality, open-ended exploration, a UX or design call, heavy benefit from the user's interaction, or a critical control gate) and become human checkpoints, and why; no human checkpoint repeats scripted inputs]

**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]

**Project Type**: [e.g., library/cli/web-service/mobile-app/compiler/desktop-app or NEEDS CLARIFICATION]

**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]

**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]

**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

[Gates determined based on constitution file]

## Project Structure

### Feature artifacts (intent record; frozen at close-out)

```text
specs/[###-feature]/
├── plan.md              # This file (/s2tdd-plan command output)
├── research.md          # Phase 0 output (/s2tdd-plan command)
├── data-model.md        # Phase 1 output (/s2tdd-plan command)
├── quickstart.md        # Phase 1 output (/s2tdd-plan command)
├── contracts/           # Phase 1 output (/s2tdd-plan command)
├── tasks.md             # /s2tdd-harden output — generated test-first (NOT created by /s2tdd-plan)
├── orchestration.md     # /s2tdd-harden output — packets, waves, judgment audit, dispatch protocol
├── handoff.md           # /s2tdd-harden output — the implementer prompt (pointers, scope, checkpoints)
├── validation.md        # /s2tdd-harden output — SC baselines + checkpoint results
├── run-ledger.md        # /s2tdd-harden skeleton — implementing sessions' running state (amendments, lease)
├── s1-wave-reports.md   # /s2tdd-implement output — each wave's report and its packets' reports
└── close-out.md         # /s2tdd-close output — delivered, deviations, where to look now
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
