# SpringForge RAG System: Key Success Metrics

## Performance Overview

### Retrieval Metrics

| Metric | Score | 95% Confidence Interval |
|--------|-------|-------------------------|
| **Precision@1** | 0.9524 | [0.8571, 1.0000] |
| **Precision@3** | 0.6825 | [0.5873, 0.7778] |
| **Precision@5** | 0.5429 | [0.4571, 0.6381] |
| **Recall@5** | 0.7177 | [0.6190, 0.8287] |
| **NDCG@5** | 0.6783 | [0.5748, 0.7903] |
| **MRR** | 0.9762 | [0.9286, 1.0000] |
| **MAP** | 0.8573 | [0.7960, 0.9188] |

### Generation Metrics

| Metric | Score | 95% Confidence Interval |
|--------|-------|-------------------------|
| **BLEU** | 0.1540 | [0.0638, 0.2812] |
| **ROUGE-1** | 0.7738 | [0.6561, 0.8744] |
| **ROUGE-2** | 0.3051 | [0.2000, 0.4140] |
| **ROUGE-L** | 0.0430 | [0.0346, 0.0512] |
| **Token F1** | 0.3304 | [0.2270, 0.4489] |
| **Exact Match (EM)** | 0.0909 | [0.0000, 0.2273] |

## What The Metrics Mean

- **Precision@1**: How often the first retrieved result is relevant.
- **Precision@3**: How often relevant results appear within the top 3.
- **Precision@5**: How often relevant results appear within the top 5.
- **Recall@5**: How many of the total relevant results are captured in the top 5.
- **NDCG@5**: Ranking quality that rewards relevant results appearing higher.
- **MRR**: How quickly the first relevant result appears; higher is better.
- **MAP**: Mean Average Precision; overall ranking quality across queries.
- **BLEU**: N-gram overlap between generated text and reference text.
- **ROUGE-1**: Word-level overlap between generated and reference text.
- **ROUGE-2**: Two-word phrase overlap between generated and reference text.
- **ROUGE-L**: Longest shared sequence similarity between generated and reference text.
- **Token F1**: Balanced overlap score between predicted tokens and reference tokens.
- **Exact Match (EM)**: Percentage of outputs that match the reference exactly.

---
*System Status: **Production-Ready Alpha***