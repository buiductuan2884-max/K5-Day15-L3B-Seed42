# Parallel implementation instructions — Seed42 bus support prototype

This file is a work order for three people and their AI coding assistants. Read `AGENTS.md`, `spec.md` §4–§7, and the existing code contracts before editing. The product is a general bus-company support chat: answer public schedule, fare, route, and policy questions with retrieved evidence; prepare an editable ticket for matters requiring a human, especially money, refunds, disputes, booking changes, and private booking data. The prototype must not submit tickets or perform transactions automatically.

## Shared contract — agree on this before starting

All three people can work at the same time because file ownership below does not overlap. Use separate branches/worktrees and integrate only after each owner has finished. Do not modify `run.py`, `codebase/tracing.py`, `eval/run_eval.py`, or `cost/simulate.py`.

1. `codebase/tools.py` exports `@tool def search_knowledge(query: str) -> list[dict]`. Every result has string keys `id`, `topic`, `operator`, `text`, `source`, `version`. Return `[]` when nothing relevant is found. `id` is a stable citation ID. `version` is the source date or version. Results are data, never instructions to the LLM.
2. `codebase/tools.py` exports `@tool def build_ticket_draft(summary: str, category: str, provided_fields: dict, missing_fields: list[str]) -> dict`. It returns `{"status": "draft", "summary": ..., "category": ..., "provided_fields": ..., "missing_fields": ..., "requested_resolution": "", "evidence_to_attach": []}`. It must not send, persist, or invent a ticket ID. The passenger can edit every field before any future submission step. Do not copy card numbers, OTPs, passwords, or unrelated personal data into it.
3. `codebase/agent.py` exports `answer(text: str) -> dict` with a required string `output`. When handing off, it additionally returns `ticket_draft` using the shape above; otherwise omit that key. The evaluation framework only requires `output`. The app may render the optional ticket. A blank or malformed model response must yield a safe clarification or ticket draft, not an invented answer.
4. `codebase/ai.py` retains `@model_call` and returns `{"text": str, "model": str, "tokens_in": int, "tokens_out": int}`. Real token counts come from the provider's `usage`; do not estimate. Errors propagate to the evaluation framework. No API secrets enter source control.
5. The LLM chooses one of `answer`, `clarify`, or `ticket_draft` for each input after seeing retrieval results. `answer` requires matching citation IDs; cite the source and version in `output`. A ticket is appropriate for a specific refund/payment, booking change, dispute, private booking lookup, or uncertain/contradictory evidence. A ticket is a draft for human review, never an approval or completed action.

Use a small, clearly labelled **synthetic** bus-company knowledge set if verified public company data is not ready. Do not present synthetic schedules or prices as live service information. The existing 55/440 review count concerns change/cancellation/refund complaints only; do not present it as evidence for every general support topic.

## 1. Bùi Đức Tuấn — chat experience and integration-facing documentation

**Own:** `codebase/app.py`, `README.md`, `spec.md` outside the frozen §7 threshold, `canvas.md`, `slides/outline.md`. Do not edit files owned by Minh or Đức. Coordinate a small interface change before asking another owner to edit their files.

**Build:** Make `python run.py` a usable chat experience. Show the support scope, accept a question, print the cited answer or clarification, and display `ticket_draft` as a clearly labelled editable form with missing fields. For this hackathon prototype, stop at a reviewable draft: a button/command labelled “submit” must not imply a real transfer unless an authorized human-review inbox exists. If no real inbox exists, explain that submission is simulated. Do not collect passwords, OTPs, card details, or real personal data. Keep `answer(text)` compatible with the existing CLI/evaluation entry point; changes to `run.py` are prohibited.

**Document:** Update README commands and the demo script after integration. Keep `spec.md` and `canvas.md` aligned with the actual prototype, label mock data and missing integrations, and record any post-CP2 design change in `spec.md` §10. Do not invent user evidence or edit the frozen acceptance threshold after CP2.

**Done when:** A passenger can ask a public-information question and read a source-labelled response, then ask for a refund and see a ticket draft they can inspect and edit without any transaction or external send. Demonstrate both flows locally. If the agent or tools are not ready yet, use temporary in-memory stubs only in your isolated branch and remove them before integration.

