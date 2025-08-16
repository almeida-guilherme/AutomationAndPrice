def getCurrentCotacao():
    import requests
    import os
    from dotenv import load_dotenv
    
    #Preparar o ambiente
    load_dotenv()

    url = f"https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BRL-USD?token={os.getenv("API_KEY")}"

    try:
        # Fazendo a requisição GET para a URL
        resposta = requests.get(url)
        
        # Converte a resposta JSON em um dicionário Python
        dados = resposta.json()
        
        return dados
        
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro na requisição: {e}")

    except ValueError as e:
        print(f"Ocorreu um erro ao decodificar a resposta JSON: {e}")