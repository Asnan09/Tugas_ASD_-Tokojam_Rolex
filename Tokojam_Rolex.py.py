from prettytable import PrettyTable
import pwinput
import os
import datetime
GREEN = "\033[92m"

def check_access_hours():
    current_time = datetime.datetime.now().time()
    start_time = datetime.time(8, 0)
    end_time = datetime.time(16, 0)
    return start_time <= current_time <= end_time

def tambah_jam(daftar_jam):
    try:
        nama = input("Masukkan nama jam: ")
        jenis = input("Masukkan jenis jam: ")
        jumlah = int(input("Masukkan jumlah jam: "))
        harga = float(input("Masukkan harga jam: Rp "))
        jam_baru = {'Nama': nama, 'Jenis': jenis, 'Harga': harga, 'Stok': jumlah}
        daftar_jam.append(jam_baru)
        print(f"Barang {nama} ({jumlah} {jenis}) dengan harga Rp {harga:,} telah ditambahkan ke stok.")
    except (ValueError, EOFError, AttributeError):
        print("Input tidak valid. Harap masukkan data yang benar.")
    except KeyboardInterrupt:
        print("\ndibatalkan.")

def tampilkan_daftar_jam(daftar_jam):
    try:
        table = PrettyTable()
        table.field_names = ["No", "Nama", "Jenis", "Harga", "Stok"]
        for i, jam in enumerate(daftar_jam, start=1):
            table.add_row([i, jam['Nama'], jam['Jenis'], f"Rp {jam['Harga']:,}", jam['Stok']])
        print(table)
    except (EOFError, AttributeError):
        print("Terjadi kesalahan saat menampilkan daftar jam.")
    except KeyboardInterrupt:
        print("\ndibatalkan.")

def beli_barang(daftar_jam, pembeli, daftar_belanja):
    try:
        total_harga = 0
        total_harga_sebelum_diskon = 0
        for item in daftar_belanja:
            nama, jumlah = item['Nama'], item['Jumlah']
            for jam in daftar_jam:
                if jam['Nama'].lower() == nama.lower():
                    if jam['Stok'] >= jumlah:
                        total_harga_sebelum_diskon += jam['Harga'] * jumlah
                        total_harga += jam['Harga'] * jumlah
                    else:
                        print(f"Stok {jam['Nama']} tidak mencukupi.")
                        return
        print(f"Total harga sebelum diskon: Rp {total_harga_sebelum_diskon:,}")

        if total_harga >= 100000:
            total_harga_diskon = total_harga * 0.9
            print(f"Total harga setelah diskon: Rp {total_harga_diskon:,}")
        else:
            total_harga_diskon = total_harga
            print(f"Total harga: Rp {total_harga_diskon:,}")

        if pembeli['E-Pay'] >= total_harga_diskon:
            pembeli['E-Pay'] -= total_harga_diskon
            print(f"Pembelian berhasil. Saldo E-Pay {pembeli['Nama']}: Rp {pembeli['E-Pay']:,}")
            for item in daftar_belanja:
                nama, jumlah = item['Nama'], item['Jumlah']
                for jam in daftar_jam:
                    if jam['Nama'].lower() == nama.lower():
                        jam['Stok'] -= jumlah
        else:
            print("Saldo E-Pay tidak mencukupi.")
    except (ValueError, EOFError, AttributeError):
        print("Terjadi kesalahan saat proses pembelian.")
    except KeyboardInterrupt:
        print("\npembelian dibatalkan.")

def top_up_epay(pembeli, jumlah):
    try:
        if pembeli['Saldo'] >= jumlah:
            pembeli['E-Pay'] += jumlah
            pembeli['Saldo'] -= jumlah
            print(f"Top-up E-Pay berhasil. Saldo E-Pay {pembeli['Nama']}: Rp {pembeli['E-Pay']:,}")
            print(f"Saldo {pembeli['Nama']}: Rp {pembeli['Saldo']:,}")
        else:
            print("Saldo tidak mencukupi untuk melakukan top-up E-Pay.")
    except (ValueError, EOFError, AttributeError):
        print("Terjadi kesalahan saat top-up E-Pay.")
    except KeyboardInterrupt:
        print("\ntop-up dibatalkan.")

