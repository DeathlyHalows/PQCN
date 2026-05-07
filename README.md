# PQCN: Post-Quantum Cryptographic Network Simulation

<!-- Dynamic Repository Shields -->
[![GitHub stars](https://img.shields.io/github/stars/DeathlyHalows/PQCN?style=social)](https://github.com/DeathlyHalows/PQCN/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/DeathlyHalows/PQCN?style=social)](https://github.com/DeathlyHalows/PQCN/network/members)

---

## 📖 About the Project

**PQCN** (Post-Quantum Cryptographic Network) is a specialized simulation workspace engineered to prototype, evaluate, and benchmark quantum-resistant cryptographic protocols. As classical cryptographic paradigms (like RSA and ECC) face future vulnerabilities from quantum computing infrastructure, this framework allows developers to study next-generation algorithm behaviors under various network conditions.

The system utilizes a high-efficiency **hybrid architecture**:
*   **Orchestration Layer:** Python controls network topology generation, execution routing, and benchmarking loops.
*   **Performance Layer:** Compiled C, C++, and Cython sub-layers manage high-compute mathematical structures, ensuring that intensive lattice-based or hash-based multi-variate computations do not throttle data transfer simulations.

---

## 🛠️ Step-by-Step Guide: How to Make it Work

Follow these sequential steps to set up your environment, resolve prerequisites, and execute a local cryptographic simulation run.

### 1. Configure System Prerequisites
The engine compiles local performance extensions on-demand. Ensure your operating system possesses a modern C/C++ compiler setup (`gcc`, `clang`, or Microsoft Visual C++ Build Tools) alongside Python 3.9+.

### 2. Clone the Repository
Pull the source files from GitHub to your local production directory:
```bash
git clone https://github.com
cd PQCN
```

### 3. Establish a Virtual Environment
Create an isolated virtual runtime directory to prevent global system package clutter:
```bash
# Windows (Command Prompt/PowerShell)
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
Update package installation tools and deploy all required project requirements outlined in the catalog:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Execute the Simulation Run
Launch the application orchestrator through the terminal:
```bash
python main.py
```
*Note: Upon initial initialization, the execution route triggers Cython/C module binding hooks to build performance layers before commencing simulated cryptographic node network events.*

---
