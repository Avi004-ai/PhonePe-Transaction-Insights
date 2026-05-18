import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json
mydb=psycopg2.connect(
    host="localhost",
    user="postgres",
    port="5432",
    database="phonepe-project",
    password="Avinab@post27"
)

cursor=mydb.cursor()

cursor.execute("select * from aggr_insurance")
mydb.commit()
table1=cursor.fetchall()
aggre_insurance=pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

cursor.execute("select * from aggr_transaction")
mydb.commit()
table2=cursor.fetchall()
aggre_transaction=pd.DataFrame(table2,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

cursor.execute("select * from aggr_user")
mydb.commit()
table3=cursor.fetchall()
aggre_user=pd.DataFrame(table3,columns=("States","Years","Quarter","Brand","Transaction_count","Percentage"))

cursor.execute("select * from map_insurance")
mydb.commit()
table4=cursor.fetchall()
map_insurance=pd.DataFrame(table4,columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

cursor.execute("select * from map_transaction")
mydb.commit()
table5=cursor.fetchall()
map_transaction=pd.DataFrame(table5,columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

cursor.execute("select * from map_user")
mydb.commit()
table6=cursor.fetchall()
map_user=pd.DataFrame(table6,columns=("States","Years","Quarter","Districts","RegisteredUsers","AppOpens"))

cursor.execute("select * from top_insurance")
mydb.commit()
table7=cursor.fetchall()
top_insurance=pd.DataFrame(table7,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))

cursor.execute("select * from top_transaction")
mydb.commit()
table8=cursor.fetchall()
top_transaction=pd.DataFrame(table8,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))

cursor.execute("select * from top_users")
mydb.commit()
table9=cursor.fetchall()
top_users=pd.DataFrame(table9,columns=("States","Years","Quarter","Pincodes","RegisteredUsers"))


def Transaction_amount_count_Y(df,year):
 tacy=df[df["Years"]== year]
 tacy.reset_index(drop=True,inplace=True)

 tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
 tacyg.reset_index(inplace=True) 

 col1,col2=st.columns(2) 
 with col1:
    fig_amount=px.bar(tacyg,x="States",y="Transaction_amount",title=f"{year}Transaction Amount",color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
    st.plotly_chart(fig_amount)
 with col2:
    fig_count=px.bar(tacyg,x="States",y="Transaction_count",title=f"{year}Transaction Count",color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
    st.plotly_chart(fig_count)

 url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
 response=requests.get(url)
 data1=json.loads(response.content)
 states_name=[]
 for feature in data1["features"]:
  states_name.append(feature["properties"]["ST_NM"])
 states_name.sort()
 fig_india_1=px.choropleth(tacyg,geojson=data1,featureidkey="properties.ST_NM",color="Transaction_amount",color_continuous_scale="Rainbow",locations="States",
                    range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),hover_name="States",title=f"{year} TRANSACTION AMOUNT",fitbounds="locations",
                    height=600,width=600)
 st.plotly_chart(fig_india_1)
 fig_india_2=px.choropleth(tacyg,geojson=data1,featureidkey="properties.ST_NM",color="Transaction_count",color_continuous_scale="Rainbow",locations="States",
                    range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),hover_name="States",title=f"{year} TRANSACTION COUNT",fitbounds="locations",
                    height=600,width=600)
 st.plotly_chart(fig_india_2)
 return tacy
 
def Transaction_amount_count_Y_Q(df,quarter):
 tacy=df[df["Quarter"]== quarter]
 tacy.reset_index(drop=True,inplace=True)

 tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
 tacyg.reset_index(inplace=True) 
 fig_amount=px.bar(tacyg,x="States",y="Transaction_amount",title=f"{tacy['Years'].unique()} YEAR {quarter} Quater Transaction Amount",color_discrete_sequence=px.colors.sequential.Aggrnyl)
 fig_count=px.bar(tacyg,x="States",y="Transaction_count",title=f"{tacy['Years'].unique()} YEAR {quarter} Quater Transaction Count",color_discrete_sequence=px.colors.sequential.Bluered_r)
 col1,col2=st.columns(2) 
 with col1:
  st.plotly_chart(fig_amount)
 with col2:
  st.plotly_chart(fig_count)
 url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
 response=requests.get(url)
 data1=json.loads(response.content)
 states_name=[]
 for feature in data1["features"]:
    states_name.append(feature["properties"]["ST_NM"])
 states_name.sort()
 fig_india_1=px.choropleth(tacyg,geojson=data1,featureidkey="properties.ST_NM",color="Transaction_amount",color_continuous_scale="Rainbow",locations="States",
                        range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),hover_name="States",title=f"{tacy['Years'].unique()} YEAR {quarter} Quater TRANSACTION AMOUNT",fitbounds="locations",
                        height=600,width=600)
 st.plotly_chart(fig_india_1)
 fig_india_2=px.choropleth(tacyg,geojson=data1,featureidkey="properties.ST_NM",color="Transaction_count",color_continuous_scale="Rainbow",locations="States",
                        range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),hover_name="States",title=f"{tacy['Years'].unique()} YEAR {quarter} Quater TRANSACTION COUNT",fitbounds="locations",
                        height=600,width=600)
 st.plotly_chart(fig_india_2)
 return tacy

