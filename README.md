# 📟 Advanced Crypto & Steganography Lab

Welcome to the **Final Edition** of the Chaos Laboratory. This project is a comprehensive cryptographic suite that merges advanced mathematics with practical security applications. It utilizes the **Jacobsthal sequence** for initial key generation and **Logistic Maps** ($x = r \cdot x \cdot (1 - x)$) for high-entropy data encryption.

## 🧪 Modules
* **🖼️ Image Sealing:** Uses chaotic XOR operations to encrypt images into noise, verifiable through real-time Histogram analysis[cite: 1].
* **✉️ Secure Messaging:** Byte-level chaotic encryption for text, ensuring privacy through complex mathematical sequences[cite: 1].
* **🕵️ Steganography:** Hide encrypted messages within the Least Significant Bits (LSB) of image pixels[cite: 1].
* **📊 Mathematical Analysis:** Detailed insights into Jacobsthal polynomials and bifurcation points in chaotic systems[cite: 1].

## 🧠 Why Jacobsthal?
In this project, I utilize the **Jacobsthal sequence** ($J_n = J_{n-1} + 2J_{n-2}$) because it grows significantly faster than the Fibonacci sequence. This provides a much larger initial value space, making the encryption motor exponentially more resistant to brute-force attacks[cite: 1].

## 🛠️ Tech Stack
* **Python**
* **Streamlit** (Customized Dark/Matrix UI)[cite: 1]
* **NumPy & Matplotlib** (Statistical security evidence)[cite: 1]
* **Pillow (PIL)** (Advanced image processing)[cite: 1]

## 🚀 Deployment
This lab is deployed on Streamlit Cloud.
1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the lab: `streamlit run app.py`

---
*Developed by Sena Yarar | Mathematics & Computer Programming*