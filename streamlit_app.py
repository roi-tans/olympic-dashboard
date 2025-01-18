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
    st.header(f'{metric_type} Height and Weight by Country', divider='gray')
    

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 7))
    

    # Calculate bar positions
    x = np.arange(len(filtered_athletes_df['region'].unique()))
    width = 0.35

    # Create bars
    height_bars = ax.bar(x - width/2, 
                        filtered_athletes_df[height_col], 
                        width, 
                        label='Height',
                        color='#4A90E2',  # Nice blue color
                        alpha=0.8)

    weight_bars = ax.bar(x + width/2, 
                        filtered_athletes_df[weight_col], 
                        width, 
                        label='Weight',
                        color='#F39C12',  # Nice gold color
                        alpha=0.8)

    # Customize the plot
    ax.set_title(f'{metric_type} Height and Weight of Athletes by Country')
    ax.set_xlabel('Country (region)')
    ax.set_ylabel(f'{metric_type} Value')

    # Set x-axis ticks
    ax.set_xticks(x)
    ax.set_xticklabels(filtered_athletes_df['region'], rotation=45, ha='right')

    # Add value labels on the bars
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom')

    add_value_labels(height_bars)
    add_value_labels(weight_bars)

    # Add legend
    ax.legend()

    # Adjust layout
    plt.tight_layout()

    # Show the plot in Streamlit
    st.pyplot(fig)

    # Display the filtered data in a table
    st.header(f'{metric_type} Height and Weight Data', divider='gray')
    st.dataframe(filtered_athletes_df[['region', height_col, weight_col]])
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
    tab1, tab2, tab3 = st.tabs(["Height vs Weight Analysis", "Event Comparisons", "Country Analysis"])

    with tab1:

        st.header('Analysis')

        # Simple scatter plot with regression line
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=filtered_grouped_df, 
                        x='mean_height', 
                        y='mean_weight',
                        s=100)
        sns.regplot(data=filtered_grouped_df, 
                    x='mean_height', 
                    y='mean_weight',
                    scatter=False,
                    color='red')
        st.pyplot(fig)

    with tab2:
        st.header('Event Analysis', divider='gray')
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Height by Event Box Plot
            fig_height, ax_height = plt.subplots(figsize=(10, len(chosen_events)*0.4 + 6))
            sns.boxplot(
                data=filtered_grouped_df,
                y='Event',
                x='mean_height',
                orient='h',
                ax=ax_height
            )
            ax_height.set_title('Height Distribution by Event')
            ax_height.set_xlabel('Height (cm)')
            st.pyplot(fig_height)
        
        with col2:
            # Weight by Event Box Plot
            fig_weight, ax_weight = plt.subplots(figsize=(10, len(chosen_events)*0.4 + 6))
            sns.boxplot(
                data=filtered_grouped_df,
                y='Event',
                x='mean_weight',
                orient='h',
                ax=ax_weight
            )
            ax_weight.set_title('Weight Distribution by Event')
            ax_weight.set_xlabel('Weight (kg)')
            st.pyplot(fig_weight)

    with tab3:
        st.header('Country Comparison', divider='gray')
        
        # Calculate average BMI for each country
        filtered_grouped_df['BMI'] = filtered_grouped_df['mean_weight'] / (filtered_grouped_df['mean_height']/100)**2
        
        country_stats = filtered_grouped_df.groupby('region').agg({
            'mean_height': 'mean',
            'mean_weight': 'mean',
            'BMI': 'mean'
        }).round(2)
        
        # Create bar chart comparing countries
        fig_countries, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6))
        
        # Height comparison
        sns.barplot(data=filtered_grouped_df, x='region', y='mean_height', ci=None, ax=ax1)
        ax1.set_title('Average Height by Country')
        ax1.set_ylabel('Height (cm)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Weight comparison
        sns.barplot(data=filtered_grouped_df, x='region', y='mean_weight', ci=None, ax=ax2)
        ax2.set_title('Average Weight by Country')
        ax2.set_ylabel('Weight (kg)')
        ax2.tick_params(axis='x', rotation=45)
        
        # BMI comparison
        sns.barplot(data=filtered_grouped_df, x='region', y='BMI', ci=None, ax=ax3)
        ax3.set_title('Average BMI by Country')
        ax3.set_ylabel('BMI')
        ax3.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        st.pyplot(fig_countries)
        
        # Display detailed statistics
        st.subheader('Detailed Country Statistics')
        st.dataframe(country_stats.style.format({
            'mean_height': '{:.1f} cm',
            'mean_weight': '{:.1f} kg',
            'BMI': '{:.1f}'
        }))

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
    st.title("Olympic Athletes: Physical Attributes and Medal Achievements")
    
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
    
    data = load_data()
    
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
