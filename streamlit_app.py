import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import zipfile
import os
import numpy as np
import plotly.express as px

# At the top of your file, replace the existing st.set_page_config with:
st.set_page_config(
    page_title='Athletes Physical Characteristics Dashboard',
    page_icon=':athletic_shoe:',
    layout='centered',  # We'll override this with custom CSS
    initial_sidebar_state='expanded'
)

# Add custom CSS right after set_page_config
st.markdown("""
    <style>
    .block-container {
        max-width: 1200px;
        padding-left: 2rem;
        padding-right: 2rem;
        padding-top: 1rem;
        padding-bottom: 1rem;
        margin: 0 auto;
    }
    
    /* Adjust chart containers */
    .stPlotlyChart {
        width: 100%;
        margin: 0 auto;
    }
    
    /* Optional: Adjust the width of the dataframe */
    .dataframe {
        width: 100%;
        margin: 0 auto;
    }
    
    /* Optional: Adjust sidebar width */
    .css-1d391kg {
        width: 20rem;
    }
    </style>
""", unsafe_allow_html=True)

# Declare some useful functions.

# Create a sidebar menu
selected_section = st.sidebar.selectbox(
    'Select Visualization Section',
    ['Introduction', 'Difference in physique between countries', 'Height and Weight Analysis', 'Budget influence on sports', 'Age distribution by sport']
)

if selected_section == 'Introduction':
    # Title
    st.title('🏅 Olympic Athletes Analysis Dashboard 🌟')
    
    try:
        # Load the data
        @st.cache_data
        def load_opening_data():
            """Load the athlete events data for the opening page."""
            zip_file_path = 'data/athlete_events.csv.zip'
            csv_file_path = 'data/athlete_events.csv'
            
            # Extract if needed
            if not os.path.exists(csv_file_path):
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall('data/')
            
            # Read the data
            return pd.read_csv(csv_file_path)

        # Load data and calculate metrics
        data = load_opening_data()
        
        # Display key metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Total Athletes",
                f"{data['ID'].nunique():,}"
            )
        with col2:
            st.metric(
                "Total Sports",
                f"{data['Sport'].nunique():,}"
            )
        with col3:
            st.metric(
                "Total Countries",
                f"{data['NOC'].nunique():,}"
            )

        # Dataset Preview section
        st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 20px 0;'>
            <h2 style='color: #1f1f1f; margin-bottom: 15px;'>📊 Dataset Preview</h2>
            <p style='font-size: 18px; color: #1f1f1f; line-height: 1.6;'>
                Our analysis is based on comprehensive Olympic data, including athlete characteristics, 
                performance metrics, and national statistics.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.dataframe(data.head(), height=300)

      
        st.title("Olympic Medals by Country")

        medals_data = data.dropna(subset=['Medal', 'NOC'])

        medals_count = medals_data.groupby('NOC')['Medal'].count().reset_index()
        medals_count.columns = ['Country', 'Total Medals']

        medals_by_type = medals_data.groupby(['NOC', 'Medal']).size().unstack(fill_value=0).reset_index()
        medals_by_type.columns = ['Country', 'Bronze', 'Gold', 'Silver']

        merged_data = pd.merge(medals_count, medals_by_type, on='Country')

        @st.cache_data
        def load_country_codes():
            country_codes_url = 'https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv'
            country_codes = pd.read_csv(country_codes_url)
            return country_codes

        country_codes = load_country_codes()

        merged_data = pd.merge(merged_data, country_codes, left_on='Country', right_on='CODE', how='inner')

        st.write("### Interactive 3D Globe of Olympic Medals")
        fig = px.choropleth(
            merged_data,
            locations="CODE",
            color="Total Medals",
            hover_name="COUNTRY",
            hover_data={"Gold": True, "Silver": True, "Bronze": True, "Total Medals": True},
            color_continuous_scale=px.colors.sequential.Plasma,
            title="Olympic Medals by Country",
            projection="orthographic"  # הופך את המפה לכדור הארץ
        )
        fig.update_geos(
            showcountries=True, countrycolor="Black",
            showcoastlines=True, coastlinecolor="Gray",
            projection_rotation=dict(lon=0, lat=0),
        )
        fig.update_layout(geo=dict(showland=True, landcolor="white"))
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig)

        

        # Research Questions section
        st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 20px 0;'>
            <h2 style='color: #1f1f1f; margin-bottom: 15px;'>Our Research Questions 🔍</h2>
            <div style='font-size: 18px; color: #1f1f1f; line-height: 1.6;'>
                <p style='margin-bottom: 15px;'>
                    <strong>1. Physical Characteristics Analysis 📏</strong><br>
                    How do athletes' physical characteristics (height and weight) vary across different countries and sports?
                </p>
                <p style='margin-bottom: 15px;'>
                    <strong>2. Medal Performance 🏅</strong><br>
                    What is the relationship between athletes' physical attributes and their medal achievements in different sports?
                </p>
                <p style='margin-bottom: 15px;'>
                    <strong>3. Budget Impact 💰</strong><br>
                    Is there a correlation between national sports budgets and Olympic medal counts?
                </p>
                <p style='margin-bottom: 15px;'>
                    <strong>4. Age Distribution 📊</strong><br>
                    How does age distribution vary across different Olympic sports, and what role does it play in medal achievements?
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error loading or processing data: {str(e)}")
        st.write("Please check if the data file is in the correct location and format.")

