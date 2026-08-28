,tajudin,tajudin-ThinkPad-X230,28.08.2026 23:30,file:///home/tajudin/.config/libreoffice/4;


import os
import json
import time
import shutil
import requests
import re
import webbrowser
import subprocess
import datetime
import logging 
from scan_album import scan_album
from deep_translator import GoogleTranslator
from googletrans import Translator


# --- WARNA ---
HIJAU = "\033[92m"
KUNING = "\033[93m"
MERAH = "\033[91m"
CYAN = "\033[96m"
PUTIH = "\033[97m"
BIRU = "\033[94m"
OREN = "\033[38;5;214m"
UNGU = "\033[95m"
KELABU = "\033[38;2;192;192;192m"
RESET = "\033[0m"

# --- TETAPAN ---
FOLDER = "data"

# ---PRIVACY PASSWORD---
PASSWORD_RAHSIA = os.environ.get("BOT_PASSWORD")
GROQ_API_KEY = "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"

def kalkulator():
    os.system("clear")
    print(f"{CYAN}{'='*40}{RESET}")
    print(f"{CYAN}             KALKULATOR{RESET}")
    print(f"{CYAN}{'='*40}{RESET}")
    print(f"{OREN}  Operasi: + - * / // % **(kuasa){RESET}")
    print(f"{CYAN}{'='*40}{RESET}\n")

    while True:
        ekspresi = input(
            f"{PUTIH}Masukkan pengiraan atau{RESET}{OREN} '0'{RESET}{PUTIH} untuk keluar: {RESET}"
        ).strip()

        if ekspresi.lower() == "0":
            break
        try:
            # Keselamatan — hanya benarkan aksara nombor dan operator
            if any(c not in "0123456789+-*/.() %\t" for c in ekspresi):
                print(f"{OREN}  Input tidak sah.{RESET}\n")
                continue
            hasil = eval(ekspresi)
            print(f"{CYAN}  = {hasil}{RESET}\n")
        except ZeroDivisionError:
            print(f"{OREN}  Ralat: Bahagi dengan sifar!{RESET}\n")
        except Exception:
            print(f"{OREN}  Ralat: Pengiraan tidak sah.{RESET}\n")

def tanya_ai(soalan):
    kata_kompleks = ["analisis", "jelaskan", "mengapa", "bagaimana"]
    guna_besar = len(soalan) > 80 or any(k in soalan.lower() for k in kata_kompleks)

    model = "llama-3.3-70b-versatile" if guna_besar else "llama-3.3-70b-versatile"
    jenis = "Kompleks" if guna_besar else "Ringkas"

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "Jawab dalam Bahasa Melayu Malaysia. Ringkas dan tepat.",
            },
            {"role": "user", "content": soalan},
        ],
    }
    try:
        r = requests.post(url, headers=headers, json=data)
        jawapan = r.json()["choices"][0]["message"]["content"]
        print(f"{KUNING}[{jenis} → {model}]{RESET}")
        return jawapan
    except Exception as e:
        return f"Error: {e}"

# --- SEMUA MENU ---
SEMUA_MENU = {
    "sembang santai.json": "Sembang",
    "nota .json": "Nota",
    "sistem.json": "Sistem",
    "memori.json": "Memori",
    "resepi.json": "Resepi",
    "elektrik.json": "Elektrik",
    "diy.json": "Diy",
    "coding.json": "Coding",
    "botpy.json": "Botpy",
    "Privacy.json": "Privacy",
}
# --- FUNGSI TYPEWRITER ---
def typewriter(teks, delay=0.02):
    for huruf in teks:
        print(huruf, end="", flush=True)
        time.sleep(delay)
    print()

# --- FUNGSI CUACA ---
#def dapatkan_cuaca():
 #   api_key = "eb1307ea5036d16cbb3f0e5a03660b97"
  #  kota = "Sungai Besar"
   # url = f"http://api.openweathermap.org/data/2.5/weather?q={kota}&appid={api_key}&units=metric&lang=id"
    #try:
     #   respon = requests.get(url, timeout=5).json()
      #  temp = respon["main"]["temp"]
       # deskripsi = respon["weather"][0]["description"]
       # return temp, deskripsi
   # except:
       # return 27.7, "Tiada Data"


logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

# --- FUNGSI CUACA ---
def dapatkan_cuaca():
    api_key = "eb1307ea5036d16cbb3f0e5a03660b97"
    kota = "Sungai Besar"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={kota}&appid={api_key}&units=metric&lang=id"
    try:
        respon = requests.get(url, timeout=5).json()
        temp = respon["main"]["temp"]
        deskripsi = respon["weather"][0]["description"]
        logging.info(f"Cuaca berjaya diambil: {temp}°C, {deskripsi}")
        return temp, deskripsi
    except requests.exceptions.Timeout:
        logging.error("Cuaca gagal: API timeout selepas 5 saat")
        return 27.7, "Tiada Data"
    except requests.exceptions.ConnectionError:
        logging.error("Cuaca gagal: Tiada sambungan internet")
        return 27.7, "Tiada Data"
    except KeyError as e:
        logging.error(f"Cuaca gagal: Format respon tidak dijangka, key hilang: {e}")
        return 27.7, "Tiada Data"
    except Exception as e:
        logging.error(f"Cuaca gagal: Ralat tidak dijangka - {e}")
        return 27.7, "Tiada Data"

# 7 - LOGIK WARNA SUHU
def warna_suhu(temp):
    if temp >= 35:
        return f"{MERAH}{temp}°C{RESET}"
    elif 27 <= temp < 35:
        return f"{HIJAU}{temp}°C{RESET}"
    else:
        return f"{KELABU}{temp}°C{RESET}"

