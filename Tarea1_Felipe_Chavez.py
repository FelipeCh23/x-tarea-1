# Tarea 1 Python en minería 
# Felipe Chávez Cuevas
# En este script se realiza un alaisis estadistico y una modelación 3D del modelo de bloques "data.txt"
#Parte 1 - Importación de librerias necesarias (Pandas, Numpy y Plotly)
import pandas as pd 
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# Configuración el renderizador para que los gráficos se abran en el navegador
pio.renderers.default = 'browser'


#Parte 2 - Carga y análisis descriptivo del modelo de bloques
df = pd.read_csv('data.txt', sep ='\t') # Se lee el archivo y se separa por tabulaciones
print(df.head())  
print(df.describe())


#Parte 3 - Visualización de la variable ley graficandose un histograma y boxplot en conjunto
Fig_histobox = px.histogram(
    df, #Desde donde se extraen los datos
    x = 'ley', # variable a graficar
    nbins = 50, #Numero de barras
    histnorm = 'percent', #Normaliza el eje Y para mostrar porcentajes
    marginal = 'box', #Grafico adicional Box
    title = 'Histrograma y boxplot de ley'
)
Fig_histobox.show()

# #Parte 4 - Se genera una columna ley2 con variables aleatorias y descripción estadistica igual a la columna 'ley'
# mu = 0.415 # Media dada por estadistica descriptiva del modelo
# sigma = 0.196 # Desviación estandar dada por estadistica descriptiva
# print('---'*40) 
# # Se generan muestras aleatorias para una distribución normal con media (mu) y desviación estandar (sigma)
# # len(df) asegura que se tenga un valor para cada bloque del DataFrame
# samples = np.random.normal(mu, sigma, len(df))  # Generar muestras con la media y desviación estándar

# # muestras generadas a la nueva columna 'ley2'
# df['ley2'] = samples

# # Se reemplaza cualquier valor negativo de 'ley2' por 0
# df.loc[df['ley2'] < 0, 'ley2'] = 0 # Se limpian datos reemplazando los menores a 0 de 'ley2' por 0

# # Se verifica el tipo de dato de ley2
# print("Tipo de dato de ley2:", df['ley2'].dtype)

# # Se verifican valores de ley2
# print(df['ley2'].describe())

# # Verificación con describe() que 'ley2' tenga rangos y dispersión similares a 'ley'.
# print(df.head())  # Ver las primeras filas para asegurarte de que 'ley2' se haya agregado correctamente
# print(df.describe())  # Ver la descripción estadística con la nueva columna 'ley2'


# # Parte 5 - Creación de una columna para cada variable de ley que valoriza cada bloque de acuerdo a la ecuación (1) dada
# # Definición de parametros ecónomicos y fisicos basado en supuestos
# densidad = 2.7  # g/cm³ o ton/m³
# precio_cu = 4.5  # USD/lb
# costo_ryv = 1  # USD/lb
# costo_mina = 18  # USD/ton
# costo_planta = 19  # USD/ton
# recuperacion = 0.85  # %
# constante = 2204.62  # lb/ton

# # Calculo de tonelaje (usando dimensiones del bloque)
# # Asumimos que cada bloque tiene el mismo tamaño en x, y, z
# # volumen = 10m x 10m x 10m = 1000 m³; tonelaje = volumen * densidad
# volumen = 1000  # m³
# ton = volumen * densidad  # Toneladas por bloque

# # Calculo de Valorización por Bloque según 'ley' y 'ley2'
# df['Vb_ley'] = ton * ((precio_cu - costo_ryv) * (df['ley'] / 100) * recuperacion * constante - (costo_mina + costo_planta))
# df['Vb_ley2'] = ton * ((precio_cu - costo_ryv) * (df['ley2'] / 100) * recuperacion * constante - (costo_mina + costo_planta))

# # Verificación de Vb_ley2
# print("Descripción estadística de Vb_ley2:")
# print(df['Vb_ley2'].describe())

# # Revición de algunas muestras para asegurar cálculo correcto
# print("Muestras de ley2 y su Vb correspondiente:")
# print(df[['ley2', 'Vb_ley2']].sample(5))


# # Parte 6 - Creación de columnas 'status' para cada valor de bloque donde: bloques positivos ==1 y bloques negativos o cero == 0.
# #Para 'ley' se evalua si el valor económico ('Vb_ley') es mayor que 0 
# # asignamos 1 (rentable); si no, 0 (no rentable o neutro). Lo mismo para 'ley2'
# df['status_ley'] = np.where(df['Vb_ley'] > 0, 1, 0)
# df['status_ley2'] = np.where(df['Vb_ley2'] > 0, 1, 0)

# #Verificación de resultados:  cantidad de bloques positivos y negativos indicando el número de bloques viables 
# # Con esto se pudo interpretar con anterioridad que se va por buen camino
# print(df['status_ley'].value_counts()) # Conteo de 1s y 0s para Vb_ley (lo mismo en la siguiente linea)
# print(df['status_ley2'].value_counts())

# # Parte 7 – Grafica en 3D de las dos envolventes de ley de acuerdo a su columna status == 1

# # Envolvente para ley original
# # Filtro los bloques con status_ley == 1
# # Solo filtramos los bloques con status == 1 (valor económico positivo) 
# # Se representará así el volumen de material que es rentable extraer.
# rentables_ley  = df[df['status_ley']  == 1]   # Bloques rentables según la ley 

# # Creación de gráfico 3D
# fig = go.Figure() # Crea figura 3D con plotly
# # Se agrega puntos 3D con coordenadas x,y,z
# fig.add_trace(go.Scatter3d(
#     x=rentables_ley['x'],
#     y=rentables_ley['y'],
#     z=rentables_ley['z'],
#     mode='markers', # Modo de visualización por puntos
#     marker=dict(
#         size=5, # Tamaño de los puntos
#         color=rentables_ley['ley'], #Color de puntos según ley
#         colorscale='plasma', # Escala de colores
#         colorbar=dict(title='Ley [%]'), # Barra de color con titulo
#         opacity=0.8 # Opacidad para mejor visualización
#     )
# ))

# fig.update_layout(
#     title='Envolvente 3D – Ley (status_ley == 1)',
#     scene=dict(
#         xaxis_title='x',
#         yaxis_title='y',
#         zaxis_title='z',
#         bgcolor='white'
#     )
# )

# fig.show()

# #status ==1 ley2
# # Filtración de los bloques con status_ley2 == 1

# rentables_ley2 = df[df['status_ley2'] == 1]   # Bloques rentables según la ley2 simulada

# # Creación de gráfico 3D para ley2

# fig2 = go.Figure()

# fig2.add_trace(go.Scatter3d(
#     x=rentables_ley2['x'],
#     y=rentables_ley2['y'],
#     z=rentables_ley2['z'],
#     mode='markers',
#     marker=dict(
#         size=5,
#         color=rentables_ley2['ley2'],
#         colorscale='Plasma',
#         colorbar=dict(title='Ley2 [%]'),
#         opacity=0.8
#     )
# ))

# fig2.update_layout(
#     title='Envolvente 3D – Ley 2 simulada(status_ley2 == 1)',
#     scene=dict(
#         xaxis_title='x',
#         yaxis_title='y',
#         zaxis_title='z',
#         bgcolor='white'
#     )
# )

# fig2.show()