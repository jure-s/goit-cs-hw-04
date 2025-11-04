from pathlib import Path

from src.threading_version.runner import run_search


def test_threading_run_search(tmp_path: Path):
    (tmp_path / "d1.txt").write_text("Apple banana apple.", encoding="utf-8")
    (tmp_path / "d2.txt").write_text("Mango and banana.", encoding="utf-8")
    (tmp_path / "d3.txt").write_text("PostgreSQL. Apple pie.", encoding="utf-8")

    files = [str(p) for p in tmp_path.glob("*.txt")]
    words = ["apple", "banana", "mango", "python"]

    result = run_search(files, words, workers=4)

    # порівнюємо множинами, бо порядок файлів у результаті не гарантований
    assert set(result["apple"]) == {str(tmp_path / "d1.txt"), str(tmp_path / "d3.txt")}
    assert set(result["banana"]) == {str(tmp_path / "d1.txt"), str(tmp_path / "d2.txt")}
    assert set(result["mango"]) == {str(tmp_path / "d2.txt")}
    assert result["python"] == []