def hapus_barang(daftar_jam, nama_jam_hapus):
    try:
        for jam in daftar_jam:
            if jam['Nama'].lower() == nama_jam_hapus.lower():
                daftar_jam.remove(jam)
                print(f"Jam {nama_jam_hapus} telah dihapus dari stok.")
                return
        print(f"Jam {nama_jam_hapus} tidak ditemukan di stok.")
    except (EOFError, AttributeError):
        print("Terjadi kesalahan saat menghapus barang.")
    except KeyboardInterrupt:
        print("\npenghapusan dibatalkan.")

def menu_admin(daftar_jam):
    while True:
        try:
            print("|================================|")
            print("|         Menu Admin             |")
            print("|================================|")
            print("| 1. Tambahkan Jam ke Stok       |")
            print("| 2. Hapus Barang dari Stok      |")
            print("| 3. Lihat Daftar Jam            |")
            print("| 4. Keluar                      |")
            print("|================================|")

            pilihan = int(input("Masukkan nomor pilihan: "))
            os.system('cls')

            if pilihan == 1:
                tambah_jam(daftar_jam)
            elif pilihan == 2:
                nama_jam_hapus = input("Masukkan nama jam yang ingin dihapus: ")
                hapus_barang(daftar_jam, nama_jam_hapus)
            elif pilihan == 3:
                tampilkan_daftar_jam(daftar_jam)
            elif pilihan == 4:
                print("Keluar dari menu admin.")
                break
            else:
                print("Pilihan tidak valid. Silakan masukkan nomor yang benar.")
        except (ValueError, EOFError):
            print("Input tidak valid. Silakan coba lagi.")
        except KeyboardInterrupt:
            print("\nSilakan coba lagi.")

def menu_pembeli(daftar_jam, daftar_pembeli):
    while True:
        try:
            pembeli_nama = input("Masukkan nama Anda: ")
            pembeli_pin = pwinput.pwinput("Masukkan PIN Anda: ", mask='*')

            pembeli = verifikasi_akun(daftar_pembeli, pembeli_nama, pembeli_pin)

            if pembeli is not None:
                print(f"Selamat datang, {pembeli['Nama']}")
                while True:
                    print("|======================================|")
                    print("|             Menu Pembeli             |")
                    print("|======================================|")
                    print("| 1. Lihat Daftar Harga                |")
                    print("| 2. Beli Jam                          |")
                    print("| 3. Top Up E-Pay                      |")
                    print("| 4. Lihat Saldo dan E-Pay             |")
                    print("| 5. Keluar                            |")
                    print("|======================================|")

                    pilihan = input("Masukkan nomor pilihan: ")
                    os.system('cls')

                    if pilihan == "1":
                        tampilkan_daftar_jam(daftar_jam)
                    elif pilihan == "2":
                        tampilkan_daftar_jam(daftar_jam)
                        daftar_belanja = []
                        while True:
                            try:
                                nomor_jam = int(input("Masukkan nomor jam yang ingin Anda beli: "))
                                if nomor_jam < 1 or nomor_jam > len(daftar_jam):
                                    print("Masukkan nomor yang valid.")
                                    continue
                                jumlah_jam = int(input("Masukkan jumlah jam yang ingin Anda beli: "))
                                daftar_belanja.append({'Nama': daftar_jam[nomor_jam-1]['Nama'], 'Jumlah': jumlah_jam})
                            except (ValueError, EOFError):
                                print("Masukkan nomor yang valid.")
                            
                            while True:
                                lagi = input("Apakah Anda ingin membeli barang lain? (ya/tidak): ").lower()
                                if lagi == 'ya' or lagi == 'tidak':
                                    break
                                else:
                                    print("Masukkan pilihan yang valid (ya/tidak).")
                        
                            if lagi != 'ya':
                                break
                        beli_barang(daftar_jam, pembeli, daftar_belanja)
                    elif pilihan == "3":
                        try:
                            jumlah_topup_epay = float(input("Masukkan jumlah top-up E-Pay: "))
                            top_up_epay(pembeli, jumlah_topup_epay)
                        except (ValueError, EOFError):
                            print("Masukkan jumlah top-up yang valid.")
                    elif pilihan == "4":
                        print(f"Saldo {pembeli['Nama']}: Rp {pembeli['Saldo']:,}")
                        print(f"Saldo E-Pay {pembeli['Nama']}: Rp {pembeli['E-Pay']:,}")
                    elif pilihan == "5":
                        print("Keluar dari menu pembeli.")
                        break
                    else:
                        print("Pilihan tidak valid. Silakan masukkan nomor yang benar.")
                if input("Apakah Anda ingin melakukan transaksi lagi? (ya/tidak): ").lower() != 'ya':
                    break
            else:
                print("Nama atau PIN tidak valid. Akun anda tidak terdaftar.")
        except (ValueError, EOFError):
            print("Input tidak valid. Silakan coba lagi.")
        except KeyboardInterrupt:
            print("\nSilakan coba lagi.")

