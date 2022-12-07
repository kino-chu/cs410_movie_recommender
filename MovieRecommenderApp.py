from dash import Dash, dcc, html, Input, Output, State
import pandas as pd 
import dash_bootstrap_components as dbc
from rank_bm25 import * 
import plotly.express as px

# Connect to dataset and load it into data frame    
data = pd.read_csv("netflix_titles.csv")

# Dash application layout using bootstrap. 
app = Dash(__name__, external_stylesheets= [dbc.themes.BOOTSTRAP])
colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}
app.layout = dbc.Container([
    # application title 
    dbc.Row ([
        dbc.Col(html.H1('Favourite Movie Recommendation', className= 'text-center')) 
    ]), 
    html.Br(), 
    
    # top 5 recommended movie based on selected ones 
    dbc.Row ([
        dbc.Col(
            html.H3('Similar Movie Recommender', className= 'text-center')) 
    ]), 
    dbc.Row ([
        dbc.Col (dcc.Dropdown (data['title'].unique(), id='movetitle_dropdown',placeholder="Select movie from below drop down to see top 5 similar ones"))
    ]), 
    dbc.Row ([
        dbc.Col(dcc.Graph (id = 'top_similar_movies'), xs=12,sm=12, md=12,lg=12,xl=12), 

    ]), 
    html.Br(), 
    
    # layout for the movie look up section 
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H3('Movie Information Lookup', className= 'text-center'),
                dcc.Dropdown(data['title'].unique(), id='movetitle_dropdown2'),
                html.Table([
                    html.Tr([html.Td('Type'), html.Td(id='type')]),
                    html.Tr([html.Td('Director'), html.Td(id='director')]),
                    html.Tr([html.Td('Cast'), html.Td(id='cast')]),
                    html.Tr([html.Td('Country'), html.Td(id='country')]),
                    html.Tr([html.Td('Release Year'), html.Td(id='year')]),
                    html.Tr([html.Td('Rating'), html.Td(id='rating')]),
                    html.Tr([html.Td('Duration'), html.Td(id='duration')]), 
                    html.Tr([html.Td('Description'), html.Td(id='description')]),
                ], style = {
                    'padding-right': '200px',
                    'margin-right': 'auto',
                }),
            ])
        )
    ]), 
    ])

# movie look up  
@app.callback(
    Output('type', 'children'),
    Output('director', 'children'),
    Output('cast', 'children'),
    Output('country', 'children'),
    Output('year', 'children'),
    Output('rating', 'children'),    
    Output('duration', 'children'),
    Output('description', 'children'),
    Input('movetitle_dropdown2', 'value')
)
def movie_lookup(value):
    df_movie = data.loc[data['title']== value]
    return df_movie['type'], df_movie['director'], df_movie['cast'], df_movie['country'], df_movie['release_year'], df_movie['rating'], df_movie['duration'], df_movie['description'] 

# top 5 similar movies 
@app.callback(
    Output('top_similar_movies', 'figure'),
    Input('movetitle_dropdown', 'value')
)
def top_similar_movies (value): 
    movie_sim = data 
    stop_words = ["i", "me", "my", "myself", 
               "we", "our", "ours", "ourselves", 
               "you", "your", "yours", 
               "their", "they", "his", "her", 
               "she", "he", "a", "an", "and",
               "is", "was", "are", "were", 
               "him", "himself", "has", "have", 
               "it", "its", "the", "us"] 
    movie_sim ['tokenized'] = movie_sim['description'].apply(lambda x: ', '.join([word for word in x.lower().split() if word not in (stop_words)]))

    selected_movie = movie_sim.loc[movie_sim['title']==value] 
    selected_desc_token = str(selected_movie['tokenized'].values) 
    bm25 = BM25Okapi(movie_sim['tokenized'])
    movie_sim['Similarity Score'] = bm25.get_scores(selected_desc_token)
    top_5  = bm25.get_top_n (selected_desc_token, movie_sim['description'], n =5)
    df_final = movie_sim[movie_sim['description'].isin(top_5)]
    df_final = df_final.sort_values(by= 'Similarity Score', ascending=False)
    fig = px.bar(df_final, x="title", y ='Similarity Score', title= "Top 5 Similar Movies based on Selection", color= "title")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)