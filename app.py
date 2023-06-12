# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import json
import altair as alt
import squarify


st.title('Cancer in the US')


# Load the CSV file
data_path= 'https://raw.githubusercontent.com/marwaajouz/Stramlit_trial/main/General_without_regoin.csv'
data = pd.read_csv(data_path)

#Some Calculations and additions on the dataframe:
# Calculate the percentage change for each unique cancer type
data['Percentage Change'] = data.groupby('Leading Cancer Sites')['Crude Rate'].transform(lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[0] * 100)
#st.write(data)


data['Severity'] = data['Crude Rate'] * data['Percentage Change'] * data['Death Rate (within 5 years)']


# Page Navigation
pages = {
    "Macro Overview": "macro",
    "Pancreas Cancer": "pancreas"
}
page = st.sidebar.radio("Select a page", list(pages.keys()))

if pages[page] == "macro":
    # A dropdown select box for Cancer Types
    cancer_types = data['Leading Cancer Sites'].unique()
    selected_cancer_type = st.selectbox('Select a Cancer Type', cancer_types)

    # Filter the data based on the selected Cancer Type
    filtered_data = data[data['Leading Cancer Sites'] == selected_cancer_type]

    # Filter the data for years 2010 and 2019
    data_2010 = filtered_data[filtered_data['Year'] == 2010]
    data_2019 = filtered_data[filtered_data['Year'] == 2019]

    # Calculate the percentage increase or decrease
    percentage_change = ((data_2019['Crude Rate'].values - data_2010['Crude Rate'].values) / data_2010['Crude Rate'].values) * 100


    # A line plot of Crude Rate across years
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_data['Year'], filtered_data['Crude Rate'])
    plt.xlabel('Year')
    plt.ylabel('Crude Rate')
    plt.title(f'Crude Incidence Rate of {selected_cancer_type} Cancer Across Years 2010 - 2019')

    # Add arrow annotation with percentage change
    for i, value in enumerate(percentage_change):
        arrow_text = f'Percentage Increase: {value:.2f}%'
        plt.annotate(arrow_text, xy=(2019, data_2019['Crude Rate'].values[i]), xytext=(2010, data_2010['Crude Rate'].values[i]-0.03),
                     arrowprops=dict(facecolor='red', arrowstyle='->'), fontsize=8)

    st.pyplot(plt)


    #Heat map for death rate
    filtered_data = data[["Leading Cancer Sites", "Death Rate (within 5 years)"]]
    filtered_data = filtered_data.sort_values(by="Death Rate (within 5 years)", ascending=False)

    #average_death_rate = filtered_data.groupby("Leading Cancer Sites")["Death Rate (within 5 years)"].mean()
    #filtered_data = filtered_data.sort_values(by="Death Rate (within 5 years)", ascending=False)
    pivot_table = filtered_data.pivot_table(index="Leading Cancer Sites", values="Death Rate (within 5 years)")
    pivot_table=pivot_table.sort_values(by="Death Rate (within 5 years)", ascending=False)
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_table, cmap="YlGnBu", annot=True, fmt=".2f")
    plt.title("Average Death Rate by Cancer Type")
    plt.xlabel("Leading Cancer Sites")
    plt.ylabel("")

    st.pyplot(plt)


    # Calculate the percentage change for each unique cancer type
    data['Percentage Change'] = data.groupby('Leading Cancer Sites')['Crude Rate'].transform(lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[0] * 100)
    #st.write(data)


    data['Severity'] = data['Crude Rate'] * data['Percentage Change'] * data['Death Rate (within 5 years)']
    data_2019 = data[data['Year'] == 2019]
    sorted_data = data_2019.sort_values('Severity', ascending=False)


    plt.figure(figsize=(10, 6))
    plt.bar(sorted_data['Leading Cancer Sites'], sorted_data['Severity'])
    plt.xlabel('Cancer Type')
    plt.ylabel('Severity')
    plt.title('Severity of Cancer Types at Year 2019')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)


    plt.figure(figsize=(10, 6))
    plt.scatter(sorted_data['Leading Cancer Sites'], sorted_data['Severity'], s=sorted_data['Severity']*10)
    plt.xlabel('Cancer Type')
    plt.ylabel('Severity')
    plt.title('Severity of Cancer Types at Year 2019')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)

    ##########
    from wordcloud import WordCloud

    wordcloud_data = dict(zip(sorted_data['Leading Cancer Sites'], sorted_data['Severity']))

    plt.figure(figsize=(10, 6))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(wordcloud_data)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Severity of Cancer Types at Year 2019 (Word Cloud)')
    st.pyplot(plt)


    ###################################
    severity_values = sorted_data['Severity']
    cancer_types = sorted_data['Leading Cancer Sites']

    # Create a scatter plot
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(cancer_types, severity_values)

    # Set labels and title
    ax.set_xlabel('Leading Cancer Sites')
    ax.set_ylabel('Severity')
    ax.set_title('Risk Chart')

    # Rotate x-axis labels for better visibility
    plt.xticks(rotation=90)

    # Display the plot using Streamlit
    st.pyplot(fig)
    
