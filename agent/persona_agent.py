import openai
from config.settings import OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME

openai.api_key = OPENAI_API_KEY
openai.api_base = OPENAI_BASE_URL


def fallback_reply(message: str):
    text = message.lower()
    if "upi" in text:
        return "Sir kis UPI ID par payment karna hai?"
    if "refund" in text or "bank" in text:
        return "Refund kis bank account se aa raha hai? Account number bata do?"
    if "link" in text:
        return "Kaunsa link use karna hai sir? Yahin bhej do."
    return "Payment kahan send karna hai sir? Details share kar do."


def generate_reply(message: str, history: list):
    try:
        base_prompt = open("prompts/victim_prompt.txt").read()
        prompt = base_prompt.format(message=message)

        messages = [{"role": "system", "content": prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": message})

        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.9,
            max_tokens=80
        )

        reply = response["choices"][0]["message"]["content"].strip()
        if "?" not in reply:
            reply += "?"
        return reply

    except Exception:
        return fallback_reply(message)
