import requests, csv

tipos_de_proposicoes = ["pl", "pls", "pec", "plp", "mpv", "msc", "msg", "pdc", "pln", "plv", "prc", "vet"]

soma = 0
dados_csv = []

for c in tipos_de_proposicoes:
    url_proposicoes = "https://legis.senado.leg.br/dadosabertos/materia/pesquisa/lista?sigla={}&ano=1988".format(c)
    headers = {"Accept": "application/json"}
    response_proposicoes = requests.get(url_proposicoes, headers=headers)

    if response_proposicoes.status_code == 200:
        try:
            dados_proposicoes = response_proposicoes.json().get('PesquisaBasicaMateria', {}).get('Materias', {}).get('Materia',{})
        except KeyError:
            dados_proposicoes = []

    for proposicao in dados_proposicoes:
        dados_combinados = {
                "Codigo": proposicao.get("Codigo"),
                "IdentificacaoProcesso": proposicao.get("IdentificacaoProcesso"),
                "DescricaoIdentificacao": proposicao.get("DescricaoIdentificacao"),  
                "Autor": proposicao.get("Autor"),
                "Data": proposicao.get("Data"),
                "UrlDetalheMateria": proposicao.get("UrlDetalheMateria")
            }
        soma += 1
        dados_csv.append([
                dados_combinados["Codigo"],
                dados_combinados["IdentificacaoProcesso"],
                dados_combinados["DescricaoIdentificacao"],
                dados_combinados["Autor"],
                dados_combinados["Data"],
                dados_combinados["UrlDetalheMateria"],
            ])

        print(" ")
        print("Proposição {:,}".format(soma))
        print(
                "Código: {}\nIdentificação Processo:{}\nDescrição Identificação:{}\nAutor: {}\nData: {}\nUrl: {}".format(
                    dados_combinados["Codigo"], dados_combinados["IdentificacaoProcesso"],
                    dados_combinados["DescricaoIdentificacao"],  
                    dados_combinados["Autor"], dados_combinados["Data"], dados_combinados["UrlDetalheMateria"]))


with open("dados_proposicoes.csv", mode="w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["ID", "Identificação Processo", "Matéria", "Autor", "Data", "Número", "URL"])
    writer.writerows(dados_csv)