if pages[page] == "pancreas":
    st.subheader('Overview of Pancreas Cancer Situation in the US')
    column1, column2 = st.columns(2)
    #number1 = int(metric.values[0])
    
    # Filter the data for Pancreas cancer and year 2010
    filtered_data = data[(data['Leading Cancer Sites'] == 'Pancreas') & (data['Year'] == 2010)]
    
    incidence_2010 = filtered_data['Count'].values[0]
    column1.metric('Pancreas Cancer Incidence in 2010', "{:,.0f}".format(incidence_2010))
    
    crude_rate_2010 = filtered_data['Crude Rate'].values[0]
    column2.metric('Pancreas Cancer Incidence Rate in 2010', crude_rate_2010)
    
    column1, column2 = st.columns(2)
    # Filter the data for Pancreas cancer and year 2019
    filtered_data = data[(data['Leading Cancer Sites'] == 'Pancreas') & (data['Year'] == 2019)]
    
    incidence_2019 = filtered_data['Count'].values[0]
    column1.metric('Pancreas Cancer Incidence in 2019', "{:,.0f}".format(incidence_2019))
    
    crude_rate_2019 = filtered_data['Crude Rate'].values[0]
    column2.metric("Pancreas Cancer Incidence Rate in 2019", crude_rate_2019)
    
    
    column1, column2 = st.columns(2)
    # Filter the data for Pancreas cancer and year 2019
    filtered_data = data[(data['Leading Cancer Sites'] == 'Pancreas') & (data['Year'] == 2019)]
    
    Death_Rate = filtered_data['Death Rate (within 5 years)'].values[0]
    column1.metric('% of Deaths Between Pancrease Cancer Patients', Death_Rate)
    
    Percentage_increaase = filtered_data['Percentage Change'].values[0]
    Severity = Percentage_increaase * Death_Rate * crude_rate_2019
    column2.metric("Calculated Risk", "{:,.0f}".format(Severity))
    
    ########
    data2_path= 'https://raw.githubusercontent.com/marwaajouz/Stramlit_trial/main/PancreasCancer.csv'
    data2 = pd.read_csv(data2_path)
    #st.write(data2)
    data2['Crude Rate'] = data2['Crude Rate'].replace('Missing', 0)
    data2['Crude Rate'] = pd.to_numeric(data2['Crude Rate'], errors='coerce')
    data2['Crude Rate'] = data2['Crude Rate'].fillna(0)
    '''
    m = folium.Map(location=[37, -102], zoom_start=4)
    data3 = data2[(data2['Year'] == 2019)]  
    st.write(data3)
    with open('gz_2010_us_040_00_500k.json') as f:
        geo_data = json.load(f)
    st.write(geo_data)
    folium.Choropleth(
        geo_data=geo_data,  # GeoJSON file containing state boundaries
        name='choropleth',
        data=data3,
        columns=['States', 'Crude Rate'],
        key_on='features.properties.NAME',
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Pancreas Cancer Rate (%)'
    ).add_to(m)
    folium_static(m)
    '''
    
# A sidebar selectbox for state selection
selected_state = st.selectbox('Select a State', data2['States'].unique())

