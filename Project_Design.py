# !pip3 install geojson
# pip uninstall geopandas fiona pyproj rtree shapely
# conda install --channel conda-forge geopandas

import numpy as np
import pandas as pd

import geopandas as gpd
from dash import Dash , html, dcc
import jupyter_dash
import plotly.express as px

from dash.dependencies import Input , Output , State
import dash_bootstrap_components as dbc
from dash import html

from urllib.request import urlopen
import json

with open('stanford-gg870xt4706-geojson.json') as f:
    ukr_json = json.load(f)

ukr1_df = pd.read_csv('ukr1_df.csv')
ukr1_df.drop('NL_NAME_1', axis = 1,inplace = True)
ukr1_df.dropna(axis = 0, inplace = True)

ukr1_df['Condition'] = np.where(
    ukr1_df['control'] == 1 ,'Russian military control' , np.where(
    ukr1_df['control'] == 2 ,'Ukrainian counter-attack','ukraine Liberated'))

Inflation_Data = pd.read_csv("Inflation.csv")
Inflation_Data.head()

# UR_Data = UR_Data.drop('Unnamed: 0' , axis =1)
# UR_Data = UR_Data.dropna(axis = 1)
Inflation_Data = Inflation_Data.drop(Inflation_Data.filter(regex='Unnamed').columns, axis=1)
Inflation_Data = Inflation_Data.drop(Inflation_Data.index[0:15] , axis = 0)
Inflation_Data.head()

UR_Data = pd.read_csv("Russia-Ukraine Equipment Losses - Origional.csv")
UR_Data.head()

UR_Data['UNHCR Ukraine Refugees'] = UR_Data['UNHCR Ukraine Refugees'].fillna(UR_Data["UNHCR Ukraine Refugees"].mean())
# UR_Data = UR_Data.dropna(axis = 1)
UR_Data = UR_Data.drop(UR_Data.filter(regex='Unnamed').columns, axis=1)

color_global =  "#fbfcfc"
# "#ffffff"  '#e9ecef'  "#60A3D9"

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP , FONT_AWESOME])

card_content = [
    dbc.CardHeader("Card header"),
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "This is some card content that we'll reuse",
                className="card-text",
            ),
        ]
    ),
]

fig_map = px.choropleth_mapbox(ukr1_df, geojson=ukr_json,
                           color="Condition",
                           color_discrete_map={'Ukrainian counter-attack': "#FFD500" ,      #e6d385',
                                               'ukraine Liberated': "#005BBB"        ,      #5c7658',
                                               'Russian military control':'#681313'
                                              },
                           opacity = 1,
                           locations="Region",
                           featureidkey="properties.name_1",
                           center={"lat": 48.3794, "lon": 31.1656},  #49.4444° N, 32.0598° ukraine E 48.3794° N, 31.1656° E
                           mapbox_style= "carto-positron",#"carto-darkmatter",     #carto-positron",
                           zoom=4.25,
                           hover_name="Region", # column to add to hover information
                           color_continuous_scale=px.colors.sequential.Plasma,
                           animation_frame='date'
                          )

fig_map.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 2000
fig_map.update_layout(
    autosize=False,
    width=1300,
    height=500,
    margin={"r":0,"t":0,"l":0,"b":0},
    legend=dict(
        x=0,
        y=1,
        traceorder="normal",
        font=dict(
            family="sans-serif",
            size=12,
            color="black"
        ),
    )
)



fig_map.update_layout(paper_bgcolor= color_global)

fourth_graph =dcc.Graph(
        id="Random_graph2",
#         figure={
#             'layout': {
#                 'plot_bgcolor': colors['background'],
#                 'paper_bgcolor': colors['background'],
#                 'font': {
#                     'color': colors['text']
#                 }
#             }
#         }
    )

draw = px.line(UR_Data , x='Date' , y =["Ukraine_Total" , "Russia_Total"] , title="Ukraine VS Russia Human Losses")
draw.update_layout(paper_bgcolor= color_global , plot_bgcolor = color_global , xaxis=dict(showgrid=False),
          yaxis=dict(showgrid=False)
                  ,
                  )
