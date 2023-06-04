# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Cancer in the US')
st.write("Hello, world!")


# Load the CSV file
data_path= 'https://github.com/marwaajouz/Stramlit_trial/blob/main/General_without_regoin.csv'
data = pd.read_csv(data_path)

# Create a dropdown select box for Cancer Types
cancer_types = data['Leading Cancer Types'].unique()
selected_cancer_type = st.selectbox('Select a Cancer Type', cancer_types)

# Filter the data based on the selected Cancer Type
filtered_data = data[data['Leading Cancer Types'] == selected_cancer_type]

# Create a line plot of Crude Rate across years
plt.figure(figsize=(10, 6))
plt.plot(filtered_data['Year'], filtered_data['Crude Rate'])
plt.xlabel('Year')
plt.ylabel('Crude Rate')
plt.title(f'Crude Rate of {selected_cancer_type} Across Years')
st.pyplot(plt)
