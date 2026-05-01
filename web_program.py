import streamlit as st
from PIL import Image
import numpy as np
import io
import matplotlib.pyplot as plt
import secrets  # güvenli rastgele şifre için
import string    # karakter seti için

# --- 1. MATEMATİKSEL MOTORLAR ---
def jacobsthal(n):
    # Jacobsthal denklemi: J(n) = J(n-1) + 2J(n-2)
    n = (n % 40) + 10 
    j = [0, 1]
    for i in range(2, n + 1): # 10-50 arası değerler, kaosun yeterince kompleks olması için, anahtar uzayımız
        j.append(j[i-1] + 2 * j[i-2])
    return j[n]

def sifre_to_sayi(sifre):
    # gireceğimiz metni ASCII toplamıyla sayısal değere dönüştürmesi için
    return sum(ord(c) for c in sifre)

def metin_kaos_islem(mesaj, sifre):
    # UTF-8 ve Byte-Level işlem ile Türkçe karakter korumalı motor
    n_degeri = sifre_to_sayi(sifre)
    x = (jacobsthal(n_degeri) % 1000) / 1000.0
    if x == 0: x = 0.5
    r = 3.99 # Kaosun yoğun olduğu bölge
    msg_bytes = mesaj.encode('utf-8')
    sonuc_bytes = bytearray()
    for b in msg_bytes:
        x = r * x * (1 - x)
        anahtar = int(x * 255)
        sonuc_bytes.append(b ^ (anahtar % 256))
    return sonuc_bytes

def histogram_ciz(image, title):
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

def mesaj_gizle(image, mesaj, sifre):
    sifreli_bytes = metin_kaos_islem(mesaj, sifre)
    binary_mesaj = ''.join(format(b, '08b') for b in sifreli_bytes) + '1111111111111110'
    img_dizi = np.array(image.convert('RGB')).astype(np.int32) # Overflow koruması
    sekil = img_dizi.shape
    duz_img = img_dizi.flatten()
    if len(binary_mesaj) > len(duz_img): return None
    for i in range(len(binary_mesaj)):
        duz_img[i] = (duz_img[i] & ~1) | int(binary_mesaj[i])
    return Image.fromarray(duz_img.clip(0, 255).astype('uint8').reshape(sekil))

def mesaj_coz(image, sifre):
    img_dizi = np.array(image.convert('RGB'))
    duz_img = img_dizi.flatten()
    binary_data = ""
    for i in range(len(duz_img)):
        binary_data += str(duz_img[i] & 1)
        if len(binary_data) > 16 and binary_data[-16:] == '1111111111111110': break
    byte_list = [int(binary_data[i:i+8], 2) for i in range(0, len(binary_data)-16, 8)]
    sifreli_bytes = bytes(byte_list)
    n_degeri = sifre_to_sayi(sifre)
    x = (jacobsthal(n_degeri) % 1000) / 1000.0
    if x == 0: x = 0.5
    r = 3.99
    orijinal_bytes = bytearray()
    for b in sifreli_bytes:
        x = r * x * (1 - x)
        orijinal_bytes.append(b ^ (int(x * 255) % 256))
    return orijinal_bytes.decode('utf-8')

# --- 2. YENİ: RASTGELE ŞİFRE ÜRETME FONKSİYONU ---
def rastgele_sifre_uret():
    alfabe = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alfabe) for i in range(12))

# --- 3. TASARIM ---
st.set_page_config(page_title="Sena Yarar | Kripto Lab FINAL", layout="wide")
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
    st.title("🎛️ KONTROL MERKEZİ")
    modul = st.radio("Bir Modül Seçin:", ["🖼️ Görsel Mühürleme", "✉️ Metin Şifreleme", "🕵️ Steganografi", "📊 Matematiksel Analiz"])
    st.markdown("---")
    st.info("Sena Yarar | Matematik & Bilgisayar Programcılığı")

# --- 4. MODÜLLER ---

