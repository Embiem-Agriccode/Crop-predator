import streamlit as st
import time
from pathlib import Path
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# CROP PREDATOR - FUD CROP SCIENCE PROJECT
# Developed by Mubarak Haruna | Level 2 Crop Science, FUD
# Data-Driven Agriculture for Nigerian Farmers
# ==========================================

st.set_page_config(
    page_title="Crop Predator - FUD",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .block-container { padding: 1rem 1rem 2rem 1rem; max-width: 800px; }
    .stButton > button {
        background-color: #2d5016;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        padding: 12px 30px;
        border: none;
        width: 100%;
        font-size: 16px;
    }
    .stButton > button:hover { background-color: #1e3a0f; }
    h1 { color: #2d5016; text-align: center; }
    h2 { color: #2d5016; }
    h3 { color: #2d5016; }
</style>
""", unsafe_allow_html=True)

# Session State
if "page" not in st.session_state:
    st.session_state.page = "input"
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = {}

# ==========================================
# CROP DATABASE (23 crops)
# ==========================================
CROPS = {
    "Cassava":      {"ph_range": (5.5, 6.5), "season": "Rainy Season", "yield": "12-15 tons/ha", "price_per_ton": 80000},
    "Yam":          {"ph_range": (5.5, 6.0), "season": "Rainy Season", "yield": "8-12 tons/ha",  "price_per_ton": 150000},
    "Rice":         {"ph_range": (5.5, 6.5), "season": "Rainy Season", "yield": "5-7 tons/ha",   "price_per_ton": 400000},
    "Maize":        {"ph_range": (5.8, 7.0), "season": "Rainy Season", "yield": "4-6 tons/ha",   "price_per_ton": 120000},
    "Groundnut":    {"ph_range": (5.9, 7.0), "season": "Dry Season",   "yield": "2-3 tons/ha",   "price_per_ton": 350000},
    "Cocoa":        {"ph_range": (5.0, 6.5), "season": "Rainy Season", "yield": "1-2 tons/ha",   "price_per_ton": 1200000},
    "Plantain":     {"ph_range": (5.5, 7.0), "season": "Rainy Season", "yield": "15-20 tons/ha", "price_per_ton": 60000},
    "Tomato":       {"ph_range": (6.0, 7.0), "season": "Dry Season",   "yield": "20-30 tons/ha", "price_per_ton": 100000},
    "Sorghum":      {"ph_range": (5.5, 7.5), "season": "Dry Season",   "yield": "2-3 tons/ha",   "price_per_ton": 100000},
    "Cowpea":       {"ph_range": (6.0, 7.0), "season": "Rainy Season", "yield": "1-2 tons/ha",   "price_per_ton": 450000},
    "Millet":       {"ph_range": (5.5, 7.0), "season": "Rainy Season", "yield": "1-2 tons/ha",   "price_per_ton": 200000},
    "Wheat":        {"ph_range": (6.0, 7.5), "season": "Dry Season",   "yield": "3-5 tons/ha",   "price_per_ton": 450000},
    "Sesame":       {"ph_range": (5.5, 7.0), "season": "Rainy Season", "yield": "1-2 tons/ha",   "price_per_ton": 600000},
    "Sweet Potato": {"ph_range": (5.5, 6.5), "season": "Rainy Season", "yield": "8-15 tons/ha",  "price_per_ton": 80000},
    "Onion":        {"ph_range": (6.0, 7.5), "season": "Dry Season",   "yield": "15-25 tons/ha", "price_per_ton": 120000},
    "Pepper":       {"ph_range": (6.0, 7.0), "season": "Dry Season",   "yield": "5-10 tons/ha",  "price_per_ton": 500000},
    "Watermelon":   {"ph_range": (6.0, 7.5), "season": "Dry Season",   "yield": "20-30 tons/ha", "price_per_ton": 60000},
    "Okra":         {"ph_range": (6.0, 7.5), "season": "Rainy Season", "yield": "5-8 tons/ha",   "price_per_ton": 200000},
    "Roselle":      {"ph_range": (5.5, 7.0), "season": "Rainy Season", "yield": "1-3 tons/ha",   "price_per_ton": 350000},
    "Bambara Nut":  {"ph_range": (5.0, 6.5), "season": "Rainy Season", "yield": "1-2 tons/ha",   "price_per_ton": 300000},
    "Sugarcane":    {"ph_range": (6.0, 7.5), "season": "Rainy Season", "yield": "60-80 tons/ha", "price_per_ton": 50000},
    "Cotton":       {"ph_range": (6.0, 8.0), "season": "Rainy Season", "yield": "1-2 tons/ha",   "price_per_ton": 800000},
    "Carrot":       {"ph_range": (6.0, 7.0), "season": "Dry Season",   "yield": "20-30 tons/ha", "price_per_ton": 150000},
}

# ==========================================
# FERTILIZER DATABASE
# ==========================================
FERTILIZER = {
    "Cassava":      {"optimal": "Apply NPK 10:10:10 at 300kg/ha. Split into 2 doses — at planting and 8 weeks after.", "acidic": "Soil too acidic! Apply Agricultural Lime (CaCO3) at 2 tons/ha. Wait 3 weeks, then apply NPK 10:10:10 at 300kg/ha.", "alkaline": "Soil too alkaline! Apply Sulfur at 1 ton/ha to lower pH. Then use NPK 15:15:15 at 250kg/ha."},
    "Yam":          {"optimal": "Apply NPK 15:15:15 at 400kg/ha before planting. Add organic manure 5 tons/ha for best results.", "acidic": "Soil too acidic for Yam! Apply lime at 1.5 tons/ha. After 4 weeks apply NPK 15:15:15 at 400kg/ha.", "alkaline": "Apply sulfur 0.5 tons/ha. Use NPK 15:15:15 at 350kg/ha."},
    "Rice":         {"optimal": "Apply Urea (46% N) at 100kg/ha + Single Superphosphate at 200kg/ha. Apply in 3 splits.", "acidic": "Apply lime 2 tons/ha first. After 2 weeks: Urea 100kg/ha + SSP 200kg/ha.", "alkaline": "Rice tolerates mild alkalinity. Apply Ammonium Sulfate instead of Urea at 150kg/ha."},
    "Maize":        {"optimal": "Apply NPK 15:15:15 at 400kg/ha at planting. Top-dress with Urea 100kg/ha at 4-6 weeks.", "acidic": "CRITICAL: Apply Agricultural Lime at 2-3 tons/ha. Wait 4 weeks then NPK 15:15:15 at 400kg/ha.", "alkaline": "Apply Ammonium Sulfate 200kg/ha + Phosphate 150kg/ha. Avoid Urea in alkaline soils."},
    "Groundnut":    {"optimal": "Apply SSP (Single Superphosphate) at 200kg/ha. Add Gypsum 250kg/ha for pod filling.", "acidic": "Apply lime 1.5 tons/ha to reach pH 6.0. Then SSP 200kg/ha + Gypsum 250kg/ha.", "alkaline": "Apply sulfur 1 ton/ha. Use DAP (Diammonium Phosphate) at 150kg/ha."},
    "Tomato":       {"optimal": "Apply NPK 20:10:10 at 500kg/ha. Foliar spray with Calcium Nitrate at fruiting stage.", "acidic": "Apply lime 2 tons/ha. After 3 weeks: NPK 20:10:10 at 500kg/ha + Calcium Nitrate foliar.", "alkaline": "Apply sulfur 1.5 tons/ha. Use Ammonium Sulfate 200kg/ha + Potassium Sulfate 100kg/ha."},
    "Sorghum":      {"optimal": "Apply NPK 15:15:15 at 300kg/ha at planting. Top-dress Urea 60kg/ha at 30 days.", "acidic": "If below 5.5: lime 1 ton/ha. Then NPK 15:15:15 at 300kg/ha.", "alkaline": "Sorghum tolerates alkalinity well. Apply NPK 15:15:15 at 250kg/ha + Zinc Sulfate 10kg/ha."},
    "Cowpea":       {"optimal": "Apply SSP 150kg/ha. Inoculate seeds with Rhizobium bacteria for nitrogen fixation.", "acidic": "Apply lime 1 ton/ha. After 2 weeks: SSP 150kg/ha + Rhizobium inoculant.", "alkaline": "Apply sulfur 0.5 tons/ha. Use SSP 150kg/ha. Avoid high Nitrogen fertilizers."},
    "Cocoa":        {"optimal": "Apply NPK 10:10:18 at 500kg/ha split into 2 applications (April and September).", "acidic": "Apply lime 1.5 tons/ha. After 4 weeks: NPK 10:10:18 at 500kg/ha.", "alkaline": "Apply sulfur 1 ton/ha. Use NPK 10:10:18 at 400kg/ha + Magnesium Sulfate 50kg/ha."},
    "Plantain":     {"optimal": "Apply NPK 15:15:15 at 500kg/ha + Urea 100kg/ha. Mulch heavily with organic matter.", "acidic": "Apply lime 2 tons/ha. After 4 weeks: NPK 15:15:15 at 500kg/ha + organic mulch.", "alkaline": "Apply sulfur 1 ton/ha. Use Ammonium Sulfate 200kg/ha + Potassium Chloride 150kg/ha."},
    "Millet":       {"optimal": "Apply NPK 15:15:15 at 200kg/ha at planting. Top-dress Urea 50kg/ha at 30 days.", "acidic": "Apply lime 1 ton/ha. Wait 3 weeks. Then NPK 15:15:15 at 200kg/ha.", "alkaline": "Millet tolerates alkalinity. Apply NPK 15:15:15 at 150kg/ha + Zinc Sulfate 10kg/ha."},
    "Wheat":        {"optimal": "Apply NPK 20:10:10 at 400kg/ha at planting. Top-dress Urea at tillering stage.", "acidic": "Apply lime 2 tons/ha. Wait 4 weeks. Then NPK 20:10:10 at 400kg/ha.", "alkaline": "Apply Ammonium Sulfate 200kg/ha + SSP 150kg/ha. Avoid high pH above 7.8."},
    "Sesame":       {"optimal": "Apply NPK 15:15:15 at 200kg/ha at planting only. Very low input crop.", "acidic": "Apply lime 1 ton/ha. Wait 2 weeks. Then NPK 15:15:15 at 200kg/ha.", "alkaline": "Apply sulfur 0.5 tons/ha. Use SSP 150kg/ha. Sesame tolerates mild alkalinity."},
    "Sweet Potato": {"optimal": "Apply NPK 10:10:20 at 300kg/ha. Add compost 3 tons/ha for root development.", "acidic": "Apply lime 1.5 tons/ha. After 3 weeks: NPK 10:10:20 at 300kg/ha.", "alkaline": "Apply sulfur 0.5 tons/ha. Use NPK 10:10:20 at 250kg/ha."},
    "Onion":        {"optimal": "Apply NPK 15:15:15 at 400kg/ha in 3 splits. Stop fertilizing 4 weeks before harvest.", "acidic": "Apply lime 2 tons/ha. After 3 weeks: NPK 15:15:15 at 400kg/ha in 3 splits.", "alkaline": "Apply sulfur 1 ton/ha. Use Ammonium Sulfate 200kg/ha + Potassium Sulfate 100kg/ha."},
    "Pepper":       {"optimal": "Apply NPK 20:20:20 at 350kg/ha. Foliar spray Calcium Nitrate to prevent blossom end rot.", "acidic": "Apply lime 2 tons/ha. After 3 weeks: NPK 20:20:20 at 350kg/ha.", "alkaline": "Apply sulfur 1.5 tons/ha. Use Ammonium Sulfate 180kg/ha + Potassium Sulfate 100kg/ha."},
    "Watermelon":   {"optimal": "Apply NPK 15:15:15 at 300kg/ha. Add Potassium Sulfate 100kg/ha at fruiting stage.", "acidic": "Apply lime 1.5 tons/ha. After 3 weeks: NPK 15:15:15 at 300kg/ha.", "alkaline": "Apply sulfur 1 ton/ha. Use NPK 15:15:15 at 250kg/ha."},
    "Okra":         {"optimal": "Apply NPK 15:15:15 at 250kg/ha. Top-dress Urea 50kg/ha at 4 weeks.", "acidic": "Apply lime 1 ton/ha. After 2 weeks: NPK 15:15:15 at 250kg/ha.", "alkaline": "Apply sulfur 0.5 tons/ha. Use Ammonium Sulfate 150kg/ha + SSP 100kg/ha."},
    "Roselle":      {"optimal": "Apply NPK 10:10:10 at 200kg/ha at planting. Very low input crop.", "acidic": "Apply lime 1 ton/ha. After 2 weeks: NPK 10:10:10 at 200kg/ha.", "alkaline": "Roselle tolerates mild alkalinity. Apply sulfur 0.5 tons/ha if pH above 7.5."},
    "Bambara Nut":  {"optimal": "Apply SSP 150kg/ha only. Fixes its own nitrogen like groundnut.", "acidic": "Apply lime 1 ton/ha. After 2 weeks: SSP 150kg/ha. Very drought tolerant.", "alkaline": "Apply sulfur 0.5 tons/ha. Use SSP 150kg/ha. Avoid nitrogen fertilizers."},
    "Sugarcane":    {"optimal": "Apply NPK 20:10:20 at 600kg/ha in 3 splits over 6 months.", "acidic": "Apply lime 2 tons/ha. After 4 weeks: NPK 20:10:20 at 600kg/ha.", "alkaline": "Apply sulfur 1.5 tons/ha. Use Ammonium Sulfate 300kg/ha + Potassium Chloride 200kg/ha."},
    "Cotton":       {"optimal": "Apply NPK 15:15:15 at 400kg/ha. Top-dress Urea at squaring stage.", "acidic": "Apply lime 2 tons/ha. After 3 weeks: NPK 15:15:15 at 400kg/ha.", "alkaline": "Apply sulfur 1 ton/ha. Use Ammonium Sulfate 200kg/ha + SSP 150kg/ha."},
    "Carrot":       {"optimal": "Apply NPK 10:20:20 at 300kg/ha. Deep loose soil needed for straight roots.", "acidic": "Apply lime 1.5 tons/ha. After 3 weeks: NPK 10:20:20 at 300kg/ha.", "alkaline": "Apply sulfur 1 ton/ha. Use NPK 10:20:20 at 250kg/ha."},
}

# ==========================================
# SOIL PROFILES
# ==========================================
SOIL_PROFILES = {
    "Dutse (FUD Farm Zone)": {"soil_type": "Sandy Loam", "organic_matter": "Low (0.5-1.2%)", "drainage": "Excellent", "challenge": "Rapid moisture loss, low nutrient retention", "tip": "Use organic mulching (5-10 tons/ha) to retain moisture. Add compost before planting."},
    "Hadejia":               {"soil_type": "Fadama Clay / Alluvial", "organic_matter": "High (2.5-4.0%)", "drainage": "Poor to Moderate", "challenge": "Waterlogging during rainy season", "tip": "Construct drainage channels. Excellent for dry-season irrigated rice and wheat."},
    "Kano":                  {"soil_type": "Sandy Clay Loam", "organic_matter": "Medium (1.0-2.0%)", "drainage": "Good", "challenge": "Shorter rainy season, wind erosion", "tip": "Use early-maturing crop varieties. Plant windbreaks to reduce erosion."},
    "Katsina":               {"soil_type": "Sandy / Light Loam", "organic_matter": "Very Low (0.3-0.8%)", "drainage": "Excessive", "challenge": "Severe drought stress, desertification risk", "tip": "Focus on drought-tolerant crops. Use zai pits for water harvesting."},
    "Jigawa":                {"soil_type": "Mixed Sandy Loam", "organic_matter": "Low (0.5-1.5%)", "drainage": "Good to Excessive", "challenge": "Erratic rainfall, low fertility", "tip": "Intercropping millet with cowpea improves soil fertility naturally."},
    "Lagos":                 {"soil_type": "Coastal Sandy / Loamy", "organic_matter": "Medium (1.5-2.5%)", "drainage": "Variable", "challenge": "High humidity, fungal disease pressure", "tip": "Use raised beds. Apply fungicide preventively. Focus on disease-resistant varieties."},
    "Kaduna":                {"soil_type": "Ferruginous Tropical Soil", "organic_matter": "Medium (1.2-2.2%)", "drainage": "Moderate to Good", "challenge": "Soil compaction, leaching in rainy season", "tip": "Deep ploughing before planting season. Apply lime if pH drops below 5.8."},
    "Ogun":                  {"soil_type": "Forest Alfisol", "organic_matter": "High (2.0-3.5%)", "drainage": "Good", "challenge": "Acidification under continuous cropping", "tip": "Rotate crops yearly. Add compost to maintain organic matter levels."},
    "Borno":                 {"soil_type": "Vertisol / Heavy Clay", "organic_matter": "Low (0.5-1.0%)", "drainage": "Poor", "challenge": "Extreme dryness, cracking clay soils", "tip": "Flood irrigation for fadama areas. Sorghum and millet are most resilient here."},
    "Niger":                 {"soil_type": "Loamy Sand", "organic_matter": "Medium (1.0-2.0%)", "drainage": "Good", "challenge": "Mid-season dry spells", "tip": "Supplemental irrigation at critical growth stages improves yield by 40%."},
    "Oyo":                   {"soil_type": "Deep Tropical Alfisol", "organic_matter": "High (2.5-4.0%)", "drainage": "Good to Moderate", "challenge": "Soil erosion on slopes", "tip": "Contour farming on slopes. Excellent conditions for cocoa and plantain."},
    "Osun":                  {"soil_type": "Derived Savanna Loam", "organic_matter": "High (2.0-3.0%)", "drainage": "Moderate", "challenge": "Seasonal flooding in low areas", "tip": "Excellent soil for high-value crops. Use raised bed system in flood-prone areas."},
    "Rivers":                {"soil_type": "Acid Sand / Ultisol", "organic_matter": "High (3.0-5.0%)", "drainage": "Poor", "challenge": "Extreme acidity, waterlogging", "tip": "Heavy liming required. Drainage channels essential. Cassava most tolerant here."},
}

LOCATION_TIPS = {
    "Lagos":                 "High humidity. Watch for fungal diseases. Use resistant varieties.",
    "Ogun":                  "Good rainfall. Focus on rainy season crops for best yield.",
    "Kaduna":                "Mix of dry and rainy zones. Diversify your crops.",
    "Borno":                 "Very dry climate. Focus on hardy crops like sorghum.",
    "Niger":                 "Moderate rainfall. Groundnut and maize do well.",
    "Oyo":                   "Tropical climate. All crops can thrive here.",
    "Osun":                  "Good soil quality. High-value crops recommended.",
    "Rivers":                "High rainfall. Watch drainage. Root crops excel.",
    "Jigawa":                "Semi-arid. Millet, sorghum, and groundnut thrive. Use irrigation wisely.",
    "Dutse (FUD Farm Zone)": "Sandy loam soils. Organic mulching highly recommended. Perfect for student research!",
    "Hadejia":               "Excellent wetland/fadama areas. Perfect for dry-season irrigated rice.",
    "Kano":                  "High market access. Focus on early-maturing varieties.",
    "Katsina":               "Semi-arid zone. Focus on drought-resistant cereals like millet."
}

# ==========================================
# PAGE 1: INPUT
# ==========================================
if st.session_state.page == "input":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 🌱 Crop Predator")
        st.markdown("<h3 style='text-align:center;'>Precision Agriculture Tool</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'><i>by Mubarak Haruna | FUD Crop Science</i></p>", unsafe_allow_html=True)

    img_path = Path(__file__).parent / "IMG_20260522_111712.jpg"
    if img_path.exists():
        st.image(str(img_path), use_container_width=True, caption="Data-Driven Yields for African Farmers")
    else:
        st.info("Crop Predator — Precision Agriculture for Nigerian Farmers")

    st.write("Enter your farm details to get crop recommendations tailored to your soil")
    st.divider()

    st.markdown("## 📋 Farm Details")
    col1, col2 = st.columns(2)
    with col1:
        ph = st.slider("Soil pH Level", 4.0, 9.0, 6.0, step=0.1)
        location = st.selectbox("Farm Location", list(LOCATION_TIPS.keys()))
    with col2:
        season = st.selectbox("Current Season", ["Dry Season", "Rainy Season"])
        farm_size = st.number_input("Farm Size (hectares)", 1, 100, 5)

    st.divider()

    if st.button("Analyse My Soil", use_container_width=True):
        st.session_state.analysis_data = {
            "ph": ph, "location": location,
            "season": season, "farm_size": farm_size
        }
        st.session_state.page = "loading"
        st.rerun()

    # ==========================================
    # BATCH UPLOAD — stays on input page only
    # ==========================================
    st.divider()
    st.markdown("### 📂 Batch Farm Analysis")
    st.write("Upload a CSV file with multiple farms to analyse them all at once!")

    uploaded_file = st.file_uploader("Upload farms.csv", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ {len(df)} farms loaded!")
        st.dataframe(df)
        st.divider()

        # Add pH Status column
        
        ph_column = None
        for col in df.columns :
            if "ph"  in col.lower ():
                ph_column = col
                break
        name_column = None
        for col in df.columns:
            if "farm" in col.lower() or "name" in col.lower():
                name_column = col
                break
        if ph_column is None:
            st.error("No pH column found! Make sure your CSV has a pH column.")
        else:
            st.success(f"pH column detected: {ph_column}")
        df["pH_Status"] = df[ph_column].apply(
            lambda x: "Good" if 5.5 <= x <= 7.5 else "Bad"
        )
        # Stats
        st.markdown("### 📊 Analysis Results")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Farms", len(df))
        with col2:
            st.metric("Good pH Farms", len(df[df["pH_Status"] == "Good"]))
        with col3:
            st.metric("Bad pH Farms", len(df[df["pH_Status"] == "Bad"]))

        st.metric("Average Soil pH", f"{df[ph_column].mean():.2f}")

        # Season breakdown
        st.markdown("### Farms by Season")
        st.dataframe(df["Season"].value_counts())

        # Chart
        st.markdown("### Soil pH Chart")
        fig, ax = plt.subplots()
        ax.bar(df[name_column], df[ph_column], color="green")
        ax.axhline(y=5.5, color="red", linestyle="--", label="Min pH (5.5)")
        ax.axhline(y=7.5, color="orange", linestyle="--", label="Max pH (7.5)")
        ax.set_xlabel("Farm")
        ax.set_ylabel("pH Level")
        ax.set_title("Soil pH by Farm")
        plt.xticks(rotation=90, fontsize=7)
        plt.tight_layout()
        ax.legend()
        st.pyplot(fig)

        # Download results
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Results",
            data=csv,
            file_name="batch_results.csv",
            mime="text/csv",
            use_container_width=True
        )

# ==========================================
# PAGE 2: LOADING
# ==========================================
elif st.session_state.page == "loading":
    st.markdown("# 🌱 Crop Predator")
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## Analyzing Your Soil...")
        st.markdown("**Please wait while we process your farm data**")
    with st.spinner(""):
        st.write("Processing soil samples...")
        time.sleep(1)
        st.write("Analyzing pH levels...")
        time.sleep(1)
        st.write("Calculating fertilizer needs...")
        time.sleep(1)
        st.write("Running profitability model...")
        time.sleep(1)
        st.write("Matching optimal crops...")
        time.sleep(1)
    st.session_state.page = "results"
    st.rerun()

# ==========================================
# PAGE 3: RESULTS
# ==========================================
elif st.session_state.page == "results":
    data = st.session_state.analysis_data
    ph = data["ph"]
    location = data["location"]
    season = data["season"]
    farm_size = data["farm_size"]
    date_today = datetime.now().strftime("%B %d, %Y")

    st.markdown("# 🌱 Crop Predator")
    st.markdown("### Analysis Complete!")
    st.divider()

    # Farm Profile
    st.markdown("### Your Farm Profile")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Location", location)
        st.metric("pH Level", f"{ph:.1f}")
    with col2:
        st.metric("Season", season)
        st.metric("Farm Size", f"{farm_size} ha")
    st.divider()

    # Best Crops
    best_crops = [
        (crop, info) for crop, info in CROPS.items()
        if info["ph_range"][0] <= ph <= info["ph_range"][1]
        and info["season"] == season
    ]

    st.markdown("### Best Crops for Your Farm")
    best_crops_sorted = []
    if best_crops:
        best_crops_sorted = sorted(
            best_crops,
            key=lambda x: float(x[1]["yield"].split("-")[1].split()[0]),
            reverse=True
        )[:3]
        for idx, (crop, info) in enumerate(best_crops_sorted, 1):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"### {idx}. {crop}")
            with col2:
                st.success("Perfect Match!")
            with col3:
                st.write(f"Yield: {info['yield']}")
            with col4:
                st.write(f"pH: {info['ph_range'][0]}-{info['ph_range'][1]}")
    else:
        st.warning("No ideal crops for this pH in current season.")
    st.divider()

    # Success Rate
    st.markdown("### 🎯 Crop Success Rate")
    if best_crops_sorted:
        top_crop, top_info = best_crops_sorted[0]
        ph_min = top_info["ph_range"][0]
        ph_max = top_info["ph_range"][1]
        ph_middle = (ph_min + ph_max) / 2
        ph_range_size = ph_max - ph_min
        distance = abs(ph - ph_middle)
        success_rate = max(0, 100 - (distance / ph_range_size * 100))

        st.progress(int(success_rate))
        if success_rate >= 80:
            st.success(f"✅ {success_rate:.0f}% — Excellent conditions for {top_crop}!")
        elif success_rate >= 60:
            st.warning(f"⚠️ {success_rate:.0f}% — Good conditions for {top_crop}.")
        else:
            st.error(f"❌ {success_rate:.0f}% — Poor conditions. Consider soil amendment first.")
    else:
        st.warning("No crops matched — fix soil pH first.")
    st.divider()

    # Soil Amendment
    st.markdown("### Soil Amendment Recommendations")
    if ph < 5.5:
        amendment_text = "Apply Agricultural Lime (CaCO3) — 2-3 tons/ha. Wait 2-4 weeks before planting."
        st.error(f"Highly Acidic Soil (pH {ph:.1f})")
        st.write("**Solution:** Apply Agricultural Lime (CaCO3)")
        st.write("**Dosage:** 2-3 tons/hectare")
        st.write("**Timeline:** Wait 2-4 weeks before planting")
    elif ph > 7.5:
        amendment_text = "Apply Elemental Sulfur — 1-2 tons/ha. Takes 3-6 months for effect."
        st.error(f"Alkaline Soil (pH {ph:.1f})")
        st.write("**Solution:** Apply Elemental Sulfur")
        st.write("**Dosage:** 1-2 tons/hectare")
        st.write("**Timeline:** 3-6 months for effect")
    else:
        amendment_text = "No amendment needed. Soil pH is ideal!"
        st.success(f"Ideal pH Range (pH {ph:.1f}) — No amendment needed!")
    st.divider()

    # Smart Fertilizer
    st.markdown("### Smart Fertilizer Recommendations")
    if best_crops_sorted:
        for crop, info in best_crops_sorted:
            fert = FERTILIZER.get(crop)
            if fert:
                with st.expander(f"Fertilizer Plan for {crop}"):
                    if ph < info["ph_range"][0]:
                        st.warning(f"Your pH ({ph}) is too low for {crop}")
                        st.write(fert["acidic"])
                    elif ph > info["ph_range"][1]:
                        st.warning(f"Your pH ({ph}) is too high for {crop}")
                        st.write(fert["alkaline"])
                    else:
                        st.success(f"pH is optimal for {crop}!")
                        st.write(fert["optimal"])
    else:
        st.info("Fix your soil pH first before applying fertilizer.")
    st.divider()

    # Soil Profile
    st.markdown("### Local Soil Profile Analysis")
    if location in SOIL_PROFILES:
        profile = SOIL_PROFILES[location]
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Soil Type:** {profile['soil_type']}")
            st.write(f"**Organic Matter:** {profile['organic_matter']}")
        with col2:
            st.write(f"**Drainage:** {profile['drainage']}")
            st.warning(f"**Challenge:** {profile['challenge']}")
        st.success(f"**Expert Tip:** {profile['tip']}")
    st.divider()

    # Profitability Calculator
    st.markdown("### Farm Profitability Calculator")
    if best_crops_sorted:
        top_crop, top_info = best_crops_sorted[0]
        col1, col2 = st.columns(2)
        with col1:
            seed_cost = st.number_input("Seed Cost (per hectare)", min_value=0, value=15000, step=1000)
        with col2:
            labor_cost = st.number_input("Labor Cost (per hectare)", min_value=0, value=30000, step=1000)
        fertilizer_cost = st.number_input("Fertilizer Cost (per hectare)", min_value=0, value=25000, step=1000)

        if st.button("Calculate Profit", use_container_width=True):
            yield_parts = top_info["yield"].replace(" tons/ha", "").split("-")
            avg_yield = (float(yield_parts[0]) + float(yield_parts[1])) / 2
            price_per_ton = top_info["price_per_ton"]
            total_yield = avg_yield * farm_size
            gross_revenue = total_yield * price_per_ton
            total_cost = (seed_cost + labor_cost + fertilizer_cost) * farm_size
            net_profit = gross_revenue - total_cost
            roi = ((net_profit / total_cost) * 100) if total_cost > 0 else 0

            st.divider()
            st.markdown(f"#### Results for {top_crop} on {farm_size} ha")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Expected Yield", f"{total_yield:.1f} tons")
            with col2:
                st.metric("Gross Revenue", f"NGN {gross_revenue:,.0f}")
            with col3:
                st.metric("Total Cost", f"NGN {total_cost:,.0f}")

            col1, col2 = st.columns(2)
            with col1:
                if net_profit > 0:
                    st.metric("Net Profit", f"NGN {net_profit:,.0f}", delta="Profitable")
                else:
                    st.metric("Net Loss", f"NGN {net_profit:,.0f}", delta="Not profitable")
            with col2:
                st.metric("Return on Investment", f"{roi:.1f}%")

            if roi > 100:
                st.success(f"Excellent! {top_crop} gives {roi:.0f}% ROI — very profitable!")
            elif roi > 50:
                st.success(f"Good investment! {top_crop} gives {roi:.0f}% ROI.")
            elif roi > 0:
                st.warning(f"Low margin ({roi:.0f}% ROI). Consider reducing costs.")
            else:
                st.error("Not profitable at current prices. Choose another crop.")

            st.session_state.analysis_data["profit_data"] = {
                "crop": top_crop, "total_yield": total_yield,
                "gross_revenue": gross_revenue, "total_cost": total_cost,
                "net_profit": net_profit, "roi": roi
            }

        st.caption("Prices are estimates based on Nigerian market averages.")
    else:
        st.warning("No suitable crops found. Please adjust your soil pH.")
    st.divider()

    # Location Tip
    st.markdown("### Location-Specific Expertise")
    st.info(f"**{location}** — {LOCATION_TIPS[location]}")
    st.divider()

    # Download Report
    st.markdown("### Download Your Farm Report")
    if best_crops_sorted:
        top_crop, top_info = best_crops_sorted[0]
        fert = FERTILIZER.get(top_crop, {})
        profit_data = st.session_state.analysis_data.get("profit_data", None)

        report = f"""
==============================================
      CROP PREDATOR - FARM ANALYSIS REPORT
      Federal University of Dutse (FUD)
==============================================
Developed by : Mubarak Haruna | Level 2 Crop Science, FUD
Date         : {date_today}
----------------------------------------------

FARM PROFILE
------------
Location     : {location}
Soil pH      : {ph:.1f}
Season       : {season}
Farm Size    : {farm_size} hectares

SOIL CONDITION
--------------
{amendment_text}

SOIL PROFILE ({location})
--------------------------
"""
        if location in SOIL_PROFILES:
            profile = SOIL_PROFILES[location]
            report += f"Soil Type     : {profile['soil_type']}\n"
            report += f"Organic Matter: {profile['organic_matter']}\n"
            report += f"Drainage      : {profile['drainage']}\n"
            report += f"Challenge     : {profile['challenge']}\n"
            report += f"Expert Tip    : {profile['tip']}\n"

        report += "\nRECOMMENDED CROPS\n-----------------\n"
        for idx, (crop, info) in enumerate(best_crops_sorted, 1):
            report += f"{idx}. {crop}\n"
            report += f"   Yield Potential : {info['yield']}\n"
            report += f"   Suitable pH     : {info['ph_range'][0]} - {info['ph_range'][1]}\n\n"

        report += f"\nFERTILIZER PLAN — {top_crop}\n----------------------------------------------\n"
        if fert:
            if ph < top_info["ph_range"][0]:
                report += fert.get("acidic", "")
            elif ph > top_info["ph_range"][1]:
                report += fert.get("alkaline", "")
            else:
                report += fert.get("optimal", "")

        if profit_data:
            report += f"""

PROFITABILITY ESTIMATE — {profit_data['crop']}
----------------------------------------------
Expected Yield  : {profit_data['total_yield']:.1f} tons
Gross Revenue   : NGN {profit_data['gross_revenue']:,.0f}
Total Cost      : NGN {profit_data['total_cost']:,.0f}
Net Profit      : NGN {profit_data['net_profit']:,.0f}
ROI             : {profit_data['roi']:.1f}%
"""

        report += f"""
LOCATION ADVICE
---------------
{LOCATION_TIPS[location]}

==============================================
  Data-Driven Agriculture for Nigerian Farmers
  Crop Predator | FUD Crop Science Department
  Developed by Mubarak Haruna | Level 2, FUD
==============================================
"""
        st.download_button(
            label="Download Full Farm Report (.txt)",
            data=report,
            file_name=f"FarmReport_{location.replace(' ', '_')}_{date_today}.txt",
            mime="text/plain",
            use_container_width=True
        )
        st.caption("Download and share this report with your agronomist or extension officer.")
    st.divider()

    if st.button("Analyse Another Farm", use_container_width=True):
        st.session_state.page = "input"
        st.rerun()

# ==========================================
# FOOTER
# ==========================================
if st.session_state.page != "loading":
    st.divider()
    st.markdown("""
**Developed by:** Mubarak Haruna | Level 2 Crop Science, FUD  
**Purpose:** Data-Driven A
griculture for Nigerian Farmers  
**Location:** Federal University of Dutse (FUD)
""")