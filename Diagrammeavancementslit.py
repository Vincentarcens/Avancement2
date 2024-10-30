import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Configurer le titre et l'icône de la page
st.set_page_config(page_title="Simulation d'une réaction chimique", page_icon="⚗️")
st.markdown("<h1 style='font-size: 36px;'>Simulation d'une réaction chimique</h1>", unsafe_allow_html=True)

# Initialisation des valeurs de session
if "avancement" not in st.session_state:
    st.session_state.avancement = 0.0

# Demande des noms des réactifs et des produits avec syntaxe LaTeX
nom_A = st.text_input("Nom du réactif A (utilisez ^ pour les exposants et _ pour les indices)", "H^+")
nom_B = st.text_input("Nom du réactif B (utilisez ^ pour les exposants et _ pour les indices)", "Mg")
nom_C = st.text_input("Nom du produit C (utilisez ^ pour les exposants et _ pour les indices)", "H_2")
nom_D = st.text_input("Nom du produit D (utilisez ^ pour les exposants et _ pour les indices)", "Mg^{2+}")

# Demande des coefficients stoechiométriques des réactifs et des produits
coeff_A = st.number_input(f"Coefficient stœchiométrique de {nom_A}", value=1.0)
coeff_B = st.number_input(f"Coefficient stœchiométrique de {nom_B}", value=1.0)
coeff_C = st.number_input(f"Coefficient stœchiométrique de {nom_C}", value=1.0)
coeff_D = st.number_input(f"Coefficient stœchiométrique de {nom_D}", value=1.0)

# Quantité initiale des réactifs
quantite_initiale_A = st.number_input(f"Quantité initiale de {nom_A}", value=10.0)
quantite_initiale_B = st.number_input(f"Quantité initiale de {nom_B}", value=10.0)

# Calcul de l'avancement où l'un des réactifs est consommé (réactif limitant)
avancement_A_epuise = quantite_initiale_A / coeff_A
avancement_B_epuise = quantite_initiale_B / coeff_B

# L'avancement maximal de la réaction est déterminé par le réactif limitant
avancement_max = min(avancement_A_epuise, avancement_B_epuise)

# Slider pour contrôler l'avancement manuel
avancement_slider = st.slider(
    "Avancement de la réaction", 
    0.0, 
    avancement_max, 
    value=st.session_state.avancement, 
    step=avancement_max / 100
)

# Synchroniser le slider avec la session state
st.session_state.avancement = avancement_slider

# Bouton pour augmenter l'avancement
if st.button("Avancer"):
    st.session_state.avancement += avancement_max / 25  # Incrémente de 4% à chaque clic
    st.session_state.avancement = min(st.session_state.avancement, avancement_max)  # Limite à l'avancement max

# Bouton pour remettre à zéro
if st.button("Remise à zéro"):
    st.session_state.avancement = 0.0

# Utiliser la valeur de session pour l'avancement
avancement = st.session_state.avancement

# Quantités en fonction de l'avancement
quantite_A = quantite_initiale_A - coeff_A * avancement  # réactif A
quantite_B = quantite_initiale_B - coeff_B * avancement  # réactif B
quantite_C = coeff_C * avancement                       # produit C
quantite_D = coeff_D * avancement                       # produit D

# Calcul du maximum pour l'axe des ordonnées
y_max = max(quantite_initiale_A, quantite_initiale_B, quantite_C, quantite_D) * 1.2  # un peu d'espace au-dessus

# Préparation du graphique
fig, ax = plt.subplots()
bar_positions = [0, 1, 2, 3]
bar_heights = [quantite_A, quantite_B, quantite_C, quantite_D]
bar_labels = [nom_A, nom_B, nom_C, nom_D]

ax.bar(bar_positions, bar_heights, color=['blue', 'orange', 'green', 'red'])
ax.set_ylim(0, y_max)
ax.set_xticks([])  # Masquer les étiquettes x

# Génération de l'équation de réaction avec suppression des coefficients de 1
equation_text = (
    rf"${'' if coeff_A == 1 else int(coeff_A)}{nom_A} + "
    rf"{'' if coeff_B == 1 else int(coeff_B)}{nom_B} \rightarrow "
    rf"{'' if coeff_C == 1 else int(coeff_C)}{nom_C} + "
    rf"{'' if coeff_D == 1 else int(coeff_D)}{nom_D}$"
)
ax.set_title(equation_text, pad=20)

# Ajouter les noms des réactifs et produits sous les barres en utilisant LaTeX
for i, label in enumerate(bar_labels):
    ax.text(i, -y_max * 0.05, f"${label}$", ha='center', va='top', fontsize=12)  # Position sous les barres

# Afficher les quantités juste au-dessus des barres, sans chevauchement avec le titre
for i, height in enumerate(bar_heights):
    position = y_max * 0.95  # Position des annotations légèrement en dessous de l'équation de réaction
    ax.text(i, position, f'{height:.4f}', ha='center', va='bottom', fontsize=10)

# Afficher le graphique dans Streamlit
st.pyplot(fig)
