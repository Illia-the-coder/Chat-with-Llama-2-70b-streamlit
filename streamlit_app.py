import streamlit as st
from gradio_client import Client

# Constants
TITLE = "Llama2 70B Chatbot"
DESCRIPTION = """
This Space demonstrates model [Llama-2-70b-chat-hf](https://huggingface.co/meta-llama/Llama-2-70b-chat-hf) by Meta, 
a Llama 2 model with 70B parameters fine-tuned for chat instructions. 
"""

# Initialize client


with st.sidebar:
    # system_promptSide = st.text_input("Optional system prompt:")
    temperatureSide = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.9, step=0.05)
    max_new_tokensSide = st.slider("Max new tokens", min_value=0.0, max_value=4096.0, value=4096.0, step=64.0)
    # ToppSide = st.slider("Top-p (nucleus sampling)", min_value=0.0, max_value=1.0, value=0.6, step=0.05)
    # RepetitionpenaltySide = st.slider("Repetition penalty", min_value=0.0, max_value=2.0, value=1.2, step=0.05)


    
# Prediction function
def predict(message, system_prompt='', temperature=0.7, max_new_tokens=4096,Topp=0.5,Repetitionpenalty=1.2):
    with st.status("Starting client"):
        client = Client("https://ysharma-explore-llamav2-with-tgi.hf.space/")
        st.write("Requesting client")
    with st.status("Requesting LLama-2"):
        st.write("Requesting API")
        response = client.predict(
    			message,	# str in 'Message' Textbox component
                system_prompt,	# str in 'Optional system prompt' Textbox component
    			temperature,	# int | float (numeric value between 0.0 and 1.0)
    			max_new_tokens,	# int | float (numeric value between 0 and 4096)
    			Topp,	# int | float (numeric value between 0.0 and 1)
    			Repetitionpenalty,	# int | float (numeric value between 1.0 and 2.0)
    			api_name="/chat"
        )
        st.write("Done")
        return response

# Streamlit UI
st.title(TITLE)
st.write(DESCRIPTION)


if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=("🧑‍💻" if message["role"] == 'human' else '🦙')):
        st.markdown(message["content"])
        
# React to user input
if prompt := st.chat_input("Ask LLama-2-70b anything..."):
    # Display user message in chat message container
    st.chat_message("human",avatar = "🧑‍💻").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "human", "content": prompt})

    response = predict(message=prompt)#, temperature= temperatureSide,max_new_tokens=max_new_tokensSide)
    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar='🦙'):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
