# 🔐 QuantumShield - BB84 Quantum Key Distribution Secure Messenger

## 📌 Project Overview

QuantumShield is a web-based educational prototype that demonstrates how BB84 Quantum Key Distribution (QKD) can be used to establish a secure communication channel between two users, Alice and Bob.

The project simulates a real-world secure messaging application similar to WhatsApp. Alice and Bob first establish a shared secret key using the BB84 protocol. Once the key is successfully established, they can exchange encrypted messages.

The project also includes an Eve (Eavesdropper) attack simulation. When Eve intercepts and measures quantum states using random bases, she can disturb some of the states. Alice and Bob detect this disturbance by calculating the Quantum Bit Error Rate (QBER). If the QBER exceeds the security threshold, the key is rejected and messaging is automatically stopped.

> Note: This is a software simulation of BB84. It does not use a physical quantum computer or actual quantum communication hardware.

---

## 🎯 Objectives

- Demonstrate the BB84 Quantum Key Distribution protocol.
- Generate a shared secret key between Alice and Bob.
- Simulate quantum-state transmission.
- Demonstrate random basis selection.
- Simulate an Eve intercept-and-measure attack.
- Calculate Quantum Bit Error Rate (QBER).
- Detect possible eavesdropping.
- Reject compromised keys.
- Stop communication when an attack is detected.
- Provide a simple WhatsApp-like secure messaging interface.
- Demonstrate message encryption and decryption.

---

## 🧠 What is BB84?

BB84 is a Quantum Key Distribution protocol introduced by Charles Bennett and Gilles Brassard in 1984.

The basic idea is that Alice sends quantum states to Bob using randomly selected bases.

The prototype represents two bases as:

    +  → Rectilinear basis
    ×  → Diagonal basis

Alice randomly generates:

    Bit:   0 or 1
    Basis: + or ×

Bob independently chooses a random basis for each incoming state.

After transmission, Alice and Bob compare their bases. They do not reveal their actual bit values.

Only positions where their bases match are retained.

These retained bits are used to create the shared secret key.

---

## 👥 Real-World Story

The application represents the following scenario:

    Alice 👩                         Bob 👨
       │                                │
       │     BB84 Key Generation        │
       │───────────────────────────────>│
       │                                │
       │       Shared Secret Key        │
       │<──────────────────────────────>│
       │                                │
       │        Secure Messaging        │
       │<──────────────────────────────>│
       │                                │
       │                                │
       │             🕵️ Eve             │
       │          tries to spy          │
       │                │               │
       │                ▼               │
       │        Measures quantum        │
       │             states             │
       │                │               │
       │                ▼               │
       │       Quantum states disturbed │
       │                │               │
       │                ▼               │
       │          QBER increases        │
       │                │               │
       │                ▼               │
       │        🚨 Attack detected      │
       │                │               │
       │                ▼               │
       │          ❌ Key rejected       │
       │                │               │
       │                ▼               │
       │          🔒 Chat stopped       │

---

## ⚙️ How the System Works

### 1. Alice Generates Random Bits

Alice generates a random sequence:

    1 0 1 1 0 0 1 0

She also randomly chooses a basis for every bit:

    + × + × × + + ×

Each quantum state is represented by its bit and basis.

---

### 2. Alice Sends the Quantum States

Alice sends the generated quantum states through the simulated quantum channel.

The prototype represents this quantum transmission using Python data structures and random values.

---

### 3. Bob Selects Random Bases

Bob does not know Alice's bases.

He independently chooses random bases:

    × + + × + × × +

Bob then measures each incoming state.

---

### 4. Basis Comparison

Alice and Bob compare their bases.

Example:

| Position | Alice Basis | Bob Basis | Keep? |
|----------|-------------|-----------|-------|
| 1 | + | + | Yes |
| 2 | × | + | No |
| 3 | + | + | Yes |
| 4 | × | × | Yes |
| 5 | + | × | No |

