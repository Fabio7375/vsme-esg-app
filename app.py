import streamlit as st
import pandas as pd
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import date

st.set_page_config(page_title="Template ESG VSME", layout="centered")

st.title("🟢 Compilazione semplificata - Bilancio di Sostenibilità VSME")

st.markdown(""" Compila i campi sottostanti per generare automaticamente un report ESG semplificato, adatto per micro e piccole imprese secondo il modello VSME (EFRAG). """)

--- SEZIONI NARRATIVE (da documento ODCEC) ---

st.header("📘 Sezioni narrative VSME")

modello_business = st.text_area("1. Modello di business 🟥 Obbligatorio", help="Descrivi in modo sintetico il core business dell'impresa, i prodotti o servizi principali, il mercato di riferimento") catena_valore = st.text_area("2. Catena del valore 🟧 Opzionale", help="Indica gli attori principali a monte e a valle (es. fornitori, clienti, distributori)") strategia_esg = st.text_area("3. Strategia ESG 🟥 Obbligatorio", help="Quali sono le priorità e gli obiettivi dell'impresa in ambito ambientale, sociale e di governance?") impatti_rischi = st.text_area("4. Impatti, rischi e opportunità 🟨 Narrativo guidato", help="Descrivi i principali rischi ESG legati all’attività e le eventuali opportunità") politiche = st.text_area("5. Politiche e obiettivi ESG 🟧 Opzionale", help="Elenca politiche attuate o in fase di implementazione e gli obiettivi dichiarati")

--- DATI QUANTITATIVI ESG ---

st.header("📊 Indicatori ESG")

azienda = st.text_input("Nome dell’impresa") settore = st.text_input("Settore di attività") paese = st.text_input("Paese") dipendenti = st.number_input("Numero di dipendenti", min_value=0, step=1) fatturato = st.number_input("Fatturato (€)", min_value=0.0, step=1000.0)

energia_rinnovabile = st.slider("Quota energia rinnovabile (%)", 0, 100, 0) riciclo = st.slider("% Rifiuti riciclati", 0, 100, 0) donne = st.slider("% Donne nella forza lavoro", 0, 100, 0) formazione = st.number_input("Ore formazione per dipendente", min_value=0.0) infortuni = st.number_input("Infortuni sul lavoro", min_value=0, step=1)

--- COMMENTO DEL PROFESSIONISTA ---

st.header("🧾 Commento del professionista") commento_professionista = st.text_area("Spazio riservato al commercialista o revisore", help="Sintesi delle osservazioni professionali a conclusione del bilancio ESG")

--- WARNING E VERIFICHE COERENZA ---

if energia_rinnovabile == 0: st.warning("⚠️ Nessuna quota di energia rinnovabile indicata: verifica se è corretto.") if donne == 0: st.warning("⚠️ Nessuna presenza femminile segnalata: verifica la correttezza del dato.") if formazione < 2: st.info("ℹ️ Ore di formazione molto basse: considera se si tratta di una media reale o assente.") if not modello_business or not strategia_esg: st.error("❌ Compila almeno le sezioni obbligatorie: Modello di business e Strategia ESG.")

--- CHECKLIST FINALE ---

st.header("✅ Checklist di completamento") checklist = [ modello_business != "", strategia_esg != "", azienda != "", settore != "" ] if all(checklist): st.success("Tutti i requisiti minimi risultano compilati. Puoi generare il report.") else: st.warning("Alcuni campi fondamentali non sono compilati: controlla le sezioni obbligatorie.")

--- COMMENTO AUTOMATICO ---

st.subheader("📝 Commento sintetico automatico") commenti = [] if energia_rinnovabile > 50: commenti.append("L'azienda mostra un buon impegno nella transizione energetica.") else: commenti.append("La quota di energia rinnovabile può essere migliorata.") if donne < 30: commenti.append("La rappresentanza femminile appare bassa: valutare politiche inclusive.") if formazione > 8: commenti.append("Buon livello di formazione interna al personale.") if infortuni > 3: commenti.append("Attenzione: numero di infortuni elevato rispetto alla media.") if riciclo > 60: commenti.append("Ottimo tasso di riciclo dei rifiuti.") for c in commenti: st.markdown(f"- {c}")

--- EXPORT EXCEL ---

if st.button("📥 Esporta Report in Excel"): data = { "Nome Impresa": [azienda], "Settore": [settore], "Paese": [paese], "Dipendenti": [dipendenti], "Fatturato": [fatturato], "Energia Rinnovabile %": [energia_rinnovabile], "Riciclo %": [riciclo], "% Donne": [donne], "Formazione Ore": [formazione], "Infortuni": [infortuni], "Modello di business": [modello_business], "Strategia ESG": [strategia_esg], "Catena del valore": [catena_valore], "Impatti e rischi": [impatti_rischi], "Politiche e obiettivi": [politiche], "Commento professionista": [commento_professionista] } df = pd.DataFrame(data) output = io.BytesIO() with pd.ExcelWriter(output, engine='xlsxwriter') as writer: df.to_excel(writer, index=False, sheet_name='ESG Report') output.seek(0) st.download_button("📄 Scarica il file Excel", output, file_name="report_esg_vsme.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

--- EXPORT PDF ---

if st.button("📄 Genera PDF del Report"): buffer = io.BytesIO() pdf = canvas.Canvas(buffer, pagesize=A4) pdf.setFont("Helvetica", 11) pdf.drawString(30, 800, f"Bilancio ESG VSME - {azienda}") pdf.drawString(30, 785, f"Data: {date.today().isoformat()}") pdf.drawString(30, 765, f"Settore: {settore} | Paese: {paese}") pdf.drawString(30, 745, f"Dipendenti: {dipendenti} | Fatturato: €{fatturato:.2f}") pdf.drawString(30, 725, f"Energia rinnovabile: {energia_rinnovabile}% | Riciclo: {riciclo}%") pdf.drawString(30, 710, f"Donne: {donne}% | Formazione: {formazione}h | Infortuni: {infortuni}") pdf.drawString(30, 690, "Commenti sintetici:") y = 675 for c in commenti: pdf.drawString(40, y, f"- {c}") y -= 15 if commento_professionista: pdf.drawString(30, y-15, "Commento del professionista:") pdf.drawString(40, y-30, commento_professionista[:120]) pdf.save() buffer.seek(0) st.download_button("📄 Scarica il PDF", buffer, file_name="report_esg_vsme.pdf", mime="application/pdf")

