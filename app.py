import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker

# Configuração para melhor visualização
plt.style.use('seaborn')
plt.rcParams['figure.figsize'] = (15, 7)
plt.rcParams['font.size'] = 12

# Função para formatar os valores com ponto como separador decimal
def format_func(value, tick_number):
    return f'{value:,.0f}'.replace(',', '.')

def plot_faturamento_realizado(df):
    fig, ax = plt.subplots(figsize=(15, 7))
    sns.barplot(x='Mês', y='Realizado', data=df[:-1], ax=ax)  # Excluindo a última linha (ACUMULADO)
    ax.set_title('Faturamento Realizado por Mês', fontsize=16)
    ax.set_xlabel('Mês')
    ax.set_ylabel('Faturamento Realizado (R$)')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_func))
    for i, v in enumerate(df['Realizado'][:-1]):
        ax.text(i, v, f'{v:,.0f}'.replace(',', '.'), ha='center', va='bottom')
    plt.tight_layout()
    return fig

def plot_faturamento_realizado_vs_orcado(df):
    fig, ax = plt.subplots(figsize=(15, 7))
    x = range(len(df['Mês'][:-1]))
    ax.plot(x, df['Realizado'][:-1], marker='o', label='Realizado')
    ax.plot(x, df['Orçado'][:-1], marker='s', label='Orçado')
    ax.set_title('Faturamento Realizado x Orçado por Mês', fontsize=16)
    ax.set_xlabel('Mês')
    ax.set_ylabel('Faturamento (R$)')
    ax.legend()
    ax.set_xticks(x)
    ax.set_xticklabels(df['Mês'][:-1], rotation=45)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_func))
    ax.grid(True, linestyle='--', alpha=0.7)

    for i, (r, o) in enumerate(zip(df['Realizado'][:-1], df['Orçado'][:-1])):
        ax.text(i, r * 1.02, f'{r:,.0f}'.replace(',', '.'), ha='center', va='bottom', fontsize=8)
        ax.text(i, o * 0.98, f'{o:,.0f}'.replace(',', '.'), ha='center', va='top', fontsize=8)

    plt.tight_layout()
    return fig

def plot_saldo_caixa(df):
    fig, ax = plt.subplots(figsize=(15, 7))

    # Converte os valores de saldo para milhões de R$
    df['Saldo (Milhões R$)'] = df['Saldo'] / 1e6

    # Cria o gráfico de barras
    bars = ax.bar(df['Mês'], df['Saldo (Milhões R$)'], color='#ADD8E6')

    # Adiciona linha lateral
    ax.grid(axis='y', color='#DCDCDC', linestyle='-')

    # Adiciona título e rótulos
    ax.set_title('Saldo de Caixa (2023)', fontsize=16)
    ax.set_xlabel('Mês')
    ax.set_ylabel('Saldo (Milhões R$)')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    # Adiciona os valores nas barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}',
                ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    return fig

def plot_nivel_estoques(df):
    fig, ax = plt.subplots(figsize=(15, 7))

    # Cria o gráfico de barras
    bars = ax.bar(df['Mês'], df['Estoque (R$)'], color='#90EE90')

    # Adiciona linha lateral
    ax.grid(axis='y', color='#DCDCDC', linestyle='-')

    # Adiciona título e rótulos
    ax.set_title('Nível de Estoques (2023)', fontsize=16)
    ax.set_xlabel('Mês')
    ax.set_ylabel('Estoque (R$)')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    # Adiciona os valores nas barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:,.0f}'.replace(',', '.'),
                ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    return fig

def calcular_metricas(df):
    media_realizado = df['Realizado'][:-1].mean()
    total_realizado = df['Realizado'][:-1].sum()
    variacao_total = df['Variação'][:-1].sum()
    percentual_variacao = (variacao_total / df['Orçado'][:-1].sum()) * 100

    return {
        "Média mensal de faturamento realizado": f"R$ {media_realizado:,.2f}".replace(',', '.'),
        "Total de faturamento realizado": f"R$ {total_realizado:,.2f}".replace(',', '.'),
        "Variação total (Realizado - Orçado)": f"R$ {variacao_total:,.2f}".replace(',', '.'),
        "Percentual de variação": f"{percentual_variacao:.2f}%".replace('.', ',')
    }

