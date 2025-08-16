import streamlit as st
from datetime import datetime
import pandas as pd
import databaseCotacao as db
from getCotacao import getCurrentCotacao
from sendEmail import send_notification_email, send_weekly_summary_email
from googleSheetsFunctions import write_to_google_sheets

def calcular_variacao_percentual(valor_atual, valor_anterior):
    """Calcula a variação percentual entre dois valores."""
    if valor_anterior is None or valor_anterior == 0:
        return 0
    return ((valor_atual - valor_anterior) / valor_anterior) * 100

# --- Interface do Streamlit ---

st.title("💰 Painel de Cotação de Moedas")

st.markdown("""
    Este painel exibe as cotações atualizadas de moedas e monitora a variação do dólar.
""")

# Configura o banco de dados antes de qualquer outra operação
db.setup_database()

# Busca os dados da API
api_data = getCurrentCotacao()

if api_data:
    # Obtém as cotações atuais do dólar e euro
    usd_valor_atual = float(api_data['USDBRL']['bid'])
    eur_valor_atual = float(api_data['EURBRL']['bid'])


    # Obtém a cotação do dólar do banco de dados (que é a do dia anterior)
    usd_anterior = db.get_cotacao('USD-BRL')

    # Salva a nova cotação do dólar para a próxima verificação
    db.save_cotacao('USD-BRL',usd_valor_atual)

    if usd_anterior:
        variacao_usd = calcular_variacao_percentual(usd_valor_atual, usd_anterior[0])
        st.subheader("Análise de Variação do Dólar")
        st.metric(
            label="Variação do Dólar (USD/BRL) em relação ao último valor salvo",
            value=f"{variacao_usd:.2f}%",
            delta=f"{variacao_usd:.2f}%" # Exibe a variação como delta visual
        )

        # Placeholder para o e-mail de notificação de variação
        if abs(variacao_usd) > 2:
            st.warning("⚠️ **ALERTA!** A variação do dólar é maior que 2%. A função de envio de e-mail será ativada.")
            if send_notification_email(usd_valor_atual, variacao_usd):
                st.success("✅ E-mail de notificação enviado com sucesso!")
            else:
                st.error("❌ Erro ao enviar o e-mail de notificação.")

    # Salva a nova cotação do dólar para a próxima verificação
    db.save_cotacao('USD-BRL', usd_valor_atual)

    # --- Exibição das Cotações no Painel ---
    st.subheader("Cotações Atuais")

    # Organiza os dados em um DataFrame do pandas para exibição em tabela
    data = {
        'Moeda': ['USD/BRL', 'EUR/BRL'],
        'Valor (R$)': [f"{usd_valor_atual:.2f}", f"{eur_valor_atual:.2f}"]
    }
    df_cotacoes = pd.DataFrame(data)
    data_to_sheets = {
        "cotacoes": {
            "USD-BRL": usd_valor_atual,
            "EUR-BRL": eur_valor_atual
        },
        "variacao_usd_percentual": variacao_usd,
        "data_atualizacao": datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    }

    write_to_google_sheets(data_to_sheets)
    # Adiciona a data e hora da última atualização
    df_cotacoes['Última Atualização'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    # Exibe a tabela de forma elegante
    st.table(df_cotacoes.set_index('Moeda'))

    # Exemplo de como você chamaria a função de e-mail semanal (não precisa rodar sempre)
    if st.button("Enviar E-mail da cotação"):
        st.info("Enviando e-mail da cotação...")
        cotacoes_para_resumo = {
            'USD-BRL': usd_valor_atual,
            'EUR-BRL': eur_valor_atual
        }
        if send_weekly_summary_email(cotacoes_para_resumo):
            st.success("✅ E-mail da cotação enviado com sucesso!")
        else:
            st.error("❌ Erro ao enviar o e-mail da cotação.")

else:
    st.error("Não foi possível carregar os dados. Verifique sua conexão ou a API.")