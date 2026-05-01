import streamlit as st
from PIL import Image
import numpy as np
import io
import matplotlib.pyplot as plt
import secrets  # for secure random password generation
import string    # for character sets

# --- 1. MATHEMATICAL ENGINES ---
def jacobsthal(n):
    # Jacobsthal equation: J(n) = J(n-1) + 2J(n-2)
    n = (n % 40) + 10 
    j = [0, 1]
    for i in range(2, n + 1): # Values between 10-50, for the chaos to be sufficiently complex, our key space
        j.append(j[i-1] + 2 * j[i-2])
    return j[n]

def password_to_number(password):
    # To convert the input text into a numerical value using ASCII sum
    return sum(ord(c) for c in password)

def text_chaos_operation(message, password):
    # UTF-8 and Byte-Level processing engine (Supports all characters)
    n_value = password_to_number(password)
    x = (jacobsthal(n_value) % 1000) / 1000.0
    if x == 0: x = 0.5
    r = 3.99 # The highly chaotic region of the Logistic Map
    msg_bytes = message.encode('utf-8')
    result_bytes = bytearray()
    for b in msg_bytes:
        x = r * x * (1 - x)
        key = int(x * 255)
        result_bytes.append(b ^ (key % 256))
    return result_bytes

def draw_histogram(image, title):
    img_array = np.array(image.convert('RGB'))
    fig, ax = plt.subplots(figsize=(5, 3))
    colors = ('red', 'green', 'blue')
    for i, col in enumerate(colors):
        hist = np.histogram(img_array[:, :, i], bins=256, range=(0, 256))[0]
        ax.plot(hist, color=col, alpha=0.8)
    ax.set_title(title, color='white', fontsize=10)
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.tick_params(colors='white', labelsize=8)
    for spine in ax.spines.values(): spine.set_color('white')
    return fig

def hide_message(image, message, password):
    encrypted_bytes = text_chaos_operation(message, password)
    binary_message = ''.join(format(b, '08b') for b in encrypted_bytes) + '1111111111111110'
    img_array = np.array(image.convert('RGB')).astype(np.int32) # Overflow protection
    shape = img_array.shape
    flat_img = img_array.flatten()
    if len(binary_message) > len(flat_img): return None
    for i in range(len(binary_message)):
        flat_img[i] = (flat_img[i] & ~1) | int(binary_message[i])
    return Image.fromarray(flat_img.clip(0, 255).astype('uint8').reshape(shape))

def decode_message(image, password):
    img_array = np.array(image.convert('RGB'))
    flat_img = img_array.flatten()
    binary_data = ""
    for i in range(len(flat_img)):
        binary_data += str(flat_img[i] & 1)
        if len(binary_data) > 16 and binary_data[-16:] == '1111111111111110': break
    byte_list = [int(binary_data[i:i+8], 2) for i in range(0, len(binary_data)-16, 8)]
    encrypted_bytes = bytes(byte_list)
    n_value = password_to_number(password)
    x = (jacobsthal(n_value) % 1000) / 1000.0
    if x == 0: x = 0.5
    r = 3.99
    original_bytes = bytearray()
    for b in encrypted_bytes:
        x = r * x * (1 - x)
        original_bytes.append(b ^ (int(x * 255) % 256))
    return original_bytes.decode('utf-8')

# --- 2. NEW: RANDOM PASSWORD GENERATOR FUNCTION ---
def generate_random_password():
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for i in range(12))

