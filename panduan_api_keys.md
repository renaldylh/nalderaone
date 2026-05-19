# Panduan Pembuatan API Key & Integrasi Media Sosial
Dokumen ini berisi panduan lengkap untuk mendapatkan API Key/Credentials dari portal developer media sosial dan cara menginstalnya ke Nalderaone (baik lewat file `.env` maupun halaman Dashboard).

---

## 🛠️ Persiapan Awal & Konfigurasi VPS (Production)
Pastikan Anda sudah mengetahui alamat dasar aplikasi Anda (Default lokal: `http://localhost:8000`).
Alamat ini (disebut `APP_URL`) sangat krusial karena setiap platform membutuhkan **OAuth Redirect URI** yang sesuai agar proses otentikasi dapat kembali ke aplikasi Anda dengan sukses.

### 🌐 Jika Di-deploy ke VPS / Menggunakan Domain Sendiri:
Jika nanti Anda meng-host aplikasi ini di VPS (misalnya menggunakan domain `https://nalderaone.com` atau IP public `http://103.123.45.67:8000`):

1. **Ubah file `.env` di VPS Anda**:
   Ganti variabel `APP_URL` agar mengarah ke domain/IP VPS Anda. Contoh:
   ```env
   APP_URL=https://nalderaone.com
   ```
2. **Ubah Redirect URI di Google Cloud / Meta / LinkedIn Developer Console**:
   Semua URL redirect yang sebelumnya berisi `http://localhost:8000` harus Anda ganti dengan domain/IP VPS baru Anda di masing-masing developer console.
   * **Contoh (Google Login)**:
     `http://localhost:8000/accounts/google/login/callback/` ➔ `https://nalderaone.com/accounts/google/login/callback/`
   * **Contoh (YouTube Publishing)**:
     `http://localhost:8000/social-accounts/callback/youtube/` ➔ `https://nalderaone.com/social-accounts/callback/youtube/`
   * Suffix/akhiran URL (seperti `/accounts/google/login/callback/`) **harus tetap sama persis**, cukup ubah nama domain di depannya saja.

---

## 1. Meta (Facebook, Instagram & Threads)
Ketiga platform ini berada di bawah payung Meta dan menggunakan satu aplikasi developer yang sama.

