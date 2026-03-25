import streamlit as st
import hashlib
import os
import time
import difflib
import matplotlib.pyplot as plt
import numpy as np
from ecdsa import SigningKey, SECP256k1

# ================= HACKER TERMINAL STYLE (ADDED) =================
st.markdown("""
<style>
body, .stApp {
    background-color: #0d0d0d;
    color: #00ff9f;
    font-family: monospace;
}
h1, h2, h3 {
    color: #00ff9f;
}
.stButton button {
    background-color: black;
    color: #00ff9f;
    border: 1px solid #00ff9f;
    font-family: monospace;
}
.stTextInput input {
    background-color: black;
    color: #00ff9f;
}
</style>
""", unsafe_allow_html=True)

# ================= ANIMATION FUNCTION (ADDED) =================
def hacker_print(text, speed=0.01):
    placeholder = st.empty()
    output = ""
    for char in text:
        output += char
        placeholder.markdown(f"```{output}```")
        time.sleep(speed)

# ================= ORIGINAL CODE =================

st.set_page_config(page_title = "Quantum Crypto Simulator", layout = "wide")
st.title("Quantum vs Post-Quantum Crypto Simulator")

message = st.text_input("Enter message", "Send 10 coins")
message_bytes = message.encode()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔐 Classical Crypto",
    "📦 Post-Quantum Crypto", 
    "🔬 Key Derivation Analysis",
    "⚙️ Quantum Attack Simulation",
    "📊 Comparison"
])

# ================= TAB 1 =================
with tab1:
    st.subheader("Classical Cryptography (ECDSA)")

    if "ecdsa_keys" not in st.session_state:
        sk = SigningKey.generate(curve=SECP256k1)
        vk = sk.verifying_key
        st.session_state.ecdsa_keys = (sk, vk)

    sk, vk = st.session_state.ecdsa_keys

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔑 Sign with Classical Crypto"):
            signature = sk.sign(message_bytes)
            st.session_state.classical_sig = signature
            st.success("✓ Signature generated")

    with col2:
        if st.button("✅ Verify Signature"):
            if "classical_sig" in st.session_state:
                try:
                    valid = vk.verify(st.session_state.classical_sig, message_bytes)
                    st.success("✓ Verification: Valid")
                except:
                    st.error("❌ Verification: Failed")
            else:
                st.warning("⚠️ No signature to verify")

    # ===== ADDED VISUAL TERMINAL =====
    if "classical_sig" in st.session_state:
        st.write("---")
        st.subheader("💻 ECDSA Terminal View")

        st.code(f"Message: {message}")
        st.code(f"Signature: {st.session_state.classical_sig.hex()[:60]}...")
        st.code(f"Public Key: {vk.to_string().hex()[:60]}...")

        if st.button("🧠 Run Visual Verification"):
            hacker_print("[+] Loading public key...")
            hacker_print("[+] Hashing message...")
            hacker_print("[+] Verifying signature...")

            try:
                valid = vk.verify(st.session_state.classical_sig, message_bytes)
                if valid:
                    hacker_print("[✔] AUTHENTIC")
                else:
                    hacker_print("[✖] INVALID")
            except:
                hacker_print("[✖] FAILED")
# ===== ENHANCED TAMPERING PROOF =====
    
    if "classical_sig" in st.session_state:
        if st.button("⚠️ Visual Tampering Proof"):

            original = message
            tampered = message + " hacked"

            st.subheader("🔍 Message Difference")

            # Highlight character differences
            diff = list(difflib.ndiff(original, tampered))

            colored_diff = ""
            for d in diff:
                if d.startswith("-"):
                    colored_diff += f":red[{d[2:]}]"
                elif d.startswith("+"):
                    colored_diff += f":green[{d[2:]}]"
                else:
                    colored_diff += d[2:]

            st.markdown(colored_diff)

            st.write("---")

            # Hash comparison
            st.subheader("🧠 Hash Comparison")

            original_hash = hashlib.sha256(original.encode()).hexdigest()
            tampered_hash = hashlib.sha256(tampered.encode()).hexdigest()

            col1, col2 = st.columns(2)

            with col1:
                st.write("Original Hash")
                st.code(original_hash)

            with col2:
                st.write("Tampered Hash")
                st.code(tampered_hash)

            st.error("⚡ Notice: Completely different hashes")

            st.write("---")

            # Verification comparison
            st.subheader("🔐 Signature Verification")

            col1, col2 = st.columns(2)

            with col1:
                st.write("Original Message")
                try:
                    vk.verify(st.session_state.classical_sig, original.encode())
                    st.success("✔ Valid")
                except:
                    st.error("❌ Invalid")

            with col2:
                st.write("Tampered Message")
                try:
                    vk.verify(st.session_state.classical_sig, tampered.encode())
                    st.success("✔ Valid")
                except:
                    st.error("❌ Invalid")

            st.error("🚨 Same signature + different message = verification fails")

