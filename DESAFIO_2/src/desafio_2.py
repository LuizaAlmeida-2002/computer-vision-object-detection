import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#caminho da base original
caminho='DESAFIO_2/dados/originais/imoveis_desafio.csv'
#Leitura da base de dados
df=pd.read_csv(caminho,encoding='utf-8-sig')
#Criando uma cópia para realizar os tratamentos
df_tratado=df.copy()
import re
#==============================
# FUNÇÃO PARA CONVERTER NÚMEROS
#==============================
def converter_numero(valor):
    if pd.isna(valor):
        return np.nan
    valor=str(valor).strip()
    if valor.upper() in ['N/D','DESCONHECIDO','']:
        return np.nan
    #Remove símbolos de moeda ee espaços
    valor=valor.replace('US$','').replace('$','').strip()
    #Identifica formatos com ponto e vírgula
    if ',' in valor and '.' in valor:
        #O último separador é considerado decimal
        if valor.rfind(',') > valor.rfind('.'):
            valor = valor.replace('.', '')
            valor = valor.replace(',', '.')
        else:
            valor=valor.replace(',','')
    elif ',' in valor:
        partes=valor.split(',')
        if len(partes[-1])==3 and len(partes)>1:
            valor=valor.replace(',','')
        else:
            valor=valor.replace(',','.')
    return pd.to_numeric(valor,errors='coerce')
#============================
# CONVERSÃO DAS ÁREAS PARA M²
#============================
def converter_area(valor):
    if pd.isna(valor):
        return np.nan
    texto = str(valor).strip().lower()
    # Identifica a unidade original
    em_pes_quadrados = "ft2" in texto
    # Remove a identificação da unidade
    texto = texto.replace("ft2", "").replace("m2", "").strip()
    # Converte o valor numérico
    numero = converter_numero(texto)
    if pd.isna(numero):
        return np.nan
    # Converte pés quadrados para metros quadrados
    if em_pes_quadrados:
        numero = numero * 0.09290304
    return round(numero, 2)
#=========================
# APLICAÇÃO DAS CONVERSÕES
#=========================
df_tratado['area_habitavel_m2']=(
    df_tratado['area_habitavel_m2'].apply(converter_area)
)
df_tratado['area_terreno_m2']=(
    df_tratado['area_terreno_m2'].apply(converter_area)
)
df_tratado['preco_venda_usd']=(
    df_tratado['preco_venda_usd'].apply(converter_numero)
)
df_tratado['vagas_garagem']=(
    df_tratado['vagas_garagem'].apply(converter_numero)
)
#==================================
# VERIFICAÇÃO DOS VALORES INVÁLIDOS
#==================================
print('\n===== VERIFICAÇÃO DOS VALORES INVÁLIDOS =====')
problemas=pd.DataFrame(index=df_tratado.index)
#Áreas e preço devem ser positivos
problemas['area_habitavel_invalida']=(
    df_tratado['area_habitavel_m2']<=0
)
problemas['area_terreo_invalida']=(
    df_tratado['area_terreno_m2']<=0
)
problemas['preco_invalido']=(
    df_tratado['preco_venda_usd']<=0
)
#Quantdades não pode ser negativas
problemas['quartos_invalidos']=(
    df_tratado['quartos']<0
)
problemas['banheiros_invalidos']=(
    df_tratado['banheiros_completos']<0
)
problemas['vagas_invalidas']=(
    df_tratado['vagas_garagem']<0
)
#A construção não pode ocorrer depois da venda
problemas['ano_invalido']=(
    df_tratado['ano_construcao']>
    df_tratado['ano_venda']
)
#Quantidade de problemas por coluna
print('\nQuantidade de valores inválidos por critério:')
print(problemas.sum())
#Identifica registros com pelo menos um problema
registros_invalidos=problemas.any(axis=1)
print(
    '\nQuantidade de registros com pelo menos um problema:',
    registros_invalidos.sum()
)
#Exibe exemplos para investigação
print('\nExemplos de registrs com problemas:')
colunas_exibicao=[
    'id_registro',
    'id_imovel',
    'area_habitavel_m2',
    'area_terreno_m2',
    'quartos',
    'banheiros_completos',
    'vagas_garagem',
    'ano_construcao',
    'ano_venda',
    'preco_venda_usd'
]
print(
    df_tratado.loc[
        registros_invalidos,
        colunas_exibicao
    ].head(20)
)
df_tratado['area_terreno_m2']=pd.to_numeric(
    df_tratado['area_terreno_m2'],
    errors='coerce'
)
#Substituindo N/D por valor ausente
df_tratado['vagas_garagem']=df_tratado['vagas_garagem'].replace(
    'N/D',np.nan    
)
#Convertendo vagas para formato numérico
df_tratado['vagas_garagem']=pd.to_numeric(
    df_tratado['vagas_garagem'],
    errors='coerce'
)
#Convertendo o preço de venda para formato numérico
df_tratado['preco_venda_usd']=pd.to_numeric(
    df_tratado['preco_venda_usd'],
    errors='coerce'
)
#====================================
# DETALHAMENTO DOS REGISTROS INÁLIDOS
#====================================
print('\n===== DETALHAMENTO DOS REGISTROS INVÁLIDOS =====')
for coluna in problemas.columns:
    registros=df_tratado.loc[
        problemas[coluna],
        [
            'id_registro',
            'id_imovel',
            'area_habitavel_m2',
            'quartos',
            'ano_venda',
            'preco_venda_usd'
        ]
    ]
    if len(registros)>0:
        print(f'\nProblema: {coluna}')
        print(registros.to_string(index=False))
