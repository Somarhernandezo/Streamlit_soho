from pickle import load
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "..", "models", "Smarthphone_addiction_XG_Boost.sav")

model = load(open(model_path, "rb"))

st.title("📱 Predicción de Adicción al Smartphone")

st.markdown("## 🧑‍🤝‍🧑 Datos del usuario")

age = st.slider("Edad", 12, 100, 25)
gender = st.selectbox("Género", ["Masculino", "Femenino", "Otro"])

st.markdown("## 🕒 Tiempo de uso del Smartphone")

daily_screen_time = st.slider("Uso de pantalla diaria (hrs.)", 0.0, 24.0, 6.0, 0.5)
social_media = st.slider("Redes sociales (hrs.)", 0.0, 24.0, 3.0, 0.5)
gaming = st.slider("Juegos y entretenimiento (hrs.)", 0.0, 24.0, 1.0, 0.5)
work_study = st.slider("Trabajo/estudio (hrs.)", 0.0, 24.0, 4.0, 0.5)

st.markdown("## ⚙️ Patrones de uso")

notifications = st.slider("Notificaciones por día", 0, 300, 100)
app_opens = st.slider("Número de apertura de aplicaciones", 0, 200, 50)
weekend = st.slider("Uso de fin de semana (hrs.)", 0.0, 15.0, 6.0, 0.5)
sleep = st.slider("Horas de sueño", 0.0, 24.0, 7.0, 0.5)

st.markdown("## 🧠 Factores psicosociales")

stress_es = st.selectbox("Nivel de estrés", ["Bajo", "Medio", "Alto"])
academic_es = st.selectbox("Impacto académico", ["Sí", "No"])

stress_map = {"Bajo": "Low", "Medio": "Medium", "Alto": "High"}
academic_map = {"Sí": "Yes", "No": "No"}
gender_map = {"Masculino": "Male", "Femenino": "Female", "Otro": "Other"}

stress = stress_map[stress_es]
academic = academic_map[academic_es]
gender = gender_map[gender]

input_dict = {
    'age': age,
    'daily_screen_time_hours': daily_screen_time,
    'social_media_hours': social_media,
    'gaming_hours': gaming,
    'work_study_hours': work_study,
    'sleep_hours': sleep,
    'notifications_per_day': notifications,
    'app_opens_per_day': app_opens,
    'weekend_screen_time': weekend,

    'gender_Male': 1 if gender == "Male" else 0,
    'gender_Other': 1 if gender == "Other" else 0,

    'stress_level_Low': 1 if stress == "Low" else 0,
    'stress_level_Medium': 1 if stress == "Medium" else 0,

    'academic_work_impact_Yes': 1 if academic == "Yes" else 0
}

input_df = pd.DataFrame([input_dict])

expected_cols = [
    'age','daily_screen_time_hours','social_media_hours','gaming_hours',
    'work_study_hours','sleep_hours','notifications_per_day',
    'app_opens_per_day','weekend_screen_time','gender_Male',
    'gender_Other','stress_level_Low','stress_level_Medium',
    'academic_work_impact_Yes'
]

input_df = input_df.reindex(columns=expected_cols, fill_value=0)

st.markdown("## 📊 Visualización del uso")

data = {
    "Pantalla diaria": daily_screen_time,
    "Redes sociales": social_media,
    "Entretenimiento": gaming,
    "Trabajo/Estudio": work_study
}

fig, ax = plt.subplots()
ax.bar(data.keys(), data.values())
ax.set_ylabel("Horas")
ax.set_title("Distribución de uso del smartphone")

st.pyplot(fig)

st.markdown("## 🔮 Predicción")

if st.button("Predecir"):

    prediction = model.predict(input_df)[0]

    if prediction == 1:
        st.error("⚠️ Es adicto al smartphone")
    else:
        st.success("✅ No es adicto al smartphone")