# ================= TAB 2 =================
with tab2:
    st.subheader("Post-Quantum Cryptography (Lamport Signatures)")

    def generate_lamport_keys_from_message(message_bytes):
        seed = hashlib.sha256(message_bytes).digest()
        private_key = []
        for i in range(256):
            seed1 = hashlib.sha256(seed + i.to_bytes(4, 'big')).digest()
            seed2 = hashlib.sha256(seed + (i + 256).to_bytes(4, 'big')).digest()
            private_key.append((seed1, seed2))
        public_key = [(hashlib.sha256(x[0]).digest(), hashlib.sha256(x[1]).digest()) for x in private_key]
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
                bit_val = (byte >> bit) & 1
                if hashlib.sha256(signature[idx]).digest() != public_key[i*8+bit][bit_val]:
                    return False
                idx += 1
        return True

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔑 Sign with Post-Quantum Crypto"):
            priv, pub = generate_lamport_keys_from_message(message_bytes)
            signature = lamport_sign(message_bytes, priv)
            st.session_state.pq_sig = signature
            st.session_state.pq_pub = pub
            st.success("✓ Signature generated")

    with col2:
        if st.button("✅ Verify Post-Quantum Signature"):
            if "pq_sig" in st.session_state:
                valid = lamport_verify(message_bytes, st.session_state.pq_sig, st.session_state.pq_pub)
                if valid:
                    st.success("✓ Verification: Valid")
                else:
                    st.error("❌ Verification: Failed")
            else:
                st.warning("⚠️ No signature to verify")

    # ===== ADDED PQ TERMINAL =====
    if "pq_sig" in st.session_state:
        st.write("---")
        st.subheader("💻 Post-Quantum Terminal View")

        st.code(f"Message: {message}")
        st.code(f"Signature fragment: {str(st.session_state.pq_sig[:2])} ...")
        st.code(f"Public Key fragment: {str(st.session_state.pq_pub[:2])} ...")

        if st.button("🧠 Run PQ Visual Verification"):
            hacker_print("[+] Hashing message...")
            hacker_print("[+] Matching signature...")
            hacker_print("[+] Verifying hashes...")

            valid = lamport_verify(
                message_bytes,
                st.session_state.pq_sig,
                st.session_state.pq_pub
            )

            if valid:
                hacker_print("[✔] QUANTUM SAFE")
            else:
                hacker_print("[✖] FAILED")


