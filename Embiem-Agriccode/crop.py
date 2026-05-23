import streamlit as st
import time
from pathlib import Path

# ==========================================
# CROP PREDATOR - FUD CROP SCIENCE PROJECT
# Developed by Mubarak Haruna | Level 2 Crop Science, FUD
# Data-Driven Agriculture for Nigerian Farmers 🌱
# ==========================================

st.set_page_config(
    page_title="Crop Predator - FUD",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stButton > button {
        background-color: #2d5016;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        padding: 12px 30px;
        border: none;
        width: 100%;
    }
    .stButton > button:hover { background-color: #1e3a0f; }
    h1 { color: #2d5016; text-align: center; }
    h3 { color: #2d5016; }
</style>
""", unsafe_allow_html=True)

# ── Session State ────────────
if "page" not in st.session_state:
    st.session_state.page = "input"
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = {}

# ── Crop Database ────────────
CROPS = {
    "Cassava":   {"ph_range": (5.5, 6.5), "season": "Rainy Season", "yield": "12-15 tons/ha", "emoji": "", "price_per_ton": 80000},
    "Yam":       {"ph_range": (5.5, 6.0), "season": "Rainy Season", "yield": "8-12 tons/ha",  "emoji": "", "price_per_ton": 150000},
    "Rice":      {"ph_range": (5.5, 6.5), "season": "Rainy Season", "yield": "5-7 tons/ha",   "emoji": "", "price_per_ton": 400000},
    "Maize":     {"ph_range": (5.8, 7.0), "season": "Rainy Season", "yield": "4-6 tons/ha",   "emoji": "", "price_per_ton": 120000},
    "Groundnut": {"ph_range": (5.9, 7.0), "season": "Dry Season",   "yield": "2-3 tons/ha",   "emoji": "", "price_per_ton": 350000},
    "Cocoa":     {"ph_range": (5.0, 6.5), "season": "Rainy Season", "yield": "1-2 tons/ha",   "emoji": "", "price_per_ton": 1200000},
    "Plantain":  {"ph_range": (5.5, 7.0), "season": "Rainy Season", "yield": "15-20 tons/ha", "emoji": "", "price_per_ton": 60000},
    "Tomato":    {"ph_range": (6.0, 7.0), "season": "Dry Season",   "yield": "20-30 tons/ha", "emoji": "", "price_per_ton": 100000},
    "Sorghum":   {"ph_range": (5.5, 7.5), "season": "Dry Season",   "yield": "2-3 tons/ha",   "emoji": "", "price_per_ton": 100000},
    "Cowpea":    {"ph_range": (6.0, 7.0), "season": "Rainy Season", "yield": "1-2 tons/ha",   "emoji": "", "price_per_ton": 450000},
}

# ── Fertilizer Recommendations by crop + pH ────────────
FERTILIZER = {
    "Cassava": {
        "optimal": "Apply NPK 10:10:10 at 300kg/ha. Split into 2 doses — at planting and 8 weeks after.",
        "acidic":  "Soil too acidic! First apply Agricultural Lime (CaCO₃) at 2 tons/ha. Wait 3 weeks, then apply NPK 10:10:10 at 300kg/ha.",
        "alkaline":"Soil too alkaline! Apply Sulfur at 1 ton/ha to lower pH. Then use NPK 15:15:15 at 250kg/ha."
    },
    "Yam": {
        "optimal": "Apply NPK 15:15:15 at 400kg/ha before planting. Add organic manure 5 tons/ha for best results.",
        "acidic":  "Soil too acidic for Yam! Apply lime at 1.5 tons/ha. After 4 weeks apply NPK 15:15:15 at 400kg/ha.",
        "alkaline":"Slightly alkaline. Apply sulfur 0.5 tons/ha. Use NPK 15:15:15 at 350kg/ha."
    },
    "Rice": {
        "optimal": "Apply Urea (46% N) at 100kg/ha + Single Superphosphate at 200kg/ha. Apply in 3 splits.",
        "acidic":  "Apply lime 2 tons/ha first. After 2 weeks: Urea 100kg/ha + SSP 200kg/ha.",
        "alkaline":"Rice tolerates mild alkalinity. Apply Ammonium Sulfate instead of Urea at 150kg/ha."
    },
    "Maize": {
        "optimal": "Apply NPK 15:15:15 at 400kg/ha at planting. Top-dress with Urea 100kg/ha at 4-6 weeks.",
        "acidic":  "CRITICAL: Maize needs pH 5.8+. Apply Agricultural Lime (CaCO₃) at 2-3 tons/ha. Wait 4 weeks before planting. Then NPK 15:15:15 at 400kg/ha.",
        "alkaline":"Apply Ammonium Sulfate 200kg/ha + Phosphate 150kg/ha. Avoid Urea in alkaline soils."
    },
    "Groundnut": {
        "optimal": "Apply SSP (Single Superphosphate) at 200kg/ha. Add Gypsum 250kg/ha for pod filling.",
        "acidic":  "Apply lime 1.5 tons/ha to reach pH 6.0. Then SSP 200kg/ha + Gypsum 250kg/ha.",
        "alkaline":"Apply sulfur 1 ton/ha. Use DAP (Diammonium Phosphate) at 150kg/ha."
    },
    "Tomato": {
        "optimal": "Apply NPK 20:10:10 at 500kg/ha. Foliar spray with Calcium Nitrate at fruiting stage.",
        "acidic":  "Apply lime 2 tons/ha. After 3 weeks: NPK 20:10:10 at 500kg/ha + Calcium Nitrate foliar.",
        "alkaline":"Apply sulfur 1.5 tons/ha. Use Ammonium Sulfate 200kg/ha + Potassium Sulfate 100kg/ha."
    },
    "Sorghum": {
        "optimal": "Apply NPK 15:15:15 at 300kg/ha at planting. Top-dress Urea 60kg/ha at 30 days.",
        "acidic":  "Sorghum tolerates mild acidity. If below 5.5: lime 1 ton/ha. Then NPK 15:15:15 at 300kg/ha.",
        "alkaline":"Sorghum tolerates alkalinity well. Apply NPK 15:15:15 at 250kg/ha + Zinc Sulfate 10kg/ha."
    },
    "Cowpea": {
        "optimal": "Apply SSP 150kg/ha. Inoculate seeds with Rhizobium bacteria for nitrogen fixation.",
        "acidic":  "Apply lime 1 ton/ha. After 2 weeks: SSP 150kg/ha + Rhizobium inoculant.",
        "alkaline":"Apply sulfur 0.5 tons/ha. Use SSP 150kg/ha. Avoid high Nitrogen fertilizers."
    },
    "Cocoa": {
        "optimal": "Apply NPK 10:10:18 at 500kg/ha split into 2 applications (April and September).",
        "acidic":  "Apply lime 1.5 tons/ha. After 4 weeks: NPK 10:10:18 at 500kg/ha.",
        "alkaline":"Apply sulfur 1 ton/ha. Use NPK 10:10:18 at 400kg/ha + Magnesium Sulfate 50kg/ha."
    },
    "Plantain": {
        "optimal": "Apply NPK 15:15:15 at 500kg/ha + Urea 100kg/ha. Mulch heavily with organic matter.",
        "acidic":  "Apply lime 2 tons/ha. After 4 weeks: NPK 15:15:15 at 500kg/ha + organic mulch.",
        "alkaline":"Apply sulfur 1 ton/ha. Use Ammonium Sulfate 200kg/ha + Potassium Chloride 150kg/ha."
    }
}

# ── Northern Nigeria Soil Profiles ────────────
SOIL_PROFILES = {
    "Dutse (FUD Farm Zone)": {
        "soil_type": "Sandy Loam",
        "organic_matter": "Low (0.5-1.2%)",
        "drainage": "Excellent",
        "challenge": "Rapid moisture loss, low nutrient retention",
        "tip": "Use organic mulching (5-10 tons/ha) to retain moisture. Add compost before planting."
    },
    "Hadejia": {
        "soil_type": "Fadama Clay / Alluvial",
        "organic_matter": "High (2.5-4.0%)",
        "drainage": "Poor to Moderate",
        "challenge": "Waterlogging during rainy season",
        "tip": "Construct drainage channels. Excellent for dry-season irrigated rice and wheat."
    },
    "Kano": {
        "soil_type": "Sandy Clay Loam",
        "organic_matter": "Medium (1.0-2.0%)",
        "drainage": "Good",
        "challenge": "Shorter rainy season, wind erosion",
        "tip": "Use early-maturing crop varieties. Plant windbreaks to reduce erosion."
    },
    "Katsina": {
        "soil_type": "Sandy / Light Loam",
        "organic_matter": "Very Low (0.3-0.8%)",
        "drainage": "Excessive",
        "challenge": "Severe drought stress, desertification risk",
        "tip": "Focus on drought-tolerant crops. Use zaï pits for water harvesting."
    },
    "Jigawa": {
        "soil_type": "Mixed Sandy Loam",
        "organic_matter": "Low (0.5-1.5%)",
        "drainage": "Good to Excessive",
        "challenge": "Erratic rainfall, low fertility",
        "tip": "Intercropping millet with cowpea improves soil fertility naturally."
    },
    "Lagos": {
        "soil_type": "Coastal Sandy / Loamy",
        "organic_matter": "Medium (1.5-2.5%)",
        "drainage": "Variable",
        "challenge": "High humidity, fungal disease pressure",
        "tip": "Use raised beds. Apply fungicide preventively. Focus on disease-resistant varieties."
    },
    "Kaduna": {
        "soil_type": "Ferruginous Tropical Soil",
        "organic_matter": "Medium (1.2-2.2%)",
        "drainage": "Moderate to Good",
        "challenge": "Soil compaction, leaching in rainy season",
        "tip": "Deep ploughing before planting season. Apply lime if pH drops below 5.8."
    },
    "Ogun": {
        "soil_type": "Forest Alfisol",
        "organic_matter": "High (2.0-3.5%)",
        "drainage": "Good",
        "challenge": "Acidification under continuous cropping",
        "tip": "Rotate crops yearly. Add compost to maintain organic matter levels."
    },
    "Borno": {
        "soil_type": "Vertisol / Heavy Clay",
        "organic_matter": "Low (0.5-1.0%)",
        "drainage": "Poor",
        "challenge": "Extreme dryness, cracking clay soils",
        "tip": "Flood irrigation for fadama areas. Sorghum and millet are most resilient here."
    },
    "Niger": {
        "soil_type": "Loamy Sand",
        "organic_matter": "Medium (1.0-2.0%)",
        "drainage": "Good",
        "challenge": "Mid-season dry spells",
        "tip": "Supplemental irrigation at critical growth stages improves yield by 40%."
    },
    "Oyo": {
        "soil_type": "Deep Tropical Alfisol",
        "organic_matter": "High (2.5-4.0%)",
        "drainage": "Good to Moderate",
        "challenge": "Soil erosion on slopes",
        "tip": "Contour farming on slopes. Excellent conditions for cocoa and plantain."
    },
    "Osun": {
        "soil_type": "Derived Savanna Loam",
        "organic_matter": "High (2.0-3.0%)",
        "drainage": "Moderate",
        "challenge": "Seasonal flooding in low areas",
        "tip": "Excellent soil for high-value crops. Use raised bed system in flood-prone areas."
    },
    "Rivers": {
        "soil_type": "Acid Sand / Ultisol",
        "organic_matter": "High (3.0-5.0%)",
        "drainage": "Poor",
        "challenge": "Extreme acidity, waterlogging",
        "tip": "Heavy liming required. Drainage channels essential. Cassava most tolerant here."
    },
}

LOCATION_TIPS = {
    "Lagos":              "🌊 High humidity. Watch for fungal diseases. Use resistant varieties.",
    "Ogun":               "🌧️ Good rainfall. Focus on rainy season crops for best yield.",
    "Kaduna":             " Mix of dry and rainy zones. Diversify your crops.",
    "Borno":              "☀️ Very dry climate. Focus on hardy crops like sorghum.",
    "Niger":              "🌱 Moderate rainfall. Groundnut and maize do well.",
    "Oyo":                "🌴 Tropical climate. All crops can thrive here.",
    "Osun":               "✨ Good soil quality. High-value crops recommended.",
    "Rivers":             "💧 High rainfall. Watch drainage. Root crops excel.",
    "Jigawa":             "🏜️ Semi-arid. Millet, sorghum, and groundnut thrive. Use irrigation wisely.",
    "Dutse (FUD Farm Zone)": "Sandy loam soils. Organic mulching highly recommended. Perfect for student research!",
    "Hadejia":            "🌾 Excellent wetland/fadama areas. Perfect for dry-season irrigated rice.",
    "Kano":               " High market access. Focus on early-maturing varieties.",
    "Katsina":            "🌵 Semi-arid zone. Focus on drought-resistant cereals like millet."
}

# ==========================================
# PAGE 1: INPUT FORM
# ==========================================
if st.session_state.page == "input":

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# 🌱 Crop Predator")
        st.markdown("<h3 style='text-align:center;'>Precision Agriculture Tool</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'><i>by Mubarak Haruna | FUD Crop Science</i></p>", unsafe_allow_html=True)

    img_path = Path(__file__).parent / "IMG_20260522_111712.jpg"
    if img_path.exists():
        st.image(str(img_path), use_container_width=True, caption="Data-Driven Yields for African Farmers")
    else:
        st.info("🌾 Crop Predator — Precision Agriculture for Nigerian Farmers")

    st.write("Enter your farm details to get crop recommendations tailored to your soil")
    st.divider()

    st.markdown("## 📋 Farm Details")
    col1, col2 = st.columns(2)
    with col1:
        ph = st.slider("🧪 Soil pH Level", 4.0, 9.0, 6.0, step=0.1)
        location = st.selectbox("📍 Farm Location", list(LOCATION_TIPS.keys()))
    with col2:
        season = st.selectbox("🌦️ Current Season", ["Dry Season", "Rainy Season"])
        farm_size = st.number_input("📐 Farm Size (hectares)", 1, 100, 5)

    st.divider()

    if st.button("🔍 Analyse My Soil", use_container_width=True):
        st.session_state.analysis_data = {
            "ph": ph, "location": location,
            "season": season, "farm_size": farm_size
        }
        st.session_state.page = "loading"
        st.rerun()

# ==========================================
# PAGE 2: LOADING
# ==========================================
elif st.session_state.page == "loading":
    st.markdown("# 🌱 Crop Predator")
    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 🔬 Analyzing Your Soil...")
        st.markdown("**Please wait while we process your farm data**")

    with st.spinner(""):
        st.write("⏳ Processing soil samples...")
        time.sleep(1)
        st.write("📊 Analyzing pH levels...")
        time.sleep(1)
        st.write("🌿 Calculating fertilizer needs...")
        time.sleep(1)
        st.write("💰 Running profitability model...")
        time.sleep(2)
        st.write("🌾 Matching optimal crops...")
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

    st.markdown("# Crop Predator")
    st.markdown("### ✅ Analysis Complete!")
    st.divider()

    # ── Farm Profile ──────────────────────
    st.markdown("### 📊 Your Farm Profile")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📍 Location", location)
        st.metric("🧪 pH Level", f"{ph:.1f}")
    with col2:
        st.metric("🌦️ Season", season)
        st.metric("📐 Farm Size", f"{farm_size} ha")

    st.divider()

    # ── Best Crops ────────────────────────
    best_crops = [
        (crop, info) for crop, info in CROPS.items()
        if info["ph_range"][0] <= ph <= info["ph_range"][1]
        and info["season"] == season
    ]

    st.markdown("### Best Crops for Your Farm")
    if best_crops:
        best_crops_sorted = sorted(
            best_crops,
            key=lambda x: float(x[1]["yield"].split("-")[1].split()[0]),
            reverse=True
        )[:3]

        for idx, (crop, info) in enumerate(best_crops_sorted, 1):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"### {idx}. {info['emoji']} {crop}")
            with col2 :
                st.success("✨ Perfect!")
            with col3:
                st.write(f" {info['yield']}")
            with col4:
                st.write(f" pH: {info['ph_range'][0]}-{info['ph_range'][1]}")
            
                
    else:
        st.warning("⚠️ No ideal crops for this pH in current season.")

    st.divider()

    # ── Soil Amendment ────────────────────
    st.markdown("### Soil Amendment Recommendations")
    if ph < 5.5:
        st.error(f"❌ **Highly Acidic Soil (pH {ph:.1f})**")
        st.write("**Solution:** Apply Agricultural Lime (CaCO₃)")
        st.write("**Dosage:** 2-3 tons/hectare")
        st.write("**Timeline:** Wait 2-4 weeks before planting")
    elif ph > 7.5:
        st.error(f"❌ **Alkaline Soil (pH {ph:.1f})**")
        st.write("**Solution:** Apply Elemental Sulfur")
        st.write("**Dosage:** 1-2 tons/hectare")
        st.write("**Timeline:** 3-6 months for effect")
    else:
        st.success(f"✅ **Ideal pH Range (pH {ph:.1f})**")
        st.write(" Your soil pH is perfect! No amendment needed.")

    st.divider()

    # ── SMART FERTILIZER RECOMMENDATIONS ──
    st.markdown("### 🌿 Smart Fertilizer Recommendations")

    if best_crops:
        for crop, info in best_crops_sorted:
            fert = FERTILIZER.get(crop, None)
            if fert:
                with st.expander(f"{info['emoji']} Fertilizer Plan for {crop}"):
                    if ph < info["ph_range"][0]:
                        st.warning(f"⚠️ Your pH ({ph}) is too low for {crop}")
                        st.write(f"{fert['acidic']}")
                    elif ph > info["ph_range"][1]:
                        st.warning(f"⚠️ Your pH ({ph}) is too high for {crop}")
                        st.write(f"{fert['alkaline']}")
                    else:
                        st.success(f"✅ pH is optimal for {crop}!")
                        st.write(f"🌱 {fert['optimal']}")
    else:
        st.info("Select suitable crops to see fertilizer recommendations.")

    st.divider()

    # ── SOIL PROFILE ──────────────────────
    st.markdown("### 🗺️ Local Soil Profile Analysis")
    if location in SOIL_PROFILES:
        profile = SOIL_PROFILES[location]
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"🪨 **Soil Type:** {profile['soil_type']}")
            st.write(f"🌿 **Organic Matter:** {profile['organic_matter']}")
        with col2:
            st.write(f"💧 **Drainage:** {profile['drainage']}")
            st.warning(f"⚠️ **Challenge:** {profile['challenge']}")
        st.success(f"💡 **Expert Tip:** {profile['tip']}")

    st.divider()

    # ── PROFITABILITY CALCULATOR ──────────
    st.markdown("### 💰 Farm Profitability Calculator")
    st.write("Estimate your potential revenue based on your farm size and top crop.")

    if best_crops:
        top_crop, top_info = best_crops_sorted[0]

        col1, col2 = st.columns(2)
        with col1:
            seed_cost = st.number_input(
                "Seed Cost (₦ per hectare)",
                min_value=0,
                value=15000,
                step=1000
            )
        with col2:
            labor_cost = st.number_input(
                "Labor Cost (₦ per hectare)",
                min_value=0,
                value=30000,
                step=1000
            )

        fertilizer_cost = st.number_input(
            "Fertilizer Cost (₦ per hectare)",
            min_value=0,
            value=25000,
            step=1000
        )

        if st.button("📊 Calculate Profit", use_container_width=True):
            # Get yield range (use average)
            yield_parts = top_info["yield"].replace(" tons/ha", "").split("-")
            min_yield = float(yield_parts[0])
            max_yield = float(yield_parts[1])
            avg_yield = (min_yield + max_yield) / 2

            price_per_ton = top_info["price_per_ton"]

            # Calculate totals
            total_yield = avg_yield * farm_size
            gross_revenue = total_yield * price_per_ton
            total_cost = (seed_cost + labor_cost + fertilizer_cost) * farm_size
            net_profit = gross_revenue - total_cost
            roi = ((net_profit / total_cost) * 100) if total_cost > 0 else 0

            st.divider()
            st.markdown(f"#### 📈 Results for {top_info['emoji']} {top_crop} on {farm_size} ha")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Expected Yield", f"{total_yield:.1f} tons")
            with col2:
                st.metric("Gross Revenue", f"₦{gross_revenue:,.0f}")
            with col3:
                st.metric("Net Profit", f"₦{net_profit:,.0f}")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Cost", f"₦{total_cost:,.0f}")
            with col2:
                st.metric("ROI", f"{roi:.1f}%")

            if net_profit > 0:
                st.success(f"This farm is PROFITABLE! You can make ₦{net_profit:,.0f} this season.")
            else:
                st.error("⚠️ Costs exceed revenue. Consider reducing input costs or choosing a different crop.")

    st.divider()

    # ── Location Tip ──────────────────────
    st.markdown("### 💡 Location-Specific Expertise")
    st.info(f"📍 **{location}**\n\n{LOCATION_TIPS[location]}")

    st.divider()

    if st.button("🔄 Analyse Another Farm", use_container_width=True):
        st.session_state.page = "input"
        st.rerun()

# ==========================================
# FOOTER
# ==========================================
if st.session_state.page != "loading":
    st.divider()
    st.markdown("""
**🌱 Developed by:** Mubarak Haruna | Level 2 Crop Science, FUD  
**Purpose:** Data-Driven Agriculture for Nigerian Farmers  
**Location:** Federal University of Dutse (FUD)
""")