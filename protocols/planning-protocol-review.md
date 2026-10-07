# Planning protocol: change and review record

Current version: **v3.2** (`planning-protocol.md`), recorded 2026-10-04.
Status: **no further valuable gaps found** (review loop saturated after round 4).

## Requested changes (v3.1 → v3.2)

| Request | Where it lives |
|---|---|
| Record every correction to execution as a lesson, with the information that prevents a repeat, classified so related lessons can be read as a group | Global Rule 11; Appendix A (template); Appendix C (tags, matching rule) |
| As the last step of implementation, request a target for pushing the lessons | Gate `G-003` (Rule 10); closing step `S-KNOW` (3.7.2) |
| In research, read the lessons related to the problem and its implementation (e.g. audio lessons for a VST, Java lessons for a Java implementation) | R0 in 1.3; intake Subject tags (0.3.1); matching rule (Appendix C) |
| Before pushing lessons, a retrospective that identifies errors and overlooked steps and adds them as lessons | Closing step `S-RETRO` (3.7.1) |
| Record research and derived knowledge in a classified knowledge base, adding new facts about the Subject whenever they are found | Global Rule 12; R2/R6 coupling in 1.3; Appendix B (template) |

Supporting design: lessons and knowledge persist across tasks in a **knowledge store** (Rule 13; intake 0.3.1, access check 0.3.7, layout in Appendix C). During a run they accumulate on the working branch as one file per entry and are pushed at the end. They never contain secrets.

## Speed review: gaps that would slow implementation

Each round read the whole protocol and asked where an implementation would stall, need rework, or wait.

### Round 1
| Gap | Why it slows implementation | Resolution |
|---|---|---|
| Access was checked only as "push permission" | Missing workflow, pull-request, or packages permission surfaces mid-implementation and blocks work | 0.1 checks every permission the plan needs |
| Network checked in general, not per host | An unreachable registry or CI log store forces late workarounds | 0.1 checks each host the work depends on and decides an alternative channel |
| No implementation start step, branch, or log | Problems surface after delivery work has started; the retrospective has no record to read | Opening step `S-000` (3.7.0): branch, setup, access re-checked, `EXECUTION_LOG.md` |
| Gates idle the implementer; `G-003` could hold up completion | Waiting for a human stops all progress | Independent steps continue at gates (3.3); implementation completes after `S-RETRO` |
| A challenged frozen test forced a re-run from Phase 0 | A local problem triggered a full re-plan | Scoped amendment of the item and its dependants (2E.4) |
| No fallback for the store | An unreadable or moved store blocks research or the final push | Unreadable store is a risk, not a blocker (0.3.7); retry and bundle fallback (3.7.2) |

### Round 2
| Gap | Why it slows implementation | Resolution |
|---|---|---|
| No concurrency rule | Independent steps run one at a time | `Exclusive resources` field and concurrency rule (3.1) |
| Unbounded retrospective | Could re-investigate or re-run work | One pass over a collected digest; re-runs nothing (3.7.1) |
| Repeated mistakes create duplicate lesson files | Slower to write now and to read later | `occurrences` on the run's lesson (Rule 11, Appendix A) |
| Schema check was prose | Every run writes its own checker | Literal script in Appendix C, tested against the templates and against broken entries |
| No reading order for prior lessons | Large stores slow R0; later phases re-read lessons | Severity-then-recency order; prevention rules compiled into a checklist (R0) |
| Facts written twice by hand (claims and knowledge items) | Double bookkeeping in research | Knowledge items generated from `claims.json` (R2) |

### Round 3
| Gap | Why it slows implementation | Resolution |
|---|---|---|
| Checkpoint schema lacked the knowledge-store fields that 0.3.7 and R0 record | Agents invent field names; resume and audits break | Fields added to the `state.json` schema (1.2) |

### Round 4
No valuable gaps. Considered and declined, because none would speed implementation enough to justify the extra process:
- a pruning or archiving policy for the store (retirement and superseding already exist, and R0 reads in priority order);
- metrics on how effective lessons are;
- confidentiality rules beyond the existing no-secrets, no-personal-data rule;
- support for several stores (personal and team);
- automatic tag suggestion.

## Open decisions for the owner
- The default knowledge store proposed at intake is a repository named `knowledge` under the target repository's owner. Each run asks at intake, so a different location can be given at any time.