### Langkah Membuat API Key:
1. Buka [Meta for Developers](https://developers.facebook.com/) dan masuk menggunakan akun Facebook Anda.
2. Klik tombol **Create App** di pojok kanan atas.
3. Pilih tipe aplikasi **Business** (jangan pilih Consumer agar mendapatkan akses izin Page).
4. Isi nama aplikasi Anda dan selesaikan pembuatan.
5. Masuk ke halaman dashboard aplikasi Anda:
   * Buka menu **App Settings → Basic** di sidebar kiri.
   * Temukan **App ID** dan **App Secret** (Klik *Show* untuk melihat App Secret). Catat kedua nilai ini.
6. Pada sidebar kiri, klik **Use cases** untuk menambahkan fitur yang dibutuhkan:
   * **Facebook Publishing**: Klik *Customize* pada use case **"Manage everything on your Page"**, lalu tambahkan izin opsional: `pages_manage_posts`, `pages_read_engagement`, `pages_read_user_content`.
   * **Instagram Publishing**: Tambahkan use case **"Manage messaging & content on Instagram"**, lalu aktifkan izin: `instagram_basic`, `instagram_content_publish`, `instagram_manage_comments`, `instagram_manage_insights`.
   * **Threads Publishing**: Tambahkan use case **"Access the Threads API"**, lalu aktifkan: `threads_content_publish`, `threads_manage_insights`, `threads_manage_replies`.
7. Tambahkan produk **Facebook Login for Business**:
   * Masuk ke **Facebook Login → Settings**.
   * Pada kolom **Valid OAuth Redirect URIs**, masukkan alamat callback berikut secara lengkap (sesuaikan domain jika di-deploy ke VPS):
     ```text
     http://localhost:8000/social-accounts/callback/facebook/
     http://localhost:8000/social-accounts/callback/instagram/
     http://localhost:8000/social-accounts/callback/threads/
     ```
   * Simpan perubahan.

> [!IMPORTANT]
> Akun Instagram yang dapat dihubungkan harus berupa **Instagram Professional (Creator atau Business)** dan telah ditautkan ke salah satu **Facebook Page** yang Anda kelola.

---

## 2. Google (YouTube & Google Business Profile)
Digunakan untuk mengupload video (YouTube) atau membuat postingan lokal bisnis (Google Business).

### Langkah Membuat API Key:
1. Masuk ke [Google Cloud Console](https://console.cloud.google.com/).
2. Buat proyek baru dengan mengklik dropdown proyek di kiri atas → **New Project**.
3. Aktifkan API yang diperlukan:
   * Masuk ke menu **APIs & Services → Library**.
   * Cari dan klik **YouTube Data API v3**, lalu klik **Enable**.
   * Cari dan klik **My Business Business Information API** dan **My Business Account Management API**, lalu klik **Enable**.
4. Konfigurasi layar persetujuan (OAuth Consent Screen):
   * Masuk ke **APIs & Services → OAuth consent screen**.
   * Pilih User Type: **External**, lalu klik **Create**.
   * Isi informasi wajib aplikasi (nama aplikasi, email dukungan, dll.), lalu klik save.
5. Buat Kredensial:
   * Masuk ke **APIs & Services → Credentials**.
   * Klik **+ Create Credentials → OAuth client ID**.
   * Pilih Application type: **Web application**.
   * Scroll ke bagian **Authorized redirect URIs** di bagian bawah, tambahkan URL berikut:
     ```text
     http://localhost:8000/social-accounts/callback/youtube/
     http://localhost:8000/social-accounts/callback/google_business/
     ```
   * Klik **Create**.
6. Salin **Client ID** dan **Client Secret** yang muncul pada pop-up.

---

## 3. LinkedIn
Digunakan untuk membagikan postingan tulisan/gambar ke profil personal atau halaman organisasi LinkedIn.

### Langkah Membuat API Key:
1. Buka [LinkedIn Developer Portal](https://developer.linkedin.com/).
2. Klik **Create App**. Isi informasi dasar dan kaitkan dengan halaman LinkedIn perusahaan Anda (jika ada).
3. Setelah aplikasi dibuat, buka tab **Products**:
   * Temukan **Share on LinkedIn** dan klik *Request access* (biasanya langsung aktif).
   * Temukan **Sign In with LinkedIn using OpenID Connect** dan klik *Request access*.
4. Buka tab **Auth**:
   * Di bawah bagian **OAuth 2.0 settings**, tambahkan link redirect berikut pada kolom **Authorized Redirect URLs for your app**:
     ```text
     http://localhost:8000/social-accounts/callback/linkedin_personal/
     http://localhost:8000/social-accounts/callback/linkedin_company/
     ```
   * Di bagian atas tab Auth, Anda akan melihat **Client ID** dan **Client Secret** (klik ikon mata untuk melihat). Salin nilai tersebut.

---

## 4. TikTok
Digunakan untuk mengunggah konten video atau Short TikTok secara otomatis.

### Langkah Membuat API Key:
1. Buka [TikTok Developer Portal](https://developers.tiktok.com/).
2. Daftarkan akun developer baru, lalu buat aplikasi baru (*Create App*).
3. Pada opsi produk yang ingin ditambahkan ke aplikasi, ajukan akses untuk:
   * **Login Kit** (untuk otentikasi login).
   * **Content Posting API** (untuk memposting video).
4. Di bagian pengaturan aplikasi, daftarkan **Redirect URI**:
   ```text
   http://localhost:8000/social-accounts/callback/tiktok/
   ```
5. TikTok menggunakan istilah **Client Key** (sebagai Client ID) dan **Client Secret**. Salin nilai tersebut dari dashboard aplikasi Anda.

---

## 5. Pinterest
Digunakan untuk membuat Pin (gambar/video) di papan (*Boards*) Pinterest Anda.

### Langkah Membuat API Key:
1. Buka [Pinterest Developer Portal](https://developers.pinterest.com/).
2. Masuk dengan akun bisnis Pinterest Anda, lalu buat aplikasi baru.
3. Di dalam menu pengaturan aplikasi, cari bagian **Redirect URIs** dan daftarkan:
   ```text
   http://localhost:8000/social-accounts/callback/pinterest/
   ```
4. Salin **App ID** (Client ID) dan **App Secret** Anda.

---

---

## 6. Google Login (Otentikasi Akun User / Google Sign-In)
Digunakan agar user/tim Anda bisa masuk atau mendaftar ke Nalderaone menggunakan akun Google mereka melalui tombol **"Continue with Google"** di halaman login.

### Langkah Membuat Kredensial Google Login:
1. Masuk ke [Google Cloud Console](https://console.cloud.google.com/).
2. Pastikan Anda telah memilih proyek yang sama (atau buat baru).
3. Jika belum pernah, buat **OAuth Consent Screen** (pilih *External*, lengkapi nama aplikasi dan email).
4. Masuk ke menu **APIs & Services → Credentials**.
5. Klik **+ Create Credentials → OAuth client ID**.
6. Pilih Application type: **Web application**.
7. Pada bagian **Authorized redirect URIs** (SANGAT PENTING), masukkan URL callback berikut:
   ```text
   http://localhost:8000/accounts/google/login/callback/
   ```
8. Klik **Create**, lalu salin **Client ID** dan **Client Secret** yang disediakan.

---

## ⚙️ Cara Memasang API Key ke Web Nalderaone

Setelah Anda mengumpulkan API Key di atas, Anda dapat menerapkannya menggunakan salah satu dari dua cara berikut:

### Metode A: Memasukkan ke file `.env` (Direkomendasikan untuk Server Mandiri)
1. Buka file `.env` di direktori utama proyek (`d:\project\nalderaone-studio\.env`).
2. Tempelkan kunci yang telah Anda dapatkan pada bagian berikut (kosongkan jika tidak digunakan):

```env
# Google OAuth Login (Untuk tombol login/daftar Google Sign-In)
GOOGLE_AUTH_CLIENT_ID=isi_client_id_google_login_anda
GOOGLE_AUTH_CLIENT_SECRET=isi_client_secret_google_login_anda

# Meta (Facebook, Instagram, Threads - Untuk posting konten)
PLATFORM_FACEBOOK_APP_ID=isi_app_id_meta_anda
PLATFORM_FACEBOOK_APP_SECRET=isi_app_secret_meta_anda

# Google (YouTube, Google Business - Untuk posting konten)
PLATFORM_GOOGLE_CLIENT_ID=isi_client_id_google_anda
PLATFORM_GOOGLE_CLIENT_SECRET=isi_client_secret_google_anda

# LinkedIn (Personal & Company - Untuk posting konten)
PLATFORM_LINKEDIN_COMPANY_CLIENT_ID=isi_client_id_linkedin_anda
PLATFORM_LINKEDIN_COMPANY_CLIENT_SECRET=isi_client_secret_linkedin_anda

# TikTok
PLATFORM_TIKTOK_CLIENT_KEY=isi_client_key_tiktok_anda
PLATFORM_TIKTOK_CLIENT_SECRET=isi_client_secret_tiktok_anda

# Pinterest
PLATFORM_PINTEREST_APP_ID=isi_app_id_pinterest_anda
PLATFORM_PINTEREST_APP_SECRET=isi_app_secret_pinterest_anda
```
3. Simpan file `.env` dan restart server Django Anda agar konfigurasi baru terbaca.

### Metode B: Melalui Dashboard Web (Platform Credentials)
Sekarang Anda bisa memasukkannya langsung dari menu dashboard utama tanpa perlu mengedit `.env` atau membuka Admin Panel Django:

1. Buka dashboard utama web Anda (misal: [http://localhost:8000](http://localhost:8000)).
2. Login sebagai administrator.
3. Di sidebar kiri, klik **Platform Credentials** (ikon gembok kunci di bawah kategori **Organization Settings**).
4. Anda akan melihat daftar semua platform media sosial yang didukung:
   * Klik **Configure** pada platform yang ingin Anda atur.
   * Masukkan **App ID/Client ID** dan **App Secret/Client Secret** ke dalam kolom input yang tersedia.
   * Klik **Save Credentials**.
5. Kredensial akan langsung terenkripsi secara otomatis, dan status platform tersebut akan berubah menjadi **Configured** (Aktif). Anda juga bisa melakukan **Edit Keys** atau **Delete** kapan saja dari halaman yang sama.

