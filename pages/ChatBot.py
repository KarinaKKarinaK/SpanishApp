#Idea: all in one OpenAI (chatbot, article summarizer, topic generator)
#Idea: for Spanish specifically: discussion topic, vocabulary, translator, chatbot in Spanish
# import sys
# print(sys.executable)

import os
import openai
import streamlit as st
from streamlit_chat import message

openai.api_key = os.getenv("OPENAI_API_KEY") #Your API key here

def generate_response(prompt):
    completions = openai.Completion.create( #Use of object oriented programming (using the openai library object 'Completion')
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 1024,
        n = 1,
        stop = None,
        temperature = 0.5
    )

    message = completions.choices[0].text
    return message

st.title("ChatBot")

#Storing teh chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("You: ", "Hola, estoy un estudiante de Espanol.", key = "input") #Turn to Spanish later
    return input_text

user_input = get_text()

if user_input:
    output = generate_response(user_input)
    #store the output in the session
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')

