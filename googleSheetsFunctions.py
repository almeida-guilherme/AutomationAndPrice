import gspread
from oauth2client.service_account import ServiceAccountCredentials
GOOGLE_SHEET_NAME = 'Cotações de Moedas'

# --- Funções do Google Sheets ---
def setup_google_sheets():
    """
    Configura a conexão com o Google Sheets.
    NOTA: Requer um arquivo de credenciais JSON.
    """
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client

def write_to_google_sheets(data):
    """Escreve os dados na planilha do Google Sheets."""
    try:
        client = setup_google_sheets()
        sheet = client.open(GOOGLE_SHEET_NAME).sheet1
        
        # Cria uma linha com os dados
        row = [
            data["data_atualizacao"],
            data["cotacoes"]["USD-BRL"],
            data["cotacoes"]["EUR-BRL"],
            data["variacao_usd_percentual"]
        ]
        
        # Adiciona a linha na planilha
        sheet.append_row(row)
        print("Dados gravados no Google Sheets com sucesso.")
    except Exception as e:
        print(f"Erro ao escrever no Google Sheets: {e}")
