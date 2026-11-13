import re


def normalize_name(name):
    " Here are some examples of the regex the script uses to get the right name from the site: ' Serena Williams' / 'Serena Williams' / 'SerenaWilliams' -> 'SerenaWilliams'.
    if not re.search(r"[A-Za-z]", name or ""):
        raise ValueError("Player name must contain letters.")
    if " " not in name.strip() and name[1:] != name[1:].lower():
        return name.strip()  # For mixed capslocks
    return "".join(w.capitalize() for w in name.split())

    