Only matching bases are retained.

This process is called sifting.

---

### 5. Shared Key Generation

The bits corresponding to matching bases are used to create the shared key.

Example:

    Alice: 1 0 1 1
    Bob:   1 0 1 1

    Shared Key: 1 0 1 1

The prototype derives an encryption key from the resulting key material.

---

## 🕵️ Eve Attack Simulation

The project contains an Eve Attack button.

When the user clicks:

    🕵️ Eve Attacks

Eve performs an intercept-and-measure attack.

Eve:

1. Intercepts the simulated quantum state.
2. Randomly chooses a measurement basis.
3. Measures the state.
4. Sends the resulting state toward Bob.

If Eve chooses the wrong basis, the quantum state can be disturbed.

---

## 📊 QBER Calculation

The system calculates Quantum Bit Error Rate (QBER).

The simplified formula is:

    QBER =

    Number of incorrect matching bits
    ---------------------------------- × 100
    Number of matching bits

Example:

    Matching bits = 50
    Incorrect bits = 10

    QBER = (10 / 50) × 100

    QBER = 20%

The prototype uses a demonstration security threshold of:

    11%

Therefore:

    QBER <= 11%
        ↓
    Channel acceptable
        ↓
    Key can be used

    QBER > 11%
        ↓
    Security risk
        ↓
    Key rejected
        ↓
    Chat stopped

---

## 🚨 Attack Detection

When Eve causes a sufficiently high QBER, the application displays:

    🚨 EAVESDROPPING DETECTED

    QBER = 20%
    Threshold = 11%

    ❌ Shared key rejected

    🔒 Secure communication stopped

The message-sending buttons are disabled.

---

## 💬 Secure Chat

After successful BB84 key generation, Alice and Bob can communicate.

Example:

    Alice:
    Hi Bob 👋

    Bob:
    Hi Alice 👋

    Alice:
    How are you?

    Bob:
    I am fine 👍

The interface is designed to look similar to a modern messaging application.

---

## 🔐 Message Encryption

The prototype uses the generated key with Fernet symmetric encryption.

The basic process is:

    Plain Message
          ↓
    BB84-derived Key
          ↓
       Encryption
          ↓
    Encrypted Message
          ↓
      Transmission
          ↓
       Decryption
          ↓
    Original Message

Example:

    Original Message:

    Hi Bob 👋

    Encrypted Message:

    gAAAAAB...

The encrypted ciphertext is not intended to be human-readable.

---

## 🛑 What Happens During an Eve Attack?

Before the attack:

    Alice                         Bob

    Hi Bob 👋  ──────────────────> Hi Bob 👋

    How are you? ────────────────> How are you?

    Status:
    🟢 Secure

When Eve enters:

    Alice
      │
      ▼
    🕵️ Eve
      │
      ▼
    Bob

The application displays:

    🚨 EVE INTERCEPTING

The QBER is then calculated.

If QBER exceeds the security threshold:

    QBER = 18%
    Threshold = 11%

    🚨 ATTACK DETECTED

    ❌ KEY REJECTED

    🔒 CHAT STOPPED

Any new message is blocked until a new secure key is generated.

---

## 🔄 New Key Generation

After an attack, the compromised key is discarded.

The user can click:

    🔄 Generate New Key

A new BB84 simulation is performed.

If the new QBER is acceptable:

    New BB84 Key
          ↓
    QBER Acceptable
          ↓
    🔑 New Shared Key
          ↓
    🟢 Secure Channel
          ↓
    Chat Resumes

---

## 📊 BB84 Visualization Table

The application displays a BB84 transmission table:

| Position | Alice Bit | Alice Basis | Eve Basis | Bob Basis | Bob Bit | Result |
|----------|-----------|-------------|-----------|-----------|---------|--------|
| 1 | 1 | + | × | + | 0 | ERROR |
| 2 | 0 | × | + | + | 1 | DISCARDED |
| 3 | 1 | + | + | + | 1 | MATCH |