draw['data'][0]['line']['color']= "#FFD500"
draw['data'][1]['line']['color']= "#005BBB"
draw

draw_inflation = px.line(Inflation_Data, x='Date', y=["Fruits and vegatables.1", "Regulated Items.1"], title="")
draw_inflation.update_layout(paper_bgcolor=color_global, plot_bgcolor=color_global, xaxis=dict(showgrid=False),
                             yaxis=dict(showgrid=False)
                             , title="Inflation"

                             )

draw_inflation['data'][0]['line']['color'] = "#ff6347"
draw_inflation['data'][1]['line']['color'] = "#005BBB"
draw_inflation

colors = {
    'background': '#e9ecef',
    'text': '#7FDBFF'
}

# inflation_fig = dcc.Graph(
#         id="Inflation_Data",
#         figure={
#             'data': [
#                 {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
#                 {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
#             ],
#             'layout': {
#                 'plot_bgcolor': colors['background'],
#                 'paper_bgcolor': colors['background'],
#                 'font': {
#                     'color': colors['text']
#                 }
#             }
#         }
#     )


inflation_fig = html.Div(children=[

    #         dcc.Dropdown(Inflation_Data.columns, 'Headline CPI', id='Select_Y_axis1'
    #                      ,style={ 'width': '200px','color': '#212121', 'background-color': '#e9ecef', }),
    dcc.Graph(figure=draw_inflation,
              id="Inflation_Data",
              #         figure={
              #             'layout': {
              #                 'plot_bgcolor': colors['background'],
              #                 'paper_bgcolor': colors['background'],
              #                 'font': {
              #                     'color': colors['text']
              #                 },

              #             }

              #         }
              )

], style={'backgroundColor': color_global})

