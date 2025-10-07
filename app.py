import streamlit as st
import json
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Bangalore House Price Predictor",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI with sound effects, navbar, and animations
st.markdown("""
    <style>
    .main {
        max-width: 1200px;
        padding: 2rem;
    }

    /* Page transition animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }

    /* Apply animations to main content */
    .main > div {
        animation: fadeInUp 0.6s ease-out;
    }

    .element-container {
        animation: slideInRight 0.5s ease-out;
    }

    h1, h2, h3 {
        animation: fadeInUp 0.7s ease-out;
    }

    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        height: 3em;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(69, 160, 73, 0.4);
    }
    .stButton>button:active {
        transform: scale(0.98);
    }

    .price-box {
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        margin: 20px 0;
        animation: scaleIn 0.5s ease-out;
    }

    .info-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #f0f2f6;
        margin: 10px 0;
        color: #000000;
        animation: fadeInUp 0.6s ease-out;
    }
    .info-box h4 {
        color: #1f1f1f;
        margin-bottom: 10px;
    }
    .info-box ul {
        color: #333333;
    }

    /* Fade animation for metrics */
    .stMetric {
        animation: scaleIn 0.5s ease-out;
    }

    /* Smooth transitions for plotly charts */
    .js-plotly-plot {
        animation: fadeInUp 0.8s ease-out;
    }
    </style>

    <script>
    // Sound effects
    const playSound = (type) => {
        const sounds = {
            click: 'data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTUIGWi77eeeTRAKT6fj77RhGgU0jNXwzn0vBSh+zPLaizsKF2G36+mhUhELTKXh8rNfGgU0i9Twz38xBSh+zPLaizsKF2G36+mhUhELTKXh8rNfGgU0i9Twz38xBSh+',
            hover: 'data:audio/wav;base64,UklGRhIAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YZAAAAAAQEZMU05UWVxdXVxZVlBKQ0A+Oz45ODc3Nzg5Ozw+QEREREVFREVFRERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERERE',
            expand: 'data:audio/wav;base64,UklGRhQAAABXQVZFZm10IBAAAAABAAEAIlYAAESsAAACABAAZGF0YQAA'
        };
        const audio = new Audio(sounds[type] || sounds.click);
        audio.volume = 0.3;
        audio.play().catch(e => console.log('Audio play failed:', e));
    };

    // Add click sound to buttons
    document.addEventListener('click', (e) => {
        if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
            playSound('click');
        }
    });

    // Add hover sound
    document.addEventListener('mouseover', (e) => {
        if (e.target.tagName === 'BUTTON' || e.target.closest('button')) {
            playSound('hover');
        }
    });

    // Add expand sound for expanders
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.target.classList && mutation.target.classList.contains('streamlit-expanderHeader')) {
                playSound('expand');
            }
        });
    });

    observer.observe(document.body, {
        attributes: true,
        subtree: true,
        attributeFilter: ['class']
    });
    </script>
""", unsafe_allow_html=True)

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Navigation buttons
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🏠 Home", key="btn_home", use_container_width=True):
        st.session_state.page = 'Home'
        st.rerun()
with col2:
    if st.button("🔮 Predict", key="btn_predict", use_container_width=True):
        st.session_state.page = 'Predict'
        st.rerun()
with col3:
    if st.button("📊 Visualizations", key="btn_viz", use_container_width=True):
        st.session_state.page = 'Visualizations'
        st.rerun()
with col4:
    if st.button("ℹ️ About", key="btn_about", use_container_width=True):
        st.session_state.page = 'About'
        st.rerun()

st.markdown("---")

# Load model and artifacts
@st.cache_resource
def load_saved_artifacts():
    """Load the trained model and location data"""
    with open("./src/models/artifacts/columns.json", 'r') as f:
        data_columns = json.load(f)['data_columns']
        locations = data_columns[4:]

    with open('./src/models/artifacts/bangalore_home_prices_model.pickle', 'rb') as f:
        model = pickle.load(f)

    return model, data_columns, locations

def get_estimated_price(location, sqft, bhk, bath, balcony, model, data_columns):
    """Predict house price based on inputs"""
    try:
        loc_index = data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = balcony
    x[3] = bhk

    if loc_index >= 0:
        x[loc_index] = 1

    return round(model.predict([x])[0], 2)