### MATCH

Alice and Bob used the same basis and obtained the same bit.

### ERROR

Alice and Bob used the same basis, but their bits differ.

These errors contribute to QBER.

### DISCARDED

Alice and Bob used different bases.

That position is not used for the final key.

---

## 🖥️ User Interface

### Alice Phone

    ┌─────────────────────────┐
    │ 👩 Bob                  │
    │ 🟢 Secure               │
    ├─────────────────────────┤
    │                         │
    │ Hi Bob 👋               │
    │                         │
    │ How are you?            │
    │                         │
    ├─────────────────────────┤
    │ Message Bob...       ➤  │
    └─────────────────────────┘

### Bob Phone

    ┌─────────────────────────┐
    │ 👨 Alice                │
    │ 🟢 Secure               │
    ├─────────────────────────┤
    │                         │
    │ Hi Alice 👋             │
    │                         │
    │ I am fine!              │
    │                         │
    ├─────────────────────────┤
    │ Message Alice...     ➤  │
    └─────────────────────────┘

### Eve

                 🕵️
            Eavesdropper

        ─────────────────
          QUANTUM CHANNEL
        ─────────────────

During an attack:

    🚨 EVE INTERCEPTING

---

## 🏗️ System Architecture

                       QuantumShield
                         │
          ┌──────────────┴──────────────┐
          │                             │
       Frontend                       Backend
          │                             │
     HTML / CSS / JS                  Flask
          │                             │
          │                       BB84 Simulation
          │                             │
          │                  ┌──────────┴──────────┐
          │                  │                     │
          │               Alice                  Bob
          │                  │                     │
          │                  └──── Quantum ────────┘
          │                        Channel
          │                           │
          │                          Eve
          │                           │
          │                          QBER
          │                           │
          │                    Security Decision
          │                           │
          │                 ┌─────────┴─────────┐
          │                 │                   │
          │               Secure              Attack
          │                 │                   │
          │                 ▼                   ▼
          │                Chat             Key Reject
          │
          ▼
       Browser

---

## 📁 Project Structure

    QuantumShield/
    │
    ├── app.py
    │
    ├── requirements.txt
    │
    ├── README.md
    │
    └── templates/
        │
        └── index.html

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Backend programming |
| Flask | Web application server |
| HTML | Webpage structure |
| CSS | User interface |
| JavaScript | Frontend interaction |
| BB84 | Quantum key distribution simulation |
| QBER | Attack detection |
| Cryptography | Message encryption |
| Fernet | Symmetric encryption |

---

## 📦 Installation

Clone the repository:

    git clone https://github.com/YOUR_USERNAME/QuantumShield.git

Go into the project:

    cd QuantumShield

Install dependencies:

    pip install -r requirements.txt

Or:

    pip install flask cryptography

---

## 📄 requirements.txt

Create a file named:

    requirements.txt

Add:

    Flask
    cryptography

---

## ▶️ Running the Project

Run:

    python app.py

Then open:

    http://127.0.0.1:5000

---

## 🧪 Hackathon Demonstration

### Step 1 - Establish Connection

Click:

    🔑 Establish BB84 Key

Explain:

Alice and Bob randomly select bases and generate a shared secret key from matching measurements.

### Step 2 - Send Messages

Alice sends:

    Hi Bob 👋

Bob sends:

    Hi Alice 👋

Demonstrate normal secure communication.

### Step 3 - Start Eve Attack

Click:

    🕵️ Eve Attacks

Explain:

Eve attempts to intercept and measure the quantum states.

### Step 4 - Show QBER

Show the QBER value in the security dashboard.

Explain:

Eve's measurement can disturb quantum states, resulting in errors.

### Step 5 - Show Detection

The system displays:

    🚨 EAVESDROPPING DETECTED
    ❌ KEY REJECTED
    🔒 MESSAGING STOPPED

