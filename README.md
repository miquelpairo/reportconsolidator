# NIR Maintenance Consolidator

Herramienta para consolidar informes de mantenimiento preventivo de espectrómetros NIR.

## ?? Características

- Consolidación de 3 tipos de informes:
  - **Baseline Adjustment**: Corrección de línea base tras cambio de lámpara
  - **Validación Óptica**: Verificación con standards certificados
  - **Predicciones**: Comparación de predicciones con muestras reales

- Generación de informe HTML único con:
  - Resumen ejecutivo
  - Estado global del mantenimiento
  - Navegación lateral indexada
  - Informes originales completos (con gráficos Plotly interactivos)
  - Estilo corporativo BUCHI

## ?? Instalación
```bash
pip install -r requirements.txt
```

## ?? Uso
```bash
streamlit run app.py
```

## ?? Requisitos

- Python 3.8+
- Streamlit
- BeautifulSoup4
- lxml

## ?? Desarrollado para

BUCHI Labortechnik AG - Equipos NIR

## ?? Licencia

Uso interno BUCHI