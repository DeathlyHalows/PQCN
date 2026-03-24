import streamlit as st
import hashlib
import os
import time
from ecdsa import SigningKey, SECP256k1

st.set_page_config(page_title="Quantum Crypto Simulator", layout="centered")

st.title("⚛️ Quantum vs Post-Quantum Crypto Simulator")

# =========================
# INPUT
# =========================
message = st.text_input("Enter Message", "Send 10 coins")
message_bytes = message.encode()

# =========================
# CLASSICAL (ECDSA)
# =========================
st.subheader("🔐 Classical Cryptography (ECDSA)")

if "ecdsa_keys" not in st.session_state:
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.verifying_key
    st.session_state.ecdsa_keys = (sk, vk)

sk, vk = st.session_state.ecdsa_keys

if st.button("Sign with Classical Crypto"):
    signature = sk.sign(message_bytes)
    st.session_state.classical_sig = signature
    st.success("Classical Signature Generated")

if "classical_sig" in st.session_state:
    try:
        valid = vk.verify(st.session_state.classical_sig, message_bytes)
        st.write("Verification:", "✅ Valid" if valid else "❌ Invalid")
        st.write("Signature Size:", len(st.session_state.classical_sig), "bytes")
    except:
        st.write("Verification: ❌ Failed")

# =========================
# POST-QUANTUM (LAMPORT - FIXED)
# =========================
st.subheader("🛡️ Post-Quantum Cryptography (Lamport - One-Time Secure)")

def generate_lamport_keys():
    private_key = [(os.urandom(32), os.urandom(32)) for _ in range(256)]
    public_key = [(hashlib.sha256(x[0]).digest(), hashlib.sha256(x[1]).digest()) for x in private_key]
    return private_key, public_key

def lamport_sign(message, private_key):
    digest = hashlib.sha256(message).digest()
    signature = []
    for i, byte in enumerate(digest):
        for bit in range(8):
            bit_val = (byte >> bit) & 1
            signature.append(private_key[i * 8 + bit][bit_val])
    return signature

def lamport_verify(message, signature, public_key):
    digest = hashlib.sha256(message).digest()
    idx = 0
    for i, byte in enumerate(digest):
        for bit in range(8):
            bit_val = (byte >> bit) & 1
            if hashlib.sha256(signature[idx]).digest() != public_key[i * 8 + bit][bit_val]:
                return False
            idx += 1
    return True

# Generate NEW keys every time (important fix)
if st.button("Sign with Post-Quantum Crypto"):
    priv, pub = generate_lamport_keys()
    signature = lamport_sign(message_bytes, priv)

    st.session_state.pq_sig = signature
    st.session_state.pq_pub = pub

    st.success("Post-Quantum Signature Generated (One-Time Key Used)")

# Verify PQ signature
if "pq_sig" in st.session_state:
    valid = lamport_verify(message_bytes, st.session_state.pq_sig, st.session_state.pq_pub)
    st.write("Verification:", "✅ Valid" if valid else "❌ Invalid")
    st.write("Signature Size:", len(st.session_state.pq_sig), "elements (very large)")

# =========================
# QUANTUM ATTACK SIMULATION
# =========================
st.subheader("⚛️ Quantum Attack Simulation")

if st.button("Simulate Quantum Attack"):
    st.info("Running Shor's Algorithm simulation...")
    time.sleep(2)

    st.error("🔓 Classical Crypto: Vulnerable (Private key can be derived)")
    st.success("🛡️ Post-Quantum Crypto: Secure (Hash-based, no known quantum break)")

# =========================
# COMPARISON
# =========================
st.subheader("📊 Comparison")

st.table({
    "Feature": ["Quantum Resistance", "Key Size", "Speed", "Key Usage"],
    "Classical (ECDSA)": ["❌ No", "Small", "Fast", "Reusable"],
    "Post-Quantum (Lamport)": ["✅ Yes", "Very Large", "Slower", "One-time only"]
})

# =========================
# EXPLANATION
# =========================
st.info("""
Lamport signatures are based only on hash functions.
Unlike classical cryptography, they are not vulnerable to Shor's algorithm.

However, each Lamport key pair must be used only once,
as reuse can leak parts of the private key.
""")
