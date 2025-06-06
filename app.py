import streamlit as st
import pandas as pd
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import date

st.set_page_config(page_title="Template ESG VSME", layout="centered")

st.title("🟢 Bilancio di Sostenibilità VSME")

st.markdown("""
Applicazione ispirata al VSME Digital Template (EFRAG) e alla guida ODCEC 2025 per la rendicontazione semplificata ESG delle microimprese.
""")

# --- ANAGRAFICA IMPRESA ---
st.header("1️⃣ Anagrafica impresa")
azienda = st.text_input("Nome dell’impresa 🟥")
settore = st.text_input("Settore di attività 🟥")
paese = st.text_input("Paese 🟥")
referente = st.text_input("Referente")
email = st.text_input("Email")
dipendenti = st.number_input("Numero di dipendenti", min_value=0, step=1)
fatturato = st.number_input("Fatturato (€)", min_value=0.0, step=1000.0)
attivo = st.number_input("Totale attivo (€)", min_value=0.0, step=1000.0)

# --- NARRATIVI ESG ---
st.header("2️⃣ Informazioni narrative")
modello_business = st.text_area("Modello di business 🟥")
catena_valore = st.text_area("Catena del valore")
strategia_esg = st.text_area("Strategia ESG 🟥")
impatti_rischi = st.text_area("Impatti, rischi e opportunità 🟥")
obiettivi = st.text_area("Obiettivi ESG")
governance = st.text_area("Struttura di governance ESG")
stakeholder = st.text_area("Coinvolgimento stakeholder")

# --- AMBIENTE ---
st.header("3️⃣ Ambiente")
energia = st.number_input("Consumo energetico (kWh)", min_value=0.0)
energia_rinnovabile = st.slider("Quota energia rinnovabile (%)", 0, 100, 0)
emissioni = st.number_input("Emissioni gas serra (tCO₂eq)", min_value=0.0)
acqua = st.number_input("Consumo idrico (m³)", min_value=0.0)
rifiuti = st.number_input("Rifiuti prodotti (kg)", min_value=0.0)
riciclo = st.slider("Percentuale rifiuti riciclati (%)", 0, 100, 0)

# --- SOCIALE ---
st.header("4️⃣ Sociale")
donne = st.slider("Percentuale donne nella forza lavoro", 0, 100, 0)
donne_mgmt = st.slider("Percentuale donne in ruoli manageriali", 0, 100, 0)
formazione = st.number_input("Ore formazione medie per dipendente", min_value=0.0)
infortuni = st.number_input("Numero di infortuni", min_value=0)
turnover = st.slider("Tasso di turnover (%)", 0, 100, 0)
diversity = st.text_area("Politica per diversità e inclusione")

# --- GOVERNANCE ---
st.header("5️⃣ Governance")
consiglio = st.radio("Consiglio di amministrazione presente?", ["Sì", "No"])
codice_etico = st.radio("Codice etico presente?", ["Sì", "No"])
anticorruzione = st.radio("Politica anticorruzione?", ["Sì", "No"])
whistle = st.radio("Sistema whistleblowing?", ["Sì", "No"])

# --- COMMENTO DEL PROFESSIONISTA ---
st.header("6️⃣ Commento del professionista")
commento_professionista = st.text_area("Nota a cura del revisore/commercialista")

# --- CHECKLIST FINALE ---
st.header("✅ Checklist automatica")
if energia_rinnovabile == 0:
    st.warning("⚠️ Energia rinnovabile non presente: verifica la correttezza.")
if donne == 0:
    st.warning("⚠️ Nessuna presenza femminile: controlla il dato.")
if formazione < 2:
    st.info("ℹ️ Ore di formazione molto basse.")
if not all([azienda, settore, paese, modello_business, strategia_esg, impatti_rischi]):
    st.error("❌ Compila tutti i campi obbligatori (🟥) prima di esportare.")
else:
    st.success("✅ Tutti i campi obbligatori sono compilati. Puoi procedere.")

# --- COMMENTI AUTOMATICI ESG ---
st.subheader("📌 Sintesi automatica ESG")
commenti = []
if energia_rinnovabile > 50:
    commenti.append("Buona quota di energia rinnovabile.")
if riciclo > 60:
    commenti.append("Ottima gestione dei rifiuti.")
if donne < 30:
    commenti.append("Bassa rappresentanza femminile.")
if formazione > 8:
    commenti.append("Formazione interna sopra la media.")
if infortuni > 3:
    commenti.append("Attenzione al tema sicurezza.")
for c in commenti:
    st.markdown(f"- {c}")

# --- EXPORT EXCEL ---
if st.button("📥 Esporta Excel"):
    data = {
        "Impresa": [azienda], "Settore": [settore], "Paese": [paese],
        "Referente": [referente], "Email": [email],
        "Dipendenti": [dipendenti], "Fatturato €": [fatturato], "Attivo €": [attivo],
        "Modello business": [modello_business], "Catena valore": [catena_valore], "Strategia ESG": [strategia_esg],
        "Impatti e rischi": [impatti_rischi], "Obiettivi": [obiettivi], "Governance": [governance],
        "Stakeholder": [stakeholder], "Energia kWh": [energia], "Energia Rinnovabile %": [energia_rinnovabile],
        "Emissioni CO2": [emissioni], "Acqua m³": [acqua], "Rifiuti kg": [rifiuti], "Riciclo %": [riciclo],
        "% Donne": [donne], "% Donne Mgmt": [donne_mgmt], "Formazione h": [formazione],
        "Infortuni": [infortuni], "Turnover %": [turnover], "Diversità": [diversity],
        "Consiglio": [consiglio], "Codice Etico": [codice_etico],
        "Anticorruzione": [anticorruzione], "Whistleblowing": [whistle],
        "Nota Revisore": [commento_professionista]
    }
    df = pd.DataFrame(data)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="ESG VSME")
    buffer.seek(0)
    st.download_button("📄 Scarica Excel", buffer, file_name="bilancio_esg_vsme.xlsx")

# --- EXPORT PDF ---
if st.button("📄 Genera PDF"):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setFont("Helvetica", 11)
    pdf.drawString(30, 800, f"Bilancio ESG VSME - {azienda}")
    pdf.drawString(30, 785, f"Data: {date.today().isoformat()}")
    pdf.drawString(30, 765, f"Settore: {settore} | Paese: {paese} | Dipendenti: {dipendenti}")
    pdf.drawString(30, 745, f"Fatturato: €{fatturato} | Attivo: €{attivo}")
    pdf.drawString(30, 725, f"Energia Rinnovabile: {energia_rinnovabile}% | Riciclo: {riciclo}%")
    pdf.drawString(30, 705, f"Formazione: {formazione}h | Infortuni: {infortuni}")
    pdf.drawString(30, 685, "Commenti automatici:")
    y = 670
    for c in commenti:
        pdf.drawString(40, y, f"- {c}")
        y -= 15
    if commento_professionista:
        pdf.drawString(30, y - 10, "Nota del professionista:")
        pdf.drawString(40, y - 25, commento_professionista[:100])
    pdf.save()
    buffer.seek(0)
    st.download_button("📄 Scarica PDF", buffer, file_name="bilancio_esg_vsme.pdf")
