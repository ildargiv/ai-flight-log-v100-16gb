# Flight log / Бортовой журнал

Index of dated entries. Language policy: root README is EN-first with a RU summary; entries are
written in the operator's language with an EN one-liner here. Append-only — corrections are new
entries, see [`../RULES.md`](../RULES.md).

Machine feed: [`feed.jsonl`](feed.jsonl). Raw runs: [`../results/`](../results/).

| № | Date | Engine | Class | EN one-liner | RU |
| --- | --- | --- | --- | --- | --- |
| [001](entries/001.md) | 2026-11-18 | 0.1.59-cuda12 | hardware/success | 16 GB card in the 32 GB chassis: PCIe 3.0 x16 confirmed, ECC 0 errors, 300 W, driver 580.178.04; first launch at 262,144 context with a 4,435-slot expert cache | карта встала без сюрпризов: x16, ECC чистая, 300 Вт, первый запуск на 262K |
| [002](entries/002.md) | 2026-11-18 | 0.1.59-cuda12 | tuning/neutral | quick auto-tune: "your current settings are already the fastest" — nothing changed, preset `iq3_s-262k-v100` saved; prefill ~1.4–1.6K tok/s on a 95.9K-token prompt, expert hit rate 97.7–99.1% | автотюнинг: дефолты уже оптимальны, пресет сохранён; hit rate 97.7–99.1% |
| [003](entries/003.md) | 2026-11-18 | 0.1.59 → 0.1.60 | engine/success + config/failure | update to engine 0.1.60 + control 0.1.61 passed its own test-start; expert cache 4,435 → 4,497 slots (+1.4%); old engines removed; tune preset ≠ `launch --preset` | обновление прошло, кэш +1.4%; пресет тюнинга не равен launch-пресету |
| [004](entries/004.md) | 2026-11-18 | 0.1.60-cuda12 | bench/success + harness/failure | needle 250k/260k × 10/50/90: 6/6 FOUND; anchor (250k, 10%, 0 reused) 200,852 tokens @ 1,086 tok/s, hit rate 94–99% at 4,497 slots — "full cache" holds; 260k/10% arm had 16,738 reused tokens | needle 6/6: на ~201k/207k recall есть, кэш держит 94–99%; один рукав не чисто fresh |
| [005](entries/005.md) | 2026-11-18 | 0.1.60 vs llama-dspine@d493f84 | bench/neutral + harness/failure | client A/B on identical prompts: Strata 410/870/1,213 tok/s prefill, 91/89/95 tok/s decode; llama-dspine A (sm_70 build, untuned: `-ncmoe 48 --moe-cache-mib 6000`, q8_0 KV) 113/142/137 and 19/19/19 — ~5–9× behind, config not swept | A/B: Strata в 5–9× быстрее нетюнингованного llama-dspine на тех же GGUF |