loss_df = pd.read_csv("Russia-Ukraine Equipment Losses - Origional.csv")
loss_df = loss_df.drop(loss_df.filter(regex='Unnamed').columns, axis=1)
url_df = pd.DataFrame({
    # 'color': ['red','green','blue','pink','purple',"brown",'yellow','lightsalmon'],
    'color': 'red',
    'img_url': [
        "https://upload.wikimedia.org/wikipedia/commons/0/03/Refugee_care_near_Poland_border_train_station_20220228.jpg",
        # 1
        "https://upload.wikimedia.org/wikipedia/commons/4/45/Ukrainian_refugees_from_2022%2C_crossing_into_Poland.jpg",
        # 2
        "https://upload.wikimedia.org/wikipedia/commons/b/b2/Warsaw_Central_Station_during_Ukrainian_refugee_crisis_10.jpg",
        # 3
        "https://media.npr.org/assets/img/2022/03/03/refugees.children.getty-7f16b5a3c923f8deac38a3ec875a217088a21421-s900-c85.webp",
        # 4 A refugee girl carries a sibling after arriving at the Hungarian border
        "https://static.euronews.com/articles/stories/06/50/67/90/1440x810_cmsv2_e6fc023b-e933-5cab-adb8-746b584ad7df-6506790.jpg",
        # 5
        "https://global.unitednations.entermediadb.net/assets/mediadb/services/module/asset/downloads/preset/Collections/UNHCR/Embargoed+2/18-03-2022_UNICEF_Ukraine-06.jpg/image1170x530cropped.jpg",
        # 6
        "https://idsb.tmgrup.com.tr/ly/uploads/images/2022/03/07/188440.jpg",  # 7
        "https://foreignpolicy.com/wp-content/uploads/2022/03/1-ukraine-refugee-russia-lviv-kyiv-slinski-lead-6O1A1436.jpg?w=1024&h=682&quality=90",
        # 8
        "https://s.abcnews.com/images/Health/refugee-family-ukraine-rt-ps-220301_1646153536012_hpMain_16x9_1600.jpg",
        # 9
        "https://www.unicef.org/sites/default/files/styles/press_release_feature/public/UN0599229.jpg?itok=7YP910M_",
        # 10
        "https://www.unicef.org/lac/sites/unicef.org.lac/files/styles/hero_mobile/public/UN0599222.jpg?itok=gxryGRtG",
        # 11
        "https://www.unicef.org/sites/default/files/styles/press_release_feature/public/UN0599229.jpg?itok=7YP910M_",
        # 12
        "https://i.inews.co.uk/content/uploads/2022/03/SEI_92096113-640x360.jpg",
        # 13       12-year-old Alexandra sits on a bus holding her sister Esyea, 6, who cries as she waves at her mother Irina, as they leave Odesa in southern Ukraine
        "https://s.abcnews.com/images/Health/refugee-family-ukraine-rt-ps-220301_1646153536012_hpMain_16x9_1600.jpg",
        # 14
        "https://feeds.abplive.com/onecms/images/uploaded-images/2022/03/15/b74c8da5878b774e2f10c5cc56c34888_original.jpg",
        # 15
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQyfZtiVK8lHcmbGJ2B-NFvV3LumAn-BCQh87CdfjkDVKos2cNmrp82mtlTMBH41oBSrTI&usqp=CAU",
        # 16
        "https://s.yimg.com/ny/api/res/1.2/WllwocvCs8Ys4atysu414A--/YXBwaWQ9aGlnaGxhbmRlcjt3PTY0MA--/https://s.yimg.com/os/creatr-uploaded-images/2022-03/601cc0e3-9b0d-11ec-bb65-12f6cf1eab0d",
        # 17
        "https://www.politico.com/dims4/default/69bff3c/2147483647/strip/true/crop/5616x3744+0+0/resize/630x420!/quality/90/?url=https%3A%2F%2Fstatic.politico.com%2Fcc%2Fc8%2Ff0e47ed24f01913f9d5f807a8900%2Fpoland-russia-ukraine-war-64536.jpg",
        # 18 Nearly two-thirds of Ukraine’s children have fled homes
        "https://i.inews.co.uk/content/uploads/2022/03/SEI_92195951.jpg",
        # 19 11-year-old Ukrainian boy who travelled 700 miles to Slovakia solo to flee the violence
        "https://www.unicef.org/sites/default/files/styles/press_release_feature/public/UN0605554%20%281%29.jpg?itok=m60-zEPv",
        # 20
        "https://i.guim.co.uk/img/media/a0be4836730cd51c3ab508f9b05c847e641aa199/0_224_6720_4032/master/6720.jpg?width=620&quality=45&auto=format&fit=max&dpr=2&s=02cfc40d1629eb4cbcfb6db8a6d2e7a1",
        # 21
        "https://i.guim.co.uk/img/media/a5e7f33fb8d54b3a77917d865a431ddeae0a31bf/0_181_6720_4032/master/6720.jpg?width=620&quality=45&auto=format&fit=max&dpr=2&s=1df4e12f3107a186632d0fc7620e6d43",
        # 22
        "https://static.independent.co.uk/2022/03/10/11/Refugees%20welcome%20Zhanna%20Tetyana.jpg?quality=75&width=990&auto=webp&crop=982:726,smart",
        # 23
        "https://s.yimg.com/ny/api/res/1.2/xc3wMblzqwLNGy189jlbXw--/YXBwaWQ9aGlnaGxhbmRlcjt3PTcwNTtoPTQ3MDtjZj13ZWJw/https://s.yimg.com/uu/api/res/1.2/kRr_qP.7JozNyqSrOUpq2A--~B/aD01NjA7dz04NDA7YXBwaWQ9eXRhY2h5b24-/https://media.zenfs.com/en/la_times_articles_853/c021cab16de5b6e898600a337305e158",
        # 24
        "https://newsinfo.inquirer.net/files/2022/03/STJZOMG2IVPXXNXA2EMGYKJFQ4-768x614.jpg",  # 25
        "https://cdn.cnn.com/cnnnext/dam/assets/150210172942-01-ukraine-on-the-ground-0210-exlarge-169.jpg",  # 26
        "https://english.cdn.zeenews.com/sites/default/files/2022/03/20/1024193-ukrainerefugeecampxx.jpg",  # 27
        "https://english.cdn.zeenews.com/sites/default/files/2022/03/20/1024195-ukrainerefugeecampx.jpg",  # 28
        "https://static.timesofisrael.com/www/uploads/2022/03/AP22067637646912.jpg",  # 29
        "https://nypost.com/wp-content/uploads/sites/2/2022/03/irpin-civilians-attached-reuters-02.jpg?quality=90&strip=all",
        # 30
        "https://static.timesofisrael.com/www/uploads/2022/03/000_324G3CQ.jpg",  # 31
        "https://see.news/wp-content/uploads/2022/02/11-2.jpg",  # 32
        "https://www.eppgroup.eu/sites/default/files/styles/crop_838x582/public/photo/2022/02/gettyimages-1238719758.jpg?itok=MGRgK1Gf",
        # 33
        "data:image/jpeg;base64,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",
        "https://images.theconversation.com/files/449726/original/file-20220303-25-1gyhn6n.jpg?ixlib=rb-1.1.0&rect=172%2C14%2C4760%2C3308&q=20&auto=format&w=320&fit=clip&dpr=2&usm=12&cs=strip",
        # 35
        "https://img.thedailybeast.com/image/upload/c_crop,d_placeholder_euli9k,h_1688,w_3000,x_0,y_126/dpr_1.5/c_limit,w_1044/fl_lossy,q_auto/v1646748600/GettyImages-1239006263_wubznv",
        # 36
        "https://gcaptain.com/wp-content/uploads/2022/03/2022-03-05T184932Z_668485574_RC2GWS9BX210_RTRMADP_3_UKRAINE-CRISIS-LVIV-TRAIN-STATION-2048x1316.jpg",
        # 37
        "https://www.vaticannews.va/content/dam/vaticannews/agenzie/images/afp/2022/03/09/13/1646827355982.jpg/_jcr_content/renditions/cq5dam.thumbnail.cropped.750.422.jpeg",
        # 38
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRamYJL5xRCpQBfCICeTr6vv7LlkJX-4IU_ow&usqp=CAU",  # 39
        "https://content.gallup.com/origin/gallupinc/GallupSpaces/Production/Cms/POLL/xgssemj54kaobqpbikihpw.jpg",  # 40
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRY47-Fpv561eO31puQaLUsePShc8l7q_yAew&usqp=CAU",  # 41
        "https://i2-prod.dailyrecord.co.uk/incoming/article26439636.ece/ALTERNATES/s1200c/1_JS260201516.jpg"  # 42
    ],
    'Story': [
        '',  # 1
        '',  # 2
        '',  # 3
        'A refugee girl carries a sibling after arriving at the Hungarian border',  # 4
        '',  # 5
        '',  # 6
        '',  # 7
        '',  # 8
        '',  # 9
        'Families board a train at the station in Lviv, Ukraine, heading toward the Polish border on March 3',  # 10
        '',  # 11
        '',  # 12
        '',  # 13
        '',  # 14
        '12-year-old Alexandra sits on a bus holding her sister Esyea, 6, who cries as she waves at her mother Irina, as they leave Odesa in southern Ukraine',
        # 15
        '',  # 16
        '',  # 17
        'Nearly two-thirds of Ukraine’s children have fled homes',  # 18
        '11-year-old Ukrainian boy who travelled 700 miles to Slovakia solo to flee the violence',  # 19
        'Families arrive in Berdyszcze, Poland, after crossing the border from Ukraine.',  # 20
        'Ukrainian children after they crossed the Poland-Ukraine border at Medyka',  # 21
        'A boy holds a soft toy after crossing the border into Poland from Ukraine.',  # 22
        "Eighty-seven year-old Tetyana Vatazhok leaned" + "<br>" + "heavily on her crutches and set her face defiantly against the freezing cold as snow fell all around her.",
        # 23
        "Refugees fleeing the conflict from neighboring Ukraine help push an elderly lady sitting in a wheelchair, at the Romanian-Ukrainian border, in Siret, Romania.",
        # 24
        "An elderly woman is helped while crossing a destroyed bridge as she tries to leave the cith of Irpin , the the Kyiv Region",
        # 25
        "Refugees escape the fighting while Grad missile systems head to the front.",  # 26
        "Children who fled inside refugee camps.",  # 27
        "Elderly women who escaped russian bombarding.",  # 28
        "Ukrianian refugee in international Woman's day.",  # 29
        "Ukrainians flee Russian bombs as civilians are killed in small Kyiv suburb.",  # 30
        "Civilianse facing full distruction.",  # 31
        "Mother holding her daughter under shock.",  # 32
        "Civiliance facing full distruction.",  # 33
        "The elderly leaving home behind.",  # 34
        "",  # 35
        "6 year old Tanya died from thirst as Russia cut water supply.",  # 36
        "A woman cries as she comforts her son after learning she has to leave a bus which was reserved for the evacuation of orphans fleeing the ongoing Russian invasion outside the main train station in Lviv, Ukraine",
        # 37
        "",  # 38
        "",  # 39
        "",  # 40
        "",  # 41
        ""  # 42

    ]

})
new_df = pd.concat([loss_df, url_df], axis=1, join='inner')