elif selected_section == 'Difference in physique between countries':
    @st.cache_data
    def get_athletes_data():
        """Grab athletes' data from a CSV file."""
        # Adjust this path as per where your file is located
        DATA_FILENAME = Path(__file__).parent/'data/country_grouped3.csv'
        raw_athletes_df = pd.read_csv(DATA_FILENAME)

        return raw_athletes_df

    athletes_df = get_athletes_data()

    st.title("Is there a difference in the physical characteristics of athletes from different countries? 💪🏽")
    st.markdown("""The bar plot shows the average height an weight of athletes by country, providing a country-wise comparison of physical characteristics.
    This helps to identify general trends in athlete physiques across different nations. The second visualization, a scatter plot with a regression line, shows
     a positive relationship between mean height and weight across countries. The red line represents the trend, while the shaded area indicates variability, showing
      that taller athletes tend to weigh more on average.""")   
    countries = athletes_df['region'].unique()

    selected_countries = st.multiselect(
        'Which countries would you like to view?',
        countries,
        ['Afghanistan','Argentina','Georgia','Japan','Israel','USA']
    )

    # Filter the data based on selected countries
    filtered_athletes_df = athletes_df[athletes_df['region'].isin(selected_countries)]

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

    # Plotting Height vs Weight by Country
    # Sort the data by the selected metric (height or weight) in descending order
    sorted_athletes_df = filtered_athletes_df.sort_values(by=height_col, ascending=False)

    # Plotting Mean Height and Weight by Country (Sorted)
    st.header(f'{metric_type} Height and Weight by Country (Sorted)', divider='gray')

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 7))

    # Calculate bar positions
    x = np.arange(len(sorted_athletes_df['region'].unique()))
    width = 0.35

    # Create bars
    height_bars = ax.bar(x - width/2, 
                        sorted_athletes_df[height_col], 
                        width, 
                        label='Height',
                        color='#4A90E2',  # Vibrant blue color
                        alpha=0.8)

    weight_bars = ax.bar(x + width/2, 
                        sorted_athletes_df[weight_col], 
                        width, 
                        label='Weight',
                        color='#73BDF2',  # Vibrant gold color
                        alpha=0.8)

    # Customize the plot
    ax.set_title(f'{metric_type} Height and Weight of Athletes by Country (Sorted)', fontsize=16, color='#333333')
    ax.set_xlabel('Country (region)', fontsize=12, color='#333333')
    ax.set_ylabel(f'{metric_type} Value', fontsize=12, color='#333333')

    # Set x-axis ticks
    ax.set_xticks(x)
    ax.set_xticklabels(sorted_athletes_df['region'], rotation=45, ha='right', fontsize=10)

    # Add value labels on the bars
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom', fontsize=9)

    add_value_labels(height_bars)
    add_value_labels(weight_bars)

    # Add legend
    ax.legend(fontsize=10)

    # Add gridlines
    ax.grid(True, linestyle='--', alpha=0.6, axis='y')

    # Adjust layout
    plt.tight_layout()

    # Show the plot in Streamlit
    st.pyplot(fig)

    # Function to load the grouped data
    def load_grouped_data2():
        """Load the grouped data for additional visualizations."""
        # Adjust the path to your CSV file
        DATA_FILENAME = Path(__file__).parent / 'data/grouped_data_by_noc_event_sex3.csv'
        grouped_data_df = pd.read_csv(DATA_FILENAME)
        
        # Clean data by removing invalid heights and weights
        grouped_data_df = grouped_data_df[
            (grouped_data_df['mean_height'] > 0) & 
            (grouped_data_df['mean_weight'] > 0)
        ]
        
        return grouped_data_df

    # Load the grouped data
    grouped_data_df = load_grouped_data2()

    # Add title for this section
    st.markdown('''
    ## Olympic Athletes Analysis: Height and Weight by Event and Sex 📊
    ''')

    # First, filter by Event
    available_events = grouped_data_df['Event'].unique()
    chosen_events = st.multiselect(
        'Choose Events:',
        available_events,
        available_events[:3],  # Default to first three events
        key='event_selector'
    )

    # Filter data by selected events
    events_filtered_df = grouped_data_df[grouped_data_df['Event'].isin(chosen_events)]

    # Then, get available countries for those events
    available_nocs = events_filtered_df['region'].unique()
    chosen_nocs = st.multiselect(
        'Choose Countries (filtered by selected events):',
        available_nocs,
        available_nocs[:3] if len(available_nocs) >= 3 else available_nocs,  # Default to first three NOCs or all if less
        key='noc_selector'
    )

    # Apply final filters to the grouped data
    filtered_grouped_df = events_filtered_df[events_filtered_df['region'].isin(chosen_nocs)]

    # Create tabs for different visualizations
    tab1, tab2 = st.tabs(["Height vs Weight Analysis", "Country Analysis"])

    with tab1:
        st.header('Analysis')

        # Simple scatter plot with regression line
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Using a custom color for scatterplot dots
        sns.scatterplot(
            data=filtered_grouped_df,
            x='mean_height',
            y='mean_weight',
            s=100,
            color='#2a9d8f',  # Custom teal-green color
            alpha=0.8
        )
        
        # Regression line in a complementary color
        sns.regplot(
            data=filtered_grouped_df,
            x='mean_height',
            y='mean_weight',
            scatter=False,
            color='#e76f51',  # Warm coral color for contrast
            line_kws={"lw": 2, "alpha": 0.9}
        )
        
        # Styling adjustments
        ax.set_title('Height vs. Weight Analysis', fontsize=16, color='#333333')
        ax.set_xlabel('Mean Height (cm)', fontsize=12, color='#333333')
        ax.set_ylabel('Mean Weight (kg)', fontsize=12, color='#333333')
        ax.grid(True, linestyle='--', alpha=0.6)
        
        st.pyplot(fig)

    with tab2:
        st.header('Country Comparison', divider='gray')
        
        # Calculate average BMI for each country
        filtered_grouped_df['BMI'] = filtered_grouped_df['mean_weight'] / (filtered_grouped_df['mean_height'] / 100) ** 2
        
        country_stats = filtered_grouped_df.groupby('region').agg({
            'mean_height': 'mean',
            'mean_weight': 'mean',
            'BMI': 'mean'
        }).round(2)
        
        # Create bar chart comparing countries with vibrant colors
        fig_countries, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6), dpi=100)
        
        # Height comparison
        sns.barplot(
            data=filtered_grouped_df,
            x='region',
            y='mean_height',
            ci=None,
            palette='crest',  # Vibrant green-blue palette
            ax=ax1
        )
        ax1.set_title('Average Height by Country', fontsize=14, color='#333333')
        ax1.set_ylabel('Height (cm)', fontsize=12, color='#333333')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, linestyle='--', alpha=0.6)
        
        # Weight comparison
        sns.barplot(
            data=filtered_grouped_df,
            x='region',
            y='mean_weight',
            ci=None,
            palette='flare',  # Vibrant pink-red palette
            ax=ax2
        )
        ax2.set_title('Average Weight by Country', fontsize=14, color='#333333')
        ax2.set_ylabel('Weight (kg)', fontsize=12, color='#333333')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, linestyle='--', alpha=0.6)
        
        # BMI comparison
        sns.barplot(
            data=filtered_grouped_df,
            x='region',
            y='BMI',
            ci=None,
            palette='mako',  # Vibrant teal-blue palette
            ax=ax3
        )
        ax3.set_title('Average BMI by Country', fontsize=14, color='#333333')
        ax3.set_ylabel('BMI', fontsize=12, color='#333333')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, linestyle='--', alpha=0.6)
        
        # Layout adjustments
        plt.tight_layout()
        st.pyplot(fig_countries)
        
        # Display detailed statistics
        st.subheader('Detailed Country Statistics')
        st.dataframe(
            country_stats.style.format({
                'mean_height': '{:.1f} cm',
                'mean_weight': '{:.1f} kg',
                'BMI': '{:.1f}'
            })
        )
    
    # Add title for this section


    # Add key insights section
    st.header('Key Insights', divider='gray')

    # Calculate some interesting statistics
    stats_cols = st.columns(3)

    with stats_cols[0]:
        st.metric(
            label="Average Height",
            value=f"{filtered_grouped_df['mean_height'].mean():.1f} cm",
            delta=f"{filtered_grouped_df['mean_height'].std():.1f} cm std"
        )

    with stats_cols[1]:
        st.metric(
            label="Average Weight",
            value=f"{filtered_grouped_df['mean_weight'].mean():.1f} kg",
            delta=f"{filtered_grouped_df['mean_weight'].std():.1f} kg std"
        )

    with stats_cols[2]:
        avg_bmi = filtered_grouped_df['BMI'].mean()
        st.metric(
            label="Average BMI",
            value=f"{avg_bmi:.1f}",
            delta=f"{filtered_grouped_df['BMI'].std():.1f} std"
        )


