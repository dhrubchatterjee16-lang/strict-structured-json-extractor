# Strict Structured JSON Extractor: Guaranteed Schema Conformance for Chemical Synthesis Protocols

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![QLoRA](https://img.shields.io/badge/Fine--Tuning-Unsloth%20%7C%20TRL-cyan)]()
[![Validation](https://img.shields.io/badge/Schema-100%25%20Pydantic%20Validated-brightgreen)]()

A production-grade QLoRA fine-tuning and constrained inference pipeline that forces small open-weight language models (Qwen-2.5-7B, Llama-3-8B) to output 100% syntactically strict, Pydantic-validated JSON from unstructured wet-lab chemistry protocols and patent experimental disclosures.

---

## 🎯 The Problem & Engineering Solution

Large Language Models frequently emit broken JSON (trailing commas, unescaped quotes, missing required fields, or hallucinations outside the schema). For automated chemical robotics (e.g. Opentrons protocols), a single schema violation crashes the physical hardware.

This repository implements a two-stage guarantee:
1. **Grammar-Constrained Decoding:** Injects Outlines / Guidance context-free grammar (CFG) state machines during autoregressive generation to ensure token transitions only match the schema.
2. **Domain-Specific QLoRA Adaptation:** Fine-tuned on 15,000+ paired chemical synthesis procedures mapping raw experimental paragraphs into strict reaction condition schemas:
   - Reactants, reagents, and catalyst loading (mol%, mg, mmol).
   - Temperature ramps, reflux durations, and agitation speeds.
   - Workup protocols: extraction solvents, washing phases, and recrystallization conditions.

---

## 🚀 Quickstart

```bash
git clone https://github.com/dhrubchatterjee16-lang/strict-structured-json-extractor.git
cd strict-structured-json-extractor
pip install -r requirements.txt
python extract.py --text "To a solution of 2-bromothiophene (1.0 mmol) in dry THF (5 mL) at -78 C was added n-BuLi..."
```
