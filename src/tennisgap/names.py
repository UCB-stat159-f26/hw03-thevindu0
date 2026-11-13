"""Turn user-typed player names into Tennis Abstract slugs."""


def build_slug(name):
    """'serena williams' / 'Serena Williams' / 'SerenaWilliams' -> 'SerenaWilliams'."""
    name = name.strip()
    if not name:
        raise ValueError("Player name must not be empty.")
    if " " in name:
        return "".join(word.capitalize() for word in name.split())
    return name