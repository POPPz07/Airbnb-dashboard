import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load cleaned dataset
def load_data():
    file_path = "Airbnb_Open_Data.csv"
    df = pd.read_csv(file_path)
    df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)
    df['service fee'] = df['service fee'].replace('[\$,]', '', regex=True).astype(float)
    df['last review'] = pd.to_datetime(df['last review'], errors='coerce')
    df.fillna({'reviews per month': 0, 'number of reviews': 0}, inplace=True)
    df.drop(columns=['license'], errors='ignore', inplace=True)

    # Ensure required columns exist
    required_columns = ['cancellation_policy', 'instant_bookable']
    for col in required_columns:
        if col not in df.columns:
            df[col] = 'Unknown'
    df.fillna({'cancellation_policy': 'Unknown', 'instant_bookable': 'Unknown'}, inplace=True)

    # Remove exact duplicate rows
    df = df.drop_duplicates()

    # Handle extreme outliers in minimum nights
    df = df[(df['minimum nights'] >= 1) & (df['minimum nights'] <= df['minimum nights'].quantile(0.99))]

    return df


df = load_data()

# Custom CSS for modern and clean styling
st.markdown("""
<style>
    /* General styling for headings */
    h1, h2, h3, h4, h5, h6 {
        color: #2E86C1;
        padding: 15px;
        border-radius: 10px;
        background-color: #F4F6F6;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    }

    /* Styling for metric boxes */
    .metric-box {
        border: 1px solid #D5D8DC;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        background-color: #F4F6F6;
        margin: 10px 0;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }
    .metric-box h3 {
        margin: 0;
        padding: 0;
    }
    .metric-box p {
        margin: 10px 0 0 0;
        padding: 0;
    }

    /* Styling for chart boxes */
    .chart-box {
        border: 1px solid #D5D8DC;
        border-radius: 10px;
        padding: 15px;
        background-color: #F4F6F6;
        margin: 10px 0;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }
    .chart-box h3 {
        margin: 0;
        padding: 0;
    }

    /* Styling for informative text */
    .info-text {
        padding: 15px;
        border-radius: 10px;
        background-color: #F4F6F6;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    }

    /* Styling for buttons */
    .stButton button {
        background-color: #2E86C1;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }

    /* Styling for the sidebar */
    .css-1d391kg {
        background-color: #2E86C1;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3, .css-1d391kg h4, .css-1d391kg h5, .css-1d391kg h6 {
        color: white;
    }

    /* Custom styling for radio buttons */
    .stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .stRadio > div > label {
        background-color: lightblue;
        color: white;
        padding: 10px;
        border-radius: 5px;
        transition: background-color 0.3s, color 0.3s;
        cursor: pointer;
        width: 100%;  
        text-align: center;  
        box-sizing: border-box;
    }
    .stRadio > div > label:hover {
        background-color: #57B9FF;
    }
    .stRadio > div > label > div:first-child {
        display: none; /* Hide the default radio button */
    }
</style>

<script>
    // JavaScript to enhance radio button interaction
    document.addEventListener("DOMContentLoaded", function() {
        const radioLabels = document.querySelectorAll('.stRadio > div > label');
        radioLabels.forEach(label => {
            label.addEventListener('click', () => {
                // Remove active class from all labels
                radioLabels.forEach(l => l.classList.remove('active'));
                // Add active class to the clicked label
                label.classList.add('active');
            });
        });
    });
</script>
""", unsafe_allow_html=True)

st.title("Airbnb Booking Insights Dashboard")

# Sidebar Navigation
menu = st.sidebar.radio("Select Analysis Section", [
    "Dashboard", "Listings Overview", "Detailed Insights", "Comparative Analysis", "Recommendation"
])

if menu == "Dashboard":

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-box">'
                    '<h3>Total Listings</h3>'
                    f'<p style="font-size: 20px; color: #2E86C1;">{df.shape[0]}</p>'
                    '</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box">'
                    '<h3>Average Price</h3>'
                    f'<p style="font-size: 20px; color: #E74C3C;">${df["price"].mean():.2f}</p>'
                    '</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box">'
                    '<h3>Average Availability</h3>'
                    f'<p style="font-size: 20px; color: #27AE60;">{df["availability 365"].mean():.1f} days/year</p>'
                    '</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-box">'
                    '<h3>Total Reviews</h3>'
                    f'<p style="font-size: 20px; color: #8E44AD;">{df["number of reviews"].sum()}</p>'
                    '</div>', unsafe_allow_html=True)

    # Row 1: Full-width Pie Chart with Legend
    st.markdown('<div class="chart-box">'
                '<h3>Cancellation Policy Distribution</h3>'
                '</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        # Cancellation Policy Distribution
        labels = df['cancellation_policy'].value_counts().index
        sizes = df['cancellation_policy'].value_counts().values
        colors = ['#2E86C1', '#E74C3C', '#27AE60', '#8E44AD', '#F1C40F'][:len(labels)]  # Dynamically adjust colors

        fig, ax = plt.subplots(figsize=(2, 1))
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 4})
        ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
        st.pyplot(fig)

    with col2:
        st.markdown("### Cancellation Policy Distribution")
        for i, (label, size) in enumerate(zip(labels, sizes)):
            st.markdown(f"<span style='color: {colors[i]};'>■</span> {label}: {size / sum(sizes) * 100:.1f}%",
                        unsafe_allow_html=True)

    # Row 2: Two-column layout for Price and Room Type Distribution
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-box">'
                    '<h3>Price Distribution</h3>'
                    '</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4, 3))
        sns.histplot(df['price'], bins=30, kde=True, color='#2E86C1', ax=ax)
        ax.set_xlabel("Price ($)")
        ax.set_ylabel("Number of Listings")
        st.pyplot(fig)

    with col2:
        st.markdown('<div class="chart-box">'
                    '<h3>Room Type Distribution</h3>'
                    '</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4, 3))
        df['room type'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['#E74C3C', '#27AE60', '#8E44AD'],
                                            ax=ax)
        ax.set_ylabel("")
        st.pyplot(fig)

    # Row 3: Three-column layout for Availability, Reviews, and Top Neighbourhoods
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="chart-box">'
                    '<h3>Availability Distribution</h3>'
                    '</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(3, 2))
        sns.histplot(df['availability 365'], bins=20, kde=True, color='#2E86C1', ax=ax)
        ax.set_xlabel("Availability (Days per Year)")
        ax.set_ylabel("Number of Listings")
        st.pyplot(fig)

    with col2:
        st.markdown('<div class="chart-box">'
                    '<h3>Reviews Distribution</h3>'
                    '</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(3, 2))
        sns.histplot(df['number of reviews'], bins=20, kde=True, color='#E74C3C', ax=ax)
        ax.set_xlabel("Number of Reviews")
        ax.set_ylabel("Number of Listings")
        st.pyplot(fig)

    with col3:
        st.markdown('<div class="chart-box">'
                    '<h3>Top Neighbourhood Groups by Average Price</h3>'
                    '</div>', unsafe_allow_html=True)
        top_neighbourhood_price = df.groupby('neighbourhood group')['price'].mean().sort_values(ascending=False).head(5)
        fig, ax = plt.subplots(figsize=(3, 2))
        top_neighbourhood_price.plot(kind='bar', color='#27AE60', ax=ax)
        ax.set_ylabel("Average Price ($)")
        ax.set_xlabel("Neighbourhood Group")
        st.pyplot(fig)

# Rest of the code for other pages remains unchanged...

elif menu == "Listings Overview":
    st.header("Listings Overview")

    # Searchable Dropdowns
    st.subheader("Available Locations")
    selected_country = st.selectbox("Search Country", ['All'] + sorted(df['country'].dropna().unique().tolist()))
    selected_neighbourhood_group = st.selectbox("Search Neighbourhood Group",
                                                ['All'] + sorted(df['neighbourhood group'].dropna().unique().tolist()))
    selected_neighbourhood = st.selectbox("Search Neighbourhood",
                                          ['All'] + sorted(df['neighbourhood'].dropna().unique().tolist()))
    selected_room_type = st.selectbox("Search Room Type", ['All'] + sorted(df['room type'].dropna().unique().tolist()))

    # Apply filters to the dataset
    filtered_df = df.copy()
    if selected_country != 'All':
            filtered_df = filtered_df[filtered_df['country'] == selected_country]
    if selected_neighbourhood_group != 'All':
        filtered_df = filtered_df[filtered_df['neighbourhood group'] == selected_neighbourhood_group]
    if selected_neighbourhood != 'All':
        filtered_df = filtered_df[filtered_df['neighbourhood'] == selected_neighbourhood]
    if selected_room_type != 'All':
        filtered_df = filtered_df[filtered_df['room type'] == selected_room_type]

    # Availability Insights
    st.subheader("Availability Insights")
    availability_bins = pd.cut(filtered_df['availability 365'], bins=[0, 100, 200, 300, 365],
                               labels=["0-100", "101-200", "201-300", "301-365"])
    availability_counts = availability_bins.value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(3, 2))
    availability_counts.plot(kind='bar', color='blue', ax=ax)
    ax.set_ylabel("Number of Listings", fontsize=5)
    ax.set_xlabel("Availability Range (Days per Year)", fontsize=5)
    ax.set_title("Availability Distribution Across Listings", fontsize=5)
    ax.tick_params(axis='both', labelsize=4)
    st.pyplot(fig)

if menu == "Detailed Insights":
    st.header("Detailed Insights")

    st.sidebar.header("Filter Options")
    selected_country = st.sidebar.selectbox("Select Country", ['All'] + list(df['country'].unique()))
    selected_neighbourhood_group = st.sidebar.selectbox("Select Neighbourhood Group",
                                                        ['All'] + list(df['neighbourhood group'].unique()))

    if selected_neighbourhood_group != 'All':
        available_neighbourhoods = df[df['neighbourhood group'] == selected_neighbourhood_group][
            'neighbourhood'].unique()
    else:
        available_neighbourhoods = df['neighbourhood'].unique()

    selected_neighbourhood = st.sidebar.selectbox("Select Neighbourhood", ['All'] + list(available_neighbourhoods))
    selected_room_type = st.sidebar.selectbox("Select Room Type", ['All'] + list(df['room type'].unique()))

    instant_book = st.sidebar.checkbox("Instant Bookable")
    cancellation_policy = st.sidebar.selectbox("Cancellation Policy",
                                               ['All', 'Strict', 'Moderate', 'Flexible', 'Unknown'])

    # Ensure the 'cancellation_policy' column exists and fill missing values with 'Unknown'
    if 'cancellation_policy' in df.columns:
        df['cancellation_policy'].fillna('Unknown', inplace=True)
    else:
        st.error("Column 'cancellation_policy' not found in the dataset.")

    min_nights = st.sidebar.slider("Minimum Nights", int(df['minimum nights'].min()), int(df['minimum nights'].max()),
                                   int(df['minimum nights'].median()))
    max_price = st.sidebar.slider("Maximum Price", int(df['price'].min()), int(df['price'].max()),
                                  int(df['price'].median()))

    filtered_df = df.copy()
    if selected_country != 'All':
        filtered_df = filtered_df[filtered_df['country'] == selected_country]
    if selected_neighbourhood_group != 'All':
        filtered_df = filtered_df[filtered_df['neighbourhood group'] == selected_neighbourhood_group]
    if selected_neighbourhood != 'All':
        filtered_df = filtered_df[filtered_df['neighbourhood'] == selected_neighbourhood]
    if selected_room_type != 'All':
        filtered_df = filtered_df[filtered_df['room type'] == selected_room_type]
    if instant_book:
        filtered_df = filtered_df[filtered_df['instant_bookable'] == 'TRUE']
    if cancellation_policy != 'All':
        filtered_df = filtered_df[filtered_df['cancellation_policy'] == cancellation_policy]
    filtered_df = filtered_df[filtered_df['minimum nights'] >= min_nights]
    filtered_df = filtered_df[filtered_df['price'] <= max_price]

    # Display total count of people who visited
    total_people = filtered_df['id'].nunique()
    st.subheader("Total People Visited")
    st.write(f"Total Visitors: {total_people}")

    # Display total host listings count
    total_host_listings = filtered_df['calculated host listings count'].sum()
    st.subheader("Total Host Listings Count")
    st.write(f"Total Host Listings: {total_host_listings}")

    # Price Distribution
    st.subheader("Price Distribution")
    fig, ax = plt.subplots(figsize=(6, 3))  # Smaller graph size
    sns.histplot(filtered_df['price'], bins=30, kde=True, color='green', ax=ax)
    ax.set_xlabel("Price ($)")
    ax.set_ylabel("Number of Listings")
    st.pyplot(fig)

    # Availability Insights
    st.subheader("Availability Distribution")
    fig, ax = plt.subplots(figsize=(6, 3))  # Smaller graph size
    sns.histplot(filtered_df['availability 365'], bins=20, kde=True, color='blue', ax=ax)
    ax.set_xlabel("Availability (Days per Year)")
    ax.set_ylabel("Number of Listings")
    st.pyplot(fig)

    # Reviews Analysis
    st.subheader("Reviews Distribution")
    fig, ax = plt.subplots(figsize=(6, 3))  # Smaller graph size
    sns.histplot(filtered_df['number of reviews'], bins=20, kde=True, color='purple', ax=ax)
    ax.set_xlabel("Number of Reviews")
    ax.set_ylabel("Number of Listings")
    st.pyplot(fig)

elif menu == "Comparative Analysis":
    st.header("Comparative Analysis")

    # Row 1: Three-column layout for Top Neighbourhood Groups by Average Price, Total Reviews, and Most Expensive Neighbourhoods
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="chart-box">'
                    '<h3>Top Neighbourhood Groups by Average Price</h3>'
                    '</div>', unsafe_allow_html=True)
        top_neighbourhood_price = df.groupby('neighbourhood group')['price'].mean().sort_values(ascending=False).head(5)
        fig, ax = plt.subplots(figsize=(4, 3))  # Smaller graph size
        top_neighbourhood_price.plot(kind='bar', color='orange', ax=ax)
        ax.set_ylabel("Average Price ($)")
        ax.set_xlabel("Neighbourhood Group")
        st.pyplot(fig)

    with col2:
        st.markdown('<div class="chart-box">'
                    '<h3>Top Neighbourhood Groups by Total Reviews</h3>'
                    '</div>', unsafe_allow_html=True)
        top_neighbourhood_reviews = df.groupby('neighbourhood group')['number of reviews'].sum().sort_values(
            ascending=False).head(5)
        fig, ax = plt.subplots(figsize=(4, 3))  # Smaller graph size
        top_neighbourhood_reviews.plot(kind='bar', color='purple', ax=ax)
        ax.set_ylabel("Total Reviews")
        ax.set_xlabel("Neighbourhood Group")
        st.pyplot(fig)

    with col3:
        st.markdown('<div class="chart-box">'
                    '<h3>Top 5 Most Expensive Neighbourhoods</h3>'
                    '</div>', unsafe_allow_html=True)
        top_expensive = df.groupby('neighbourhood')['price'].mean().sort_values(ascending=False).head(5)
        fig, ax = plt.subplots(figsize=(4, 3))  # Smaller graph size
        top_expensive.plot(kind='bar', color='red', ax=ax)
        ax.set_ylabel("Average Price ($)")
        st.pyplot(fig)

    # Row 2: Three-column layout for Most Reviewed Neighbourhoods, Room Type Distribution, and Average Price by Room Type
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="chart-box">'
                    '<h3>Top 5 Most Reviewed Neighbourhoods</h3>'
                    '</div>', unsafe_allow_html=True)
        top_reviewed = df.groupby('neighbourhood')['number of reviews'].sum().sort_values(ascending=False).head(5)
        fig, ax = plt.subplots(figsize=(4, 3))  # Smaller graph size
        top_reviewed.plot(kind='bar', color='purple', ax=ax)
        ax.set_ylabel("Total Reviews")
        st.pyplot(fig)

    with col2:
        st.markdown('<div class="chart-box">'
                    '<h3>Room Type Distribution</h3>'
                    '</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4, 3))  # Smaller graph size
        df['room type'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['gold', 'lightcoral', 'lightblue'],
                                            ax=ax)
        ax.set_ylabel("")
        st.pyplot(fig)

    with col3:
        st.markdown('<div class="chart-box">'
                    '<h3>Average Price by Room Type</h3>'
                    '</div>', unsafe_allow_html=True)
        avg_price_by_room = df.groupby('room type')['price'].mean().dropna()
        fig, ax = plt.subplots(figsize=(4, 3))  # Smaller graph size
        avg_price_by_room.sort_values().plot(kind='barh', color='orange', ax=ax)
        ax.set_xlabel("Average Price ($)")
        ax.set_ylabel("Room Type")
        st.pyplot(fig)

    # Row 3: Three-column layout for Total Listings by Room Type, Average Availability by Room Type, and Instant Bookable Listings
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="chart-box">'
                    '<h3>Total Listings by Room Type</h3>'
                    '</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4, 3))  # Smaller graph size
        df['room type'].value_counts().plot(kind='bar', color=['gold', 'lightcoral', 'lightblue'], ax=ax)
        ax.set_ylabel("Number of Listings")
        st.pyplot(fig)

    with col2:
        st.markdown('<div class="chart-box">'
                    '<h3>Average Availability by Room Type</h3>'
                    '</div>', unsafe_allow_html=True)
        availability_by_room = df.groupby('room type')['availability 365'].mean()
        fig, ax = plt.subplots(figsize=(4, 3))  # Smaller graph size
        availability_by_room.sort_values().plot(kind='bar', color=['gold', 'lightcoral', 'lightblue'], ax=ax)
        ax.set_ylabel("Average Availability (Days per Year)")
        ax.set_xlabel("Room Type")
        st.pyplot(fig)

    with col3:
        if 'instant_bookable' in df.columns:
            st.markdown('<div class="chart-box">'
                        '<h3>Instant Bookable Listings</h3>'
                        '</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(4, 3))  # Smaller graph size
            df['instant_bookable'].value_counts().plot(kind='pie', autopct='%1.1f%%',
                                                       labels=df['instant_bookable'].unique(),
                                                       colors=['red', 'green'], ax=ax)
            ax.set_ylabel("")
            st.pyplot(fig)
        else:
            st.write("Instant bookable data not available.")

elif menu == "Recommendation":
    st.header("Find the Best Airbnb for You!")

    # Dropdown for Neighbourhood Group
    selected_group = st.selectbox("Select Neighbourhood Group", sorted(df['neighbourhood group'].dropna().unique()))

    # Filter Neighbourhoods based on selected group
    filtered_neighbourhoods = df[df['neighbourhood group'] == selected_group]['neighbourhood'].dropna().astype(
        str).unique()
    selected_neighbourhood = st.selectbox("Select Neighbourhood", sorted(filtered_neighbourhoods))

    # Price input
    total_budget = st.number_input("Enter Your Total Budget ($)", min_value=0, value=100)

    # Number of nights
    num_nights = st.number_input("Enter Number of Nights", min_value=1, value=1)

    # Room Type selection (Added 'Any' option)
    room_types = ['Any'] + sorted(df['room type'].dropna().unique().tolist())
    selected_room_type = st.selectbox("Select Room Type", room_types)

    # Filter based on user selection
    filtered_df = df[(df['neighbourhood group'] == selected_group) &
                     (df['neighbourhood'] == selected_neighbourhood)]

    # Apply Room Type filter only if a specific type is selected
    if selected_room_type != 'Any':
        filtered_df = filtered_df[filtered_df['room type'] == selected_room_type]

    # Allow flexibility in budget (+/- 15%)
    price_lower = total_budget * 0.85
    price_upper = total_budget * 1.15
    filtered_df = filtered_df[(filtered_df['price'] + (filtered_df['service fee'] * num_nights) >= price_lower) &
                              (filtered_df['price'] + (filtered_df['service fee'] * num_nights) <= price_upper)]

    # Allow flexibility in nights (+/- 2 nights)
    filtered_df = filtered_df[(filtered_df['minimum nights'] >= max(1, num_nights - 2)) &
                              (filtered_df['minimum nights'] <= num_nights + 2)]

    if not filtered_df.empty:
        st.subheader("Available Locations")
        st.write(filtered_df[['NAME', 'price', 'service fee', 'room type', 'availability 365']])
    else:
        st.write("No available listings match your criteria.")