# --- BACKUP ---
#def buat_backup():
   # asal = os.getcwd()
   # destinasi = os.path.expanduser("~/Documents/BACKUP_BOT")
   # destinasi_data = os.path.join(destinasi, "data")

   # if not os.path.exists(destinasi):
       # os.makedirs(destinasi)

   # if not os.path.exists(destinasi_data):
       # os.makedirs(destinasi_data)

    # Backup fail .py dan .json folder utama
   # fail_fail = [
       # f for f in os.listdir(asal) if f.endswith(".py") or f.endswith(".json")
   # ] + ["index.html", "viewer.html"]

    # Backup fail dalam folder data/
   # fail_data = []
   # folder_data = os.path.join(asal, "data")
   # if os.path.exists(folder_data):
       # fail_data = [f for f in os.listdir(folder_data) if f.endswith(".json")]

   # jumlah = len(fail_fail) + len(fail_data)
   # print(f"{KUNING}Data Sedang Disimpan... {jumlah} fail...{RESET}")

   # for f in fail_fail:
       # shutil.copy(f, destinasi)
       # print(f"{OREN}> {f} [OK]{RESET}")

   # for f in fail_data:
       # shutil.copy(os.path.join(folder_data, f), destinasi_data)
       # print(f"{OREN}> data/{f} [OK]{RESET}")

   # print(f"{HIJAU}[ OK ] Data Sudah Disimpan di: {destinasi}{RESET}")
   # input(f"{UNGU}Tekan 'ENTER' untuk ke menu utama...{RESET}")

# --- BACKUP ---
def buat_backup():
    asal = os.getcwd()
    destinasi = os.path.expanduser("~/Documents/BACKUP_BOT")
    destinasi_data = os.path.join(destinasi, "data")
    if not os.path.exists(destinasi):
        os.makedirs(destinasi)
    if not os.path.exists(destinasi_data):
        os.makedirs(destinasi_data)

    fail_fail = [
        f for f in os.listdir(asal) if f.endswith(".py") or f.endswith(".json")
    ] + ["index.html", "viewer.html"]

    fail_data = []
    folder_data = os.path.join(asal, "data")
    if os.path.exists(folder_data):
        fail_data = [f for f in os.listdir(folder_data) if f.endswith(".json")]

    jumlah = len(fail_fail) + len(fail_data)
    print(f"{KUNING}Data Sedang Disimpan... {jumlah} fail...{RESET}")
    logging.info(f"Backup bermula: {jumlah} fail dijangka")

    berjaya = 0
    gagal = 0

    for f in fail_fail:
        try:
            shutil.copy(f, destinasi)
            print(f"{OREN}> {f} [OK]{RESET}")
            berjaya += 1
        except FileNotFoundError:
            print(f"{MERAH}> {f} [GAGAL - tidak wujud]{RESET}")
            logging.error(f"Backup gagal untuk {f}: fail tidak wujud")
            gagal += 1
        except PermissionError:
            print(f"{MERAH}> {f} [GAGAL - akses ditolak]{RESET}")
            logging.error(f"Backup gagal untuk {f}: akses ditolak")
            gagal += 1
        except Exception as e:
            print(f"{MERAH}> {f} [GAGAL]{RESET}")
            logging.error(f"Backup gagal untuk {f}: {e}")
            gagal += 1

    for f in fail_data:
        try:
            shutil.copy(os.path.join(folder_data, f), destinasi_data)
            print(f"{OREN}> data/{f} [OK]{RESET}")
            berjaya += 1
        except Exception as e:
            print(f"{MERAH}> data/{f} [GAGAL]{RESET}")
            logging.error(f"Backup gagal untuk data/{f}: {e}")
            gagal += 1

    if gagal == 0:
        print(f"{HIJAU}[ OK ] Data Sudah Disimpan di: {destinasi}{RESET}")
        logging.info(f"Backup selesai: {berjaya} berjaya, 0 gagal")
    else:
        print(f"{MERAH}[ AMARAN ] {gagal} fail gagal dibackup. Semak bot.log{RESET}")
        logging.warning(f"Backup selesai dengan masalah: {berjaya} berjaya, {gagal} gagal")

    input(f"{UNGU}Tekan 'ENTER' untuk ke menu utama...{RESET}")

# --- SEMAK & PULIH FOLDER DATA ---
def semak_folder_data():
    import shutil

    folder_betul = os.path.abspath(FOLDER)
    folder_salah = folder_betul + " "

    # Tiada masalah
    if not os.path.exists(folder_salah):
        return
    fail_json = sorted(
        [f for f in os.listdir(folder_salah) if f.lower().endswith(".json")]
    )

    if not fail_json:
        return

    # Fail log
    log_file = os.path.join(os.path.dirname(__file__), "diagnostic.log")
    with open(log_file, "a", encoding="utf-8") as log:
        log.write("\n" + "=" * 60 + "\n")
        log.write(f"Tarikh : {datetime.datetime.now()}\n")
        log.write(f"Current Directory : {os.getcwd()}\n")
        log.write(f"Folder Betul : {folder_betul}\n")
        log.write(f"Folder Salah : {folder_salah}\n")
        log.write(f"JSON Dijumpai : {len(fail_json)}\n")
        log.write(f"Versi Bot : 2026-07-02\n")
        log.write(f"Versi Bot : {BOT_VERSION}\n")
        log.write("Senarai Fail:\n")
        for f in fail_json:
            log.write(f"  - {f}\n")

    print("\n" + "=" * 55)
    print("⚠️  AMARAN")
    print("=" * 55)
    print(f"Dijumpai {len(fail_json)} fail JSON dalam folder:")
    print(folder_salah)
    print()
    print("Kemungkinan inilah sebab semua nota kelihatan hilang.")
    print()
    print("1. Pulihkan fail sekarang")
    print("2. Keluar tanpa membuat perubahan")
    print("=" * 55)
    pilih = input("Pilihan : ").strip()

    if pilih == "1":
        dipindah = 0
        for fail in fail_json:
            asal = os.path.join(folder_salah, fail)
            destinasi = os.path.join(folder_betul, fail)
            shutil.move(asal, destinasi)
            dipindah += 1
        try:
            os.rmdir(folder_salah)
        except:
            pass
        with open(log_file, "a", encoding="utf-8") as log:
            log.write(f"Tindakan : Pulihkan\n")
            log.write(f"Berjaya Dipindahkan : {dipindah}\n")
            log.write("=" * 60 + "\n")
        print(f"\n✅ {dipindah} fail berjaya dipulihkan.")
        input("\nTekan ENTER untuk meneruskan...")
    else:
        with open(log_file, "a", encoding="utf-8") as log:
            log.write("Tindakan : Tiada perubahan dibuat.\n")
            log.write("=" * 60 + "\n")
        print("\nBot ditutup bagi mengelakkan kehilangan data.")
        exit()

