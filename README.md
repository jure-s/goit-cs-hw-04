# goit-cs-hw-04 — Паралельний пошук ключових слів у текстових файлах

## Мета
Реалізувати пошук ключових слів у наборі `.txt` файлів із трьома режимами виконання:
- `single` — базовий послідовний пошук;
- `threading` — паралелізація на потоках (I/O-bound сценарії);
- `multiprocessing` — паралелізація на процесах (CPU-bound сценарії).

Повертається словник у форматі: `word -> [list_of_files]`. Є вимірювання часу виконання.

---

## Структура проєкту
```
goit-cs-hw-04/
├─ README.md
├─ requirements.txt
├─ pytest.ini
├─ .flake8
├─ pyproject.toml
├─ main.py
├─ data/
│  └─ sample_texts/
│     ├─ doc1.txt
│     ├─ doc2.txt
│     └─ doc3.txt
├─ src/
│  ├─ __init__.py
│  ├─ common/
│  │  ├─ __init__.py
│  │  ├─ io_utils.py
│  │  ├─ search_logic.py
│  │  ├─ timing.py
│  │  └─ validators.py
│  ├─ threading_version/
│  │  ├─ __init__.py
│  │  ├─ runner.py
│  │  └─ worker.py
│  └─ multiprocessing_version/
│     ├─ __init__.py
│     ├─ runner.py
│     └─ worker.py
├─ tests/
│  ├─ test_search_logic.py
│  ├─ test_threading_runner.py
│  └─ test_multiprocessing_runner.py
└─ scripts/
   ├─ generate_texts.py
   ├─ run_all.ps1
   └─ run_all.sh
```

---

## Встановлення
Python 3.11+ (перевірено на 3.13).

```bash
python -m venv .venv
# Windows
. .venv/Scripts/activate
# Linux/macOS
# source .venv/bin/activate

pip install -r requirements.txt
```

`requirements.txt` містить:
```
pytest
black
isort
flake8
mypy
```

---

## Використання

### 1) Приклади запуску
```bash
# Послідовно
python main.py --words "apple, banana, mango" --path data/sample_texts --mode single

# Потоки (4 потоки)
python main.py --words "apple, banana, mango" --path data/sample_texts --mode threading --workers 4

# Процеси (4 процеси)
python main.py --words "apple, banana, mango" --path data/sample_texts --mode multiprocessing --workers 4
```

Вивід (приклад):
```
Result (word -> files):
  apple:
    - data/sample_texts/doc1.txt
    - data/sample_texts/doc3.txt
  banana:
    - data/sample_texts/doc1.txt
    - data/sample_texts/doc2.txt
  mango:
    - data/sample_texts/doc2.txt
    - data/sample_texts/doc3.txt

Elapsed: 0.00xxx s
```

### 2) Генерація великого набору файлів
```bash
python scripts/generate_texts.py --out data/bigset --files 500 --words-per-file 500 --seed 42
```

### 3) Порівняння часу (готові скрипти)
- **Windows PowerShell**:
  ```powershell
  scriptsun_all.ps1 -Path "dataigset" -Words "apple,banana,mango,python,sql,postgresql" -Workers 8
  ```
- **Linux/macOS**:
  ```bash
  bash scripts/run_all.sh --path data/bigset --words "apple,banana,mango,python,sql,postgresql" --workers 8
  ```
> На Windows `.sh` не обовʼязково виконувати (призначено для Linux/macOS).

---

## Тести та перевірки стилю
```bash
# автоформатування та сортування імпортів
black .
isort .

# лінтер та статичний аналіз
flake8
mypy src

# тести
pytest -q
```
Файли конфігурацій: `pytest.ini`, `.flake8`, `pyproject.toml`.

---

## Дизайн-рішення
- **Пошук**: нечутливий до регістру; перевіряємо входження підрядка (substring) — простий і швидкий підхід для текстів.
- **Threading**: `ThreadPoolExecutor` — ефективний для I/O-bound задач (паралельне читання файлів під GIL).
- **Multiprocessing**: `multiprocessing.Pool` з топ-рівневими функціями (сумісно з Windows `spawn`) — доцільно для CPU-bound обробки.
- **Обробка помилок FS**: валідація шляху, безпечне читання UTF-8 з `errors="ignore"`.
- **Вимір часу**: контекст-менеджер `timer()` друкує сумарний час виконання.
- **Тести** створюють тимчасові файли самостійно (не залежать від `data/`).

---

## Висновки (бенчмарк на реальних даних)
Набір: `data\bigset` (**500 файлів × 500 слів**), слова: `apple,banana,mango,python,sql,postgresql`, Workers: 8.

```
single           14.801281 s
threading         0.180834 s
multiprocessing   0.479504 s
```
- На **I/O-bound** задачі (читання файлів) `threading` показує найкращий час завдяки паралельному I/O.
- `multiprocessing` теж суттєво швидший за `single`, але має оверхед створення процесів/серіалізації.
- Для **CPU-bound** (важка обробка тексту) очікувано перемагає `multiprocessing`.

---

## .gitignore (рекомендовано)
```
.venv/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
dist/
data/bigset/
*.zip
.DS_Store
.vscode/
.idea/
```
