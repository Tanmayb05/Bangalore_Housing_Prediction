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

## 📁 Project Structure

```
Bangalore_Housing_Prediction/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Git ignore rules
│
├── data/                       # Dataset files
│   └── Bengaluru_House_Data.csv
│
├── notebooks/                  # Jupyter notebooks for analysis
│   └── CodeBasics Data Science Project - Housing Price Prediction.ipynb
│
├── src/                        # Source code
│   ├── models/                 # Trained models
│   │   └── artifacts/
│   │       ├── bangalore_home_prices_model.pickle
│   │       └── columns.json
│   │
│   └── utils/                  # Utility scripts
│       └── retrain_model.py    # Model training script
│
└── .venv/                      # Virtual environment (gitignored)
```

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd Bangalore_Housing_Prediction
```

2. Create a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Streamlit app:
```bash
streamlit run app.py
```

5. Open your browser to `http://localhost:8501`

## 📦 Deployment

### Streamlit Community Cloud (Recommended)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Deploy with one click!

### Other Platforms

**Heroku:**
```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create your-app-name
git push heroku master
```

**Railway/Render:**
- Connect your GitHub repository
- Set start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
- Deploy automatically

## 🔧 Retrain Model

To retrain the model with updated data:

```bash
cd src/utils
python retrain_model.py
```

This will:
- Load data from `data/Bengaluru_House_Data.csv`
- Clean and preprocess the data
- Train a Linear Regression model
- Save the model to `src/models/artifacts/`
