import re


def normalize_name(name):
    " Using regex we can make all these methods give the same answer 'serena williams' / 'Serena Williams' / 'SerenaWilliams' -> 'SerenaWilliams'."
    if not re.search(r"[A-Za-z]", name or ""):
        raise ValueError("Player name must contain letters.")
    if " " not in name.strip() and name[1:] != name[1:].lower():
        return name.strip()  # already MixedCaps
    return "".join(w.capitalize() for w in name.split())
