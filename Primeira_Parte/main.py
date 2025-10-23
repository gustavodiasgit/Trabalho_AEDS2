from pathlib import Path
import sys

data_path = Path(__file__).resolve().parent / "dados.dat"

if not data_path.exists():
    print(f"Arquivo não encontrado: {data_path}", file=sys.stderr)
    sys.exit(1)

with data_path.open(encoding="utf-8") as f:
    for linhas in f:
        campos = linhas.strip().split(";")
        print(campos)
