from pathlib import Path
import sys
import Gerador_de_dados as gd


def validar_entrada(prompt, min_val, max_val, mensagem_erro):
    """Valida entrada numérica dentro do intervalo especificado"""
    while True:
        try:
            valor = int(input(prompt))
            if min_val <= valor <= max_val:
                return valor
            raise ValueError
        except ValueError:
            print(f"⚠ Erro: {mensagem_erro}")
            if input("Tentar novamente? (s/n): ").lower() != 's':
                sys.exit(1)


def salvar_bloco(bloco, contador, bytes_lidos, limite, modo=""):
    """Salva um bloco em arquivo e retorna bytes salvos"""
    nome_saida = saida_dir / f"bloco_{contador:03d}.dat"
    with nome_saida.open("wb") as out:
        out.writelines([
            registro if isinstance(registro, bytes) else registro.encode("utf-8")
            for registro in bloco
        ])

    # Atualiza contador global de blocos
    global blocos_criados
    blocos_criados += 1

    ocupacao = (bytes_lidos / limite) * 100 if limite > 0 else 0
    print(f"📦 Bloco {contador} salvo{f' ({modo})' if modo else ''}: {ocupacao:.1f}% ocupado")
    return bytes_lidos


def processar_registro(registro, tamanho_registro, bytes_lidos, limite):
    """Verifica se um registro cabe no bloco atual"""
    if tamanho_registro > limite:
        print("⚠ Registro maior que o limite! Ignorado.")
        return False
    return bytes_lidos + tamanho_registro <= limite


# Diretório do arquivo de dados
data_path = Path(__file__).resolve().parent / "dados.dat"

# Diretório de saída para os blocos
saida_dir = data_path.parent / "blocos_saida"
saida_dir.mkdir(exist_ok=True)

# Algoritmo para excluir arquivos antigos presentes na pasta de saída
for arquivo_existente in saida_dir.iterdir():
    if arquivo_existente.is_file():
        try:
            arquivo_existente.unlink()
        except Exception as e:
            print(f"⚠ Não foi possível deletar {arquivo_existente.name}: {e}")

# Escolha do modo de operação
print("\n=== Configuração do Processamento ===")
escolha = validar_entrada(
    "Escolha o modo de operação:\n1 - Registros de tamanho fixo\n2 - Registros de tamanho variável\nOpção: ",
    1,
    2,
    "Escolha deve ser 1 (fixo) ou 2 (variável)"
)

# Definição do limite de memória (agora em BYTES)
print("\n=== Configuração de Memória ===")
limite = validar_entrada(
    "Digite o limite de memória em BYTES para cada bloco: ",
    1,
    1024 * 1024 * 1024,  # 1 byte até 1 GB
    "Limite deve ser entre 1 e 1.073.741.824 bytes (1 GB)"
)

print(f"Limite configurado: {limite:,} bytes")

# Contadores auxiliares
contador_arquivos = 1
bytes_lidos = 0
bloco = []
bytes_totais = 0
blocos_criados = 0

# Escolha do modo principal
match escolha:
    # =====================================================
    # MODO 1 - REGISTROS DE TAMANHO FIXO
    # =====================================================
    case 1:
        gd.gerador_fixo()

        with data_path.open(encoding="utf-8") as f:
            for linha in f:
                registro = linha.encode("utf-8")
                tamanho = len(registro)

                if tamanho > limite:
                    print("⚠ Registro maior que o limite! Ignorado.")
                    continue

                # Se o registro atual não couber no bloco, salva o bloco atual
                if bytes_lidos + tamanho > limite:
                    if bloco:
                        bytes_totais += salvar_bloco(bloco, contador_arquivos, bytes_lidos, limite)
                        contador_arquivos += 1
                    bloco = []
                    bytes_lidos = 0

                bloco.append(registro)
                bytes_lidos += tamanho

            # Salva o último bloco restante
            if bloco:
                bytes_totais += salvar_bloco(bloco, contador_arquivos, bytes_lidos, limite, "último")

    # =====================================================
    # MODO 2 - REGISTROS DE TAMANHO VARIÁVEL
    # =====================================================
    case 2:
        gd.gerador_variavel()

        print("Escolha o modo como irá trabalhar com os registros de tamanho variável:")
        print("1 - Contíguos (sem espalhamento)")
        print("2 - Espalhados (fragmentados entre blocos)")
        sub_escolha = int(input("Digite a opção desejada: "))

        match sub_escolha:
            # -----------------------------------------------------
            # MODO CONTÍGUO (cada registro inteiro em um bloco)
            # -----------------------------------------------------
            case 1:
                with data_path.open(encoding="utf-8") as f:
                    for linha in f:
                        registro = linha.encode("utf-8")
                        tamanho = len(registro)

                        if tamanho > limite:
                            print("⚠ Registro maior que o limite! Ignorado.")
                            continue

                        if not processar_registro(registro, tamanho, bytes_lidos, limite):
                            bytes_totais += salvar_bloco(
                                bloco, contador_arquivos, bytes_lidos, limite, "contíguo"
                            )
                            contador_arquivos += 1
                            bloco = []
                            bytes_lidos = 0

                        bloco.append(registro)
                        bytes_lidos += tamanho

                # Salva o último bloco após o processamento
                if bloco:
                    bytes_totais += salvar_bloco(
                        bloco, contador_arquivos, bytes_lidos, limite, "último"
                    )

            # -----------------------------------------------------
            # MODO ESPALHADO (fragmenta registros entre blocos)
            # -----------------------------------------------------
            case 2:
                with data_path.open(encoding="utf-8") as f:
                    for linha in f:
                        registro = linha.encode("utf-8")
                        tamanho_restante = len(registro)
                        inicio = 0

                        # Enquanto ainda houver bytes do registro a gravar
                        while tamanho_restante > 0:
                            espaco = limite - bytes_lidos

                            # Se o bloco atual estiver cheio, salva e inicia um novo
                            if espaco == 0:
                                bytes_totais += salvar_bloco(
                                    bloco, contador_arquivos, bytes_lidos, limite, "espalhado"
                                )
                                contador_arquivos += 1
                                bloco = []
                                bytes_lidos = 0
                                espaco = limite

                            # Calcula o tamanho da parte que cabe neste bloco
                            parte = min(tamanho_restante, espaco)

                            # Adiciona o fragmento atual
                            bloco.append(registro[inicio:inicio + parte])
                            bytes_lidos += parte

                            # Atualiza os ponteiros
                            inicio += parte
                            tamanho_restante -= parte

                            # Se o bloco ficou cheio, salva imediatamente
                            if bytes_lidos == limite:
                                bytes_totais += salvar_bloco(
                                    bloco, contador_arquivos, bytes_lidos, limite, "espalhado"
                                )
                                contador_arquivos += 1
                                bloco = []
                                bytes_lidos = 0

                # Salva o último bloco após processamento
                if bloco:
                    bytes_totais += salvar_bloco(
                        bloco, contador_arquivos, bytes_lidos, limite, "último"
                    )

# =====================================================
# RELATÓRIO FINAL
# =====================================================
print("\n=== Processamento concluído ===")
print(f"Total de blocos criados: {blocos_criados}")

if blocos_criados > 0 and limite > 0:
    eficiencia = bytes_totais / (blocos_criados * limite) * 100
    print(f"Eficiência total: {eficiencia:.1f}%")
else:
    print("Eficiência total: 0%")
