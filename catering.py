# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/115UAwHu3017oe9SuKOvira95PNmMbIWe
"""

import streamlit as st
import pandas as pd
import numpy as np

# Initialize the menu in session state if not already done
if 'menu' not in st.session_state:
    st.session_state['menu'] = {
        "Nasi Goreng": 25000,
        "Mie Goreng": 20000,
        "Ayam Geprek": 30000,
        "Sate Ayam": 35000,
        "Es Teh Manis": 5000,
        "Jus Jeruk": 10000,
    }

subscribers = [
    {"name": "Budi", "email": "budi@example.com"},
    {"name": "Siti", "email": "siti@example.com"},
    {"name": "Andi", "email": "andi@example.com"},
]

def tampilkan_menu():
    st.write("Menu Katering:")
    for item, harga in st.session_state['menu'].items():
        st.write(f"- {item}: Rp{harga:,}")

def pesan_makanan():
    st.header("Pesan Makanan")
    with st.form(key='order_form'):
        nama_pelanggan = st.text_input("Nama Pelanggan:")
        if not nama_pelanggan:
            st.warning("Silakan masukkan nama pelanggan.")
            return None, None, None

        tampilkan_menu()
        pesanan = {}
        item = st.selectbox("Pilih makanan:", [""] + list(st.session_state['menu'].keys()))
        if item:
            jumlah = st.number_input(f"Masukkan jumlah {item}:", min_value=1, step=1)
            if st.form_submit_button("Tambah ke Pesanan"):
                if item in pesanan:
                    pesanan[item] += jumlah
                else:
                    pesanan[item] = jumlah

        metode_pembayaran = st.selectbox("Pilih Metode Pembayaran:", ["Tunai", "Kartu Kredit", "Transfer Bank", "E-Wallet"])
        if not metode_pembayaran:
            st.warning("Silakan pilih metode pembayaran.")
            return None, None, None

        submit_button = st.form_submit_button(label='Selesaikan Pesanan')
        if submit_button:
            return nama_pelanggan, pesanan, metode_pembayaran

    return None, None, None

def hitung_total_harga(pesanan):
    total_harga = 0
    for item, jumlah in pesanan.items():
        total_harga += st.session_state['menu'][item] * jumlah
    return total_harga

def tampilkan_pesanan(nama_pelanggan, pesanan, metode_pembayaran):
    st.write(f"Pesanan Anda, {nama_pelanggan}:")
    for item, jumlah in pesanan.items():
        st.write(f"- {item} x {jumlah}")
    total_harga = hitung_total_harga(pesanan)
    st.write(f"Total Harga: Rp{total_harga:,}")
    st.write(f"Metode Pembayaran: {metode_pembayaran}")

def login_admin():
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    if st.button("Login"):
       if username == "admin" and password == "admin123":
          st.success("Login admin berhasil!")
          st.session_state['logged_in'] = True
       else:
          st.error("Login admin gagal.")

def menu_admin():
    st.write("\nMenu Admin:")
    pilihan = st.radio("Pilihan Anda:", ["List Langganan", "Tambah Menu", "Edit Menu", "Hapus Menu", "Logout"])

    if pilihan == "List Langganan":
        st.write("Daftar Langganan:")
        for subscriber in subscribers:
            st.write(f"- {subscriber['name']} ({subscriber['email']})")
    
    elif pilihan == "Tambah Menu":
        nama_makanan = st.text_input("Nama Makanan Baru:")
        harga_makanan = st.number_input("Harga Makanan Baru:", min_value=0, step=1000)
        if st.button("Tambah"):
            if nama_makanan and harga_makanan:
                st.session_state['menu'][nama_makanan] = harga_makanan
                st.success(f"{nama_makanan} berhasil ditambahkan ke menu!")
            else:
                st.error("Nama dan harga makanan harus diisi.")
    
    elif pilihan == "Edit Menu":
        nama_makanan = st.selectbox("Pilih Makanan yang Akan Diedit:", list(st.session_state['menu'].keys()))
        harga_baru = st.number_input("Harga Baru:", min_value=0, step=1000)
        if st.button("Edit"):
            if nama_makanan in st.session_state['menu']:
                st.session_state['menu'][nama_makanan] = harga_baru
                st.success(f"Harga {nama_makanan} berhasil diubah!")
            else:
                st.error("Makanan tidak ditemukan di menu.")
    
    elif pilihan == "Hapus Menu":
        nama_makanan = st.selectbox("Pilih Makanan yang Akan Dihapus:", list(st.session_state['menu'].keys()))
        if st.button("Hapus"):
            if nama_makanan in st.session_state['menu']:
                del st.session_state['menu'][nama_makanan]
                st.success(f"{nama_makanan} berhasil dihapus dari menu!")
            else:
                st.error("Makanan tidak ditemukan di menu.")
    
    elif pilihan == "Logout":
        st.session_state['logged_in'] = False

# Program utama

st.title("Sistem Katering")
pilihan = st.radio("Pilih tipe pengguna:", ("Pengguna", "Admin"))

if pilihan == "Pengguna":
    st.header("Menu Makanan")
    tampilkan_menu()

    nama_pelanggan, pesanan, metode_pembayaran = pesan_makanan()  # Memanggil fungsi untuk memesan makanan

    if pesanan:
        st.header("Detail Pesanan")
        tampilkan_pesanan(nama_pelanggan, pesanan, metode_pembayaran)  # Memanggil fungsi untuk menampilkan pesanan

elif pilihan == "Admin":
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        st.header("Login Admin")
        login_admin()  # Memanggil fungsi untuk login admin
    else:
        menu_admin()  # Memanggil fungsi menu admin jika login berhasil