from jupyter_dash import JupyterDash
from dash import Dash, dcc, html, Input, Output, no_update
import plotly.graph_objects as go

fig = go.Figure(
    go.Scatter(
        x=loss_df['Date'],
        y=loss_df['UNHCR Ukraine Refugees'],
        # mode='markers',
        # mode = "lines",
        mode='lines+markers',
        # size = loss_df['UNHCR Ukraine Refugees'],
        # marker=dict(color=new_df['color'])
        marker=dict(color='#005BBB')
        # marker=dict(color='red')
    )
)

fig.update_traces(hoverinfo="none", hovertemplate=None)
fig.update_layout(
    paper_bgcolor=color_global, plot_bgcolor=color_global, xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    title={
        'text': "Ukraine Refugees",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title="Date",
    yaxis_title="Number of Refugees",
    legend_title="Ukraine Refugees",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#005BBB"
    )
)

# app = JupyterDash(_name_)

# server = app.server
# app = Dash()

Ukraine_refugees = html.Div([
    dcc.Graph(id="graph-basic-2", figure=fig, clear_on_unhover=True),
    dcc.Tooltip(id="graph-tooltip", direction='bottom'),
])


@app.callback(
    Output("graph-tooltip", "show"),
    Output("graph-tooltip", "bbox"),
    Output("graph-tooltip", "children"),
    Output("graph-tooltip", "direction"),

    Input("graph-basic-2", "hoverData"),
)
def display_hover(hoverData):
    if hoverData is None:
        return False, no_update, no_update, no_update

    # demo only shows the first point, but other points may also be available
    pt = hoverData["points"][0]
    bbox = pt["bbox"]
    num = pt["pointNumber"]

    df_row = new_df.iloc[num]
    img_src = df_row['img_url']

    children = [
        html.Div([
            html.Img(
                src=img_src,
                style={"width": "250px"},
            ),
            html.P(
                df_row['Story'],
                style={"overflow-y": "auto"}
            )
        ],
            style={"width": "250px",
                   "overflow-y": "hidden"},
        )

    ]

    y = hoverData["points"][0]['y']
    direction = "bottom" if y > 2 else "top"

    return True, bbox, children, direction