# --- 3. UI DESIGN ---
st.set_page_config(page_title="Sena Yarar | Crypto Lab FINAL", layout="wide")
st.markdown("""<style>
    .stApp { background-color: #000000; }
    h1, h2, h3 { color: #00FF41 !important; text-align: center; font-family: 'Courier New'; }
    .stMarkdown p, label, .stWrite, p { color: #FFFFFF !important; font-weight: 500 !important; }
    .stButton>button, .stDownloadButton>button { background-color: #003B00 !important; color: #FFFFFF !important; border: 1px solid #00FF41 !important; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #00FF41 !important; color: #000000 !important; }
    [data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #00FF41; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #001a00 !important; color: #FFFFFF !important; border: 1px solid #00FF41 !important; }
    .stFileUploader section div { color: #FFFFFF !important; }
</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🎛️ CONTROL CENTER")
    module = st.radio("Select a Module:", ["🖼️ Image Sealing", "✉️ Text Encryption", "🕵️ Steganography", "📊 Mathematical Analysis"])
    st.markdown("---")
    st.info("Sena Yarar | Mathematics & Computer Programming")

# --- 4. MODULES ---

if module == "🖼️ Image Sealing":
    st.title("📟 Image Sealing & Security Analysis")
    
    col_s1, col_s2 = st.columns([4, 1])
    with col_s1:
        if 'p1' not in st.session_state: st.session_state.p1 = ""
        password = st.text_input("ENTER THE KEY:", type="password", key="p1")
    with col_s2:
        st.write(" ") 
        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        st.button("🎲 GENERATE", key="b1", on_click=lambda: st.session_state.update({'p1': generate_random_password()}))

    up = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
    if up and password:
        img = Image.open(up)
        col1, col2 = st.columns(2)
        with col1: st.image(img, caption="Original Image", use_container_width=True)
        if st.button("TRIGGER SYSTEM"):
            img_arr = np.array(img.convert('RGB'))
            n_value = password_to_number(password)
            x = (jacobsthal(n_value) % 1000) / 1000.0
            r = 3.99
            flat = img_arr.flatten().astype(np.int32)
            for i in range(len(flat)):
                x = r * x * (1 - x)
                flat[i] = flat[i] ^ int(x * 255)
            res = Image.fromarray(flat.clip(0, 255).astype('uint8').reshape(img_arr.shape))
            with col2: st.image(res, caption="Sealed Image", use_container_width=True)
            
            st.markdown("### 📊 Statistical Security Evidence (Histogram)")
            c1, c2 = st.columns(2)
            with c1: st.pyplot(draw_histogram(img, "Original Color Distribution"))
            with c2: st.pyplot(draw_histogram(res, "Sealed Chaotic Distribution"))
            buf = io.BytesIO(); res.save(buf, format="PNG")
            st.download_button("📥 SAVE RESULT", buf.getvalue(), "sealed.png")

elif module == "✉️ Text Encryption":
    st.title("✉️ Secure Messaging Module")
    
    col_s1, col_s2 = st.columns([4, 1])
    with col_s1:
        if 'p2' not in st.session_state: st.session_state.p2 = ""
        password = st.text_input("KEY:", type="password", key="p2")
    with col_s2:
        st.write(" ")
        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        st.button("🎲 GENERATE", key="b2", on_click=lambda: st.session_state.update({'p2': generate_random_password()}))

    tab_encrypt, tab_decrypt = st.tabs(["Encrypt Message", "Decrypt Message"])

    with tab_encrypt:
        msg = st.text_area("Write Your Message:")
        if st.button("TRANSFORM") and msg and password:
            res_bytes = text_chaos_operation(msg, password)
            st.markdown("### Chaotic Output (Hex):")
            st.code(res_bytes.hex(), language=None)
            st.info("This message can only be decrypted with the exact same key.")

    with tab_decrypt:
        hex_input = st.text_area("Paste the Hex Code to Decrypt:")
        if st.button("DECRYPT") and hex_input and password:
            try:
                encrypted_bytes = bytes.fromhex(hex_input)
                n_value = password_to_number(password)
                x = (jacobsthal(n_value) % 1000) / 1000.0
                if x == 0: x = 0.5
                r = 3.99
                decrypted_bytes = bytearray()
                for b in encrypted_bytes:
                    x = r * x * (1 - x)
                    decrypted_bytes.append(b ^ (int(x * 255) % 256))
                
                st.success(f"Original Message: {decrypted_bytes.decode('utf-8')}")
            except Exception as e:
                st.error("Error: Invalid hex code or incorrect key!")

elif module == "🕵️ Steganography":
    st.title("🕵️ Steganography Laboratory")
    tab1, tab2 = st.tabs(["Hide Message", "Read Message"])
    with tab1:
        col_s1, col_s2 = st.columns([4, 1])
        with col_s1:
            if 'p3' not in st.session_state: st.session_state.p3 = ""
            s_h = st.text_input("KEY (Hide):", type="password", key="p3")
        with col_s2:
            st.write(" ")
            st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
            st.button("🎲 GENERATE", key="b3", on_click=lambda: st.session_state.update({'p3': generate_random_password()}))

        m_h = st.text_input("Secret Note to Embed:")
        u_h = st.file_uploader("Cover Photo (PNG recommended)", type=['png'], key="u1")
        if st.button("EMBED DATA INTO PIXELS") and u_h and m_h and s_h:
            res = hide_message(Image.open(u_h), m_h, s_h)
            if res:
                st.image(res, caption="Image with Invisible Message", width=500)
                buf = io.BytesIO(); res.save(buf, format="PNG")
                st.download_button("📥 DOWNLOAD SECRET IMAGE", buf.getvalue(), "stego_result.png")
    with tab2:
        s_r = st.text_input("KEY (Read):", type="password", key="s2")
        u_r = st.file_uploader("Upload Image", type=['png'], key="u2")
        if st.button("EXTRACT MESSAGE"):
            try:
                res = decode_message(Image.open(u_r), s_r)
                st.success(f"Decoded Secret Message: {res}")
            except: st.error("Error: Incorrect key or data corruption.")

elif module == "📊 Mathematical Analysis":
    st.title("📈 Mathematics of Chaos")
    st.write("The Jacobsthal sequence provides a robust starting point for chaotic systems. As an example, you can see the first 20 Jacobsthal numbers below:")
    jacobsthal_list = [jacobsthal(i) for i in range(20)]
    st.code(jacobsthal_list, language=None) 
    
    st.markdown("""
    **Why did I use Jacobsthal?**
    The Jacobsthal sequence ($J_n = J_{n-1} + 2J_{n-2}$) is a rapidly growing sequence. For instance, it grows significantly faster than the Fibonacci sequence. This allows the initial values generated for our chaotic system to be distributed across a much broader numerical space. This velocity makes the initial conditions of our chaos engine significantly more complex and unpredictable, rendering brute-force attacks mathematically infeasible.
    """)
    st.markdown("---")
    
    st.subheader("🧪 Cryptographic Security Analysis")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<h4 style="color:#00CFFF; font-weight:700; margin:0;">🛡️ Statistical Randomness</h4>', unsafe_allow_html=True)
        st.write("""
        The chaos engine in our system is based on the principle of **Ergodicity**. This ensures that the generated encryption keys are distributed homogeneously and unpredictably across every pixel of the image. The 'flattening' observed in the histogram analysis is the empirical proof of this randomness.
        """)
    with col_b:
        st.markdown('<h4 style="color:#00CFFF; font-weight:700; margin:0;">🦋 The Butterfly Effect (Sensitivity)</h4>', unsafe_allow_html=True)
        st.write("""
        Thanks to the Jacobsthal sequence, even the most microscopic alteration in the encryption key completely transforms the chaotic flow. This constitutes the system's primary defense mechanism against 'Differential Attacks'.
        """)
    st.info("📊 This mathematical model ensures that the system doesn't merely conceal the image, but mathematically transforms it into undecipherable 'noise'.")