print('\n===== VERIFICAÇÃO DE QUANTIDADES NÃO INTEIRAS =====')
for coluna in ['quartos','banheiros_completos','vagas_garagem']:
    valores=df_tratado[coluna].dropna()
    nao_inteiros=valores[valores%1 != 0]
    print(f'\nColuna: {coluna}')
    print(f'Quantidade de valores não inteiros: {len(nao_inteiros)}')
    print(nao_inteiros)
#=====================================
# INVESTIGAÇÃO DOS ANOS INCONSISTENTES
#=====================================
print('\n===== ANOS DE CONSTRUÇÃO INCONSISTENTES =====')
print(
    df_tratado.loc[
        problemas['ano_invalido'],
        [
            'id_registro',
            'id_imovel',
            'ano_construcao',
            'ano_venda',
            'preco_venda_usd'
        ]
    ].to_string(index=False)
)
#======================================
# INVESTIGAÇÃO DOS QUARTOS NÃO INTEIROS
#======================================
print('\n===== QUARTOS NÃO INTEIROS =====')
quartos_nao_inteiros=(
    df_tratado['quartos'].notna()
    & (df_tratado['quartos'] % 1 !=0)
)
print(
    df_tratado.loc[
        quartos_nao_inteiros,
        [
            'id_registro',
            'id_imovel',
            'quartos',
            'area_habitavel_m2',
            'preco_venda_usd'
        ]   
    ].to_string(index=False)
)
#================================
# APLICACAO DAS REGRAS DE LIMPEZA
#================================
print('\n===== APLICACAO DAS REGRAS DE LIMPEZA =====')
#Guarda a quantidade de valores ausentes antes da limpeza
ausentes_antes=df_tratado.isna().sum()
#Dicionário para registrar as alterações
registro_limpeza={}
#1. Area habitavel para registrar as alterações
registro_limpeza={}
#1. Área haitável deve ser positiva
mascara_area=df_tratado['area_habitavel_m2']<=0
registro_limpeza['area_habitavel_m2']=int(mascara_area.sum())
df_tratado.loc[
    mascara_area,
    'area_habitavel_m2'
] = np.nan
#2. Preço de venda deve ser positivo
mascara_preco=df_tratado['preco_venda_usd']<=0
registro_limpeza['preco_venda_usd']=int(mascara_preco.sum())
df_tratado.loc[
    mascara_preco,
    'preco_venda_usd'
]=np.nan
#3. Quartos não podem ser negativos
mascara_quartos_negativos=df_tratado['quartos']<0
registro_limpeza['quartos_negativos']=int(
    mascara_quartos_negativos.sum()
)
df_tratado.loc[
    mascara_quartos_negativos,
    'quartos'
]=np.nan
#4. Quartos devem ser numeros inteiros
mascara_quartos_fracionados=(
    df_tratado['quartos'].notna()
    & (df_tratado['quartos']%1!=0)
)
registro_limpeza['quartos_nao_inteiros']=int(
    mascara_quartos_fracionados.sum()
)
df_tratado.loc[
    mascara_quartos_fracionados,
    'quartos'
]=np.nan
#5. Ano de construção não pode ser posterior ao ano de venda
mascara_ano=(
    df_tratado['ano_construcao']>
    df_tratado['ano_venda']
)
registro_limpeza['ano_construcao_invalido']=int(
    mascara_ano.sum()
)
df_tratado.loc[
    mascara_ano,
    'ano_construcao'
]=np.nan
#6. Recalcula o preço por metro quadrado
#Esse campo e derivado do preço e da área habitável
df_tratado['preco_m2_usd']=(
    df_tratado['preco_venda_usd']/
    df_tratado['area_habitavel_m2']
)
# ==========================================
# ANALISE DOS PRECOS EXTREMAMENTE ELEVADOS
# ==========================================
print("\n===== ANALISE DOS PRECOS MUITO ELEVADOS =====")
precos_elevados = df_tratado[
    df_tratado["preco_venda_usd"] > 1_000_000
].sort_values(
    by="preco_venda_usd",
    ascending=False
)
print("Quantidade de preços acima de US$ 1 milhão:", len(precos_elevados))
print(
    precos_elevados[
        [
            "id_registro",
            "id_imovel",
            "area_habitavel_m2",
            "preco_venda_usd",
            "bairro",
            "ano_venda"
        ]
    ].to_string(index=False)
)
# ==========================================
# TRATAMENTO DOS PRECOS EXTREMAMENTE ELEVADOS
# ==========================================
print("\n===== TRATAMENTO DOS PRECOS SUSPEITOS =====")
mascara_preco_suspeito = df_tratado["preco_venda_usd"] > 1_000_000
quantidade_suspeitos = int(mascara_preco_suspeito.sum())
print("Preços suspeitos identificados:", quantidade_suspeitos)
# Preserva os registros, mas invalida o preço suspeito
df_tratado.loc[mascara_preco_suspeito, "preco_venda_usd"] = np.nan
# Recalcula o preço por metro quadrado
df_tratado["preco_m2_usd"] = (
    df_tratado["preco_venda_usd"] / df_tratado["area_habitavel_m2"]
)
print("Registros excluídos:", 0)
print("Preços suspeitos convertidos em ausentes:", quantidade_suspeitos)
#Exibe o registro das alterações
print('\nQuantidade de valores tratados:')
for coluna, quantidade in registro_limpeza.items():
    print(f'{coluna}: {quantidade}')
 #Compara valores ausentes antes e depois
