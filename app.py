# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import json
import altair as alt
import squarify
import matplotlib.cm as cm
from wordcloud import WordCloud



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
    st.subheader('Analysis of Cancer Cases in the Unied States of America - General Overview')
    # A dropdown select box for Cancer Types


    
    cancer_types = data['Leading Cancer Sites'].unique()
    selected_cancer_type = st.selectbox('Select a Cancer Type', cancer_types)

    data_2010_ = data[data['Year'] == 2010]
    data_2019_ = data[data['Year'] == 2019]
    percentage_change_ = ((data_2019_['Crude Rate'].values - data_2010_['Crude Rate'].values) / data_2010_['Crude Rate'].values) * 100
    
    # Filter the data based on the selected Cancer Type
    filtered_data = data[data['Leading Cancer Sites'] == selected_cancer_type]

    # Filter the data for years 2010 and 2019
    data_2010 = filtered_data[filtered_data['Year'] == 2010]
    data_2019 = filtered_data[filtered_data['Year'] == 2019]

    # Calculate the percentage increase or decrease
    percentage_change = ((data_2019['Crude Rate'].values - data_2010['Crude Rate'].values) / data_2010['Crude Rate'].values) * 100


    # A line plot of Crude Rate across years
    plt.figure(figsize=(6, 4))
    plt.plot(filtered_data['Year'], filtered_data['Crude Rate'])
    plt.xlabel('Year')
    plt.ylabel('Incident Rate')
    plt.title(f'Incidence Rate of {selected_cancer_type} Cancer (2010-2019)')

    # Add arrow annotation with percentage change
    for i, value in enumerate(percentage_change):
        arrow_text = f'Percentage Increase: {value:.2f}%'
        plt.annotate(arrow_text, xy=(2019, data_2019['Crude Rate'].values[i]), xytext=(2010, data_2010['Crude Rate'].values[i]-0.03),
                     arrowprops=dict(facecolor='red', arrowstyle='->'), fontsize=8)
        
    data_2019['Crude Rate'] = pd.to_numeric(data_2019['Crude Rate'], errors='coerce')

    
    # Find cancer type with highest Crude Rate in 2019
    highest_crude_rate = data_2019_[data_2019_['Crude Rate'] == data_2019_['Crude Rate'].max()]['Leading Cancer Sites'].values[0]
    highest_crude_rate_value = data_2019_['Crude Rate'].max()

    # Find cancer type with highest percentage increase
    highest_percentage_increase_index = percentage_change_.argmax()
    highest_percentage_increase = data['Leading Cancer Sites'].values[highest_percentage_increase_index]
    highest_percentage_increase_value = percentage_change_[highest_percentage_increase_index]
    

        # Layout
    col1, col2 = st.columns(([1.5, 1]))

    with col1:
        # Display the line plot
        st.pyplot(plt)

    with col2:
        
        # Display the results
        col3, col4 = st.columns(2)

        col3.metric('Highest Rate Value', "{:,.0f}".format(highest_crude_rate_value))
        col4.metric('Cancer Type', highest_crude_rate)

        # Display the results
        col5, col6 = st.columns(2)

        col5.metric('Highest % Increase', "{:,.0f}".format(highest_percentage_increase_value))
        col6.metric('Cancer Type', 'Skin')
        
    
    
    
    #Heat map for death rate
    filtered_data = data[["Leading Cancer Sites", "Death Rate (within 5 years)"]]
    filtered_data = filtered_data.sort_values(by="Death Rate (within 5 years)", ascending=False)

    #average_death_rate = filtered_data.groupby("Leading Cancer Sites")["Death Rate (within 5 years)"].mean()
    #filtered_data = filtered_data.sort_values(by="Death Rate (within 5 years)", ascending=False)
    pivot_table = filtered_data.pivot_table(index="Leading Cancer Sites", values="Death Rate (within 5 years)")
    pivot_table=pivot_table.sort_values(by="Death Rate (within 5 years)", ascending=False)
    plt.figure(figsize=(8, 4))
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
    highest_severity_cancer = sorted_data.iloc[0]['Leading Cancer Sites']
    highest_severity_value = sorted_data.iloc[0]['Severity']
    
    st.subheader('Severity = Incidence Rate (2019) x % increase x Death Rate (within 5 years)')
    plt.figure(figsize=(10, 6))
    plt.bar(sorted_data['Leading Cancer Sites'], sorted_data['Severity'])
    plt.xlabel('Cancer Type')
    plt.ylabel('Severity')
    plt.title('Severity of Cancer Types at Year 2019')
    plt.xticks(rotation=90)
    plt.tight_layout()
    #st.pyplot(plt)
    
    col1, col2 = st.columns(([3, 1]))

    with col1:
        # Display the line plot
        st.pyplot(plt)

    with col2:
    
        col2.metric('Highest Severity', highest_severity_cancer)
   
        col2.metric('Severity Value', "{:,.0f}".format(highest_severity_value))
        
        

    wordcloud_data = dict(zip(sorted_data['Leading Cancer Sites'], sorted_data['Severity']))

    plt.figure(figsize=(10, 6))
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(wordcloud_data)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.subheader('Large words correspond to high severity ')
    st.pyplot(plt)

    
