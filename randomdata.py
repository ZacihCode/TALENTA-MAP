import pandas as pd
import numpy as np
import random
import json

# -----------------------------
# KONFIGURASI DASAR
# -----------------------------
JABATAN_LIST = [
    "Analis Kepegawaian", "Pranata Komputer", "Verifikator Keuangan",
    "Statistisi", "Auditor", "Perencana", "Analis Data",
    "Pengelola Barang Milik Negara", "Arsiparis", "Penyusun Laporan Keuangan",
    "Pranata Humas", "Penyusun Program", "Analis SDM Aparatur",
    "Penyusun Rencana Kinerja", "Analis Kebijakan"
]

JABATAN_TUJUAN_LIST = [
    "Kepala Subbagian Kepegawaian", "Koordinator TI Instansi",
    "Kepala Seksi Keuangan", "Kepala Bagian Perencanaan",
    "Koordinator Evaluasi Program", "Kepala Subbagian Umum",
    "Kepala Seksi Perbendaharaan", "Koordinator Pengembangan SDM",
    "Kepala Seksi Data dan Informasi"
]

UNIT_KERJA_LIST = [
    "Badan Kepegawaian Daerah", "Bappeda", "Dinas Pendidikan",
    "Inspektorat Daerah", "Kementerian PANRB", "Dinas Kominfo",
    "Sekretariat Daerah", "Dinas Kesehatan", "Badan Pusat Statistik"
]

SERTIFIKASI_LIST = [
    "Diklatpim III; Manajemen ASN", "Pelatihan Kepemimpinan",
    "Pelatihan SPBE", "Diklat Analisis Jabatan", "Diklat Pengadaan Barang/Jasa",
    "Diklat Kepemimpinan Pengawas", "Manajemen Risiko", "Analisis Data Pemerintahan"
]

# -----------------------------
# FUNGSI PEMBUAT DATA
# -----------------------------
def generate_asn_data(n=500):
    np.random.seed(42)
    data = []

    for i in range(1, n+1):
        nama = f"{random.choice(['Andi','Budi','Citra','Dewi','Eko','Farhan','Gita','Hendra','Ika','Joko','Kusuma','Lina','Mega','Nanda','Putra','Rizki','Sari','Taufik','Utami','Wahyu'])} {random.choice(['Saputra','Wijaya','Putri','Santoso','Halim','Siregar','Pratama','Kurniawan','Nasution','Sihombing','Hartono','Syahrul','Fadillah'])}"
        jabatan = random.choice(JABATAN_LIST)
        jabatan_tujuan = random.choice(JABATAN_TUJUAN_LIST)
        unit_kerja = random.choice(UNIT_KERJA_LIST)
        masa_kerja = np.clip(int(np.random.normal(10, 5)), 1, 30)
        nilai_skp = round(np.clip(np.random.normal(85, 7), 70, 100), 2)
        sertifikasi = random.choice(SERTIFIKASI_LIST)
        kompetensi_teknis = round(random.uniform(0.5, 1.0), 2)
        kompetensi_manajerial = round(random.uniform(0.5, 1.0), 2)
        kompetensi_sosial = round(random.uniform(0.5, 1.0), 2)
        riwayat_diklat = random.randint(1, 10)

        # Hitung skor_kinerja rata-rata
        skor_kinerja = round((nilai_skp * 0.6) + (kompetensi_teknis + kompetensi_manajerial + kompetensi_sosial) * 15, 2)

        # Tentukan potensi promosi (korelasi logis)
        base = (kompetensi_teknis + kompetensi_manajerial + kompetensi_sosial) / 3
        potensi_promosi = np.clip(
            (0.4 * base) + (0.3 * (nilai_skp / 100)) + (0.2 * (skor_kinerja / 100)) + (0.1 * (masa_kerja / 30)),
            0, 1
        )
        potensi_promosi = round(potensi_promosi, 2)

        data.append({
            "id": i,
            "nama": nama,
            "jabatan_saat_ini": jabatan,
            "jabatan_tujuan": jabatan_tujuan,
            "unit_kerja": unit_kerja,
            "masa_kerja_tahun": masa_kerja,
            "nilai_skp": nilai_skp,
            "sertifikasi": sertifikasi,
            "kompetensi_teknis": kompetensi_teknis,
            "kompetensi_manajerial": kompetensi_manajerial,
            "kompetensi_sosial_kultural": kompetensi_sosial,
            "riwayat_diklat": riwayat_diklat,
            "skor_kinerja": skor_kinerja,
            "potensi_promosi": potensi_promosi
        })

    df = pd.DataFrame(data)
    return df

# -----------------------------
# MAIN EXECUTION
# -----------------------------
if __name__ == "__main__":
    n = int(input("Masukkan jumlah data ASN dummy (misal 500): ") or 500)
    df = generate_asn_data(n)

    # Simpan CSV
    csv_file = f"asn_dummy_{n}.csv"
    df.to_csv(csv_file, index=False, encoding="utf-8-sig")

    # Simpan JSON
    json_file = f"asn_dummy_{n}.json"
    df.to_json(json_file, orient="records", indent=2, force_ascii=False)

    print(f"✅ Dataset berhasil dibuat: {csv_file} & {json_file}")
