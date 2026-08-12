import json
from pathlib import Path

from llm_interface import analyse, build_prompt
from simulation import simulate, summarise


ROOT = Path(__file__).resolve().parents[1]


def main():
    config = json.loads((ROOT / "config" / "case_config.json").read_text(encoding="utf-8"))
    system_prompt = (ROOT / "prompts" / "system_prompt.txt").read_text(encoding="utf-8").strip()
    prompt_template = (ROOT / "prompts" / "macro_analysis_prompt.txt").read_text(encoding="utf-8").strip()
    regime = config["representative_regime"]
    rows = simulate(
        regime,
        config["seed"],
        config["baseline_agents"],
        config["baseline_steps"],
        config["regimes"],
    )
    trajectory_summary = summarise(rows)
    user_prompt = build_prompt(
        prompt_template,
        regime,
        config["regimes"][regime]["label"],
        trajectory_summary,
    )
    result = analyse(config, system_prompt, user_prompt)
    print(f"Trajectory summary: {trajectory_summary}")
    print(f"Emergence label: {result['emergence_label']}")
    print(f"Interpretation: {result['interpretation']}")
    print(f"Confidence: {result['confidence']}")


if __name__ == "__main__":
    main()