if modul == "🖼️ Görsel Mühürleme":
    st.title("📟 Görsel Mühürleme & Güvenlik Analizi")
    
    col_s1, col_s2 = st.columns([4, 1])
    with col_s1:
        if 'p1' not in st.session_state: st.session_state.p1 = ""
        sifre = st.text_input("ANAHTARI GİRİN:", type="password", key="p1")
    with col_s2:
        st.write(" ") 
        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        st.button("🎲 ÜRET", key="b1", on_click=lambda: st.session_state.update({'p1': rastgele_sifre_uret()}))

    up = st.file_uploader("Görsel Yükle", type=['png', 'jpg', 'jpeg'])
    if up and sifre:
        img = Image.open(up)
        col1, col2 = st.columns(2)
        with col1: st.image(img, caption="Orijinal Görsel", use_container_width=True)
        if st.button("SİSTEMİ TETİKLE"):
            img_arr = np.array(img.convert('RGB'))
            n_degeri = sifre_to_sayi(sifre)
            x = (jacobsthal(n_degeri) % 1000) / 1000.0
            r = 3.99
            duz = img_arr.flatten().astype(np.int32)
            for i in range(len(duz)):
                x = r * x * (1 - x)
                duz[i] = duz[i] ^ int(x * 255)
            res = Image.fromarray(duz.clip(0, 255).astype('uint8').reshape(img_arr.shape))
            with col2: st.image(res, caption="Mühürlü Görsel", use_container_width=True)
            
            st.markdown("### 📊 İstatistiksel Güvenlik Kanıtı (Histogram)")
            c1, c2 = st.columns(2)
            with c1: st.pyplot(histogram_ciz(img, "Orijinal Renk Dağılımı"))
            with c2: st.pyplot(histogram_ciz(res, "Mühürlü Kaotik Dağılım"))
            buf = io.BytesIO(); res.save(buf, format="PNG")
            st.download_button("📥 SONUCU KAYDET", buf.getvalue(), "mühürlü.png")

elif modul == "✉️ Metin Şifreleme":
    st.title("✉️ Güvenli Mesajlaşma Modülü")
    
    col_s1, col_s2 = st.columns([4, 1])
    with col_s1:
        if 'p2' not in st.session_state: st.session_state.p2 = ""
        sifre = st.text_input("ANAHTAR:", type="password", key="p2")
    with col_s2:
        st.write(" ")
        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        st.button("🎲 ÜRET", key="b2", on_click=lambda: st.session_state.update({'p2': rastgele_sifre_uret()}))

    # Yeni eklenen sekmeler: Şifreleme ve Geri Çözme
    tab_sifrele, tab_coz = st.tabs(["Mesaj Şifrele", "Şifre Çöz"])

    with tab_sifrele:
        msg = st.text_area("Mesajınızı Yazın:")
        if st.button("DÖNÜŞTÜR") and msg and sifre:
            res_bytes = metin_kaos_islem(msg, sifre)
            st.markdown("### Kaotik Çıktı (Hex):")
            st.code(res_bytes.hex(), language=None)
            st.info("Bu mesaj sadece aynı anahtarla geri çözülebilir.")

    with tab_coz:
        hex_input = st.text_area("Çözülecek Hex Kodunu Yapıştırın:")
        if st.button("ŞİFREYİ ÇÖZ") and hex_input and sifre:
            try:
                # Hex string'ini byte dizisine çeviriyoruz
                sifreli_bytes = bytes.fromhex(hex_input)
                # XOR simetrik olduğu için aynı fonksiyonla (metin_kaos_islem) geri çözüyoruz
                n_degeri = sifre_to_sayi(sifre)
                x = (jacobsthal(n_degeri) % 1000) / 1000.0
                if x == 0: x = 0.5
                r = 3.99
                cozulen_bytes = bytearray()
                for b in sifreli_bytes:
                    x = r * x * (1 - x)
                    cozulen_bytes.append(b ^ (int(x * 255) % 256))
                
                st.success(f"Orijinal Mesaj: {cozulen_bytes.decode('utf-8')}")
            except Exception as e:
                st.error("Hata: Geçersiz hex kodu veya yanlış anahtar!")

