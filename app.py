# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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
    column1.metric('% of Deaths Between Pancrease Cancer Patients', "{:,.0f}".format(Death_Rate))
    
    Percentage_increaase = filtered_data['Percentage Change'].values[0]
    Severity = Percentage_increaase * Death_Rate * crude_rate_2019
    column2.metric("Calculated Risk", Severity)
