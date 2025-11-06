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

                    print(f"✅ Bloco {contador_arquivos} salvo: {nome_saida.name} ({(bytes_lidos/limite)*100:.0f}% ocupado)")

                    #Reseta os contadores
                    contador_arquivos += 1
                    bytes_totais += bytes_lidos
                    bytes_lidos = 0
                    bloco = []

                # Salva o último bloco restante
            if bloco:
                nome_saida = saida_dir / f"bloco_{contador_arquivos:03d}.dat"
                with nome_saida.open("w", encoding="utf-8") as out:
                    out.writelines(bloco)
                print(f"✅ Bloco {contador_arquivos} salvo (último): {nome_saida.name} ({(bytes_lidos/limite)*100:.0f}% ocupado)")

    case 2:

        #Chamada de função para gerar dados de tamanho variável
        gd.gerador_variavel()

        print("Escolha o modo como irá trabalhar com os registros de tamanho variável:\n1 - Contíguos (sem espalhamento)\n2 - Espalhados (fragmentados entre blocos)")
        sub_escolha = int(input("Digite a opção desejada: "))


print("Processamento concluído")
print("Total de blocos criados:", contador_arquivos)
print(f"Eficiência total: {bytes_totais / (contador_arquivos * limite) * 100:.0f}%")