card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

card1 = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H6("Human Losses", className="card-title", style={"text-align": "center"}),
                    html.H1("14,000", className="card-title", style={"text-align": "center"}),
                    #                     html.P("People Loss of 🇺🇦 VS 🇷🇺", className="card-text",),
                ]
            )
        ),
        dbc.Card([
            html.H1(" ", style={"text-align": "center"}),
            html.H1(" ", style={"text-align": "center"}),
            html.H1(" ", style={"text-align": "center"}),
            html.H1("🩸", style={"text-align": "center"}),
            #             html.Div(className="fa-regular fa-user❤😍", style=card_icon),

        ],
            className="bg-primary",
            style={"maxWidth": 75}, ),
    ],
    className="mt-4 shadow",
)

card2 = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H6("Oil Barrel Price", className="card-title", style={"text-align": "center"}),
                    html.H1("107$", className="card-title", style={"text-align": "center"}),
                    #                     html.P("People Loss of 🇺🇦 VS 🇷🇺", className="card-text",),
                ]
            )
        ),
        dbc.Card([
            html.H1(" ", style={"text-align": "center"}),
            html.H1(" ", style={"text-align": "center"}),
            html.H1(" ", style={"text-align": "center"}),
            html.H1("🛢️", style={"text-align": "center"}),
            #             html.Div(className="fa-regular fa-user❤😍", style=card_icon),

        ],
            className="bg-primary",
            style={"maxWidth": 75}, ),
    ],
    className="mt-4 shadow",
)

