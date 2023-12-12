import streamlit as st
import OpenAI_NoteTaker as nt
import OpenAI_Summarizer as sm
import OpenAI_Transcriber as transcriber
import os

# NOTE: magic-bin currently doesn't provide support for linux, but it supports x32, x64 and OSX

# const
# api_key_local = st.secrets['OPEN_API_KEY']

# functions
def testCallback(file):
  # parse note taker file
  if not file:
    print('Input file first.')
    return
  print('Processing...')
  print(file)

# Page Content
st.title('Note Taker by Lanz Lagman')

file = st.file_uploader("Upload your audio here!")
st.button("Submit", on_click=testCallback(file), use_container_width=True)

# st.write(api_key_local)

# TODO: implement a basic file upload that 

st.divider()
st.write("""
    <div style="display: flex; flex-direction: column; align-items: end;">
      <span>Streamlit build designed by Jay Cruz</span>
      <span>Source code here</span>
    </div>
  """, unsafe_allow_html=True)