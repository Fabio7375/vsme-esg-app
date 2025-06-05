import streamlit as st import pandas as pd import io

st.set_page_config(page_title="Template ESG VSME", layout="centered")

st.title("🟢 Compilazione semplificata - Bilancio di Sostenibilità VSME")

st.markdown(""" Compila i campi sottostanti per generare automaticamente un report ESG semplificato, adatto per micro e piccole imprese secondo il modello VSME (EFRAG). """)

1. Informazioni Generali

st.header("1. Informazioni Generali") azienda = st.text_input("Nome dell’impresa") settore = st.text_input("Settore di attività") paese = st.text_input("Paese") referente = st.text_input("Nome del referente") email = st.text_input("Email del referente") dipendenti = st.number_input("Numero di dipendenti", min_value=0, step=1) fatturato = st.number_input("Fatturato (€)", min_value=0.0, step=1000.0) attivo = st.number_input("Totale attivo (€)", min_value=0.0, step=1000.0)

2. Strategia ESG

tab2 = st.expander("2. Strategia e Governance ESG") with tab2: strategia = st.text_area("L’impresa ha una strategia ESG?") rischi = st.text_area("Principali rischi ESG identificati") obiettivi = st.text_area("Obiettivi ESG definiti") governance = st.text_area("Struttura di governance ESG") stakeholder = st.text_area("Coinvolgimento stakeholder su temi ESG")

3. Ambiente

ambiente = st.expander("3. Ambiente") with ambiente: energia = st.number_input("Consumo energetico (kWh)", min_value=0.0) energia_rinnovabile = st.slider("Quota energia rinnovabile (%)", 0, 100, 0) emissioni = st.number_input("Emissioni gas serra (Scope 1 e 2, tCO₂eq)", min_value=0.0) acqua = st.number_input("Consumo idrico (m³)", min_value=0.0) rifiuti = st.number_input("Rifiuti prodotti (kg)", min_value=0.0) riciclo = st.slider("% Rifiuti riciclati", 0, 100, 0)

4. Sociale

sociale = st.expander("4. Sociale") with sociale: donne = st.slider("% Donne nella forza lavoro", 0, 100, 0) donne_mgmt = st.slider("% Donne in posizioni manageriali", 0, 100, 0) formazione = st.number_input("Ore formazione per dipendente", min_value=0.0) infortuni = st.number_input("Infortuni sul lavoro", min_value=0, step=1) turnover = st.slider("Tasso di turnover (%)", 0, 100, 0) diversity = st.text_area("Politica per diversità e inclusione")

5. Governance

governance_section = st.expander("5. Governance") with governance_section: consiglio = st.radio("Esiste un consiglio di amministrazione?", ["Sì", "No"]) codice_etico = st.radio("Codice etico presente?", ["Sì", "No"]) anticorruzione = st.radio("Politica anticorruzione presente?", ["Sì", "No"]) whistle = st.radio("Sistema di segnalazione anonima presente?", ["Sì", "No"])

6. Analisi e Dashboard

st.header("📊 Analisi ESG sintetica")

col1, col2 = st.columns(2) with col1: st.metric("% Energia rinnovabile", f"{energia_rinnovabile}%") st.metric("% Donne in azienda", f"{donne}%") with col2: st.metric("% Rifiuti riciclati", f"{riciclo}%") st.metric("Ore di formazione", f"{formazione:.1f}")

Commenti dinamici

st.subheader("📝 Commento automatico") commenti = [] if energia_rinnovabile > 50: commenti.append("L'azienda mostra un buon impegno nella transizione energetica.") else: commenti.append("La quota di energia rinnovabile può essere migliorata.") if donne < 30: commenti.append("La rappresentanza femminile appare bassa: valutare politiche inclusive.") if formazione > 8: commenti.append("Buon livello di formazione interna al personale.") if infortuni > 3: commenti.append("Attenzione: numero di infortuni elevato rispetto alla media." ) if riciclo > 60: commenti.append("Ottimo tasso di riciclo dei rifiuti.")

for c in commenti: st.markdown(f"- {c}")

7. Esportazione Excel

if st.button("📥 Esporta Report in Excel"): data = { "Nome Impresa": [azienda], "Settore": [settore], "Paese": [paese], "Referente": [referente], "Email": [email], "Dipendenti": [dipendenti], "Fatturato €": [fatturato], "Totale Attivo €": [attivo], "Strategia ESG": [strategia], "Rischi ESG": [rischi], "Obiettivi ESG": [obiettivi], "Governance ESG": [governance], "Coinvolgimento Stakeholder": [stakeholder], "Energia kWh": [energia], "Energia Rinnovabile %": [energia_rinnovabile], "Emissioni tCO2eq": [emissioni], "Consumo Idrico": [acqua], "Rifiuti kg": [rifiuti], "Riciclo %": [riciclo], "% Donne": [donne], "% Donne Mgmt": [donne_mgmt], "Formazione Ore": [formazione], "Infortuni": [infortuni], "Turnover %": [turnover], "Diversity": [diversity], "Consiglio Amm.": [consiglio], "Codice Etico": [codice_etico], "Anticorruzione": [anticorruzione], "Whistleblowing": [whistle] } df = pd.DataFrame(data) output = io.BytesIO() with pd.ExcelWriter(output, engine='xlsxwriter') as writer: df.to_excel(writer, index=False, sheet_name='Report ESG VSME') output.seek(0)

st.download_button(
    label="📄 Scarica il file Excel",
    data=output,
    file_name="report_esg_vsme.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

