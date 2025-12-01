#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import json
import requests

#######################
# Page configuration
st.set_page_config(
	page_title="Usury Dashboard",
	layout="wide",
	initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
	padding-left: 2rem;
	padding-right: 2rem;
	padding-top: 1rem;
	padding-bottom: 0rem;
	margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
	padding-left: 0rem;
	padding-right: 0rem;
}

[data-testid="stMetric"] {
	background-color: #393939;
	text-align: center;
	padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
	position: relative;
	left: 38%;
	-webkit-transform: translateX(-50%);
	-ms-transform: translateX(-50%);
	transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
	position: relative;
	left: 38%;
	-webkit-transform: translateX(-50%);
	-ms-transform: translateX(-50%);
	transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)


#######################
# Load data
df_reshaped = pd.read_csv('Data/usury_state_data.csv')
print("csv_retrieval complete")
print(df_reshaped)


# Make a GET request to the API
response = requests.get('http://whatdoesthefedsay.com/rate')
fed_rate = 0
# Check if the request was successful
if response.status_code == 200:
    # Parse JSON data
    json_data = response.json()
    fed_rate += round(float(json_data['rate']),2)
else:
    print(f"Error: {response.status_code}")

print("fed_rate:" , fed_rate)
st.markdown("<h1 style='text-align: center;'>Usury Dashboard</h1>", unsafe_allow_html=True)
#######################
# # Sidebar
# with st.sidebar:
# 	st.title('🏂 Usury Limit Dashboard')

# 	color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
# 	selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
# 	selected_year = 2010
# 	df_selected_year = df_reshaped[df_reshaped.year == selected_year]
# 	df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)


#######################
# Plots

# Heatmap
# def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
# 	heatmap = alt.Chart(input_df).mark_rect().encode(
# 			y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
# 			x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
# 			color=alt.Color(f'max({input_color}):Q',
# 							 legend=None,
# 							 scale=alt.Scale(scheme=input_color_theme)),
# 			stroke=alt.value('black'),
# 			strokeWidth=alt.value(0.25),
# 		).properties(width=900
# 		).configure_axis(
# 		labelFontSize=12,
# 		titleFontSize=12
# 		) 
# 	# height=300
# 	return heatmap

# Choropleth map

print('marker')
df_selected_year = df_reshaped
df_selected_year['legal_interest_rate%'] = df_selected_year['legal_interest_rate%'].str.replace('%', '')
df_selected_year['legal_interest_rate%'] = df_selected_year['legal_interest_rate%'].astype(float)
print(df_selected_year['legal_interest_rate%'])
def make_choropleth(input_df, input_id, input_column, input_color_theme):
	choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="USA-states",
							   color_continuous_scale=input_color_theme,
							   range_color=(0, max(df_selected_year['legal_interest_rate%'])),
							   scope="usa",
							  )
	choropleth.update_layout(
		template='plotly_dark',
		plot_bgcolor='rgba(0, 0, 0, 0)',
		paper_bgcolor='rgba(0, 0, 0, 0)',
		margin=dict(l=0, r=0, t=0, b=0),
		height=700
	)
	return choropleth


# Donut chart
def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
	  chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
	  chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
	  chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
	  chart_color = ['#E74C3C', '#781F16']
	
  source = pd.DataFrame({
	  "Topic": ['', input_text],
	  "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
	  "Topic": ['', input_text],
	  "% value": [100, 0]
  })
	
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
	  theta="% value",
	  color= alt.Color("Topic:N",
					  scale=alt.Scale(
						  #domain=['A', 'B'],
						  domain=[input_text, ''],
						  # range=['#29b5e8', '#155F7A']),  # 31333F
						  range=chart_color),
					  legend=None),
  ).properties(width=300, height=130)
	
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
	  theta="% value",
	  color= alt.Color("Topic:N",
					  scale=alt.Scale(
						  # domain=['A', 'B'],
						  domain=[input_text, ''],
						  range=chart_color),  # 31333F
					  legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text


#######################
# Dashboard Main Panel
# col = st.columns((1.5, 4.5, 1), gap='medium')

# with col[0]:
# 	st.markdown('#### Gains/Losses')

# 	df_population_difference_sorted = calculate_population_difference(df_reshaped, selected_year)

# 	if selected_year > 2010:
# 		first_state_name = df_population_difference_sorted.states.iloc[0]
# 		first_state_population = format_number(df_population_difference_sorted.population.iloc[0])
# 		first_state_delta = format_number(df_population_difference_sorted.population_difference.iloc[0])
# 	else:
# 		first_state_name = '-'
# 		first_state_population = '-'
# 		first_state_delta = ''
# 	st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)

# 	if selected_year > 2010:
# 		last_state_name = df_population_difference_sorted.states.iloc[-1]
# 		last_state_population = format_number(df_population_difference_sorted.population.iloc[-1])   
# 		last_state_delta = format_number(df_population_difference_sorted.population_difference.iloc[-1])   
# 	else:
# 		last_state_name = '-'
# 		last_state_population = '-'
# 		last_state_delta = ''
# 	st.metric(label=last_state_name, value=last_state_population, delta=last_state_delta)

# with col[1]:
# st.markdown('#### Total Population')
selected_color_theme = "reds"
choropleth = make_choropleth(df_selected_year, 'state_code', 'legal_interest_rate%', selected_color_theme)
st.plotly_chart(choropleth, use_container_width=True)
	

# with col[2]:
# 	st.markdown('#### Top States')

# 	st.dataframe(df_selected_year_sorted,
# 				 column_order=("states", "population"),
# 				 hide_index=True,
# 				 width=None,
# 				 column_config={
# 					"states": st.column_config.TextColumn(
# 						"States",
# 					),
# 					"population": st.column_config.ProgressColumn(
# 						"Population",
# 						format="%f",
# 						min_value=0,
# 						max_value=max(df_selected_year_sorted.population),
# 					 )}
# 				 )
st.write(f'''- Current Federal Reserve Rate = {fed_rate}%.''')
# with st.expander('About', expanded=True):
# 	st.write(f'''
# 		- Current Federal Reserve Rate = {fed_rate}.
# 		''')