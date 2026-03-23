import streamlit as st
import hashlib
import os
import time
from ecdsa import SigningKey, SECP256k1

st.set_page_config(page_title = "Quantum Crypto SImulator", layout = "centered")
st.title("Quantum vs Post-Quantum Crypto Simulator")

message = st.text_input("Enter message", "Send 10 coins")
message_bytes = message.encode()

st.subheader("Classical Cryptography (ECDSA)")

if "ecdsa_keys" not in st.session_state:
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.verifying_key
    st.session_state.ecdsa_keys = (sk,vk)

sk,vk = st.session_state.ecdsa_keys

if st.button("Sign with Classical Crypto"):
    signature = sk.sign(message_bytes)
    st.session_state.classical_sig = signature
    st.success("Signature generated")

if "classical_sig" in st.session_state:
    try:
        valid = vk.verify(st.session.classical_sig,message_bytes)
        st.write("Verfication: ", "Valid" if valid else "Invalid")
    except:
        st.write("Verification: Failed")

st.subheader("Post-Quantum Cryptography (Lamport Signatures)")

def generate_lamport_keys():
    private_key = [(os.urandom(32),os.urandom(32)) for _ in range(256)]
    public_key = [(hashlib.sha256(x[0]).digest(),hashlib.sha256(x[1]).digest()) for x in private_key]
    return private_key, public_key

def lamport_sign(message, private_key):
    digest = hashlib.sha256(message).digest()
    signature = []
    for i, byte in enumerate(digest):
        for bit in range(8):
            bit_val = (byte >> bit) & 1
            signature.append(private_key[i*8 + bit][bit_val])
    return signature

def lamport_verify(message, signature, public_key):
    digest = hashlib.sha256(message).digest()
    idx = 0
    for i, byte in enumerate(digest):
        for bit in range(8):
            bit_val= (byte >> bit) & 1
            if hashlib.sha256(signature[idx]).digest() != public_key[i*8+bit][bit_val]:
                return False
            idx += 1
    return True

if "lamport_keys" not in st.session_state:
    priv, pub = generate_lamport_keys()
    st.session_state.lamport_keys = (priv, pub)

priv, pub = st.session_state.lamport_keys

if st.button("Sign with Post-Quantum Crypto"):
    signature = lamport_sign(message_bytes,priv)
    st.session_state.pq_sig = signature
    st.success("Post-Quantum Signature Generated")

if "pq_sig" in st.session_state:
    valid = lamport_verify(message_bytes, st.session_state.pq_sig, pub)
    st.write("Verification:", "Valid" if valid else "Invalid")

st.subheader("Signature Size Comparison")

if "classical_sig" in st.session_state:
    st.write("Classical Signature Size:", len(st.session_state.classical_sig), "bytes")

if "pq_sig" in st.session_state:
    st.write("Post-Quantum Signature Size:", len(st.session_state.pq_sig), "elements")


st.subheader("Quantum Attack Simulation")

if st.button("Simualate Quantum Attack"):
    st.info("Running Shor's Algorithm Simulation..")
    time.sleep(2)

    st.write("Classical Crypto : Vulerable (private key can be derived)")
    st.write("Post-Quantum Crypto: Secure (No efficient quantum attack known)")

st.subheader("Comparison")

st.table({
    "Feature":["Quantum Resistance", "Key Size", "Speed"],
    "Classical (ECDSA)" : ["No", "Small", "Fast"],
    "Post-Quantum (Lamport)" : ["Yes","Large","Slower"]
})

st.caption("Note: Quantum Attack s theoreically based on Shor's Algorithm, not executed in this demo")

st.info("Lamport signatures are one-time use, so in a real application you would need to generate new keys for each message. This demo is simplified for educational purposes.")
st.info("In practice, more efficient post-quantum schemes like CRYSTALS-Dilithium or Falcon would be used instead of Lamport signatures.")
st.info("This demo is for educational purposes and does not implement actual quantum algorithms or attacks, but simulates the concepts.")
st.info("In a real-world scenario, the security of post-quantum schemes is based on hard mathematical problems that are believed to be resistant to quantum attacks, but this is still an active area of research.")
st.info("Lamport signatures are based only on hash functions, which are believed to be quantum-resistant, while ECDSA relies on the hardness of the elliptic curve discrete logarithm problem, which can be efficiently solved by a quantum computer using Shor's algorithm.")