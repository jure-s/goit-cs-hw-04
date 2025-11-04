from __future__ import annotations

import argparse
from collections import defaultdict

from src.common.io_utils import list_text_files
from src.common.search_logic import search_words_in_file
from src.common.timing import timer
from src.common.validators import parse_words


def run_singlepath(dir_path: str, words: list[str]) -> dict[str, list[str]]:
    files = list_text_files(dir_path)
    result: dict[str, list[str]] = defaultdict(list)
    for fp in files:
        flags = search_words_in_file(fp, words)
        for w, ok in flags.items():
            if ok:
                result[w].append(fp)
    for w in words:
        result.setdefault(w, [])
    return dict(result)


def run_threading(dir_path: str, words: list[str], workers: int) -> dict[str, list[str]]:
    files = list_text_files(dir_path)
    from src.threading_version.runner import run_search

    return run_search(files, words, workers=workers)


def run_multiprocessing(dir_path: str, words: list[str], workers: int) -> dict[str, list[str]]:
    files = list_text_files(dir_path)
    from src.multiprocessing_version.runner import run_search

    return run_search(files, words, workers=workers)


def build_cli() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Keyword search (single/threading/multiprocessing)")
    p.add_argument("--path", default="data/sample_texts", help="Шлях до папки/файлу з .txt")
    p.add_argument("--words", required=True, help='Слова через кому, напр.: "apple,banana"')
    p.add_argument(
        "--mode",
        choices=["single", "threading", "multiprocessing"],
        default="single",
        help="Режим виконання",
    )
    p.add_argument("--workers", type=int, default=4, help="Кількість потоків/процесів")
    return p


def main():
    args = build_cli().parse_args()
    words = parse_words(args.words)

    with timer() as t:
        if args.mode == "single":
            result = run_singlepath(args.path, words)
        elif args.mode == "threading":
            result = run_threading(args.path, words, args.workers)
        elif args.mode == "multiprocessing":
            result = run_multiprocessing(args.path, words, args.workers)
        else:
            raise ValueError("Unknown mode")
    elapsed = t()

    print("Result (word -> files):")
    for w, files in result.items():
        print(f"  {w}:")
        for f in files:
            print(f"    - {f}")
    print(f"\nElapsed: {elapsed:.6f}s")


if __name__ == "__main__":
    main()
