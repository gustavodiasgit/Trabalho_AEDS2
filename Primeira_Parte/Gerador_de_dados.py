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

n = int(input('Digite quantos registros você quer gerar: '))

with open(arquivo, "wb") as f:
    for _ in range(n):
        matricula = fake.numerify(text='#########')
        nome = fake.name()[:50]
        cpf = fake.cpf()
        curso = gerar_curso()[:30]
        mae = fake.name_female()[:30]
        pai = fake.name_male()[:30]
        ano = fake.year()
        ca = fake.numerify(text='#.##')

        linha = f"{matricula};{nome};{cpf};{curso};{mae};{pai};{ano};{ca}\n"
        f.write(linha.encode('utf-8'))

print(f"{n} registros foram salvos em '{arquivo}'.")
