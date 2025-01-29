import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import base64

# Configura il client OpenAI
client = OpenAI(api_key='sk-proj_dXEHA8KD9pYpCNM7lS0AOZEv_KcxUScrT8A')  # Sostituisci con la tua API key

# Titolo dell'app
st.title("ChatBot per la Cura dei Capelli 🧴💇‍♀")
st.write("Ciao! Sono qui per aiutarti a capire il problema dei tuoi capelli.")

# Funzione per analizzare la foto
def analyze_photo(image_bytes):
    try:
        # Converti l'immagine in base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        # Invia l'immagine a OpenAI per l'analisi
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # Usa un modello che supporta l'analisi delle immagini
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analizza questa foto dei capelli e descrivi in dettaglio eventuali problemi visibili (es. secchezza, forfora, doppie punte, cute grassa, cute secca, prurito, ecc.)."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"  # Formato corretto
                            },
                        },
                    ],
                }
            ],
            max_tokens=400,
        )

        # Estrai la risposta
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Errore durante l'analisi dell'immagine: {str(e)}"

# Funzione per gestire la chat con OpenAI
def chat_with_openai(messages):
    try:
        # Invia i messaggi a OpenAI
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # Usa un modello di testo
            messages=messages,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Errore durante la chat: {str(e)}"

# Funzione per suggerire prodotti in base al problema
def suggest_products(problem_description):
    # Mappa dei problemi e dei prodotti corrispondenti
    products = {
        "secchezza": {
            "Cute secca": ["Shampoo camomilla", "Lozione aloe", "Maschera AHA"],
            "Capelli secchi con bisogno di nutrimento intenso": ["Maschera girasole"],
            "Crespi, senza forma": ["Impacco passiflora"],
            "Lisci, morbidi e setosi": ["Balsamo zenzero"],
            "Mossi ed elastici": ["Maschera nocciola"],
            "Ricci, idratati e nutriti": ["Maschera avena"],
            "Protezione dagli agenti inquinanti": ["Balsamo zeolite"],
            "Districare facilmente i nodi": ["Balsamo spray", "Balsamo meliloto"],
        },
        "grasso": {
            "Cute grassa": ["Shampoo cisto", "Lozione rosmarino"],
            "Eccesso di sebo": ["Maschera AHA"],
            "Lisci e setosi": ["Balsamo zenzero"],
            "Capelli fini e con volume": ["Balsamo zafferano"],
            "Protezione dagli agenti inquinanti": ["Balsamo zeolite"],
        },
        "forfora": {
            "Forfora secca o grassa": ["Shampoo bardana", "Peeling tea tree", "Lozione tarassaco"],
            "Purificazione e rigenerazione": ["Maschera AHA"],
        },
        "sensibile": {
            "Cute sensibile, prurito o infiammazioni": ["Shampoo fiordaliso", "Lozione avena"],
            "Capelli secchi e nutriti": ["Maschera girasole"],
            "Protezione e districabilità": ["Balsamo spray", "Balsamo meliloto"],
        },
        "fine": {
            "Mancanza di volume": ["Shampoo magnolia", "Maschera AHA"],
            "Capelli voluminosi e leggeri": ["Balsamo zafferano"],
            "Districare senza appesantire": ["Balsamo spray"],
        },
        "liscio": {
            "Ribelli e senza forma": ["Shampoo ninfea", "Maschera AHA"],
            "Lisci, morbidi e setosi": ["Balsamo zenzero"],
        },
        "mosso": {
            "Definizione ed elasticità": ["Shampoo ribes", "Maschera nocciola"],
            "Sostegno e struttura": ["Impacco passiflora"],
        },
        "riccio": {
            "Idratazione e lucentezza": ["Shampoo mela verde", "Maschera avena"],
            "Districare facilmente": ["Balsamo spray", "Balsamo meliloto"],
        },
        "caduta": {
            "Capelli deboli e radi": ["Shampoo ylang ylang", "Lozione foglie d’olivo"],
            "Rinforzare dalla radice": ["Lozione stimolante"],
        },
        "inquinanti": {
            "Purificazione dagli inquinanti": ["Shampoo detox", "Maschera AHA"],
        },
    }

    # Lista per memorizzare i suggerimenti
    suggestions = []

    # Cerca corrispondenze nei problemi rilevati
    for keyword, category in products.items():
        if keyword in problem_description.lower():
            for sub_problem, product_list in category.items():
                # Formatta i prodotti come elenco puntato
                product_list_formatted = "\n".join([f"- {product}" for product in product_list])
                suggestions.append(f"{sub_problem}:\n{product_list_formatted}")

    # Se non vengono trovati suggerimenti specifici, usa un fallback generico
    if not suggestions:
        generic_products = ["Shampoo camomilla", "Balsamo zenzero", "Maschera AHA"]
        generic_list = "\n".join([f"- {product}" for product in generic_products])
        suggestions.append(f"*Problema generico:*\n{generic_list}")

    # Unisci tutti i suggerimenti in un'unica stringa
    return "\n\n".join(suggestions)

# Funzione principale del chatbot
def chat_with_user():
    # Inizializza la conversazione
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Ciao! Posso aiutarti a capire il problema dei tuoi capelli. Puoi descrivermi il problema che stai riscontrando?"}
        ]

    # Mostra la conversazione
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input dell'utente
    if user_input := st.chat_input("Scrivi qui..."):
        # Aggiungi il messaggio dell'utente alla conversazione
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Risposta del chatbot
        with st.chat_message("assistant"):
            if len(st.session_state.messages) == 2:  # Prima domanda
                response = "Mi dispiace sentire che stai riscontrando questo problema. Quale effetto vorresti avere sui tuoi capelli?"
            elif len(st.session_state.messages) == 4:  # Seconda domanda
                response = "Grazie per le informazioni! Per individuare al meglio il problema, sarebbe utile se caricassi una foto dei tuoi capelli."
            else:
                response = chat_with_openai(st.session_state.messages)

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    # Sezione per il caricamento della foto
    if len(st.session_state.messages) >= 5:  # Mostra il caricatore solo dopo la conversazione
        st.subheader("Carica una foto dei tuoi capelli")
        uploaded_file = st.file_uploader("Carica una foto (formato JPG):", type=["jpg", "jpeg"], key="file_uploader")

        if uploaded_file is not None:
            # Mostra l'immagine caricata
            image = Image.open(uploaded_file)
            st.image(image, caption="Foto caricata", use_column_width=True)

            if st.button("Analizza la Foto"):
                # Converti l'immagine in bytes
                image_bytes = uploaded_file.getvalue()

                # Analizza la foto
                photo_analysis = analyze_photo(image_bytes)
                st.success(f"Analisi della foto: {photo_analysis}")

                # Suggerisci prodotti in base all'analisi
                product_suggestion = suggest_products(photo_analysis)
                st.success(f"Suggerimenti di prodotti:\n{product_suggestion}")

                # Confronta l'analisi con la descrizione dell'utente
                user_description = st.session_state.messages[1]["content"]  # Prima risposta dell'utente
                comparison_response = chat_with_openai([
                    {"role": "user", "content": f"L'utente ha descritto il problema come: {user_description}. L'analisi della foto ha rilevato: {photo_analysis}. Confermi o smentisci l'idea dell'utente?"}
                ])
                st.success(f"Confronto con la tua descrizione: {comparison_response}")

# Esegui la funzione principale
chat_with_user()
