# app.py
import random
import streamlit as st

st.set_page_config(page_title="InspireFlowApp", page_icon="✨", layout="centered")

QUOTES = [
    "Believe you can and you're halfway there.",
    "Keep going. Everything you need will come at the perfect time.",
    "Small steps every day lead to big results.",
    "You are stronger than you think.",
    "Progress, not perfection."
]

st.title("✨ InspireFlowApp")
st.write("กดปุ่มเพื่อรับพลังใจหนึ่งประโยค 💪")

if st.button("ให้กำลังใจฉันหน่อย"):
    st.success(random.choice(QUOTES))

# เพิ่มโซนสุ่มอัตโนมัติเล็กน้อย
st.caption("Tip: กดปุ่มด้านบนได้เรื่อย ๆ เพื่อสุ่มคำคมใหม่")
