import gate


def judge(question: str, expects: str, answer: str, results) -> bool:
    if not expects:
        return False
    if answer == gate.REFUSAL:
        return False
    return expects.strip().lower() in (answer or "").lower()
