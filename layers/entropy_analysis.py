"""
Entropi Analizi Katmanı (Entropy Analysis Layer)
Dosyaları sabit boyutlu bloklara bölüp her bloğun Shannon entropi değerini hesaplar.
Yüksek entropili bölgeler şifrelenmiş/gizlenmiş kod şüphesi taşır.
"""

import math
import os
from collections import Counter

# Bir bloğun "şüpheli" sayılması için eşik değer (0-8 arası, 8 = maksimum rastgelelik)
ENTROPY_THRESHOLD = 6.8
BLOCK_SIZE = 256  # byte


def calculate_entropy(data):
    """Verilen byte dizisinin Shannon entropi değerini hesaplar (0-8 arası)."""
    if not data:
        return 0.0

    byte_counts = Counter(data)
    length = len(data)
    entropy = 0.0

    for count in byte_counts.values():
        probability = count / length
        entropy -= probability * math.log2(probability)

    return entropy


def analyze_file_entropy(file_path, block_size=BLOCK_SIZE):
    """Bir dosyayı bloklara böler, her bloğun entropisini hesaplar.
    Dönen değer: [{block_index, offset, entropy, suspicious}, ...] listesi
    """
    results = []
    with open(file_path, "rb") as f:
        block_index = 0
        while True:
            block = f.read(block_size)
            if not block:
                break
            entropy = calculate_entropy(block)
            results.append({
                "block_index": block_index,
                "offset": block_index * block_size,
                "entropy": round(entropy, 3),
                "suspicious": entropy >= ENTROPY_THRESHOLD,
            })
            block_index += 1
    return results


def scan_directory_entropy(directory_path):
    """Bir dizindeki tüm dosyalar için entropi analizini çalıştırır.
    Dönen değer: {göreli_dosya_yolu: [blok sonuçları]} sözlüğü
    """
    all_results = {}
    for root, _, files in os.walk(directory_path):
        for filename in files:
            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, directory_path)
            all_results[relative_path] = analyze_file_entropy(full_path)
    return all_results


def summarize_suspicious_blocks(scan_results):
    """Şüpheli (yüksek entropili) blokları dosya bazında özetler."""
    summary = {}
    for file_path, blocks in scan_results.items():
        suspicious_blocks = [b for b in blocks if b["suspicious"]]
        if suspicious_blocks:
            summary[file_path] = {
                "total_blocks": len(blocks),
                "suspicious_block_count": len(suspicious_blocks),
                "suspicious_offsets": [b["offset"] for b in suspicious_blocks],
                "max_entropy": max(b["entropy"] for b in blocks),
            }
    return summary


if __name__ == "__main__":
    print("=== Entropi Analizi: data/original ===")
    original_results = scan_directory_entropy("data/original")
    original_summary = summarize_suspicious_blocks(original_results)
    print(f"Şüpheli dosya sayısı: {len(original_summary)}")
    for file_path, info in original_summary.items():
        print(f"  {file_path}: {info}")

    print("\n=== Entropi Analizi: data/suspicious ===")
    suspicious_results = scan_directory_entropy("data/suspicious")
    suspicious_summary = summarize_suspicious_blocks(suspicious_results)
    print(f"Şüpheli dosya sayısı: {len(suspicious_summary)}")
    for file_path, info in suspicious_summary.items():
        print(f"  {file_path}: {info}")