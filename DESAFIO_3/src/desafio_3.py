from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# Localização das pastas
PASTA_PROJETO = Path(__file__).resolve().parents[2]
CAMINHO_BASE = (
    PASTA_PROJETO
    / "DESAFIO_2"
    / "dados"
    / "tratados"
    / "imoveis_tratados.csv"
)
# Verifica se o arquivo existe
if not CAMINHO_BASE.exists():
    raise FileNotFoundError(
        f"Arquivo não encontrado: {CAMINHO_BASE}"
    )
# Carrega a base tratada do Desafio 2
df = pd.read_csv(CAMINHO_BASE)
print("===== CONFERÊNCIA DA BASE =====")
print("\nDimensões:")
print(df.shape)
print("\nColunas:")
print(df.columns.tolist())
print("\nTipos de dados:")
print(df.dtypes)
print("\nValores ausentes:")
print(df.isnull().sum())
print("\nQuantidade de IDs de imóveis:")
print(df["id_imovel"].nunique())
print("\nRegistros com preço de venda ausente:")
print(df["preco_venda_usd"].isnull().sum())
print("\nPrimeiras linhas:")
print(df.head())
from sklearn.model_selection import GroupShuffleSplit
# Variável alvo
ALVO = "preco_venda_usd"
# Remove apenas registros sem preço de venda
# Não é possível treinar um modelo sem conhecer o valor real
df_modelo = df.dropna(subset=[ALVO]).copy()
# Primeira divisão: 70% treino e 30% restante
separador_1 = GroupShuffleSplit(
    n_splits=1,
    test_size=0.30,
    random_state=42
)
indices_treino, indices_restantes = next(
    separador_1.split(
        df_modelo,
        groups=df_modelo["id_imovel"]
    )
)
df_treino = df_modelo.iloc[indices_treino].copy()
df_restante = df_modelo.iloc[indices_restantes].copy()
# Segunda divisão: metade validação e metade teste
separador_2 = GroupShuffleSplit(
    n_splits=1,
    test_size=0.50,
    random_state=42
)
indices_validacao, indices_teste = next(
    separador_2.split(
        df_restante,
        groups=df_restante["id_imovel"]
    )
)
df_validacao = df_restante.iloc[indices_validacao].copy()
df_teste = df_restante.iloc[indices_teste].copy()
# Verificação de grupos compartilhados
ids_treino = set(df_treino["id_imovel"])
ids_validacao = set(df_validacao["id_imovel"])
ids_teste = set(df_teste["id_imovel"])
print("\n===== DIVISÃO DOS CONJUNTOS =====")
print(f"Registros disponíveis para modelagem: {len(df_modelo)}")
print(f"Registros sem preço excluídos da modelagem: {df['preco_venda_usd'].isna().sum()}")
print(f"\nTreino: {len(df_treino)} registros ({len(df_treino) / len(df_modelo) * 100:.2f}%)")
print(f"Validação: {len(df_validacao)} registros ({len(df_validacao) / len(df_modelo) * 100:.2f}%)")
print(f"Teste: {len(df_teste)} registros ({len(df_teste) / len(df_modelo) * 100:.2f}%)")
print("\n===== VERIFICAÇÃO DE VAZAMENTO ENTRE GRUPOS =====")
print("IDs compartilhados entre treino e validação:", len(ids_treino & ids_validacao))
print("IDs compartilhados entre treino e teste:", len(ids_treino & ids_teste))
print("IDs compartilhados entre validação e teste:", len(ids_validacao & ids_teste))
print("\n===== VERIFICAÇÃO DA VARIÁVEL ALVO =====")
print("Preços ausentes no treino:", df_treino[ALVO].isna().sum())
print("Preços ausentes na validação:", df_validacao[ALVO].isna().sum())
print("Preços ausentes no teste:", df_teste[ALVO].isna().sum())
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
# Variáveis numéricas
variaveis_numericas = [
    "area_habitavel_m2",
    "area_terreno_m2",
    "quartos",
    "banheiros_completos",
    "vagas_garagem",
    "ano_construcao",
    "ano_venda"
]
# Variáveis categóricas
variaveis_categoricas = [
    "tipo_garagem",
    "bairro",
    "tipo_imovel"
]
# Características utilizadas como entrada
CARACTERISTICAS = variaveis_numericas + variaveis_categoricas
# Preparação das variáveis numéricas
pipeline_numerica = Pipeline(steps=[
    ("imputacao", SimpleImputer(strategy="median")),
    ("padronizacao", StandardScaler())
])
# Preparação das variáveis categóricas
pipeline_categorica = Pipeline(steps=[
    ("imputacao", SimpleImputer(strategy="most_frequent")),
    ("codificacao", OneHotEncoder(handle_unknown="ignore"))
])
# Combinação dos dois tipos de variáveis
preprocessador = ColumnTransformer(transformers=[
    ("numericas", pipeline_numerica, variaveis_numericas),
    ("categoricas", pipeline_categorica, variaveis_categoricas)
])
print("\n===== PREPARAÇÃO DAS CARACTERÍSTICAS =====")
print("Variáveis numéricas:", variaveis_numericas)
print("Quantidade:", len(variaveis_numericas))
print("\nVariáveis categóricas:", variaveis_categoricas)
print("Quantidade:", len(variaveis_categoricas))
print("\nTotal de características originais:", len(CARACTERISTICAS))
print("\nVariável alvo:", ALVO)
print("Identificadores excluídos das entradas: id_registro e id_imovel")
print("Variável excluída por vazamento: preco_m2_usd")
# Separação das características (X) e variável alvo (y)
X_treino = df_treino[CARACTERISTICAS]
y_treino = df_treino[ALVO]
X_validacao = df_validacao[CARACTERISTICAS]
y_validacao = df_validacao[ALVO]
X_teste = df_teste[CARACTERISTICAS]
y_teste = df_teste[ALVO]
# Modelo 1: referência pela média
modelo_referencia = DummyRegressor(strategy="mean")
modelo_referencia.fit(X_treino, y_treino)
# Modelo 2: regressão linear com pré-processamento
modelo_linear = Pipeline(steps=[
    ("preprocessamento", preprocessador),
    ("regressao", LinearRegression())
])
modelo_linear.fit(X_treino, y_treino)
print("\n===== TREINAMENTO DOS MODELOS =====")
print("Modelo de referência pela média: treinado.")
print("Modelo de regressão linear: treinado.")
# Gerar previsões para cada conjunto
previsoes = {
    "Referência pela média": {
        "Treino": modelo_referencia.predict(X_treino),
        "Validação": modelo_referencia.predict(X_validacao),
        "Teste": modelo_referencia.predict(X_teste)
    },
    "Regressão linear": {
        "Treino": modelo_linear.predict(X_treino),
        "Validação": modelo_linear.predict(X_validacao),
        "Teste": modelo_linear.predict(X_teste)
    }
}
# Valores reais de cada conjunto
valores_reais = {
    "Treino": y_treino,
    "Validação": y_validacao,
    "Teste": y_teste
}
# Calcular métricas
resultados_metricas = []
for nome_modelo, conjuntos in previsoes.items():
    for nome_conjunto, valores_previstos in conjuntos.items():
        reais = valores_reais[nome_conjunto]
        mae = mean_absolute_error(reais, valores_previstos)
        rmse = np.sqrt(mean_squared_error(reais, valores_previstos))
        r2 = r2_score(reais, valores_previstos)
        quantidade = len(reais)
        resultados_metricas.append({
            "Modelo": nome_modelo,
            "Conjunto": nome_conjunto,
            "Nº de registros": quantidade,
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2
        })
# Organizar e apresentar os resultados
df_metricas = pd.DataFrame(resultados_metricas)
print("\n===== AVALIAÇÃO DOS MODELOS =====")
print(df_metricas.to_string(index=False, formatters={
    "MAE": "{:,.2f}".format,
    "RMSE": "{:,.2f}".format,
    "R2": "{:.4f}".format
}))
# Criar pastas de resultados
PASTA_RESULTADOS = PASTA_PROJETO / "DESAFIO_3" / "resultados"
PASTA_GRAFICOS = PASTA_RESULTADOS / "graficos"
PASTA_PREVISOES = PASTA_RESULTADOS / "previsoes"
PASTA_METRICAS = PASTA_PROJETO / "DESAFIO_3" / "metricas"
PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)
PASTA_PREVISOES.mkdir(parents=True, exist_ok=True)
PASTA_METRICAS.mkdir(parents=True, exist_ok=True)
# Salvar tabela de métricas
caminho_metricas = PASTA_METRICAS / "metricas_modelos.csv"
df_metricas.to_csv(
    caminho_metricas,
    index=False,
    encoding="utf-8-sig"
)
print("\n===== ARQUIVOS SALVOS =====")
print(f"Métricas: {caminho_metricas}")
# Gráfico de valores reais versus previstos no teste
plt.figure(figsize=(8, 6))
plt.scatter(
    y_teste,
    previsoes["Regressão linear"]["Teste"],
    alpha=0.6
)
limite_minimo = min(
    y_teste.min(),
    previsoes["Regressão linear"]["Teste"].min()
)
limite_maximo = max(
    y_teste.max(),
    previsoes["Regressão linear"]["Teste"].max()
)
plt.plot(
    [limite_minimo, limite_maximo],
    [limite_minimo, limite_maximo],
    linestyle="--"
)
plt.xlabel("Preço real (USD)")
plt.ylabel("Preço previsto (USD)")
plt.title("Preços reais versus previstos - Teste")
plt.tight_layout()
caminho_grafico = PASTA_GRAFICOS / "valores_reais_vs_previstos.png"
plt.savefig(caminho_grafico, dpi=300)
plt.close()
print(f"Gráfico salvo: {caminho_grafico}")
# Calcular resíduos do conjunto de teste
residuos = (
    y_teste.values -
    previsoes["Regressão linear"]["Teste"]
)
# Gráfico de resíduos
plt.figure(figsize=(8, 6))
plt.scatter(
    previsoes["Regressão linear"]["Teste"],
    residuos,
    alpha=0.6
)
plt.axhline(y=0, linestyle="--")
plt.xlabel("Preço previsto (USD)")
plt.ylabel("Resíduo (USD)")
plt.title("Gráfico de resíduos - Teste")
plt.tight_layout()
caminho_grafico = PASTA_GRAFICOS / "residuos_teste.png"
plt.savefig(caminho_grafico, dpi=300)
plt.close()
print(f"Gráfico salvo: {caminho_grafico}")
# Organizar previsões do conjunto de teste
df_previsoes_teste = pd.DataFrame({
    "id_registro": df_teste["id_registro"].values,
    "id_imovel": df_teste["id_imovel"].values,
    "preco_real_usd": y_teste.values,
    "preco_previsto_usd": previsoes["Regressão linear"]["Teste"],
    "residuo_usd": residuos
})
caminho_previsoes = PASTA_PREVISOES / "previsoes_teste.csv"
df_previsoes_teste.to_csv(
    caminho_previsoes,
    index=False,
    encoding="utf-8-sig"
)
print(f"Previsões salvas: {caminho_previsoes}")
print("\nPrimeiras previsões:")
print(df_previsoes_teste.head())






