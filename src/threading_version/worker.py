from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple

from src.common.search_logic import search_words_in_file


def match_words_in_file(file_path: str, words: List[str]) -> Tuple[str, List[str]]:
    """Повертає (file_path, matched_words[]) для одного файлу."""
    flags = search_words_in_file(file_path, words)
    matched = [w for w, ok in flags.items() if ok]
    return file_path, matched


def run_parallel_on_files(
    file_paths: List[str], words: List[str], workers: int
) -> List[Tuple[str, List[str]]]:
    """Паралельно обробляє файли та повертає список результатів по кожному файлу."""
    if not file_paths:
        return []
    with ThreadPoolExecutor(max_workers=workers or None) as ex:
        futures = [ex.submit(match_words_in_file, fp, words) for fp in file_paths]
        return [f.result() for f in as_completed(futures)]
