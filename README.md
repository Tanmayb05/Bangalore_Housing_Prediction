# Bangalore_Housing_Prediction
Bangalore Housing Prediction Using Python, Machine Learning & Modern Web Frameworks

## 📊 Dataset Information

### Bengaluru House Price Data
This dataset contains housing data from Bengaluru (Bangalore), India, and is widely used for real estate price prediction, data analysis, and regression modeling, especially in the context of Indian urban markets.

#### Dataset Summary
- **Source:** Kaggle (Bengaluru House Price Data)
- **File:** `Bengaluru_House_Data.csv`
- **Size:** ~938 KB
- **Popularity:** 89K+ downloads, 321K+ views on Kaggle
- **License:** CC0: Public Domain—free for use without restriction

#### Year/Timeframe
- **Data Collection Years:** Primarily 2017–2018, with some entries possibly up to 2019 or 2020
- **Example availability dates:** "18-Dec", "19-Dec", "20-Dec", "21-Dec" suggest listings primarily in 2017–2018

#### Features / Columns

| Column Name | Description |
|------------|-------------|
| `area_type` | Type of area (e.g., super built-up, plot area, built-up) |
| `availability` | Availability status or date (e.g., ready to move, 18-Dec) |
| `location` | Area within Bengaluru |
| `size` | Number of bedrooms (BHK), e.g., '2 BHK' |
| `society` | Name of housing society (many entries are null) |
| `total_sqft` | Total covered area (sq ft) |
| `bath` | Number of bathrooms |
| `balcony` | Number of balconies |
| `price` | Price (in lakhs; 1 lakh = 100,000 INR) |

#### Sample Entries
- Super built-up Area | Ready To Move | Whitefield | 2 BHK | DuenaTa | 1170 | 2 | 1 | 38
- Plot Area | Ready To Move | Gandhi Bazar | 6 Bedroom | 1020 | 6 | 370
- Built-up Area | Ready To Move | Uttarahalli | 3 BHK | 1440 | 2 | 3 | 62

#### Use Cases
- Predicting house prices in Bengaluru using machine learning models
- Exploratory data analysis and visualization
- Studying impact of features like size, locality, and amenities on price
- Market pattern analysis post-demonetization, regulatory changes, etc.

#### Tags
Real estate, Regression, India, Data cleaning, Housing market

---

## 🚀 Quick Start

### Option 1: Streamlit App (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd Bangalore_Housing_Prediction
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:
```bash
streamlit run app_streamlit.py
```

4. Open your browser to `http://localhost:8501`

### Option 2: Flask API + HTML Frontend

1. Clone The Repository In Your Computer.
2. Install dependencies: `pip install -r requirements.txt`
3. Type "python server.py" in the command prompt.
4. The server will start.
5. Open `templates/app.html` in your default browser.
6. Enter the inputs and click on estimate to get the Price Prediction.

## 📦 Deployment

### Deploy Streamlit App

**Streamlit Community Cloud:**
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy with one click!

**Heroku:**
```bash
# Create Procfile for Streamlit
echo "web: streamlit run app_streamlit.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create your-app-name
git push heroku master
```

### Deploy Flask App

**Heroku:**
```bash
heroku create your-app-name
git push heroku master
```

The existing `Procfile` is configured for Flask deployment.
