import streamlit as st
import pandas as pd
import pubchempy as pcp
import random

# =====================================================
# RDKit
# =====================================================

try:

    from rdkit import Chem
    from rdkit.Chem import Descriptors
    from rdkit.Chem import Draw
    from rdkit.Chem import Crippen
    from rdkit.Chem import Lipinski
    from rdkit.Chem import rdMolDescriptors

    RDKIT_OK = True

except:

    RDKIT_OK = False

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="IsoChem AI 13.0",
    page_icon="🧪",
    layout="wide"
)

# =====================================================
# CSS FUTURISTA
# =====================================================

st.markdown("""
<style>

/* =====================================================
FONDO GENERAL
===================================================== */

.stApp{

    background:
    radial-gradient(circle at top left,#00ffd530,transparent 20%),
    radial-gradient(circle at bottom right,#00ffd510,transparent 25%),
    linear-gradient(
        135deg,
        #020617,
        #0f172a,
        #111827,
        #1e293b
    );

    background-attachment: fixed;
    overflow-x:hidden;
}

/* =====================================================
SIDEBAR
===================================================== */

section[data-testid="stSidebar"]{

    background:
    linear-gradient(
        180deg,
        #020617,
        #0f172a,
        #111827
    ) !important;

    border-right:
    2px solid #00ffd5;
}

/* =====================================================
TITULOS
===================================================== */

h1,h2,h3,h4,h5,h6{

    color:#00ffd5 !important;

    font-weight:900 !important;
}

/* =====================================================
TEXTOS
===================================================== */

p,label,span{

    color:white !important;
}

/* =====================================================
INPUTS
===================================================== */

input{

    background:white !important;

    color:black !important;

    border-radius:15px !important;

    border:2px solid #00ffd5 !important;
}

/* =====================================================
BOTONES
===================================================== */

.stButton>button{

    background:#00ffd5 !important;

    color:black !important;

    border:none !important;

    border-radius:15px !important;

    padding:12px 24px !important;

    font-size:16px !important;

    font-weight:bold !important;
}

/* =====================================================
CARDS
===================================================== */

.card{

    background:
    linear-gradient(
        135deg,
        rgba(255,255,255,0.04),
        rgba(0,255,213,0.04)
    );

    border:
    1px solid rgba(0,255,213,0.25);

    border-radius:30px;

    padding:30px;

    margin-bottom:30px;
}

/* =====================================================
PORTADA
===================================================== */

.hero{

    background:
    linear-gradient(
        135deg,
        rgba(0,255,213,0.12),
        rgba(255,255,255,0.02)
    );

    border:
    1px solid rgba(0,255,213,0.35);

    padding:70px;

    border-radius:40px;

    text-align:center;

    margin-bottom:35px;
}

.big-title{

    font-size:75px;

    font-weight:900;

    color:#00ffd5;
}

.subtitle{

    font-size:24px;

    color:white;
}

/* =====================================================
SCROLL
===================================================== */

::-webkit-scrollbar{

    width:12px;
}

::-webkit-scrollbar-thumb{

    background:#00ffd5;

    border-radius:20px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION
# =====================================================

if "score" not in st.session_state:
    st.session_state.score = 0

if "analisis" not in st.session_state:
    st.session_state.analisis = {}

# =====================================================
# BASE QUIMICA
# =====================================================

isomer_db = {

    "C3H6O":[

        {
            "nombre":"Acetona",
            "tipo":"Cetona",
            "uso":"Solvente",
            "riesgo":"Inflamable",
            "smiles":"CC(=O)C"
        },

        {
            "nombre":"Propanal",
            "tipo":"Aldehído",
            "uso":"Industria química",
            "riesgo":"Tóxico",
            "smiles":"CCC=O"
        }

    ],

    "C2H6O":[

        {
            "nombre":"Etanol",
            "tipo":"Alcohol",
            "uso":"Combustible",
            "riesgo":"Inflamable",
            "smiles":"CCO"
        },

        {
            "nombre":"Dimetil éter",
            "tipo":"Éter",
            "uso":"Aerosoles",
            "riesgo":"Inflamable",
            "smiles":"COC"
        }

    ],

    "C4H8O2":[

        {
            "nombre":"Acetato de etilo",
            "tipo":"Éster",
            "uso":"Solvente",
            "riesgo":"Inflamable",
            "smiles":"CCOC(=O)C"
        }

    ],

    "C2H5NH2":[

        {
            "nombre":"Etilamina",
            "tipo":"Amina",
            "uso":"Farmacéutica",
            "riesgo":"Corrosivo",
            "smiles":"CCN"
        }

    ],

    "C6H6":[

        {
            "nombre":"Benceno",
            "tipo":"Aromático",
            "uso":"Industria química",
            "riesgo":"Cancerígeno",
            "smiles":"c1ccccc1"
        }

    ]

}

# =====================================================
# FUNCION PROPIEDADES
# =====================================================

def obtener_propiedades(smiles):

    if not RDKIT_OK:
        return None

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return None

    return{

        "masa": round(Descriptors.MolWt(mol),2),

        "logp": round(Crippen.MolLogP(mol),2),

        "atomos": mol.GetNumAtoms(),

        "enlaces": mol.GetNumBonds(),

        "formula": rdMolDescriptors.CalcMolFormula(mol),

        "hdonors": Lipinski.NumHDonors(mol),

        "hacceptors": Lipinski.NumHAcceptors(mol),

        "imagen": Draw.MolToImage(mol,size=(350,350))
    }

# =====================================================
# IA
# =====================================================

def analizar_con_ia(compuesto):

    riesgo = compuesto["riesgo"].lower()

    if "tóxico" in riesgo or "cancer" in riesgo:

        clasificacion = "🔴 Riesgoso"

    elif "inflamable" in riesgo:

        clasificacion = "🟡 Precaución"

    else:

        clasificacion = "🟢 Seguro"

    return f"""

🤖 ANÁLISIS IA

Clasificación:
{clasificacion}

Tipo:
{compuesto['tipo']}

Uso:
{compuesto['uso']}

Riesgo:
{compuesto['riesgo']}
"""

# =====================================================
# PORTADA
# =====================================================

st.markdown("""

<div class="hero">

<div class="big-title">
🧪 IsoChem AI 13.0
</div>

<div class="subtitle">
Plataforma Inteligente de Química Computacional
</div>

<br>

🚀 IA • Isomería • Visualización molecular • Química computacional

</div>

""", unsafe_allow_html=True)

# =====================================================
# METRICAS
# =====================================================

col1,col2,col3 = st.columns(3)

with col1:
    st.metric("🏆 Puntaje", st.session_state.score)

with col2:
    st.metric("🧠 IA", "Activa")

with col3:
    st.metric("🔬 Sistema", "Online")

# =====================================================
# MENU
# =====================================================

menu = st.sidebar.selectbox(
    "📌 Navegación",
    [
        "🏠 Inicio",
        "🔬 Analizador molecular",
        "🎮 Quiz químico",
        "📊 Comparación molecular",
        "🧑‍🏫 Modo profesor"
    ]
)

# =====================================================
# INICIO
# =====================================================

if menu == "🏠 Inicio":

    st.markdown("""

<div class="card">

# 🚀 Bienvenido a IsoChem AI

### Funciones:

✅ Identificación molecular  
✅ IA química  
✅ Isomería estructural  
✅ Comparación molecular  
✅ Visualización científica  
✅ Quiz académico  

</div>

""", unsafe_allow_html=True)

# =====================================================
# ANALIZADOR
# =====================================================

elif menu == "🔬 Analizador molecular":

    busqueda = st.text_input(
        "Buscar compuesto",
        placeholder="Ejemplo: acetona o C2H6O"
    )

    if busqueda:

        resultados = []

        for formula, compuestos in isomer_db.items():

            for iso in compuestos:

                if (
                    busqueda.lower() in formula.lower()
                    or
                    busqueda.lower() in iso["nombre"].lower()
                    or
                    busqueda.lower() in iso["smiles"].lower()
                ):

                    resultados.append(iso)

        if resultados:

            st.success(f"Resultados encontrados: {len(resultados)}")

            for i, iso in enumerate(resultados,1):

                props = obtener_propiedades(iso["smiles"])

                if props is None:
                    continue

                st.markdown('<div class="card">', unsafe_allow_html=True)

                st.subheader(f"🧪 {iso['nombre']}")

                st.image(props["imagen"], width=350)

                st.write(f"🧬 Fórmula: {props['formula']}")
                st.write(f"⚖ Masa molecular: {props['masa']}")
                st.write(f"🧪 LogP: {props['logp']}")
                st.write(f"🧱 Átomos: {props['atomos']}")
                st.write(f"🔗 Enlaces: {props['enlaces']}")
                st.write(f"💧 Donadores H: {props['hdonors']}")
                st.write(f"🧲 Aceptores H: {props['hacceptors']}")
                st.write(f"🔬 Tipo: {iso['tipo']}")
                st.write(f"🏭 Uso: {iso['uso']}")
                st.write(f"⚠ Riesgo: {iso['riesgo']}")

                st.code(iso["smiles"])

                if st.button(f"🤖 Analizar IA {i}"):

                    st.session_state.analisis[i] = analizar_con_ia(iso)

                    st.session_state.score += 2

                if i in st.session_state.analisis:

                    st.info(st.session_state.analisis[i])

                st.markdown("</div>", unsafe_allow_html=True)

        else:

            st.error("❌ No se encontraron resultados")

# =====================================================
# QUIZ
# =====================================================

elif menu == "🎮 Quiz químico":

    preguntas = [

        {
            "pregunta":"¿Qué es un isómero?",
            "opciones":["","Misma fórmula diferente estructura","Sin relación","Misma estructura"],
            "respuesta":"Misma fórmula diferente estructura"
        },

        {
            "pregunta":"¿Qué grupo contiene OH?",
            "opciones":["","Alcohol","Amina","Cetona"],
            "respuesta":"Alcohol"
        },

        {
            "pregunta":"¿Qué compuesto es aromático?",
            "opciones":["","Benceno","Acetona","Etanol"],
            "respuesta":"Benceno"
        }

    ]

    respuestas = []

    for i,p in enumerate(preguntas):

        r = st.radio(
            p["pregunta"],
            p["opciones"],
            index=0,
            key=i
        )

        respuestas.append(r)

    if st.button("📘 Evaluar"):

        correctas = 0

        for i,p in enumerate(preguntas):

            if respuestas[i] == p["respuesta"]:
                correctas += 1

        st.success(f"✅ Resultado: {correctas}/3")

        st.session_state.score += correctas

# =====================================================
# COMPARACION
# =====================================================

elif menu == "📊 Comparación molecular":

    datos = []

    for formula, compuestos in isomer_db.items():

        for iso in compuestos:

            props = obtener_propiedades(iso["smiles"])

            if props:

                datos.append({

                    "Compuesto":iso["nombre"],
                    "Tipo":iso["tipo"],
                    "Masa":props["masa"],
                    "LogP":props["logp"],
                    "Riesgo":iso["riesgo"]

                })

    df = pd.DataFrame(datos)

    st.dataframe(
        df,
        use_container_width=True
    )

# =====================================================
# PROFESOR
# =====================================================

elif menu == "🧑‍🏫 Modo profesor":

    st.subheader("🧑‍🏫 Panel docente")

    st.write(f"🏆 Puntaje total: {st.session_state.score}")

    if st.session_state.score >= 10:

        st.success("🥇 Nivel experto")

    elif st.session_state.score >= 5:

        st.info("🥈 Nivel intermedio")

    else:

        st.warning("🥉 Nivel básico")

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption("IsoChem AI 13.0 — Plataforma de química computacional")