# --- PENGURUSAN DATA ---
def muat_data(nama_fail):
    full_path = os.path.join(FOLDER, nama_fail)
    if not os.path.exists(full_path):
        return {"soalan": {}}
    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)

def simpan_data(nama_fail, data):
    full_path = os.path.join(FOLDER, nama_fail)
    os.makedirs(
        os.path.dirname(full_path) if os.path.dirname(full_path) else FOLDER,
        exist_ok=True,
    )
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- AMBIL ISI NOTA ---
def ambil_isi_nota(nilai):
    if isinstance(nilai, dict):
        return nilai.get("isi", "")
    else:
        return nilai

# --- AMBIL SENARAI IMEJ DARI NOTA ---
def ambil_imej(isi):
    """Cari semua baris [IMEJ]: dalam nota"""
    senarai = []
    for baris in isi.split("\n"):
        baris = baris.strip()
        if baris.startswith("[IMEJ]:"):
            path = baris.replace("[IMEJ]:", "").strip()
            senarai.append(path)
    return senarai

def ambil_muzik(isi):
    senarai = []
    for baris in isi.split("\n"):
        baris = baris.strip()
        if baris.startswith("[MUZIK]:"):
            path = baris.replace("[MUZIK]:", "").strip()
            senarai.append(path)
    return senarai

def ada_tulisan_arab(teks):
    return any('\u0600' <= aksara <= '\u06FF' for aksara in teks)

