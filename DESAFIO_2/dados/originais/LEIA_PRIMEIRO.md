# Base fornecida para o teste de IA e programação

Este material complementa os desafios 2 e 3 do teste técnico. **Utilize o arquivo `imoveis_desafio.csv` em vez de escolher outra base pública.** Os demais requisitos permanecem válidos, incluindo treino, validação e teste, regressão linear, métricas e documentação.

O prazo continua sendo **3 dias corridos (72 horas) após o envio do e-mail do teste**. Entregas parciais são aceitas e serão avaliadas pelo conteúdo enviado. A entrega destes anexos junto ao teste não cria um segundo prazo.

## Contexto

A base parte de registros públicos de vendas de imóveis de Ames, Iowa, Estados Unidos, disponibilizados como Ames Housing. Foi preparada uma versão didática com 2.990 linhas e 14 colunas, incluindo inconsistências deliberadas para avaliar limpeza, diagnóstico e modelagem. Nem toda diferença ou valor incomum representa erro.

O objetivo é prever `preco_venda_usd`. Todos os preços são em **dólares americanos (USD)**, sem atualização monetária. As áreas têm como unidade esperada o **metro quadrado**. Os registros históricos não representam o mercado imobiliário brasileiro nem preços atuais.

## Como ler

- Arquivo CSV com separador **vírgula**, campos textuais entre aspas quando necessário e codificação **UTF-8 com BOM**.
- A primeira linha contém os nomes das colunas. Há 2.990 linhas de dados, além do cabeçalho.
- Recomenda-se começar lendo os campos como texto para inspecionar as representações originais. A leitura direta com inferência de tipos também é aceita, desde que suas consequências sejam compreendidas.
- Não altere o arquivo recebido: grave a versão tratada em outro caminho.
- Consulte `DICIONARIO.md` para entender significado, unidade e disponibilidade dos campos.

## Escopo do exercício

Diagnostique inconsistências, documente as regras adotadas e apresente as quantidades de linhas afetadas. Há informações suficientes para realizar os desafios sem buscar outra base, contratar serviços ou obter credenciais.

Não é necessário recuperar exatamente os valores anteriores às alterações. Quando um valor não puder ser inferido com segurança, documente a decisão de invalidá-lo, imputá-lo ou excluir o registro, conforme a natureza do campo. Não use a base pública original para substituir automaticamente os dados recebidos nem para reconstruir valores ausentes: a habilidade avaliada é o tratamento da base fornecida.

A modelagem deve usar características disponíveis antes de conhecer o preço final da venda. Justifique a seleção das variáveis e previna vazamento de informação tanto entre colunas quanto entre os conjuntos de treino, validação e teste.

Mantenha valores incomuns quando houver justificativa. Não existe uma quantidade única obrigatória de linhas após a limpeza nem uma métrica mínima para aprovação. Serão avaliadas a coerência, a execução e a explicação das escolhas.

## Arquivos deste pacote

- `imoveis_desafio.csv`: entrada dos desafios de limpeza e regressão.
- `DICIONARIO.md`: significado e unidades dos campos.
- `FONTES_E_ATRIBUICAO.md`: procedência e adaptações.
- `LEIA_PRIMEIRO.md`: estas instruções.

Siga os entregáveis e o formato de envio descritos no teste principal.