# Filter the data based on the selected state
data_2019 = data2[data2['Year'] == 2019]
filtered_data = data_2019[data_2019['States'] == selected_state]
filtered_data = filtered_data[~filtered_data['Age Groups'].isin(['< 1 year', '1-4 years', '5-9 years'])]

'''
# Create a population pyramid chart using Altair
chart = alt.Chart(filtered_data).mark_bar().encode(
    x='Crude Rate',
    y=alt.Y('Age Groups', sort=alt.EncodingSortField(field='Age Groups', order='ascending'),#'-x'),
    color='Sex',
    column='Sex',
    tooltip=['Age Groups', 'Sex', 'Crude Rate']
).properties(
    width=200,
    height=200
)

chart = chart.resolve_scale(y='independent').configure_view(strokeWidth=0)
# Render the chart using Streamlit
st.altair_chart(chart)#, use_container_width=True)
'''

chart = alt.Chart(filtered_data).mark_bar().encode(
    #x=alt.X('Crude Rate:Q', axis=None),
    x='Crude Rate',
    #y=alt.Y('Age Groups:O', sort=alt.EncodingSortField(field='Age Groups', order='ascending')),# axis=alt.Axis(title='Age Groups')),
    y=alt.Y('Age Groups', sort=alt.EncodingSortField(field='Age Groups', order='ascending')),
    #color='Sex',
    #column='Sex',
    color=alt.Color('Sex:N', scale=alt.Scale(range=['#FF6492', '#6495ED']), legend=alt.Legend(title='Sex')),
    column=alt.Column('Sex:N', header=alt.Header(title=None, labels=False)),
    tooltip=['Age Groups', 'Sex', 'Crude Rate']
).properties(
    width=200,
    height=200
)

# Set the chart layout
#chart = chart.resolve_scale(y='independent').configure_view(strokeWidth=0)

# Show the chart
st.altair_chart(chart)

#####
# Group the data by 'States' and calculate the mean 'Crude Rate' for each state
state_crude_rates = data2.groupby('States')['Crude Rate'].mean().reset_index()

# Sort the states based on the 'Crude Rate' values in descending order
sorted_states = state_crude_rates.sort_values('Crude Rate', ascending=False)

# Display the states with their corresponding 'Crude Rate' values and ranks
sorted_states['Rank'] = sorted_states['Crude Rate'].rank(ascending=False)
#st.write(sorted_states)


########
'''
plt.figure(figsize=(10, 6))
squarify.plot(sizes=sorted_states['Crude Rate'], label=sorted_states['States'], alpha=0.8)
plt.axis('off')
plt.title('Ranking of States by Crude Rate (TreeMap)')
plt.show()
'''
#########

# Filter out rows with zero Crude Rate
filtered_states = sorted_states[sorted_states['Crude Rate'] > 0]

# Create the figure and axes
fig, ax = plt.subplots(figsize=(15, 8))

label_text = [f'{state}\n({cr:.2f})' for state, cr in zip(filtered_states['States'], filtered_states['Crude Rate'])]
# Plot the treemap using squarify
squarify.plot(sizes=filtered_states['Crude Rate'], label=label_text, alpha=0.8, ax=ax)#filtered_states['States']
# Configure the plot
ax.axis('off')
ax.set_title('Ranking of States by Crude Rate (TreeMap)')
# Display the plot in Streamlit
st.pyplot(fig)

# Load the CSV file
data4_path= 'https://raw.githubusercontent.com/marwaajouz/Stramlit_trial/main/Pancreas_Cancer_Race.csv'
data4 = pd.read_csv(data4_path)

selected_year = st.sidebar.selectbox('Select a Year', data4['Year'].unique())
filtered_data = data4[(data4['Year'] == selected_year) & (~data4['Race'].isin(['Other Races and Unknown combined']))]

plt.figure(figsize=(10, 6))
sns.barplot(data=filtered_data, x='Race', y='Crude Rate', hue='Sex')
plt.xlabel('Race')
plt.ylabel('Crude Rate')
plt.title(f'Crude Rate by Race for Year {selected_year}')
plt.xticks(rotation=45)
plt.legend()
st.pyplot(plt)



    
    
    