ausentes_depois=df_tratado.isna().sum()
print('\nValores ausentes antes e depois da limpeza:')
comparacao_ausentes=pd.DataFrame({
     'Antes': ausentes_antes,
     'Depois':ausentes_depois
})
print(comparacao_ausentes)
print('\nQuantidade de linhas após a limpeza:')
print(len(df_tratado))
# ==========================================
# VERIFICACAO DE DUPLICATAS APOS A LIMPEZA
# ==========================================
print("\n===== DUPLICATAS APOS A LIMPEZA =====")
print(
    "Linhas completamente duplicadas:",
    df_tratado.duplicated().sum()
)
print(
    "IDs de registros repetidos:",
    df_tratado["id_registro"].duplicated().sum()
)
print(
    "IDs de imoveis repetidos:",
    df_tratado["id_imovel"].duplicated().sum()
)
# ==========================================
# REMOCAO DE DUPLICATAS COMPLETAS
# ==========================================
print("\n===== REMOCAO DE DUPLICATAS COMPLETAS =====")
linhas_antes = len(df_tratado)
df_tratado = df_tratado.drop_duplicates().copy()
duplicatas_removidas = linhas_antes - len(df_tratado)
print("Duplicatas completas removidas:", duplicatas_removidas)
print("Quantidade de linhas antes:", linhas_antes)
print("Quantidade de linhas depois:", len(df_tratado))
print(
    "Duplicatas completas restantes:",
    df_tratado.duplicated().sum()
)
print(
    "IDs de imóveis repetidos restantes:",
    df_tratado["id_imovel"].duplicated().sum()
)
#=========================================
# INVESTIGAÇÃO DOS VALORES NÃO CONVERTIDOS
#=========================================
print('\n===== VALORES DA ORIGEM QUE FICARAM AUSENTES APÓS O TRATAMENTO =====')
colunas_numericas=[
    'area_habitavel_m2',
    'area_terreno_m2',
    'vagas_garagem',
    'preco_venda_usd'
]
for coluna in colunas_numericas:
    #Identifica valores que eram preenchidos na base original, mas viraram ausentes após a conversão
    problema=df[coluna].notna() & df_tratado[coluna].isna()
    print(f'\nColuna: {coluna}')
    print('Quantidade de valores não convertidos',problema.sum())
    print('Exemplos encontrados:')
    print(df.loc[problema,coluna].head(20).to_list())
