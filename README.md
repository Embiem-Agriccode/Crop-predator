# 🌱 SoilIQ (formerly Crop Predator)

**Soil-aware fertilizer and profitability guidance for Nigerian farmers.**

SoilIQ is a Streamlit web app that helps farmers, extension workers, and agric students estimate fertilizer needs and expected returns for common Nigerian crops, based on soil profile and farm size.

🔗 **Live app:** `https://crop-predator.streamlit.app/`
📦 **Repo:** [github.com/Embiem-Agriccode/Crop-predator](https://github.com/Embiem-Agriccode/Crop-predator)

---

## ⚠️ Important Notice

SoilIQ is an **advisory tool, not a replacement for a soil test or an extension officer.** Fertilizer recommendations are estimates and are currently being **validated against institutional feedback**. Always confirm dosages with a certified agronomist or your local ADP/extension office before applying.

---

## Features

- **Fertilizer dosage calculator**: recommended fertilizer quantities per crop and farm size
- **ROI estimator**: projected costs, revenue, and profit for a planting season
- **Batch CSV upload**: analyze multiple farms or plots at once, with interactive Plotly charts
- **Downloadable farm reports**: export results to share or keep for records
- **Wide coverage**: 23 Nigerian crops and 13 location-based soil profiles

## Tech Stack

- Python
- Streamlit (UI and deployment on Streamlit Cloud)
- Pandas (data handling)
- Plotly (charts)

## Getting Started

```bash
# 1. Clone the repo
git clone https://github.com/Embiem-Agriccode/Crop-predator.git
cd Crop-predator

# 2. (Optional) create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

> Replace `app.py` with the actual entry file name if it differs.

## Batch Upload Format

Upload a CSV with one row per farm or plot. Example:

| crop | soil_profile | farm_size_ha |
|------|--------------|--------------|
| Maize | Kano Savanna | 2.5 |
| Rice | Jigawa Floodplain | 1.0 |

> Update column names to match what the app actually expects.

## Roadmap

- [ ] Review and recalibrate fertilizer dosage logic against extension guidelines
- [ ] Coordinate-based (lat/long) soil mapping, since soil varies within the same LGA
- [ ] LGA-level soil data via NAERLS
- [ ] Real-time data integration
- [ ] Machine learning layer for yield and recommendation modeling

## Known Limitations

- Soil profiles are location-based, not field-specific
- Dosage recommendations are under review and may overestimate
- No live weather or soil sensor data yet

## Author

Built by **Mubarak** under **EMBIEM**, a student tech agency.
Crop Science, Federal University Dutse.

GitHub: [Embiem-Agriccode](https://github.com/Embiem-Agriccode)

## Contributing

Suggestions and feedback from agronomists, extension workers, and farmers are welcome. Open an issue or reach out directly.

## License

`<choose one, e.g. MIT>`
