"""
Streamlit web interface for the firmware forensics toolkit.
Day 8: file upload + analysis trigger + summary cards.
Day 9: per-layer tabs (FR-8).
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


def get_new_yara_matches(results):
    """Returns only YARA matches that are new in suspicious (not present in
    original), matching the same comparative logic used in scoring.py."""
    original_signatures = set()
    for file_path, matches in results["yara_original"].items():
        for match in matches:
            original_signatures.add((file_path, match["rule_name"]))

    new_matches = []
    for file_path, matches in results["yara_suspicious"].items():
        for match in matches:
            signature = (file_path, match["rule_name"])
            if signature in original_signatures:
                continue
            new_matches.append({
                "Dosya": file_path,
                "Kural": match["rule_name"],
                "Risk": match["risk"],
                "Açıklama": match["description"],
            })
    return new_matches


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

    st.session_state["last_results"] = results
    st.session_state["last_findings"] = findings
    st.session_state["last_score"] = score

if "last_score" in st.session_state:
    st.divider()
    score = st.session_state["last_score"]
    findings = st.session_state["last_findings"]
    results = st.session_state["last_results"]

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

    st.divider()

    tab_static, tab_entropy, tab_yara, tab_permission = st.tabs(
        ["Statik Bütünlük", "Entropi Analizi", "YARA Tarama", "İzin/Yetki Analizi"]
    )

    with tab_static:
        static_result = results["static"]
        st.write(f"**Eklenen dosyalar** ({len(static_result['added_files'])})")
        if static_result["added_files"]:
            st.table({"Dosya": static_result["added_files"]})
        else:
            st.caption("Bulgu yok.")

        st.write(f"**Değiştirilen dosyalar** ({len(static_result['modified_files'])})")
        if static_result["modified_files"]:
            st.table({"Dosya": static_result["modified_files"]})
        else:
            st.caption("Bulgu yok.")

        st.write(f"**Silinen dosyalar** ({len(static_result['deleted_files'])})")
        if static_result["deleted_files"]:
            st.table({"Dosya": static_result["deleted_files"]})
        else:
            st.caption("Bulgu yok.")

    with tab_entropy:
        entropy_result = results["entropy"]
        changed = entropy_result["changed_entropy_files"]
        new_files = entropy_result["new_suspicious_files"]

        st.write(f"**Entropisi değişen dosyalar** ({len(changed)})")
        if changed:
            st.table({"Dosya": list(changed.keys()), "Değişim": list(changed.values())})
        else:
            st.caption("Bulgu yok.")

        st.write(f"**Yeni yüksek entropili dosyalar** ({len(new_files)})")
        if new_files:
            st.table({"Dosya": new_files})
        else:
            st.caption("Bulgu yok.")

    with tab_yara:
        yara_matches = get_new_yara_matches(results)
        st.write(f"**Yeni YARA eşleşmeleri** ({len(yara_matches)})")
        if yara_matches:
            st.table(yara_matches)
        else:
            st.caption("Bulgu yok.")

    with tab_permission:
        permission_result = results["permission"]
        new_suid = permission_result["new_suid_or_sgid_files"]
        changed_perms = permission_result["permission_changes"]

        st.write(f"**Yeni SUID/SGID dosyaları** ({len(new_suid)})")
        if new_suid:
            st.table({
                "Dosya": list(new_suid.keys()),
                "İzin": [v["filemode"] for v in new_suid.values()],
            })
        else:
            st.caption("Bulgu yok.")

        st.write(f"**İzin değişiklikleri** ({len(changed_perms)})")
        if changed_perms:
            st.table({"Dosya": list(changed_perms.keys())})
        else:
            st.caption("Bulgu yok.")

    st.info("Zaman çizelgesi ve delil zinciri görünümü yakında eklenecek.")