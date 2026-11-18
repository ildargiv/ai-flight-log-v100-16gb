#!/usr/bin/env bash
# llama-dspine A/B config A (first pass, not tuned)
cd /home/linux1/src/llama-dspine/build/bin
./llama-server \
  -m /home/linux1/models/strata/Qwen3.8-Flash-Next-GSQ-RCO-IQ3_S/Qwen3.8-Flash-Next-GSQ-RCO-IQ3_S-00001-of-00002.gguf \
  -ngl 99 --n-cpu-moe 48 --moe-cache-mib 6000 \
  -c 262144 -ctk q8_0 -ctv q8_0 -fa on \
  --host 127.0.0.1 --port 8081 -np 1 --jinja -t 8
