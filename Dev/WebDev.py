#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.express as px
import geopandas as gpd
from dash import Dash, dcc, html, Output, Input, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_ag_grid as dag


# In[2]:


#CUSTOM GRAPHS
import ipynb.fs.full.GraphFunctions as MyGraphs


# ## Prep Pandas Dataframe

# In[3]:


df_Raw = MyGraphs.GetDataframe()
#df_Raw.head()


# ## Prep GeoJson

# In[4]:


gj_PhMap = MyGraphs.GetGeoJson()
#gj_PhMap.head()


# # Website Development
# ### Stylesheet

# In[5]:


# CSS_Styles = [dbc.themes.CERULEAN, "./assets/FIES_styles.css"] #"https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/lumen/bootstrap.min.css"]
app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN, "/assets/FIES_styles.css"],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )


# # Components

# #### [1] Income Choropleth

# In[6]:


graph_1 = dcc.Graph(id='Choropleth_Income', figure={}, clickData=None)
radio_1 = dcc.RadioItems(id='Choropleth_Radio', options=['Mean','Median', 'Min', 'Max'], value='Mean', 
                           labelStyle={"margin-right":"1rem", 'display': 'inline-block'});


# #### [2] Top 10 Jobs

# In[7]:


graph_2 = dcc.Graph(id='Pie_TopJobs', figure={})

topJobsColumnDefs = [{"field": i} for i in ["Household Head Occupation", "count"]]
Table_TopJobs = dag.AgGrid(
            id="Table_TopJobs",
            columnDefs=topJobsColumnDefs,
            rowData=[],
            columnSize="sizeToFit",
            defaultColDef={"filter": True},
            dashGridOptions={"pagination": True, "animateRows": False},
        )


# #### [3] Income vs Expenses

# In[8]:


dropdown_3 = dcc.Dropdown(id='Dropdown_RegionIncomeVsExpenses', options=list(MyGraphs.GetRegionIDs().keys()), value=list(MyGraphs.GetRegionIDs().keys()), clearable=False, multi=True)
checklist_3 = dcc.Checklist(id='Checklist_RegionIncomeVsExpenses', options=list(MyGraphs.GetExpenseTypes().keys()), value=list(MyGraphs.GetExpenseTypes().keys()),
                           labelStyle={"margin-right":"1rem", 'display': 'inline-block'});
toggle_3 = daq.BooleanSwitch(id='Toggle_RegionIncomeVsExpenses');
graph_3 = dcc.Graph(id='Bar_IncomeVsExpenses', figure={})
graph_3_1 = dcc.Graph(id='Scatter_IncomeVsExpenses', figure={})


# #### [4] Food Expenditure Breakdown

# In[9]:


checklist_4 = dcc.Checklist(id='Food_Checklist', value= MyGraphs.GetColumnNames_ForFood(), 
                            options = MyGraphs.GetColumnNames_ForFood(),
                            labelStyle={"margin-right":"1rem", 'display': 'inline-block'},
                           )
dropdown_4 = dcc.Dropdown(id='Food_Dropdown', value=MyGraphs.GetGroupings_ForFoodBreakdown()[0],
                            options= MyGraphs.GetGroupings_ForFoodBreakdown(), clearable=False, 
                         )
graph_4 = dcc.Graph(id='Bar_FoodBreakdown', figure={})


# # Layout

# #### [0] Navbar

# In[10]:


navbar = dbc.Navbar(className = 'sticky-top custom-navbar', children=
    dbc.Container([
            dbc.NavbarBrand("FIES Visualization", className="align-self-start text-light"),
            dbc.Nav(children=[
                        dbc.NavItem(dbc.NavLink("Income", href="#Income Card", external_link=True, className="text-light")),
                        dbc.NavItem(dbc.NavLink("Expenses", href="#Expenses Card", external_link=True, className="text-light")),
                        dbc.NavItem(dbc.NavLink("Food", href="#Food Card", external_link=True, className="text-light"))
                    ]),
        ]),       
    color="primary"
    #dark=True,
)


