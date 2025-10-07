import streamlit as st
import json
import pickle
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Bangalore House Price Predictor",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI with sound effects
st.markdown("""
    <style>
    .main {
        max-width: 1200px;
        padding: 2rem;
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
    }
    .info-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #f0f2f6;
        margin: 10px 0;
        color: #000000;
    }
    .info-box h4 {
        color: #1f1f1f;
        margin-bottom: 10px;
    }
    .info-box ul {
        color: #333333;
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

# Load artifacts
try:
    model, data_columns, locations = load_saved_artifacts()

    # Header
    st.title("🏠 Bangalore House Price Predictor")
    st.markdown("### Get accurate price predictions for houses in Bangalore")

    # About section - always visible
    st.markdown("""
    This prediction model uses machine learning to estimate house prices in Bangalore based on:
    **Location/Area**, **Total square footage**, **Number of bedrooms (BHK)**, **Number of bathrooms**, and **Number of balconies**.
    """)

    # Tips and Quick Stats side by side
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

    # Main content in single column
    st.subheader("📋 Enter Property Details")

    # Location selection
    location = st.selectbox(
        "🗺️ Location",
        options=sorted(locations),
        help="Select the location/area in Bangalore"
    )

    # Create sub-columns for numeric inputs
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

    # Predict button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔮 Predict Price"):
        with st.spinner("Calculating price..."):
            predicted_price = get_estimated_price(
                location, total_sqft, bhk, bath, balcony, model, data_columns
            )

            # Store in session state
            st.session_state['show_metrics'] = True
            st.session_state['predicted_price'] = predicted_price
            st.session_state['total_sqft'] = total_sqft
            st.session_state['bhk'] = bhk
            st.session_state['bath'] = bath

            # Display result
            st.markdown(f"""
                <div class="price-box">
                    <h2>Estimated Price</h2>
                    <h1>₹ {predicted_price:,.2f} Lakhs</h1>
                    <p>≈ ₹ {predicted_price * 100000:,.0f}</p>
                </div>
            """, unsafe_allow_html=True)

    # Additional metrics in full width below prediction
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

    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: gray;'>Built with ❤️ using Streamlit and Machine Learning</p>",
        unsafe_allow_html=True
    )

except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    st.info("Please ensure the artifacts folder contains the required model and columns files.")
