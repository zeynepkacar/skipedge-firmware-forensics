"""Generates a high-entropy (random) file for testing purposes."""
import os

os.makedirs("data/suspicious", exist_ok=True)

# Simulates "encrypted code" made of random bytes
random_data = os.urandom(2048)  # 2 KB of random data

with open("data/suspicious/hidden_payload.bin", "wb") as f:
    f.write(random_data)

print("data/suspicious/hidden_payload.bin created (high-entropy test file)")