# ============ TAB 3: KEY DERIVATION ANALYSIS ============
with tab3:
    st.subheader("🔬 Why Private Keys Cannot Be Derived from Public Keys")
    
    # === APPROACH 1: Key Structure Visualization ===
    with st.expander("📐 Approach 1: Key Structure Visualization", expanded=True):
        st.write("### Understanding Key Generation")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Step 1: Generate Random Private Key**")
            sample_private = os.urandom(32)
            st.code(sample_private.hex()[:40] + "...", language="text")
        
        with col2:
            st.write("**Step 2: Apply Hash Function (SHA-256)**")
            st.write("```{sha256(private_key)}```")
        
        with col3:
            st.write("**Step 3: Resulting Public Key**")
            sample_public = hashlib.sha256(sample_private).digest()
            st.code(sample_public.hex()[:40] + "...", language="text")
        
        st.info("""
        **Key Insight:** The public key is derived using a **one-way hash function**:
        - ✅ Forward direction (Private → Public): **Easy & Fast** (milliseconds)
        - ❌ Reverse direction (Public → Private): **Impossible & Slow** (requires 2^256 operations)
        """)
        
        # Display actual key pairs
        st.write("### Live Key Pair Generation")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Sample Private Key:**")
            priv_sample = os.urandom(32)
            st.code(priv_sample.hex(), language="text")
        
        with col2:
            st.write("**Corresponding Public Key:**")
            pub_sample = hashlib.sha256(priv_sample).digest()
            st.code(pub_sample.hex(), language="text")
        
        st.warning("💡 Notice: The public key looks completely random and unrelated to the private key!")
    
    # === APPROACH 2: Reverse Attempt Simulation ===
    with st.expander("🔄 Approach 2: Trying to Reverse the Hash", expanded=False):
        st.write("### Computational Impossibility")
        
        if st.button("🚀 Try to Reverse Public Key → Private Key"):
            st.write("Attempting to brute-force reverse the hash...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(0, 101, 10):
                progress_bar.progress(i)
                status_text.text(f"Tested {i}% of 2^256 possibilities...")
                time.sleep(0.3)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.error("❌ **FAILED**")
                st.write("Cannot find matching private key")
            
            with col2:
                st.metric("Theoretical Time Needed", "10^77 years")
                st.metric("Universe Age", "13.8 billion years")
            
            st.error("""
            **Why This is Impossible:**
            - There are 2^256 ≈ 1.15 × 10^77 possible private keys
            - Even checking 1 trillion keys per second would take 10^64 seconds
            - This is **vastly longer** than the age of the universe (4 × 10^17 seconds)
            
            **The Hash Function is Cryptographically Secure** - it's designed to make the reverse operation computationally infeasible!
            """)
    
    # === APPROACH 3: One-Way Hash Function Visualization ===
    with st.expander("↔️ Approach 3: One-Way Hash Function Demonstration", expanded=False):
        st.write("### Hash Function Properties")
        
        st.write("Generate a new sample key pair to see the one-way nature:")
        
        if st.button("🔄 Generate New Sample Pair"):
            private_sample = os.urandom(32)
            public_sample = hashlib.sha256(private_sample).digest()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.success("**INPUT (Private Key) - 32 Random Bytes**")
                st.code(private_sample.hex(), language="hex")
            
            with col2:
                st.success("**OUTPUT (Public Key) - SHA-256 Hash**")
                st.code(public_sample.hex(), language="hex")
            
            # Display properties
            st.write("### One-Way Hash Function Properties:")
            
            properties = {
                "✅ Deterministic": "Same input always produces same output",
                "✅ Uniform Distribution": "Output looks completely random",
                "✅ Avalanche Effect": "Small input change → completely different output",
                "❌ NOT Reversible": "Cannot recover input from output",
                "❌ NO Collisions (ideally)": "Different inputs should give different outputs"
            }
            
            for prop, description in properties.items():
                st.write(f"**{prop}**")
                st.write(f"→ {description}")
                st.write("")
    
    # === APPROACH 4: Attack Complexity Comparison ===
    with st.expander("📊 Approach 4: Attack Complexity Visualization", expanded=False):
        st.write("### Security Strength Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("#### Chart 1: Security Against Different Attackers")
            
            # Chart 1: Security levels
            fig, ax = plt.subplots(figsize=(10, 6))
            
            schemes = ["ECDSA\n(Classical)", "Lamport\n(Hash-based)"]
            classical_security = [128, 128]  # bits
            quantum_security = [0, 128]  # bits
            
            x = np.arange(len(schemes))
            width = 0.35
            
            bars1 = ax.bar(x - width/2, classical_security, width, label='Against Classical Attackers', color='#2ecc71')
            bars2 = ax.bar(x + width/2, quantum_security, width, label='Against Quantum Attackers', color='#e74c3c')
            
            ax.set_ylabel('Effective Security (bits)', fontsize=12)
            ax.set_title('Security Strength Comparison', fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(schemes)
            ax.legend()
            ax.set_ylim(0, 150)
            
            # Add value labels on bars
            for bars in [bars1, bars2]:
                for bar in bars:
                    height = bar.get_height()
                    if height > 0:
                        ax.text(bar.get_x() + bar.get_width()/2., height,
                               f'{int(height)}',
                               ha='center', va='bottom')
            
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            st.write("#### Chart 2: Computational Difficulty (Log Scale)")
            
            # Chart 2: Computational cost
            fig, ax = plt.subplots(figsize=(10, 6))
            
            attacks = [
                'ECDSA\n(Classical)',
                'ECDSA\n(Quantum)',
                'Lamport\n(Brute Force)'
            ]
            operations = [float(2**128), float(2**128), float(2**256)]
            colors = ['#3498db', '#e74c3c', '#2ecc71']
            
            bars = ax.bar(attacks, operations, color=colors)
            ax.set_ylabel('Operations Needed (log scale)', fontsize=12)
            ax.set_title('Computational Difficulty to Break Cryptosystem', fontsize=14, fontweight='bold')
            ax.set_yscale('log')
            
            # Add labels
            labels_text = ['~10^38', '~10^38', '~10^77']
            for bar, label in zip(bars, labels_text):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       label,
                       ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            st.pyplot(fig)
        
        st.success("""
        **Key Takeaways:**
        1. **ECDSA** loses its security against quantum computers (Shor's Algorithm)
        2. **Lamport Signatures** remain secure because hash functions are quantum-resistant
        3. The computational difficulty of reversing a hash is astronomically high (2^256)
        4. Private keys embedded in public keys through cryptographic hashing cannot be extracted
        """)

# ============ TAB 4: QUANTUM ATTACK SIMULATION ============
with tab4:
    st.subheader("⚛️ Quantum Attack Simulation")
    
    if st.button("🚀 Simulate Shor's Algorithm Attack"):
        st.info("Running Shor's Algorithm Simulation...")
        
        progress_bar = st.progress(0)
        status = st.empty()
        
        for i in range(101):
            progress_bar.progress(i)
            status.text(f"Progress: {i}%")
            time.sleep(0.02)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.error("""
            **Classical Crypto (ECDSA)**: 🚨 VULNERABLE
            - ❌ Private key CAN be derived with quantum computer
            - ❌ Shor's Algorithm breaks ECDSA in polynomial time
            - ⚠️ Security: Broken
            """)
        
        with col2:
            st.success("""
            **Post-Quantum Crypto (Lamport)**: 🛡️ SECURE
            - ✅ Private key CANNOT be derived
            - ✅ No known efficient quantum attack
            - ✅ Based on hash function one-way property
            - ✅ Security: Maintained against quantum
            """)
    
    st.write("---")
    st.info("""
    **Note:** This simulation is theoretical and based on Shor's Algorithm concepts. 
    The actual quantum attack is not executed in this demo.
    """)

# ============ TAB 5: COMPARISON ============
with tab5:
    st.subheader("📊 Comprehensive Comparison")
    
    comparison_data = {
        "Feature": [
            "Quantum Resistance",
            "Key Size",
            "Signature Size",
            "Speed",
            "Private Key Derivable",
            "One-Time Use",
            "Standardization",
            "Real-World Adoption"
        ],
        "Classical (ECDSA)": [
            "❌ No",
            "256 bits",
            "~64 bytes",
            "⚡ Fast",
            "✅ Yes (with quantum computer)",
            "❌ No (reusable)",
            "✅ Yes (NIST standardized)",
            "✅ Widespread"
        ],
        "Post-Quantum (Lamport)": [
            "✅ Yes",
            "~8KB",
            "~8KB",
            "🐢 Slower",
            "❌ No (hash-based)",
            "✅ Yes (one-time only)",
            "⚠️ Experimental",
            "⚠️ Limited"
        ]
    }
    
    st.table(comparison_data)
    
    st.caption("**Note:** Quantum Attack is theoretically based on Shor's Algorithm, not executed in this demo")
    
    st.info("""
    **Summary:**
    - Lamport signatures are one-time use, so in a real application you would need to generate new keys for each message
    - In practice, more efficient post-quantum schemes like CRYSTALS-Dilithium or Falcon would be used instead of Lamport signatures
    - This demo is for educational purposes and does not implement actual quantum algorithms or attacks
    - The security of post-quantum schemes is based on hard mathematical problems believed resistant to quantum attacks
    - Lamport signatures are based only on hash functions (quantum-resistant), while ECDSA relies on elliptic curve discrete logarithm (broken by Shor's Algorithm)
    """)
    st.info("Currently only Grover's Algorithm can reduce the time complexity of lamport based cryptocurrency.")
