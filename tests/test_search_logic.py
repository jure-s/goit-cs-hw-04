from pathlib import Path

from src.common.search_logic import search_words_in_file


def test_search_words_in_file(tmp_path: Path):
    p = tmp_path / "doc.txt"
    p.write_text("Apple banana. PostgreSQL and Mango.", encoding="utf-8")
    words = ["apple", "banana", "mango", "python"]
    flags = search_words_in_file(str(p), words)
    assert flags == {
        "apple": True,
        "banana": True,
        "mango": True,
        "python": False,
    }
