set -e

PATH_ARG="data/sample_texts"
WORDS_ARG="apple,banana,mango"
WORKERS_ARG=4

while [[ $# -gt 0 ]]; do
  case "$1" in
    --path) PATH_ARG="$2"; shift 2 ;;
    --words) WORDS_ARG="$2"; shift 2 ;;
    --workers) WORKERS_ARG="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

echo "=== Benchmark modes on ${PATH_ARG} ==="
echo "Words: ${WORDS_ARG}"
echo "Workers: ${WORKERS_ARG}"
echo

echo "[single]"
python ./main.py --path "${PATH_ARG}" --words "${WORDS_ARG}" --mode single | grep "Elapsed:"

echo
echo "[threading]"
python ./main.py --path "${PATH_ARG}" --words "${WORDS_ARG}" --mode threading --workers "${WORKERS_ARG}" | grep "Elapsed:"

echo
echo "[multiprocessing]"
python ./main.py --path "${PATH_ARG}" --words "${WORDS_ARG}" --mode multiprocessing --workers "${WORKERS_ARG}" | grep "Elapsed:"
