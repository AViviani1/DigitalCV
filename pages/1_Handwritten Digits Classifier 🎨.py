from pathlib import Path

import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np

import torch
import torch.nn.functional as F


# --- Path Settings ---
project_dir = Path(__file__).parent.parent if "__file__" in locals() else Path.cwd()
css_file = project_dir/"styles"/"main.css"
model_file = project_dir/"assets"/"model_scripted.pt"

# --- General Settings ---
PAGE_TITLE = "Handwritten Digits Classifier"
PAGE_ICON = "🎨"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# --- LOAD CSS AND MODEL ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

@st.cache_resource
def load_model():
    model = torch.jit.load(model_file)
    return model

model = load_model()
model.eval()


# --- Title and Description ---
st.header("Handwritten Digits Classifier 🎨")
st.subheader("Description:")
st.write(
"""
In this page you can draw a number from 0 to 9 and the AI will guess which is it.
""")
st.write("---")


col1, col2 = st.columns(2, gap="small")
with col2:
    st.markdown("***Settings:***")
    # Specify canvas parameters
    stroke_color = st.color_picker("Color: ", value="#FFFFFF")
    stroke_width = st.slider("Width: ", 1, 25, 8)
    
with col1:
    st.write("***Small canvas to draw on:***")
    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color= "#000000",
        update_streamlit=True,
        height=132,
        width=132,
        drawing_mode="freedraw",
        key="canvas",
    )

st.write("---")

# Classify Image
drawing = canvas_result.image_data
if drawing is not None and np.max(drawing[:,:,:3]) != 0:
    
    grayscale_image = np.dot(drawing[..., :3], [0.2989, 0.5870, 0.1140])
    tensor_im = torch.from_numpy(np.float32(grayscale_image))
    # Perform the bicubic downscaling with anti-aliasing
    downscaled_image_tensor = F.interpolate(tensor_im.unsqueeze(0).unsqueeze(0), size=[32,32], mode='bicubic', align_corners=False)
    downscaled_image_tensor = torch.clamp(downscaled_image_tensor, 0, 1) # Normalize
    with torch.no_grad():
        y_pred = model(downscaled_image_tensor)
    y_prob = F.softmax(y_pred, dim = -1)
    y_prob = np.reshape(y_prob.numpy(), 10)
    result = str(y_prob.argmax())

    st.subheader("AI Results:")
    col1, col2, col3 = st.columns([1,1,2], gap="small")
    with col1:
        st.write('\n')
        st.markdown("I think you drew:")
    with col2:
        st.markdown(f"### :red[{result}]")
    st.write("Below are the probabilities for each number according to the AI model:")
    st.bar_chart(y_prob)

st.subheader("Brief explanation of the model:")
st.write(
"""
The model is a CNN with a LeNet-like architecture made with Pytorch and trained on the popular MNIST dataset for 30 epochs.
It performs well considering it is a simple and small model and the input samples have some differences from the train samples
(pre-processing, domain...)
"""
)



