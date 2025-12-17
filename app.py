import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="CrowdAID - Smart Hospital Recommendation",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    h1, h2, h3 {
        color: white !important;
    }
    .stSelectbox label, .stRadio label {
        color: white !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2em;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df_hospital = pd.read_csv('Hospital_Banten.csv', sep=';')
    df_faskes = pd.read_csv('Faskes_BPJS_Banten_2019.csv')
    df_faskes['KotaKab_Clean'] = df_faskes['KotaKab'].str.extract(r'(Kab\.|Kota)\s+(.+?)(?:\r|$)', expand=False)[1]
    df_faskes['KotaKab_Clean'] = df_faskes['KotaKab_Clean'].str.strip()
    return df_hospital, df_faskes

df_hospital, df_faskes = load_data()
kabupaten_list = sorted(df_hospital['kab'].unique().tolist())

# Title
st.title("🏥 CrowdAID")
st.subheader("Sistem Rekomendasi Fasilitas Kesehatan Cerdas Berbasis AI")
st.markdown("**Provinsi Banten**")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📊 Statistik Dataset")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🏥 Rumah Sakit", len(df_hospital))
        st.metric("🏛️ Kelas B", len(df_hospital[df_hospital['kelas'] == 'B']))
        st.metric("🏛️ Kelas C", len(df_hospital[df_hospital['kelas'] == 'C']))
    with col2:
        st.metric("🏥 Puskesmas", len(df_faskes[df_faskes['TipeFaskes'] == 'Puskesmas']))
        st.metric("🏥 Klinik", len(df_faskes[df_faskes['TipeFaskes'] == 'Klinik Pratama']))
        st.metric("🏛️ Kelas D", len(df_hospital[df_hospital['kelas'] == 'D']))
    
    st.markdown("---")
    st.header("🤖 Tentang AI Classification")
    st.info("""
    **CrowdAID** menggunakan **Rule-Based Classification Model** untuk mengarahkan pasien ke fasilitas kesehatan yang tepat.
    
    **Model Klasifikasi:**
    - 📍 Location-based filtering
    - 🏥 Facility type classification
    - ⭐ Priority ranking
    - 🎯 Smart recommendation
    """)
    
    st.markdown("---")
    st.success("""
    **SDG #3: Good Health and Well-being**
    
    Mengatasi masalah:
    ✅ Hospital overcrowding
    ✅ Inefficient referrals
    ✅ Better resource distribution
    """)

# Main content
col1, col2 = st.columns([1, 2])

with col1:
    st.header("🎯 Input Pasien")
    
    kabupaten = st.selectbox(
        "📍 Pilih Kabupaten/Kota",
        kabupaten_list,
        index=0
    )
    
    st.markdown("⚕️ **Pilih Kondisi Pasien:**")
    kondisi_options = {
        "1": "🤧 Gejala Ringan (Pilek, Batuk, Sakit Perut, Pusing)",
        "2": "💔 Penyakit Dalam (Jantung, Paru-paru, dll)",
        "3": "⚕️ Bedah (Operasi)",
        "4": "👶 Anak",
        "5": "🤰 Kebidanan",
        "6": "🦷 Gigi",
        "7": "🏥 Banyak Spesialis / Komprehensif"
    }
    
    kondisi = st.selectbox(
        "Kondisi",
        options=list(kondisi_options.keys()),
        format_func=lambda x: kondisi_options[x],
        label_visibility="collapsed"
    )
    
    st.markdown("")
    cari_button = st.button("🔍 Cari Rekomendasi AI", type="primary", use_container_width=True)

