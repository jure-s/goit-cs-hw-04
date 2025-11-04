from __future__ import annotations

from collections import defaultdict
from typing import Dict, List

from .worker import run_parallel_on_files


def run_search(file_paths: List[str], words: List[str], workers: int = 4) -> Dict[str, List[str]]:
    """
    Паралельний пошук на потоках.
    Повертає: { word: [files...] }
    """
    result: Dict[str, List[str]] = defaultdict(list)

    per_file_results = run_parallel_on_files(file_paths, words, workers)
    for file_path, matched_words in per_file_results:
        for w in matched_words:
            result[w].append(file_path)

    # гарантовано повертаємо всі ключі
    for w in words:
        result.setdefault(w, [])
    return dict(result)