# #### [1 & 2] Income and Job Cards

# In[11]:


incomeCards = [
        dbc.Card(id='Income Card',
            children = [
            html.H3("Household Income", className='card-header text-primary'),
            dbc.CardBody([
                dbc.Accordion(dbc.AccordionItem([
                        html.H5("Compare the income of each region."),
                        html.H6("Income is an indicator of not just growth per capita but also potential for social mobility. Having more wealth allows families to better afford and access services, education, and oppurtunities."),
                    ]), start_collapsed=False, flush=True),
                 
                dbc.Row([
                    dbc.Col(html.B("Select "), width=1),
                    dbc.Col(radio_1)
                ]),
                graph_1,

                html.Div(id="Label_SelectedRegion")
            ]),
            dbc.CardFooter("See right figures for job data in selected region")
        ]),
    
        dbc.Card([
            html.H3("Regional Professions", className='card-header text-primary'),
            dbc.CardBody([
                dbc.Accordion(dbc.AccordionItem([
                        html.H5("Discover the most common jobs and trades."),
                        html.H6("Not all regions are as well developed and urbanized as NCR, thus certain professions may be restricted in specific regions."),
                    ]), start_collapsed=False, flush=True), 
                graph_2,
                Table_TopJobs
                #dash_table.DataTable(id='Table_TopJobs', data=[]),
            ])
        ])
]


# #### [3] Expenses Card

# In[12]:


expensesCard = dbc.Card(id="Expenses Card", className = 'mt-4',
         children=[
            html.H3("Household Expenses", className='card-header text-primary'),
            
            dbc.CardBody(children=[
                dbc.Accordion(dbc.AccordionItem([
                    html.H5("Utilize the graphs to isolate expenses and see its effect on a household's savings."),
                    html.H6("Poverty is a long persistent issue plaguing the nation. Its causes are rooted in high costs of living and low salaries."),
                ]), start_collapsed=False, flush=True),
        
                #INTERACTIONS
                dbc.Row([
                    dbc.Col(html.B("Regions"), width=1),
                    dbc.Col(dropdown_3)
                ]),
                dbc.Row(style={'justify-items': 'start'}, children=[
                    dbc.Col(html.B("Expenses"), width=1),
                    dbc.Col(checklist_3, width = 3),
                    dbc.Col(html.B("Collapse"), width=1),
                    dbc.Col(toggle_3, width=1),
                ]),
                        
                dbc.Row([
                
                    dbc.Col(graph_3),
                    dbc.Col(graph_3_1, width=3)
                ])
            ])
    ])


# #### [4] FoodCard

# In[13]:


# GRAPH 4 Foods Expenditure
foodCard = dbc.Card(id="Food Card", className='mt-4',
       children=[
           html.H3("Food Expenditure", className='card-header text-primary'),
           dbc.CardBody(children=[
               dbc.Accordion(dbc.AccordionItem([
                   html.H5("Explore different categories to find those requiring assistance for nurtitional balance."),
                   html.H6("Being able to monitor food expenditure amongst different groups can help us analyze the nurtitional intake of varying types of households."),
               ]), start_collapsed=False, flush=True),
               
               #INTERACTIONS
               dbc.Row([
                   dbc.Col(html.B("Factors"), width=1), 
                   dbc.Col(dropdown_4, width=3)
               ]),
               dbc.Row([
                   dbc.Col(html.B("Food"), width=1),
                   dbc.Col(checklist_4)
               ]),
               
               graph_4
           ])
   ])


# # Callback

# #### [1] Income Choropleth

# In[14]:


@app.callback(
    Output(component_id='Choropleth_Income', component_property='figure'),
    Input(component_id='Choropleth_Radio', component_property='value')
)
def UpdateIncomeChoropleth(aggChoice):
    fig = MyGraphs.GetFig_Choropleth(
        ref_Dataframe = df_Raw, 
        ref_GeoJson = gj_PhMap, 
        agg_Mode = aggChoice
    )
    return fig


# #### [2] Top 10 Jobs

# In[15]:


@app.callback(
    [
        Output(component_id='Pie_TopJobs', component_property='figure'),
        Output(component_id='Table_TopJobs', component_property='rowData'),
        Output(component_id='Label_SelectedRegion', component_property='children')
    ],
    Input(component_id='Choropleth_Income', component_property='clickData')
)
def UpdateTopJobs(clk_data):
        if clk_data is None:
            fig2 = MyGraphs.GetFig_MostEmployedJobs(df_Raw, 'NCR', 0, 10);
            table2 = MyGraphs.Filter_TopJobs(df_Raw, 'NCR', 0, 1000).reset_index().to_dict('records');
            markdown2 = html.H3("Select a region by clicking on the map.")
            return fig2, table2, markdown2 
        else:
            clk_Region = clk_data['points'][0]['location']
            fig2 = MyGraphs.GetFig_MostEmployedJobs(df_Raw, clk_Region, 0, 10);
            table2 = MyGraphs.Filter_TopJobs(df_Raw, clk_Region, 0, 1000).reset_index().to_dict('records');
            markdown2 = [
                html.H3("Inspecting Region " + clk_Region, className='mb-2'),
                html.H5("Aggregated Income  :  " + format(int(clk_data['points'][0]['z']), ','), className='my-2 text-monospace'),
                html.H5("Responses Collected :  " + str(df_Raw.groupby('Region').get_group(clk_Region).shape[0]), className='my-2 text-monospace')
            ]
            return fig2, table2, markdown2


# #### [3] Income vs Expenses

# In[16]:


@app.callback(
    [
        Output(component_id='Bar_IncomeVsExpenses', component_property='figure'),
        Output(component_id='Scatter_IncomeVsExpenses', component_property='figure')
    ],
    Input(component_id='Dropdown_RegionIncomeVsExpenses', component_property='value'),
    Input(component_id='Checklist_RegionIncomeVsExpenses', component_property='value'),
    Input(component_id='Toggle_RegionIncomeVsExpenses', component_property='on')
)
def UpdateIncomeExpenseComparison(slct_Regions, slct_Category, is_Collapse):
    # if slct_Regions is None or slct_Category is None:
    #     return MyGraphs.GetFig_IncomeVsExpenses(df_Raw, ['NCR'], ['Income'])
    # else:
    barGraph = MyGraphs.GetFig_IncomeVsExpenses(df_Raw, slct_Regions, slct_Category, is_Collapse) 
    scatterGraph = MyGraphs.GetFig_IncomeVsExpensesScatter(df_Raw, slct_Regions, slct_Category) 
    return barGraph, scatterGraph


# #### [4] Food Expenditure Breakdown

# In[17]:


@app.callback(
    Output(component_id='Bar_FoodBreakdown', component_property='figure'),
    Input(component_id='Food_Checklist', component_property='value'),
    Input(component_id='Food_Dropdown', component_property='value')
)
def UpdateFoodExpenditure(slct_foods, slct_grouping):
    # if slct_foods is None or slct_grouping is None:
    #     return MyGraphs.GetFig_FoodBreakdown(df_Raw, MyGraphs.GetColumnNames_ForFood(), 'Total Number of Family members')
    # else:
    return MyGraphs.GetFig_FoodBreakdown(df_Raw, slct_foods, slct_grouping)


# In[18]:


app.layout = dbc.Container(fluid=True, children=[
    navbar,
    dbc.CardGroup(children = incomeCards, className = 'mt-4'),    
    expensesCard,
    foodCard,
])


# # Run

# In[19]:


from flask import Flask, render_template

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8053)

# if __name__ == '__main__':
    # app.run_server(port=8053)


# In[ ]:




