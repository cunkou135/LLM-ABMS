import os
import re

from openai import OpenAI


def build_prompt(template, regime, regime_label, trajectory_summary):
    return template.format(
        regime=regime,
        regime_label=regime_label,
        trajectory_summary=trajectory_summary,
    )


def parse_response(text):
    label_match = re.search(r"\[\s*Emergence\s+Label\s*\]\s*:?\s*(.+)", text, flags=re.I)
    interpretation_match = re.search(
        r"\[\s*Interpretation\s*\]\s*:?\s*(.*?)(?=\n\s*\[\s*Confidence\s*\]|\Z)",
        text,
        flags=re.I | re.S,
    )
    confidence_match = re.search(r"\[\s*Confidence\s*\]\s*:?\s*(.+)", text, flags=re.I)
    label = label_match.group(1).strip().splitlines()[0] if label_match else "UNPARSED"
    label = re.sub(r"^[*_`\"']+|[*_`\"']+$", "", label).rstrip(". ")
    interpretation = interpretation_match.group(1).strip() if interpretation_match else ""
    confidence = confidence_match.group(1).strip().splitlines()[0] if confidence_match else ""
    return {
        "emergence_label": label,
        "interpretation": interpretation,
        "confidence": confidence,
    }


def analyse(config, system_prompt, user_prompt):
    api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("DEEPSEEK_API_KEY is required")

    client = OpenAI(api_key=api_key, base_url=config["base_url"], timeout=180.0)
    response = client.chat.completions.create(
        model=config["model"],
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=config["temperature"],
        top_p=config["top_p"],
        max_tokens=config["max_tokens"],
        reasoning_effort=config["reasoning_effort"],
        extra_body={"thinking": {"type": config["thinking"]}},
    )
    text = response.choices[0].message.content or ""
    if not text.strip():
        raise RuntimeError("The API returned empty content")
    return parse_response(text)