# --- FUNGSI BUKA NOTA ---
def buka_nota_papar(tajuk_asal, data, nama_fail, balik_fn=None):
    nilai = data["soalan"][tajuk_asal]
    isi = ambil_isi_nota(nilai)
    nota_siap = (
        isi.replace("{HIJAU}", HIJAU)
        .replace("{KUNING}", KUNING)
        .replace("{MERAH}", MERAH)
        .replace("{CYAN}", CYAN)
        .replace("{BIRU}", "\033[94m")
        .replace("{RESET}", RESET)
        .replace("{PUTIH}", PUTIH)
        .replace("{OREN}", OREN)
        .replace("{UNGU}", UNGU)
        .replace("{KELABU}",KELABU)
    )
    final_teks = nota_siap
    os.system("clear")
    print(f"{HIJAU}=== {tajuk_asal.upper()} ==={RESET}\n")
    if nama_fail != "galeri.json":
        if ada_tulisan_arab(final_teks):
            print(final_teks)
        else:
            typewriter(final_teks)
        time.sleep(1)

    # Semak ada imej atau tidak
    senarai_imej = ambil_imej(isi)
    senarai_muzik = ambil_muzik(isi)

    # Bina prompt ikut apa yang ada
    if nama_fail == "galeri.json":
        pilihan_teks = "'ENTER' kembali ke senarai | 'padam album' PADAM SELURUH ALBUM"
    else:
        pilihan_teks = (
            "'ENTER' kembali ke senarai tajuk | 'e'untuk edit nota | 'd' padam nota"
        )
    if senarai_imej:
        pilihan_teks += " | 'i' imej"
    if senarai_muzik:
        pilihan_teks += " | 'm' muzik"

    pilihan = input(f"\n{KUNING}{pilihan_teks}: {RESET}").strip().lower()
    if not pilihan:
        if balik_fn:
            balik_fn()
        return

    # --- EDIT NOTA ---
    if pilihan == "e":
        fail_tmp = "/tmp/bot_edit.txt"
        with open(fail_tmp, "w", encoding="utf-8") as f:
            f.write(isi)
        os.system(f"nano {fail_tmp}")
        with open(fail_tmp, "r", encoding="utf-8") as f:
            isi_baru = f.read().strip()
        if isi_baru and isi_baru != isi:
            if isinstance(nilai, dict):
                data["soalan"][tajuk_asal]["isi"] = isi_baru
            else:
                data["soalan"][tajuk_asal] = isi_baru
            simpan_data(nama_fail, data)
            print(f"\n{HIJAU}✅ Nota berjaya dikemaskini!{RESET}")
            input(f"{KUNING}Tekan 'Enter' untuk kembali..{RESET}")
            if balik_fn:
                balik_fn()
            return
            time.sleep(1)
            os.system("clear")
        else:
            print(f"\n{CYAN}Tiada perubahan.{RESET}")
            time.sleep(1)

    # --- PADAM ---
    elif (nama_fail == "galeri.json" and pilihan == "padam album") or (
        nama_fail != "galeri.json" and pilihan == "d"
    ):
        sahkan = (
            input(
                f"\n{MERAH}Padam '{tajuk_asal}'? Tindakan ini TAK BOLEH UNDO! (y/n): {RESET}"
            )
            .strip()
            .lower()
        )
        if sahkan == "y":
            del data["soalan"][tajuk_asal]
            simpan_data(nama_fail, data)
            print(f"\n{HIJAU}✅ '{tajuk_asal}' berjaya dipadam!{RESET}")
            time.sleep(1)
        else:
            print(f"\n{CYAN}Padam dibatalkan.{RESET}")
            time.sleep(1)
        if balik_fn:
            balik_fn()
        return

    # --- BUKA IMEJ ---
    elif pilihan == "i":
        if not senarai_imej:
            print(f"\n{MERAH}Tiada imej dalam nota ini.{RESET}")
            print(
                f"{KUNING}Tambah imej dengan format: [IMEJ]: /path/ke/imej.jpg{RESET}"
            )
            time.sleep(2)
        elif len(senarai_imej) == 1:
            path = senarai_imej[0]
            if os.path.exists(path):
                print(f"\n{HIJAU}Membuka imej...{RESET}")
                os.system(f"xdg-open '{path}' > /dev/null 2>&1 &")
                time.sleep(1)
                aksi = (
                    input(f"\n{KUNING}'ENTER' kembali | 'd' padam imej ni: {RESET}")
                    .strip()
                    .lower()
                )
                if aksi == "d":
                    sahkan = (
                        input(
                            f"{MERAH}Padam '{os.path.basename(path)}'? (y/n): {RESET}"
                        )
                        .strip()
                        .lower()
                    )
                    if sahkan == "y":
                        try:
                            os.remove(path)
                        except FileNotFoundError:
                            pass
            else:
                print(f"\n{MERAH}❌ Fail tidak dijumpai!{RESET}")
                time.sleep(2)
                buang = (
                    input(f"{KUNING}Nak padam entry ini dari senarai? (y/n): {RESET}")
                    .strip()
                    .lower()
                )
                if buang == "y":
                    baris_baru = [
                        b for b in isi.split("\n") if b.strip() != f"[IMEJ]:{path}"
                    ]
                    data["soalan"][tajuk_asal] = "\n".join(baris_baru)
                    simpan_data(nama_fail, data)
                    print(f"{HIJAU}✅ Entry dipadam dari senarai!{RESET}")
                    time.sleep(1)
        else:
            os.system("clear")
            print(f"{CYAN}=== SENARAI IMEJ ==={RESET}\n")
            lebar = 35
            baris_perlu = (len(senarai_imej) + 3) // 4

            def fmt(idx):
                if idx >= len(senarai_imej):
                    return ""
                nama = os.path.basename(senarai_imej[idx])
                wujud = "✅" if os.path.exists(senarai_imej[idx]) else "❌"
                return f"{idx+1}. {nama} {wujud}"

            for i in range(baris_perlu):
                idx1 = i
                idx2 = i + baris_perlu
                idx3 = i + (baris_perlu * 2)
                idx4 = i + (baris_perlu * 3)
                t1 = fmt(idx1)
                t2 = fmt(idx2)
                t3 = fmt(idx3)
                t4 = fmt(idx4)
                print(
                    f"{HIJAU}{t1:<{lebar}}{RESET} {CYAN}{t2:<{lebar}}{RESET} {KUNING}{t3:<{lebar}}{RESET} {OREN}{t4:<{lebar}}{RESET}"
                )

            print(f"\n{CYAN}Pilih nombor untuk buka | {MERAH}'0' batal{RESET}")
            pilih_imej = input(f"\n{HIJAU}NOMBOR: {RESET}").strip()

            if pilih_imej.isdigit() and pilih_imej != "0":
                idx = int(pilih_imej) - 1
                if 0 <= idx < len(senarai_imej):
                    path = senarai_imej[idx]
                    if os.path.exists(path):
                        print(f"\n{HIJAU}Membuka imej...{RESET}")
                        os.system(f"xdg-open '{path}' > /dev/null 2>&1 &")
                        time.sleep(1)
                        aksi = (
                            input(
                                f"\n{KUNING}'ENTER' kembali | 'd' padam imej ni: {RESET}"
                            )
                            .strip()
                            .lower()
                        )
                        if aksi == "d":
                            sahkan = (
                                input(
                                    f"{MERAH}Padam '{os.path.basename(path)}'? (y/n): {RESET}"
                                )
                                .strip()
                                .lower()
                            )
                            if sahkan == "y":
                                try:
                                    os.remove(path)
                                except FileNotFoundError:
                                    pass
                                baris_baru = [
                                    b
                                    for b in isi.split("\n")
                                    if b.strip() != f"[IMEJ]:{path}"
                                ]
                                data["soalan"][tajuk_asal] = "\n".join(baris_baru)
                                simpan_data(nama_fail, data)
                                print(f"\n{HIJAU}✅ Gambar dipadam!{RESET}")
                                time.sleep(1)
                    else:
                        print(f"\n{MERAH}❌ Fail tidak dijumpai!{RESET}")
                        time.sleep(2)
                        buang = (
                            input(f"{KUNING}Nak padam entry ini? (y/n): {RESET}")
                            .strip()
                            .lower()
                        )
                        if buang == "y":
                            baris_baru = [
                                b
                                for b in isi.split("\n")
                                if b.strip() != f"[IMEJ]:{path}"
                            ]
                            data["soalan"][tajuk_asal] = "\n".join(baris_baru)
                            simpan_data(nama_fail, data)
                            print(f"{HIJAU}✅ Entry dipadam!{RESET}")
                            time.sleep(1)

       # --- BUKA MUZIK ---
    elif pilihan == "m":
        if not senarai_muzik:
            print(f"\n{MERAH}Tiada muzik dalam nota ini.{RESET}")
            print(f"{KUNING}Tambah muzik dengan format: [MUZIK]: /path/lagu.mp3{RESET}")
            time.sleep(2)
        elif len(senarai_muzik) == 1:
            path = senarai_muzik[0]
            if os.path.exists(path):
                print(f"\n{HIJAU}Memainkan muzik...{RESET}")
                os.system(f"xdg-open '{path}' > /dev/null 2>&1 &")
                time.sleep(1)
            else:
                print(f"\n{MERAH}Fail tidak dijumpai: {path}{RESET}")
                time.sleep(2)
        else:
            os.system("clear")
            print(f"{CYAN}=== SENARAI MUZIK ==={RESET}\n")
            for i, path in enumerate(senarai_muzik, 1):
                nama = os.path.basename(path)
                wujud = (
                    f"{HIJAU}✅{RESET}" if os.path.exists(path) else f"{MERAH}❌{RESET}"
                )
                print(f"  {i}. {nama}  {wujud}")
            pilih_m = input(f"\n{HIJAU}NOMBOR: {RESET}").strip()
            if pilih_m.isdigit() and pilih_m != "0":
                idx = int(pilih_m) - 1
                if 0 <= idx < len(senarai_muzik):
                    path = senarai_muzik[idx]
                    if os.path.exists(path):
                        os.system(f"xdg-open '{path}' > /dev/null 2>&1 &")
                        time.sleep(1)

    else:
        if balik_fn:
            balik_fn()