def verifikasi_akun(daftar_pembeli, nama, pin):
    try:
        for pembeli in daftar_pembeli:
            if pembeli['Nama'].lower() == nama.lower() and pembeli['PIN'] == pin:
                return pembeli
        return None
    except (EOFError, AttributeError):
        print("Terjadi kesalahan saat verifikasi akun.")
    except KeyboardInterrupt:
        print("\nOperasi verifikasi dibatalkan.")

def verifikasi_admin(admin_data, username, password):
    try:
        return admin_data['Username'] == username and admin_data['Password'] == password
    except (EOFError, AttributeError):
        print("Terjadi kesalahan saat verifikasi admin.")
    except KeyboardInterrupt:
        print("\nverifikasi dibatalkan.")

if __name__ == "__main__":
    daftar_jam = [
        {'Nama': 'GMT Master II', 'Jenis': 'Analog', 'Harga': 75000, 'Stok': 10},
        {'Nama': 'Lady Datejust', 'Jenis': 'Analog', 'Harga': 95000, 'Stok': 10},
        {'Nama': 'Oyster Perpetual', 'Jenis': 'Analog', 'Harga': 95000, 'Stok': 10},
        {'Nama': 'Day Date', 'Jenis': 'Analog', 'Harga': 65000, 'Stok': 10},
        {'Nama': 'Yacht', 'Jenis': 'Analog', 'Harga': 50000, 'Stok': 10},
        {'Nama': 'Air King', 'Jenis': 'Analog', 'Harga': 50000, 'Stok': 10}
    ]

    admin_data = {
        'Username': 'admin',
        'Password': '123'
    }

    daftar_pembeli = [
        {'Nama': 'asnan', 'PIN': '1234', 'Saldo': 500000, 'E-Pay': 100000},
    ]

    if check_access_hours():
        while True:
            try:
                print(GREEN +"|==========================================|")
                print(       "|      Selamat datang di toko Jam Rolex    |")
                print(       "|==========================================|")
                print(       "| 1. Admin                                 |")
                print(       "| 2. Pembeli                               |")   
                print(       "| 3. Keluar                                |")
                print(       "|==========================================|")

                pilihan = int(input("Pilih Menu: "))
                os.system('cls')

                if pilihan == 1:
                    username = input("Masukkan username: ")
                    password = pwinput.pwinput("Masukkan password: ", mask='*')
                    if verifikasi_admin(admin_data, username, password):
                        print("Login berhasil.")
                        menu_admin(daftar_jam)
                    else:
                        print("Username atau password salah.")
                elif pilihan == 2:
                    menu_pembeli(daftar_jam, daftar_pembeli)
                elif pilihan == 3:
                    print("Terima kasih telah menggunakan sistem manajemen toko.")
                    break
                else:
                    print("Pilihan tidak valid. Silakan masukkan nomor yang benar.")
            except (ValueError, EOFError):
                print("Input tidak valid. Silakan coba lagi.")
            except KeyboardInterrupt:
                print("\nSilakan coba lagi .")
    else:
        print(GREEN +"Mohon Maaf, toko hanya bisa diakses dari jam 08.00 pagi sampai 16.00 sore.")