@st.cache_data
def load_faturamento_data():
    data = {
        'Mês': ['Jan 2023', 'Fev 2023', 'Mar 2023', 'Abr 2023', 'Mai 2023', 'Jun 2023',
                'Jul 2023', 'Ago 2023', 'Set 2023', 'Out 2023', 'Nov 2023', 'Dez 2023', 'ACUMULADO 2023'],
        'Orçado': [1871448.17, 1881305.31, 0.0, 2384933.31, 1892838.98, 2426768.57,
                   3365436.01, 2775783.80, 2939719.37, 4351472.10, 3158080.11, 3255719.92, 32451515.57],
        'Realizado': [2121320.90, 2612526.50, 1775687.17, 2631239.75, 2483240.08, 3061423.79,
                      2307138.54, 2429037.59, 2582752.71, 2157419.62, 2323382.35, 2699379.40, 29184548.40],
        'Variação': [249872.73, 731221.19, -372322.74, 246306.44, 590401.10, 634655.22,
                     -1058297.47, -346746.21, -356966.66, -2194052.48, -834697.76, -556340.52, -3266967.17],
        'Variação %': [13.4, 38.9, 0.0, 10.3, 31.2, 26.2,
                       -31.4, -12.5, -12.1, -50.4, -26.4, -17.1, -10.1]
    }
    return pd.DataFrame(data)

@st.cache_data
def load_saldo_caixa_data():
    data = {
        'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
        'Ano': [2023] * 12,
        'Saldo': [
            1330570.62, 934686.68, 962080.73, 1042521.56, 1727837.58,
            2018840.63, 1933067.98, 1116155.23, 1108564.22, 2225567.45,
            1624441.35, 1707548.49
        ]
    }
    return pd.DataFrame(data)

@st.cache_data
def load_nivel_estoques_data():
    data = {
        'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
        'Ano': [2023] * 12,
        'Estoque (R$)': [
            641877, 688367, 694277, 708432, 720714, 747526, 768522, 779630, 793544, 903170, 884213, 880647
        ]
    }
    return pd.DataFrame(data)

def main():
    st.title('Dashboard de Faturamento')

    df_faturamento = load_faturamento_data()
    df_saldo_caixa = load_saldo_caixa_data()
    df_nivel_estoques = load_nivel_estoques_data()

    # Gráfico de Faturamento Realizado
    st.subheader('Faturamento Realizado por Mês')
    fig1 = plot_faturamento_realizado(df_faturamento)
    st.pyplot(fig1)

    # Gráfico de Faturamento Realizado x Orçado
    st.subheader('Faturamento Realizado x Orçado por Mês')
    fig2 = plot_faturamento_realizado_vs_orcado(df_faturamento)
    st.pyplot(fig2)

    # Gráfico de Saldo de Caixa
    st.subheader('Saldo de Caixa')
    fig3 = plot_saldo_caixa(df_saldo_caixa)
    st.pyplot(fig3)

    # Gráfico de Nível de Estoques
    st.subheader('Nível de Estoques')
    fig4 = plot_nivel_estoques(df_nivel_estoques)
    st.pyplot(fig4)

    # Métricas
    st.subheader('Métricas de Faturamento')
    metricas = calcular_metricas(df_faturamento)
    for chave, valor in metricas.items():
        st.metric(label=chave, value=valor)

    # Dados brutos
    if st.checkbox('Mostrar dados brutos'):
        st.subheader('Dados de Faturamento')
        st.dataframe(df_faturamento)
        st.subheader('Dados de Saldo de Caixa')
        st.dataframe(df_saldo_caixa)
        st.subheader('Dados de Nível de Estoques')
        st.dataframe(df_nivel_estoques)

if __name__ == "__main__":
    main()