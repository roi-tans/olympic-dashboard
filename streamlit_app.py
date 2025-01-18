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

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Athletes Physical Characteristics Dashboard',
    page_icon=':athletic_shoe:',  # Emoji for a sports theme
    layout='wide',  # Set layout to wide mode
    initial_sidebar_state='expanded'

)

# Declare some useful functions.

# Create a sidebar menu
selected_section = st.sidebar.selectbox(
    'Select Visualization Section',
    ['Roi', 'Idan', 'Amit', 'Alex']
)

# Display content based on selected section
if selected_section == 'Roi':
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
    st.header('amitbenzona', divider='gray')
    # כותרת האפליקציה
    st.title("Is there a correlation between height or weight and winning medals, and if so, in which sports? 🏅")
    st.markdown("""The scatter plot shows each athlete’s height and weight, with dots colored by medal. This allows
    us to see how individual physiques are distributed, spot trends, and identify any outliers. The bar plot compares
    the average height and weight across the three medal categories, making it clear at a glance if one group tends to
    be taller or heavier than the others.
    """)   
    
    # טעינת הנתונים מתוך קובץ zip
    @st.cache_data
    def load_data():
        zip_file_path = 'data/athlete_events.csv.zip'
        csv_file_path = 'data/athlete_events.csv'
        
        # חילוץ הקובץ אם הוא לא חולץ עדיין
        if not os.path.exists(csv_file_path):
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall('data/')
        
        # קריאת הקובץ
        data = pd.read_csv(csv_file_path)
        return data
    
    data1 = load_data()

    data = data1[
    (data1['Height'] != -1) &
    (data1['Weight'] != -1)
]

    # ניקוי בסיסי של הנתונים
    data = data.dropna(subset=['Height', 'Weight', 'Medal', 'Year'])
    
    # בחירת ענף ספורט מתוך רשימת האפשרויות
    sports_list = data['Sport'].unique().tolist()
    selected_sport = st.selectbox("Select a Sport:", sports_list)
    
    # סינון לפי ענף הספורט הנבחר
    sport_data = data[data['Sport'] == selected_sport]
    
    # יצירת גרף פיזור לפי ענף ספורט ומדליה
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
    
    # גרף עמודות ממוצע גובה ומשקל לפי מדליה
    st.write("### Bar Plot: Average Height and Weight by Medal")
    avg_data = sport_data.groupby('Medal')[['Height', 'Weight']].mean().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=avg_data.melt(id_vars='Medal'), x='Medal', y='value', hue='variable', palette='muted', ax=ax)
    plt.xlabel('Medal')
    plt.ylabel('Average Value')
    plt.title(f'{selected_sport}: Average Height and Weight by Medal')
    st.pyplot(fig)
    
    # הוספת מידע נוסף
    st.write("### Insights:")
    st.write("- The scatter plot shows how height and weight vary across medal types.")
    st.write("- The bar plot provides an average comparison of height and weight across medal categories.")
    st.write("- Outliers and clusters can be observed using the scatter plot.")

  
