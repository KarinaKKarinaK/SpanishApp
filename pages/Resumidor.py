#Importing teh libraries required
import os 
import openai
import streamlit as st
from streamlit_chat import message

# Setting up the API key
openai.api_key = os.getenv("OPENAI_API_KEY") #Your API key here

#Visuals of the Streamlit app
st.header("Resumidor")

#Read the text from teh article from a file
article_text = st.text_area("Introduzca el texto para resumir.")
#Get the output sized (what does the user want?)
temp = st.slider("¿Qué tan breve será el resumen?", 0.0, 1.0, 0.5)

#Get the scietific text to summarize from teh Streamlit app
#Check if enough words (in the scientific text)
if len(article_text) > 100:
    #If enough words --> show "Generate Summary" button to teh user on teh Streamlit app
    if st.button("Generar resumen"):
        # Use OpenAI (API) to generate the summary
        response2 = openai.Completion.create(
            engine = "text-davinci-003",
            prompt = "Please summarize this article for me: " + article_text,
            # Set the maximum number of tokens based on the output size selected
            max_tokens = 516,
            temperature = temp
        )

        # Print teh summary generated
        res2 = response2["choices"][0]["text"]
        st.info(res2)
        st.download_button("Descargar Resultado", res2)
else:
    st.warning("Su texto es demasiado corto para resumirlo.")