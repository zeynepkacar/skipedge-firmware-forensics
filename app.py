"""
Streamlit web interface for the firmware forensics toolkit.
Day 8: file upload + analysis trigger + summary cards.
"""
import os
import shutil
import tempfile
import gzip

import streamlit as st

from layers.scoring import run_all_layers, build_findings_and_score
from data.extract_squashfs import extract_and_save_permissions

st.set_page_config(page_title="Firmware Forensics Toolkit", layout="wide")

st.title("Firmware Bütünlük İhlali Tespit Aracı")
st.caption("Çok katmanlı adli bilişim analiz sistemi — Spikedge staj projesi")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Orijinal Firmware")
    original_file = st.file_uploader(
        "Squashfs imajı yükleyin (.img veya .img.gz)",
        type=["img", "gz"],
        key="original_upload",
    )

with col2:
    st.subheader("Şüpheli Firmware")
    suspicious_file = st.file_uploader(
        "Squashfs imajı yükleyin (.img veya .img.gz)",
        type=["img", "gz"],
        key="suspicious_upload",
    )

analyze_clicked = st.button(
    "Analizi Başlat",
    type="primary",
    disabled=not (original_file and suspicious_file),
)


def save_and_prepare(uploaded_file, work_dir, label):
    """Saves an uploaded file, decompresses if needed, and extracts it."""
    raw_path = os.path.join(work_dir, f"{label}_raw")
    with open(raw_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    img_path = raw_path
    if uploaded_file.name.endswith(".gz"):
        img_path = raw_path + ".img"
        with gzip.open(raw_path, "rb") as f_in:
            with open(img_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

    extract_dir = os.path.join(work_dir, label)
    manifest_path = os.path.join(work_dir, f"{label}_permissions.json")
    extract_and_save_permissions(img_path, extract_dir, manifest_path)

    return extract_dir, manifest_path


if analyze_clicked:
    with st.spinner("Analiz çalışıyor, bu birkaç dakika sürebilir..."):
        with tempfile.TemporaryDirectory() as work_dir:
            original_dir, original_manifest = save_and_prepare(
                original_file, work_dir, "original"
            )
            suspicious_dir, suspicious_manifest = save_and_prepare(
                suspicious_file, work_dir, "suspicious"
            )

            results = run_all_layers(
                original_dir, suspicious_dir, original_manifest, suspicious_manifest
            )
            findings, score = build_findings_and_score(results)

    st.session_state["last_findings"] = findings
    st.session_state["last_score"] = score

if "last_score" in st.session_state:
    st.divider()
    score = st.session_state["last_score"]
    findings = st.session_state["last_findings"]

    if score >= 70:
        risk_label, risk_color = "Yüksek Risk", "red"
    elif score >= 35:
        risk_label, risk_color = "Orta Risk", "orange"
    else:
        risk_label, risk_color = "Düşük Risk", "green"

    summary_col1, summary_col2, summary_col3 = st.columns(3)
    summary_col1.metric("Şüphe Skoru", f"{score}/100")
    summary_col2.metric("Toplam Bulgu", len(findings))
    summary_col3.markdown(f"### :{risk_color}[{risk_label}]")

    st.info("Katman bazlı detaylı görünüm ve zaman çizelgesi yakında eklenecek.")