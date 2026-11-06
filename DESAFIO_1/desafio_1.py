# Importando as bibliotecas
import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO
import numpy as np
import pandas as pd
import os
# Carregando a imagem original
imagem = cv2.imread('desafio_1/imagens/imagem_original.png')
# Verificando se a imagem foi carregada
if imagem is None:
    print('Erro: não foi possível carregar a imagem.')
    raise SystemExit
# Obtendo as dimensões da imagem
altura, largura, canais = imagem.shape
print('Imagem carregada com sucesso!')
print('Largura:', largura, 'pixels')
print('Altura:', altura, 'pixels')
print('Canais de cor:', canais)
# Convertendo a imagem original de BGR para RGB
imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
print('Imagem original carregada antes do YOLO.')
# Importando e carregando o modelo YOLO
modelo = YOLO('yolo11s-seg.pt')
# Fazendo a identificação dos objetos
resultados = modelo.predict(
    source='desafio_1/imagens/imagem_original.png',
    conf=0.10,
    imgsz=960,
    retina_masks=True
)
# Pegando o resultado da análise
resultado = resultados[0]
# Extraindo os contornos dos objetos
dados_objetos = []
# Criando uma cópia da imagem original
imagem_contornos = imagem.copy()
# Verificando se existem máscaras
if resultado.masks is not None:
    # Percorrendo as máscaras dos objetos
    for i, mascara in enumerate(resultado.masks.data):
        # Identificando a categoria do objeto
        classe = int(resultado.boxes.cls[i])
        nome = resultado.names[classe]
        # Ignorando a mesa
        if nome == 'dining table':
            continue
        # Convertendo a máscara para um array NumPy
        mascara = mascara.cpu().numpy()
        # Redimensionando a máscara para o tamanho original
        mascara = cv2.resize(
            mascara,
            (largura, altura),
            interpolation=cv2.INTER_NEAREST
        )
        # Transformando a máscara em imagem binária
        mascara_binaria = (mascara > 0.5).astype('uint8') * 255
        # Encontrando os contornos externos
        contornos, hierarquia = cv2.findContours(
            mascara_binaria,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        # Verificando se algum contorno foi encontrado
        if len(contornos) == 0:
            continue
        # Selecionando o maior contorno
        contorno = max(contornos, key=cv2.contourArea)
        # Calculando a área
        area = cv2.contourArea(contorno)
        #Ignorando contornos muito pequenos
        if area<100:
            continue
        # Calculando o centro do objeto
        momentos = cv2.moments(contorno)
        if momentos['m00'] != 0:
            centro_x = int(momentos['m10'] / momentos['m00'])
            centro_y = int(momentos['m01'] / momentos['m00'])
        else:
            centro_x = 0
            centro_y = 0
        # Guardando os dados do objeto
        dados_objetos.append({
            "id": len(dados_objetos) + 1,
            "categoria": nome,
            "area_contorno": area,
            "centro_x": centro_x,
            "centro_y": centro_y
        })
        # Desenhando o contorno na imagem
        cv2.drawContours(
            imagem_contornos,
            [contorno],
            -1,
            (0, 255, 0),
            2
        )
        #Escrevendo o nome da categoria próximo ao contorno
        cv2.putText(
            imagem_contornos,
            nome,
            (centro_x,centro_y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,0,255),
            2
        )
#Organizando os dados em uma tabela
tabela=pd.DataFrame(dados_objetos)
print('\nDados dos objetos:')
print(tabela)
#Criando a pasta dos resultados,caso não exista
os.makedirs('desafio_1/resultados',exist_ok=True)
#Salvando o CSV
tabela.to_csv(
    'desafio_1/resultados/objetos_identificados.csv',
    index=False
)
#Salvando a imagem com os contornos
cv2.imwrite(
    'desafio_1/resultados/imagem_contornos.png',
    imagem_contornos
)
print('\nCSV e imagem com contornos salvos com sucesso!')
# Verificando a quantidade de máscaras
if resultado.masks is not None:
    print('\nQuantidade de máscaras:', len(resultado.masks.data))
else:
    print('\nNenhuma máscara foi encontrada.')
# Exibindo os objetos identificados
print('\nObjetos identificados:')
for classe in resultado.boxes.cls:
    nome = resultado.names[int(classe)]
    print('-', nome)
# Criando a imagem com as marcações do YOLO
imagem_yolo = resultado.plot()
# Convertendo a imagem do YOLO de BGR para RGB
imagem_yolo_rgb = cv2.cvtColor(
    imagem_yolo,
    cv2.COLOR_BGR2RGB
)
print('Imagem original:',imagem_rgb.shape)
print('Imagem YOLO:',imagem_yolo_rgb.shape)
# Exibindo as duas imagens
plt.figure(figsize=(12, 6))
# Primeira imagem: original
plt.subplot(1, 2, 1)
plt.imshow(imagem_rgb)
plt.title('Imagem original')
plt.axis('off')
# Segunda imagem: resultado do YOLO
plt.subplot(1, 2, 2)
plt.imshow(imagem_yolo_rgb)
plt.title('Objetos identificados')
plt.axis('off')
plt.tight_layout()
plt.show()




