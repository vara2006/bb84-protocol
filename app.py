from flask import Flask, render_template, jsonify, request
import random
import hashlib
import base64
from cryptography.fernet import Fernet

app = Flask(__name__)

shared_key = None
key_number = 0
messages = []

SECURITY_THRESHOLD = 11.0
TOTAL_QUBITS = 100


# ============================================================
# BB84 PROTOCOL
# ============================================================

def run_bb84(eve=False):

    # Alice creates random bits
    alice_bits = [
        random.randint(0, 1)
        for _ in range(TOTAL_QUBITS)
    ]

    # Alice randomly selects bases
    # 0 = +
    # 1 = x
    alice_bases = [
        random.randint(0, 1)
        for _ in range(TOTAL_QUBITS)
    ]

    # Bob randomly selects measurement bases
    bob_bases = [
        random.randint(0, 1)
        for _ in range(TOTAL_QUBITS)
    ]

    # Eve's information
    eve_bases = []
    eve_bits = []

    bob_bits = []

    # ========================================================
    # QUANTUM TRANSMISSION
    # ========================================================

    for i in range(TOTAL_QUBITS):

        original_bit = alice_bits[i]
        alice_basis = alice_bases[i]

        # ----------------------------------------------------
        # NO EVE
        # ----------------------------------------------------

        if not eve:

            if alice_basis == bob_bases[i]:

                bob_bit = original_bit

            else:

                bob_bit = random.randint(0, 1)

            bob_bits.append(bob_bit)

            eve_bases.append(None)
            eve_bits.append(None)

        # ----------------------------------------------------
        # EVE ATTACK
        # ----------------------------------------------------

        else:

            # Eve randomly chooses a basis
            eve_basis = random.randint(0, 1)

            eve_bases.append(eve_basis)

            # Eve measures the qubit
            if eve_basis == alice_basis:

                eve_bit = original_bit

            else:

                # Wrong basis gives random result
                eve_bit = random.randint(0, 1)

            eve_bits.append(eve_bit)

            # Eve sends her measured state toward Bob
            if bob_bases[i] == eve_basis:

                bob_bit = eve_bit

            else:

                # Bob uses different basis
                bob_bit = random.randint(0, 1)

            bob_bits.append(bob_bit)

    # ========================================================
    # SIFTING
    # ========================================================

    sifted_alice = []
    sifted_bob = []

    matching_positions = []
    error_positions = []

    for i in range(TOTAL_QUBITS):

        # Alice and Bob publicly compare bases
        if alice_bases[i] == bob_bases[i]:

            matching_positions.append(i)

            sifted_alice.append(alice_bits[i])
            sifted_bob.append(bob_bits[i])

            if alice_bits[i] != bob_bits[i]:

                error_positions.append(i)

    # ========================================================
    # QBER
    # ========================================================

    matching_count = len(sifted_alice)
    error_count = len(error_positions)

    if matching_count > 0:

        qber = (
            error_count /
            matching_count
        ) * 100

    else:

        qber = 100.0

    qber = round(qber, 2)

    # ========================================================
    # SECURITY DECISION
    # ========================================================

    secure = qber <= SECURITY_THRESHOLD

    # ========================================================
    # CREATE DISPLAY TABLE
    # ========================================================

    table = []

    for i in range(min(TOTAL_QUBITS, 30)):

        if alice_bases[i] == 0:
            alice_basis_display = "+"
        else:
            alice_basis_display = "×"

        if bob_bases[i] == 0:
            bob_basis_display = "+"
        else:
            bob_basis_display = "×"

        if eve:

            if eve_bases[i] == 0:
                eve_basis_display = "+"
            else:
                eve_basis_display = "×"

        else:

            eve_basis_display = "-"

        if alice_bases[i] == bob_bases[i]:

            result = (
                "ERROR"
                if alice_bits[i] != bob_bits[i]
                else "MATCH"
            )

        else:

            result = "DISCARDED"

        table.append({

            "position": i + 1,

            "alice_bit": alice_bits[i],

            "alice_basis": alice_basis_display,

            "eve_basis": eve_basis_display,

            "bob_basis": bob_basis_display,

            "bob_bit": bob_bits[i],

            "result": result

        })

    # ========================================================
    # KEY
    # ========================================================

    if secure:

        key_bits = sifted_alice

    else:

        key_bits = []

    return {

        "alice_bits": alice_bits,

        "alice_bases": alice_bases,

        "eve_bases": eve_bases,

        "eve_bits": eve_bits,

        "bob_bases": bob_bases,

        "bob_bits": bob_bits,

        "sifted_alice": sifted_alice,

        "sifted_bob": sifted_bob,

        "matching_count": matching_count,

        "error_count": error_count,

        "error_positions": error_positions,

        "qber": qber,

        "secure": secure,

        "table": table

    }


