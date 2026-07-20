"""Test amaçlı yüksek entropili (rastgele) bir dosya üretir."""
import os

os.makedirs("data/suspicious", exist_ok=True)

# Rastgele byte'lardan oluşan "şifrelenmiş kod" simülasyonu
random_data = os.urandom(2048)  # 2 KB rastgele veri

with open("data/suspicious/hidden_payload.bin", "wb") as f:
    f.write(random_data)

print("data/suspicious/hidden_payload.bin oluşturuldu (yüksek entropili test dosyası)")