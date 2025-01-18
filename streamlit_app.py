import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import zipfile
import os
import numpy as np
import zipfile
import os

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
    ['Opening', 'Roi', 'Idan', 'Amit', 'Alex']
)

if selected_section == 'Opening':
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

elif selected_section == 'Roi':
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
    ## :bar_chart: Olympic Athletes Analysis: Height and Weight by Event and Sex
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

elif selected_section == 'Idan':
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
    st.markdown("### 🎯 Select a Sport to Analyze:")
    selected_sport = st.selectbox("", sports_list)  # Empty string to avoid double label
    sport_data = data[data['Sport'] == selected_sport]
    
    # Scatter Plot
    st.markdown("## 📈 Scatter Plot: Height vs. Weight by Medal")
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
    st.markdown("## 📊 Bar Plot: Average Height and Weight by Medal")
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
        <h2 style='color: #1f1f1f; margin-bottom: 15px;'>🔍 Key Insights</h2>
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
  
elif selected_section == 'Amit':
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
            <h2 style='color: #1f1f1f; margin-bottom: 15px;'>🎯 Budget Efficiency Analysis</h2>
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
            <h2 style='color: #1f1f1f; margin-bottom: 15px;'>📊 Detailed Country Analysis</h2>
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

elif selected_section == 'Alex':

    np.random.seed(111)

    # Main content container
    with st.container():
        st.title("To what extent does the age of athletes affect their chances of succeeding in a particular sport? 👴🏼")
        
        st.markdown("""
        The age distribution plot shows the spread of ages for athletes across various sports. 
        Different sports display varying age ranges, suggesting that success in certain sports may correlate with specific age brackets. 
        For example, sports like swimming and athletics show younger peak ages, while sports like basketball and ice hockey exhibit a 
        broader range, possibly allowing older athletes to succeed.
        """)
        
        # Medal highlight options using radio buttons
        medal_selection = st.radio(
            "Highlight Medals:",
            options=["All", "Gold", "Silver", "Bronze"],
            index=0
        )

        # Load data from CSV
        athlete_data = pd.read_csv("data/preprocessed_athlete_events.csv")

        # Get all unique sports and sort by average age
        sports_avg_age = athlete_data.groupby('Sport')['Age'].mean().sort_values()
        all_sports = sports_avg_age.index.tolist()

        # Define default sports
        default_sports = [
            'Basketball', 'Football', 'Speed Skating',
            'Athletics', 'Ice Hockey', 'Swimming'
        ]

        # Filter defaults to only those that exist in the data
        default_sports_in_data = [s for s in default_sports if s in all_sports]

        # Multiselect of sports 
        selected_sports = st.multiselect(
            'Select Sports:',
            options=all_sports,
            default=default_sports_in_data
        )

        if len(selected_sports) > 0:
            # Filter to selected sports
            filtered_data = athlete_data[athlete_data['Sport'].isin(selected_sports)].copy()

            # Replace -1 values in Age column with the mean age of this subset
            mean_age = filtered_data['Age'].replace(-1, np.nan).mean()
            filtered_data['Age'] = filtered_data['Age'].replace(-1, mean_age)

            # If a specific medal is selected, filter the data accordingly
            if medal_selection != "All":
                filtered_data = filtered_data[filtered_data['Medal'] == medal_selection]

            # Determine plot styling based on medal selection
            if medal_selection == "Gold":
                marker_color = "#FFD700"  # Gold color
            elif medal_selection == "Silver":
                marker_color = "#C0C0C0"  # Silver color
            elif medal_selection == "Bronze":
                marker_color = "#CD7F32"  # Bronze color
            else:
                marker_color = None  # Default rainbow for all

            # Calculate the median age for each sport
            sport_medians = filtered_data.groupby('Sport')['Age'].mean().reindex(selected_sports)

            # Create figure with dynamic size based on the number of sports
            fig_width = max(20, len(selected_sports) * 1.5)  # Adjust width
            fig_height = 10
            
            fig, ax = plt.subplots(figsize=(fig_width, fig_height))
            
            # Draw a stripplot with medal-specific or rainbow palette
            sns.stripplot(
                data=filtered_data,
                x='Sport',
                y='Age',
                hue='Sport' if marker_color is None else None,  # Hue for all sports or none
                palette='rainbow' if marker_color is None else None,  # Rainbow for all sports
                color=marker_color,  # Medal-specific color
                size=4,
                jitter=0.35,
                alpha=0.6,
                dodge=False,
                edgecolor='black',
                linewidth=0.5,
                ax=ax
            )

            # Add median points for each sport
            for sport, median in sport_medians.items():
                # Find the x-coordinate for the sport
                x_coord = selected_sports.index(sport)
                ax.scatter(x_coord, median, color='black', s=100, zorder=5)
                ax.text(
                    x_coord, median + 1,  # Slightly above the median point
                    f'{median:.1f}',
                    color='black',
                    fontsize=12,
                    fontweight='bold',
                    ha='center'
                )

            # Customize the plot
            ax.set_title(f"Age Distribution in Olympic Sports ({medal_selection} Medals)", fontsize=16, pad=20)
            ax.set_xlabel("Sport", fontsize=14)
            ax.set_ylabel("Age", fontsize=14)
            plt.xticks(rotation=45, ha='right')
            ax.grid(True)  # Add gridlines for better readability

            # Place legend outside to the right (only for "All" selection)
            if marker_color is None:
                ax.legend(title='Sport', bbox_to_anchor=(1.05, 1), loc='upper left')
            
            # Adjust layout to prevent label cutoff
            plt.tight_layout()
            
            # Use the full width of the page for the plot
            st.pyplot(fig, use_container_width=True)

                        # Calculate key insights
            mean_age_all = filtered_data['Age'].mean()
            std_age = filtered_data['Age'].std()
            max_age = filtered_data['Age'].max()

            # Display key insights in metrics style
            stats_cols = st.columns(3)

            with stats_cols[0]:
                st.metric(
                    label="Mean Age",
                    value=f"{mean_age_all:.1f} years",
                    delta=None  # No delta needed here
                )

            with stats_cols[1]:
                st.metric(
                    label="Standard Deviation of Age",
                    value=f"{std_age:.1f}",
                    delta=None  # No delta needed here
                )

            with stats_cols[2]:
                st.metric(
                    label="Maximum Age",
                    value=f"{max_age:.1f} years",
                    delta=None  # No delta needed here
                )

        else:
            st.write("Please select at least one sport to display the visualization.")
