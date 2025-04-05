#Importing teh libraries required
import os 
import openai
import streamlit as st
from streamlit_chat import message

# Setting up the API key
openai.api_key = os.getenv("OPENAI_API_KEY") #Your API key here

#Visuals of the Streamlit app

# KEYWORD FINDER  =======================================================
#Visuals of the Streamlit app
st.header("Buscador De Palabras Clave")

#Read the text from teh article from a file
text = st.text_area("Inserte el texto del que extraer las palabras clave.")
#Get the output sized (what does the user want?)

#Get the scietific text to summarize from teh Streamlit app
#Check if enough words (in the scientific text)

#If enough words --> show "Generate Summary" button to teh user on teh Streamlit app
if st.button("Buscar palabras clave"):
    # Use OpenAI (API) to generate the summary
    response4 = openai.Completion.create(
    model="text-davinci-003",
    prompt="Extract keywords from this text: " + text,
    temperature=0.5,
    max_tokens=60,
    top_p=1.0,
    frequency_penalty=0.8,
    presence_penalty=0.0
)

    # Print teh summary generated
    res4 = response4["choices"][0]["text"]
    st.info(res4)
    st.download_button("Descargar Resultado", res4)