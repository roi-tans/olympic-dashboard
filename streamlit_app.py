import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import zipfile
import os

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Athletes Physical Characteristics Dashboard',
    page_icon=':athletic_shoe:',  # Emoji for a sports theme
)

# Declare some useful functions.

@st.cache_data
def get_athletes_data():
    """Grab athletes' data from a CSV file."""
    # Adjust this path as per where your file is located
    DATA_FILENAME = Path(__file__).parent/'data/country_grouped.csv'
    raw_athletes_df = pd.read_csv(DATA_FILENAME)

    return raw_athletes_df

athletes_df = get_athletes_data()

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

# Create a sidebar menu
selected_section = st.sidebar.selectbox(
    'Select Visualization Section',
    ['Roi', 'Idan', 'Amit', 'Alex']
)

# Display content based on selected section
if selected_section == 'Roi':
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

    # Display a table with the selected data
    st.header(f'{metric_type} Height and Weight Data', divider='gray')

    # Display the filtered data in a table
    st.dataframe(filtered_athletes_df[['NOC_', height_col, weight_col]])

elif selected_section == 'Idan':
    # Additional Visualizations and Insights

    @st.cache_data
    def load_grouped_data():
        """Load the grouped data for additional visualizations."""
        # Adjust the path to your CSV file
        DATA_FILENAME = Path(__file__).parent / 'data/grouped_data_by_noc_event_sex.csv'
        grouped_data_df = pd.read_csv(DATA_FILENAME)

        return grouped_data_df

    # Load the grouped data
    grouped_data_df = load_grouped_data()

    # Additional Filters

    # Add title for this section
    '''
    ## :bar_chart: Additional Insights: Height and Weight by Event and Sex
    '''

    # Filter NOCs
    available_nocs = grouped_data_df['NOC'].unique()
    chosen_nocs = st.multiselect(
        'Choose NOCs (Countries):',
        available_nocs,
        available_nocs[:3]  # Default to first three NOCs
    )

    # Filter Events
    available_events = grouped_data_df['Event'].unique()
    chosen_events = st.multiselect(
        'Choose Events:',
        available_events,
        available_events[:3]  # Default to first three events
    )

    # Filter Sex
    available_sexes = grouped_data_df['Sex'].unique()
    chosen_sexes = st.multiselect(
        'Choose Sex:',
        available_sexes,
        available_sexes  # Default to all sexes
    )

    # Apply filters to the grouped data
    filtered_grouped_df = grouped_data_df[
        (grouped_data_df['NOC'].isin(chosen_nocs)) &
        (grouped_data_df['Event'].isin(chosen_events)) &
        (grouped_data_df['Sex'].isin(chosen_sexes))
    ]

    # Visualization: Heatmap

    st.header('Mean Height and Weight Heatmap', divider='gray')

    # Create a pivot table for heatmap visualization
    pivot_table = filtered_grouped_df.pivot_table(
        values='mean_height',
        index='Event',
        columns='NOC',
        aggfunc='mean'
    )

    # Plot the heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        pivot_table,
        annot=True,
        fmt=".1f",
        cmap='coolwarm',
        cbar_kws={'label': 'Mean Height (cm)'},
        ax=ax
    )

    ax.set_title('Heatmap of Mean Height by Event and NOC')
    ax.set_xlabel('NOC (Country)')
    ax.set_ylabel('Event')

    # Display the heatmap in Streamlit
    st.pyplot(fig)

elif selected_section == 'Amit':
    st.title('🏅 Olympic Success & National Sports Budgets')
    st.write("Exploring the relationship between national sports budgets and Olympic performance")

    try:
        # Load the data
        budget_df = pd.read_csv('data/Correlation Sports Budget to Olympic Medals.csv', sep=';')
        
        # Clean the budget data - simplified cleaning
        budget_df['Budget_Clean'] = (budget_df['Total 2017-2019 (MM U$D)']
            .str.replace('$', '')
            .str.replace(' ', '')
            .str.replace('.', '')
            .str.replace(',', '.')
            .astype(float))
        
        budget_df['Total Medals'] = pd.to_numeric(budget_df['Total Medals'])

        # Display key metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Budget (MM USD)", f"${budget_df['Budget_Clean'].mean():,.2f}")
        with col2:
            st.metric("Average Medals", f"{budget_df['Total Medals'].mean():.1f}")
        with col3:
            correlation = budget_df['Budget_Clean'].corr(budget_df['Total Medals'])
            st.metric("Budget-Medals Correlation", f"{correlation:.2f}")

        # Create main scatter plot
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=budget_df, x='Budget_Clean', y='Total Medals', ax=ax1)
        
        # Add labels and title
        ax1.set_xlabel('Sports Budget (Million USD)')
        ax1.set_ylabel('Olympic Medals')
        ax1.set_title('National Sports Budget vs Olympic Medals')
        
        # Add country labels
        for _, row in budget_df.iterrows():
            ax1.annotate(row['Country'], (row['Budget_Clean'], row['Total Medals']))
        
        st.pyplot(fig1)
        plt.close()

        # Calculate and display efficiency
        st.subheader("Budget Efficiency Analysis", divider='gray')
        budget_df['Medals per Billion'] = (budget_df['Total Medals'] / budget_df['Budget_Clean']) * 1000
        
        # Create efficiency bar plot
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        efficiency_data = budget_df.nlargest(10, 'Medals per Billion')
        sns.barplot(data=efficiency_data, x='Country', y='Medals per Billion', ax=ax2)
        plt.xticks(rotation=45)
        ax2.set_title('Top 10 Countries: Olympic Medals per Billion USD')
        
        st.pyplot(fig2)
        plt.close()

        # Display data table
        st.subheader("Detailed Data", divider='gray')
        st.dataframe(
            budget_df[['Country', 'Budget_Clean', 'Total Medals', 'Medals per Billion']]
            .sort_values('Medals per Billion', ascending=False)
            .style.format({
                'Budget_Clean': '${:,.2f}M',
                'Medals per Billion': '{:.1f}',
                'Total Medals': '{:.0f}'
            })
        )

    except Exception as e:
        st.error(f"Error loading or processing data: {str(e)}")
        st.write("Please check if the data file is in the correct location and format.")

elif selected_section == 'Alex':
    st.title("Alex's Visualization")
    st.write("Coming soon...")
