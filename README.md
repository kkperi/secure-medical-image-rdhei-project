# Secure Reversible Data Hiding in Encrypted Medical Images Using Huffman Tree Coding

## 📌 Overview

This project presents an implementation of **Secure Reversible Data Hiding in Encrypted Medical Images (RDHEMI)** using **Hybrid Tree Coding (HTC)** and **Count Encryption (CE)**. The framework enables secure embedding of secret information into encrypted medical images while ensuring **perfect recovery of both the embedded payload and the original medical image**.

The implementation is based on the research paper:

**"Reversible Data Hiding in Encrypted Medical Images Based on Huffman Tree Coding and Count-Encryption."**

---

# 🏥 Workflow

```
Medical Image (X)
        │
        ▼
MED Prediction
        │
        ▼
Prediction Error Map (P)
        │
        ▼
Hybrid Tree Coding (HTC)
        │
        ▼
Count Encryption (CE)
        │
        ▼
Reserved Room Generation
        │
        ▼
Bit Replacement (Data Hiding)
        │
        ▼
Marked Encrypted Image (Z)
        │
        ▼
Payload Extraction
        │
        ▼
Perfect Image Recovery
```

---

# ✨ Features

- MED Prediction based prediction error generation
- Huffman Coding (HC)
- Leaf-to-Leaf Coding (LLC)
- Hybrid Tree Coding (HTC)
- Count Encryption (CE)
- Reserved Room Generation
- Bit Replacement based reversible data hiding
- Secure payload embedding
- Exact payload extraction
- Perfect original image recovery

---

# 🛠 Technologies Used

- Python
- NumPy
- OpenCV
- Matplotlib
- Scikit-image
- Pillow
- Medical Image Processing
- Data Compression
- Cryptography

---

# 📊 Experimental Results

| Metric | Value |
|---------|------:|
| HC Blocks | 1 |
| LLC Blocks | 4095 |
| Coding Stream Length | 717,713 bits |
| Reserved Room | 1,377,394 bits |
| Embedding Capacity | **1,377,394 bits** |
| Embedding Rate | **5.2543 bpp** |
| PSNR (Original vs Encrypted) | **6.5446 dB** |
| PSNR (Original vs Marked Encrypted) | **6.5462 dB** |
| Entropy | **7.9994** |
| Payload Recovery | ✅ 100% |
| Image Recovery | ✅ 100% |

---

# 📂 Dataset

The implementation was evaluated using publicly available medical image datasets from Kaggle.

### SIIM Medical Images (CT Images)

https://www.kaggle.com/datasets/kmader/siim-medical-images

### Brain MRI Images for Brain Tumor Detection

https://www.kaggle.com/datasets/navoneel/brain-mri-images-for-brain-tumor-detection

### Labeled Chest X-Ray Images

https://www.kaggle.com/datasets/tolgadincer/labeled-chest-xray-images/data

The datasets include CT, MRI, and Chest X-Ray images to evaluate the proposed framework on different medical imaging modalities.

---

# 📖 Research Paper

This implementation is based on the following IEEE publication:

**Reversible Data Hiding in Encrypted Medical Images Based on Huffman Tree Coding and Count-Encryption**

IEEE Xplore:

https://ieeexplore.ieee.org/document/11125529

---

# 🎯 Applications

- Secure Medical Image Storage
- Hospital Information Systems
- Cloud Healthcare
- Electronic Health Records (EHR)
- Telemedicine
- Medical Image Archiving
- Secure Medical Image Transmission

---

# 🔮 Future Scope

- AI-assisted medical image security
- Blockchain-enabled healthcare systems
- Real-time encrypted image transmission
- IoT healthcare applications
- Multi-user cloud security

---

# 📚 References

1. IEEE Xplore – Reversible Data Hiding in Encrypted Medical Images Based on Huffman Tree Coding and Count-Encryption

https://ieeexplore.ieee.org/document/11125529

2. SIIM Medical Images Dataset

https://www.kaggle.com/datasets/kmader/siim-medical-images

3. Brain MRI Images for Brain Tumor Detection

https://www.kaggle.com/datasets/navoneel/brain-mri-images-for-brain-tumor-detection

4. Labeled Chest X-Ray Images

https://www.kaggle.com/datasets/tolgadincer/labeled-chest-xray-images/data

---

# 📜 Disclaimer

This repository contains an independent academic implementation developed for educational and research purposes. It is inspired by the referenced IEEE publication. For complete theoretical details, please refer to the original paper.

---

# 👨‍💻 Author

**Krish Gupta**

Research Interests:
Medical Image Processing • Computer Vision • Cryptography • Data Compression • Artificial Intelligence
