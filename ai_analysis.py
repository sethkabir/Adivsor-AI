import json, re

def run_ai(prompt, ai_client):
    res = ai_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Financial portfolio AI assistant. JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        max_tokens=2000
    )
    return res.choices[0].message.content


def extract_json_safe(text: str) -> dict:
    text = re.sub(r"```json|```", "", text)
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return {}
    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return {}
