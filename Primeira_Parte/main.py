with open("dados.dat", "r") as f:
    linhas = f.read()

for linha in linhas:
    valores = linha.strip().spli(",")
    print(valores)
