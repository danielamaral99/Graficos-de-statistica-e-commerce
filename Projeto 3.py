import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# ======== Carregar os dados =========
df = pd.read_csv("ecommerce_estatistica.csv")

# Agrupamento de gênero
temp_df = df.copy()
temp_df['genero_agrupado'] = temp_df['Gênero'].replace({
    'Unissex': 'Outros',
    'infantil': 'Outros',
    'Sem gênero infantil': 'Outros',
    'Sem gênero': 'Outros',
    'Meninos': 'Masculino',
    'roupa para gordinha pluss P ao 52': 'Outros',
    'Bebês': 'Outros',
    'Meninas': 'Feminino'
})

# ========= Gráficos =========
fig_pie = px.pie(temp_df, names='genero_agrupado',
                 title="Distribuição de Gêneros de produtos", hole=0.3)

fig_hist = px.histogram(df, x="Preço", nbins=100,
                        title="Histograma - Distribuição de Preços",
                        color_discrete_sequence=["green"])

fig_hex = px.density_heatmap(df, x="Preço", y="Qtd_Vendidos_Cod",
                             nbinsx=40, nbinsy=40,
                             color_continuous_scale="Blues",
                             title="Dispersão de Qtd_Vendidos_Cod e Preço")

df_corr = df[['Preço', 'Qtd_Vendidos_Cod', 'Nota', 'Desconto']].corr()
fig_corr = px.imshow(df_corr, text_auto=True, aspect="auto",
                     color_continuous_scale="RdBu",
                     title="Mapa de calor da Correlação entre variáveis")

# ✅ Correção aqui para o erro do "index"
df_temp = df['Temporada_Cod'].value_counts().reset_index()
df_temp.columns = ["Temporada_Cod", "Quantidade"]

fig_bar = px.bar(df_temp,
                 x="Temporada_Cod", y="Quantidade",
                 title="Produtos divididos em Códigos de Temporada",
                 labels={"Temporada_Cod": "Código da Temporada",
                         "Quantidade": "Qtd de Produtos"},
                 color_discrete_sequence=["#60aa65"])

fig_kde = px.density_contour(df, x="Preço",
                             title="Densidade de Preços em R$")
fig_kde.update_traces(contours_coloring="fill", colorscale="Purples")

fig_reg = px.scatter(df, x="Qtd_Vendidos_Cod", y="Preço",
                     title="Regressão de Quantidade vendida por preço",
                     opacity=0.5)
fig_reg.update_traces(marker=dict(color="#34c289"))

# ========= Layout =========
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard E-commerce - Estatística", style={"textAlign": "center"}),

    # Grid em flexbox para organizar gráficos em duas colunas
    html.Div([
        html.Div(dcc.Graph(figure=fig_pie), style={"flex": "50%"}),
        html.Div(dcc.Graph(figure=fig_hist), style={"flex": "50%"}),
    ], style={"display": "flex"}),

    html.Div([
        html.Div(dcc.Graph(figure=fig_hex), style={"flex": "50%"}),
        html.Div(dcc.Graph(figure=fig_corr), style={"flex": "50%"}),
    ], style={"display": "flex"}),

    html.Div([
        html.Div(dcc.Graph(figure=fig_bar), style={"flex": "50%"}),
        html.Div(dcc.Graph(figure=fig_kde), style={"flex": "50%"}),
    ], style={"display": "flex"}),

    html.Div([
        html.Div(dcc.Graph(figure=fig_reg), style={"flex": "50%"}),
    ], style={"display": "flex"})
])

if __name__ == "__main__":
    app.run(debug=True)