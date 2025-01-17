import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuração do Streamlit
st.set_page_config(page_title="Relatório Diário", layout="centered")

# Criação das páginas
menu = ["Introdução", "Registro de Vacinas"]
opcao = st.sidebar.selectbox("Navegar", menu)

if opcao == "Introdução":
    st.title("Relatório Diário")
    st.markdown(""" 
    ### Descrição do Projeto
    A ideia surgiu quando minha esposa fez uma analogia ao falar comigo no telefone, dizendo: "Lucas, eu queria mesmo é que você fizesse outra de mim", justamente por conta das diversas atividades praticadas no dia a dia. Por conta disso, resolvi ajudar em uma das tarefas que a outra "Tatiane" iria fazer.

    O projeto consiste na automação de uma tarefa simples, onde minha esposa, que atua como técnica de enfermagem em uma clínica, precisa enviar um relatório diário pra enfermeira mostrando quantas vacinas foram aplicadas no dia anterior. Isso tudo pra manter o estoque sempre em dias e não prejudicar os clientes e o faturamento da empresa.
    """)

elif opcao == "Registro de Vacinas":
    st.title("Registro de Vacinas")

    # Lista de vacinas
    vacinas = [
        "BCG",
        "Hepatite B",
        "Pentavalente",
        "Pneumocócica 10-valente",
        "Rotavírus",
        "Meningocócica C",
        "Febre Amarela",
        "Tríplice Viral",
        "Varicela",
        "COVID-19"
    ]

    st.markdown("Informe abaixo a quantidade de cada vacina administrada no dia:")

    # Entrada de dados para cada vacina
    dados = {}
    for vacina in vacinas:
        quantidade = st.number_input(f"{vacina}", min_value=0, step=1, value=0)
        dados[vacina] = quantidade

    if st.button("Salvar e Enviar"):
        # Salvar dados em um arquivo CSV
        df = pd.DataFrame(list(dados.items()), columns=["Vacina", "Quantidade"])
        arquivo_csv = "relatorio_vacinas.csv"
        df.to_csv(arquivo_csv, index=False)
        st.success("Dados salvos com sucesso!")

        # Preparar mensagem com vacinas e quantidades formatadas
        relatorio = "\n".join(
            [f"{row['Vacina']:<30} {row['Quantidade']}" for _, row in df.iterrows()]
        )

        destinatario = "edson.pessoa.atento@gmail.com"
        assunto = "Relatório diário"
        mensagem = f"""
Prezado gestor,

Segue o relatório do dia anterior referente às vacinas:

{"Vacina":<30} Quantidade
{'-' * 40}
{relatorio}

Qualquer dúvida, estou à disposição!

Atte.
"""

        # Envio do e-mail
        try:
            email_usuario = st.secrets["email_usuario"]
            email_senha = st.secrets["email_senha"]

            msg = MIMEMultipart()
            msg["From"] = email_usuario
            msg["To"] = destinatario
            msg["Subject"] = assunto
            msg.attach(MIMEText(mensagem, "plain"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(email_usuario, email_senha)
                server.send_message(msg)

            st.success("E-mail enviado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao enviar o e-mail: {e}")

        st.write("Dados enviados:")
        st.dataframe(df)
