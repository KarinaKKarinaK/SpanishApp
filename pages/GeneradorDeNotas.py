#Importing teh libraries required
import os 
import openai
import streamlit as st
from streamlit_chat import message

# Setting up the API key
openai.api_key =  os.getenv("OPENAI_API_KEY") #Your API key here

# NOTE_GENERATOR =========================================================
#Visuals of the Streamlit app
st.header("Generador De Notas ")

#Read the text from teh article from a file
user_prompt1 = st.text_area("Introduce el tema sobre el que quieres notas.")

#Get the scietific text to summarize from teh Streamlit app
#Check if enough words (in the scientific text)

#If enough words --> show "Generate Summary" button to teh user on teh Streamlit app
if st.button("Generar notas"):
    # Use OpenAI (API) to generate the summary
    response3 = openai.Completion.create(
        model="text-davinci-003",
        prompt=user_prompt1 + " as key points",
        temperature=0.3,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Print teh summary generated
    res3 = response3["choices"][0]["text"]
    st.info(res3)
    st.download_button("Descargar Resultado", res3)



