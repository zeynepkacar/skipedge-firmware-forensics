"""
Report Generator
Builds a self-contained HTML report summarizing the analysis results,
including the suspicion score, per-layer findings, and the chain of custody
timeline. The HTML file can be opened directly or printed to PDF from a
browser.
"""
from datetime import datetime, timezone


def _rows(items, columns):
    """Builds HTML table rows from a list of dicts."""
    rows_html = ""
    for item in items:
        cells = "".join(f"<td>{item.get(col, '')}</td>" for col in columns)
        rows_html += f"<tr>{cells}</tr>"
    return rows_html


def build_html_report(score, risk_label, findings, timeline, integrity_ok):
    """Builds a complete HTML report string."""
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    findings_rows = "".join(
        f"<tr><td>{f['layer']}</td><td>{f['file']}</td><td>{f['type']}</td><td>+{f['points']}</td></tr>"
        for f in findings
    )

    timeline_rows = "".join(
        f"<tr><td>{e['event_id']}</td><td>{e['layer']}</td><td>{e['file']}</td>"
        f"<td>{e['finding_type']}</td><td>+{e['points']}</td>"
        f"<td><code>{e['evidence_hash']}</code></td></tr>"
        for e in timeline
    )

    integrity_text = (
        "Doğrulandı - bu rapordaki bulgu kayıtları araç tarafından üretildiği haliyle duruyor, sonradan değiştirilmemiş (bu, firmware'in güvenli olduğu anlamına gelmez, sadece kayıtların tahrif edilmediğini gösterir)"
        if integrity_ok
        else "BAŞARISIZ - bir veya daha fazla kayıt sonradan değiştirilmiş olabilir"
    )

    integrity_color = "#1a7f37" if integrity_ok else "#cf222e"

    html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>Firmware Bütünlük Analiz Raporu</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 40px; color: #1f2328; }}
  h1 {{ border-bottom: 2px solid #1f2328; padding-bottom: 8px; }}
  h2 {{ margin-top: 32px; }}
  table {{ border-collapse: collapse; width: 100%; margin-top: 8px; }}
  th, td {{ border: 1px solid #d0d7de; padding: 6px 10px; text-align: left; font-size: 13px; }}
  th {{ background-color: #f6f8fa; }}
  .score-box {{ display: inline-block; padding: 16px 24px; border-radius: 8px; background: #f6f8fa; margin-right: 16px; }}
  .integrity {{ font-weight: bold; color: {integrity_color}; }}
  code {{ font-size: 11px; }}
</style>
</head>
<body>
  <h1>Firmware Bütünlük İhlali Tespit Raporu</h1>
  <p>Oluşturulma zamanı: {generated_at}</p>

  <div class="score-box"><strong>Şüphe Skoru:</strong> {score}/100</div>
  <div class="score-box"><strong>Risk Seviyesi:</strong> {risk_label}</div>
  <div class="score-box"><strong>Toplam Bulgu:</strong> {len(findings)}</div>

<h2>Rapor Kayıtlarının Bütünlüğü (Delil Zinciri)</h2>
  <p class="integrity">{integrity_text}</p>

  <h2>Bulgular (Katman Bazlı)</h2>
  <table>
    <tr><th>Katman</th><th>Dosya</th><th>Bulgu Türü</th><th>Puan</th></tr>
    {findings_rows if findings_rows else '<tr><td colspan="4">Bulgu yok.</td></tr>'}
  </table>

  <h2>Zaman Çizelgesi ve Delil Hash'leri</h2>
  <table>
    <tr><th>Sıra</th><th>Katman</th><th>Dosya</th><th>Bulgu Türü</th><th>Puan</th><th>SHA-256 Delil Hash'i</th></tr>
    {timeline_rows if timeline_rows else '<tr><td colspan="6">Kayıt yok.</td></tr>'}
  </table>

  <hr style="margin-top: 40px;">
  <p style="font-size: 12px; color: #57606a;">
    Bu rapor, Spikedge staj projesi kapsamında geliştirilen çok katmanlı
    firmware bütünlük ihlali tespit aracı tarafından otomatik olarak
    üretilmiştir.
  </p>
</body>
</html>"""

    return html