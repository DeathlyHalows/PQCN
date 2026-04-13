import streamlit as st
import hashlib
import time
import os
import base64
import matplotlib.pyplot as plt
import numpy as np
import difflib

from ecdsa import SigningKey, SECP256k1
from cryptography.fernet import Fernet

# ================= CONFIG =================
st.set_page_config(
    page_title="Quantum Crypto Simulator",
    layout="wide",
    page_icon="🔐"
)

# ================= CLEAN UI STYLE =================
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f14;
        color: #e6edf3;
        font-family: monospace;
    }

    h1, h2, h3 {
        color: #00ff9f;
    }

    .stButton button {
        background-color: #111;
        color: #00ff9f;
        border: 1px solid #00ff9f;
        border-radius: 6px;
        padding: 0.5rem 1rem;
    }

    .stTextInput input {
        background-color: #111;
        color: #00ff9f;
        border: 1px solid #333;
    }

    .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# ================= UTIL =================
def fake_terminal(text, delay=0.01):
    box = st.empty()
    out = ""
    for c in text:
        out += c
        box.code(out)
        time.sleep(delay)


def sha(msg: str):
    return hashlib.sha256(msg.encode()).hexdigest()


# ================= SIDEBAR NAV =================
st.sidebar.title("🔐 Quantum Crypto Lab")

page = st.sidebar.radio(
    "Navigate",
    [
        "ECDSA Demo",
        "Post-Quantum Crypto",
        "Quantum Attack Simulation",
        "Security Comparison"
    ]
)

st.title("🔐 Quantum vs Classical Cryptography Simulator")


# =========================================================
# 🔴 ECDSA DEMO
# =========================================================
if page == "ECDSA Demo":
    st.header("🔴 Classical Cryptography (ECDSA)")

    if "sk" not in st.session_state:
        sk = SigningKey.generate(curve=SECP256k1)
        vk = sk.verifying_key
        st.session_state.sk = sk
        st.session_state.vk = vk

    message = st.text_input("Message", "Send 10 coins")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sign Message"):
            digest = hashlib.sha256(message.encode()).digest()
            sig = st.session_state.sk.sign(digest)

            st.session_state.sig = sig
            st.session_state.msg = message

            st.success("Message signed")

    with col2:
        if st.button("Verify Signature"):
            if "sig" in st.session_state:
                try:
                    digest = hashlib.sha256(message.encode()).digest()
                    st.session_state.vk.verify(st.session_state.sig, digest)
                    st.success("Valid signature")
                except:
                    st.error("Invalid signature")
            else:
                st.warning("No signature found")

    if "sig" in st.session_state:
        st.subheader("📡 Signature View")
        st.code(st.session_state.sig.hex()[:80] + "...")


# =========================================================
# 🟢 POST QUANTUM CRYPTO
# =========================================================
elif page == "Post-Quantum Crypto":
    st.header("🟢 Post-Quantum Cryptography (Fernet Simulation)")

    if "pqc_key" not in st.session_state:
        st.session_state.pqc_key = Fernet.generate_key()

    message = st.text_input("Message", "Hello Secure Future")

    if st.button("Encrypt Message"):
        f = Fernet(st.session_state.pqc_key)
        enc = f.encrypt(message.encode())
        st.session_state.enc = enc
        st.success("Encrypted successfully")
        st.code(enc.decode())

    if st.button("Decrypt Message"):
        if "enc" in st.session_state:
            f = Fernet(st.session_state.pqc_key)
            dec = f.decrypt(st.session_state.enc).decode()
            st.success("Decrypted message")
            st.code(dec)
        else:
            st.warning("No encrypted message found")

    st.info("Based on lattice-style PQC simulation (Kyber concept)")


# =========================================================
# ⚛️ QUANTUM ATTACK SIMULATION
# =========================================================
elif page == "Quantum Attack Simulation":
    st.header("⚛️ Quantum Attack Simulation")

    if st.button("Run Attack on ECDSA"):
        with st.spinner("Running Shor's Algorithm..."):
            time.sleep(2)

        st.error("ECDSA BROKEN")
        st.write("- Private key can be derived")
        st.write("- Signature forgeable")

    if st.button("Attack Post-Quantum Crypto"):
        with st.spinner("Attempting quantum brute force..."):
            time.sleep(2)

        st.success("ATTACK FAILED")
        st.write("- Based on lattice problems")
        st.write("- No known quantum break")


# =========================================================
# 📊 COMPARISON
# =========================================================
elif page == "Security Comparison":
    st.header("📊 Cryptography Comparison")

    st.table({
        "Feature": [
            "Security Basis",
            "Quantum Resistance",
            "Speed",
            "Future Proof"
        ],
        "ECDSA": [
            "Elliptic Curve Log Problem",
            "❌ Broken (Shor)",
            "⚡ Fast",
            "❌ No"
        ],
        "Post-Quantum": [
            "Lattice / Hash based",
            "✅ Yes",
            "🐢 Slower",
            "✅ Yes"
        ]
    })

    st.markdown("### Summary")
    st.success("""
✔ ECDSA = Fast but vulnerable to quantum attacks  
✔ PQC = Slower but quantum-safe  
✔ Future systems will fully migrate to PQC  
""")
