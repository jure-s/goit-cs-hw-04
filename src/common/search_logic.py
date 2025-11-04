from __future__ import annotations

from typing import Dict, List

from .io_utils import read_text


def search_words_in_file(file_path: str, words: List[str]) -> Dict[str, bool]:
    """
    Для кожного слова повертає True/False — чи зустрічається воно у файлі.
    Пошук нечутливий до регістру, працює по "вхождению" (substring).
    """
    text = read_text(file_path).lower()
    return {w: (w in text) for w in words}
