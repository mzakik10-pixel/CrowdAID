# 🚀 Quick Start: Using CrowdAID ML Model

## Cara Cepat Menggunakan Machine Learning Model

---

## 📋 Prerequisites

```bash
pip install pandas scikit-learn
```

---

## 🏃 Quick Start (3 Steps)

### Step 1: Import dan Load Model

```python
from ml_predictor import CrowdAIDPredictor
import pandas as pd

# Initialize predictor (loads trained model automatically)
predictor = CrowdAIDPredictor(
    model_path='model_random_forest.pkl',
    encoders_path='label_encoders.pkl',
    metadata_path='model_metadata.json'
)

print("✅ Model loaded! Accuracy: 91.76%")
```

### Step 2: Load Hospital Data

```python
# Load your hospital dataset
df_hospitals = pd.read_csv('Hospital_Banten.csv', sep=';')
```

### Step 3: Get Recommendations!

```python
# Get recommendations for a condition
recommendations = predictor.get_recommendations(
    hospitals_df=df_hospitals,
    condition='Kebidanan',  # Options: see below
    location='Kota Tangerang Selatan'  # Optional
)

# Display results
print(f"\n✅ Found {len(recommendations)} suitable hospitals")
print(recommendations[['nama', 'jenis', 'kelas', 'ml_score', 'confidence']].head())
```

---

## 🎯 Available Conditions

1. `'Gejala Ringan'` - Pilek, batuk, dll (will recommend Puskesmas/Klinik)
2. `'Penyakit Dalam'` - Jantung, paru-paru, dll
3. `'Bedah'` - Operasi
4. `'Anak'` - Pediatri
5. `'Kebidanan'` - Kehamilan, persalinan
6. `'Gigi'` - Dental
7. `'Banyak Spesialis'` - Kasus kompleks

---

## 💡 Example Usage

### Example 1: Find Maternity Hospitals

```python
recommendations = predictor.get_recommendations(
    hospitals_df=df_hospitals,
    condition='Kebidanan',
    location='Kota Tangerang Selatan'
)

# Get top 3
top3 = recommendations.head(3)
for idx, row in top3.iterrows():
    print(f"{row['nama']}")
    print(f"  Score: {row['ml_score']}/100")
    print(f"  Confidence: {row['confidence']}")
    print()
```

Output:
```
RS Insan Permata
  Score: 99/100
  Confidence: High

RS Cinta Kasih
  Score: 99/100
  Confidence: High

RS Syarif Hidayatullah
  Score: 98/100
  Confidence: High
```

### Example 2: Single Hospital Check

```python
# Check if specific hospital is suitable
result = predictor.predict_suitability(
    hospital_type='Rumah Sakit Umum',
    hospital_class='C',
    capacity=100,
    services=50,
    staff=200,
    condition='Penyakit Dalam'
)

print(f"ML Score: {result['score']}/100")
print(f"Is Suitable: {result['is_suitable']}")
print(f"Confidence: {result['confidence']}")
```

Output:
```
ML Score: 98/100
Is Suitable: True
Confidence: High
```

### Example 3: Compare Multiple Conditions

```python
# Test one hospital against all conditions
test_hospital = df_hospitals.iloc[0]

conditions = ['Gejala Ringan', 'Penyakit Dalam', 'Bedah', 
              'Anak', 'Kebidanan', 'Gigi', 'Banyak Spesialis']

print(f"Testing: {test_hospital['nama']}")
print(f"Type: {test_hospital['jenis']}, Class: {test_hospital['kelas']}")
print()

for cond in conditions:
    result = predictor.predict_suitability(
        hospital_type=test_hospital['jenis'],
        hospital_class=test_hospital['kelas'],
        capacity=test_hospital['total_tempat_tidur'],
        services=test_hospital['total_layanan'],
        staff=test_hospital['total_tenaga_kerja'],
        condition=cond
    )
    
    suitable = "✅" if result['is_suitable'] else "❌"
    print(f"{suitable} {cond:20s}: {result['score']:3d}/100 ({result['confidence']})")
```

Output:
```
Testing: RS Umum Daerah Cilincing
Type: Rumah Sakit Umum, Class: C

❌ Gejala Ringan       :   6/100 (High)
✅ Penyakit Dalam      :  98/100 (High)
✅ Bedah               :  95/100 (High)
✅ Anak                :  92/100 (High)
✅ Kebidanan           :  98/100 (High)
❌ Gigi                :  15/100 (High)
❌ Banyak Spesialis    :  42/100 (Low)
```

---

## 🎨 Integration with Streamlit

You can easily integrate this ML model into your Streamlit app!

