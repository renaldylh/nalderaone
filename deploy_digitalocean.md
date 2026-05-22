# Panduan Deploy Nalderaone ke DigitalOcean (Docker & Caddy)

Dokumen ini berisi panduan langkah demi langkah untuk melakukan deploy aplikasi Nalderaone ke VPS **DigitalOcean Droplet** menggunakan **Docker Compose** dan **Caddy Server** untuk subdomain `studio.naldera.tech` (atau subdomain pilihan Anda).

---

## 📋 Prasyarat
1. Akun **DigitalOcean** aktif.
2. Akses ke panel pengelolaan DNS domain `naldera.tech` (misal di Cloudflare, GoDaddy, dll.).
3. Kredensial **Google API / YouTube** (Client ID & Client Secret) yang sudah dibuat.

---

## 🚀 Langkah 1: Membuat Droplet di DigitalOcean

1. Masuk ke [DigitalOcean Control Panel](https://cloud.digitalocean.com/).
2. Klik tombol **Create** di kanan atas, lalu pilih **Droplets**.
3. Konfigurasikan Droplet baru Anda:
   * **Region**: Pilih region terdekat dengan pengguna Anda (misalnya **Singapore**).
   * **OS/Image**: Pilih **Ubuntu** (versi LTS terbaru seperti **24.04 LTS** atau **22.04 LTS**).
   * **Size (Spesifikasi)**: Pilih **Basic**. Disarankan memilih minimal **2 GB RAM / 1 atau 2 vCPUs** (sekitar $12 - $18/bulan) agar proses transcoding video lewat FFmpeg berjalan lancar.
   * **Authentication**: Pilih **SSH Key** (sangat direkomendasikan karena jauh lebih aman daripada password).
4. Klik **Create Droplet** dan tunggu hingga proses selesai. Catat **IP Public** Droplet baru Anda (misal: `103.123.45.67`).

---

## 🌐 Langkah 2: Hubungkan Subdomain `naldera.tech`

Sebelum menyalakan server, Anda harus mengarahkan subdomain Anda agar ketika diakses, ia tahu harus pergi ke IP Droplet Anda.

1. Buka DNS Management tempat Anda membeli domain `naldera.tech` (misalnya Cloudflare, Niagahoster, dll.).
2. Tambahkan **A Record** baru:
   * **Type**: `A`
   * **Name**: `studio` (atau subdomain lain yang Anda inginkan, misal `app`)
   * **IPv4 Address / Value**: Masukkan **IP Public Droplet** Anda (misal: `103.123.45.67`).
   * **TTL**: `Auto` atau `3600`.
3. Simpan perubahan. Tunggu beberapa menit hingga DNS terpropagasi.

---

## 🛠️ Langkah 3: Setup Server VPS (SSH & Install Docker)

1. Buka terminal komputer lokal Anda dan masuk ke Droplet menggunakan SSH:
   ```bash
   ssh root@IP_PUBLIC_DROPLET_ANDA
   ```
2. Lakukan update paket sistem operasi:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
3. Install Docker dan Docker Compose plugin:
   ```bash
   sudo apt install docker.io docker-compose-v2 -y
   ```
4. Pastikan Docker berhasil terinstal dengan mengecek versinya:
   ```bash
   docker --version
   docker compose version
   ```

---

## 📂 Langkah 4: Upload Project & Buat File `.env` Produksi

1. Clone repositori project Anda ke server (misal ke direktori `/app`):
   ```bash
   git clone <URL_REPOSiTORI_ANDA> /app
   cd /app
   ```
2. Buat file `.env` produksi dengan menyalin file `.env.example`:
   ```bash
   cp .env.example .env
   nano .env
   ```
3. Edit variabel-variabel berikut di dalam file `.env`:
   ```env
   # CORE settings
   SECRET_KEY=masukkan_kunci_random_yang_panjang_dan_aman
   ENCRYPTION_KEY_SALT=masukkan_kunci_salt_random_yang_panjang_dan_aman
   DEBUG=false
   ALLOWED_HOSTS=studio.naldera.tech,localhost,127.0.0.1
   APP_URL=https://studio.naldera.tech
   APP_DOMAIN=studio.naldera.tech

   # DATABASE
   # (Gunakan settingan ini karena PostgreSQL berjalan di container docker yang sama)
   DATABASE_URL=postgres://postgres:postgres@postgres:5432/nalderaone

   # STORAGE (Penyimpanan lokal di dalam server)
   STORAGE_BACKEND=local
   MEDIA_ROOT=/app/media

   # PLATFORM CREDENTIALS (YouTube)
   PLATFORM_GOOGLE_CLIENT_ID=client_id_youtube_dari_google_cloud
   PLATFORM_GOOGLE_CLIENT_SECRET=client_secret_youtube_dari_google_cloud

   # WEBHOOK
   YOUTUBE_WEBHOOK_SECRET=buat_string_acak_bebas_untuk_verifikasi
   ```
   *Tekan `CTRL + O`, lalu `Enter` untuk menyimpan, kemudian `CTRL + X` untuk keluar dari editor nano.*

---

## ⚡ Langkah 5: Nyalakan Aplikasi dengan Docker Compose

Untuk menjalankan aplikasi dalam mode produksi dengan setup lengkap (Django + PostgreSQL + Worker + Caddy SSL Proxy), jalankan perintah berikut di folder `/app`:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

### Apa saja yang dilakukan perintah ini?
1. **Membangun image Django** dan meng-compile file Tailwind CSS secara otomatis.
2. **Menjalankan container database PostgreSQL** secara mandiri.
3. **Menjalankan container migrasi database** untuk memastikan tabel-tabel terbuat dengan benar.
4. **Menyalakan container backend Django (`app`)** dengan web server produksi Gunicorn.
5. **Menyalakan background worker (`worker`)** yang bertugas mengunggah konten ke YouTube di belakang layar.
6. **Menyalakan container pemeliharaan (`maintenance`)** untuk membersihkan session dan file media sampah secara otomatis setiap 24 jam.
7. **Menyalakan web server Caddy (`caddy`)** sebagai reverse proxy pada port 80 & 443. Caddy akan mendeteksi domain `studio.naldera.tech` dan mendaftarkan sertifikat SSL (HTTPS) dari Let's Encrypt secara otomatis dan gratis!

---

## 📈 Langkah 6: Perintah Penting untuk Pemeliharaan

Berikut adalah beberapa perintah praktis yang akan sering Anda gunakan di server:

* **Melihat status container yang berjalan**:
  ```bash
  docker compose ps
  ```
* **Melihat log real-time aplikasi**:
  ```bash
  docker compose logs app -f
  ```
* **Melihat log worker YouTube**:
  ```bash
  docker compose logs worker -f
  ```
* **Mematikan aplikasi**:
  ```bash
  docker compose down
  ```
* **Me-restart aplikasi tanpa downtime**:
  ```bash
  docker compose restart
  ```
* **Membuat user administrator (Superuser) baru pertama kali**:
  ```bash
  docker compose exec app python manage.py createsuperuser
  ```

---

> [!IMPORTANT]
> **Pengingat Google Cloud Console:**
> Jangan lupa untuk masuk ke [Google Cloud Console](https://console.cloud.google.com/) dan menambahkan URL redirect produksi ini pada kredensial YouTube Anda:
> `https://studio.naldera.tech/social-accounts/callback/youtube/`

---

## 🔀 Menjalankan Bersama Project Lain di Satu VPS

Jika VPS Anda sudah memiliki project lain yang berjalan (yang memakai port 80 dan 443), Anda tidak bisa menjalankan Caddy bawaan project ini secara langsung karena port tersebut bentrok.

Ada dua skenario utama untuk menyelesaikannya:

### Skenario A: Jika VPS Anda Menggunakan Nginx (Host)
Jika project lain menggunakan Nginx sebagai reverse proxy utama di VPS:

1. **Jalankan project ini tanpa Caddy Docker**:
   Jangan jalankan service `caddy` saat menghidupkan Docker Compose, jalankan service spesifik lainnya saja:
   ```bash
   docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build app worker postgres maintenance
   ```
   *Catatan: Port `8000` pada container `app` akan diekspos ke host (`127.0.0.1:8000`). Jika port 8000 bentrok dengan project lain, Anda bisa menggantinya di file `docker-compose.yml` pada bagian ports (misal `"8081:8000"`).*

2. **Tambahkan Konfigurasi Block Server Nginx baru**:
   Buat file konfigurasi Nginx baru untuk subdomain Anda di VPS:
   ```bash
   sudo nano /etc/nginx/sites-available/nalderaone
   ```
   Masukkan konfigurasi reverse proxy berikut:
   ```nginx
   server {
       listen 80;
       server_name studio.naldera.tech;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
   Aktifkan konfigurasi dan restart Nginx:
   ```bash
   sudo ln -s /etc/nginx/sites-available/nalderaone /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

3. **Install SSL dengan Certbot (Let's Encrypt)**:
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d studio.naldera.tech
   ```

---

### Skenario B: Jika VPS Anda Menggunakan Caddy (Host)
Jika VPS Anda sudah menggunakan Caddy yang terpasang langsung di server host (bukan di dalam Docker):

1. **Jalankan project tanpa container Caddy**:
   ```bash
   docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build app worker postgres maintenance
   ```

2. **Tambahkan Subdomain ke Caddyfile Host**:
   Buka Caddyfile yang sudah ada di VPS Anda (biasanya di `/etc/caddy/Caddyfile`) dan tambahkan blok berikut di bagian bawah:
   ```caddy
   studio.naldera.tech {
       reverse_proxy localhost:8000
       encode gzip
   }
   ```
3. **Restart Caddy Host**:
   ```bash
   sudo systemctl restart caddy
   ```

