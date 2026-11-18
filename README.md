# AI Flight Log — Tesla V100 SXM2 16 GB (Volta, sm_70)

Measured on 2026-11-18 by **ildargiv**, ongoing. Fourth card in the fleet line:
[rtx3060-strata-tuning](https://github.com/ildargiv/rtx3060-strata-tuning) →
[cmp90hx-strata-tuning](https://github.com/ildargiv/cmp90hx-strata-tuning) →
[ai-flight-log-v100](https://github.com/ildargiv/ai-flight-log-v100) (32 GB) → **this one (16 GB)**.

Sister repo: the 32 GB card journal covers the same chassis, same driver branch, same engine. This
repo exists to answer one question the 32 GB log cannot: *what changes when the card has half the
VRAM and the model still does not fit?*

This repo is a **flight log**, not a one-shot benchmark: dated entries, append-only, and a failed
measurement is a first-class entry with the same rank as a passing one. Rules:
[`RULES.md`](RULES.md), template: [`TEMPLATE.md`](TEMPLATE.md),
index + machine-readable feed: [`journal/README.md`](journal/README.md) /
[`journal/feed.jsonl`](journal/feed.jsonl).

Anchor line (comparable over time): one V100 SXM2-16GB, Qwen3.8-Flash-Next IQ3_S, 262,144 context,
`--kv int8`, engine defaults plus `STRATA_ROUTE_PRIOR=1.5`.

## Hardware and software

- GPU: Tesla V100-SXM2-16GB, GV100, 16,384 MiB, SXM2-to-PCIe adapter. Link: PCIe 3.0 x16
  (`gen 3 / 16 lanes`, max is the same — no downgrade). ECC enabled, 0 errors. Power limit 300 W.
  No video outputs (compute-only); the desktop runs on the Ryzen iGPU.
- CPU: Ryzen 5 5600G (6c/12t, Cezanne iGPU). RAM 90 GiB. Storage: Samsung 980 500 GB NVMe,
  102 GiB free at the time of writing.
- OS: Ubuntu 22.04.5, kernel 6.8.0-149-generic. Driver `580.178.04` (R580 is the last branch with
  Volta; `-open` is Turing+ only).
- Strata: terminal/app 0.2.15, control **0.1.61**, engine **0.1.60 linux-x86_64-cuda-cuda12**
  (build `09b603886925+cuda12.9`, sm_60/61/70/75/80/86/89, min driver 575.51) from the signed feed
  (sequence 127, stable). Previous engine 0.1.59 kept for rollback.

## Model and configuration

Qwen3.8-Flash-Next GSQ-RCO **IQ3_S**, 78 GB on disk in 2 shards (54.8 + 28.8 GB), GGUF arch
`qwen4exp`: 48 layers, 512 experts / 10 active, expert FFN 640, shared FFN 640, hidden 2560,
24 heads / 2 KV heads, native context 262,144. Pack `iq3_s`, DFlash2 draft
(`qwen3.8-flash-next-dflash2.q4_0-selq4.pack`), `--kv int8 --kv-resident 32768`,
`--expert-cache auto`, `--spec 6 --draft-conf 0.7`, env `STRATA_ROUTE_PRIOR=1.5`.

The whole model does not fit in 16 GB of VRAM (nor does it need to: 78 GB in 16 GB means the expert
cache is the product). With 0.1.60 the cache lands on **4,497 slots / 8.58 GiB**; with 0.1.59 it was
**4,435 / 8.46 GiB** — the new engine spends ~120 MiB less on overhead.

## Method

Two layers of numbers, labelled as such:

- **Engine bench** (`strata bench run`, protocol `standard-v1`) — the comparable series, same
  protocol as the 32 GB repo.
- **Client-side A/B harness** (`tools/ab_bench.py`) — identical prompts to two servers, TTFT and
  tok/s measured at the client. Used for engine-vs-engine comparisons where no shared protocol
  exists. TTFT-inclusive prefill numbers are lower than engine timings; do not mix the two columns.

## Results (index)

| Date | Entry | What |
| --- | --- | --- |
| 2026-11-18 | [001](journal/entries/001.md) | Card brought up on the existing chassis: link, ECC, driver, first launch |
| 2026-11-18 | [002](journal/entries/002.md) | Strata auto-tune (quick): defaults win, preset `iq3_s-262k-v100` saved |
| 2026-11-18 | [003](journal/entries/003.md) | Engine 0.1.59 → 0.1.60 + control 0.1.61: test-start, +1.4% expert slots, old engines removed |
| 2026-11-18 | [004](journal/entries/004.md) | Needle 250k/260k × 10/50/90: 6/6 found, anchor 1,086 tok/s @ 200,852 t, hit rate 94–99% |
| 2026-11-18 | [005](journal/entries/005.md) | A/B Strata vs llama-dspine (untuned): Strata ~5–9× faster on identical prompts |

Headline so far: **16 GB does not cost throughput, it costs cache.** Prefill and decode sit in the
same corridor as the 32 GB card; the expert cache is 2.7× smaller (4,497 vs 11,963 slots). On a
~201k-token needle ("full cache") recall is 6/6 and expert hit rate stays 94–99%, but a diverse
agent workload will stress that smaller cache first. A fair Strata-vs-llama-dspine comparison still
needs a llama-dspine sweep.

## Кратко по-русски

Карта V100 SXM2 16 ГБ встала в тот же корпус, что и 32-гигабайтная: PCIe 3.0 x16, ECC чистая,
лимит 300 Вт, драйвер 580.178.04. Модель Qwen3.8-Flash-Next IQ3_S (78 ГБ) в 16 ГБ не влезает и не
должна — работает кэш экспертов: 4 497 слотов / 8,58 ГиБ на движке 0.1.60 (на 0.1.59 было 4 435 /
8,46 ГиБ). Автотюнинг Strata сказал «текущие настройки уже самые быстрые», пресет
`iq3_s-262k-v100` сохранён. По скорости 16-гигабайтная карта практически не уступает 32-гигабайтной
(полоса HBM2 одинаковая), но кэш экспертов в 2,7 раза меньше (11 963 слота у 32 ГБ) — именно это
первым почувствует длинная агентская нагрузка. Подробности — в записях журнала.
