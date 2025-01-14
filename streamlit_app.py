import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import zipfile
import os

# Set the page config at the very top of the script
st.set_page_config(
    page_title='Olympic Athletes Physical Characteristics Dashboard',
    page_icon=':athletic_shoe:',
    layout='wide',  # This makes the dashboard use the full width
    initial_sidebar_state='expanded'
)

# Add custom CSS to maximize space usage
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        .element-container {
            margin-bottom: 0.5rem;
        }
        .stPlotlyChart {
            margin-bottom: 0rem;
        }
    </style>
""", unsafe_allow_html=True)

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
st.markdown('<h1 style="text-align: center; width: 100%;">Olympic Athletes Physical Characteristics Dashboard</h1>', unsafe_allow_html=True)

# Add some spacing
''
''

# Create a sidebar menu
selected_section = st.sidebar.selectbox(
    'Select Visualization Section',
    ['Roi', 'Idan', 'Amit', 'Alex']
)

# Display content based on selected section
if selected_section == 'Roi':
    # Plotting Height vs Weight by Country
    st.header('Height and Weight by Country', divider='gray')

    # Plot Height and Weight
    fig, ax = plt.subplots(figsize=(14, 7))

    # Bar plot for Height
    sns.barplot(
        data=athletes_df,
        x='NOC_',
        y='height_mean',
        color='blue',
        label='Height',
        ax=ax
    )

    # Bar plot for Weight
    sns.barplot(
        data=athletes_df,
        x='NOC_',
        y='weight_mean',
        color='orange',
        label='Weight',
        ax=ax
    )

    ax.set_title('Height and Weight of Athletes by Country')
    ax.set_xlabel('Country (NOC)')
    ax.set_ylabel('Value')
    plt.xticks(rotation=90)

    # Add a legend
    ax.legend()

    # Show the plot in Streamlit
    st.pyplot(fig)

    # Display a table with the selected data
    st.header('Height and Weight Data', divider='gray')

    # Display the filtered data in a table
    st.dataframe(athletes_df[['NOC_', 'height_mean', 'weight_mean']])

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
    st.title("Olympic Athletes: Physical Attributes and Medal Achievements")

    @st.cache_data
    def load_data():
        zip_file_path = 'data/athlete_events.csv.zip'
        csv_file_path = 'data/athlete_events.csv'
        
        if not os.path.exists(csv_file_path):
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall('data/')
        
        data = pd.read_csv(csv_file_path)

        # Replace -1 values in Age column with the mean age
        mean_age = data['Age'].replace(-1, np.nan).mean()
        data['Age'] = data['Age'].replace(-1, mean_age)
        
        return data

    data = load_data()

    data = data.dropna(subset=['Height', 'Weight', 'Medal', 'Year'])

    sports_list = data['Sport'].unique().tolist()
    selected_sport = st.selectbox("Select a Sport:", sports_list)

    sport_data = data[data['Sport'] == selected_sport]

    st.write("### Scatter Plot: Height vs. Weight by Medal")
    fig, ax = plt.subplots()
    sns.scatterplot(
        data=sport_data, 
        x='Height', 
        y='Weight', 
        hue='Medal', 
        palette='muted', 
        alpha=0.7, 
        ax=ax
    )
    plt.xlabel('Height (cm)')
    plt.ylabel('Weight (kg)')
    plt.title(f'{selected_sport}: Height vs. Weight by Medal')
    st.pyplot(fig)

    st.write("### Bar Plot: Average Height and Weight by Medal")
    avg_data = sport_data.groupby('Medal')[['Height', 'Weight']].mean().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=avg_data.melt(id_vars='Medal'), x='Medal', y='value', hue='variable', palette='muted', ax=ax)
    plt.xlabel('Medal')
    plt.ylabel('Average Value')
    plt.title(f'{selected_sport}: Average Height and Weight by Medal')
    st.pyplot(fig)

elif selected_section == 'Alex':
    np.random.seed(111)

    col1, col2 = st.columns([3, 1])  # 3:1 ratio for main plot vs controls
    
    with col1:
        st.title("How much does age matter at Olympic Sports?")
    
    with col2:
        # Medal highlight options
        show_bronze = st.checkbox('Highlight Bronze Medals', value=False)
        show_silver = st.checkbox('Highlight Silver Medals', value=False)
        show_gold   = st.checkbox('Highlight Gold Medals', value=False)

    # Load data from CSV
    athlete_data = pd.read_csv("G:/Python Projects/olympic-dashboard/data/preprocessed_athlete_events.csv")

    # Get all unique sports and sort by average age
    sports_avg_age = athlete_data.groupby('Sport')['Age'].mean().sort_values()
    all_sports = sports_avg_age.index.tolist()

    # Define default sports
    default_sports = ['Basketball', 'Football', 'Speed Skating', 'Athletics', 'Ice Hockey', 
                     'Swimming']

    # Filter defaults to only those that exist in the data
    default_sports_in_data = [s for s in default_sports if s in all_sports]

    # Multiselect of sports - place it in a wider container
    selected_sports = st.multiselect(
        'Select Sports:',
        options=all_sports,
        default=default_sports_in_data
    )

    if len(selected_sports) > 0:
        filtered_data = athlete_data[athlete_data['Sport'].isin(selected_sports)].copy()

        # Replace -1 values in Age column with the mean age
        mean_age = filtered_data['Age'].replace(-1, np.nan).mean()
        filtered_data['Age'] = filtered_data['Age'].replace(-1, mean_age)

        def decide_display_category(row):
            medal = row['Medal']
            if medal == 'Gold' and show_gold:
                return 'Gold'
            elif medal == 'Silver' and show_silver:
                return 'Silver'
            elif medal == 'Bronze' and show_bronze:
                return 'Bronze'
            else:
                return 'No Medal'

        filtered_data['DisplayMedal'] = filtered_data.apply(decide_display_category, axis=1)

        # Simple color palette with transparent white for non-medals
        display_palette = {
            'No Medal': (1, 1, 1, 0.3),  # White with 0.3 opacity
            'Gold': 'gold',
            'Silver': 'silver',
            'Bronze': 'brown'
        }

        # Create figure with dynamic size based on number of sports
        fig_width = max(20, len(selected_sports) * 1.5)  # Adjust width based on number of sports
        fig_height = 10
        
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        
        # Create denser stripplot
        sns.stripplot(
            data=filtered_data,
            x='Sport',
            y='Age',
            hue='DisplayMedal',
            palette=display_palette,
            size=4,
            jitter=0.35,
            alpha=0.6,
            dodge=False,
            edgecolor='black',
            linewidth=0.5,
            ax=ax
        )

        # Customize the plot
        ax.set_title("Age Distribution in Olympic Sports", fontsize=14, pad=20)
        ax.set_xlabel("Sport", fontsize=12)
        ax.set_ylabel("Age", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        
        # Customize legend
        handles = []
        labels = []
        if show_gold:
            handles.append(plt.scatter([], [], color='gold', edgecolor='black', linewidth=0.5))
            labels.append('Gold Medal')
        if show_silver:
            handles.append(plt.scatter([], [], color='silver', edgecolor='black', linewidth=0.5))
            labels.append('Silver Medal')
        if show_bronze:
            handles.append(plt.scatter([], [], color='brown', edgecolor='black', linewidth=0.5))
            labels.append('Bronze Medal')
            
        if handles:
            ax.legend(handles, labels, title='Medals', bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Use the full width of the page for the plot
        st.pyplot(fig, use_container_width=True)
    else:
        st.write("Please select at least one sport to display the visualization.")
