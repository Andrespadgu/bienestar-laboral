# Bienestar Laboral — Dashboard EDA

Dashboard interactivo de Análisis Exploratorio de Datos sobre bienestar laboral: agotamiento, liderazgo comprometido y señales organizacionales. Construido con **Streamlit** y **Plotly**.

🔗 **Demo en vivo:** *bienestar-laboral-ytucnmq8btmevkgytrxnit.streamlit.app*

---

## Hallazgos principales

Los hallazgos se calculan en tiempo real desde los datos; los números a continuación corresponden a la muestra total (N = 400).

| # | Hallazgo | Número clave |
|---|---|---|
| 1 | **El burnout no es el mayor problema** — Salud Mental organizacional (SM) encabeza el riesgo en el índice IRE | IRE 51.5 · puesto 1 de 16 |
| 2 | **1 de cada 4 trabajadores** supera el umbral de burnout moderado–alto | 24.5 % con BU > 3 |
| 3 | **Paradoja del directivo**: los jefes están más agotados que los operativos | 37.1 % vs 18.8 % con burnout moderado |
| 4 | **El liderazgo es el mayor escudo**: con liderazgo comprometido el burnout cae ~47 % | BU = 1.85 (CL alto) vs 2.72 (CL bajo) |
| 5 | **Satisfacción e intención de retiro** son la correlación más fuerte del estudio | ρ = −0.654 · p < 0.001 |
| 6 | **Casi 1 de cada 3** reporta somatización alta | 27.8 % con SOM > 4 |
| 7 | **1 de cada 5** tiene intención alta de retiro | 20.5 % con IR > 4.5 |
| 8 | **Paradoja del híbrido**: trabajadores en modalidad híbrida reportan 18 % más desgaste (n = 32, interpretar con cautela) | DL medio híbrido = 3.43 vs presencial = 2.90 |

---

## Estructura del proyecto

```
dashboard_eda_final/
├── app.py                          # Pantalla de inicio (Streamlit)
├── pages/
│   ├── 01_introduccion.py          # El mapa del riesgo (IRE · modelo JD-R)
│   ├── 02_panorama_general.py      # Perfil sociodemográfico
│   ├── 03_distribucion_variables.py# Distribuciones y umbrales críticos
│   ├── 04_relaciones.py            # Correlaciones Spearman
│   └── 05_hallazgos.py             # Evidencia → Acción (4 recomendaciones)
├── components/
│   ├── kpi_cards.py
│   └── sidebar.py
├── utils/
│   ├── data_loader.py              # Carga del CSV (UTF-8, sep=";")
│   ├── stats.py                    # Cálculos estadísticos centralizados
│   ├── charts.py                   # Gráficas Plotly reutilizables
│   ├── styles.py                   # CSS inyectado (tema oscuro editorial)
│   └── preprocessing.py
├── config/
│   └── settings.py                 # Definición de las 16 dimensiones y pares de correlación
├── data/
│   └── bienestar_laboral.csv       # Dataset anonimizado (N = 400, UTF-8)
├── notebooks/
│   └── eda_bienestar_laboral.ipynb # Análisis completo en Colab (74 celdas)
├── assets/
│   ├── images/                     # Capturas de pantalla para documentación
│   └── styles/
├── historia_bienestar.html         # Historia de datos (versión HTML standalone)
└── requirements.txt
```

---

## Cómo correr localmente

```bash
# 1. Clonar el repositorio
git clone https://github.com/Andrespadgu/bienestar-laboral.git
cd bienestar-laboral

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Lanzar la app
streamlit run app.py
```

La app abre en `http://localhost:8501`.

---

## Sobre los datos

`data/bienestar_laboral.csv` contiene respuestas de una encuesta aplicada a **400 trabajadores** del sector público y mixto en Colombia.

**Los datos son anónimos.** El archivo no contiene nombres, correos electrónicos, cédulas ni ningún otro identificador personal. Solo incluye:
- Un ID secuencial sin relación con la identidad real.
- Variables demográficas agregadas (sexo, rango de edad, tipo de cargo, sector, modalidad, nivel educativo, rango salarial).
- Puntuaciones en escalas psicosociales validadas (Likert 1–5 y 1–7).
- Los 16 promedios por dimensión ya calculados (`BU_prom`, `SAT_prom`, etc.).

---

## Dataset

| Característica | Valor |
|---|---|
| N | 400 trabajadores |
| Columnas | 128 (sociodemográficas + ítems de escala + promedios de dimensión) |
| Separador | `;` |
| Encoding | UTF-8 |
| Dimensiones psicosociales | 16 (escalas Likert 1–5 y 1–7) |

---

## Stack

- [Streamlit](https://streamlit.io) - interfaz interactiva
- [Plotly](https://plotly.com/python/) - visualizaciones
- [pandas](https://pandas.pydata.org) + [NumPy](https://numpy.org) - manipulación de datos
- [SciPy](https://scipy.org) - correlaciones Spearman y pruebas estadísticas

---

## Autor

Andrés Padilla · padillachl815@gmail.com
