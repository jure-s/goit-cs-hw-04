param(
  [string]$Path = "data\sample_texts",
  [string]$Words = "apple,banana,mango",
  [int]$Workers = 4
)

Write-Host "=== Benchmark modes on $Path ==="
Write-Host "Words: $Words"
Write-Host "Workers: $Workers`n"

Write-Host "[single]"
python .\main.py --path $Path --words $Words --mode single | Select-String "Elapsed:"

Write-Host "`n[threading]"
python .\main.py --path $Path --words $Words --mode threading --workers $Workers | Select-String "Elapsed:"

Write-Host "`n[multiprocessing]"
python .\main.py --path $Path --words $Words --mode multiprocessing --workers $Workers | Select-String "Elapsed:"
