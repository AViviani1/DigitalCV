from pathlib import Path

import streamlit as st
from PIL import Image


# --- Path Settings ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir/"styles"/"main.css"
resume_file = current_dir/"assets"/"CV_Alessandro_Viviani_2024.pdf"
profile_pic = current_dir/"assets"/"profile-pic-res.png"

# --- General Settings ---
PAGE_TITLE = "Digital CV | Alessandro Viviani"
PAGE_ICON = "🙋‍♂️"
NAME = "Alessandro Viviani"
DESCRIPTION = """
Artificial Intelligence Expert, seeking opportunities to contribute to cutting-edge AI projects. Let's innovate!
"""

SOCIAL_MEDIA = {
    "📫 a.viviani246@gmail.com": "mailto:a.viviani246@gmail.com",
    "LinkedIn": "https://www.linkedin.com/in/alessandro-viviani-cv",
    "GitHub": "https://github.com/AViviani1",
}


st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# --- LOAD CSS, PDF & PROFIL PIC ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

@st.cache_data 
def load_resume(resume_file):
    with open(resume_file, "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    return PDFbyte

@st.cache_data 
def load_profile_pic(profile_pic):
    profile_pic = Image.open(profile_pic)
    return profile_pic

# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small")
with col1:
    st.image(load_profile_pic(profile_pic))

with col2:
    st.title(NAME)
    st.write(DESCRIPTION)
    st.download_button(
        label=" 📄 Download Curriculum",
        data=load_resume(resume_file),
        file_name=resume_file.name,
        mime="application/octet-stream",
    )
    

# --- SOCIAL LINKS ---
col1, col2, col3 = st.columns([2,3,1], gap="small")

with col1:
    st.write("[LinkedIn](https://www.linkedin.com/in/alessandro-viviani-cv)")

with col2:
    st.markdown('<a href="mailto:a.viviani246@gmail.com" target="_blank" rel="noopener noreferrer">a.viviani246@gmail.com</a>', unsafe_allow_html=True)

with col3:
    st.write("[GitHub](https://github.com/AViviani1)")

st.write(
    """
    🎉 NOTE: In the side-bar I made for you some simple and fun AI applications to play with!
    """)
st.write("---")


# --- EXPERIENCE & QUALIFICATIONS ---
st.subheader("Experience & Qualifications")
st.write(
    """
- ✔️ Master Degree in Artificial Intelligence in Bicocca University (Milan)
- ✔️ Bachelor Degree in Informatics in Bicocca University (Milan)
- ✔️ Strong hands on experience in Python
- ✔️ Cybersecurity course certification by ONstairs academy
"""
)

# --- SKILLS ---
st.write('\n')
st.subheader("Skills")
st.write(
    """
- 🤖 AI: Computer Vision, NLP, Recommender Systems, Domotics
- 👩‍💻 Programming: Python, Java, C, C++, Matlab
- 🗄️ Databases: SQL, MongoDB, Neo4j, Hadoop, Spark
- 😄 Excellent team-player, responsible and reliable
"""
)

# --- WORK HISTORY ---
st.write('\n')
st.subheader("Work History")
st.write("---")

# --- JOB 1
st.write("🚧", "**Curricular Stage at Bicocca University** - (May - September 2022)")
st.write(
    """
- Worked on Neanias, a European open science project. 
- Developed a Streamlit web application for image dataset analysis through ML techniques. 
"""
)

# --- JOB 2
st.write('\n')
st.write("🚧", "**High School Work Experience at Sumitomo** - (June 2017)")
st.write(
    """
- Sumitomo is a multinational company that sells chemical and agricultural products. 
- Managed documents and studied marketing strategies.
"""
)

# --- JOB 3
st.write('\n')
st.write("🚧", "**Volunteering at Telethon** - (April 2017)")
st.write(
    """
- Collection and promotion of donations for research against rare diseases.
"""
)
