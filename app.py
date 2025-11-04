from flask import Flask, render_template, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

DATA_FILE = "asn_dummy_500.json"


# -----------------------------
# RENDER HALAMAN UTAMA
# -----------------------------
@app.route("/rekomendasi-ai")
def rekomendasi_ai():
    if not os.path.exists(DATA_FILE):
        return "<h2 style='color:red;'>❌ File data belum ditemukan. Jalankan generator dulu.</h2>"

    df = pd.read_json(DATA_FILE, encoding="utf-8")

    # Ambil semua jabatan tujuan unik untuk dropdown
    jabatan_options = sorted(df["jabatan_tujuan"].unique().tolist())

    return render_template(
        "rekomendasi-ai.html",
        title="Rekomendasi AI",
        jabatan_options=jabatan_options,
    )


# -----------------------------
# API UNTUK AJAX
# -----------------------------
@app.route("/api/rekomendasi-data")
def api_rekomendasi_data():
    if not os.path.exists(DATA_FILE):
        return jsonify({"error": "File data tidak ditemukan"}), 404

    df = pd.read_json(DATA_FILE, encoding="utf-8")

    jabatan = request.args.get("jabatan")

    # Jika user pilih "Semua Data"
    if jabatan == "Semua Data" or jabatan is None:
        kandidat = df.copy()
    else:
        kandidat = df[df["jabatan_tujuan"] == jabatan]

    kandidat = kandidat.sort_values(
        by=["potensi_promosi", "skor_kinerja"], ascending=False
    ).head(500)

    kandidat_list = kandidat[
        [
            "nama",
            "unit_kerja",
            "jabatan_saat_ini",
            "jabatan_tujuan",
            "nilai_skp",
            "skor_kinerja",
            "potensi_promosi",
        ]
    ].to_dict(orient="records")

    return jsonify(kandidat_list)


@app.route("/api/rekomendasi-chart")
def api_rekomendasi_chart():
    if not os.path.exists(DATA_FILE):
        return jsonify({"error": "File data tidak ditemukan"}), 404

    df = pd.read_json(DATA_FILE, encoding="utf-8")
    jabatan = request.args.get("jabatan")

    if jabatan == "Semua Data" or jabatan is None:
        kandidat = df.copy()
    else:
        kandidat = df[df["jabatan_tujuan"] == jabatan]

    kandidat = kandidat.sort_values(
        by=["potensi_promosi", "skor_kinerja"], ascending=False
    ).head(10)

    if kandidat.empty:
        return jsonify([])

    kandidat_list = kandidat.to_dict(orient="records")

    chart_data = []
    for k in kandidat_list:
        chart_data.append(
            {
                "label": k["nama"],
                "data": [
                    k["kompetensi_teknis"] * 100,
                    k["kompetensi_manajerial"] * 100,
                    k["kompetensi_sosial_kultural"] * 100,
                    k["nilai_skp"],
                    k["skor_kinerja"] / 2,
                    k["potensi_promosi"] * 100,
                ],
                "color": "#6366F1" if len(chart_data) == 0 else "#9333EA",
            }
        )
    return jsonify(chart_data)


# -----------------------------
# HALAMAN LAIN (TETAP)
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html", title="Home")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", title="Dashboard")


@app.route("/data-asn")
def data_asn():
    return render_template("data-asn.html", title="Data ASN")


@app.route("/statistik")
def statistik():
    return render_template("statistik.html", title="Statistik")


@app.route("/api/statistik")
def api_statistik():
    json_file = "asn_dummy_500.json"
    if not os.path.exists(json_file):
        return jsonify({"error": "File asn_dummy_500.json tidak ditemukan."}), 404

    df = pd.read_json(json_file, encoding="utf-8")

    # ---- 1. Distribusi Jabatan (Top 10) ----
    jabatan_counts = df["jabatan_saat_ini"].value_counts().head(10)

    # ---- 2. Distribusi Unit Kerja (Top 10) ----
    unit_counts = df["unit_kerja"].value_counts().head(10)

    # ---- 3. Tren Efisiensi & Motivasi (simulasi 2022–2025) ----
    trend = {
        "years": ["2022", "2023", "2024", "2025"],
        "efisiensi": [
            round(df["potensi_promosi"].mean() * 100 * 0.8, 2),
            round(df["potensi_promosi"].mean() * 100 * 0.9, 2),
            round(df["potensi_promosi"].mean() * 100, 2),
            round(df["potensi_promosi"].mean() * 100 * 1.1, 2),
        ],
        "motivasi": [
            round(df["skor_kinerja"].mean() / 2 * 0.8, 2),
            round(df["skor_kinerja"].mean() / 2 * 0.9, 2),
            round(df["skor_kinerja"].mean() / 2, 2),
            round(df["skor_kinerja"].mean() / 2 * 1.1, 2),
        ],
    }

    # ---- 4. Pemetaan Kompetensi Nasional ----
    kompetensi_means = {
        "kompetensi_teknis": round(df["kompetensi_teknis"].mean() * 100, 2),
        "kompetensi_manajerial": round(df["kompetensi_manajerial"].mean() * 100, 2),
        "kompetensi_sosial_kultural": round(
            df["kompetensi_sosial_kultural"].mean() * 100, 2
        ),
    }

    # ---- 5. Top 10 Jabatan dengan Potensi Promosi Tertinggi ----
    top_promotion = (
        df.groupby("jabatan_saat_ini")["potensi_promosi"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .apply(lambda x: round(x * 100, 2))
    )

    # ---- 6. Distribusi Sertifikasi (kategori dari kolom 'sertifikasi') ----
    sertifikasi_counts = df["sertifikasi"].value_counts().head(6)

    # ---- 7. Scatter Points (Nilai SKP vs Skor Kinerja) ----
    scatter_points = [
        {"x": float(row["nilai_skp"]), "y": float(row["skor_kinerja"])}
        for _, row in df.sample(n=min(100, len(df))).iterrows()
    ]

    # ---- 8. Statistik Nasional Summary ----
    summary = {
        "total_asn": len(df),
        "avg_potensi": round(df["potensi_promosi"].mean() * 100, 1),
        "avg_kinerja": round(df["skor_kinerja"].mean(), 1),
        "avg_skp": round(df["nilai_skp"].mean(), 1),
    }

    return jsonify(
        {
            "jabatan_counts": jabatan_counts.to_dict(),
            "unit_counts": unit_counts.to_dict(),
            "trend": trend,
            "kompetensi_means": kompetensi_means,
            "top_promotion": top_promotion.to_dict(),
            "sertifikasi_counts": sertifikasi_counts.to_dict(),
            "scatter_points": scatter_points,
            "summary": summary,
        }
    )


@app.route("/profil")
def profil():
    return render_template("profil.html", title="Profil")


@app.route("/login")
def login():
    return render_template("login.html", title="Login")


if __name__ == "__main__":
    app.run(debug=True)