if pages[page] == "pancreas":
    st.subheader('Overview of Pancreas Cancer Situation in the US')
    column1, column2 = st.columns(2)
    
    
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

    
    # A sidebar selectbox for state selection
    selected_state = st.selectbox('Select a State', data2['States'].unique())

    # Filter the data based on the selected state
    data_2019 = data2[data2['Year'] == 2019]
    filtered_data = data_2019[data_2019['States'] == selected_state]
    filtered_data = filtered_data[~filtered_data['Age Groups'].isin(['< 1 year', '1-4 years', '5-9 years'])]



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
        width=250,
        height=250
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
    
    # Filter out rows with zero Crude Rate
    filtered_states = sorted_states[sorted_states['Crude Rate'] > 0]

    # Define colormap
    cmap = cm.get_cmap('tab20')  # Choose a desired colormap (e.g., 'viridis', 'cool', 'cubehelix', etc.)

    # Generate color values based on Crude Rate
    color_values = filtered_states['Crude Rate']
    color_range = color_values.max() - color_values.min()
    normalized_values = (color_values - color_values.min()) / color_range
    
    fig, ax = plt.subplots(figsize=(30, 20))

    label_text = [f'{state}\n({cr:.2f})' for state, cr in zip(filtered_states['States'], filtered_states['Crude Rate'])]
    # Plot the treemap using squarify
    squarify.plot(sizes=filtered_states['Crude Rate'], label=label_text, alpha=0.7, color=cmap(normalized_values), ax=ax)#filtered_states['States']
    # Configure the plot
    ax.axis('off')
    ax.set_title('Ranking of States by Crude Rate (TreeMap)')
    for label in ax.texts:
        label.set_fontsize(20)
    
    st.pyplot(fig)

    # Load the CSV file
    data4_path= 'https://raw.githubusercontent.com/marwaajouz/Stramlit_trial/main/Pancreas_Cancer_Race.csv'
    data4 = pd.read_csv(data4_path)

    #selected_year = st.sidebar.selectbox('Select a Year', data4['Year'].unique())
    years = data4['Year'].unique().astype(int)
    selected_year = st.slider('Select a Year', min_value=int(min(years)), max_value=int(max(years)))

    filtered_data = data4[(data4['Year'] == selected_year) & (~data4['Race'].isin(['Other Races and Unknown combined']))]
    filtered_data['Crude Rate'] = pd.to_numeric(filtered_data['Crude Rate'], errors='coerce')

    plt.figure(figsize=(8, 4))
    sns.barplot(data=filtered_data, x='Race', y='Crude Rate', hue='Sex',ci=None)
    plt.xlabel('Race')
    plt.ylabel('Crude Rate')
    plt.title(f'Crude Rate by Race for Year {selected_year}')
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(plt)



    
    
    
