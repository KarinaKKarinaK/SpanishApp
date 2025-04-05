#Importing teh libraries required
import os 
import openai
import streamlit as st
from streamlit_chat import message

# Setting up the API key
openai.api_key = os.getenv("OPENAI_API_KEY") #Your API key here

#Visuals of the Streamlit app
st.header("Inglés - Español | Traductor")

#Read the text from teh article from a file
user_prompt = st.text_area("Introduzca la palabra o frase a traducir.")
# user_language = st.text_area("The language You want to translate to.")

#Get the scietific text to summarize from teh Streamlit app
#Check if enough words (in the scientific text)

#If enough words --> show "Generate Summary" button to teh user on teh Streamlit app
if st.button("Traducir"):
    # Use OpenAI (API) to generate the summary
    response1 = openai.Completion.create(
        model="text-davinci-003",
        prompt="Translate this into Spanish\n\n"+user_prompt+"\n\n1.",
        temperature=0.3,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Print teh summary generated
    res1 = response1["choices"][0]["text"]
    st.info(res1)
    st.download_button("Descargar Resultado", res1)

