import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Athletes Physical Characteristics Dashboard',
    page_icon=':athletic_shoe:',  # Emoji for a sports theme
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_athletes_data():
    """Grab athletes' data from a CSV file."""
    # Adjust this path as per where your file is located
    DATA_FILENAME = Path(__file__).parent/'data/country_grouped.csv'
    raw_athletes_df = pd.read_csv(DATA_FILENAME)

    return raw_athletes_df

athletes_df = get_athletes_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :athletic_shoe: Athletes Physical Characteristics Dashboard

Explore data on the height and weight of athletes from different countries.
'''

# Add some spacing
''
''

# Filter countries (NOC)
countries = athletes_df['NOC_'].unique()

selected_countries = st.multiselect(
    'Which countries would you like to view?',
    countries,
    ['AFG', 'AHO', 'ALB', 'ALG', 'AND']
)

# Filter the data based on selected countries
filtered_athletes_df = athletes_df[athletes_df['NOC_'].isin(selected_countries)]

# Select metric type (Mean or Median)
metric_type = st.selectbox(
    'Which metric would you like to view?',
    ['Mean', 'Median']
)

# Set the column names based on selected metric
if metric_type == 'Mean':
    height_col = 'height_mean'
    weight_col = 'weight_mean'
else:
    height_col = 'height_median'
    weight_col = 'weight_median'

# -----------------------------------------------------------------------------
# Visualization: Plotting

# Plotting Height vs Weight by Country
st.header(f'{metric_type} Height and Weight by Country', divider='gray')

# Plot Height and Weight
fig, ax = plt.subplots(figsize=(14, 7))

# Bar plot for Height
sns.barplot(
    data=filtered_athletes_df,
    x='NOC_',
    y=height_col,
    color='blue',
    label='Height',
    ax=ax
)

# Bar plot for Weight
sns.barplot(
    data=filtered_athletes_df,
    x='NOC_',
    y=weight_col,
    color='orange',
    label='Weight',
    ax=ax
)

ax.set_title(f'{metric_type} Height and Weight of Athletes by Country')
ax.set_xlabel('Country (NOC)')
ax.set_ylabel(f'{metric_type} Value')
plt.xticks(rotation=90)

# Add a legend
ax.legend()

# Show the plot in Streamlit
st.pyplot(fig)

# -----------------------------------------------------------------------------
# Display a table with the selected data

st.header(f'{metric_type} Height and Weight Data', divider='gray')

# Display the filtered data in a table
st.dataframe(filtered_athletes_df[['NOC_', height_col, weight_col]])