# --- SEMAK PASSWORD ---
def semak_password():
    os.system("clear")
    print(f" {HIJAU}[ PRIVACY ]{RESET}")
    print(f" {MERAH}==========={RESET}\n")
    for cuba in range(3):
        pw = input(f"  {OREN}Password: {RESET}").strip()
        if pw == PASSWORD_RAHSIA:
            print(f"\n{HIJAU}✅ Akses Diterima..{RESET}")
            time.sleep(0.8)
            return True
        else:
            baki = 2 - cuba
            if baki > 0:
                print(f"{MERAH}❌ Password salah! {baki} percubaan lagi.{RESET}\n")
            else:
                print(f"{MERAH}❌ Akses Ditolak!{RESET}")
                time.sleep(1.5)
    return False

# google translator

def terjemah_teks(teks, bahasa_dari="ms", bahasa_ke="en"):
    try:
        translator = Translator()
        hasil = translator.translate(teks, src=bahasa_dari, dest=bahasa_ke)
        return hasil.text
    except Exception as e:
        return f"❌ Ralat terjemahan: {e}"
def menu_terjemah():
    print(f"\n{CYAN}=== TERJEMAH TEKS ==={RESET}")
    teks = input("Taip teks nak terjemah: ").strip()
    if not teks:
        print(f"{MERAH}Tiada teks dimasukkan.{RESET}")
        return
    print("Bahasa: 1) MS→EN  2) EN→MS  3) MS→AR  4) Custom")
    pilihan = input("Pilihan: ").strip()
    pasangan = {
        "1": ("ms", "en"),
        "2": ("en", "ms"),
        "3": ("ms", "ar"),
    }
    if pilihan in pasangan:
        dari, ke = pasangan[pilihan]
    elif pilihan == "4":
        dari = input("Kod bahasa asal (contoh: ms): ").strip()
        ke = input("Kod bahasa sasaran (contoh: ja): ").strip()
    else:
        print(f"{MERAH}Pilihan tak sah.{RESET}")
        return
    hasil = terjemah_teks(teks, dari, ke)
    print(f"\n{HIJAU}✅ Hasil terjemahan:{RESET}")
    print(f"{PUTIH}{hasil}{RESET}")
    input(f"\n{KUNING}Tekan 'ENTER'...{RESET}")

# --- CARIAN INDEX ---
def carian_index():
    while True:
        os.system("clear")
        print(f"{KELABU}╔══════════════════════════════════╗{RESET}")
        print(f"{KELABU}║       CARIAN SEMUA INDEX         ║{RESET}")
        print(f"{KELABU}╚══════════════════════════════════╝{RESET}\n")
        kata = (
            input(f"{HIJAU}Kata kunci ({MERAH}'0' untuk keluar{HIJAU}): {RESET}")
            .lower()
            .strip()
        )
        if kata == "0" or not kata:
            break
        hasil = []
        for nm, label_menu in SEMUA_MENU.items():
            if nm == "rahsia.json":
                continue
            data = muat_data(nm)
            if "soalan" not in data:
                continue
            for tajuk in data["soalan"].keys():
                if kata in tajuk.lower():
                    hasil.append((tajuk, nm, label_menu))
        os.system("clear")
        if not hasil:
            print(f"\n{MERAH}Tiada nota dijumpai untuk '{kata}'.{RESET}")
            print(f"{KUNING}Cuba kata kunci lain.{RESET}")
            time.sleep(1.5)
            continue
        print(f"{CYAN}=== HASIL CARIAN: '{kata}' ==={RESET}")
        print(f"{HIJAU}Jumpa {len(hasil)} nota:{RESET}\n")
        lebar = 30
        for i, (tajuk, _, label_menu) in enumerate(hasil, 1):
            print(f"{PUTIH}  {i}. {tajuk:<{lebar}}{CYAN}[{label_menu}]{RESET}")
        print(f"\n{CYAN}Pilih nombor untuk buka nota{RESET}")
        print(f"{MERAH}'0' untuk cari semula | 'q' untuk keluar{RESET}")
        pilihan = input(f"\n{HIJAU}NOMBOR: {RESET}").strip()

        if pilihan == "q":
            break
        if pilihan == "0" or not pilihan:
            continue
        if pilihan.isdigit():
            idx = int(pilihan) - 1
            if 0 <= idx < len(hasil):
                tajuk_dipilih, nama_fail_dipilih, label_dipilih = hasil[idx]
                data = muat_data(nama_fail_dipilih)
                print(f"\n{KUNING}[ {label_dipilih} ]{RESET}")
                buka_nota_papar(tajuk_dipilih, data, nama_fail_dipilih)
            else:
                print(f"{MERAH}Pilihan tidak sah.{RESET}")
                time.sleep(0.8)


# --- CARI DALAM MENU ---
def cari_tajuk(kata_kunci, senarai_tajuk):
    return [t for t in senarai_tajuk if kata_kunci.lower() in t.lower()]