# ============================================================
# CREATE CRYPTOGRAPHIC KEY
# ============================================================

def create_encryption_key(bits):

    bit_string = "".join(
        str(bit)
        for bit in bits
    )

    # Add extra randomness to the derivation
    hash_value = hashlib.sha256(
        bit_string.encode()
    ).digest()

    return base64.urlsafe_b64encode(
        hash_value
    )


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return render_template("index.html")


# ============================================================
# GENERATE SECURE BB84 KEY
# ============================================================

@app.route("/generate-key")
def generate_key():

    global shared_key
    global key_number
    global messages

    result = run_bb84(eve=False)

    if result["secure"]:

        shared_key = create_encryption_key(
            result["sifted_alice"]
        )

        key_number += 1

        messages = []

        return jsonify({

            "success": True,

            "secure": True,

            "attack": False,

            "key_number": key_number,

            "qber": result["qber"],

            "errors": result["error_count"],

            "matching": result["matching_count"],

            "total_qubits": TOTAL_QUBITS,

            "threshold": SECURITY_THRESHOLD,

            "table": result["table"],

            "message":
                "Secure BB84 key established."

        })

    shared_key = None

    return jsonify({

        "success": False,

        "secure": False,

        "attack": False,

        "key_number": key_number,

        "qber": result["qber"],

        "errors": result["error_count"],

        "matching": result["matching_count"],

        "total_qubits": TOTAL_QUBITS,

        "threshold": SECURITY_THRESHOLD,

        "table": result["table"],

        "message":
            "Key rejected."

    })


# ============================================================
# EVE ATTACK
# ============================================================

@app.route("/eve-attack")
def eve_attack():

    global shared_key
    global messages

    # The previous key must immediately be considered invalid
    shared_key = None

    # Run BB84 with Eve
    result = run_bb84(eve=True)

    qber = result["qber"]

    # ========================================================
    # SECURITY EVENT LOG
    # ========================================================

    messages = [

        {
            "sender": "SYSTEM",
            "text": "🕵️ Eve entered the quantum channel.",
            "system": True
        },

        {
            "sender": "SYSTEM",
            "text": "⚛️ Eve selected random measurement bases.",
            "system": True
        },

        {
            "sender": "SYSTEM",
            "text": "🔬 Eve measured intercepted qubits.",
            "system": True
        },

        {
            "sender": "SYSTEM",
            "text": "⚠️ Some quantum states were disturbed.",
            "system": True
        },

        {
            "sender": "SYSTEM",
            "text":
                "📊 QBER = "
                + str(qber)
                + "%",
            "system": True
        }

    ]

    # ========================================================
    # ATTACK DETECTED
    # ========================================================

    if qber > SECURITY_THRESHOLD:

        messages.extend([

            {
                "sender": "SYSTEM",
                "text":
                    "🚨 POSSIBLE EAVESDROPPING DETECTED!",
                "system": True
            },

            {
                "sender": "SYSTEM",
                "text":
                    "❌ Shared key rejected.",
                "system": True
            },

            {
                "sender": "SYSTEM",
                "text":
                    "🔒 Alice ↔ Bob messaging blocked.",
                "system": True
            }

        ])

        return jsonify({

            "success": False,

            "secure": False,

            "attack": True,

            "detected": True,

            "qber": qber,

            "errors": result["error_count"],

            "matching": result["matching_count"],

            "threshold": SECURITY_THRESHOLD,

            "total_qubits": TOTAL_QUBITS,

            "table": result["table"],

            "error_positions":
                result["error_positions"],

            "message":
                "Eve detected. Key rejected."

        })

    # ========================================================
    # LOW QBER
    # ========================================================

    messages.append({

        "sender": "SYSTEM",

        "text":
            "🟢 QBER is below the security threshold.",

        "system": True

    })

    return jsonify({

        "success": False,

        "secure": False,

        "attack": True,

        "detected": False,

        "qber": qber,

        "errors": result["error_count"],

        "matching": result["matching_count"],

        "threshold": SECURITY_THRESHOLD,

        "total_qubits": TOTAL_QUBITS,

        "table": result["table"],

        "error_positions":
            result["error_positions"],

        "message":
            "Eve attack simulated, but QBER did not cross threshold."

    })