# Load dataset for visualizations
@st.cache_data
def load_data():
    df = pd.read_csv("./data/Bengaluru_House_Data.csv")
    df = df.dropna()
    df['bhk'] = df['size'].apply(lambda x: int(x.split()[0]) if isinstance(x, str) else 0)

    def convert_sqft_to_num(x):
        if isinstance(x, str):
            tokens = x.split('-')
            if len(tokens) == 2:
                return (float(tokens[0]) + float(tokens[1])) / 2
            try:
                return float(x)
            except:
                return None
        return x

    df['total_sqft'] = df['total_sqft'].apply(convert_sqft_to_num)
    df = df[df['total_sqft'].notna()]
    df['price_per_sqft'] = df['price'] * 100000 / df['total_sqft']
    df.location = df.location.apply(lambda x: x.strip() if isinstance(x, str) else x)

    return df

# Load artifacts
try:
    model, data_columns, locations = load_saved_artifacts()

    # PAGE: HOME
    if st.session_state.page == 'Home':
        st.title("🏠 Bangalore House Price Predictor")
        st.markdown("### Get accurate price predictions for houses in Bangalore")

        st.markdown("""
        This prediction model uses machine learning to estimate house prices in Bangalore based on:
        **Location/Area**, **Total square footage**, **Number of bedrooms (BHK)**, **Number of bathrooms**, and **Number of balconies**.
        """)

        expander_col1, expander_col2 = st.columns(2)

        with expander_col1:
            with st.expander("💡 Tips"):
                st.markdown("""
                - Prices are shown in **Lakhs** (1 Lakh = ₹100,000)
                - The model is trained on historical data from 2017-2018
                - Actual prices may vary based on current market conditions
                - Price per sq ft helps compare value across properties
                """)

        with expander_col2:
            with st.expander("📊 Dataset Info"):
                st.markdown("""
                - **Source**: Kaggle - Bengaluru House Price Data
                - **Size**: ~938 KB
                - **Data Period**: 2017-2018
                - **Total Entries**: 13,320 properties
                - **License**: CC0 Public Domain
                """)

        st.markdown("---")
        st.markdown("### 🚀 Quick Start")
        st.info("👉 Click on **🔮 Predict** in the navigation above to start predicting house prices!")

    # PAGE: PREDICT
    elif st.session_state.page == 'Predict':
        st.title("🔮 Price Prediction")
        st.markdown("### Enter property details to get an estimated price")

        st.subheader("📋 Enter Property Details")

        location = st.selectbox(
            "🗺️ Location",
            options=sorted(locations),
            help="Select the location/area in Bangalore"
        )

        input_col1, input_col2 = st.columns(2)

        with input_col1:
            total_sqft = st.number_input(
                "📏 Total Square Feet",
                min_value=300,
                max_value=30000,
                value=1000,
                step=50,
                help="Enter the total area in square feet"
            )

            bhk = st.selectbox(
                "🛏️ BHK",
                options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                index=2,
                help="Number of bedrooms"
            )

        with input_col2:
            bath = st.selectbox(
                "🚿 Bathrooms",
                options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                index=1,
                help="Number of bathrooms"
            )

            balcony = st.selectbox(
                "🏞️ Balconies",
                options=[0, 1, 2, 3, 4],
                index=1,
                help="Number of balconies"
            )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔮 Predict Price"):
            with st.spinner("Calculating price..."):
                predicted_price = get_estimated_price(
                    location, total_sqft, bhk, bath, balcony, model, data_columns
                )

                st.session_state['show_metrics'] = True
                st.session_state['predicted_price'] = predicted_price
                st.session_state['total_sqft'] = total_sqft
                st.session_state['bhk'] = bhk
                st.session_state['bath'] = bath

                st.markdown(f"""
                    <div class="price-box">
                        <h2>Estimated Price</h2>
                        <h1>₹ {predicted_price:,.2f} Lakhs</h1>
                        <p>≈ ₹ {predicted_price * 100000:,.0f}</p>
                    </div>
                """, unsafe_allow_html=True)

        if st.session_state.get('show_metrics', False):
            st.markdown("---")
            st.markdown("### 📊 Property Details")

            price_per_sqft = (st.session_state['predicted_price'] * 100000) / st.session_state['total_sqft']
            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)

            with metrics_col1:
                st.metric("💰 Price per sq ft", f"₹ {price_per_sqft:,.0f}")
            with metrics_col2:
                st.metric("📐 Total Area", f"{st.session_state['total_sqft']:,.0f} sq ft")
            with metrics_col3:
                st.metric("🏠 Configuration", f"{st.session_state['bhk']} BHK, {st.session_state['bath']} Bath")

    # PAGE: VISUALIZATIONS
    elif st.session_state.page == 'Visualizations':
        st.title("📊 Data Visualizations")
        st.markdown("### Explore the Bangalore housing dataset")

        df_viz = load_data()

        viz_tab1, viz_tab2, viz_tab3 = st.tabs(["📈 Price Comparison", "💰 Price Distribution", "🚿 Bathroom Analysis"])

        with viz_tab1:
            st.markdown("### 2 BHK vs 3 BHK Price Comparison by Location")

            top_locations = df_viz['location'].value_counts().head(20).index.tolist()
            selected_location = st.selectbox("Select Location for Comparison", top_locations, key="scatter_location")

            bhk2 = df_viz[(df_viz.location == selected_location) & (df_viz.bhk == 2)]
            bhk3 = df_viz[(df_viz.location == selected_location) & (df_viz.bhk == 3)]

            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=bhk2['total_sqft'], y=bhk2['price'],
                mode='markers',
                name='2 BHK',
                marker=dict(color='#4A90E2', size=8)
            ))
            fig1.add_trace(go.Scatter(
                x=bhk3['total_sqft'], y=bhk3['price'],
                mode='markers',
                name='3 BHK',
                marker=dict(color='#50C878', size=10, symbol='diamond')
            ))
            fig1.update_layout(
                xaxis_title="Total Square Feet Area",
                yaxis_title="Price (Lakhs)",
                title=f"Price vs Area - {selected_location}",
                hovermode='closest',
                height=500
            )
            st.plotly_chart(fig1, use_container_width=True)

        with viz_tab2:
            st.markdown("### Price per Square Feet Distribution")

            price_filtered = df_viz[df_viz['price_per_sqft'] < df_viz['price_per_sqft'].quantile(0.95)]

            fig2 = px.histogram(
                price_filtered,
                x='price_per_sqft',
                nbins=50,
                title='Distribution of Price per Square Feet',
                labels={'price_per_sqft': 'Price per Sq Ft (₹)'},
                color_discrete_sequence=['#667eea']
            )
            fig2.update_layout(
                xaxis_title="Price per Square Feet (₹)",
                yaxis_title="Count",
                showlegend=False,
                height=500
            )
            st.plotly_chart(fig2, use_container_width=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average", f"₹ {df_viz['price_per_sqft'].mean():,.0f}")
            with col2:
                st.metric("Median", f"₹ {df_viz['price_per_sqft'].median():,.0f}")
            with col3:
                st.metric("Std Dev", f"₹ {df_viz['price_per_sqft'].std():,.0f}")

        with viz_tab3:
            st.markdown("### Number of Bathrooms Distribution")

            bath_counts = df_viz['bath'].value_counts().sort_index()

            fig3 = px.bar(
                x=bath_counts.index,
                y=bath_counts.values,
                labels={'x': 'Number of Bathrooms', 'y': 'Count'},
                title='Distribution of Bathrooms',
                color=bath_counts.values,
                color_continuous_scale='Viridis'
            )
            fig3.update_layout(
                xaxis_title="Number of Bathrooms",
                yaxis_title="Count",
                showlegend=False,
                height=500
            )
            st.plotly_chart(fig3, use_container_width=True)

    # PAGE: ABOUT
    elif st.session_state.page == 'About':
        st.title("ℹ️ About This Project")
        st.markdown("### Bangalore House Price Prediction using Machine Learning")

        st.markdown("""
        ## 📖 Overview
        This application predicts house prices in Bangalore using a Linear Regression model trained on historical data.

        ## 🎯 Features
        - **237+ Locations** - Covers major areas in Bangalore
        - **Real-time Predictions** - Get instant price estimates
        - **Interactive Visualizations** - Explore the dataset
        - **Responsive Design** - Works on all devices

        ## 🛠️ Technology Stack
        - **Frontend**: Streamlit
        - **ML Model**: Linear Regression (scikit-learn)
        - **Visualizations**: Plotly
        - **Data Processing**: Pandas, NumPy

        ## 📊 Model Performance
        - **R² Score**: 0.8585
        - **Training Data**: 6,958 properties
        - **Features**: 241 (including location encodings)

        ## 📄 Dataset
        - **Source**: Kaggle - Bengaluru House Price Data
        - **Size**: ~938 KB
        - **Period**: 2017-2018
        - **Total Entries**: 13,320 properties
        - **License**: CC0 Public Domain

        ## 🤝 Credits
        Built with ❤️ using Streamlit and Machine Learning
        """)

    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>Built with ❤️ using Streamlit and Machine Learning</p>",
        unsafe_allow_html=True
    )

except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    st.info("Please ensure the artifacts folder contains the required model and columns files.")
