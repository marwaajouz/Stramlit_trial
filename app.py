# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.title('Cancer in the US')


# Load the CSV file
data_path= 'https://raw.githubusercontent.com/marwaajouz/Stramlit_trial/main/General_without_regoin.csv'
data = pd.read_csv(data_path)


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
plt.title(f'Crude Rate of {selected_cancer_type} Across Years')

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





