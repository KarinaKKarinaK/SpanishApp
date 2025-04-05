import streamlit as st
from bokeh.models.widgets import Panel, Tabs
from bokeh.models.widgets import Button
from bokeh.models.widgets import Panel
from bokeh.models.widgets import Tabs
from bokeh.models import CustomJS

from streamlit_bokeh_events import streamlit_bokeh_events
import os
from gtts import gTTS
from io import BytesIO
import openai

# openai.api_key = '{Your API Key}'
openai.api_key = os.getenv("OPENAI_API_KEY") #Your API key here

# Check if 'prompts' is not already in session_state, if not initialize it
if 'prompts' not in st.session_state:
    st.session_state['prompts'] = [{"role": "system", "content": "You are a helpful assistant and Spanish teacher who encourages students to practice their Spanish. Answer as concisely as possible with a little humor expression."}]

# Function to generate response using OpenAI ChatCompletion
def generate_response(prompt):

    st.session_state['prompts'].append({"role": "user", "content":prompt})
    completion=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = st.session_state['prompts']
    )
    
    message=completion.choices[0].message.content
    return message

# Initialize BytesIO object for audio output
sound = BytesIO()

# Create a container using streamlit's container component
placeholder = st.container()

# Set the title for the application
placeholder.title("Bot de chat de voz")

# Create a button for speech-to-text functionality
stt_button = Button(label='HABLAR', button_type='success', margin = (5, 5, 5, 5), width=200)

# Add JavaScript event handling for the button click event
stt_button.js_on_event("button_click", CustomJS(code="""
    var value = "";
    var rand = 0;
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'es';

    document.dispatchEvent(new CustomEvent("GET_ONREC", {detail: 'start'}));
    
    recognition.onspeechstart = function () {
        document.dispatchEvent(new CustomEvent("GET_ONREC", {detail: 'running'}));
    }
    recognition.onsoundend = function () {
        document.dispatchEvent(new CustomEvent("GET_ONREC", {detail: 'stop'}));
    }
    recognition.onresult = function (e) {
        var value2 = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
                rand = Math.random();
                
            } else {
                value2 += e.results[i][0].transcript;
            }
        }
        document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: {t:value, s:rand}}));
        document.dispatchEvent(new CustomEvent("GET_INTRM", {detail: value2}));

    }
    recognition.onerror = function(e) {
        document.dispatchEvent(new CustomEvent("GET_ONREC", {detail: 'stop'}));
    }
    recognition.start();
    """))

# Add the speech-to-text button to the streamlit_bokeh_events component for event handling
result = streamlit_bokeh_events(
    bokeh_plot = stt_button,
    events="GET_TEXT,GET_ONREC,GET_INTRM",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

tr = st.empty()

# Check if 'input' is not already in session_state, if not initialize it
if 'input' not in st.session_state:
    st.session_state['input'] = dict(text='', session=0)

# Display a text area for user input, using the value from session_state['input']['text']
tr.text_area("**Tu aportación**", value=st.session_state['input']['text'])

# Check if there is a result from the event handling
if result:
    # Check if "GET_TEXT" event is present in the result
    if "GET_TEXT" in result:
        # Check if the received text and session ID are different from the ones stored in session_state
        if result.get("GET_TEXT")["t"] != '' and result.get("GET_TEXT")["s"] != st.session_state['input']['session']:
            # Update the stored text and session ID with the received values
            st.session_state['input']['text'] = result.get("GET_TEXT")["t"]
            # Update the text area with the updated input text
            tr.text_area("**Tu aportación**", value=st.session_state['input']['text'])
            st.session_state['input']['session'] = result.get("GET_TEXT")["s"]

    # Check if "GET_INTRM" event is present in the result
    if "GET_INTRM" in result:
        # Check if the received intermediate text is not empty
        if result.get("GET_INTRM") != '':
            # Append the intermediate text to the stored input text and update the text area
            tr.text_area("**Tu aportación**", value=st.session_state['input']['text']+' '+result.get("GET_INTRM"))

    # Check if "GET_ONREC" event is present in the result
    if "GET_ONREC" in result:
        # Check the value of the event to perform corresponding actions
        if result.get("GET_ONREC") == 'start':
            placeholder.text("Iniciado")
            st.session_state['input']['text'] = ''  # Clear the stored input text
        elif result.get("GET_ONREC") == 'running':
            placeholder.text("Ejecutando...")
        elif result.get("GET_ONREC") == 'stop':
            placeholder.text("Detenido")
            if st.session_state['input']['text'] != '':
                input = st.session_state['input']['text']
                output = generate_response(input)
                st.write("**ChatBot:**")
                st.write(output)
                st.session_state['input']['text'] = ''  # Clear the stored input text

                # Generate speech audio from the chatbot response and play it
                tts = gTTS(output, lang='es', tld='com')
                tts.write_to_fp(sound)
                st.audio(sound)

                # Append user and assistant messages to the 'prompts' list in session_state
                st.session_state['prompts'].append({"role": "user", "content": input})
                st.session_state['prompts'].append({"role": "assistant", "content": output})
