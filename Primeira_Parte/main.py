from pathlib import Path
import sys
import Gerador_de_dados as gd

# Diretório do arquivo de dados
data_path = Path(__file__).resolve().parent / "dados.dat"

# Entrada de tipo de registro antes de qualquer verificação
escolha = int(input("Escolha o tipo de registro:\n1 - Tamanho fixo\n2 - Tamanho variável\nDigite a opção desejada: "))

# Geração dos dados antes de verificar se o arquivo existe
if escolha == 1:
    gd.gerador_fixo()
else:
    gd.gerador_variavel()

# Verificação se o arquivo existe agora sim ✅
if not data_path.exists():
    print(f"Arquivo não encontrado: {data_path}", file=sys.stderr)
    sys.exit(1)

# Diretório de saída
saida_dir = data_path.parent / "blocos_saida"
saida_dir.mkdir(exist_ok=True)

# Remove blocos antigos
for arquivo_existente in saida_dir.iterdir():
    if arquivo_existente.is_file():
        arquivo_existente.unlink()

# Definição do limite
limite = int(input("Digite o limite de memória em KB para cada bloco: "))
limite *= 1024

contador_arquivos = 1
bytes_lidos = 0
bloco = []
bytes_totais = 0

# Se variável, perguntar contíguo ou espalhado
if escolha == 2:
    sub_escolha = int(input("Modo variável:\n1 - Contíguos\n2 - Espalhados\nOpção: "))

with data_path.open("r", encoding="utf-8") as f:
    for linha in f:
        registro = linha.encode("utf-8")
        tamanho = len(registro)

        if escolha == 1:  # FIXO
            bloco.append(linha)
            bytes_lidos += tamanho

            if bytes_lidos >= limite:
                nome_saida = saida_dir / f"bloco_{contador_arquivos:03d}.dat"
                with nome_saida.open("w", encoding="utf-8") as out:
                    out.writelines(bloco)

                print(f"📦 Bloco {contador_arquivos} salvo: {(bytes_lidos/limite)*100:.0f}% ocupado")

                contador_arquivos += 1
                bytes_totais += bytes_lidos
                bytes_lidos = 0
                bloco = []

        else:  # VARIÁVEL
            if sub_escolha == 1:  # CONTÍGUOS
                if tamanho > limite:
                    print("⚠ Registro maior que o limite, ignorado")
                    continue

                if bytes_lidos + tamanho > limite:
                    nome_saida = saida_dir / f"bloco_{contador_arquivos:03d}.dat"
                    with nome_saida.open("wb") as out:
                        out.writelines(bloco)

                    print(f"📦 Bloco {contador_arquivos} salvo (contíguo): {(bytes_lidos/limite)*100:.0f}% ocupado")

                    contador_arquivos += 1
                    bytes_totais += bytes_lidos
                    bloco = []
                    bytes_lidos = 0

                bloco.append(registro)
                bytes_lidos += tamanho

            else:  # ESPALHADO
                restante = tamanho
                inicio = 0

                while restante > 0:
                    espaco = limite - bytes_lidos

                    if espaco == 0:
                        nome_saida = saida_dir / f"bloco_{contador_arquivos:03d}.dat"
                        with nome_saida.open("wb") as out:
                            out.writelines(bloco)

                        print(f"📦 Bloco {contador_arquivos} salvo (espalhado): 100% ocupado")

                        contador_arquivos += 1
                        bytes_totais += bytes_lidos
                        bloco = []
                        bytes_lidos = 0
                        espaco = limite

                    parte = min(restante, espaco)
                    bloco.append(registro[inicio:inicio+parte])
                    bytes_lidos += parte
                    restante -= parte
                    inicio += parte

# Salva último bloco
if bloco:
    nome_saida = saida_dir / f"bloco_{contador_arquivos:03d}.dat"
    with nome_saida.open("wb") as out:
        for linha in bloco:
            out.write(linha.encode('utf-8'))
    print(f"✅ Bloco {contador_arquivos} salvo (último): {(bytes_lidos/limite)*100:.0f}% ocupado")
    bytes_totais += bytes_lidos

# Cálculo real da quantidade de blocos
quantidade_blocos = contador_arquivos
eficiencia = bytes_totais / (quantidade_blocos * limite) * 100

print("\n📌 --- Processamento concluído! ---")
print(f"📦 Total de blocos criados: {quantidade_blocos}")
print(f"📊 Eficiência total: {eficiencia:.0f}%")
