# Study C: confidence and identity

Five open-weight models (Gemma 3 27B, Gemma 4 31B, gpt-oss-120b, Qwen3-Next-80B-A3B, Nemotron 3 Super), 142 factual questions in a fully specified and a referent-removed form, three identity probes, 5,620 responses. Registered on OSF before scoring: https://doi.org/10.17605/OSF.IO/CS967

| Folder | Contents |
|---|---|
| `data/prompts/` | Prompt set and question sources |
| `data/probes/` | Pronoun, authority and safety probes |
| `data/raw_outputs/` | Every model response |
| `data/scoring/` | Both raters' scoring sheets, the blind key and the 600-response overlap list |
| `docs/` | Pre-registration, scoring rubric, prompt taxonomy |
| `code/` | Sampling, collection, agreement and analysis scripts |
| `results/` | Inter-rater agreement report |

The scoring sheets carry the original correctness labels. Run `python code/run_analysis.py` to reproduce the original-label figures that the thesis reports as a robustness check: error 39.9% (clear) and 66.7% (referent removed), and 77.4% of wrong answers unhedged. The headline figures in Chapter 6 of the thesis (39.1% and 52.0%, 75.3% unhedged, AUROC 0.56) come from the final registered analysis. That analysis treats a pure clarification request as an abstention rather than an error, as the rubric specifies, after a label-validity check of all 468 replies containing clarification or refusal language. Both versions lead to the same conclusion.