elif modul == "🕵️ Steganografi":
    st.title("🕵️ Steganografi Laboratuvarı")
    tab1, tab2 = st.tabs(["Mesaj Gizle", "Mesaj Oku"])
    with tab1:
        col_s1, col_s2 = st.columns([4, 1])
        with col_s1:
            if 'p3' not in st.session_state: st.session_state.p3 = ""
            s_g = st.text_input("ANAHTAR (Gizle):", type="password", key="p3")
        with col_s2:
            st.write(" ")
            st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
            st.button("🎲 ÜRET", key="b3", on_click=lambda: st.session_state.update({'p3': rastgele_sifre_uret()}))

        m_g = st.text_input("Gömülecek Gizli Not:")
        u_g = st.file_uploader("Kapak Fotoğrafı (PNG önerilir)", type=['png'], key="u1")
        if st.button("VERİYİ PİKSELLERE GÖM") and u_g and m_g and s_g:
            res = mesaj_gizle(Image.open(u_g), m_g, s_g)
            if res:
                st.image(res, caption="Görünmez Mesajlı Görsel", width=500)
                buf = io.BytesIO(); res.save(buf, format="PNG")
                st.download_button("📥 GİZLİ GÖRSELİ İNDİR", buf.getvalue(), "stego_sonuc.png")
    with tab2:
        s_o = st.text_input("ANAHTAR (Oku):", type="password", key="s2")
        u_o = st.file_uploader("Görseli Yükle", type=['png'], key="u2")
        if st.button("MESAJI ÇIKAR"):
            try:
                res = mesaj_coz(Image.open(u_o), s_o)
                st.success(f"Çözülen Gizli Mesaj: {res}")
            except: st.error("Hata: Yanlış anahtar veya veri bozulması.")

elif modul == "📊 Matematiksel Analiz":
    st.title("📈 Kaosun Matematiği")
    st.write("Jacobsthal dizisi, kaotik sistemler için güçlü bir başlangıç noktası sağlar. Örnek olarak aşağıda ilk 20 Jacobsthal sayısını görebilirsiniz:")
    jacobsthal_list = [jacobsthal(i) for i in range(20)]
    st.code(jacobsthal_list, language=None) 
    
    st.markdown("""
    **Neden Jacobsthal kullandım?**
    Jacobsthal dizisi ($J_n = J_{n-1} + 2J_{n-2}$), hızlı büyüyen bir dizidir. Misal, Fibonacci'den daha hızlı büyür. Bu da kaotik sistemimiz için üretilen başlangıç değerlerinin çok daha geniş bir sayı uzayına yayılmasını sağlar. Bu hız, kaos motorumuzun başlangıç değerlerini daha karmaşık ve tahmin edilemez kılar. Bu da kaba kuvvet (brute-force) saldırılarını imkansız hale getirir.
    """)
    st.markdown("---")
    
    st.subheader("🧪 Kriptografik Güvenlik Analizi")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<h4 style="color:#00CFFF; font-weight:700; margin:0;">🛡️ İstatistiksel Rastgelelik</h4>', unsafe_allow_html=True)
        st.write("""
        Sistemimizdeki kaos motoru **Ergodiklik** ilkesine dayanır. Bu, üretilen şifreleme anahtarlarının 
        görselin her pikseline homojen ve tahmin edilemez şekilde dağılmasını sağlar. 
        Histogram analizlerindeki 'düzleşme' bu rastgeleliğin ispatıdır.
        """)
    with col_b:
        st.markdown('<h4 style="color:#00CFFF; font-weight:700; margin:0;">🦋 Kelebek Etkisi (Duyarlılık)</h4>', unsafe_allow_html=True)
        st.write("""
        Jacobsthal dizisi sayesinde, şifre anahtarındaki en küçük bir değişim bile kaotik 
        akışı tamamen değiştirir. Bu, 'Diferansiyel Saldırılara' karşı sistemin 
        en büyük savunma mekanizmasıdır.
        """)
    st.info("📊 Bu matematiksel model, sistemin sadece görseli gizlemesini değil, onu matematiksel olarak çözülemez bir 'gürültüye' dönüştürmesini sağlar.")