#######################################

elif selected_section == 'Height and Weight Analysis':
    # Title and Introduction
    st.title("Is there a correlation between height or weight and winning medals, and if so, in which sports? 📏")
    
    # Enhanced introduction with larger text and better formatting
    st.markdown("""
    <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 20px 0;'>
        <h2 style='color: #1f1f1f; margin-bottom: 15px;'>Understanding the Visualizations 📊</h2>
        <p style='font-size: 20px; color: #1f1f1f; line-height: 1.6;'>
            <strong>The Scatter Plot</strong> displays each athlete's height and weight, with points colored by medal type. 
            This visualization helps us identify patterns in physical characteristics among medal winners.
        </p>
        <p style='font-size: 20px; color: #1f1f1f; line-height: 1.6;'>
            <strong>The Bar Plot</strong> shows the average height and weight for each medal category, 
            making it easy to compare physical attributes across different levels of achievement.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Data Loading
    @st.cache_data
    def load_data():
        zip_file_path = 'data/athlete_events.csv.zip'
        csv_file_path = 'data/athlete_events.csv'
        
        # Extract file if needed
        if not os.path.exists(csv_file_path):
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall('data/')
        
        # Read the file
        data = pd.read_csv(csv_file_path)
        return data
    
    data1 = load_data()
    
    # Data cleaning
    data = data1[
        (data1['Height'] != -1) &
        (data1['Weight'] != -1)
    ]
    data = data.dropna(subset=['Height', 'Weight', 'Medal', 'Year'])
    
    # Sport selection with larger font
    sports_list = data['Sport'].unique().tolist()
    st.markdown("### Select a Sport to Analyze 🎯:")
    selected_sport = st.selectbox("", sports_list)  # Empty string to avoid double label
    sport_data = data[data['Sport'] == selected_sport]
    
    # Scatter Plot
    st.markdown("## Scatter Plot: Height vs. Weight by Medal 📈")
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Define medal colors
    medal_colors = {
        'Gold': '#FFD700',    # Bright gold
        'Silver': '#C0C0C0',  # Brighter silver
        'Bronze': '#CD7F32'   # Warm bronze
    }
    
    # Create scatter plot
    for medal in ['Bronze', 'Silver', 'Gold']:  # Plot in this order to have gold on top
        mask = sport_data['Medal'] == medal
        ax.scatter(
            sport_data[mask]['Height'],
            sport_data[mask]['Weight'],
            c=medal_colors[medal],
            label=medal,
            alpha=0.7,
            s=100,  # Larger point size
            edgecolor='white',  # White edge for better contrast
            linewidth=0.5
        )
    
    # Enhance scatter plot styling
    ax.set_xlabel('Height (cm)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Weight (kg)', fontsize=14, fontweight='bold')
    ax.set_title(f'{selected_sport}: Height vs. Weight by Medal', fontsize=16, pad=20)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Enhanced legend
    ax.legend(
        title='Medal Type',
        title_fontsize=14,
        fontsize=12,
        bbox_to_anchor=(1.05, 1),
        loc='upper left'
    )
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Bar Plot
    st.markdown("## Bar Plot: Average Height and Weight by Medal 📊")
    avg_data = sport_data.groupby('Medal')[['Height', 'Weight']].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Define measurement colors
    measurement_colors = {
        'Height': '#FF6B6B',  # Warm coral for height
        'Weight': '#4ECDC4'   # Fresh teal for weight
    }
    
    # Create bar plot
    for i, measure in enumerate(['Height', 'Weight']):
        data_for_measure = avg_data[['Medal', measure]].copy()
        data_for_measure.columns = ['Medal', 'Value']
        
        bars = ax.bar(
            [x + i*0.25 for x in range(len(avg_data))], 
            data_for_measure['Value'],
            0.25,
            label=measure,
            color=measurement_colors[measure],
            alpha=0.8
        )
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'{height:.1f}',
                ha='center',
                va='bottom',
                fontsize=12
            )
    
    # Enhance bar plot styling
    ax.set_xlabel('Medal Type', fontsize=14, fontweight='bold')
    ax.set_ylabel('Value', fontsize=14, fontweight='bold')
    ax.set_title(f'{selected_sport}: Average Height and Weight by Medal', 
                 fontsize=16, pad=20)
    ax.set_xticks([x + 0.25/2 for x in range(len(avg_data))])
    ax.set_xticklabels(avg_data['Medal'], fontsize=12)
    ax.grid(True, axis='y', linestyle='--', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(fontsize=12, title_fontsize=14)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Enhanced insights section
    st.markdown("""
    <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 20px 0;'>
        <h2 style='color: #1f1f1f; margin-bottom: 15px;'>Key Insights 🔍</h2>
        <ul style='font-size: 18px; color: #1f1f1f; line-height: 1.6;'>
            <li><strong>Distribution Pattern:</strong> The scatter plot reveals how physical attributes are distributed among medal winners, 
            showing any clusters or patterns that might indicate optimal characteristics for success.</li>
            <li><strong>Average Trends:</strong> The bar plot highlights any significant differences in average height and weight 
            across medal categories, helping identify if certain physical attributes correlate with higher achievement.</li>
            <li><strong>Sport-Specific Patterns:</strong> By comparing different sports, we can see how the importance of 
            physical characteristics varies across disciplines.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
  
elif selected_section == 'Budget influence on sports':
    # Define color scheme
    colors = {
        'primary': '#4361EE',    # Vibrant Blue
        'accent': '#4CC9F0',     # Light Blue
        'accent2': '#2E8B57',    # Sea Green - representing efficiency/performance       
        'text': '#2C3E50',       # Dark Gray
        'grid': '#E9ECEF',       # Light Gray
        'background': '#FFFFFF'   # White
    }

    # Title 
    st.title("Exploring the correlation between national sports budgets and Olympic performance 💸")
    
    try:
        # Load and clean data
        budget_df = pd.read_csv('data/Correlation Sports Budget to Olympic Medals.csv', sep=';')
        
        budget_df['Budget_Clean'] = (budget_df['Total 2017-2019 (MM U$D)']
            .str.replace('$', '')
            .str.replace(' ', '')
            .str.replace('.', '')
            .str.replace(',', '.')
            .astype(float))
        
        budget_df['Total Medals'] = pd.to_numeric(budget_df['Total Medals'])
        
        # Display metrics first
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Average Budget (MM USD)", 
                f"${budget_df['Budget_Clean'].mean():,.2f}",
                delta_color="normal"
            )
        with col2:
            st.metric(
                "Average Medals", 
                f"{budget_df['Total Medals'].mean():.1f}"
            )
        with col3:
            correlation = budget_df['Budget_Clean'].corr(budget_df['Total Medals'])
            st.metric(
                "Budget-Medals Correlation", 
                f"{correlation:.2f}"
            )

        # Analysis explanation
        st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 20px 0;'>
            <h2 style='color: #1f1f1f; margin-bottom: 15px;'>Understanding the Analysis 📊</h2>
            <p style='font-size: 20px; color: #1f1f1f; line-height: 1.6;'>
                <strong>The Scatter Plot</strong> demonstrates the relationship between a country's sports budget and their Olympic medal count,
                revealing how financial investment might influence athletic success on the international stage.
            </p>
            <p style='font-size: 20px; color: #1f1f1f; line-height: 1.6;'>
                <strong>The Efficiency Plot</strong> highlights which countries achieve the most medals relative to their budget,
                showing that success isn't solely dependent on financial resources.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Calculate Medals per Billion
        budget_df['Medals per Billion'] = (budget_df['Total Medals'] / budget_df['Budget_Clean']) * 1000

        # Scatter Plot
        st.markdown("## 📈 Budget vs. Medals Relationship")
        fig1, ax1 = plt.subplots(figsize=(12, 8))
        
        def should_show_label(row):
            # Show only if:
            # - More than 30 medals OR
            # - Budget more than 15000M USD OR
            # - Top 3 in medals per billion OR
            # - Specifically selected key countries
            is_top_3_efficient = row['Country'] in budget_df.nlargest(3, 'Medals per Billion')['Country'].values
            
            return (row['Total Medals'] > 30 or 
                    row['Budget_Clean'] > 15000 or 
                    is_top_3_efficient or 
                    row['Country'] in ['Netherlands', 'Italy'])
        
        # Create scatter plot with enhanced styling
        scatter = ax1.scatter(
            budget_df['Budget_Clean'], 
            budget_df['Total Medals'],
            s=100,
            alpha=0.7,
            color=colors['primary']
        )
        
        # Add country labels with improved visibility
        for _, row in budget_df.iterrows():
            if should_show_label(row):
                ax1.annotate(
                    row['Country'], 
                    (row['Budget_Clean'], row['Total Medals']),
                    xytext=(5, 5),
                    textcoords='offset points',
                    fontsize=11,
                    color=colors['text'],
                    fontweight='bold',
                    alpha=0.9
                )
        
        # Enhanced plot styling
        ax1.grid(True, linestyle='--', alpha=0.4, color=colors['grid'])
        ax1.set_facecolor(colors['background'])
        for spine in ax1.spines.values():
            spine.set_color(colors['grid'])
        
        ax1.set_xlabel('Sports Budget (Million USD)', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Olympic Medals', fontsize=14, fontweight='bold')
        ax1.set_title('National Sports Budget vs Olympic Medals', 
                    fontsize=16, 
                    pad=20,
                    fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close()

        # Efficiency Analysis
        st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 20px 0;'>
            <h2 style='color: #1f1f1f; margin-bottom: 15px;'>Budget Efficiency Analysis 🎯</h2>
            <p style='font-size: 18px; color: #1f1f1f; line-height: 1.6;'>
                Examining how effectively countries convert their sports budget into Olympic medals.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create efficiency bar plot
        fig2, ax2 = plt.subplots(figsize=(12, 8))
        efficiency_data = budget_df.nlargest(10, 'Medals per Billion')
        
        bars = ax2.bar(
            efficiency_data['Country'], 
            efficiency_data['Medals per Billion'],
            color=colors['accent2'],
            alpha=0.8
        )
        
        # Enhanced bar plot styling
        ax2.grid(True, linestyle='--', alpha=0.3, color=colors['grid'], axis='y')
        ax2.set_axisbelow(True)
        ax2.set_facecolor(colors['background'])
        for spine in ax2.spines.values():
            spine.set_color(colors['grid'])
        
        # Rotate labels for better readability
        plt.xticks(rotation=45, ha='right', fontsize=12)
        
        # Add value labels with enhanced visibility
        for bar in bars:
            height = bar.get_height()
            ax2.text(
                bar.get_x() + bar.get_width()/2., 
                height,
                f'{height:.1f}',
                ha='center',
                va='bottom',
                fontsize=12,
                fontweight='bold'
            )
        
        ax2.set_title('Top 10 Countries: Olympic Medals per Billion USD',
                    fontsize=16,
                    pad=20,
                    fontweight='bold')
        ax2.set_xlabel('Country', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Medals per Billion USD', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

        # Data Table Section
        st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 20px 0;'>
            <h2 style='color: #1f1f1f; margin-bottom: 15px;'>Detailed Country Analysis 📊</h2>
            <p style='font-size: 18px; color: #1f1f1f; line-height: 1.6;'>
                Comprehensive breakdown of each country's budget allocation and medal achievements.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        styled_df = (budget_df[['Country', 'Budget_Clean', 'Total Medals', 'Medals per Billion']]
            .sort_values('Medals per Billion', ascending=False)
            .style
            .format({
                'Budget_Clean': '${:,.2f}M',
                'Medals per Billion': '{:.1f}',
                'Total Medals': '{:.0f}'
            })
            .background_gradient(cmap='RdYlBu', subset=['Medals per Billion'])
            .set_properties(**{
                'text-align': 'right',
                'font-size': '14px',
                'padding': '10px'
            })
            .set_table_styles([
                {'selector': 'th', 'props': [
                    ('background-color', colors['primary']),
                    ('color', 'white'),
                    ('font-weight', 'bold'),
                    ('padding', '12px'),
                    ('font-size', '16px')
                ]},
                {'selector': 'td', 'props': [('padding', '10px')]}
            ])
        )
        st.dataframe(styled_df, height=400)

    except Exception as e:
        st.error(f"Error loading or processing data: {str(e)}")
        st.write("Please check if the data file is in the correct location and format.")

elif selected_section == 'Age distribution by sport':
    np.random.seed(111)

    # Title with white text
    st.markdown("""
        <h1 style='color: black; margin: 0 0 24px 0;'>To what extent does the age of athletes affect their chances of succeeding in a particular sport? 👴🏼</h1>
    """, unsafe_allow_html=True)

    try:
        # Load data and filter out invalid measurements
        athlete_data = pd.read_csv("data/preprocessed_athlete_events.csv")
        valid_age_data = athlete_data[
            (athlete_data['Age'] != -1) & 
            (athlete_data['Height'] > 0) &  # Filter out zero heights
            (athlete_data['Weight'] > 0)     # Filter out zero weights
        ]
        
        # Display key age metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Average Athlete Age",
                f"{valid_age_data['Age'].mean():.1f} years"
            )
        with col2:
            st.metric(
                "Youngest Athlete",
                f"{valid_age_data['Age'].min():.0f} years"
            )
        with col3:
            st.metric(
                "Oldest Athlete",
                f"{valid_age_data['Age'].max():.0f} years"
            )

        # Physical Attributes Distribution Section with styled container
        st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 20px 0;'>
            <h2 style='color: #1f1f1f; margin-bottom: 15px;'>Athletes' Physical Attributes Distribution 📊</h2>
            <p style='font-size: 18px; color: #1f1f1f; line-height: 1.6; margin-bottom: 20px;'>
                Explore the distribution of athletes' height and weight across Olympic sports. The histograms show 
                the frequency of different physical measurements, with red lines indicating the mean values.
            </p>
        """, unsafe_allow_html=True)

        # Create two columns for the histograms
        hist_col1, hist_col2 = st.columns(2)

        with hist_col1:
            # Height histogram with enhanced styling    
            fig_height = plt.figure(figsize=(10, 6))
            plt.hist(valid_age_data['Height'], bins=30, color='#90EE90', alpha=0.7, edgecolor='black')
            plt.title('Distribution of Athletes\' Height', fontsize=14, fontweight='bold', pad=15)
            plt.xlabel('Height (cm)', fontsize=12, fontweight='bold')
            plt.ylabel('Number of Athletes', fontsize=12, fontweight='bold')
            plt.grid(True, alpha=0.3, linestyle='--')
            # Add mean line
            height_mean = valid_age_data['Height'].mean()
            plt.axvline(height_mean, color='#FF6B6B', linestyle='dashed', linewidth=2)
            plt.text(height_mean*1.02, plt.ylim()[1]*0.9, 
                    f'Mean: {height_mean:.1f} cm', 
                    color='#FF6B6B', 
                    fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig_height)

        with hist_col2:
            # Weight histogram with enhanced styling and limited range
            fig_weight = plt.figure(figsize=(10, 6))
            # Filter weights up to 150 kg
            filtered_weights = valid_age_data[valid_age_data['Weight'] <= 150]['Weight']
            plt.hist(filtered_weights, bins=30, color='#2E8B57', alpha=0.7, edgecolor='black')
            plt.title('Distribution of Athletes\' Weight', fontsize=14, fontweight='bold', pad=15)
            plt.xlabel('Weight (kg)', fontsize=12, fontweight='bold')
            plt.ylabel('Number of Athletes', fontsize=12, fontweight='bold')
            plt.grid(True, alpha=0.3, linestyle='--')
            # Set x-axis limit explicitly
            plt.xlim(0, 150)
            # Add mean line (using filtered data mean)
            weight_mean = filtered_weights.mean()
            plt.axvline(weight_mean, color='#FF6B6B', linestyle='dashed', linewidth=2)
            plt.text(weight_mean*1.02, plt.ylim()[1]*0.9, 
                    f'Mean: {weight_mean:.1f} kg', 
                    color='#FF6B6B', 
                    fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig_weight)

        # Physical attributes metrics with explanations
        st.markdown("""
            <p style='font-size: 18px; color: #1f1f1f; line-height: 1.6; margin-top: 20px;'>
                Key statistics about athletes' physical characteristics:
            </p>
        """, unsafe_allow_html=True)

        phys_col1, phys_col2, phys_col3 = st.columns(3)
        with phys_col1:
            st.metric(
                "Average Height",
                f"{valid_age_data['Height'].mean():.1f} cm",
                delta=f"±{valid_age_data['Height'].std():.1f} cm"
            )
        with phys_col2:
            st.metric(
                "Average Weight",
                f"{valid_age_data['Weight'].mean():.1f} kg",
                delta=f"±{valid_age_data['Weight'].std():.1f} kg"
            )
        with phys_col3:
            bmi = valid_age_data['Weight'] / ((valid_age_data['Height']/100) ** 2)
            st.metric(
                "Average BMI",
                f"{bmi.mean():.1f}",
                delta=f"±{bmi.std():.1f}"
            )
            
        # Close the styled container div
        st.markdown("""</div>""", unsafe_allow_html=True)

        # Introduction for age analysis
        st.markdown("""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 20px 0;'>
            <h2 style='color: #1f1f1f; margin-bottom: 15px;'>Understanding the Analysis 📊</h2>
            <p style='font-size: 20px; color: #1f1f1f; line-height: 1.6;'>
                <strong>The Age Distribution Plot</strong> reveals how athlete ages vary across different Olympic sports. 
                Each point represents an individual athlete, with black markers showing the median age for each sport.
            </p>
            <p style='font-size: 20px; color: #1f1f1f; line-height: 1.6;'>
                By examining these patterns, we can understand how age influences success in different sports, 
                from those favoring younger athletes to those where experience plays a crucial role.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Medal selection header without box - white text
        st.markdown("""
            <h2 style='color: black; margin: 20px 0 15px 0;'>Select Medal Type to Analyze 🏅</h2>
        """, unsafe_allow_html=True)

        # Custom CSS with specific text color rules for radio buttons
        st.markdown("""
        <style>
        div.stRadio > div[role='radiogroup'] > label {
            font-size: 20px !important;
            padding: 10px 25px !important;
            margin: 4px 8px !important;
            background-color: #f8f9fa !important;
            border-radius: 8px !important;
            transition: all 0.2s !important;
        }
        div.stRadio > div[role='radiogroup'] > label:hover {
            background-color: #e9ecef !important;
        }
        div.stRadio > div[role='radiogroup'] {
            display: flex !important;
            justify-content: center !important;
        }
        div.stRadio > div[role='radiogroup'] label p {
            color: black !important;
            font-weight: 500 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        medal_selection = st.radio(
            "",  # Empty label since we have the header above
            options=["All", "Gold", "Silver", "Bronze"],
            index=0,
            horizontal=True
        )

        # Sport selection header without box - white text
        st.markdown("""
            <h2 style='color: black; margin: 30px 0 15px 0;'>Select Sports to Compare 🎯</h2>
            <p style='font-size: 18px; color: white; line-height: 1.6; margin-bottom: 15px;'>
                Choose multiple sports to compare their age distributions. The visualization will update automatically.
            </p>
        """, unsafe_allow_html=True)

        # Get all unique sports and sort by average age
        sports_avg_age = valid_age_data.groupby('Sport')['Age'].mean().sort_values()
        all_sports = sports_avg_age.index.tolist()

        # Define default sports
        default_sports = [
            'Basketball', 'Football', 'Speed Skating',
            'Athletics', 'Ice Hockey', 'Swimming'
        ]
        default_sports_in_data = [s for s in default_sports if s in all_sports]

        # Sport selection
        selected_sports = st.multiselect(
            '',  # Empty label since we have the header above
            options=all_sports,
            default=default_sports_in_data
        )

        if len(selected_sports) > 0:
            # Data processing
            filtered_data = valid_age_data[valid_age_data['Sport'].isin(selected_sports)].copy()
            
            if medal_selection != "All":
                filtered_data = filtered_data[filtered_data['Medal'] == medal_selection]

            # Determine plot styling
            medal_colors = {
                "Gold": "#FFD700",
                "Silver": "#C0C0C0",
                "Bronze": "#CD7F32"
            }
            marker_color = medal_colors.get(medal_selection, None)

            # Calculate medians
            sport_medians = filtered_data.groupby('Sport')['Age'].mean().reindex(selected_sports)

            # Create visualization
            st.markdown("""
                <h2 style='color: black; margin: 20px 0 15px 0;'>Age Distribution Visualization 📈</h2>
            """, unsafe_allow_html=True)
            
            fig_width = max(20, len(selected_sports) * 1.5)
            fig_height = 10
            fig, ax = plt.subplots(figsize=(fig_width, fig_height))
            
            # Create enhanced stripplot
            sns.stripplot(
                data=filtered_data,
                x='Sport',
                y='Age',
                hue='Sport' if marker_color is None else None,
                palette='rainbow' if marker_color is None else None,
                color=marker_color,
                size=4,
                jitter=0.35,
                alpha=0.6,
                dodge=False,
                edgecolor='black',
                linewidth=0.5,
                ax=ax
            )

            # Add median markers
            for sport, median in sport_medians.items():
                x_coord = selected_sports.index(sport)
                ax.scatter(x_coord, median, color='black', s=100, zorder=5)
                ax.text(
                    x_coord, median + 1,
                    f'{median:.1f}',
                    color='black',
                    fontsize=12,
                    fontweight='bold',
                    ha='center'
                )

            # Enhanced plot styling
            ax.set_title(f"Age Distribution in Olympic Sports ({medal_selection} Medals)", 
                        fontsize=16, pad=20, fontweight='bold')
            ax.set_xlabel("Sport", fontsize=14, fontweight='bold')
            ax.set_ylabel("Age", fontsize=14, fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            ax.grid(True, linestyle='--', alpha=0.3)
            
            if marker_color is None:
                ax.legend(title='Sport', bbox_to_anchor=(1.05, 1), loc='upper left')
            
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)

            # Key insights section header
            st.markdown("""
                <h2 style='color: black; margin: 30px 0 15px 0;'>Key Insights 🔍</h2>
                <p style='font-size: 18px; color: white; line-height: 1.6; margin-bottom: 15px;'>
                    Statistical summary of the selected sports and medals:
                </p>
            """, unsafe_allow_html=True)

            stats_cols = st.columns(3)
            
            with stats_cols[0]:
                st.metric(
                    label="Mean Age",
                    value=f"{filtered_data['Age'].mean():.1f} years"
                )

            with stats_cols[1]:
                st.metric(
                    label="Age Standard Deviation",
                    value=f"±{filtered_data['Age'].std():.1f} years"
                )

            with stats_cols[2]:
                st.metric(
                    label="Age Range",
                    value=f"{filtered_data['Age'].max() - filtered_data['Age'].min():.1f} years"
                )

        else:
            st.warning("Please select at least one sport to display the visualization.")

    except Exception as e:
        st.error(f"Error loading or processing data: {str(e)}")
        st.write("Please check if the data file is in the correct location and format.")
