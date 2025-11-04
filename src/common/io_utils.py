from pathlib import Path
from typing import List


def list_text_files(root: str | Path) -> List[str]:
    """Повертає список шляхів до .txt (рекурсивно). Порожній список — валідний випадок."""
    p = Path(root)
    if not p.exists():
        raise FileNotFoundError(f"Path not found: {root}")
    if p.is_file():
        return [str(p)] if p.suffix.lower() == ".txt" else []
    return [str(fp) for fp in p.rglob("*.txt")]


def read_text(file_path: str) -> str:
    """Безпечне читання текстового файлу як UTF-8."""
    return Path(file_path).read_text(encoding="utf-8", errors="ignore")
