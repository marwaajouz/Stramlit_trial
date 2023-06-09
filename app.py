# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.title('Cancer in the US')


# Load the CSV file
data_path= 'https://raw.githubusercontent.com/marwaajouz/Stramlit_trial/main/General_without_regoin.csv'
data = pd.read_csv(data_path)

# Create a dropdown select box for Cancer Types
cancer_types = data['Leading Cancer Sites'].unique()
selected_cancer_type = st.selectbox('Select a Cancer Type', cancer_types)

# Filter the data based on the selected Cancer Type
filtered_data = data[data['Leading Cancer Sites'] == selected_cancer_type]

# Create a line plot of Crude Rate across years
plt.figure(figsize=(10, 6))
plt.plot(filtered_data['Year'], filtered_data['Crude Rate'])
plt.xlabel('Year')
plt.ylabel('Crude Rate')
plt.title(f'Crude Rate of {selected_cancer_type} Across Years')
st.pyplot(plt)


#Heat map for death rate
filtered_data = data[["Leading Cancer Sites", "Death Rate (within 5 years)"]]
average_death_rate = filtered_data.groupby("Leading Cancer Sites")["Death Rate (within 5 years)"].mean()
pivot_table = filtered_data.pivot_table(index="Leading Cancer Sites", values="Death Rate (within 5 years)")

plt.figure(figsize=(10, 8))
sns.heatmap(pivot_table, cmap="YlGnBu", annot=True, fmt=".2f")
plt.title("Average Death Rate by Cancer Type")
plt.xlabel("Leading Cancer Sites")
plt.ylabel("")

st.pyplot()