card3 = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H6("Inflation", className="card-title", style={"text-align": "center"}),
                    html.H1("8.8%", className="card-title", style={"text-align": "center"}),
                    #                     html.P("People Loss of 🇺🇦 VS 🇷🇺", className="card-text",),
                ]
            )
        ),
        dbc.Card([
            html.H1(" ", style={"text-align": "center"}),
            html.H1(" ", style={"text-align": "center"}),
            html.H1(" ", style={"text-align": "center"}),
            html.H1("🍅", style={"text-align": "center"}),

            #             html.H1("📈" , style = {"text-align" : "center"}),
            #             html.Div(className="fa-regular fa-user❤😍", style=card_icon),

        ],
            className="bg-primary",
            style={"maxWidth": 75}, ),
    ],
    className="mt-4 shadow",
)
card4 = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H6("Refugees", className="card-title", style={"text-align": "center"}),
                    html.H1("4,278,789", className="card-title", style={"text-align": "center"}),
                    #                     html.P("People Loss of 🇺🇦 VS 🇷🇺", className="card-text",),
                ]
            )
        ),
        dbc.Card([
            html.H1(" ", style={"text-align": "center"}),
            html.H1(" ", style={"text-align": "center"}),
            html.H1(" ", style={"text-align": "center"}),
            html.H1("🏠", style={"text-align": "center"}),

            #             html.H1("📈" , style = {"text-align" : "center"}),
            #             html.Div(className="fa-regular fa-user❤😍", style=card_icon),

        ],
            className="bg-primary",
            style={"maxWidth": 75}, ),
    ],
    className="mt-4 shadow",
)

app.layout = html.Div(html.Div(children=[

    dbc.Row(
        [
            html.H1("Ukraine Invasion", className="card-title",
                    style={"text-align": "center"})],
        className="py-4",
    ),
    dbc.Row(
        [

            dbc.Col(card1),
            dbc.Col(card2),
            dbc.Col(card3),
            dbc.Col(card4),

        ], className="py-4",
    ),

    dbc.Row([

        dbc.Col(dcc.Graph(id="Random_graph1",
                          figure=fig_map
                          )),

    ], className="py-4", ),

    dbc.Row([

        dbc.Col(html.Div(children=[
            #     dcc.Dropdown(UR_Data.columns, 'Date', id='Select_Y_axis'
            #                  ,style={ 'width': '200px','color': '#212121', 'background-color': '#e9ecef', }),
            dcc.Graph(id="UR_Graph", figure=draw),

        ]), lg=7),

        dbc.Col(inflation_fig,
                style={"width": 350, "height": 350},
                ),

        #     dbc.Col(fourth_graph, lg=5),
    ], className="py-4",

        style={'backgroundColor': color_global}),

    dbc.Row([

        dbc.Col(Ukraine_refugees),

    ], className="py-4", ),

], className="py-2 container", )

    , style={'backgroundColor': color_global})
# '#e9ecef'



app.run_server()