#!/usr/bin/env python3
"""Сводная таблица по ab-*.json (Strata и llama-dspine)."""
import glob
import json
import sys

files = sys.argv[1:] or sorted(glob.glob('results/ab-*.json'))
rows = []
for f in files:
    try:
        d = json.load(open(f))
    except Exception as e:
        print(f'skip {f}: {e}')
        continue
    for c in d.get('cases', []):
        rows.append({
            'label': d.get('label'),
            'case': c.get('case'),
            'prompt_tokens': c.get('prompt_tokens'),
            'completion_tokens': c.get('completion_tokens'),
            'ttft_s': c.get('ttft_s'),
            'prefill_tok_s': c.get('prefill_tok_s'),
            'decode_tok_s': c.get('decode_tok_s'),
        })

order = {'short-1k': 0, 'medium-8k': 1, 'long-32k': 2}
rows.sort(key=lambda r: (r['case'] not in order, order.get(r['case'], 9), str(r['label'])))

hdr = f"{'конфиг':<18}{'кейс':<11}{'prompt':>8}{'gen':>6}{'TTFT s':>9}{'prefill':>10}{'decode':>9}"
print(hdr)
print('-' * len(hdr))
for r in rows:
    print(f"{str(r['label']):<18}{str(r['case']):<11}{str(r['prompt_tokens']):>8}"
          f"{str(r['completion_tokens']):>6}{str(r['ttft_s']):>9}"
          f"{str(r['prefill_tok_s']):>10}{str(r['decode_tok_s']):>9}")