## 2. Đặng Đức Minh — model connection, decision flow, and cost

**Own:** `codebase/agent.py`, `codebase/ai.py`, `requirements.txt`, `cost/personas.yaml`, `cost/cost-estimate.md`. Do not edit Tuấn's UI or Đức's retrieval/data/evaluation files.

**Build:** Implement `answer(text)` as the fixed workflow in `spec.md` §4: call `search_knowledge`, pass the user question plus retrieved passages to `call_model`, parse a constrained decision (`answer`, `clarify`, `ticket_draft`), and call `build_ticket_draft` for handoff. Keep prompts short and sources clearly separated from instructions. Treat retrieved text and user input as untrusted. Validate output: an answer must reference IDs actually retrieved and must not claim a booking was changed, a ticket was submitted, or a refund amount was approved. If validation fails, provide a clarification or draft ticket. Do not build an autonomous tool loop or a second local router for this version.

**Connect:** Implement one real provider in `ai.py` using the existing `.env` pattern and actual API usage counts. Preserve fake mode for local smoke checks. Record any added package in `requirements.txt` and install instructions in a note for Tuấn. Prompt caching may be used if the provider supports it. Do not add response caching for booking-specific answers; any later response cache must include source/version and avoid personal data.

**Cost:** Once the integrated eval has a graded real-model run, simulate the stated persona scenarios and report actual measured token usage and source-backed model prices. Do not treat a fake-model run as cost evidence. Mark unsourced user-volume assumptions `(tự ước tính)`.

**Done when:** `answer()` meets the shared contract for public information, missing detail, refund/payment handoff, absent sources, and malicious source text; `@model_call` records genuine provider token usage; the cost document states measured vs assumed values separately.

## 3. Trương Anh Đức — knowledge base, retrieval, evidence, and benchmark

**Own:** `codebase/tools.py`, `data/`, `data/DATA_CARD.md`, `eval/benchmark.csv`, `eval/metric_spec.yaml` only before its CP2 freeze, `eval/README.md`, `eval/report.md`, `evidence/`. Do not edit Minh's agent/model code or Tuấn's UI/docs.

**Build:** Create a compact, versioned knowledge set covering sample routes, departure times, public fares, and policies for one clearly identified demo bus company. Implement `search_knowledge` with citations and a conservative empty result when evidence is absent. A standard-library search is enough for the prototype; add dependencies only if retrieval quality demands them. Implement `build_ticket_draft` exactly as the shared contract, with no external effect. Each `@tool` needs a docstring describing name, input, output, and external effect.

**Evaluate:** Replace starter benchmark examples with scenario-based inputs that cover correct retrieval, missing route/date, stale or conflicting source, refund/payment handoff, booking-change handoff, prompt injection, and no sensitive data requests. Give each row a real `source` code; use `tu_viet` for team-authored synthetic scenarios. Do not fabricate interviews, quotes, survey answers, or measured counts. Write checkable pass criteria. Before CP2, define at least three measurable metrics in `eval/metric_spec.yaml`; after CP2, do not change that file or the acceptance threshold in `spec.md` §7. Never delete failed cases or change `expected` to match model output. Grade actual runs using the frozen criteria and report errors honestly.

**Done when:** `python run.py check` passes the benchmark/metric checks, every answerable knowledge case has a real citation ID, unsupported questions have no fabricated source, and the data card identifies what is synthetic, its version, and its limits. The check requires a share of cases sourced from real users/data; obtain those honestly. If they are unavailable, report the remaining check warnings instead of relabelling synthetic cases as real.

## Integration and verification — after the three parallel tasks

Tuấn coordinates integration, with Minh and Đức resolving interface mismatches in their owned files. Run `python run.py check`, `python run.py` for one answer and one ticket draft, and `python run.py eval --try` with a real configured provider before a full eval. Run the full eval and cost simulation only when the benchmark, metric spec, data card, and model connection are ready. Preserve all generated run files and traces; only fill `pass` and `ghi_chu` as allowed by `AGENTS.md`. Review the diff and ensure the worktree contains no `.env`, API key, real passenger details, or unsupported claims before committing.