print('\n===== TIPOS DE DADOS APÓS A CONVERSÃO =====')
print(df_tratado.dtypes)
print('\n===== VALORES AUSENTES APÓS A CONVERSÃO =====')
print(df_tratado.isna().sum())
#Diagnóstico inicial
print('===== DIAGNÓSTICO INICIAL =====')
print('\nQuantidade de linhas e colunas:')
print(df.shape)
print('\nPrimeiras linhas da base:')
print(df.head())
print('\nInformações das colunas:')
print(df.info())
print('\nValores ausentes:')
print(df.isna().sum())
print('\nLinhas duplicadas:')
print(df.duplicated().sum())
print('\nEstatísticas das variáveis:')
print(df.describe(include='all'))
print('\n===== INVESTIGAÇÃO DOS VALORES =====')
colunas_texto=[
    'area_habitavel_m2',
    'area_terreno_m2',
    'vagas_garagem',
    'tipo_garagem',
    'bairro',
    'tipo_imovel',
    'preco_venda_usd',
]
for coluna in colunas_texto:
    print(f'\nValores diferentes encontrados em:{coluna}')
    print(df[coluna].value_counts(dropna=False).head(15))
print("\n===== VERIFICAÇÃO DOS IDENTIFICADORES =====")
print(
    "IDs de registros repetidos:",
    df["id_registro"].duplicated().sum()
)
print(
    "IDs de imóveis repetidos:",
    df["id_imovel"].duplicated().sum()
)
print("\n===== INVESTIGAÇÃO DOS REGISTROS REPETIDOS =====")
print("\nIDs de registros repetidos:")
print(df["id_registro"].duplicated().sum())
print("\nIDs de imóveis repetidos:")
print(df["id_imovel"].duplicated().sum())
print("\nImóveis que aparecem mais de uma vez:")
repetidos = df[df.duplicated(subset="id_imovel", keep=False)]
print(
    repetidos.sort_values("id_imovel")
    [["id_imovel", "id_registro", "ano_venda", "preco_venda_usd"]]
    .head(30)
)
print("\n===== INVESTIGAÇÃO DOS VALORES AUSENTES =====")
colunas_ausentes = [
    "area_habitavel_m2",
    "quartos",
    "bairro",
    "preco_venda_usd"
]
print(
    df[colunas_ausentes]
    .isna()
    .sum(axis=1)
    .value_counts()
    .sort_index()
)
print('\n===== ANÁLISE DE CONFLITOS POR IMÓVEL =====')
colunas_comparacao=[
    'ano_venda',
    'area_habitavel_m2',
    'area_terreno_m2',
    'quartos',
    'banheiros_completos',
    'vagas_garagem',
    'tipo_garagem',
    'bairro',
    'tipo_imovel',
    'preco_venda_usd'
]
#Considera apenas imóveis com ID repetido
imoveis_repetidos=df[
    df.duplicated(subset='id_imovel',keep=False)
]
#Conta quantos valores diferentes existem em cada coluna
analise_conflitos=(
    imoveis_repetidos
    .groupby('id_imovel')[colunas_comparacao]
    .nunique(dropna=False)
)
#Seleciona imóveis com pelo menos uma informação diferente
conflitos=analise_conflitos[
    (analise_conflitos>1).any(axis=1)
]
print('Quantidade dos imóveis com informações conflitantes:')
print(len(conflitos))
print('\nExemplos de conflitos:')
print(conflitos.head(15))
print('\nQuantidade de IDs repetidos sem conflitos:')
print(len(analise_conflitos)-len(conflitos))
# ==========================================
# EXPORTACAO DA BASE TRATADA
# ==========================================
import os
print("\n===== EXPORTACAO DA BASE TRATADA =====")
pasta_saida = "DESAFIO_2/dados/tratados"
os.makedirs(pasta_saida, exist_ok=True)
caminho_saida = os.path.join(
    pasta_saida,
    "imoveis_tratados.csv"
)
df_tratado.to_csv(
    caminho_saida,
    index=False,
    encoding="utf-8-sig"
)
print("Arquivo salvo em:", caminho_saida)
print("Quantidade de linhas:", len(df_tratado))
print("Quantidade de colunas:", len(df_tratado.columns))
print("Arquivo exportado com sucesso!")
# ==========================================
# GRAFICOS DA BASE TRATADA
# ==========================================
print("\n===== GERACAO DOS GRAFICOS =====")
pasta_graficos = "DESAFIO_2/resultados/graficos"
os.makedirs(pasta_graficos, exist_ok=True)
# Grafico 1: Distribuicao dos precos de venda
plt.figure(figsize=(10, 6))
sns.histplot(
    data=df_tratado,
    x="preco_venda_usd",
    bins=30,
    kde=True
)
plt.title("Distribuicao dos Precos de Venda dos Imoveis")
plt.xlabel("Preco de venda (USD)")
plt.ylabel("Quantidade de imoveis")
plt.tight_layout()
plt.savefig(
    os.path.join(pasta_graficos, "distribuicao_precos.png"),
    dpi=300
)
plt.close()
# Grafico 2: Area habitavel x preco de venda
dados_grafico = df_tratado.dropna(
    subset=["area_habitavel_m2", "preco_venda_usd"]
)
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=dados_grafico,
    x="area_habitavel_m2",
    y="preco_venda_usd",
    alpha=0.6
)
plt.title("Relacao entre Area Habitavel e Preco de Venda")
plt.xlabel("Area habitavel (m²)")
plt.ylabel("Preco de venda (USD)")
plt.tight_layout()
plt.savefig(
    os.path.join(pasta_graficos, "area_vs_preco.png"),
    dpi=300
)
plt.close()
print("Graficos salvos com sucesso!")
# ==========================================
# INVESTIGACAO DE VALORES EXTREMOS (OUTLIERS)
# ==========================================
print("\n===== INVESTIGACAO DE VALORES EXTREMOS =====")
colunas_outliers = ["preco_venda_usd", "area_habitavel_m2"]
resultados_outliers = []
mascaras_outliers = {}
for coluna in colunas_outliers:
    serie = df_tratado[coluna].dropna()
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    intervalo = q3 - q1
    limite_inferior = q1 - 1.5 * intervalo
    limite_superior = q3 + 1.5 * intervalo
    mascara = (
        (df_tratado[coluna] < limite_inferior)
        | (df_tratado[coluna] > limite_superior)
    )
    mascaras_outliers[coluna] = mascara
    resultados_outliers.append({
        "variavel": coluna,
        "q1": q1,
        "q3": q3,
        "limite_inferior": limite_inferior,
        "limite_superior": limite_superior,
        "quantidade_outliers": int(mascara.sum())
    })
    print(f"\nVariavel: {coluna}")
    print(f"Primeiro quartil (Q1): {q1:.2f}")
    print(f"Terceiro quartil (Q3): {q3:.2f}")
    print(f"Limite inferior: {limite_inferior:.2f}")
    print(f"Limite superior: {limite_superior:.2f}")
    print(f"Quantidade de valores extremos: {mascara.sum()}")
