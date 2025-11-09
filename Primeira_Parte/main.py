from pathlib import Path
import sys
import Gerador_de_dados as gd

#Diretório do arquivo de dados
data_path = Path(__file__).resolve().parent / "dados.dat"

#Verificação se o arquivo existe no diretório
if not data_path.exists():
    print(f"Arquivo não encontrado: {data_path}", file=sys.stderr)
    sys.exit(1)

#Diretório de saída para os blocos
saida_dir = data_path.parent / "blocos_saida"
saida_dir.mkdir(exist_ok=True)

#Algorítmo para excluir arquivos antigos presentes na pasta de saída 
for arquivo_existente in saida_dir.iterdir(): 
    if arquivo_existente.is_file(): 
        try: 
            arquivo_existente.unlink() 
        except Exception as e: 
            print(f"⚠ Não foi possível deletar {arquivo_existente.name}: {e}")

#Definição do limite de memória (em bytes)
limite = int(input("Digite o limite de memória em bytes para cada bloco: "))
limite = limite * 1024  # Convertendo para bytes

#Contadores auxiliares
contador_arquivos = 1
bytes_lidos = 0
bloco = []
bytes_totais = 0;

escolha = int(input("Escolha o modo de operação:\n1 - Registros de tamanho fixo\n2 - Registros de tamanho variável\nDigite a opção desejada: "))

match escolha:
    case 1:

        #Chamada de função para gerar dados de tamanho fixo
        gd.gerador_fixo()
        # Leitura e escrita em blocos
        with data_path.open(encoding="utf-8") as f:
            for linha in f:
                bloco.append(linha)
                bytes_lidos += len(linha.encode("utf-8"))

                #Se atingir o limite, salva o bloco em um novo arquivo
                if bytes_lidos >= limite:
                    nome_saida = saida_dir / f"bloco_{contador_arquivos:03d}.dat"
                    with nome_saida.open("w", encoding="utf-8") as out:
                        out.writelines(bloco)

                    print(f"Bloco {contador_arquivos} salvo: {nome_saida.name} ({(bytes_lidos/limite)*100:.0f}% ocupado)")

                    #Reseta os contadores
                    contador_arquivos += 1
                    bytes_totais += bytes_lidos
                    bytes_lidos = 0
                    bloco = []

            #Salva o último bloco restante
            if bloco:
                nome_saida = saida_dir / f"bloco_{contador_arquivos:03d}.dat"
                with nome_saida.open("w", encoding="utf-8") as out:
                    out.writelines(bloco)
                print(f"Bloco {contador_arquivos} salvo (último): {nome_saida.name} ({(bytes_lidos/limite)*100:.0f}% ocupado)")

    case 2:
        # Chamada à função para gerar registros variáveis
        gd.gerador_variavel()

        print("Escolha o modo como irá trabalhar com os registros de tamanho variável:")
        print("1 - Contíguos (sem espalhamento)")
        print("2 - Espalhados (fragmentados entre blocos)")
        sub_escolha = int(input("Digite a opção desejada: "))

        match sub_escolha:
            #MODO CONTÍGUO
            case 1:
                with data_path.open(encoding="utf-8") as f:
                    for linha in f:
                        registro = linha.encode("utf-8")
                        tamanho = len(registro)

                        if tamanho > limite:
                            print("⚠ Registro maior que o limite! Ignorado.")
                            continue

                        if bytes_lidos + tamanho > limite:
                            nome_saida = saida_dir / f"bloco_{contador_arquivos:03d}.dat"
                            with nome_saida.open("wb") as out:
                                out.writelines(bloco)
                            print(f"📦 Bloco {contador_arquivos} salvo (contíguo): {(bytes_lidos/limite)*100:.0f}% ocupado")

                            bytes_totais += bytes_lidos
                            contador_arquivos += 1
                            bloco = []
                            bytes_lidos = 0

                        bloco.append(registro)
                        bytes_lidos += tamanho

            #MODO ESPALHADO
            case 2:
                with data_path.open(encoding="utf-8") as f:
                    for linha in f:
                        registro = linha.encode("utf-8")
                        restante = len(registro)
                        inicio = 0

                        while restante > 0:
                            espaco = limite - bytes_lidos

                            #bloco cheio → salvar e criar novo
                            if espaco == 0:
                                nome_saida = saida_dir / f"bloco_{contador_arquivos:03d}.dat"
                                with nome_saida.open("wb") as out:
                                    out.writelines(bloco)
                                print(f"Bloco {contador_arquivos} salvo (espalhado): 100% ocupado")

                                bytes_totais += bytes_lidos
                                contador_arquivos += 1
                                bloco = []
                                bytes_lidos = 0
                                espaco = limite

                            #salva parte do registro
                            parte = min(restante, espaco)
                            bloco.append(registro[inicio:inicio+parte])
                            bytes_lidos += parte
                            restante -= parte
                            inicio += parte

        #Salva o último bloco após processamento
        if bloco:
            nome_saida = saida_dir / f"bloco_{contador_arquivos:03d}.dat"
            with nome_saida.open("wb") as out:
                out.writelines(bloco)
            print(f"✅ Bloco {contador_arquivos} salvo (último): {(bytes_lidos/limite)*100:.0f}% ocupado")
            bytes_totais += bytes_lidos

print("Processamento concluído")
print("Total de blocos criados:", contador_arquivos)
print(f"Eficiência total: {bytes_totais / (contador_arquivos * limite) * 100:.0f}%")