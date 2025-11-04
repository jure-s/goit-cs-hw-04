def parse_words(raw: str) -> list[str]:
    """
    Приймає рядок типу: "apple, banana, mango" -> ["apple","banana","mango"] (без порожніх).
    Нормалізує до нижнього регістру.
    """
    words = [w.strip().lower() for w in raw.split(",")]
    return [w for w in words if w]
