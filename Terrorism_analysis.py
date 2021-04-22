import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import webbrowser
import base64
import dash.dependencies 
import plotly.graph_objects as go
import plotly.express as px
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc


app=dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
def load_data():
    
    
    dataset_name="global_terror.csv"
    global df
    df=pd.read_csv(dataset_name)
    
    #month dictionary
    month={
        "January":1,
        "February":2,
        "March":3,
        "April":4,
        "May":5,
        "June":6,
        "July":7,
        "August":8,
        "September":9,
        "October":10,
        "November":11,
        "December":12
        }
    
    
    global month_list
    month_list=[{"label":key,"value":values} for key,values in month.items()]
     
    global region_list
    region_list=[{"label":str(i),"value":str(i)} for i in sorted(df['region_txt'].unique().tolist())]
    
    global country_list
    country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()
    #print(country_list)
    
    global state_list
    state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()
    
    global city_list
    city_list  = df.groupby("provstate")["city"].unique().apply(list).to_dict()

    global attack_type_list
    attack_type_list = [{"label": str(i), "value": str(i)}  for i in df['attacktype1_txt'].unique().tolist()]
    
    #slider
    global year_list
    year_list = sorted(df['iyear'].unique().tolist())
    global year_dict
    year_dict={str(year):str(year) for year in year_list}
    
    
    
    #chart dropdown options
    global chart_dropdown_values
    chart_dropdown_values = {"Terrorist Organisation":'gname', 
                             "Target Nationality":'natlty1_txt', 
                             "Target Type":'targtype1_txt', 
                             "Type of Attack":'attacktype1_txt', 
                             "Weapon Type":'weaptype1_txt', 
                             "Region":'region_txt', 
                             "Country Attacked":'country_txt'
                          }
                              
    chart_dropdown_values = [{"label":keys, "value":value} for keys, value in chart_dropdown_values.items()]
    

    global encoded_image
    image_filename = 't2.png' # replace with your own image
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
  

    
def create_app_ui():
    
    
    
    main_layout=html.Div(
        
        
        
        
        
        children=[
            
            
        html.Div(
        [
            html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                height=200,
                width='100%',
                 )
            
        ],style={'textAlign': 'center'}),
           
        
        html.H1(children='Terrorism Analysis with Insights',id='main_title',style={'color': 'black','textAlign': 'center'}),
        
        dcc.Tabs(id="Tabs",value="tab-1",children=[
            dcc.Tab(label="Map Tool",id="Map Tool",value="tab-1",children=[
                dcc.Tabs(id="subtab1",value="tab-1",children=[
                    dcc.Tab(label="World Map Tool",id="World",value="tab-1"),
                    dcc.Tab(label="India Map Tool",id="India",value="tab-2")
                    ]),
                    
                    
                    dcc.Dropdown(id='month',
                    options=month_list,
                     placeholder='Select Month',
                     multi=True
                     ),
        
         dcc.Dropdown(id='date',
                    #options=date_list,
                     placeholder='Select Date',
                      multi=True
                     ),
         
         dcc.Dropdown(id='region',
                    options=region_list,
                     placeholder='Select Region',
                      multi=True
                      ),
          
          dcc.Dropdown(id='country',
                       options=[{'label':'All','value':'All'}],
                     placeholder='Select Country',
                      multi=True
                      ),
           
          dcc.Dropdown(id='state',
                    options=[{'label':'All','value':'All'}],
                     placeholder='Select State',
                      multi=True
                      ),
            
          dcc.Dropdown(id='city',
                      options=[{'label':'All','value':'All'}],
                     placeholder='Select City',
                       multi=True
                     ),
             
          dcc.Dropdown(id='attack',
                    options=attack_type_list,
                     placeholder='Select AttackType',
                      multi=True
                      ),
       
        html.Br(),
        
        html.H5('Select the Year',id='year_title',style={'textAlign':'center'}),
        
        dcc.RangeSlider(
          id='year_slider',
          min=min(year_list),
          max=max(year_list),
          value=[min(year_list),max(year_list)],
          marks=year_dict
      
                ),
       
          html.Div(id='graph-object',children=[
              
              
               html.Div(
    [
        html.H5('Loading Map'),
        dbc.Spinner(color="warning", type="border"),
        dbc.Spinner(color="danger", type="border"),
        dbc.Spinner(color="info", type="border"),
        
        ]),
 
              ])          
                    
                    ]),

            dcc.Tab(label="Chart Tool",id="Chart Tool",value="tab-2",children=[
                dcc.Tabs(id="subtab2",value="tab-2",children=[
                    dcc.Tab(label="World Chart Tool",id="WorldC",value="tab-3"),
                    dcc.Tab(label="India Chart Tool",id="IndiaC",value="tab-4")
                    
                    
              
                
                
                ]),
                
                html.Br(),
                
            dcc.Dropdown(id="chart_dropdown",
                         options=chart_dropdown_values,
                         placeholder='Select Options'
                         
             
                     ),
            html.Br(),
            
               html.Div(id='alert1',children=[
            dbc.Alert(
                html.P(
            "Choose The Filter Above. "),
                
                )
            
            ]),
      
              html.Br(),
              #html.Div("Search Filter"),
             dcc.Input(id='search',placeholder="Search Filter"),
             html.Br(),
              #html.Br(),
             #html.Hr(),
             
             
             
              html.Br(),
              html.Div("Select Year Range"),
               html.Br(),
            
             
        dcc.RangeSlider(
          id='chart_year_slider',
          min=min(year_list),
          max=max(year_list),
          value=[min(year_list),max(year_list)],
          marks=year_dict
      
                ),
             
             html.Br(),
                
                
                
             html.Div(id='chart-object',children=[
                 
                          
               html.Div(
    [
        html.H5('Loading Chart'),
        dbc.Spinner(color="warning", type="border"),
        dbc.Spinner(color="danger", type="border"),
        dbc.Spinner(color="info", type="border"),
        
        ]),
    
                 ]),  
       
            ]),
   
            
            ]),
         
        html.Hr(),
        
         ]
      
       )
 
    return main_layout

@app.callback(
    
    
    dash.dependencies.Output('graph-object','children'),
    
    
    
    [
     dash.dependencies.Input('month','value'),
     dash.dependencies.Input('date','value'),
     dash.dependencies.Input('region','value'),
     dash.dependencies.Input('country','value'),
     dash.dependencies.Input('state','value'),
     dash.dependencies.Input('city','value'),
     dash.dependencies.Input('attack','value'),
     dash.dependencies.Input('year_slider','value'),
     dash.dependencies.Input('Tabs','value'),
     dash.dependencies.Input('subtab1','value'),
     dash.dependencies.Input('subtab2','value')
     
     
     ]
    )
def update_app_ui(month_value, date_value,region_value,country_value,state_value,city_value,attack_value,year_value,tab_value,s1,s2):
    
    
  
    print("Data Type of month value = " ,str(type(month_value)))
    print("Data of month value = " ,month_value)
    print("Data Type of Day value = " ,str(type(date_value)))
    print("Data of Day value = " ,date_value)
    print("Data Type of region value = " ,str(type(region_value)))
    print("Data of region value = " ,region_value)
    print("Data Type of country value = " ,str(type(country_value)))
    print("Data of country value = " ,country_value)
    print("Data Type of state value = " ,str(type(state_value)))
    print("Data of state value = " ,state_value)
    print("Data Type of city value = " ,str(type(city_value)))
    print("Data of city value = " ,city_value)
    print("Data Type of Attack value = " ,str(type(attack_value)))
    print("Data of Attack value = " ,attack_value)
    print("Data Type of year value = " ,str(type(year_value)))
    print("Data of year value = " ,year_value)
    print("Tab value = " ,tab_value)
    print("Subtab1 value = " ,s1)
    print("Subtab2 value = " ,s2)
    
    figure=go.Figure()
    
    if tab_value=="tab-1":
        
    
        # year_filter
        year_range = range(year_value[0], year_value[1]+1)
        # how to filter the data frame 
        # df['iyear'] == 1991
        # new_df = df[df["iyear"]== year_value]  slider
        new_df = df[df["iyear"].isin(year_range)]
    
        # month and date filter
        if month_value is None or month_value==[]:#changes made here
            pass
        else:
            if date_value is None or date_value==[]:
                new_df = new_df[(new_df["imonth"].isin(month_value))&
                        (new_df["iyear"].isin(year_range))]
                            
            else:
                new_df = new_df[(new_df["imonth"].isin(month_value))&
                             (df["iday"].isin(date_value))&
                             (df["iyear"].isin(year_range))]
            
    
        # region, country, state, city filter
        if s1=="tab-1":
            
        
            if region_value is None or region_value==[]:
                pass
            else:
                if country_value is None or country_value==[]:
                    new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["iyear"].isin(year_range))]
                    

           
                        
                else:
                    if state_value is None or state_value==[]:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                (new_df["country_txt"].isin(country_value))&
                                (new_df["iyear"].isin(year_range))]
              
                    else:
                        if city_value is None or city_value==[]:
                            new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                (new_df["country_txt"].isin(country_value)) &
                                (new_df["provstate"].isin(state_value))&
                                 (new_df["iyear"].isin(year_range))]

                        else:
                            new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                (new_df["country_txt"].isin(country_value)) &
                                (new_df["provstate"].isin(state_value))&
                                (new_df["city"].isin(city_value))&
                                 (new_df["iyear"].isin(year_range))]

        elif s1=="tab-2":
            
            
            
            region_value=['South Asia']
            country_value=['India']
           
                
            new_df = new_df[(new_df["region_txt"].isin(['South Asia']))&
                    (new_df["iyear"].isin(year_range))
                    ]
           
                        
                
            if state_value is None or state_value==[]:
                
                new_df = new_df[(new_df["region_txt"].isin(['South Asia']))&
                                 (new_df["country_txt"].isin(['India']))&
                                (new_df["iyear"].isin(year_range))]
                 
                        
            else:
                if city_value is None or city_value==[]:
                    new_df = new_df[(new_df["region_txt"].isin(['South Asia']))&
                                (new_df["country_txt"].isin(['India'])) &
                                (new_df["provstate"].isin(state_value))&
                                 (new_df["iyear"].isin(year_range))]
                    
                else:
                    new_df = new_df[(new_df["region_txt"].isin(['South Asia']))&
                                (new_df["country_txt"].isin(['India'])) &
                                (new_df["provstate"].isin(state_value))&
                                (new_df["city"].isin(city_value))&
                                 (new_df["iyear"].isin(year_range))]
           
        if attack_value is None or attack_value==[]:
            pass
        else:
            new_df=new_df[(new_df["attacktype1_txt"].isin(attack_value))]
                     
     
        if new_df.shape[0]:
            pass
        else:
            new_df=pd.Dataframe(columns=['iyear','imonth','iday','country_txt','region_txt','provstate',
                                     'city','latitude','longitude','attacktype1_txt','nkill'
                                     ])
            new_df.iloc[0]=[0,0,0,None,None,None,None,None,None,None,None]
        
        figure=px.scatter_mapbox(
            new_df,
            lat="latitude",
            lon="longitude",
            color="attacktype1_txt",
            hover_data=["country_txt","provstate","city","nkill","iyear","imonth","iday"],
            
            zoom=1)
       
        figure.update_layout(mapbox_style="open-street-map",
                    autosize=True,
                    margin=dict(l=0, r=0, t=25, b=20),
                  )
        return dcc.Graph(figure=figure)
    
    
    
    
@app.callback(
    dash.dependencies.Output('chart-object','children'),
    [
     dash.dependencies.Input('Tabs','value'),
     dash.dependencies.Input('subtab1','value'),
     dash.dependencies.Input('subtab2','value'),
      dash.dependencies.Input('chart_dropdown','value'),
       dash.dependencies.Input('search','value'),
       dash.dependencies.Input('chart_year_slider','value')

     ]
 
    )    

def update_chart_ui(tab_value,sc1,sc2,chart_dropdown,search,cyear_value):
    
    print("Data Type of tab value = " ,str(type(tab_value)))
    print("Data of Tab value = " ,tab_value)
    print("Data of subtab1 value = " ,sc1)
    print("Data of subtab2 value = " ,sc2)
    
    
    print("Data Type of ChartDropdown value = " ,str(type(chart_dropdown)))
    print("Data of ChartDropdown value = " ,chart_dropdown)
    print("Data Type of Search value = " ,str(type(search)))
    print("Data of Search value = " ,search)
    print("Data Type of Chart Year Slider = " ,str(type(cyear_value)))

    print("Data of Chart Year Slider = " ,cyear_value)
    if tab_value=="tab-2":
        
    
        if sc2=="tab-3":
            
            chart_df = None
            
            cyear_range = range(cyear_value[0], cyear_value[1]+1)
            chart_df = df[df["iyear"].isin(cyear_range)]
            
            if chart_dropdown is not None:
                
                if search is not None: 
                
                    
                    chart_df = chart_df.groupby("iyear")[chart_dropdown].value_counts().reset_index(name = "count")
                    chart_df  = chart_df[chart_df[chart_dropdown].str.contains(search, case = False)]
                else:
                    chart_df = chart_df.groupby("iyear")[chart_dropdown].value_counts().reset_index(name="count")
            else:
                raise PreventUpdate
                
                
        elif sc2=="tab-4":
            chart_df = None
            country_txt="India"
            
            chart_df = df[(df["country_txt"].isin(['India']))]
            
            cyear_range = range(cyear_value[0], cyear_value[1]+1)
            chart_df = chart_df[chart_df["iyear"].isin(cyear_range)]
            
            
            if chart_dropdown is not None:
               
                if search is not None: 

                    chart_df = chart_df.groupby("iyear")[chart_dropdown].value_counts().reset_index(name = "count")

                    
                    
                    chart_df  = chart_df[chart_df[chart_dropdown].str.contains(search, case = False)]
                    
                else:
                    chart_df = chart_df.groupby("iyear")[chart_dropdown].value_counts().reset_index(name="count")
            else:
                raise PreventUpdate
            
        
        
        
                
        if chart_df.shape[0]:
            pass
        else: 
            chart_df = pd.DataFrame(columns = ['iyear', 'count', chart_dropdown])
            #  , chart_dropdown
                
            chart_df.loc[0] = [0, 0,"No data"]
            
                
        fig = px.area(chart_df, x= "iyear", y ="count", color = chart_dropdown)
            
    
        
    return dcc.Graph(figure=fig)

      
    
    
    
    

#   CHAINING CONCEPT
@app.callback(
    dash.dependencies.Output('date','options'),
    [
     dash.dependencies.Input('month','value')
     ]
    )

def update_date(month):
   
    
    if month is None:
        raise PreventUpdate()
    elif(month==[1] or month==[3] or month==[5] or month==[7] or month==[8] or month==[10] or month==[12]):
        date_list1=[x for x in range(1,32)]
        return [{"label":int(x),"value":int(x)} for x in date_list1]
        
  
    elif(month==[4] or month==[6] or month==[9] or month==[11] ):
        date_list2=[x for x in range(1,31)]
        return [{"label":int(x),"value":int(x)} for x in date_list2]
    
    else:
        if(month==[2]):
            date_list3=[x for x in range(1,30)]
            return  [{"label":int(x),"value":int(x)} for x in date_list3] 
           
        
  
    
@app.callback(
    dash.dependencies.Output('region','options'),
    [
     
     dash.dependencies.Input('subtab1','value')
     
     ]
    )  

def set_india_region(s1):
    if s1=="tab-1":
        option=region_list
        return option
    
    elif s1=="tab-2":
        option=['South Asia']
        return [{"label":m,"value":m} for m in option]
    
   
    
@app.callback(
    dash.dependencies.Output('country','options'),
    [
     dash.dependencies.Input('region','value'),
     dash.dependencies.Input('subtab1','value')
     
     ]
    )  
def set_country_options(region,s1) :
    if s1=="tab-1":
        option=[]
        # Making the country Dropdown data
        if region is  None:
            raise PreventUpdate()

        else:
            for var in region:
                if var in country_list.keys():
                    option.extend(country_list[var])
                    
        return [{"label":x,"value":x} for x in option]
    
    elif s1=="tab-2":
        option=['India']
        return  [{"label":m,"value":m} for m in option]



@app.callback(
    dash.dependencies.Output('state','options'),
    [
     dash.dependencies.Input('country','value')
     ]
    )  

def set_state_options(country) :
    
 
    option=[]
    if country is None:
        raise PreventUpdate()
    else:
        for var in country:
            if var in state_list.keys():
                option.extend(state_list[var])
            
    return [{"label":x,"value":x} for x in option]


@app.callback(
    dash.dependencies.Output('city','options'),
    [
     dash.dependencies.Input('state','value')
     
     ]
    )  

 
def set_state_options(state):
   
        
   option=[]
   if state is None:
       raise PreventUpdate()
   else:
       for var in state:
           if var in city_list.keys():
               option.extend(city_list[var])
            
   return [{"label":x,"value":x} for x in option]


def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')


# Main Function
def main():
    print("Starting The MAIN function")
    load_data() 
    print(df.sample(5))
    print(df.sample(1))
    print("Ending The MAIN function")


# Calling Main    
if __name__=="__main__":
        print("Hello and Welcome")
        print("Project is Starting......")
        main()
       
        app.layout=create_app_ui()
        app.title="Terrorism Analysis With Insights"
        
        #facicon.ico
        # create folder in directory>assets>favicon.ico
        
        
        open_browser()
        print("Project is Ending......")
        app.run_server()
        df=None
        app=None
       
