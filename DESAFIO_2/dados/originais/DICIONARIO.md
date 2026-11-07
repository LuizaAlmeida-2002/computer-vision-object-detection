# Dicionário de dados

Os tipos abaixo são os **tipos esperados após o tratamento**. O arquivo de entrada pode conter representações diferentes. A variável alvo é `preco_venda_usd`.

| Coluna | Tipo esperado | Significado / regra de interpretação | Origem |
| --- | --- | --- | --- |
| id_registro | Texto | Identificador didático de uma linha importada. Não é uma característica física do imóvel. | Gerado no exercício. |
| id_imovel | Texto | Identificador didático da observação da fonte. Cópias da mesma observação mantêm este identificador. Não é um cadastro imobiliário oficial. | Gerado a partir de `rownames`. |
| area_habitavel_m2 | Número real positivo | Área habitável acima do solo, em m². Não inclui o porão. | `Gr_Liv_Area`, convertido de ft². |
| area_terreno_m2 | Número real positivo | Área total do terreno, em m². | `Lot_Area`, convertido de ft². |
| quartos | Inteiro não negativo | Quartos acima do solo; não inclui quartos no porão. Zero existe na fonte e requer interpretação, não exclusão automática. | `Bedroom_AbvGr`. |
| banheiros_completos | Inteiro não negativo | Banheiros completos acima do solo. Não soma lavabos ou banheiros no porão. Zero é possível. | `Full_Bath`. |
| vagas_garagem | Inteiro não negativo | Capacidade da garagem em veículos. Zero pode significar ausência de garagem. | `Garage_Cars`. |
| tipo_garagem | Categoria | `Attchd`: anexa; `Detchd`: separada; `BuiltIn`: integrada à construção; `Basment`: no porão; `CarPort`: cobertura para veículos; `More_Than_Two_Types`: rótulo de categoria herdado da versão modeldata; `No_Garage`: sem garagem. | `Garage_Type`. |
| ano_construcao | Inteiro | Ano de construção original. Deve ser compatível com o ano de venda. | `Year_Built`. |
| ano_venda | Inteiro | Ano da venda registrada. Contexto temporal do histórico. | `Year_Sold`. |
| bairro | Categoria | Nome/código do bairro na versão modeldata, mantido em inglês. | `Neighborhood`. |
| tipo_imovel | Categoria | `OneFam`: residência unifamiliar; `TwoFmCon`: conversão para duas famílias; `Duplex`: duplex; `Twnhs`: casa geminada interna; `TwnhsE`: casa geminada de extremidade. | `Bldg_Type`. |
| preco_venda_usd | Número real positivo | Preço final da venda, em USD. É a variável alvo; não disponível antes da venda. | `Sale_Price`. |
| preco_m2_usd | Número real positivo, quando válido | Campo de relatório calculado depois da venda, dividindo o preço final pela área habitável em m². Pode ficar desatualizado quando outros campos são alterados. | Derivado para o exercício. |

## Convenções

- Conversão de área: **1 ft² = 0,09290304 m²**. A referência usa duas casas decimais.
- O CSV usa, em geral, ponto decimal, mas o processo de importação didático admite formatos brasileiros e norte-americanos. Identifique o padrão antes de converter separadores.
- Um sufixo explícito `ft2` informa uma área em pés quadrados; um sufixo `m2` informa metros quadrados.
- O símbolo `US$` continua indicando USD; não há conversão de câmbio no exercício.
- Texto vazio e marcadores de indisponibilidade devem ser interpretados conforme seu contexto. **`No_Garage` é uma categoria válida**, não um marcador genérico de ausência de informação.
- O identificador da linha não contém prioridade, qualidade ou data de atualização. Não há coluna que permita determinar qual importação conflitante é a mais recente.
- As linhas recebidas podem conter cópias da mesma observação. A numeração `AMES-...` não permite provar que duas observações diferentes da fonte representam propriedades físicas distintas em vendas repetidas.