def Aggre_Tran_Trasaction_type(df,state):
    tacy=df[df["States"]== state]
    tacy.reset_index(drop=True,inplace=True)
    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True) 
    col1,col2=st.columns(2)
    with col1:
        fig_pie_1=px.pie(data_frame=tacyg,names="Transaction_type",values="Transaction_amount",width=600,title=f"{state} TRANSACTION AMOUNT",hole=0.5)
        st.plotly_chart(fig_pie_1)
    with col2:
        fig_pie_2=px.pie(data_frame=tacyg,names="Transaction_type",values="Transaction_count",width=600,title=f"{state} TRANSACTION COUNT",hole=0.5)
        st.plotly_chart(fig_pie_2)

def Aggre_User_Plot_1(df,year):
    aguy=df[df["Years"]==year]
    aguy.reset_index(drop=True,inplace=True)
    aguyg=pd.DataFrame(aguy.groupby("Brand")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)
    fig_bar_1=px.bar(aguyg,x="Brand",y="Transaction_count",title=f"{aguy['Years'].unique()} USER TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Darkmint)
    st.plotly_chart(fig_bar_1)
    return aguy

def Aggre_User_Plot_2(df,quarter):
    aguyq=df[df["Quarter"]==quarter]
    aguyq.reset_index(drop=True,inplace=True)
    aguyqg=pd.DataFrame(aguyq.groupby("Brand")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)
    fig_bar_1=px.bar(aguyqg,x="Brand",y="Transaction_count",title=f"{aguyq['Years'].unique()} YEAR {aguyq['Quarter'].unique()} QUARTER TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Darkmint)
    st.plotly_chart(fig_bar_1)
    return aguyq

def Aggre_User_Plot_3(df, state):
    auyqs= df[df["States"] == state]
    auyqs.reset_index(drop= True, inplace= True)

    fig_line_1= px.line(auyqs, x= "Brand", y= "Transaction_count", hover_data= "Percentage",
                        title= f"{state.upper()}  BRANDS, TRANSACTION COUNT, PERCENTAGE",width= 1000, markers= True)
    st.plotly_chart(fig_line_1)

def Map_insur_District(df,state):
    tacy=df[df["States"]== state]
    tacy.reset_index(drop=True,inplace=True)
    tacyg=tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True) 
    col1,col2=st.columns(2)
    with col1:
     fig_bar_1=px.bar(data_frame=tacyg,x="Transaction_amount",y="Districts",height=600,orientation='h',title=f"{state.upper()} TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Aggrnyl)
     st.plotly_chart(fig_bar_1)
    with col2:
     fig_bar_2=px.bar(data_frame=tacyg,x="Transaction_count",y="Districts",height=600,orientation='h',title=f"{state.upper()} TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Bluered_r)
     st.plotly_chart(fig_bar_2)

def Map_User_Plot_1(df,year):
    muy=map_user[map_user["Years"]==year]
    muy.reset_index(drop=True,inplace=True)
    muyg=muy.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    muyg.reset_index(inplace=True)
    fig_line_1=px.line(muyg,x="States",y=["RegisteredUsers","AppOpens"],title=f"{muy['Years'].unique()} YEAR REGISTERED USERS & APPOPENS",markers=True,width=1000)
    st.plotly_chart(fig_line_1)

    return muy

def Map_User_Plot_2(df,quarter):
    muyq=df[df["Quarter"]==quarter]
    muyq.reset_index(drop=True,inplace=True)
    muyqg=pd.DataFrame(muyq.groupby("States")[["RegisteredUsers","AppOpens"]].sum())
    muyqg.reset_index(inplace=True)
    fig_line_1=px.line(muyqg,x="States",y=["RegisteredUsers","AppOpens"],title=f"{muyq['Years'].unique()} YEAR {muyq['Quarter'].unique()} QUARTER REGISTERED USERS & APPOPENS",markers=True,width=1000)
    st.plotly_chart(fig_line_1)
    return muyq

def Map_User_Plot_3(df, state):
    muyqs= df[df["States"] == state]
    muyqs.reset_index(drop= True, inplace= True)
    col1,col2=st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(muyqs, x= "RegisteredUsers", y= "Districts",orientation='h', title= f"{state.upper()} DISTRICTS, REGISTERED USERS", width= 1000)
        st.plotly_chart(fig_map_bar_1)
    with col2:
        fig_map_bar_2= px.bar(muyqs, x= "AppOpens", y= "Districts",orientation='h', title= f"{state.upper()} DISTRICTS, APP OPENS", width= 1000)
        st.plotly_chart(fig_map_bar_2)

def Top_insur_Plot_1(df,state):
    tiy=df[df["States"]==state]
    tiy.reset_index(drop=True,inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig_top_isur_bar_1=px.bar(tiy,x="Quarter",y="Transaction_amount",title=f"{state} INSURANCE TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Aggrnyl,hover_data="Pincodes")
        st.plotly_chart(fig_top_isur_bar_1)
    with col2:
        fig_top_isur_bar_1=px.bar(tiy,x="Quarter",y="Transaction_count",title=f"{state} INSURANCE TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Bluered_r,hover_data="Pincodes")
        st.plotly_chart(fig_top_isur_bar_1)

def top_user_plot_1(df,year):
    tuy=top_users[top_users["Years"]==year]
    tuy.reset_index(drop=True,inplace=True)
    tuyg=pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)
    fig_top_plot_1=px.bar(tuyg,x="States",y="RegisteredUsers",color="Quarter",title=f"{year} YEAR REGISTERED USERS", width=1000,height=800,color_discrete_sequence=px.colors.sequential.Burgyl,hover_name="States")
    st.plotly_chart(fig_top_plot_1)
    return tuy

def top_user_plot_2(df,states):
    tuys=df[df["States"]==states]
    tuys.reset_index(drop=True,inplace=True)
    fig_top_plot_2=px.bar(tuys,x="Quarter",y="RegisteredUsers",title=f"REGISTEREDUSERS,PINCODES,QUARTER",width=1000,height=800,hover_name="Pincodes",color_continuous_scale=px.colors.sequential.Magenta,color="RegisteredUsers")
    st.plotly_chart(fig_top_plot_2)

#Top Charts

def top_chart_transaction_amount(table_name):
    mydb=psycopg2.connect(
        host="localhost",
        user="postgres",
        port="5432",
        database="phonepe-project",
        password="Avinab@post27"
    )
    cursor=mydb.cursor()
    query=f'''Select states, sum(transaction_amount) as transaction_amount from {table_name} 
    group by states 
    order by transaction_amount 
    desc limit 10;'''
    cursor.execute(query)
    table1=cursor.fetchall()
    mydb.commit()
    df1=pd.DataFrame(table1,columns=["States","Transaction_amount"])

    query2=f'''select states, sum(transaction_amount) as transaction_amount from {table_name} 
    group by states 
    order by transaction_amount 
    limit 10;'''
    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()
    df2=pd.DataFrame(table2,columns=["States","Transaction_amount"])

    col1,col2=st.columns(2)
    with col1:
        fig1=px.bar(df1,x="States",y="Transaction_amount",title=f"Top 10 states by transaction amount in {table_name}",color_discrete_sequence=px.colors.sequential.Aggrnyl,height= 650,width= 600)
        st.plotly_chart(fig1)
    with col2:
        fig2=px.bar(df2,x="States",y="Transaction_amount",title=f"Bottom 10 states by transaction amount in {table_name}",color_discrete_sequence=px.colors.sequential.Bluered_r,height= 650,width= 600 )
        st.plotly_chart(fig2)

    query3=f'''select states,avg(transaction_amount) as transaction_amount from {table_name} 
    group by states 
    order by transaction_amount;'''
    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()
    df3=pd.DataFrame(table3,columns=["States","Transaction_amount"])
    fig3=px.bar(df3,x="Transaction_amount",y="States",title=f"Average transaction amount by states in {table_name}",color_discrete_sequence=px.colors.sequential.Rainbow,height= 650,width= 1000,orientation="h")
    st.plotly_chart(fig3)

def top_chart_transaction_count(table_name):
    mydb=psycopg2.connect(
        host="localhost",
        user="postgres",
        port="5432",
        database="phonepe-project",
        password="Avinab@post27"
    )
    cursor=mydb.cursor()
    query=f'''Select states, sum(transaction_count) as transaction_count from {table_name} 
    group by states 
    order by transaction_count 
    desc limit 10;'''
    cursor.execute(query)
    table1=cursor.fetchall()
    mydb.commit()
    df1=pd.DataFrame(table1,columns=["States","Transaction_count"])

    query2=f'''select states, sum(transaction_count) as transaction_count from {table_name} 
    group by states 
    order by transaction_count 
    limit 10;'''
    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()
    df2=pd.DataFrame(table2,columns=["States","Transaction_count"])

    col1,col2=st.columns(2)
    with col1:
        fig1=px.bar(df1,x="States",y="Transaction_count",title=f"Top 10 states by transaction count in {table_name}",color_discrete_sequence=px.colors.sequential.Aggrnyl,height= 650,width= 600)
        st.plotly_chart(fig1)
    with col2:
        fig2=px.bar(df2,x="States",y="Transaction_count",title=f"Bottom 10 states by transaction count in {table_name}",color_discrete_sequence=px.colors.sequential.Bluered_r,height= 650,width= 600 )
        st.plotly_chart(fig2)

    query3=f'''select states,avg(transaction_count) as transaction_count from {table_name} 
    group by states 
    order by transaction_count;'''
    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()
    df3=pd.DataFrame(table3,columns=["States","Transaction_count"])
    fig3=px.bar(df3,x="Transaction_count",y="States",title=f"Average transaction count by states in {table_name}",color_discrete_sequence=px.colors.sequential.Rainbow,height= 650,width= 1000,orientation="h")
    st.plotly_chart(fig3)

def top_chart_registered_users(table_name,state):
    mydb=psycopg2.connect(
        host="localhost",
        user="postgres",
        port="5432",
        database="phonepe-project",
        password="Avinab@post27"
    )
    cursor=mydb.cursor()
    query=f'''Select districts, sum(registeredusers) as registered_users from {table_name} 
    where states='{state}'
    group by districts
    order by registered_users 
    desc limit 10;'''
    cursor.execute(query)
    table1=cursor.fetchall()
    mydb.commit()
    df1=pd.DataFrame(table1,columns=["Districts","Registered_Users"])

    query2=f'''select districts, sum(registeredusers) as registered_users from {table_name} 
    where states='{state}'
    group by districts
    order by registered_users 
    limit 10;'''
    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()
    df2=pd.DataFrame(table2,columns=["Districts","Registered_Users"])

    col1,col2=st.columns(2)
    with col1:
        fig1=px.bar(df1,x="Districts",y="Registered_Users",title=f"Top 10 districts by registered users in {state}",color_discrete_sequence=px.colors.sequential.Aggrnyl,height= 650,width= 600)
        st.plotly_chart(fig1)
    with col2:
        fig2=px.bar(df2,x="Districts",y="Registered_Users",title=f"Bottom 10 districts by registered users in {state}",color_discrete_sequence=px.colors.sequential.Bluered_r,height= 650,width= 600 )
        st.plotly_chart(fig2)

    query3=f'''select districts,avg(registeredusers) as registered_users from {table_name} 
    where states='{state}'
    group by districts 
    order by registered_users;'''
    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()
    df3=pd.DataFrame(table3,columns=["Districts","Registered_Users"])
    fig3=px.bar(df3,x="Registered_Users",y="Districts",title=f"Average registered users by districts in {state}",color_discrete_sequence=px.colors.sequential.Rainbow,height= 650,width= 1000,orientation="h")
    st.plotly_chart(fig3)

def top_chart_AppOpens(table_name,state):
    mydb=psycopg2.connect(
        host="localhost",
        user="postgres",
        port="5432",
        database="phonepe-project",
        password="Avinab@post27"
    )
    cursor=mydb.cursor()
    query=f'''Select districts, sum(appOpens) as app_opens from {table_name} 
    where states='{state}'
    group by districts 
    order by app_opens 
    desc limit 10;'''
    cursor.execute(query)
    table1=cursor.fetchall()
    mydb.commit()
    df1=pd.DataFrame(table1,columns=["Districts","App_Opens"])

    query2=f'''select districts, sum(appOpens) as app_opens from {table_name} 
    where states='{state}'
    group by districts 
    order by app_opens 
    limit 10;'''
    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()
    df2=pd.DataFrame(table2,columns=["Districts","App_Opens"])

    col1,col2=st.columns(2)
    with col1:
        fig1=px.bar(df1,x="Districts",y="App_Opens",title=f"Top 10 districts by app opens in {table_name}",color_discrete_sequence=px.colors.sequential.Aggrnyl,height= 650,width= 600)
        st.plotly_chart(fig1)
    with col2:
        fig2=px.bar(df2,x="Districts",y="App_Opens",title=f"Bottom 10 districts by app opens in {table_name}",color_discrete_sequence=px.colors.sequential.Bluered_r,height= 650,width= 600 )
        st.plotly_chart(fig2)

    query3=f'''select districts,avg(appOpens) as app_opens from {table_name} 
    where states='{state}'
    group by districts 
    order by app_opens;'''
    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()
    df3=pd.DataFrame(table3,columns=["Districts","App_Opens"])
    fig3=px.bar(df3,x="App_Opens",y="Districts",title=f"Average app opens by districts in {state}",color_discrete_sequence=px.colors.sequential.Rainbow,height= 650,width= 1000,orientation="h")
    st.plotly_chart(fig3)


def top_chart_registered_users_by_top(table_name):
    mydb=psycopg2.connect(
        host="localhost",
        user="postgres",
        port="5432",
        database="phonepe-project",
        password="Avinab@post27"
    )
    cursor=mydb.cursor()
    query=f'''Select states, sum(registeredusers) as registered_users 
    from {table_name} 
    group by states 
    order by registered_users 
    desc 
    limit 10'''
    cursor.execute(query)
    table1=cursor.fetchall()
    mydb.commit()
    df1=pd.DataFrame(table1,columns=["States","Registered_Users"])

    query2=f'''select states, sum(registeredusers) as registered_users 
    from {table_name} 
    group by states 
    order by registered_users 
    limit 10'''
    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()
    df2=pd.DataFrame(table2,columns=["States","Registered_Users"])
    col1,col2=st.columns(2)
    with col1:
        fig1=px.bar(df1,x="States",y="Registered_Users",title=f"Top 10 states by registered users in {table_name}",color_discrete_sequence=px.colors.sequential.Aggrnyl,height= 650,width= 600)
        st.plotly_chart(fig1)
    with col2:
        fig2=px.bar(df2,x="States",y="Registered_Users",title=f"Bottom 10 states by registered users in {table_name}",color_discrete_sequence=px.colors.sequential.Bluered_r,height= 650,width= 600 )
        st.plotly_chart(fig2)

    query3=f'''select states,avg(registeredusers) as registered_users 
    from {table_name} 
    group by states 
    order by registered_users'''
    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()
    df3=pd.DataFrame(table3,columns=["States","Registered_Users"])
    fig3=px.bar(df3,x="Registered_Users",y="States",title=f"Average registered users by state in {table_name}",color_discrete_sequence=px.colors.sequential.Rainbow,height= 650,width= 1000,orientation="h")
    st.plotly_chart(fig3)

# Streamlit part

st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLAINATION")

with st.sidebar:
    select = option_menu("Main Menu", ["HOME", "DATA EXPLORATION", "TOP CHARTS"])


if select == "HOME":
    st.write("Welcome to PhonePe Data Visualization Dashboard")
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        phonepe_url = (
            "https://www.phonepe.com/app-download/"
            "?shortlink=2kk1w03o"
            "&c=consumer_app_icon"
            "&pid=PPWeb_app_download_page"
            "&af_xp=custom"
            "&source_caller=ui"
        )
        st.link_button(
        label="📱 Download PhonePe App",
        url=phonepe_url,
        use_container_width=True
        )
    with col2:
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzvsLe12D-ihkNmcJM0-pBV-DjZQy9NmNzeQ&s",width=600)

    col3,col4= st.columns(2)
    
    with col3:
        st.image("https://www.phonepe.com/webstatic/13941/static/2066bae038a366a4b54e0a3e22f6fa4e/dcd6b/PhonePe-Press-3-2.png",width=600)

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.video("https://youtu.be/_andnIwLKDk?si=DpX1Yabpc3SUTN21&autoplay=1")

elif select == "DATA EXPLORATION":

    tab1, tab2, tab3 = st.tabs(
        ["Aggregated Analysis", "Map Analysis", "Top Analysis"]
    )


    with tab1:
        method = st.radio(
            "Select a Method",
            ["Insurace Analysis", "Transaction Analysis", "User Analysis"]
        )

        if method == "Insurace Analysis":
            col1,col2=st.columns(2)
            with col1:
                years = st.slider(
                    "Select the year",
                    int(aggre_insurance["Years"].min()),
                    int(aggre_insurance["Years"].max()),
                    int(aggre_insurance["Years"].min())
                )
            tac_Y=Transaction_amount_count_Y(aggre_insurance, years)
            with col2:
               quarters = st.slider(
                    "Select the quarter",
                    int(aggre_insurance["Quarter"].min()),
                    int(aggre_insurance["Quarter"].max()),
                    int(aggre_insurance["Quarter"].min())
                )
            Transaction_amount_count_Y_Q(tac_Y, quarters)

        elif method == "Transaction Analysis":
            col1,col2=st.columns(2)
            with col1:
                years = st.slider(
                    "Select the year",
                    int(aggre_transaction["Years"].min()),
                    int(aggre_transaction["Years"].max()),
                    int(aggre_transaction["Years"].min())
                )
            aggre_tran_tac_Y=Transaction_amount_count_Y(aggre_transaction, years)
            col1,col2=st.columns(2)
            with col1:
               states=st.selectbox("Select the State",aggre_tran_tac_Y["States"].unique())
            Aggre_Tran_Trasaction_type(aggre_tran_tac_Y,states)
            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter",aggre_tran_tac_Y["Quarter"].min(),aggre_tran_tac_Y["Quarter"].max(),aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q= Transaction_amount_count_Y_Q(aggre_tran_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_Ty", Aggre_tran_tac_Y_Q["States"].unique())

            Aggre_Tran_Trasaction_type(Aggre_tran_tac_Y_Q, states)
        elif method == "User Analysis":
             col1,col2=st.columns(2)
             with col1:
                    years = st.slider(
                        "Select the year",
                        int(aggre_user["Years"].min()),
                        int(aggre_user["Years"].max()),
                        int(aggre_user["Years"].min())
                    )
            
             Aggre_user_Y=Aggre_User_Plot_1(aggre_user, years)
             col1,col2= st.columns(2)
             with col1:
                quarters= st.slider("Select The Quarter",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
             Aggre_user_Y_Q=Aggre_User_Plot_2(Aggre_user_Y, quarters)
             col1,col2=st.columns(2)
             with col1:
               states=st.selectbox("Select the State",Aggre_user_Y_Q["States"].unique())
             Aggre_User_Plot_3(Aggre_user_Y_Q, states)

    with tab2:
        method_2 = st.radio(
            "Select a Method",
            ["Map Insurance", "Map Transaction", "Map User"]
        )

        if method_2 == "Map Insurance":
            col1,col2=st.columns(2)
            with col1:
                years = st.slider(
                    "Select the year",
                    int(map_insurance["Years"].min()),
                    int(map_insurance["Years"].max()),
                    int(map_insurance["Years"].min()),
                    key="map_insurance_year_slider"
                )
            map_insur_tac_Y=Transaction_amount_count_Y(map_insurance, years)
            col1,col2=st.columns(2)
            with col1:
               states=st.selectbox("Select the State",map_insur_tac_Y["States"].unique())
            Map_insur_District(map_insur_tac_Y,states)
            col1,col2= st.columns(2)
            with col1:
                quarters= st.slider("Select The Quarter",map_insur_tac_Y["Quarter"].min(),map_insur_tac_Y["Quarter"].max(),map_insur_tac_Y["Quarter"].min())
            map_insur_tac_Y_Q=Transaction_amount_count_Y_Q(map_insur_tac_Y, quarters)
            col1,col2=st.columns(2)
            with col1:
               states=st.selectbox("Select the State",map_insur_tac_Y_Q["States"].unique(),key="map_insurance_state_selectbox")
            Map_insur_District(map_insur_tac_Y_Q, states)
        elif method_2 == "Map Transaction":
            col1,col2=st.columns(2)
            with col1:
                    years = st.slider(
                        "Select the year",
                        int(map_transaction["Years"].min()),
                        int(map_transaction["Years"].max()),
                        int(map_transaction["Years"].min())
                    )
            Map_tran_tac_Y=Transaction_amount_count_Y(map_transaction, years)
            col1,col2=st.columns(2)
            with col1:
               states=st.selectbox("Select the State",Map_tran_tac_Y["States"].unique())
            Map_insur_District(Map_tran_tac_Y,states)
            col1,col2= st.columns(2)
            with col1:
                quarters= st.slider("Select The Quarter",Map_tran_tac_Y["Quarter"].min(),Map_tran_tac_Y["Quarter"].max(),Map_tran_tac_Y["Quarter"].min())
            Map_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Map_tran_tac_Y, quarters)
            col1,col2=st.columns(2)
            with col1:
               states=st.selectbox("Select the State",Map_tran_tac_Y_Q["States"].unique(),key="map_transaction_state_selectbox")
            Map_insur_District(Map_tran_tac_Y_Q, states)
        elif method_2 == "Map User":
                col1,col2=st.columns(2)
                with col1:
                    years = st.slider(
                        "Select the year",
                        int(map_user["Years"].min()),
                        int(map_user["Years"].max()),
                        int(map_user["Years"].min())
                    )
                Map_user_Y=Map_User_Plot_1(map_user, years)
                col1,col2= st.columns(2)
                with col1:
                    quarters= st.slider("Select The Quarter for Map",Map_user_Y["Quarter"].min(),Map_user_Y["Quarter"].max(),Map_user_Y["Quarter"].min())
                Map_user_Y_Q=Map_User_Plot_2(Map_user_Y, quarters)
                col1,col2=st.columns(2)
                with col1:
                 states=st.selectbox("Select the State for Map",Map_user_Y_Q["States"].unique())
                Map_User_Plot_3(Map_user_Y_Q, states)
    with tab3:
        method_3 = st.radio(
            "Select a Method",
            ["Top Insurance", "Top Transaction", "Top User"]
        )

        if method_3 == "Top Insurance":
            col1,col2=st.columns(2)
            with col1:
                years = st.slider(
                    "Select the year for top",
                    int(top_insurance["Years"].min()),
                    int(top_insurance["Years"].max()),
                    int(top_insurance["Years"].min()),
                )
            top_insur_tac_Y=Transaction_amount_count_Y(top_insurance, years)
            col1,col2=st.columns(2)
            with col1:
               states=st.selectbox("Select the State for Top Insurance",top_insur_tac_Y["States"].unique())
            Top_insur_Plot_1(top_insur_tac_Y, states)
            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter for Top Insurance",top_insur_tac_Y["Quarter"].min(),top_insur_tac_Y["Quarter"].max(),top_insur_tac_Y["Quarter"].min())
            Top_insur_tac_Y_Q= Transaction_amount_count_Y_Q(top_insur_tac_Y, quarters)
        elif method_3 == "Top Transaction":
            col1,col2=st.columns(2)
            with col1:
                years = st.slider(
                    "Select the year for top",
                    int(top_transaction["Years"].min()),
                    int(top_transaction["Years"].max()),
                    int(top_transaction["Years"].min()),
                )
            top_tran_tac_Y=Transaction_amount_count_Y(top_transaction, years)
            col1,col2=st.columns(2)
            with col1:
               states=st.selectbox("Select the State for Top Transaction",top_tran_tac_Y["States"].unique())
            Top_insur_Plot_1(top_tran_tac_Y, states)
            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter for Top Transaction",top_tran_tac_Y["Quarter"].min(),top_tran_tac_Y["Quarter"].max(),top_tran_tac_Y["Quarter"].min())
            Top_tran_tac_Y_Q= Transaction_amount_count_Y_Q(top_tran_tac_Y, quarters)
        elif method_3 == "Top User":
            col1,col2=st.columns(2)
            with col1:
                years = st.slider(
                    "Select the year for top",
                    int(top_users["Years"].min()),
                    int(top_users["Years"].max()),
                    int(top_users["Years"].min()),
                )
            top_user_Y=top_user_plot_1(top_users, years)
            col1,col2=st.columns(2)
            with col1:
               states=st.selectbox("Select the State",top_user_Y["States"].unique())
            top_user_plot_2(top_user_Y, states)


elif select == "TOP CHARTS":
    question= st.selectbox("Select the Topchart",["1. Transaction Amount and Count of Aggregated Insurance",
                                                    "2. Transaction Amount and Count of Map Insurance",
                                                    "3. Transaction Amount and Count of Top Insurance",
                                                    "4. Transaction Amount and Count of Aggregated Transaction",
                                                    "5. Transaction Amount and Count of Map Transaction",
                                                    "6. Transaction Amount and Count of Top Transaction",
                                                    "7. Transaction Count of Aggregated User",
                                                    "8. Registered users of Map User",
                                                    "9. App opens of Map User",
                                                    "10. Registered users of Top User",
                                                    ])
    if question == "1. Transaction Amount and Count of Aggregated Insurance":
        st.subheader("Transaction Amount")
        top_chart_transaction_amount("aggr_insurance")
        st.subheader("Transaction Count")
        top_chart_transaction_count("aggr_insurance")
    elif question=="2. Transaction Amount and Count of Map Insurance":
        st.subheader("Map Insurance Transaction Amount")
        top_chart_transaction_amount("map_insurance")
        st.subheader("Map Insurance Transaction Count")
        top_chart_transaction_count("map_insurance")
    elif question=="3. Transaction Amount and Count of Top Insurance":
        st.subheader("Top Insurance Transaction Amount")
        top_chart_transaction_amount("top_insurance")
        st.subheader("Top Insurance Transaction Count")
        top_chart_transaction_count("top_insurance")
    elif question=="4. Transaction Amount and Count of Aggregated Transaction":
        st.subheader("Aggregated Transaction Amount")
        top_chart_transaction_amount("aggr_transaction")
        st.subheader("Aggregated Transaction Count")
        top_chart_transaction_count("aggr_transaction")
    elif question=="5. Transaction Amount and Count of Map Transaction":
        st.subheader("Map Transaction Amount")
        top_chart_transaction_amount("map_transaction")
        st.subheader("Map Transaction Count")
        top_chart_transaction_count("map_transaction")
    elif question=="6. Transaction Amount and Count of Top Transaction":
        st.subheader("Top Transaction Amount")
        top_chart_transaction_amount("top_transaction")
        st.subheader("Top Transaction Count")
        top_chart_transaction_count("top_transaction")
    elif question=="7. Transaction Count of Aggregated User":
        st.subheader("Aggregated User Transaction Count")
        top_chart_transaction_count("aggr_user")
    elif question=="8. Registered users of Map User":
        st.subheader("Registered users of Map User")
        col1,col2=st.columns(2)
        with col1:
            states=st.selectbox("Select the State for RegisteredUsers by District",map_user["States"].unique())
        top_chart_registered_users("map_user",states)
    elif question=="9. App opens of Map User":
        st.subheader("App Opens of Map User")
        col1,col2=st.columns(2)
        with col1:
            states=st.selectbox("Select the State for AppOpens by District",map_user["States"].unique())
        top_chart_AppOpens("map_user",states)
    elif question=="10. Registered users of Top User":
        st.subheader("Registered users of Top User")
        top_chart_registered_users_by_top("top_users")

