# Memory retrieval evaluation

- **Corpus / commit:**
- **Search method:** `rg` | script | hybrid | other
- **Evaluation date:** YYYY-MM-DD
- **Evaluator:**

## Benchmark cases

Prepare 10–20 real tasks/questions you have encountered. Record the expected entry before running the search to avoid grading against results you have already seen.

| Case | Query/task | Expected memory ID/path | In top 5? | Opened a useful result? | Applied correctly? | Result |
|---|---|---|---|---|---|---|
| E-01 | | | Yes/No | Yes/No | Yes/No/N/A | |

## Metrics

- **Recall@5:** expected relevant entries appearing in the top 5 / cases with relevant memory = ___ / ___ = ___%
- **Precision@5:** useful results among the top-5 results opened / total results opened = ___ / ___ = ___%
- **Adoption rate:** related tasks where memory was applied correctly / total related tasks = ___ / ___ = ___%
- **Stale-memory rate:** retrieved entries that conflict with current evidence / total entries checked = ___ / ___ = ___%
- **Duplicates/conflicts found:**
- **Time to find / time to fix:**

## Findings and next actions

- Main retrieval failures:
- Main content-quality issues:
- Taxonomy/tag/index changes to try first:
- Evidence needed before using embeddings/vector search/a database:
