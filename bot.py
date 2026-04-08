import shutil
import os
import json
import time
import sys
import requests

def dapatkan_cuaca():
    api_key = "eb1307ea5036d16cbb3f0e5a03660b97"
    kota = "Sungai Besar"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={kota}&appid={api_key}&units=metric&lang=id"
    try:
        respon = requests.get(url, timeout=5)
        data = respon.json()
        temp = round(data['main']['temp'])
        ket = data['weather'][0]['description'].capitalize()
        return temp, ket
    except:
        return "--", "Offline"

def warna_suhu(temp):
    if temp == "--": return f"{PUTIH}--°C{RESET}"
    temp = int(temp)
    if temp <= 26: return f"{CYAN}{temp}°C{RESET}" # Sejuk
    elif temp <= 32: return f"{KUNING}{temp}°C{RESET}" # Suam
    else: return f"{MERAH}{temp}°C{RESET}" # Panas


# --- 1. WARNA (ANSI Escape Codes) ---
BIRU = '\033[94m'
UNGU = '\033[95m'
TEBAL = '\033[1m'
PUTIH = '\033[97m'
MERAH = '\033[91m'
KUNING = '\033[93m'
KELABU = '\033[90m'
HIJAU = '\033[92m'
CYAN = '\033[96m'
RESET = '\033[0m'
OREN = '\033[38;5;208m'

# --- 2. FUNGSI SISTEM ---
def buat_backup():
    asal = os.getcwd()
    destinasi = '~/Documents/BACKUP_BOT/'
    if not os.path.exists(destinasi):
        os.makedirs(destinasi)
    fail_fail = [f for f in os.listdir(asal) if f.endswith('.py') or f.endswith('.json')]
    for f in fail_fail:
        shutil.copy(f, destinasi)
    print(f"\n{HIJAU}[ OK ] Semua fail dah selamat di-backup!{RESET}")
    input(f"Tekan Enter untuk balik...")

# --- 4 - DEF BACA JSON (VERSI KUNCI MATI) ---
def muat_data(nama_fail):
    if not os.path.exists(nama_fail):
        return {"soalan": {}} # Kalau fail tak ada, baru buat baru

    try:
        with open(nama_fail, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # INI KUNCI DIA: Bagitahu ada error, jangan pulangkan data kosong!
        os.system('clear')
        print(f"{MERAH}[!] BAHAYA: Fail {nama_fail} rosak format!{RESET}")
        print(f"{KUNING}[!] Bot takkan simpan apa-apa supaya nota lama tak hilang.{RESET}")
        print(f"{KUNING}[!] Sila betulkan fail {nama_fail} guna 'nano' dulu.{RESET}")
        input("\nTekan Enter untuk keluar...")
        return None

# --- 5 - DEF SIMPAN JSON (VERSI KUNCI MATI) ---
def simpan_data(nama_fail, data):
    # Kalau data tu 'None' (sebab fail rosak tadi), jangan simpan!
    if data is None:
        return

    with open(nama_fail, 'w') as f:
        json.dump(data, f, indent=4)

def padam_nota(nama_fail, tajuk):
    data = muat_data(nama_fail)
    # Check kalau tajuk tu wujud dalam senarai "soalan"
    if tajuk in data.get("soalan", {}):
        del data["soalan"][tajuk]
        simpan_data(nama_fail, data)
        print(f"\n{HIJAU}[ OK ] Nota '{tajuk}' sudah dibuang!{RESET}")
    else:
        print(f"\n{MERAH}[ ! ] Tajuk '{tajuk}' tak jumpa dalam {nama_fail}.{RESET}")


def typewriter(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05) # Laju sikit biar tak tunggu lama
    print()

# --- 3. LOGIK CARI & PAPAR ---
def urus_rak(nama_fail, tajuk):
    data = muat_data(nama_fail)
    os.system('clear')
    print(f"                 === [ MOD {tajuk.upper()} ] ===")
    print(f"                 Taip{CYAN} '0'{RESET} utk ke menu.\n")

    while True:
        user_input = input(f"{KUNING}Tanya {tajuk}:{RESET} ").lower().strip()

        if not user_input: continue # Brek kalau tertekan Enter kosong
        if user_input == '0': break

        if user_input == 'list':
            print(f"\n{HIJAU}---SOALAN TERSEDIA ({tajuk}):{RESET}")
            for i, s in enumerate(data['soalan'].keys() ,1):
                print(f"{i}. {s}")
            continue

        # Proses Mencari
        if user_input in data['soalan']:
            nota = data['soalan'][user_input]
            # Penterjemah Warna & Simbol
            # Tambah .replace("{BIRU}", "\033[94m") dalam rantaian kod tu
            nota_siap = nota.replace("{HIJAU}", HIJAU).replace("{KUNING}", KUNING)\
                            .replace("{MERAH}", MERAH).replace("{CYAN}", CYAN)\
                            .replace("{BIRU}", "\033[94m")\
                            .replace("{RESET}", RESET).replace("{PUTIH}", PUTIH)\
                            .replace("{OREN}", OREN).replace("{UNGU}", UNGU)

            # Sokongan baris baru (\n)
            final_teks = nota_siap.encode().decode('unicode_escape')
            typewriter(f"{HIJAU}Bot:{RESET} {final_teks}{RESET}")
        else:
            print(f"{MERAH}Bot: Aku tak tahu lagi pasal ni.{RESET}")
            print(f"{KUNING}Ajar aku (taip nota di bawah, letak '.' di baris baru utk simpan):{RESET}")

            isi_nota = []
            while True:
                baris = input()
                if baris.strip() == ".": break
                isi_nota.append(baris)

            if isi_nota:
                jawapan = "\n".join(isi_nota)
                if jawapan.strip():
                    # 1. Update data dalam memori
                    data['soalan'][user_input] = jawapan

                    # 2. Simpan ke fail
                    simpan_data(nama_fail, data)

                    # 3. PENTING: Muat semula data dari fail (Refresh)
                    data = muat_data(nama_fail)

                    print(f"{HIJAU}Bot: Data telah disimpan dan disegarkan!{RESET}")

def warna_suhu(temp):
    if temp == "--": return f"{PUTIH}--°C{RESET}"
    # Tukar suhu jadi nombor bulat
    t = int(temp)
    if t <= 26: return f"{CYAN}{t}°C{RESET}"
    elif t <= 32: return f"{KUNING}{t}°C{RESET}"
    else: return f"{MERAH}{t}°C{RESET}"


# --- 4. DASHBOARD UTAMA ---
def main():
    while True:
        os.system('clear')
        masa = time.strftime("%I:%M %p")

        # --- TAMBAH BARIS NI ---
        temp_cuaca, ket_cuaca = dapatkan_cuaca()
        # -----------------------

        print(f"{HIJAU}------------------------------------------------------{RESET}")
        print(f"{OREN}                     TAJUDIN ADNAN{RESET}")
        print(f"{HIJAU}======================================================{RESET}")
        print(f"                    {CYAN}     V4.1 {RESET}")
        print(f"{HIJAU}======================================================{RESET}")
        print(f" MASA: {HIJAU}{masa}{RESET} | CUACA: {warna_suhu(temp_cuaca)} ({ket_cuaca})")
        print(f"{HIJAU}------------------------------------------------------{RESET}")
        print(" 1. Sembang        2. Nota         3. Sistem")
        print(" 4. Memori         5. Alam         6. Elektrik")
        print(" 7. Diy            8. Coding       9. Tech")
        print(f" {UNGU}10.BACKUP{RESET}         {MERAH}11.EXIT{RESET}")
        print(f" {CYAN}12.DELJSON{RESET}")
        print(f"{HIJAU}------------------------------------------------------{RESET}")

        p = input(f"{KUNING} PILIH MENU: {RESET}")

        map_fail = {
            '1':'sembang.json', '2':'nota.json', '4':'memori.json',
            '5':'alam.json', '6':'elektrik.json', '7':'diy.json',
            '8':'coding.json', '9':'tech.json'
        }

        if p in map_fail:
            urus_rak(map_fail[p], map_fail[p].replace('.json','').capitalize())
        elif p == '10': buat_backup()
        elif p == '12':
            os.system('clear')
            print(f"{MERAH}=== [ MENU PADAM GLOBAL ] ==={RESET}")
            print(f"{KUNING}Pilih fail mana nak dibersihkan:{RESET}")
            # Tunjukkan senarai fail yang ada dalam map_fail
            for key, val in map_fail.items():
                print(f" {key}. {val}")

            pilih_f = input(f"\n{CYAN}Pilih No Fail: {RESET}")

            if pilih_f in map_fail:
                fail_target = map_fail[pilih_f]
                target_nota = input(f"{MERAH}Taip Tajuk/No nota nak padam dalam {fail_target}: {RESET}")

                # Tanya pengesahan (Brek keselamatan)
                confirm = input(f"{KUNING}Betul ke nak buang '{target_nota}'? (y/n): {RESET}")
                if confirm.lower() == 'y':
                    padam_nota(fail_target, target_nota)
            else:
                print(f"{MERAH}No fail tak wujud!{RESET}")

            input(f"\n{KUNING}Tekan Enter balik ke menu...{RESET}")

        elif p == '11': break
        else: time.sleep(0.5)

if __name__ == "__main__":
    main()