elif selected_section == 'Amit':
    # Define color scheme
    colors = {
        'primary': '#1f77b4',    # Blue
        'accent': '#2ecc71',     # Green
        'text': '#2c3e50',       # Dark Gray
        'grid': '#ecf0f1',       # Light Gray
        'background': '#ffffff'   # White
    }

    st.title("Exploring the correlation between national sports budgets and Olympic performance 💸")
    st.markdown("""
        The scatter plot shows a positive relationship between a country's sports budget and Olympic medals won, indicating that 
        higher budgets may contribute to better performance. The bar plot highlights countries with the most efficient medal production relative
        to their budget, showing that some nations achieve high success despite smaller budgets.
        """)
    try:
        # Load the data
        budget_df = pd.read_csv('data/Correlation Sports Budget to Olympic Medals.csv', sep=';')
        
        # Clean the budget data
        budget_df['Budget_Clean'] = (budget_df['Total 2017-2019 (MM U$D)']
            .str.replace('$', '')
            .str.replace(' ', '')
            .str.replace('.', '')
            .str.replace(',', '.')
            .astype(float))
        
        budget_df['Total Medals'] = pd.to_numeric(budget_df['Total Medals'])

        # Enhanced metrics display
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Budget (MM USD)", 
                    f"${budget_df['Budget_Clean'].mean():,.2f}",
                    delta_color="normal")
        with col2:
            st.metric("Average Medals", 
                    f"{budget_df['Total Medals'].mean():.1f}")
        with col3:
            correlation = budget_df['Budget_Clean'].corr(budget_df['Total Medals'])
            st.metric("Budget-Medals Correlation", 
                    f"{correlation:.2f}")

        # Create scatter plot
        fig1 = plt.figure(figsize=(12, 7))
        ax1 = fig1.add_subplot(111)
        
        # Function to determine which countries to label
        def should_show_label(row):
            medals_per_billion = (row['Total Medals'] / row['Budget_Clean']) * 1000
            return (row['Total Medals'] > 20 or 
                    row['Budget_Clean'] > 10000 or 
                    medals_per_billion > 2.0 or 
                    row['Country'] in ['Hungary', 'Netherlands', 'Spain'])

        # Plot points
        ax1.scatter(budget_df['Budget_Clean'], 
                budget_df['Total Medals'],
                s=100,
                alpha=0.7,
                color=colors['primary'])
        
        # Add labels for selected countries
        for _, row in budget_df.iterrows():
            if should_show_label(row):
                ax1.annotate(row['Country'], 
                            (row['Budget_Clean'], row['Total Medals']),
                            xytext=(5, 5),
                            textcoords='offset points',
                            fontsize=9,
                            color=colors['text'],
                            alpha=0.8)
        
        # Style the plot
        ax1.grid(True, linestyle='--', alpha=0.7, color=colors['grid'])
        ax1.set_facecolor(colors['background'])
        for spine in ax1.spines.values():
            spine.set_color(colors['grid'])
        
        ax1.set_xlabel('Sports Budget (Million USD)', fontsize=12, color=colors['text'])
        ax1.set_ylabel('Olympic Medals', fontsize=12, color=colors['text'])
        ax1.set_title('National Sports Budget vs Olympic Medals', 
                    fontsize=14, 
                    color=colors['text'],
                    pad=20)
        
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close()

        # Efficiency analysis
        st.subheader("Budget Efficiency Analysis", divider='gray')
        budget_df['Medals per Billion'] = (budget_df['Total Medals'] / budget_df['Budget_Clean']) * 1000
        
        # Create efficiency bar plot
        fig2 = plt.figure(figsize=(12, 7))
        ax2 = fig2.add_subplot(111)
        efficiency_data = budget_df.nlargest(10, 'Medals per Billion')
        
        bars = ax2.bar(efficiency_data['Country'], 
                    efficiency_data['Medals per Billion'],
                    color=colors['accent'],
                    alpha=0.8)
        
        # Style the plot
        ax2.grid(True, linestyle='--', alpha=0.3, color=colors['grid'], axis='y')
        ax2.set_axisbelow(True)
        ax2.set_facecolor(colors['background'])
        for spine in ax2.spines.values():
            spine.set_color(colors['grid'])
        
        plt.xticks(rotation=45, ha='right')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center',
                    va='bottom',
                    color=colors['text'],
                    fontsize=10)
        
        ax2.set_title('Top 10 Countries: Olympic Medals per Billion USD',
                    fontsize=14,
                    color=colors['text'],
                    pad=20)
        ax2.set_xlabel('Country', fontsize=12, color=colors['text'])
        ax2.set_ylabel('Medals per Billion USD', fontsize=12, color=colors['text'])
        
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

        # Data table
        st.subheader("Detailed Data", divider='gray')
        styled_df = (budget_df[['Country', 'Budget_Clean', 'Total Medals', 'Medals per Billion']]
            .sort_values('Medals per Billion', ascending=False)
            .style
            .format({
                'Budget_Clean': '${:,.2f}M',
                'Medals per Billion': '{:.1f}',
                'Total Medals': '{:.0f}'
            })
            .background_gradient(cmap='Blues', subset=['Medals per Billion'])
            .set_properties(**{'text-align': 'right'})
            .set_table_styles([
                {'selector': 'th', 'props': [('background-color', colors['primary']), 
                                        ('color', 'white'),
                                        ('font-weight', 'bold'),
                                        ('padding', '8px')]},
                {'selector': 'td', 'props': [('padding', '8px')]}
            ])
        )
        st.dataframe(styled_df)

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