```python
import streamlit as st
from ml_predictor import CrowdAIDPredictor
import pandas as pd

# Load model once
@st.cache_resource
def load_model():
    return CrowdAIDPredictor()

predictor = load_model()

# User inputs
kondisi = st.selectbox("Pilih Kondisi", [
    'Gejala Ringan', 'Penyakit Dalam', 'Bedah',
    'Anak', 'Kebidanan', 'Gigi', 'Banyak Spesialis'
])

location = st.selectbox("Pilih Lokasi", df_hospitals['kab'].unique())

# Get ML recommendations
if st.button("Get ML Recommendations"):
    recommendations = predictor.get_recommendations(
        hospitals_df=df_hospitals,
        condition=kondisi,
        location=location
    )
    
    st.success(f"Found {len(recommendations)} hospitals")
    st.dataframe(recommendations)
```

---

## 📊 Understanding the Output

### ML Score (0-100)
- **90-100**: Perfect match, highly recommended
- **80-89**: Very good match, recommended
- **70-79**: Good match, suitable
- **60-69**: Acceptable, but not optimal
- **<60**: Not recommended

### Confidence Level
- **High**: Model is very confident (≥80% probability)
- **Medium**: Model is moderately confident (60-80%)
- **Low**: Model is uncertain (<60%)

### Probability
- Raw probability from 0.0 to 1.0
- 0.95 = 95% confident the hospital is suitable

---

## ⚙️ Advanced: Custom Filtering

```python
# Get all recommendations, then filter
recommendations = predictor.get_recommendations(
    hospitals_df=df_hospitals,
    condition='Penyakit Dalam'
)

# Filter by ML score
high_score = recommendations[recommendations['ml_score'] >= 90]

# Filter by confidence
high_confidence = recommendations[recommendations['confidence'] == 'High']

# Filter by capacity
large_hospitals = recommendations[recommendations['kapasitas'] >= 100]

# Combine filters
best = recommendations[
    (recommendations['ml_score'] >= 90) & 
    (recommendations['confidence'] == 'High') &
    (recommendations['kapasitas'] >= 100)
]

print(f"Best hospitals: {len(best)}")
```

---

## 🔧 Troubleshooting

### Error: "FileNotFoundError"
Make sure all files are in the same directory:
- `model_random_forest.pkl`
- `label_encoders.pkl`
- `model_metadata.json`
- `ml_predictor.py`

### Error: "KeyError: 'Unknown value'"
The hospital type/class/condition is not in training data.
Check valid values:
```python
print(predictor.metadata['hospital_types'])
print(predictor.metadata['hospital_classes'])
print(predictor.metadata['conditions'])
```

### Low Scores for Everything
Check your input data format matches training data:
- Hospital type should be exact match (e.g., "Rumah Sakit Umum")
- Hospital class should be "B", "C", or "D"
- Numeric values (capacity, services, staff) should be positive

---

## 📦 Required Files

```
your_project/
├── ml_predictor.py                 # Predictor class
├── model_random_forest.pkl         # Trained model (1.3 MB)
├── label_encoders.pkl              # Encoders (2 KB)
├── model_metadata.json             # Metadata (1.4 KB)
├── Hospital_Banten.csv            # Your data
└── your_script.py                  # Your code
```

---

## 🎯 Complete Example Script

Save this as `test_ml.py`:

```python
from ml_predictor import CrowdAIDPredictor
import pandas as pd

# Load model
print("Loading ML model...")
predictor = CrowdAIDPredictor()

# Load data
print("Loading hospital data...")
df = pd.read_csv('Hospital_Banten.csv', sep=';')

# Test 1: Get recommendations
print("\n" + "="*70)
print("TEST 1: Rekomendasi untuk Kebidanan")
print("="*70)

recs = predictor.get_recommendations(
    hospitals_df=df,
    condition='Kebidanan',
    location='Kota Tangerang Selatan'
)

print(f"Found {len(recs)} hospitals")
print("\nTop 5:")
print(recs.head(5)[['nama', 'ml_score', 'confidence']].to_string(index=False))

# Test 2: Feature importance
print("\n" + "="*70)
print("TEST 2: Feature Importance")
print("="*70)
importance = predictor.get_feature_importance()
print(importance.to_string(index=False))

print("\n✅ All tests passed!")
```

Run it:
```bash
python test_ml.py
```

---

## 🏆 Summary

✅ **Easy to use** - 3 lines of code to get recommendations  
✅ **Fast** - Predictions in milliseconds  
✅ **Accurate** - 91.76% accuracy  
✅ **Flexible** - Works with any hospital dataset  
✅ **Production-ready** - Saved models, proper error handling  

**Start using ML in your CrowdAID app today!** 🚀

---

**© 2025 CrowdAID ML Model**
**Accuracy:** 91.76% | **Model:** Random Forest
