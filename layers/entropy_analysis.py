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

def compare_entropy(original_dir, suspicious_dir):
    """İki firmware'i karşılaştırır, ortak dosyalarda entropi değişimini tespit eder."""
    original_results = scan_directory_entropy(original_dir)
    suspicious_results = scan_directory_entropy(suspicious_dir)

    common_files = set(original_results.keys()) & set(suspicious_results.keys())
    only_in_suspicious = set(suspicious_results.keys()) - set(original_results.keys())

    entropy_changes = {}

    # Ortak dosyalarda entropi profili değişmiş mi?
    for file_path in common_files:
        orig_blocks = original_results[file_path]
        susp_blocks = suspicious_results[file_path]
        if len(orig_blocks) != len(susp_blocks):
            entropy_changes[file_path] = "boyut değişti, blok sayısı farklı"
            continue
        orig_avg = sum(b["entropy"] for b in orig_blocks) / len(orig_blocks) if orig_blocks else 0
        susp_avg = sum(b["entropy"] for b in susp_blocks) / len(susp_blocks) if susp_blocks else 0
        if abs(orig_avg - susp_avg) > 0.5:  # anlamlı bir sapma
            entropy_changes[file_path] = f"ortalama entropi {orig_avg:.2f} -> {susp_avg:.2f}"

    # Sadece şüpheli tarafta olan YENİ dosyalar (asıl önemli olan burası)
    new_high_entropy_files = {
        f: suspicious_results[f]
        for f in only_in_suspicious
        if any(b["suspicious"] for b in suspicious_results[f])
    }

    return {
        "changed_entropy_files": entropy_changes,
        "new_suspicious_files": list(new_high_entropy_files.keys()),
    }        
if __name__ == "__main__":
    print("=== Karşılaştırmalı Entropi Analizi: original vs suspicious ===")
    comparison = compare_entropy("data/original", "data/suspicious")
    print(f"Entropisi değişen ortak dosyalar: {comparison['changed_entropy_files']}")
    print(f"Sadece suspicious'ta olan yüksek entropili yeni dosyalar: {comparison['new_suspicious_files']}")
