from faker import Faker
import random
from pathlib import Path

script_dir = Path(__file__).resolve().parent
arquivo = script_dir / "dados.dat"

fake = Faker('pt_BR')
areas = ["Engenharia", "Ciência", "Gestão", "Tecnologia", "Design", "Administração"]
especialidades = ["Software", "Dados", "Sistemas", "Ambiental", "Marketing", "Financeira", "Industrial"]

def gerar_curso():
    return f"{random.choice(areas)} de {random.choice(especialidades)}"

def ajustar(texto, tamanho):
    return texto[:tamanho].ljust(tamanho, '#')

def gerador_fixo():

    n = int(input("Digite quantos registros você quer gerar: "))

    with open(arquivo, "wb") as f:
        for _ in range(n):
            matricula = ajustar(fake.numerify('#########'), 9)
            nome = ajustar(fake.name(), 50)
            cpf = ajustar(fake.cpf(), 14)
            curso = ajustar(gerar_curso(), 30)
            #Randomizador para gerar nomes de pais com possibilidade de campo vazio
            prob_branco = 0.05  # 5% de chance de ficar vazio
            mae_valor = fake.name_female() if random.random() > prob_branco else ""
            pai_valor = fake.name_male() if random.random() > prob_branco else ""
            mae = ajustar(fake.name_female(), 30)
            pai = ajustar(fake.name_male(), 30)
            ano = ajustar(fake.year(), 4)
            ca = ajustar(fake.numerify('#.##'), 4)

            linha = f"{matricula};{nome};{cpf};{curso};{mae};{pai};{ano};{ca}\n"
            f.write(linha.encode("utf-8"))

    print(f"{n} registros foram salvos em '{arquivo}'.")

def gerador_variavel():

    n = int(input("Digite quantos registros você quer gerar: "))

    with open(arquivo, "wb") as f:
        for _ in range(n):
            matricula = fake.numerify('#########'), 9
            nome = fake.name(), 50
            cpf = fake.cpf(), 14
            curso = gerar_curso(), 30
            #Randomizador para gerar nomes de pais com possibilidade de campo vazio
            prob_branco = 0.05  # 5% de chance de ficar vazio
            mae_valor = fake.name_female() if random.random() > prob_branco else ""
            pai_valor = fake.name_male() if random.random() > prob_branco else ""
            mae = fake.name_female(), 30
            pai = fake.name_male(), 30
            ano = fake.year(), 4
            ca = fake.numerify('#.##'), 4

            linha = f"{matricula};{nome};{cpf};{curso};{mae};{pai};{ano};{ca}\n"
            f.write(linha.encode("utf-8"))

    print(f"{n} registros foram salvos em '{arquivo}'.")