def urus_rak(nama_fail, tajuk):
    data = muat_data(nama_fail)
    if "soalan" not in data:
        data["soalan"] = {}

    def papar_list():
        os.system("clear")
        print(f"{HIJAU}SENARAI TAJUK{RESET}{CYAN} ({tajuk}) {RESET}\n")
        tajuk_list = list(data["soalan"].keys())
        jumlah = len(tajuk_list)
        if jumlah == 0:
            print(f"{KUNING}  (Tiada nota lagi){RESET}\n")
        else:
            baris_perlu = (jumlah + 3) // 4
            lebar = 28

            for i in range(baris_perlu):
                idx1 = i
                t1 = f"{idx1+1}. {tajuk_list[idx1]}" if idx1 < jumlah else ""
                idx2 = i + baris_perlu
                t2 = f"{idx2+1}. {tajuk_list[idx2]}" if idx2 < jumlah else ""
                idx3 = i + (baris_perlu * 2)
                t3 = f"{idx3+1}. {tajuk_list[idx3]}" if idx3 < jumlah else ""
                idx4 = i + (baris_perlu * 3)
                t4 = f"{idx4+1}. {tajuk_list[idx4]}" if idx4 < jumlah else ""
                idx5 = i + (baris_perlu * 4)
                t5 = f"{idx5+1}. {tajuk_list[idx5]}" if idx5 < jumlah else ""

                print(
                    f"{HIJAU}{t1:<{lebar}}{RESET} {CYAN} {t2:<{lebar}}{RESET} {KUNING}{t3:<{lebar}}{RESET}{OREN} {t4:<{lebar}}{RESET}{BIRU} {t5:<{lebar}}{RESET}"
                )

        print(f"\n{CYAN}TEKAN {MERAH}'0'{RESET}{CYAN} UTK KEMBALI MENU UTAMA{RESET}")
        print(f"{HIJAU}JUMLAH NOTA: {RESET}{jumlah}")

    def buka_nota(tajuk_asal):
        buka_nota_papar(tajuk_asal, data, nama_fail, balik_fn=papar_list)

    os.system("clear")
    print(f"=== [ MOD {tajuk.upper()} ] ===")
    papar_list()

    while True:
        user_input = input(f"\n{HIJAU}NOMBOR/TAJUK:{RESET} ").lower().strip()

        if not user_input:
            continue

        if user_input == "0":
            break

        if user_input == "list":
            papar_list()
            continue

        if user_input.isdigit():
            index = int(user_input) - 1
            keys = list(data["soalan"].keys())
            if 0 <= index < len(keys):
                buka_nota(keys[index])
            else:
                print(f"{MERAH}Nombor tak valid!{RESET}")
                time.sleep(0.8)
            continue

        tajuk_list_semua = list(data["soalan"].keys())
        tajuk_lower_semua = [t.lower() for t in tajuk_list_semua]

        if user_input in tajuk_lower_semua:
            idx = tajuk_lower_semua.index(user_input)
            buka_nota(tajuk_list_semua[idx])

        else:
            hasil_carian = cari_tajuk(user_input, tajuk_list_semua)

            if hasil_carian:
                os.system("clear")
                print(f"{CYAN}=== HASIL CARIAN: '{user_input}' ==={RESET}")
                print(
                    f"{HIJAU}Jumpa {len(hasil_carian)} tajuk dalam menu ini:{RESET}\n"
                )

                for i, t in enumerate(hasil_carian, 1):
                    print(f"{PUTIH}  {i}. {t}{RESET}")

                print(f"\n{CYAN}Pilih nombor untuk buka nota{RESET}")
                print(f"{MERAH}Tekan '0' untuk batal{RESET}")

                pilihan = input(f"\n{HIJAU}NOMBOR: {RESET}").strip()

                if pilihan.isdigit() and pilihan != "0":
                    idx = int(pilihan) - 1
                    if 0 <= idx < len(hasil_carian):
                        buka_nota(hasil_carian[idx])
                    else:
                        print(f"{MERAH}Pilihan tidak sah.{RESET}")
                        time.sleep(0.8)

                papar_list()

            else:
                print(f"\n{KUNING}Tajuk '{user_input}' tidak dijumpai.{RESET}")
                print(f"{CYAN}Nak buat nota baru? (y/n): {RESET}", end="")
                sahkan = input().strip().lower()

                if sahkan != "y":
                    print(f"{MERAH}Dibatalkan.{RESET}")
                    time.sleep(0.8)
                    papar_list()
                    continue

                print(f"\n{HIJAU}SILA MASUKKAN DATA ANDA....{RESET}")
                print(f"{KUNING}Taip '.' untuk SIMPAN atau 'C' untuk CANCEL{RESET}\n")

                isi_nota = []
                while True:
                    baris = input()

                    if baris.lower().strip() == "c":
                        isi_nota = []
                        print(f"{MERAH}PENGISIAN DIBATALKAN!{RESET}")
                        time.sleep(1)
                        break
                    if baris.strip() == ".":
                        break
                    isi_nota.append(baris)
                if isi_nota:
                    jawapan = "\n".join(isi_nota)
                    data["soalan"][user_input] = jawapan
                    simpan_data(nama_fail, data)
                    data = muat_data(nama_fail)
                    if "soalan" not in data:
                        data["soalan"] = {}
                    print(f"{HIJAU}✅ BERJAYA DISIMPAN!{RESET}")
                    time.sleep(1)
                else:
                    print(f"{CYAN}Tiada data disimpan.{RESET}")
                    time.sleep(1)

                papar_list()


# --- export nota_py---
FOLDER = "data"
OUTPUT_FOLDER = "export_nota"
SKIP = ["rahsia.json", "privacy.json"]

def export_semua_nota():
    output = ""

    for fail in sorted(os.listdir(FOLDER)):
        if fail in SKIP:
            continue
        if fail.endswith(".json"):
            path = os.path.join(FOLDER, fail)

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            tajuk = fail.replace(".json", "").upper()
            output += f"\n{'='*50}\n"
            output += f"{tajuk}\n"
            output += f"{'='*50}\n\n"

            if "soalan" in data:
                for subtajuk, isi in data["soalan"].items():
                    output += f"\n[ {subtajuk} ]\n"
                    if isinstance(isi, dict):
                        isi_bersih = re.sub(r"\{[A-Z]+\}", "", isi.get("isi", ""))
                    else:
                        isi_bersih = re.sub(r"\{[A-Z]+\}", "", str(isi))
                    output += isi_bersih.replace("\\n", "\n") + "\n"

    with open("export_nota.txt", "w", encoding="utf-8") as f:
        f.write(output)
    print("✅ Nota berjaya diexport ke export_nota.txt")

