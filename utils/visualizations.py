import plotly.express as px
import pandas as pd


def histogram(df: pd.DataFrame, col: str, title: str = ""):
    return px.histogram(df, x=col, title=title or f"Distribucion de {col}", template="plotly_white")


def boxplot(df: pd.DataFrame, col: str, title: str = ""):
    return px.box(df, y=col, title=title or f"Boxplot de {col}", template="plotly_white")


def correlation_heatmap(df: pd.DataFrame):
    corr = df.select_dtypes("number").corr()
    return px.imshow(corr, text_auto=True, title="Mapa de correlacion", template="plotly_white")


def scatter(df: pd.DataFrame, x: str, y: str, color: str = None):
    return px.scatter(df, x=x, y=y, color=color, template="plotly_white")
