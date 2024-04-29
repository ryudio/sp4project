import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.header("Homicide Reports, 1980-2014")

df = pd.read_csv('./database.zip')

df1 = df.drop(df[df['Perpetrator Sex'] == 'Unknown'].index)
df2 = df1.groupby('Year')['Perpetrator Sex'].value_counts().reset_index()

male_counts = df2[df2['Perpetrator Sex']=='Male']
female_counts = df2[df2['Perpetrator Sex']=='Female']

figb = go.Figure()
figb.add_trace(go.Bar(x=male_counts['Year'], y=male_counts['count'], name='Male', marker_color='blue'))
figb.add_trace(go.Bar(x=female_counts['Year'], y=female_counts['count'], name='Female', marker_color='pink'))
figb.update_layout(title='Perpetrator Sex by Year', xaxis=dict(title='Year'), yaxis=dict(title='Count'), barmode='group')

st.plotly_chart(figb)
del df1, df2, male_counts, female_counts

df['Weapon'] = df['Weapon'].replace(['Rifle', 'Shotgun', 'Handgun'],'Firearm')
df['Weapon'].unique()

df3 = df.drop(df[df['Weapon'] == 'Unknown'].index)
df3 = df3.groupby('Year')['Weapon'].value_counts().reset_index()

figl = px.line(df3, x='Year', y='count', color='Weapon', template='plotly_dark', title='Weapon Used in Homicides 1980-2014')
st.plotly_chart(figl)
del df3

df4 = df.groupby('Year')['State'].value_counts().reset_index()
df4 = df4.groupby('State')['count'].sum().reset_index()

figp = px.pie(df4, values='count', names='State', template='plotly_dark', title='Homicides Documented by State')
figp.update_traces(textposition='inside')
figp.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
st.plotly_chart(figp)
del df4

df5 = df.drop(df[df['Perpetrator Race'] == 'Unknown'].index)
df5 = df5.groupby('Year')['Perpetrator Race'].value_counts().reset_index()

figs = px.scatter(df5, x='Year', y='count', color='Perpetrator Race', template='plotly_dark', title='Perpetrator Race')
st.plotly_chart(figs)
del df5

df['Perpetrator Age'] = df['Perpetrator Age'].replace(' ',0)
df['Perpetrator Age'] = pd.to_numeric(df['Perpetrator Age'], errors='coerce')

df6 = df[df['Weapon']=='Firearm']
df6.drop(df6[df6['Perpetrator Age'] < 5].index, inplace=True)

figh = px.histogram(df6, x='Perpetrator Age', title='Homicide by Firearm 1980-2014')
st.plotly_chart(figh)
del df6

st.subheader("Crime Solved Percentage CA/TX/NY")

option = st.selectbox('Select state', ('California', 'Texas', 'New York'))

stdf = df[df['State']==option]
stdf = stdf['Crime Solved'].value_counts()

figp2 = px.pie(stdf, values=stdf.values, color=stdf.index, template='plotly_dark')
st.plotly_chart(figp2)
del stdf
