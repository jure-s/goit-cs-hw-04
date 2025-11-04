from __future__ import annotations

import argparse
import random
from pathlib import Path

VOCAB = [
    "apple",
    "banana",
    "mango",
    "orange",
    "grape",
    "python",
    "java",
    "golang",
    "rust",
    "csharp",
    "database",
    "sql",
    "postgresql",
    "mysql",
    "sqlite",
    "thread",
    "process",
    "lock",
    "queue",
    "future",
    "index",
    "table",
    "row",
    "column",
    "cursor",
]


def build_cli() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate many .txt files with random words")
    p.add_argument("--out", default="data/bigset", help="Output folder")
    p.add_argument("--files", type=int, default=200, help="Number of files to generate")
    p.add_argument("--words-per-file", type=int, default=300, help="Words per file")
    p.add_argument("--seed", type=int, default=42, help="RNG seed")
    return p


def main():
    args = build_cli().parse_args()
    random.seed(args.seed)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    for i in range(1, args.files + 1):
        words = random.choices(VOCAB, k=args.words_per_file)
        text = " ".join(words) + "\n"
        (out / f"doc_{i:05d}.txt").write_text(text, encoding="utf-8")

    print(f"Generated {args.files} files to {out}")


if __name__ == "__main__":
    main()