# --- DASHBOARD UTAMA ---
def main():
    import os
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)
    semak_folder_data()
    while True:
        os.system("clear")
        masa = time.strftime("%I:%M %p")
        temp_cuaca, ket_cuaca = dapatkan_cuaca()
        suhu_cpu = os.popen("sensors | grep 'Core 0' | awk '{print $3}'").read().strip()

        print(
            f"{MERAH} ⬤ {RESET}{KUNING} ⬤ {RESET}{HIJAU} ⬤ {RESET}                                                      {KELABU}31012026{RESET}\n"
        )
        print(
            f"                                         {KUNING}MASA:{RESET}{HIJAU}{masa}{RESET} |{KUNING}CPU:{RESET} {suhu_cpu}  |{KUNING}CUACA:{RESET} {temp_cuaca}\u00b0C :{CYAN}{ket_cuaca}{RESET}"
        )
        print(
            f"{HIJAU}                                                             THINKPAD X230    {RESET}"
        )
        print(
            f"{KUNING}                                                            TAJUDIN  ADNAN{RESET}\n"
        )
        print(
            f"{PUTIH}=========================================================    {PUTIH}SENARAI MENU{RESET}{PUTIH}    ========================================================================{RESET}\n"
        )
        print(
            f" {KELABU} 0{RESET}{OREN}1.{RESET}{HIJAU} SEMBANG {RESET}                                             {KELABU} 0{RESET}{OREN}2.{RESET}{HIJAU} CARI NOTA{RESET}                                                   {KELABU} 0{RESET}{OREN}3.{RESET}{HIJAU} PANDUAN BOT {RESET}"
        )
        print(
            f" {KELABU} 0{RESET}{OREN}4.{RESET}{HIJAU} MUZIK{RESET}                                                {KELABU} 0{RESET}{OREN}5.{RESET}{HIJAU} NOTA HTML{RESET}                                                   {KELABU} 0{RESET}{OREN}6.{RESET}{HIJAU} ELEKTRIK{RESET}"
        )
        print(
            f" {KELABU} 0{RESET}{OREN}7.{RESET}{HIJAU} GALERI{RESET}                                               {KELABU} 0{RESET}{OREN}8.{RESET}{HIJAU} CODING{RESET}                                                      {KELABU} 0{RESET}{OREN}9.{RESET}{HIJAU} BOT PY{RESET}"
        )
        print(
            f" {OREN} 10.{RESET}{BIRU} BACKUP{RESET}                                               {OREN} 11.{RESET}{HIJAU} KELUAR{RESET}                                                      {OREN} 15.{RESET}{HIJAU} AZKAR{RESET}"
        )
        print(
            f" {OREN} 12.{RESET}{MERAH} PADAM     {RESET}                                           {OREN} 13.{RESET}{HIJAU} GITHUB{RESET}                                                      {OREN} 14.{RESET}{HIJAU} PRIVACY{RESET}"
        )
        print(
            f" {OREN} 16.{RESET}{HIJAU} SAWET    {RESET}                                            {OREN} 17.{RESET}{HIJAU} TANYA AI {RESET}                                                   {OREN} 18.{RESET}{HIJAU} SCAN NETWORK{RESET}"
        )
        print(
            f" {OREN} 19.{RESET}{HIJAU} E-BOOK {RESET}                                              {OREN} 20.{RESET}{HIJAU} KALKULATOR {RESET}                                                 {CYAN} 21.{RESET}{HIJAU} FREEDOM BLOG{RESET}"
        )
        print(
            f" {OREN} 22.{RESET}{HIJAU} TERJEMAHAN {RESET}"
        )
        print(
            f"{PUTIH}======================================================================================================================================================{RESET}\n"
        )

        p = input(f"{PUTIH}PILIH TAJUK MENU: {RESET}").strip()

        map_fail = {
            "1": "sembang santai.json",
            "3": "Nota.json",
            "4": "muzik.json",
            "6": "elektrik.json",
            "7": "galeri.json",
            "8": "coding.json",
            "9": "botpy.json",
            "16": "sawet.json",
            "19": "e-book.json",
            "15": "azkar.json",
        }
        if p == "2":
            carian_index()

        elif p == "14":
            if semak_password():
                urus_rak("rahsia.json", "Rahsia")

        elif p == "5":
            urus_rak("html.json", "HTML")

        elif p in map_fail:
            nama = map_fail[p]
            label = nama.replace(".json", "").replace(" ", "_").capitalize()
            if nama == "galeri.json":
                cache_file = (
                    "/home/tajudin/BOT_PROJECT/FAIL_TECH/BOT/data/galeri_cache.txt"
                )
                folder = os.path.expanduser(
                    "~/BOT_PROJECT/FAIL_TECH/BOT/Pictures/GALERI ALBUM"
                )
                ext = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp")
                jumlah_folder = len(
                    [f for f in os.listdir(folder) if f.lower().endswith(ext)]
                )
                jumlah_cache = 0
                if os.path.exists(cache_file):
                    with open(cache_file, "r") as cf:
                        jumlah_cache = int(cf.read().strip() or "0")
                if jumlah_folder != jumlah_cache:
                    scan_album()
            urus_rak(nama, label)

        elif p == "17":
            os.system("clear")
            print(f"{CYAN}{'─'*30}{RESET}")
            print(f"      {OREN}[ TANYA AI ]{RESET}")
            print(f"{CYAN}{'─'*30}{RESET}\n")
            last_soalan = None
            last_jawapan = None
            while True:
                soalan = input(
                    f"{HIJAU}Soalan ({MERAH}'0' keluar{HIJAU}): {RESET}"
                ).strip()
                if soalan == "0":
                    break
                elif soalan == "simpan":
                    if last_jawapan:
                        simpan = input(f"{KUNING}Nama nota: {RESET}").strip()
                        if simpan:
                            os.makedirs("data/.txt", exist_ok=True)
                            with open(
                                f"data/.txt/{simpan}.txt", "w", encoding="utf-8"
                            ) as f:
                                f.write(
                                    f"Soalan: {last_soalan}\n\nJawapan:\n{last_jawapan}"
                                )
                            print(f"{HIJAU}✓ Tersimpan sebagai '{simpan}.txt'{RESET}\n")
                    else:
                        print(f"{MERAH}Tiada jawapan untuk disimpan.{RESET}\n")
                elif soalan:
                    print(f"\n{KUNING}Sedang berfikir...{RESET}")
                    jawapan = tanya_ai(soalan)
                    last_soalan = soalan
                    last_jawapan = jawapan
                    print(f"\n{HIJAU}AI:{RESET} {jawapan}\n")
                    print(
                        f"{KUNING}[Taip{RESET}{HIJAU} simpan {RESET}{KUNING} untuk simpan jawapan ini]{RESET}\n"
                    )

       # elif p == "18":
           # os.system("clear")
           # print(f"{CYAN}{'─'*40}{RESET}")
           # print(f"     {OREN}[ KESELAMATAN NETWORK ]{RESET}")
           # print(f"{CYAN}{'─'*40}{RESET}\n")
           # print(f"{HIJAU}1. Scan IP (Nmap){RESET}")
           # print(f"{HIJAU}2. Semak Laptop Sendiri{RESET}")
           # print(f"{HIJAU}3. Device Dalam Network{RESET}\n")
           # pilih = input(f"Pilih: ").strip()

           # if pilih == "1":
               # target = input(f"IP target: ").strip()
               # os.system(f"nmap -Pn -sV {target}")
               # input(f"\n{CYAN}Tekan Enter untuk kembali...{RESET}")
           # elif pilih == "2":
               # os.system("ss -tulnp")
               # os.system("last -n 20")
               # input(f"\n{CYAN}Tekan Enter untuk kembali...{RESET}")
           # elif pilih == "3":
               # os.system("arp -a")
               # input(f"\n{CYAN}Tekan Enter untuk kembali...{RESET}")

           # input(f"\n{KUNING}Tekan Enter untuk ke{RESET}{HIJAU} MENU UTAMA...{RESET}")

        elif p == "18":
            os.system("clear")
            print(f"{CYAN}{'─'*40}{RESET}")
            print(f"     {OREN}[ KESELAMATAN NETWORK ]{RESET}")
            print(f"{CYAN}{'─'*40}{RESET}\n")
            print(f"{HIJAU}1. Scan IP (Nmap){RESET}")
            print(f"{HIJAU}2. Semak Laptop Sendiri{RESET}")
            print(f"{HIJAU}3. Device Dalam Network{RESET}\n")
            pilih = input(f"Pilih: ").strip()
            if pilih == "1":
                target = input(f"IP target: ").strip()
                if not target:
                    print(f"{MERAH}IP tidak boleh kosong{RESET}")
                    logging.warning("Scan nmap dibatalkan: IP kosong")
                else:
                    logging.info(f"Scan nmap dimulakan pada target: {target}")
                    hasil = os.system(f"nmap -Pn -sV {target}")
                    if hasil != 0:
                        logging.warning(f"Scan nmap pada {target} tamat dengan kod ralat: {hasil}")
                    else:
                        logging.info(f"Scan nmap pada {target} selesai")
                input(f"\n{CYAN}Tekan Enter untuk kembali...{RESET}")
            elif pilih == "2":
                logging.info("Semakan laptop sendiri (ss + last) dijalankan")
                os.system("ss -tulnp")
                os.system("last -n 20")
                input(f"\n{CYAN}Tekan Enter untuk kembali...{RESET}")
            elif pilih == "3":
                logging.info("Semakan device dalam network (arp -a) dijalankan")
                os.system("arp -a")
                input(f"\n{CYAN}Tekan Enter untuk kembali...{RESET}")
            input(f"\n{KUNING}Tekan Enter untuk ke{RESET}{HIJAU} MENU UTAMA...{RESET}")

       
        elif p == "20":
            kalkulator()

        elif p == "21":
            import webbrowser
            import os

            subprocess.run(
                [
                    "python3",
                    os.path.expanduser(
                        "~/BOT_PROJECT/FAIL_TECH/BOT/update_pdf_list.py"
                    ),
                ]
            )
            fail_html = os.path.expanduser("~/BOT_PROJECT/FAIL_TECH/BOT/index.html")
            print(f"\n{CYAN}Freedom Diy 3-in-1 Hub...{RESET}")
            time.sleep(2)
            input(f"Tekan{HIJAU}'ENTER'{RESET}{PUTIH} untuk buka blog...{RESET}")
            webbrowser.open(f"file://{fail_html}")


        elif p == "22":
            menu_terjemah()

        elif p == "13":
            import webbrowser

            webbrowser.open("https://github.com/dhinai")

        elif p == "10":
            buat_backup()

        elif p == "11":
            print(f"\n{HIJAU}Bot ditutup. Jumpa lagi Tajudin!{RESET}")
            exit()

        elif p == "12":
            os.system("clear")
            print(f"{MERAH}=== [ MENU PADAM ] ==={RESET}")
            for key, val in map_fail.items():
                print(f"  {key}. {val}")

            pilih_f = input(f"\n{CYAN}Pilih No Fail: {RESET}").strip()

            if pilih_f in map_fail:
                fail_target = map_fail[pilih_f]
                target_nota = (
                    input(f"{MERAH}Taip tajuk nak padam: {RESET}").strip().lower()
                )
                data = muat_data(fail_target)

                keys = list(data.get("soalan", {}).keys())
                keys_lower = [k.lower() for k in keys]

                if target_nota in keys_lower:
                    tajuk_asal = keys[keys_lower.index(target_nota)]
                    confirm = input(
                        f"{MERAH}Betul nak buang '{tajuk_asal}'? (y/n): {RESET}"
                    ).strip()
                    if confirm.lower() == "y":
                        del data["soalan"][tajuk_asal]
                        simpan_data(fail_target, data)
                        print(f"{HIJAU}✅ Tajuk '{tajuk_asal}' Telah Dipadam{RESET}")
                else:
                    print(f"{MERAH}Tajuk '{target_nota}' tidak dijumpai.{RESET}")

            input(f"{KUNING}Tekan 'ENTER'...{RESET}")

        else:
            if p != "":
                print(f"{MERAH}Menu {p} tak wujud!{RESET}")
                time.sleep(0.8)


if __name__ == "__main__":
    main()