### Step 6 - Show BB84 Table

Explain:

The table displays Alice's basis, Eve's basis, Bob's basis, measured bits, and the final result.

### Step 7 - Generate New Key

Click:

    🔄 Generate New Key

If the QBER is acceptable, communication resumes.

---

## 🌍 Real-World Applications

The concepts demonstrated by this project are relevant to:

- Government communications
- Financial institutions
- Defense communication
- Data centers
- Critical infrastructure
- Secure research networks
- High-security enterprise communication

The messaging application is used as an easy-to-understand demonstration of secure key establishment.

---

## ⚠️ Limitations

This project is an educational prototype and not a production quantum communication system.

It currently:

- Simulates quantum behavior using classical Python.
- Does not transmit actual photons.
- Does not use a physical quantum processor.
- Does not connect to quantum hardware.
- Uses simplified BB84 modeling.
- Uses a demonstration QBER threshold.
- Does not implement a complete production-grade QKD stack.
- Does not provide complete production authentication.

Therefore, this project should be described as:

"A software simulation and visualization of BB84-based Quantum Key Distribution with an intercept-and-measure attack demonstration."

---

## 🚀 Future Enhancements

### 1. Real Quantum Hardware

Integrate the project with quantum computing platforms and real quantum hardware.

### 2. Multiple Attack Types

Possible additions:

- Intercept and Measure
- Man-in-the-Middle
- Photon Loss
- Basis Manipulation
- Noise Attack

### 3. Real-Time QBER Graph

Add a real-time graph showing QBER changes during communication.

### 4. Key History

Store key-generation events:

    Key #1 → Secure
    Key #2 → Rejected
    Key #3 → Secure

### 5. Authentication

Add authentication between Alice and Bob to reduce impersonation risks.

### 6. Database

Store:

- Users
- Chat history
- Security events
- QBER measurements
- Key-generation events

### 7. Real-Time Communication

Use WebSockets for real-time messaging between users.

---

## 🏆 Why This Project Is Suitable for a Hackathon

QuantumShield combines:

    Quantum Computing
           +
    Cybersecurity
           +
    Cryptography
           +
    Web Development
           +
    Interactive Visualization

Instead of displaying only mathematical BB84 calculations, QuantumShield demonstrates the concept through a familiar secure-messaging scenario.

The main security flow is:

    Eve Attack
         ↓
    Quantum Disturbance
         ↓
    QBER Increase
         ↓
    Security Check
         ↓
    Key Rejection
         ↓
    Chat Automatically Blocked

This makes the concept understandable to both technical and non-technical audiences.

---

## 🔮 Future Vision

The long-term goal of QuantumShield is to evolve from a BB84 educational simulation into a more complete quantum-secure communication platform with:

- Real quantum hardware integration
- Advanced QKD protocols
- Real-time communication
- Strong authentication
- Advanced attack detection
- Security analytics
- QBER monitoring
- Quantum-safe cryptography

---

## 👨‍💻 Project Status

    🟢 BB84 Simulation              Completed
    🟢 Shared Key Generation       Completed
    🟢 Eve Attack Simulation       Completed
    🟢 QBER Detection              Completed
    🟢 Key Rejection               Completed
    🟢 Secure Chat UI              Completed
    🟢 BB84 Visualization          Completed
    🟢 Encryption Demonstration    Completed
    🔵 Real Quantum Hardware       Future Work

---

## 📜 Disclaimer

QuantumShield is developed for educational, demonstration, and hackathon purposes.

It is a classical software simulation of the BB84 protocol and should not be considered a real-world QKD implementation.

---

## ⭐ If You Like This Project

If you find this project useful, please consider giving the repository a ⭐ on GitHub.

#QuantumComputing #BB84 #QKD #CyberSecurity #Cryptography #Python #Flask #QuantumSecurity #Hackathon