# Tabela-resumo
resumo_outliers = pd.DataFrame(resultados_outliers)
print("\n===== RESUMO DOS OUTLIERS =====")
print(resumo_outliers.to_string(index=False))
# Registros extremos em pelo menos uma das variaveis
mascara_geral = (
    mascaras_outliers["preco_venda_usd"]
    | mascaras_outliers["area_habitavel_m2"]
)
registros_outliers = df_tratado.loc[
    mascara_geral,
    [
        "id_registro",
        "id_imovel",
        "area_habitavel_m2",
        "preco_venda_usd",
        "bairro",
        "ano_venda"
    ]
].copy()
print("\n===== REGISTROS COM VALORES EXTREMOS =====")
print("Quantidade de registros:", len(registros_outliers))
print(registros_outliers.to_string(index=False))
# Grafico de boxplots
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
sns.boxplot(y=df_tratado["preco_venda_usd"])
plt.title("Valores extremos - Preco de venda")
plt.ylabel("Preco (USD)")
plt.subplot(1, 2, 2)
sns.boxplot(y=df_tratado["area_habitavel_m2"])
plt.title("Valores extremos - Area habitavel")
plt.ylabel("Area (m²)")
plt.tight_layout()
plt.savefig(
    os.path.join(pasta_graficos, "boxplots_outliers.png"),
    dpi=300
)
plt.close()
print("\nBoxplots salvos com sucesso!")
print("Nenhum registro foi excluido ou alterado nesta analise.")
