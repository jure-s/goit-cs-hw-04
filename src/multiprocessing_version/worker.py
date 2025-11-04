from __future__ import annotations

from multiprocessing import Pool
from typing import List, Tuple

from src.common.search_logic import search_words_in_file


def match_words_in_file(args: tuple[str, List[str]]) -> Tuple[str, List[str]]:
    """
    ОК для Windows (spawn): топ-рівнева функція, щоб була picklable.
    Повертає (file_path, matched_words[]).
    """
    file_path, words = args
    flags = search_words_in_file(file_path, words)
    matched = [w for w, ok in flags.items() if ok]
    return file_path, matched


def run_parallel_on_files(
    file_paths: List[str], words: List[str], workers: int
) -> List[Tuple[str, List[str]]]:
    """Паралельна обробка файлів процесами."""
    if not file_paths:
        return []
    with Pool(processes=workers or None) as pool:
        return list(pool.imap_unordered(match_words_in_file, [(fp, words) for fp in file_paths]))
