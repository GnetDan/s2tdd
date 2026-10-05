<!-- Adapted from github/spec-kit (MIT). -->
# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Mandatory and test-first. The first task of every story writes that story's acceptance tests (one per scenario ID in spec.md; scenarios that need a live service become scripted CHECKPOINT rows, and only those that need a person, benefit heavily from the user's interaction, or are critical control gates become human CHECKPOINT rows) and they fail until the story lands. Every implementation task is preceded by a separate task that writes its test and shows it failing for the expected reason; no task writes and passes the same test. Tests are owned by test tasks — implementation tasks never edit them. Deterministic/mechanical components come first when tests are prioritized.

**Docs**: every implementation task is done only when README and docs/ still describe the app as it now is — updated concisely if the task changed behaviour, setup or commands. Docs describe the application, not its history: no change-log prose (git history is the decision log; an ADR only for a genuinely complex design).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

<!--
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.

  The /s2tdd-harden command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/

  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment

  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize [language] project with [framework] dependencies
- [ ] T003 [P] Configure linting and formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [ ] T004 Setup database schema and migrations framework
- [ ] T005 [P] Implement authentication/authorization framework
- [ ] T006 [P] Setup API routing and middleware structure
- [ ] T007 Create base models/entities that all stories depend on
- [ ] T008 Configure error handling and logging infrastructure
- [ ] T009 Setup environment configuration management

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

**Scenarios**: US1-AC1 → tests/acceptance/test_[capability].py::test_[NNN]_us1_ac1_[slug]; US1-AC2 → CHECKPOINT V1 scripted [the live service it needs]; US1-AC3 → CHECKPOINT V2 human [why a person is needed]

### Acceptance for User Story 1 (first; expected to fail until the story lands)

- [ ] T010 [US1] Write the US1 acceptance tests in tests/acceptance/test_[capability].py, one per scenario ID above (docstring = the scenario verbatim + provenance). Done-when: each fails for the expected reason: [quoted failure]

### Tests first for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T011 [P] [US1] Contract test for [endpoint] in tests/contract/test_[name].py. Done-when: fails for the expected reason: [quoted failure]
- [ ] T012 [P] [US1] Unit test for [component] in tests/unit/test_[name].py. Done-when: fails for the expected reason: [quoted failure]

### Implementation for User Story 1

- [ ] T013 [P] [US1] Create [Entity1] model in src/models/[entity1].py. Done-when: T012 passes and the wave's test run is green
- [ ] T014 [P] [US1] Create [Entity2] model in src/models/[entity2].py. Done-when: [its test] passes and the wave's test run is green
- [ ] T015 [US1] Implement [Service] in src/services/[service].py (depends on T013, T014). Done-when: T011 passes and the wave's test run is green
- [ ] T016 [US1] Implement [endpoint/command] in src/[location]/[file].py. Done-when: each US1 acceptance test (T010) passes and the wave's test run is green

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - [Title] (Priority: P2)

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

**Scenarios**: US2-AC1 → tests/acceptance/test_[capability].py::test_[NNN]_us2_ac1_[slug]

### Acceptance for User Story 2 (first; expected to fail until the story lands)

- [ ] T018 [US2] Write the US2 acceptance tests in tests/acceptance/test_[capability].py, one per scenario ID above. Done-when: each fails for the expected reason: [quoted failure]

### Tests first for User Story 2

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T019 [P] [US2] Contract test for [endpoint] in tests/contract/test_[name].py. Done-when: fails for the expected reason: [quoted failure]

### Implementation for User Story 2

- [ ] T020 [P] [US2] Create [Entity] model in src/models/[entity].py
- [ ] T021 [US2] Implement [Service] in src/services/[service].py
- [ ] T022 [US2] Implement [endpoint/feature] in src/[location]/[file].py
- [ ] T023 [US2] Integrate with User Story 1 components (if needed)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - [Title] (Priority: P3)

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

**Scenarios**: US3-AC1 → tests/acceptance/test_[capability].py::test_[NNN]_us3_ac1_[slug]

### Acceptance for User Story 3 (first; expected to fail until the story lands)

- [ ] T024 [US3] Write the US3 acceptance tests in tests/acceptance/test_[capability].py, one per scenario ID above. Done-when: each fails for the expected reason: [quoted failure]

### Tests first for User Story 3

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T025 [P] [US3] Contract test for [endpoint] in tests/contract/test_[name].py. Done-when: fails for the expected reason: [quoted failure]

### Implementation for User Story 3

- [ ] T026 [P] [US3] Create [Entity] model in src/models/[entity].py
- [ ] T027 [US3] Implement [Service] in src/services/[service].py
- [ ] T028 [US3] Implement [endpoint/feature] in src/[location]/[file].py

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] TXXX [P] Docs pass: README and docs/ describe the app as it now is (concise; no change log)
- [ ] TXXX Code cleanup and refactoring
- [ ] TXXX Performance optimization across all stories
- [ ] TXXX [P] Edge-case acceptance tests (EC-### scenarios not owned by a story) in tests/acceptance/. Done-when: each fails for the expected reason, then passes after its fix
- [ ] TXXX Security hardening
- [ ] TXXX Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests MUST be written and FAIL before implementation; no task both writes a test and makes it pass; implementation tasks never edit tests (a needed change goes back to a test task)
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All test tasks for a user story marked [P] can run in parallel (the acceptance task runs first)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all test tasks for User Story 1 together:
Task: "Contract test for [endpoint] in tests/contract/test_[name].py"
Task: "Integration test for [user journey] in tests/integration/test_[name].py"

# Launch all models for User Story 1 together:
Task: "Create [Entity1] model in src/models/[entity1].py"
Task: "Create [Entity2] model in src/models/[entity2].py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing; every task carries a `Done-when:` — test tasks: "fails for the expected reason: …"; implementation tasks: "that test passes and the wave's test run is green"
- Each wave commits itself once the wave's test run is green (one commit per wave)
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Next, `/s2tdd-harden` (in the same run that filled this template) rewrites this file
  test-first, pins cross-task interfaces and judgments, and produces a file-disjoint
  orchestration plan plus a handoff prompt, so tasks can be executed by smaller models and
  concurrent subagents without touching each other's tests. The chain then runs
  `/s2tdd-implement` (a fresh session per slice) with `/s2tdd-verify-done` after each, then
  `/s2tdd-converge`, a PR and `/s2tdd-pr-review`, and `/s2tdd-close`; `/s2tdd-next` prints
  each step's prompt
- `/s2tdd-close` stamps spec.md `Closed`, writes close-out.md, and freezes this directory.
  From then on the acceptance tests are the documentation — later features never edit these
  files
