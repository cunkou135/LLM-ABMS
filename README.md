# LLM-ABMS Case Study Code

This repository provides the core source code, prompts, configuration, and selected intermediate specifications used in the illustrative urban-alert case study described in the accompanying paper.

The released materials cover selected components of the connected case study across conceptual modeling, simulation modeling, and simulation experimentation.

## Contents

- `case_study/conceptual_modeling/`: scenario materials and reported diagram-generation prompts
- `case_study/simulation_modeling/`: selected runtime implementation materials used in the agent-level illustration
- `src/`: reduced population simulation, LLM interface, and runnable macro-level interpretation example
- `prompts/`: prompt templates used by the released macro-level interpretation implementation
- `config/`: model and reduced-simulation configuration

## Installation

```powershell
pip install -r requirements.txt
```

## API configuration

Set `DEEPSEEK_API_KEY` in the environment before running the case. The DeepSeek endpoint is accessed through its OpenAI-compatible API interface using the OpenAI Python client.

The model service used for the original case-study generation was accessed in June 2026.

## Running the illustrative case

```powershell
python src/run_case.py
```

## Notes

This is a minimal release of the core illustrative implementation. Experimental outputs and publication figures are not distributed. Hosted API behavior may change over time, so generated text may differ in future runs.
