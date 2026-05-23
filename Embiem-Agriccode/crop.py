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
    "Cassava":   {"ph_range": (5.5, 6.5), "season": "Rainy Season", "yield": "12-15 tons/ha", "emoji": "🥔"},
    "Yam":       {"ph_range": (5.5, 6.0), "season": "Rainy Season", "yield": "8-12 tons/ha",  "emoji": "🍠"},
    "Rice":      {"ph_range": (5.5, 6.5), "season": "Rainy Season", "yield": "5-7 tons/ha",   "emoji": "🍚"},
    "Maize":     {"ph_range": (5.8, 7.0), "season": "Rainy Season", "yield": "4-6 tons/ha",   "emoji": "🌽"},
    "Groundnut": {"ph_range": (5.9, 7.0), "season": "Dry Season",   "yield": "2-3 tons/ha",   "emoji": "🥜"},
    "Cocoa":     {"ph_range": (5.0, 6.5), "season": "Rainy Season", "yield": "1-2 tons/ha",   "emoji": "🍫"},
    "Plantain":  {"ph_range": (5.5, 7.0), "season": "Rainy Season", "yield": "15-20 tons/ha", "emoji": "🍌"},
    "Tomato":    {"ph_range": (6.0, 7.0), "season": "Dry Season",   "yield": "20-30 tons/ha", "emoji": "🍅"},
    "Sorghum":   {"ph_range": (5.5, 7.5), "season": "Dry Season",   "yield": "2-3 tons/ha",   "emoji": "🌾"},
    "Cowpea":    {"ph_range": (6.0, 7.0), "season": "Rainy Season", "yield": "1-2 tons/ha",   "emoji": "🫘"},
}

LOCATION_TIPS = {
    "Lagos":              "🌊 High humidity. Watch for fungal diseases. Use resistant varieties.",
    "Ogun":               "🌧️ Good rainfall. Focus on rainy season crops for best yield.",
    "Kaduna":             "🔀 Mix of dry and rainy zones. Diversify your crops.",
    "Borno":              "☀️ Very dry climate. Focus on hardy crops like sorghum.",
    "Niger":              "🌱 Moderate rainfall. Groundnut and maize do well.",
    "Oyo":                "🌴 Tropical climate. All crops can thrive here.",
    "Osun":               "✨ Good soil quality. High-value crops recommended.",
    "Rivers":             "💧 High rainfall. Watch drainage. Root crops excel.",
    "Jigawa":             "🏜️ Semi-arid. Millet, sorghum, and groundnut thrive. Use irrigation wisely.",
    "Dutse (FUD Farm Zone)": "🎓 Sandy loam soils. Organic mulching highly recommended. Perfect for student research!",
    "Hadejia":            "🌾 Excellent wetland/fadama areas. Perfect for dry-season irrigated rice.",
    "Kano":               "🏪 High market access. Focus on early-maturing varieties.",
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

    # ── Farm Image ── (fixed path for both local and cloud)
    img_path = Path(__file__).parent / "IMG_20260522_111712.jpg"
    if img_path.exists():
        st.image(str(img_path), width=700, caption="Data-Driven Yields for African Farmers")
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
        st.write("🌾 Matching optimal crops...")
        time.sleep(2)

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

    st.markdown("# 🌱 Crop Predator")
    st.markdown("### ✅ Analysis Complete!")
    st.divider()

    st.markdown("### 📊 Your Farm Profile")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📍 Location", location)
        st.metric("🧪 pH Level", f"{ph:.1f}")
    with col2:
        st.metric("🌦️ Season", season)
        st.metric("📐 Farm Size", f"{farm_size} ha")

    st.divider()

    best_crops = [
        (crop, info) for crop, info in CROPS.items()
        if info["ph_range"][0] <= ph <= info["ph_range"][1]
        and info["season"] == season
    ]

    st.markdown("### ✅ Best Crops for Your Farm")
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
            with col2:
                st.success(f"🎯 {info['yield']}")
            with col3:
                st.info(f"📏 pH: {info['ph_range'][0]}-{info['ph_range'][1]}")
            with col4:
                st.write("✨ Perfect!")
    else:
        st.warning("⚠️ No ideal crops for this pH in current season.")

    st.divider()

    st.markdown("### 🧬 Soil Amendment Recommendations")
    if ph < 5.5:
        st.error(f"❌ **Highly Acidic Soil (pH {ph:.1f})**")
        st.write("🛠️ **Solution:** Apply agricultural lime")
        st.write("📌 **Dosage:** 2-3 tons/hectare")
        st.write("⏱️ **Timeline:** Wait 2-4 weeks before planting")
    elif ph > 7.5:
        st.error(f"❌ **Alkaline Soil (pH {ph:.1f})**")
        st.write("🛠️ **Solution:** Apply elemental sulfur")
        st.write("📌 **Dosage:** 1-2 tons/hectare")
        st.write("⏱️ **Timeline:** 3-6 months for effect")
    else:
        st.success(f"✅ **Ideal pH Range (pH {ph:.1f})**")
        st.write("👍 Your soil pH is perfect! No amendment needed.")

    st.divider()

    st.markdown("### 💡 Location-Specific Expertise")
    st.info(f"📍 **{location}**\n\n{LOCATION_TIPS[location]}")

    st.divider()

    st.markdown("### 📈 Expected Productivity")
    if best_crops:
        top_crop, top_info = sorted(
            best_crops,
            key=lambda x: float(x[1]["yield"].split("-")[1].split()[0]),
            reverse=True
        )[0]
        st.write(f"🌾 **Top Crop:** {top_info['emoji']} **{top_crop}**")
        st.write(f"📊 **Yield Potential:** {top_info['yield']} per hectare")
        st.write(f"💰 **Your Farm ({farm_size} ha):** High productivity expected!")
        st.success("🎉 Ready to plant with confidence!")

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