# ============================================================
# SEND MESSAGE
# ============================================================

@app.route(
    "/send-message",
    methods=["POST"]
)
def send_message():

    global shared_key
    global messages

    data = request.get_json()

    sender = data.get(
        "sender",
        "Alice"
    )

    message = data.get(
        "message",
        ""
    ).strip()

    # Empty message
    if not message:

        return jsonify({

            "success": False,

            "error":
                "Message cannot be empty."

        })

    # No valid BB84 key
    if shared_key is None:

        return jsonify({

            "success": False,

            "blocked": True,

            "error":
                "🚨 Secure channel blocked. BB84 key is not valid."

        })

    # ========================================================
    # ENCRYPT
    # ========================================================

    cipher = Fernet(shared_key)

    encrypted = cipher.encrypt(
        message.encode()
    ).decode()

    # ========================================================
    # DECRYPT
    # ========================================================

    decrypted = cipher.decrypt(
        encrypted.encode()
    ).decode()

    # ========================================================
    # SAVE MESSAGE
    # ========================================================

    messages.append({

        "sender": sender,

        "text": decrypted,

        "encrypted": encrypted,

        "system": False

    })

    return jsonify({

        "success": True,

        "sender": sender,

        "text": decrypted,

        "encrypted": encrypted

    })


# ============================================================
# GET CHAT MESSAGES
# ============================================================

@app.route("/messages")
def get_messages():

    return jsonify({

        "messages": messages

    })


# ============================================================
# GET BB84 DETAILS
# ============================================================

@app.route("/bb84-details")
def bb84_details():

    result = run_bb84(eve=False)

    return jsonify({

        "total_qubits": TOTAL_QUBITS,

        "matching_bases":
            result["matching_count"],

        "errors":
            result["error_count"],

        "qber":
            result["qber"],

        "threshold":
            SECURITY_THRESHOLD,

        "table":
            result["table"]

    })


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return jsonify({

        "application":
            "QuantumShield",

        "protocol":
            "BB84",

        "status":
            "running",

        "quantum_hardware":
            "simulation"

    })


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 55)
    print("              QUANTUMSHIELD")
    print("          BB84 Secure Messenger")
    print("=" * 55)
    print()
    print("Server:")
    print("http://127.0.0.1:5000")
    print()
    print("Features:")
    print("  ✓ BB84 simulation")
    print("  ✓ Eve intercept attack")
    print("  ✓ QBER calculation")
    print("  ✓ Key rejection")
    print("  ✓ Secure messaging")
    print("  ✓ Encryption")
    print()
    print("=" * 55)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )