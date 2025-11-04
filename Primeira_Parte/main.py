from pathlib import Path
import sys
import os

# Caminho do arquivo original
data_path = Path(__file__).resolve().parent / "dados.dat"

# Verifica se o arquivo existe
if not data_path.exists():
    print(f"Arquivo não encontrado: {data_path}", file=sys.stderr)
    sys.exit(1)

# Diretório de saída para os blocos
saida_dir = data_path.parent / "blocos_saida"
saida_dir.mkdir(exist_ok=True)

# Limite de memória (em bytes)
limite = 50 * 1024  #50 bytes

# Contadores e estruturas auxiliares
contador_arquivos = 1
bytes_lidos = 0
bloco = []

# Leitura e escrita em blocos
with data_path.open(encoding="utf-8") as f:
    for linha in f:
        bloco.append(linha)
        bytes_lidos += len(linha.encode("utf-8"))

        # Se atingir o limite, salva o bloco em um novo arquivo
        if bytes_lidos >= limite:
            nome_saida = saida_dir / f"bloco_{contador_arquivos:03d}.dat"
            with nome_saida.open("w", encoding="utf-8") as out:
                out.writelines(bloco)

            print(f"✅ Bloco {contador_arquivos} salvo: {nome_saida.name} ({bytes_lidos/1024/1024:.2f} MB)")

            # Reseta os contadores
            contador_arquivos += 1
            bytes_lidos = 0
            bloco = []

# Salva o último bloco restante
if bloco:
    nome_saida = saida_dir / f"bloco_{contador_arquivos:03d}.dat"
    with nome_saida.open("w", encoding="utf-8") as out:
        out.writelines(bloco)
    print(f"✅ Bloco {contador_arquivos} salvo (último): {nome_saida.name} ({bytes_lidos/1024/1024:.2f} MB)")

print("Processamento concluído")