with col2:
    st.header("🏥 Hasil Rekomendasi")
    
    if cari_button:
        with st.spinner("🤖 AI sedang menganalisis..."):
            recommendations = []
            classification_info = ""
            
            if kondisi == "1":
                classification_info = """
                **🤖 AI Classification Result:**
                - **Kategori:** Gejala Ringan
                - **Rekomendasi:** Puskesmas atau Klinik Pratama
                - **Alasan:** Kondisi tidak memerlukan fasilitas RS, dapat ditangani di layanan primer
                """
                
                puskesmas = df_faskes[
                    (df_faskes['TipeFaskes'] == 'Puskesmas') & 
                    (df_faskes['KotaKab'].str.contains(kabupaten, case=False, na=False))
                ]
                
                klinik = df_faskes[
                    (df_faskes['TipeFaskes'].str.contains('Klinik', case=False, na=False)) & 
                    (df_faskes['KotaKab'].str.contains(kabupaten, case=False, na=False))
                ]
                
                for _, row in puskesmas.head(5).iterrows():
                    recommendations.append({
                        'nama': row['NamaFaskes'].strip(),
                        'alamat': row['AlamatFaskes'],
                        'tipe': 'Puskesmas',
                        'kelas': '-',
                        'score': 95
                    })
                
                for _, row in klinik.head(3).iterrows():
                    recommendations.append({
                        'nama': row['NamaFaskes'].strip(),
                        'alamat': row['AlamatFaskes'],
                        'tipe': 'Klinik Pratama',
                        'kelas': '-',
                        'score': 90
                    })
            
            elif kondisi == "6":
                classification_info = """
                **🤖 AI Classification Result:**
                - **Kategori:** Kesehatan Gigi
                - **Rekomendasi:** RS Kelas D atau Klinik Gigi
                - **Alasan:** Masalah gigi memerlukan fasilitas dental khusus
                """
                
                rs_d = df_hospital[
                    (df_hospital['kelas'] == 'D') & 
                    (df_hospital['kab'] == kabupaten)
                ]
                
                klinik_gigi = df_faskes[
                    (df_faskes['TipeFaskes'].str.contains('Gigi', case=False, na=False)) & 
                    (df_faskes['KotaKab'].str.contains(kabupaten, case=False, na=False))
                ]
                
                for _, row in rs_d.iterrows():
                    recommendations.append({
                        'nama': row['nama'],
                        'alamat': row['alamat'],
                        'tipe': row['jenis'],
                        'kelas': 'D',
                        'kapasitas': row['total_tempat_tidur'],
                        'layanan': row['total_layanan'],
                        'score': 95
                    })
                
                for _, row in klinik_gigi.head(3).iterrows():
                    recommendations.append({
                        'nama': row['NamaFaskes'].strip(),
                        'alamat': row['AlamatFaskes'],
                        'tipe': 'Klinik Gigi',
                        'kelas': '-',
                        'score': 85
                    })
            
            elif kondisi == "7":
                classification_info = """
                **🤖 AI Classification Result:**
                - **Kategori:** Komprehensif / Multi-Spesialis
                - **Rekomendasi:** RS Kelas B
                - **Alasan:** Kondisi kompleks memerlukan RS dengan banyak spesialis dan fasilitas lengkap
                """
                
                rs_b = df_hospital[
                    (df_hospital['kelas'] == 'B') & 
                    (df_hospital['kab'] == kabupaten)
                ].sort_values('total_layanan', ascending=False)
                
                for idx, row in rs_b.iterrows():
                    recommendations.append({
                        'nama': row['nama'],
                        'alamat': row['alamat'],
                        'tipe': row['jenis'],
                        'kelas': 'B',
                        'kapasitas': row['total_tempat_tidur'],
                        'layanan': row['total_layanan'],
                        'staff': row['total_tenaga_kerja'],
                        'score': 100 - (len(recommendations) * 3)
                    })
            
            else:
                kondisi_map = {
                    "2": "Penyakit Dalam",
                    "3": "Bedah",
                    "4": "Anak",
                    "5": "Kebidanan"
                }
                
                classification_info = f"""
                **🤖 AI Classification Result:**
                - **Kategori:** {kondisi_map[kondisi]}
                - **Rekomendasi:** RS Kelas C
                - **Alasan:** Kondisi memerlukan perawatan RS dengan spesialisasi, kelas C optimal untuk kasus ini
                """
                
                rs_c = df_hospital[
                    (df_hospital['kelas'] == 'C') & 
                    (df_hospital['kab'] == kabupaten)
                ]
                
                if kondisi in ["4", "5"]:
                    rs_spesialis = rs_c[rs_c['jenis'].str.contains('Ibu dan Anak', case=False, na=False)]
                    rs_umum = rs_c[rs_c['jenis'].str.contains('Umum', case=False, na=False)]
                    
                    for idx, row in rs_spesialis.iterrows():
                        recommendations.append({
                            'nama': row['nama'],
                            'alamat': row['alamat'],
                            'tipe': row['jenis'],
                            'kelas': 'C',
                            'kapasitas': row['total_tempat_tidur'],
                            'layanan': row['total_layanan'],
                            'score': 100
                        })
                    
                    for idx, row in rs_umum.head(5).iterrows():
                        recommendations.append({
                            'nama': row['nama'],
                            'alamat': row['alamat'],
                            'tipe': row['jenis'],
                            'kelas': 'C',
                            'kapasitas': row['total_tempat_tidur'],
                            'layanan': row['total_layanan'],
                            'score': 85
                        })
                
                elif kondisi == "3":
                    rs_bedah = rs_c[rs_c['jenis'].str.contains('Bedah', case=False, na=False)]
                    rs_umum = rs_c[rs_c['jenis'].str.contains('Umum', case=False, na=False)]
                    
                    for idx, row in rs_bedah.iterrows():
                        recommendations.append({
                            'nama': row['nama'],
                            'alamat': row['alamat'],
                            'tipe': row['jenis'],
                            'kelas': 'C',
                            'kapasitas': row['total_tempat_tidur'],
                            'layanan': row['total_layanan'],
                            'score': 100
                        })
                    
                    for idx, row in rs_umum.head(5).iterrows():
                        recommendations.append({
                            'nama': row['nama'],
                            'alamat': row['alamat'],
                            'tipe': row['jenis'],
                            'kelas': 'C',
                            'kapasitas': row['total_tempat_tidur'],
                            'layanan': row['total_layanan'],
                            'score': 88
                        })
                
                else:
                    rs_umum = rs_c[rs_c['jenis'].str.contains('Umum', case=False, na=False)].sort_values('total_layanan', ascending=False)
                    
                    for idx, row in rs_umum.iterrows():
                        recommendations.append({
                            'nama': row['nama'],
                            'alamat': row['alamat'],
                            'tipe': row['jenis'],
                            'kelas': 'C',
                            'kapasitas': row['total_tempat_tidur'],
                            'layanan': row['total_layanan'],
                            'score': 95 - (len(recommendations) * 2)
                        })
            
            # Display results
            st.info(classification_info)
            
            if len(recommendations) == 0:
                st.warning(f"⚠️ Tidak ditemukan fasilitas kesehatan yang sesuai di {kabupaten}. Coba kabupaten lain atau hubungi layanan darurat 119.")
            else:
                st.success(f"✅ Ditemukan **{len(recommendations)}** rekomendasi fasilitas kesehatan")
                
                # Display each recommendation
                for idx, rec in enumerate(recommendations[:10]):
                    is_top = idx == 0
                    
                    # Create container with proper styling
                    with st.container():
                        if is_top:
                            st.markdown("### ⭐ REKOMENDASI TERBAIK")
                        
                        st.markdown(f"### {idx + 1}. {rec['nama']}")
                        st.markdown(f"**🏥 Tipe:** {rec['tipe']}")
                        st.markdown(f"**🏛️ Kelas:** {rec['kelas']}")
                        st.markdown(f"**📍 Alamat:** {rec['alamat']}")
                        
                        if 'kapasitas' in rec:
                            st.markdown(f"**🛏️ Kapasitas:** {rec['kapasitas']} tempat tidur")
                        if 'layanan' in rec:
                            st.markdown(f"**⚕️ Layanan:** {rec['layanan']} jenis")
                        
                        # Score badge
                        if is_top:
                            st.success(f"🤖 AI Score: {rec['score']}/100")
                        else:
                            st.info(f"🤖 AI Score: {rec['score']}/100")
                        
                        st.markdown("---")
                
                # Summary
                st.markdown("### 📋 Ringkasan Rekomendasi")
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Total Rekomendasi", len(recommendations))
                with col_b:
                    avg_score = sum(r['score'] for r in recommendations[:5]) / min(5, len(recommendations))
                    st.metric("Rata-rata AI Score", f"{avg_score:.1f}/100")
                with col_c:
                    st.metric("Top Score", f"{recommendations[0]['score']}/100" if recommendations else "N/A")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: white; padding: 20px;">
    <p><strong>CrowdAID - Smart Hospital Recommendation System</strong></p>
    <p>Powered by AI Classification Model | SDG #3: Good Health and Well-being</p>
    <p style="font-size: 0.9em;">© 2025 - Artificial Intelligence Project | COMP6056001</p>
</div>
""", unsafe_allow_html=True)
