# IRASA Python Style Guide

Panduan ini mencakup konvensi penulisan kode Python yang diadopsi dari [PEP 8](https://peps.python.org/pep-0008/). Mengikuti konvensi ini akan membantu Anda menulis kode Python yang bersih, konsisten, dan mudah dipahami.

# Daftar Isi

1. [Penamaan (Naming Conventions)](#1-penamaan-naming-conventions)
   - 1.1 Variabel
   - 1.2 Fungsi
   - 1.3 Kelas
   - 1.4 Konstanta
   - 1.5 Modul dan Paket
2. [Indentasi dan Spasi](#2-indentasi-dan-spasi)
   - 2.1 Indentasi
   - 2.2 Spasi Setelah Koma
   - 2.3 Spasi Sekitar Operator
   - 2.4 Penulisan Baris
3. [Komentar](#3-komentar)
   - 3.1 Komentar Satu Baris
   - 3.2 Komentar Multiline
   - 3.3 Docstrings
4. [Penggunaan Impor](#4-penggunaan-impor)
   - 4.1 Penempatan Impor
   - 4.2 Jenis Impor
5. [Penggunaan Fungsi dan Kelas](#5-penggunaan-fungsi-dan-kelas)
   - 5.1 Fungsi dan Metode
   - 5.2 Kelas
6. [Penanganan Exception](#6-penanganan-exception)
7. [Praktik Terbaik Lainnya](#7-praktik-terbaik-lainnya)
   - 7.1 Hindari Duplikasi Kode
   - 7.2 Gunakan Tipe Data yang Tepat
   - 7.3 Gunakan Anotasi Tipe
8. [Format dan Penataan Kode](#8-format-dan-penataan-kode)
   - 8.1 Pisahkan Blok Kode
   - 8.2 Struktur Kontrol yang Jelas
9. [Penggunaan Tipe Data dan Struktur Kontrol](#9-penggunaan-tipe-data-dan-struktur-kontrol)
10. [Kesimpulan](#10-kesimpulan)


## 1. Penamaan (Naming Conventions)

### 1.1 Variabel
- Gunakan huruf kecil dengan pemisah kata menggunakan garis bawah (`snake_case`).
  - Contoh: `my_variable`, `user_age`

### 1.2 Fungsi
- Fungsi harus menggunakan `snake_case` (huruf kecil dengan garis bawah).
  - Contoh: `calculate_total()`, `get_user_input()`

### 1.3 Kelas
- Gunakan `PascalCase` (setiap kata dimulai dengan huruf kapital).
  - Contoh: `CustomerAccount`, `UserProfile`

### 1.4 Konstanta
- Gunakan huruf kapital dengan pemisah garis bawah (`UPPER_SNAKE_CASE`).
  - Contoh: `MAX_VALUE`, `PI`

### 1.5 Modul dan Paket
- Nama modul menggunakan huruf kecil dan jika perlu, pisahkan dengan garis bawah (`snake_case`).
  - Contoh: `math_utilities`, `data_processor`

## 2. Indentasi dan Spasi

### 2.1 Indentasi
- Gunakan 4 spasi untuk setiap level indentasi. Jangan menggunakan tab.

### 2.2 Spasi Setelah Koma
- Gunakan spasi setelah koma dalam argumen atau elemen dalam daftar.
  - Contoh: `my_function(1, 2, 3)`, `list_of_values = [1, 2, 3]`

### 2.3 Spasi Sekitar Operator
- Gunakan satu spasi di sekitar operator seperti `+`, `=`, `-`, `*`, dll.
  - Contoh: `x = 5 + 10`, `result = a * b`

### 2.4 Penulisan Baris
- Batasi panjang baris hingga 79 karakter. Untuk docstrings, batasi hingga 72 karakter per baris.
- Jika baris terlalu panjang, bagi kode ke beberapa baris menggunakan tanda kurung atau garis miring terbalik (`\`).

## 3. Komentar

### 3.1 Komentar Satu Baris
- Gunakan komentar satu baris untuk penjelasan singkat. Mulai dengan huruf kapital dan beri spasi setelah tanda `#`.
  - Contoh: `# This is a single-line comment`

### 3.2 Komentar Multiline
- Gunakan komentar blok untuk penjelasan yang lebih panjang, dengan tanda `#` di awal setiap baris.
  - Contoh:
    ```python
    # This is a multi-line comment
    # explaining the function below
    ```

### 3.3 Docstrings
- Gunakan docstring untuk mendokumentasikan modul, kelas, fungsi, atau metode. Gunakan tiga tanda kutip (`"""`) untuk mendeklarasikan docstring.
  - Contoh:
    ```python
    def add(a, b):
        """
        Menambahkan dua angka dan mengembalikan hasilnya.
        
        Parameter:
        a (int): Angka pertama
        b (int): Angka kedua
        
        Returns:
        int: Hasil penjumlahan
        """
        return a + b
    ```

## 4. Penggunaan Impor

### 4.1 Penempatan Impor
- Semua impor harus ditempatkan di bagian atas file, sebelum kode lain.
- Impor harus dipisahkan ke dalam tiga grup:
  1. Impor dari Python standar library
  2. Impor dari library pihak ketiga
  3. Impor dari modul lokal

### 4.2 Jenis Impor
- Gunakan `import module` daripada `from module import *` untuk menghindari polusi namespace.

## 5. Penggunaan Fungsi dan Kelas

### 5.1 Fungsi dan Metode
- Fungsi dan metode harus diberi nama yang deskriptif dan menggunakan `snake_case`.
- Fungsi harus memiliki docstring untuk mendeskripsikan fungsinya.

### 5.2 Kelas
- Nama kelas harus menggunakan `PascalCase`.
- Kelas juga harus memiliki docstring yang menjelaskan tujuan kelas.

## 6. Penanganan Exception

- Gunakan blok `try` dan `except` untuk menangani kesalahan.
- Hindari menggunakan `except:` tanpa menyebutkan tipe kesalahan.
- Jika menangani tipe kesalahan tertentu, sebutkan tipe kesalahan dalam `except`.

  - Contoh:
    ```python
    try:
        value = int(input("Masukkan angka: "))
    except ValueError:
        print("Input bukan angka.")
    ```

## 7. Praktik Terbaik Lainnya

### 7.1 Hindari Duplikasi Kode
- Hindari duplikasi kode dengan memecah kode menjadi fungsi atau kelas yang dapat digunakan kembali.

### 7.2 Gunakan Tipe Data yang Tepat
- Gunakan tipe data yang sesuai dengan kebutuhan untuk meningkatkan kejelasan kode dan menghindari kesalahan.

### 7.3 Gunakan Anotasi Tipe
- Jika menggunakan Python 3.5 atau lebih baru, gunakan anotasi tipe untuk menjelaskan tipe data dari parameter dan nilai balik.
  - Contoh:
    ```python
    def add_numbers(a: int, b: int) -> int:
        return a + b
    ```

## 8. Format dan Penataan Kode

### 8.1 Pisahkan Blok Kode
- Gunakan garis kosong untuk memisahkan blok kode yang berbeda dan meningkatkan keterbacaan.

### 8.2 Struktur Kontrol yang Jelas
- Gunakan struktur kontrol seperti `if`, `for`, `while` dengan jelas dan hindari penulisan kode yang terlalu rumit.

## 9. Penggunaan Tipe Data dan Struktur Kontrol

- Pilih tipe data yang tepat sesuai dengan kebutuhan. Gunakan `list`, `tuple`, `set`, atau `dict` dengan bijaksana.
- Gunakan `list comprehensions` atau `generator expressions` jika memungkinkan untuk membuat kode lebih ringkas dan efisien.

## 10. Kesimpulan

Mengikuti konvensi ini akan membuat kode Python Anda lebih bersih, konsisten, dan mudah dipelihara. Pastikan untuk selalu mengikuti standar ini untuk meningkatkan kolaborasi dalam pengembangan perangkat lunak.

