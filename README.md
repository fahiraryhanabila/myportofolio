Name    : Fahira Ryhanabila
NPM     : 2506623660
Class   : PBP E

## Tentang Proyek
Sebuah website portofolio personal yang interaktif dan responsif, guna memenuhi tugas individu (*Individual Assignment*) mata kuliah Pemrograman Berbasis Platform (PBP).

Konten pada halaman portofolio ini meliputi:
- **Hero Section**: Menampilkan identitas utama (nama, program studi, NPM), tagline personal, serta tautan menuju GitHub, LinkedIn, dan Email, dengan latar belakang visual bertema kampus.
- **Credentials Section**: Menampilkan logo dan nama kepanitiaan yang pernah diikuti (Open House Fasilkom UI 2025, BETIS Fasilkom UI, COMPFEST 18, FUKI Fasilkom UI) dalam tata letak sejajar.
- **About Me Section**: Perkenalan singkat mengenai diri.
- **Interactive Skills Section**: Tata letak 2 kolom (Hard Skills & Soft Skills) berbentuk kartu (*card*) yang dapat diklik untuk efek "terangkat" (*is-raised*), serta menampilkan deskripsi tambahan saat *hover*.
- **Autentikasi & Otorisasi Pengguna**: Pengunjung dapat melakukan Register, Login, dan Logout menggunakan sistem autentikasi bawaan Django, dengan status login di navbar dan waktu login terakhir tercatat melalui cookie. Hak akses dibagi menjadi empat peran: pengunjung (hanya membaca), pengguna terdaftar (membaca dan memberi star), editor (membaca, memberi star, dan mengubah data lewat `PUT`/`PATCH`, tetapi tidak dapat membuat atau menghapus), dan superuser/pemilik portofolio (akses penuh). Aturan yang sama berlaku di halaman maupun di API.
- **Experience Page**: Menampilkan riwayat pengalaman kepanitiaan, organisasi, dan volunteer dalam bentuk kartu berisi kategori, status keberlangsungan, dan gambar pendukung. Data dimuat secara asinkron dari REST API (`/api/v1/experiences/`) lewat `fetch()` dengan indikator *loading*, tampilan data kosong, dan tampilan error. Dilengkapi pencarian *real-time* dengan *debouncing*, *star*/*unstar* (pengunjung yang belum login diarahkan ke halaman login), serta tambah, ubah, dan hapus data tanpa *reload* halaman sesuai hak akses peran.
- **Education Page**: Menampilkan riwayat pendidikan dalam format *timeline*, mencakup jenjang, tahun, deskripsi, dan daftar *skill* yang diperoleh. Data dimuat secara asinkron dari REST API (`/api/v1/education/`) dengan indikator *loading*, tampilan data kosong, dan tampilan error. Dilengkapi pencarian *real-time* dengan *debouncing*, *star*/*unstar*, serta tambah data lewat modal, ubah data lewat modal edit (`PUT`), dan hapus data tanpa *reload* halaman sesuai hak akses peran.
- **Form & Data Delivery**: Form HTML dikelola lewat `ModelForm` Django dengan validasi dan proteksi CSRF. Data untuk halaman Experience dan Education disajikan lewat REST API (lihat bagian *REST API*). Endpoint JSON lama `/api/experience/` dan `/api/education/` (dirakit manual dengan `JsonResponse`) serta halaman edit lama tetap dipertahankan.
- **Notifikasi Toast**: Komponen toast yang dapat dipakai ulang (berbasis Popover API) menampilkan umpan balik saat data berhasil ditambahkan maupun saat gagal, termasuk pesan kesalahan validasi dari server.
- **Keamanan Input (Perlindungan XSS & CSRF)**: Setiap nilai teks yang disisipkan ke HTML lewat JavaScript di-*escape* dengan `escapeHtml`. Di sisi server, input dibersihkan dengan `strip_tags` pada `clean_<field>` (`ModelForm`) dan `validate_<field>` (serializer), serta validasi URL gambar yang menolak skema berbahaya seperti `javascript:`. Setiap request yang mengubah data menyertakan header `X-CSRFToken`.
- **Responsive Layout**: Tata letak menyesuaikan otomatis antara tampilan desktop dan mobile menggunakan CSS Grid, Flexbox, `clamp()` untuk ukuran font, dan `@media` *query* untuk perubahan susunan elemen.

## REST API
API dibangun dengan Django REST Framework, memakai `@api_view` berbasis fungsi dan `SessionAuthentication`, di bawah prefix `/api/v1/`. Browsable API dapat dibuka di alamat endpoint.

| Method | Endpoint | Tindakan | Siapa yang boleh |
|---|---|---|---|
| GET | `/api/v1/education/` | Daftar (`?title=...` untuk mencari) | Semua pengunjung |
| POST | `/api/v1/education/` | Tambah data | Pemilik (superuser) |
| GET | `/api/v1/education/<id>/` | Detail | Semua pengunjung |
| PUT / PATCH | `/api/v1/education/<id>/` | Ubah data | Pemilik dan Editor |
| DELETE | `/api/v1/education/<id>/` | Hapus data | Pemilik |
| POST | `/api/v1/education/<id>/star/` | Beri/batalkan star | Pengguna login |

Endpoint Experience memakai pola yang sama di `/api/v1/experiences/` dengan ID berupa UUID.

- **Serializer** (`main/serializers.py`) memakai daftar `fields` eksplisit, menyertakan `star_count` dan `is_starred` sebagai field *read-only*, dan tidak menampilkan data akun sensitif.
- **Permission** (`main/permissions.py`) membatasi akses sesuai empat peran. Izin Editor memakai izin Django `change_<model>`.
- **Status HTTP**: `201` dibuat, `400` input tidak valid, `403` ditolak, `404` tidak ditemukan, `204` dihapus.
- **Test** (`main/tests_api.py`) memakai `APITestCase`, mencakup tiap peran, validasi, star, dan pemeriksaan CSRF dengan `APIClient(enforce_csrf_checks=True)`.

## Cara Menjalankan Proyek Secara Lokal
1. Unduh salinan repositori ini ke perangkat Anda, kemudian pindah ke direktori proyek:
    ```
    git clone https://github.com/fahiraryhanabila/myportofolio.git
    cd myportofolio
    ```
2. Siapkan lingkungan virtual (*virtual environment*) agar dependensi proyek tidak bercampur dengan instalasi Python global di komputer Anda:
    ```
    python -m venv env
    env\Scripts\activate    # Windows
    source env/bin/activate # macOS/Linux
    ```
3. Pasang seluruh pustaka (*library*) yang dibutuhkan proyek melalui berkas `requirements.txt`:
    ```
    pip install -r requirements.txt
    ```
4. Terapkan migrasi basis data bawaan Django agar struktur tabel tersinkronisasi:
    ```
    python manage.py migrate
    ```
5. Jalankan server:
    ```
    python manage.py runserver
    ```
6. Akses proyek melalui browser dengan membuka alamat `http://localhost:8000`

## Weekly Setup Instructions
Untuk memastikan proyek tetap berjalan dengan baik, beberapa langkah setup perlu dilakukan pada setiap awal minggu atau setelah memperoleh perubahan terbaru dari repository. 
1. Ambil perubahan terbaru dari repository menggunakan perintah:
    ```bash
    git pull
    ```
2. Pastikan virtual environment proyek telah aktif sebelum menjalankan proyek:
    ```
    env\Scripts\activate
    ```
3. Jika terdapat perubahan atau penambahan dependencies pada proyek, lakukan instalasi melalui:
    ```
    pip install -r requirements.txt
    ```
4. Jika terdapat perubahan pada model atau migration, terapkan perubahan tersebut ke database:
    ```
    python manage.py migrate
    ```
5. Sebelum menjalankan aplikasi, pastikan seluruh fitur yang telah dikembangkan tetap berjalan dengan baik melalui:
    ```
    python manage.py test
    ```
6. Setelah seluruh test berhasil, jalankan proyek secara lokal:
    ```
    python manage.py runserver
    ```
7. Periksa halaman dan fitur yang sedang dikembangkan untuk memastikan tidak terdapat error setelah perubahan diterapkan. Setelah seluruh perubahan dipastikan berjalan dengan baik, perubahan dapat disimpan melalui commit dan dikirimkan ke repository.

## Assets & Credits
- Ikon menggunakan **[Lucide Icons](https://lucide.dev/)**, dimuat melalui CDN.
- Font **Poppins** dari [Google Fonts](https://fonts.google.com/specimen/Poppins).
- API dibangun dengan **[Django REST Framework](https://www.django-rest-framework.org/)**.

## Progress Tugas Mingguan

### Tugas 1
1. Dalam pengerjaan Tutorial 1 dan Tugas 1, saya menggunakan beberapa elemen semantik HTML5 seperti `<header>`, `<nav>`, `<main>`, `<section>`, dan `<footer>` untuk menyusun struktur halaman. Elemen-elemen tersebut memudahkan saya dalam membuat static web terutama pada aspek keterbacaan dan aksesibilitas kode. Pada aspek keterbacaan, saya dapat dengan mudah mengidentifikasi satu-satu elemen kode sehingga akan sangat efisien dan efektif dalam melakukan debugging.  Elemen semantik juga membantu aksesibilitas, karena *screen reader* dan mesin pencari bisa lebih mudah memahami struktur dan hierarki.
Namun, dalam pengerjaan Tugas 1 ini, saya belum sepenuhnya konsisten menerapkan elemen semantik di semua bagian. Misalnya, untuk bagian *skill-card* atau *credential card* dimana saya masih menggunakan `<div>` biasa alih-alih `<article>`. karena pada saat itu saya fokus pada tampilan dari konten, padahal jika dipikirkan lebih dalam lagi, kedua hal tersebut lebih cocok dibungkus dengan `<article>`. Hal ini akan menjadi catatan perbaikan untuk iterasi berikutnya.

2. Tantangan utama yang saya temukan saat mengatur CSS agar *responsive* bukan hanya soal ukuran elemen yang mengecil, tapi juga soal perubahan layout dan urutan elemen antara desktop dan mobile. Contohnya, pada bagian Hero, saya awalnya menyusun identitas, foto, dan detail menggunakan CSS Grid dengan area yang saling bersebelahan (grid-template-columns), tapi di layar mobile susunan seperti itu jadi terlalu sempit dan berantakan. Saya kemudian menggunakan `@media (max-width: 600px)` untuk mengubah `grid-template-columns` menjadi satu kolom penuh.
Tantangan lain adalah menentukan elemen mana yang prioritas ukurannya harus fleksibel. Untuk judul-judul besar (seperti nama saya di Hero atau judul section), saya menggunakan fungsi `clamp()` pada `font-size` agar ukuran teks otomatis menyesuaikan lebar layar.
Evaluasi yang saya lakukan biasanya dengan langsung membuka *DevTools* dan mengecek tampilan di berbagai lebar layar, lalu menentukan breakpoint.

3. Website yang saya buat saat ini adalah *static web* murni, sehingga ada beberapa batasan yang saya rasakan saat mencoba menyajikan informasi secara optimal. Di awal saya berencana ingin menambahkan section *Experiences*. Namun, saya belum mengetahui cara untuk menyimpan dan menampilkan data secara dinamis menggunakan JavaScript. Selain itu, interaktivitas yang sudah ada seperti *toggle* pada *skill-card* masih lumayan biasa.
Adapun Fungsionalitas dinamis yang ingin saya tambahkan pada iterasi selanjutnya adalah:
    -Navigasi aktif dengan highlight modern
    indikator visual (*modern-bubble*) yang menunjukkan section mana yang sedang aktif dilihat pengguna, menggunakan JavaScript untuk mendeteksi posisi *scroll* dan memperbarui *state* navigasi secara *real-time*
   -Pengelolaan data secara terpisah dari markup
    Untuk menyimpan data pengalaman organisasi dalam bentuk array/objek JavaScript (atau nantinya JSON), sehingga menambah pengalaman baru cukup dengan menambah data, tanpa perlu menulis ulang blok HTML.

### **AI Disclosure - Tugas 1**

Dalam pengerjaan dan pengembangan web portofolio ini, saya memanfaatkan AI, yaitu Google Gemini, sebagai thought partner dan teman diskusi teknis. AI membantu saya memahami alur berpikir (*mindset*) pemrograman web, mengeksplorasi struktur HTML semantik, membedah logika CSS, hingga menentukan standar praktik *development* yang baik seperti pembuatan *commit message*.

Secara garis besar, hal-hal yang saya lakukan bersama AI meliputi:
    - Diskusi Struktur dan Alur Berpikir HTML: Berdiskusi mengenai langkah awal pembuatan *space* baru, pemilihan tag HTML semantik (seperti `<section>`, `<h2>`, `<h3>`), hingga menentukan cara terbaik menampilkan daftar *skills* (menggunakan pendekatan *card component* dan ikon).
    - Eksplorasi Konsep & Interaktivitas CSS: Memahami logika efek *hover* untuk menampilkan deskripsi *skill* secara mulus, pemanfaatan `box-shadow` dan `transform`   untuk efek timbul (*raised/tactile feedback*), serta integrasi *font* Poppins dari Google Fonts.
    - Konsultasi *Best Practices & Sizing*: Berdiskusi mengenai pengelompokan CSS Global vs Section-specific, prinsip efisiensi penulisan selector, konversi nilai *font-weight* dari Figma ke CSS, serta penentuan *padding* menggunakan Sistem Kelipatan 8px (8pt Grid System) dan variabel CSS.
    - Strategi Integrasi Asset & Git: Berdiskusi mengenai cara terbaik mengganti foto profil (pendekatan *background-image* dengan file ekspor Figma) serta menyusun judul *commit message* berstandar *Conventional Commits*.

Saya tidak pernah menyalin dan menempelkan kode dari AI secara mentah-mentah. Setiap masukan, *hint*, atau potongan kode yang diberikan AI selalu saya pelajari logika kerjanya, saya sesuaikan penamaan *class*-nya dengan kebutuhan file saya, dan saya uji coba secara mandiri dalam pengerjaannya.

Berikut 3 contoh interaksi saya bersama AI selama proses pengerjaan:
1. **Menentukan Alur Pembuatan Section Skills (HTML)**
* Prompt: *"aku ingin membuat section baru, dengan latar belakang gradasi coklat muda kekuningan hingga putih dengan judul besar "Skills" dimana, section itu terbagi menjadi 2 yaitu hard skills dan soft skills. masing-masing terdiri atas point-point berupa bullet agak panjang"*
* Tujuan: Mendapatkan masukan struktur HTML yang tepat untuk membagi dua kategori *skills* sebelum masuk ke tahap *styling*.
* Respon AI: Menjelaskan pembagian wadah utama (`<section>`), *container*, *heading*, pembagi kolom (`skills-wrapper/grid`), serta menyarankan penggunaan tag *unordered list* (`<ul>`).
* Tindakan Saya: Saya mengevaluasi saran AI, tetapi memutuskan untuk menggunakan pendekatan komponen kartu (`skill-card`) yang dipadu dengan *icon library* (Lucide Icons) karena tampilannya terasa jauh lebih modern dan sesuai dengan rancangan desain saya dibanding *bullet points* biasa.

2. **Memahami Penentuan Ukuran Padding dan Font Weight dari Figma ke CSS**
* Prompt: *"sebenernya dalam css ketika kita ingin padding gitu dan menentukan angkanya atau seberapa jauhnya itu dri mana? apakah kita memperkirakan sndiri atau ada parameter short cut tertentu yang memudahkan dalam penentuan padding?"*
* Tujuan: Memahami standar profesional dalam menentukan angka *padding/margin* agar tampilan web konsisten dan tidak sekadar dikira-kira.
* Respon AI: Menjelaskan konversi piksel Figma ke `rem`, konsep Sistem Kelipatan 8px (8pt Grid System), serta penggunaan variabel CSS (`:root`) sebagai *shortcut* batas ukuran.
* Tindakan Saya: Saya menerapkan prinsip kelipatan 8px (`0.5rem`, `1rem`, `1.5rem`) pada properti *padding* dan *gap* di file CSS saya untuk menjaga kerapian tata letak secara visual.

3. **Optimasi Struktur File Gambar dan CSS Hero Section**
* Prompt: *"aku pgn ganti photoku dg menghilangkan border kotak itu dan ganti background keseluruhan disitu. brti aku perlu manipulasi html yang hero-photo itu dihapus, trs nanti di css aku tambahin url yang ngarah langsung ke file.png photoku, dan aku juga hapus yang bagian foto berkaitan dg frame lama aja kan ya?"*
* Tujuan: Memvalidasi alur pemikiran saya saat ingin merombak tampilan foto *hero* dari bentuk frame kotak menjadi foto yang menyatu dengan latar belakang.
* Respon AI: Memvalidasi logika saya dan memberikan contoh penulisan CSS `background-image` beserta penjelasan properti *positioning*-nya.
* Tindakan Saya: Setelah memahami penjelasan AI, saya memilih opsi yang lebih efisien yaitu menyatukan foto dan background langsung saat ekspor dari Figma, sehingga saya cukup memanggil satu gambar utuh di CSS tanpa perlu memposisikan gambar secara terpisah.

### Tugas 2
1. Alur yang terjadi ketika pengguna membuka halaman portofolio baru dimulai dengan browser mengirimkan HTTP request ke alamat website. Request tersebut kemudian diterima oleh urls.py proyek yang bertugas menentukan aplikasi yang menangani URL tersebut. Selanjutnya, request diteruskan ke urls.py aplikasi yang memetakan URL ke fungsi view yang sesuai. Pada project ini, URL dapat diarahkan ke show_main, show_experience, dan show_education.
Selanjutnya, view akan memproses request dan mengambil data yang diperlukan dari model. Model disini bertugas merepresentasikan struktur data dalam database, seperti model Education dan Experience, dimana masing-masing model menyimpan informasi yang diperlukan. Data yang telah diperoleh oleh view kemudian dikirimkan ke template HTML. Template menggunakan data tersebut untuk membentuk halaman portofolio. Setelah template selesai dirender menjadi HTML, response dikirim kembali ke browser sehingga pengguna dapat melihat halaman portofolio beserta data yang berasal dari database.

2. Hal ini berkaitan dengan konsep **MVT (Model, View, Template)** pada Django, dimana tiap komponen pada konsep ini memiliki tanggung jawab yang berbeda, antara lain:
    a. Model bertugas mengelola dan menyimpan data
    b. View bertugas memproses request dan mengambil data dari model
    c. Template bertugas menampilkan data dalam bentuk halaman HTML
Oleh karena itu, sebaiknya data untuk section baru disimpan pada model dan tidak ditulis langsung di dalam template agar terdapat pemisahan antara data dan tampilan. 
Dengan adanya pemisahan ini pula, aplikasi akan lebih mudah dipelihara dan dikembangkan sehingga nantinya jika terdapat perubahan atau penambahan data, developer cukup mengubah pada model atau database tanpa harus mengubah struktur HTML pada template. Selain itu, template dapat digunakan kembali untuk menampilkan data yang berbeda, sehingga mengurangi penulisan data secara berulang dan membuat kode lebih terstruktur.

3. Fungsi dari makemigrations dan migrate pada Django cukup berbeda. **makemigrations** digunakan untuk membuat file migration berdasarkan perubahan yang dilakukan pada model di models.py . Sedangkan, **migrate** digunakan untuk menerapkan perubahan yang terdapat dalam file migration tersebut ke database. Sebagai contoh, jika pada model Education ditambahkan field baru seperti **start_year**, maka setelah mengubah models.py kita perlu menjalankan **python manage.py makemigrations** untuk membuat migration yang mencatat penambahan field tersebut, kemudian menjalankan **python manage.py migrate** agar perubahan tersebut benar-benar diterapkan pada struktur database.

### Testing
Unit test ditambahkan untuk memastikan fitur utama pada halaman proyek ini berjalan dengan baik. Pengujian mencakup akses URL dan penggunaan template yang sesuai, penampilan data dari model ketika data tersedia, serta penampilan pesan kondisi kosong ketika belum terdapat data.

* Pengujian dilakukan menggunakan perintah:

    ```bash
    python manage.py test
    ```
* Hasil pengujian:
    ```
    Ran 10 tests

    OK
    ```
* Aplikasi juga diuji dengan menjalankan development server menggunakan:
    ```
    python manage.py runserver
    ```
    Aplikasi dapat dijalankan secara lokal tanpa error dan seluruh halaman dapat diakses sesuai dengan rute yang telah ditentukan.

### **AI Disclosure - Tugas 2**
Proyek ini dikembangkan dengan bantuan asisten berbasis Kecerdasan Buatan (AI) untuk membantu proses perancangan, *refactoring*, dan penyelesaian masalah teknis secara efisien dan etis.

### 1. Alat AI yang Digunakan
* **Google Gemini** (Model Bahasa / AI Assistant)

### 2. Ruang Lingkup Bantuan AI
* **Alur Kerja & Arsitektur Django:** Membantu menentukan urutan pengembangan fitur baru (alur *Model-View-Template* dan penataan rute URL).
* **Diskusi Perancangan Model:** Membahas opsi *Model Inheritance* vs pembuatan model mandiri pada `models.py`.
* **Perancangan Komponen UI/UX:** Memberikan ide awal struktur kelas CSS dan logika perulangan Django (`forloop.counter`) untuk komponen *Timeline*.
* **Konsultasi Konsep Web Development:** Menjelaskan konsep routing Django, strategi unit responsif CSS (`width`/`height`/`max-width`), serta tata cara pengelolaan berkas media/aset.

### 3. Strategi *Prompting*
* **Iterative & Conversational Prompting:** Mengajukan pertanyaan secara bertahap seiring berkembangnya logika kode dan kebutuhan fitur.
* **Scenario-Based Questioning:** Menanyakan kendala teknis spesifik (misal: penataan URL, struktur pewarisan model, dan tata letak responsif CSS) untuk mendapatkan solusi.

### 4. Log Perintah & Hasil Interaksi

| No | Perintah/Pertanyaan Utama | Ringkasan Bantuan AI | Keputusan / Tindakan Saya |
| :---: | :--- | :--- | :--- |
| **1** | Mengonfirmasi langkah lanjutan setelah membuat `views.py` dan `models.py`. | Mengonfirmasi alur dan mengingatkan tahapan penting (*migrate*, `urls.py`, dan *template* HTML). | Melakukan penyusunan rute URL terlebih dahulu. |
| **2** | Menanyakan urutan pengerjaan terbaik antara routing (`urls.py`) dan pembuatan *template* HTML. | Menyusun alur kerja logis: `models.py` → `views.py` → `urls.py` → *template* HTML. | Mengikuti rekomendasi alur kerja dengan mengonfigurasi `urls.py` sebelum membuat file `.html`. |
| **3** | Menanyakan fungsi pasti dari perintah `path()` di Django. | Menjelaskan peran `path()` sebagai pemeta rute URL ke fungsi *view* dan struktur parameternya. | Memahami konsep pemetaan URL dan menerapkan penamaan rute (`name="..."`) secara konsisten. |
| **4** | Menanyakan cara menerapkan *inheritance* pada model agar tidak terjadi redundansi data. | Menjelaskan opsi *Model Inheritance* (seperti *Abstract Base Class*) untuk berbagi bidang (*field*) antar-kelas. | Mempertimbangkan saran AI, namun memutuskan tidak menggunakan *base class*** dan memilih membuat model `Education` secara mandiri agar struktur tiap model tetap eksplisit. |
| **5** | Menanyakan urgensi penambahan tautan navigasi antar-halaman (*experience* ke *education*). | Memberikan praktik terbaik penggunaan *template tag* dinamis `{% url 'show_experience' %}`. | Menambahkan komponen navigasi menggunakan tag `{% url %}` pada berkas *template*. |
| **6** | Menanyakan keharusan pendaftaran model di `admin.py` untuk pengisian berkas gambar. | Menjelaskan bahwa pendaftaran di `admin.py` bersifat opsional dan memberikan alternatif lain (misal: Django Shell). | Mengisi data awal/dummy melalui Python Shell dan Project Web Terminal pada Pacil Web Server (PWS)|
| **7** | Menanyakan sintaks loop penomoran otomatis di *template* Django. | Memberikan contoh penggunaan variabel bawaan Django seperti `forloop.counter` dan `forloop.counter0`. | Menggunakan `forloop.counter` di dalam tag perulangan HTML untuk menampilkan nomor urut pada *marker timeline*. |
| **8** | Meminta arahan struktur kelas CSS untuk membuat komponen *timeline*. | Menyediakan opsi struktur kelas CSS *Vertical Timeline* dan ide layout zigzag. | Menerapkan struktur *Vertical Timeline* searah dengan posisi garis di sebelah kiri (`education-timeline`) serta kartu di sisi kanan. |
| **9** | Menanyakan pilihan unit yang tepat (`%` vs `px`) untuk pengaturan `width` dan `height`. | Memberikan panduan penggunaan unit `%` untuk responsivitas lebar dan `auto`/`px` untuk tinggi elemen. | Mengatur ukuran foto dengan `px` pasti (`110px x 110px`) dan menggunakan `rem`/`px` untuk *gap* dan *padding*. |
| **10** | Mengonfirmasi cara kerja fungsi `max-width` pada CSS. | Menjelaskan fungsi `max-width` dalam membatasi lebar maksimal elemen di layar berukuran besar. | Menerapkan `max-width: 960px` pada `.container` dan `max-width: 100%` pada elemen gambar agar responsif. |

### 5. Evaluasi Kritis terhadap Penggunaan AI
AI digunakan sebagai alat bantu dalam proses pengembangan, bukan sebagai pengganti proses pemrograman yang saya lakukan. Saya tidak langsung menerapkan seluruh solusi yang diberikan AI, tetapi terlebih dahulu memahami alasan dan logika di balik setiap saran, kemudian menyesuaikannya dengan struktur proyek dan kebutuhan tugas.

Sebagai contoh, ketika AI memberikan saran mengenai struktur komponen dan implementasi fitur, saya membandingkan solusi tersebut dengan kode yang sudah saya miliki sebelum menentukan apakah solusi tersebut sesuai untuk digunakan. Saya juga menggunakan pertanyaan lanjutan (*follow-up prompting*) ketika terdapat konsep yang belum saya pahami, sehingga proses penggunaan AI tidak hanya berfokus pada menghasilkan kode, tetapi juga membantu memahami konsep yang sedang dipelajari.

### Tugas 3
1. Alasan mengapa menggunakan ModelForm dibanding menggunakan form HTML manual antara lain:
    - Django dapat secara otomatis men-generate field form, tipe data, dan validasi langsung dari struktur model.
    - Mengurangi duplikasi kode, terutama untuk constraint yang banyak dipakai di beberapa file tanpa menulis ulang di HTML.
    - Melakukan validasi tipe data secara otomatis dan cukup dengan memanggil form.save() untuk menyimpan data ke database.
    - Jika model suatu saat berubah, form akan menyesuaikan secara otomatis tanpa merombak kode HTML dari nol.
    - ModelForm dapat membuat proses CRUD menjadi lebih sederhana melalui form.save() yang berfungsi untuk membuat data baru maupun mengubah data yang sudah ada.
Sedangkan penambahan `{% csrf_token %}` pada form memiliki kegunaan, yaitu:
    - Mencegah pihak luar atau website lain dalam memalsukan request (*Cross-Site Request Forgery*) atas nama pengguna yang sedang login.
    - Django menyisipkan token unik ke form dan mencocokkannya dengan sesi pengguna saat disubmit; request tanpa token yang valid akan langsung ditolak.

2. JSON lebih disukai dibandingkan XML hal ini didukung dengan Kegunaan JSON, yaitu:
    - JSON lebih ringkas karena tidak membutuhkan tag pembuka dan penutup yang panjang seperti XML (`"key": "value"`).
    - `JSON.parse()` membuat JSON dapat langsung di parsing tanpa library tambahan.
    - Struktur objek dan array pada JSON secara komputasi lebih ringan dibanding fitur kompleks XML.
    - Penggunaan format *key-value* membuat kode menjadi lebih intuitif dan mudah dibaca oleh manusia.
    - Menjadi format *default* untuk mayoritas REST API modern, sehingga membuat integrasi antar sistem lebih seragam.

3. Alur yang terjadi saat menggunakan fungsi view untuk mengembalikan data portofolio dalam bentuk JSON, yaitu:
    - Client mengakses URL endpoint, (misal `/api/experience/`).
    - Fungsi view akan memanggil data dari database menggunakan Django ORM melalui `Experience.objects.all()`.
    - QuerySet objek Python tersebut diserialisasi menjadi string JSON menggunakan `serializers.serialize("json", experience)`.
    - Hasil serialisasi dikembalikan ke client menggunakan `HttpResponse` dengan `content_type="application/json"`.

Alasan diperlukannya proses serialization pada model Django sebelum data dikembalikan, antara lain karena objek Python yang hidup di memori server tidak bisa dikirimkan secara langsung melalui protokol HTTP yang berbasis teks/byte. Selain itu, proses serialization mengubah objek internal Python menjadi format standar berbasis teks (JSON) agar dapat dibaca dan diproses oleh berbagai bahasa pemrograman atau platform lain, seperti *frontend* JavaScript dan aplikasi *mobile*.

### **AI Disclosure - Tugas 3**
Proyek ini dikembangkan dengan bantuan asisten berbasis Kecerdasan Buatan (AI) untuk mendukung proses **pemahaman konsep, konsultasi teknis, implementasi, debugging, serta verifikasi hasil pengembangan**. AI digunakan sebagai sarana pendukung dalam memahami konsep Django, data delivery, serta pengelolaan repository menggunakan Git dan GitHub. Keputusan dan implementasi akhir tetap dilakukan oleh saya berdasarkan kebutuhan dan kondisi proyek.

### **1. Alat AI yang Digunakan**
* **ChatGPT** (Model Bahasa / AI Assistant)

### **2. Ruang Lingkup Bantuan AI**
* **Pemahaman Konsep Django:** Membantu menjelaskan konsep `ModelForm`, proses Create dan Update, penggunaan `instance`, serta mekanisme pengambilan object berdasarkan `id` atau unique fields.
* **Form Validation & Security:** Menjelaskan alasan penggunaan `ModelForm` dibandingkan form HTML manual serta fungsi `{% csrf_token %}` untuk perlindungan terhadap serangan *Cross-Site Request Forgery* (CSRF).
* **Data Delivery:** Membantu memahami konsep data delivery menggunakan format JSON dan XML serta alasan penggunaan JSON dalam pengembangan aplikasi web.
* **Serialization:** Menjelaskan proses mengubah object/model Django menjadi format JSON agar data dapat dikirim melalui HTTP dan digunakan oleh client.
* **Django API / Endpoint:** Membantu menjelaskan alur request ketika client mengakses endpoint seperti `/api/experience/`, mulai dari pengambilan data menggunakan Django ORM hingga pengembalian data dalam bentuk JSON.
* **Debugging & Update Feature:** Membantu memahami error pada proses Update, khususnya ketika object `Experience` tidak ditemukan berdasarkan ID yang diberikan pada URL.
* **Git & GitHub:** Membantu memahami proses *branching*, *merge*, sinkronisasi `main` dengan `origin/main`, serta interpretasi Git Graph setelah proses *merge*.
* **Verifikasi Repository:** Membantu memeriksa hasil `git status` untuk memastikan branch lokal telah sinkron dengan branch `main` pada GitHub.

### **3. Strategi *Prompting***
* **Contextual Prompting:** Memberikan konteks berupa struktur proyek, kode, pesan error, kondisi repository, maupun pertanyaan refleksi agar AI dapat memberikan bantuan yang sesuai dengan permasalahan yang sedang dihadapi.
* **Iterative & Conversational Prompting:** Mengajukan pertanyaan secara bertahap berdasarkan respons AI. Pertanyaan lanjutan digunakan untuk memperdalam pemahaman atau memastikan bahwa solusi yang diberikan sesuai dengan kondisi proyek.
* **Problem-Based Questioning:** Mengajukan permasalahan teknis secara spesifik, seperti error `No Experience matches the given query`, penggunaan `instance` pada ModelForm, serta kondisi branch setelah proses *merge*.
* **Verification Prompting:** Memberikan hasil aktual dari implementasi atau terminal, seperti output `git status`, untuk memvalidasi kondisi proyek dan memastikan solusi yang diberikan sesuai dengan keadaan repository.
* **Conceptual Follow-up:** Menggunakan pertanyaan lanjutan untuk memahami alasan di balik suatu implementasi, bukan hanya meminta kode. Contohnya adalah menanyakan alasan penggunaan serialization sebelum data model dikembalikan dalam bentuk JSON.

### **4. Log *Prompting* AI**
Penggunaan AI dalam Tugas 3 didokumentasikan untuk menunjukkan bagian-bagian proses pengembangan yang mendapatkan bantuan AI.

**Format Log:** `[ID] / [Tugas] - [Deskripsi Penggunaan AI]: [Link ke Chat]`

Keterangan:
- **ID** = nomor urut interaksi AI.
- **Tugas** = nomor tugas/tutorial yang dikerjakan.
- **Deskripsi Penggunaan AI** = ringkasan tujuan atau topik bantuan AI.
- **Link ke Chat** = tautan menuju percakapan AI yang digunakan.

**001 / Tugas 3 - Pemahaman alur Update menggunakan ID dan `instance`:** https://chatgpt.com/share/6ab00afb-9404-83ec-9e2e-48af8ed7914c
Membantu memahami proses Update, khususnya pengambilan object berdasarkan ID, penggunaan `get_object_or_404()`, pengisian `ModelForm` menggunakan `instance`, serta penyimpanan perubahan menggunakan `form.save()`.

**002 / Tugas 3 - Perancangan ModelForm untuk fitur CRUD:** https://chatgpt.com/share/6ab00afb-9404-83ec-9e2e-48af8ed7914c
Membantu memahami alasan penggunaan `ModelForm` dibandingkan form HTML manual, termasuk otomatisasi field dan validasi berdasarkan model serta kemudahan implementasi proses Create dan Update.

**003 / Tugas 3 - Pemahaman keamanan form dengan CSRF:** https://chatgpt.com/share/6ab00afb-9404-83ec-9e2e-48af8ed7914c
Membantu memahami fungsi `{% csrf_token %}` pada form Django dalam melindungi request dari serangan *Cross-Site Request Forgery* (CSRF).

**004 / Tugas 3 - Analisis JSON dan XML untuk data delivery:** https://chatgpt.com/share/6ab00afb-9404-83ec-9e2e-48af8ed7914c
Membantu memahami perbedaan JSON dan XML sebagai format data delivery, terutama dari sisi struktur data, keterbacaan, ukuran data, dan kemudahan pertukaran data antarplatform.

**005 / Tugas 3 - Analisis alur data delivery dan serialization:** https://chatgpt.com/share/6ab00afb-9404-83ec-9e2e-48af8ed7914c
Membantu memahami alur pengiriman data dari database hingga client melalui endpoint, mulai dari pengambilan data menggunakan Django ORM, proses serialization menggunakan `serializers.serialize("json", ...)`, hingga pengembalian data melalui `HttpResponse` dengan `content_type="application/json"`.

**006 / Tugas 3 - Debugging proses Update:** https://chatgpt.com/share/6ab00afb-9404-83ec-9e2e-48af8ed7914c
Membantu menganalisis error `No Experience matches the given query` pada proses Update dengan menghubungkan ID yang terdapat pada URL dengan object `Experience` yang dicari pada database.

**007 / Tugas 3 - Verifikasi branch dan proses merge Git:** https://chatgpt.com/share/6ab00afb-9404-83ec-9e2e-48af8ed7914c
Membantu memahami tampilan Git Graph setelah proses merge, termasuk alasan branch dan riwayat commit yang telah di-merge masih terlihat pada repository.

**008 / Tugas 3 - Sinkronisasi repository lokal dengan GitHub:** https://chatgpt.com/share/6ab00afb-9404-83ec-9e2e-48af8ed7914c
Membantu menjelaskan fungsi `git pull origin main`, perbedaan `git pull` dan `git push`, serta penggunaan `git status` untuk memverifikasi bahwa branch `main` lokal telah sinkron dengan `origin/main`.

### **5. Evaluasi Kritis terhadap Penggunaan AI**
AI digunakan sebagai alat bantu pembelajaran, konsultasi teknis, dan verifikasi, bukan sebagai pengganti proses pemrograman yang saya lakukan. Dalam pengerjaan Tugas 3, AI membantu memahami konsep **ModelForm, Update, CSRF, JSON, serialization, data delivery, serta Git dan GitHub**. Penggunaan AI dilakukan secara iteratif dan kontekstual dengan memberikan permasalahan atau kondisi aktual, kemudian mengajukan pertanyaan lanjutan untuk memperdalam pemahaman dan memverifikasi solusi.
Saya tidak menerapkan seluruh saran AI secara langsung, tetapi terlebih dahulu memahami dan menyesuaikannya dengan struktur serta kebutuhan proyek. Hasil implementasi kemudian diverifikasi melalui pengujian aplikasi dan pemeriksaan repository menggunakan Git. Dengan demikian, AI berperan sebagai **pendukung proses pembelajaran dan pemecahan masalah teknis**, sedangkan implementasi, pengujian, verifikasi, dan pengambilan keputusan akhir tetap dilakukan oleh saya.

### Tugas 4
### **AI Disclosure - Tugas 4**
AI digunakan dalam proyek ini sebagai sarana pendukung dalam memahami konsep autentikasi dan otorisasi Django, penggunaan Group dan Permission, *server-side authorization*, HTTP 403 Forbidden, serta keamanan form menggunakan CSRF. Keputusan dan implementasi akhir tetap dilakukan oleh saya berdasarkan kebutuhan dan kondisi proyek.

### **1. Alat AI yang Digunakan**
* **ChatGPT** (Model Bahasa / AI Assistant)

### **2. Ruang Lingkup Bantuan AI**
* **Role & Permission Django:** Membantu memahami penggunaan ``Group`` dan ``Permission`` untuk membuat role Editor serta membedakan hak akses berdasarkan permission.
* **Server-Side Authorization:** Membantu memahami penggunaan ``has_perm()`` dan ``permission_required`` untuk membatasi akses terhadap action tertentu serta menghasilkan HTTP 403 Forbidden.
* **Pengujian Hak Akses:** Membantu menentukan skenario pengujian untuk setiap role serta cara memverifikasi status HTTP melalui Network tab pada browser.
* **Keamanan Form:** Membantu memahami fungsi CSRF pada form ``POST`` Star/Unstar serta perbedaanya dengan authentication dan permission.
* **UI/UX:** Membantu mengevaluasi konsistensi tampilan tombol Star pada bagian Education dan Experience berdasarkan state tombol.

### **3. Strategi *Prompting***
* **Contextual Prompting:** Memberikan konteks mengenai kebutuhan role Editor, struktur hak akses, tampilan antarmuka, serta kondisi implementasi agar AI dapat memberikan bantuan yang sesuai dengan proyek.
* **Iterative & Conversational Prompting:** Mengajukan pertanyaan secara bertahap berdasarkan respons AI untuk memperjelas implementasi, terutama mengenai role, permission, dan keamanan aplikasi.
* **Problem-Based Questioning:** Mengajukan permasalahan teknis secara spesifik, seperti penggunaan ``has_perm()``, penambahan role melalui Django Admin, pengujian HTTP 403, serta keamanan from Star/Unstar.
* **Verification Prompting:** Meminta cara untuk memverifikasi pembatasan hak ases melalui status HTTP dan pengujian langsung pada aplikasi.
* **UI Evaluation Prompting:** Memberikan kondisi dan tampilan aktual dari proyek untuk memperoleh masukan mengenai konsistensi warna dan state tombol Star pada bagian Education dan Experience.
* **Conceptual Follow-up:** Mengajukan pertanyaan lanjutan unntuk memahami alasan dibalik penggunaan *permission-based check* dan perbedaan fungsi CSRF, authentication, dan permission.

### **4. Log *Prompting* AI**
Penggunaan AI dalam Tugas 3 didokumentasikan untuk menunjukkan bagian-bagian proses pengembangan yang mendapatkan bantuan AI.

**Format Log:** `[ID] / [Tugas] - [Deskripsi Penggunaan AI]: [Link ke Chat]`

Keterangan:
- **ID** = nomor urut interaksi AI.
- **Tugas** = nomor tugas/tutorial yang dikerjakan.
- **Deskripsi Penggunaan AI** = ringkasan tujuan atau topik bantuan AI.
- **Link ke Chat** = tautan menuju percakapan AI yang digunakan

**001 / Tugas 4 - Perancangan role Editor menggunakan Group dan Permission:** https://chatgpt.com/share/6ab92506-7624-83ec-9f91-bda88225bbfb
Membantu memahami cara membuat role Editor menggunakan fitur ``Group`` dan ``Permission`` yang disediakan Django serta menentukan permission yang sesuai untuk role tersebut.

**002 / Tugas 4 - Pembatasan hak akses berdasarkan role:** https://chatgpt.com/share/6ab92506-7624-83ec-9f91-bda88225bbfb
Membantu memahami perbedaan hak akses antara User, Editor, dan Admin serta penyesuaian action yang dapat dilakukan masing-masing role.

**003 / Tugas 4 - Pengujian server-side authorization dan HTTP 403 Forbidden:** https://chatgpt.com/share/6ab92506-7624-83ec-9f91-bda88225bbfb
Membantu memahami cara memastikan pembatasan hak akses dilakukan di sisi server, termasuk pengujian akses endpoint yang tidak diizinkan dan verifikasi bahwa server mengembalikan HTTP 403 Forbidden.

**004 / Tugas 4 - Penyusunan skenario pengujian role:** https://chatgpt.com/share/6ab92506-7624-83ec-9f91-bda88225bbfb
Membantu menyusun skenario pengujian untuk Guest, User, Editor, dan Admin dengan membandingkan action yang diperbolehkan dan hasil yang diharapkan.

**005 / Tugas 4 - Keamanan form Star/Unstar** https://chatgpt.com/share/6ab92506-7624-83ec-9f91-bda88225bbfb
Membantu memahami fungsi CSRF token pada form ``POST`` Star/Unstar serta perbedaan antara perlindungan CSRF, authentication, dan permission dalam mengamankan suatu action.

**006 / Tugas 4 - Konsultasi konsistensi UI tombol Star:** https://chatgpt.com/share/6ab92506-7624-83ec-9f91-bda88225bbfb
Membantu mengevaluasi perbedaan warna tombol Star pada bagian Education dan Experience serta menentukan pendekatan styling berdasarkan state tombol agar tampilan lebih konsisten.

### **5. Evaluasi Kritis terhadap Penggunaan AI**
AI digunakan dalam membantu pemahaman terkait konsep role, permission, *server-side authorization*, HTTP 403 Forbidden, serta keamanan CSRF pada form Star/Unstar. Setiap saran dari AI tetap saya sesuaikan dengan kondisi dan kebutuhan proyek. Implementasi, pengujian aplikasi, verifikasi hasil, dan pengambilan keputusan akhir tetap dilakukan oleh saya. Dengan demikian, AI berperan sebagai pendukung proses pembelajaran dan pemecahan masalah, sedangkan hasil akhir proyek tetap merupakan hasil pengembangan dan keputusan saya.

### Tugas 5
1. *Debouncing* merupakan teknik untuk menunda eksekusi suatu fungsi sampai tidak ada event baru selama jangka waktu tertentu. Fitur ini berguna agar browser tidak langsung mengirim request AJAX setiap kali pengguna mengetik satu karakter. Teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX untuk mengurangi request yang tidak perlu ke server sekaligus membuat pencarian tetap terasa responsif.
2. ``await`` pada ``fetch()`` berfungsi untuk menunggu sampai proses pengambilan data dari server selesai sebelum menjalankan kode berikutnya. ``fetch()`` sendiri bersifat *asynchronous* dan menghasilkan ``Promise``. Jika ``await`` tidak digunakan, program tidak menunggu proses tersebut selesai sehingga baris berikutnya langsung dijalankan, dan hasil dari ``fetch()`` yang diperoleh masih berupa ``Promise``, bukan respons dari server.
3. XSS (Cross-Site Scripting) adalah suatu serangan yang dilakukan dengan cara menyisipkan kode JavaScript berbahaya ke dalam halaman web sehingga dapat dijalankan oleh pengguna lain. Pada Django, *auto-escaping* digunakan dalam perlindungan data sehingga karakter ``<`` dan ``>`` tidak langsung dianggap sebagai tag HTML. Namun apabila menggunakan AJAX, data JSON dapat dimasukkan langsung ke HTML melalui JavaScript, sehingga *auto-escaping* Django tidak berlaku. Akibatnya jika terdapat data yang mengandung kode berbahaya, kode tersebut dapat dijalankan oleh browser, sehingga data dari AJAX perlu di-*escape* terlebih dahulu sebelum ditampilkan.

### **AI Disclosure Tugas 5**
AI digunakan dalam proyek ini sebagai sarana pendukung dalam memahami konsep penggunaan ``fetch()``, penanganan HTTP response, ``response.ok``, ``await``, *debouncing*, dan ``AbortController``. Keputusan dan implementasi akhir tetap dilakukan oleh saya berdasarkan kebutuhan dan kondisi proyek.

### **1. Alat AI yang Digunakan**
* **ChatGPT** (Model Bahasa / AI Assistant)

### **2. Ruang Lingkup Bantuan AI**
* **``fetch()`` dan ``response.ok``**:  Membantu memahami mengapa response dengan status HTTP seperti 403 tidak otomatis menyebabkan ``fetch()`` masuk ke ``catch()``, serta memahami fungsi ``response.ok``.
* **``await`` pada ``fetch()``**: Membantu memahami fungsi ``await`` ketika digunakan bersama ``fetch()``.
* **Debouncing**: Membantu memahami cara kerja *debouncing* dan alasan penggunaannya pada fitur pencarian.
* **AbortController**: Membantu memahami fungsi ``AbortController`` dalam membatalkan request ``fetch()`` yang sedang berjalan serta perbedaannya dengan *debouncing*.
* **Debugging**: Membantu mengidentifikasi penyebab error berdasarkan hasil yang muncul setelah implementasi dijalankan.

### **3. Strategi *Prompting***
* **Problem-Based Questioning**: Mengajukan pertanyaan mengenai perilaku ``fetch()`` ketika menerima HTTP response seperti 403 serta fungsi ``response.ok``.
* **Conceptual Follow-up**: Mengajukan pertanyaan lanjutan untuk memahami cara kerja ``await``, *debouncing*, dan ``AbortController``.
* **Comparative Prompting**: Membandingkan fungsi *debouncing* dengan ``Abort Controller`` untuk memahami perbedaan fungsi keduanya dalam proses request.
* **Verification Prompting**: Menggunakan penjelasan AI untuk memeriksa pemahaman terhadap alur ``fetch()``, ``catch()``, *debouncing*, dan pembatalan request.

### **4. Log *Prompting* AI**
Penggunaan AI dalam Tugas 5 didokumentasikan untuk menunjukkan bagian-bagian proses pengembangan yang mendapatkan bantuan AI.

**Format Log:** `[ID] / [Tugas] - [Deskripsi Penggunaan AI]: [Link ke Chat]`

Keterangan:
- **ID** = nomor urut interaksi AI.
- **Tugas** = nomor tugas/tutorial yang dikerjakan.
- **Deskripsi Penggunaan AI** = ringkasan tujuan atau topik bantuan AI.
- **Link ke Chat** = tautan menuju percakapan AI yang digunakan

**001 / Tugas 5 - Memahami ``fetch()`` dan HTTP error**: https://chatgpt.com/share/6ac35d6c-4948-83ec-a928-b283d5cf67ed
Membantu memahami mengapa  ``fetch()`` tidak otomatis masuk ke ``catch()`` ketika server mengembalikan status HTTP seperti 403, serta memahami fungsi ``response.ok`` dalam mengecek keberhasilan HTTP response.

**002 / Tugas 5 - Memahami penggunaan ``await`` pada ``fetch()``**: https://chatgpt.com/share/6ac35d6c-4948-83ec-a928-b283d5cf67ed
Membantu memahami fungsi ``await`` ketika digunakan bersama ``fetch()`` serta apa yang terjadi apabila ``await`` tidak digunakan.

**003 / Tugas 5 - Memahami cara kerja debouncing**:https://chatgpt.com/share/6ac35d6c-4948-83ec-a928-b283d5cf67ed
Membantu memahami cara kerja *debouncing*, terutama penggunaan ``clearTimeout()`` dan ``setTimeout()`` untuk menunggu hingga pengguna berhenti mengetik sebelum menjalankan request.

**004 / Tugas 5 - Memahami fungsi ``AbortController``**: https://chatgpt.com/share/6ac35d6c-4948-83ec-a928-b283d5cf67ed
Membantu memahami fungsi ``AbortController`` untuk membatalkan request ``fetch()`` yang masih berjalan serta cara penggunaannya bersama ``signal``.

**005 / Tugas 5 - Perbedaan debouncing dan ``AbortController``**: https://chatgpt.com/share/6ac35d6c-4948-83ec-a928-b283d5cf67ed
Membantu memahami perbedaan fungsi *debouncing* dan ``AbortController``, yaitu *debouncing* untuk mengatur kapan request dikirim, sedangkan ``AbortController`` untuk membatalkan request yang sudah terlanjur dikirim.

**006 / Tugas 5 - Identifikasi error setelah menjalankan implementasi**: https://chatgpt.com/share/6ac35d6c-4948-83ec-a928-b283d5cf67ed
Mengirimkan hasil atau kondisi error yang muncul setelah menjalankan implementasi untuk membantu mengidentifikasi bagian yang menyebabkan error dan memahami penyebabnya.

### **5. Evaluasi Kritis terhadap Penggunaan AI**
AI digunakan untuk membantu memahami konsep ``fetch()``, ``response.ok``, ``await``, *debouncing*, dan ``AbortController``serta membantu mengidentifikasi penyebab error yang muncul saat implementasi dijalankan. Penjelasan dari AI digunakan sebagai bahan untuk memahami konsep, mengevaluasi permasalahan, dan memeriksa pemahaman terhadap implementasi yang digunakan.

#### Tugas 6
1. **REST (Representational State Transfer)** adalah gaya arsitektur untuk merancang web API yang mengatur komunikasi antara client dan server. Dalam REST, data diperlakukan sebagai *resource* yang diidentifikasi oleh URL, sedangkan HTTP method menentukan operasi yang dilakukan: `GET` untuk membaca, `POST` untuk menambahkan, `PUT`/`PATCH` untuk memperbarui, dan `DELETE` untuk menghapus. Server tidak menyimpan keadaan client di antara request (*stateless*), dan hasil setiap operasi dinyatakan lewat status code HTTP.
**Mengapa JSON saja belum cukup.** JSON hanyalah format pertukaran data, bukan aturan dalam merancang API. Sebuah endpoint bisa mengembalikan JSON tetapi tetap tidak RESTful. API disebut RESTful apabila juga mengikuti prinsip REST:
   - URL berbasis resource (kata benda), bukan perintah.
   - HTTP method sesuai fungsinya.
   - Status code yang tepat, misalnya `201` saat data dibuat, `400` untuk input tidak valid, `403` untuk tindakan yang tidak diizinkan, `404` untuk data yang tidak ditemukan, dan `204` setelah data dihapus.
Sebagai pembanding pada proyek ini:
   | | Tidak RESTful | RESTful |
   |---|---|---|
   | Menghapus data | `POST /education/3/delete/` | `DELETE /api/v1/education/3/` |
   | Respons sukses | JSON dengan status `200` | Body kosong dengan status `204` |

   Endpoint pertama mengembalikan JSON, tetapi operasi hapus ditulis di URL dan memakai method yang tidak sesuai. Endpoint kedua menyatakan operasinya lewat method dan hasilnya lewat status code.

   **Adapun perbedaan `PUT` dan `PATCH`antara lain:**
   - `PUT` mengganti **seluruh** data suatu resource, sehingga semua field wajib dikirim. Bila ada field wajib yang tidak dikirim, request ditolak dengan `400`.
     ```
     PUT /api/v1/education/3/
     {"title": "SMA Negeri 1", "description": "IPA", "category_edu": "Senior High School",
      "start_year": 2020, "end_year": 2023, "is_ongoing": false}
     ```
     `PUT` cocok dipakai saat client memegang data lengkap dan ingin menggantinya sekaligus, misalnya form edit yang mengirim semua isian.

   - `PATCH` memperbarui **sebagian** field saja, sedangkan field lain tidak berubah.
     ```
     PATCH /api/v1/education/3/
     {"title": "SMA Negeri 2"}
     ```
     `PATCH` cocok dipakai saat hanya satu atau beberapa field yang berubah, misalnya mengganti judul tanpa menyentuh deskripsi dan tahun.
   Dengan demikian, `PUT` sesuai untuk penggantian data secara keseluruhan, sedangkan `PATCH` lebih sesuai untuk perubahan sebagian.

2. **Serializer** adalah komponen DRF yang menjadi penghubung antara data di aplikasi (objek model Django) dan data yang dipertukarkan lewat API. Serializer bekerja dua arah:
- **Serialization:** Mengubah objek model menjadi tipe data Python yang dapat dikirim melalui API. Contohnya pada `GET /api/v1/education/`.
- **Deserialization:** Mengubah input yang dikirim client menjadi data yang sudah divalidasi sebelum disimpan melalui `is_valid()`, dan ``save(()``, misalnya pada `POST`, `PUT`, dan `PATCH`.
Penggunaan serializer memiliki beberapa kelebihan dibandingkan membuat dictionary secara manual dengan `JsonResponse` seperti pada Tutorial 05:
- **Lebih praktis:** Struktur data cukup didefinisikan sekali menggunakan `ModelSerializer`, sehingga tidak perlu menyusun dictionary berulang kali.
- **Validasi dilakukan secara otomatis:** Aturan validasi dapat ditulis langsung di serializer dan digunakan kembali pada berbagai operasi.
- **Mudah dikelola:** Field yang ditampilkan, bersifat *read-only*, atau membutuhkan perhitungan tambahan dapat diatur dalam satu tempat.
- **Pesan error lebih konsisten:** DRF dapat mengembalikan pesan kesalahan untuk setiap field jika data tidak valid.
Dengan demikian, serializer membuat pengelolaan data API lebih ringkas, konsisten, dan mudah dikembangkan dibandingkan menyusun response secara manual menggunakan ``JsonResponse`.

3. **Autentikasi** adalah proses memverifikasi identitas pengguna, yaitu memastikan siapa yang mengirim request. Pada proyek ini, tugas itu dilakukan oleh `SessionAuthentication`, yang membaca sesi login lalu mengisi `request.user`.
**Otorisasi** adalah proses menentukan apa yang boleh dilakukan oleh pengguna yang sudah dikenali. Pada proyek ini:
- Tamu dan user biasa hanya bisa membaca.
- Editor dapat melakukan `PUT` dan `PATCH`.
- Pemilik (superuser) boleh membuat, mengubah, dan menghapus.
Hak akses harus diperiksa dengan *permission class* di server, karena menyembunyikan tombol di template hanya mengubah tampilan dan tidak melindungi data. Kode HTML dan JavaScript yang berjalan di browser bisa diubah lewat DevTools, atau dilewati sepenuhnya dengan mengirim request langsung memakai `fetch()`, Postman, atau `curl`.
Permission class menjalankan `has_permission` sebelum isi view dijalankan, dan menolak request dengan status 403 jika tidak diizinkan. Dengan begitu, data tetap terlindungi. Menyembunyikan tombol tetap berguna untuk kenyamanan pengguna, tetapi hanya sebagai pelengkap.

4. Alasan mengapa token CSRF tetap diperlukan adalah karena `SessionAuthentication` mengenali pengguna melalui *cookie session*, dan browser mengirim cookie ini otomatis pada setiap request ke situs yang sama, termasuk yang dipicu oleh situs lain. Jika pengguna sedang login lalu membuka halaman berbahaya, halaman itu dapat membuat browser mengirim `DELETE /api/v1/education/3/`, dan server menganggapnya sah. Serangan ini disebut *Cross-Site Request Forgery* (CSRF). Karena itu, request yang mengubah data wajib membawa token lewat header `X-CSRFToken` yang cocok dengan cookie `csrftoken`. Situs lain tidak bisa membaca token ini, sehingga request tanpa token yang benar ditolak dengan `403`.
`force_authenticate` tidak cukup karena `force_authenticate` memasang user langsung ke request tanpa menjalankan `SessionAuthentication`, padahal pemeriksaan CSRF (`enforce_csrf`) ada di dalamnya. `APIClient` juga tidak memeriksa CSRF secara bawaan. Akibatnya, test tetap lulus walaupun perlindungan CSRF rusak, sehingga tidak membuktikan apa pun. Pembuktian yang benar memakai `enforce_csrf_checks=True` dan `.login()`:
```python
client = APIClient(enforce_csrf_checks=True)
client.login(username="owner", password="test-password")
response = client.post(url, payload, format="json")  
assert response.status_code == 403
```
### **AI Disclosure Tugas 6**
AI digunakan dalam proyek ini sebagai sarana pendukung dalam memahami konsep Django REST Framework, penggunaan decorator pada API view, struktur pengujian API, serta perbedaan JSON dan prinsip REST. Keputusan dan implementasi akhir tetap dilakukan oleh saya berdasarkan kebutuhan dan kondisi proyek.

### **1. Alat AI yang Digunakan**
* **ChatGPT** (Model Bahasa / AI Assistant)

### **2. Ruang Lingkup Bantuan AI**
* **Serializer DRF:** Membantu memahami perbedaan ``read_only_fields`` dan ``SerializerMethodField``, serta penerapan ``SerializerMethodField`` untuk menghitung jumlah star (``star_count``) dan status star pengguna (``is_starred``).
* **Decorator API View:** Membantu memahami fungsi ``@api_view``, ``@authentication_classes``, dan ``@permission_classes`` dalam mengatur HTTP method, autentikasi, dan hak akses.
* **Debugging:** Membantu mengidentifikasi penyebab error ``ImproperlyConfigured`` pada ``EducationSerializer`` berdasarkan pesan error yang muncul.
* **Pengujian API:** Membantu memahami struktur test Education dan Experience dalam satu file ``tests_api.py`` serta cara menjalankan test per file maupun per class.
* **Konsep REST:** Membantu memahami mengapa JSON hanyalah format data dan API yang mengembalikan JSON belum tentu RESTful.

### **3. Strategi *Prompting***
* **Conceptual Questioning:** Mengajukan pertanyaan mengenai perbedaan ``read_only_fields`` dan ``SerializerMethodField`` untuk memahami fungsi dan kapan masing-masing digunakan.
* **Confirmation Prompting:** Menyampaikan pemahaman sendiri, seperti penerapan ``SerializerMethodField`` pada fitur star, untuk memastikan pemahaman tersebut sudah benar.
* **Code Explanation Prompting:** Mengirimkan potongan kode decorator pada API view untuk meminta penjelasan fungsi setiap bagiannya.
* **Problem-Based Questioning:** Mengirimkan tangkapan layar error pada ``EducationSerializer`` untuk membantu menemukan penyebabnya.
* **Clarification Follow-up:** Mengajukan pertanyaan lanjutan ketika bagian tertentu belum dipahami, seperti alasan JSON belum tentu RESTful.

### **4. Log *Prompting* AI**
Penggunaan AI dalam Tugas 6 didokumentasikan untuk menunjukkan bagian-bagian proses pengembangan yang mendapatkan bantuan AI.

**Format Log:** `[ID] / [Tugas] - [Deskripsi Penggunaan AI]: [Link ke Chat]`

Keterangan:
- **ID** = nomor urut interaksi AI.
- **Tugas** = nomor tugas yang dikerjakan.
- **Deskripsi Penggunaan AI** = ringkasan tujuan atau topik bantuan AI.
- **Link ke Chat** = tautan menuju percakapan AI yang digunakan

**001 / Tugas 6 - Memahami perbedaan ``read_only_fields`` dan ``SerializerMethodField``**: https://chatgpt.com/share/6af18804-bdac-83ec-891c-8ec0954798ed
Membantu memahami perbedaan ``read_only_fields``, yang membatasi field model agar tidak bisa diubah lewat request, dengan ``SerializerMethodField``, yang membuat field tambahan dari hasil method Python, serta kapan masing-masing digunakan pada serializer Education.

**002 / Tugas 6 - Menerapkan ``SerializerMethodField`` untuk fitur star**: https://chatgpt.com/share/6af18804-bdac-83ec-891c-8ec0954798ed
Membantu memahami cara menggunakan ``SerializerMethodField`` untuk menghitung jumlah star (``star_count``) dan mengecek apakah pengguna yang login sudah memberi star (``is_starred``), serta memahami bahwa perubahan star tetap membutuhkan endpoint tersendiri.

**003 / Tugas 6 - Memahami decorator pada API view**: https://chatgpt.com/share/6af18804-bdac-83ec-891c-8ec0954798ed
Membantu memahami fungsi ``@api_view``, ``@authentication_classes``, dan ``@permission_classes``, yaitu mengatur HTTP method yang diterima, cara autentikasi, dan hak akses, serta memperbaiki penulisan ``permission_classes`` yang seharusnya berupa list.

**004 / Tugas 6 - Identifikasi error ``ImproperlyConfigured`` pada ``EducationSerializer``**: https://chatgpt.com/share/6af18804-bdac-83ec-891c-8ec0954798ed
Mengirimkan tangkapan layar error "Field name ``idtitle`` is not valid for model ``Education``" untuk membantu mengidentifikasi kemungkinan penyebabnya, yaitu koma yang hilang di daftar ``fields`` sehingga dua string tergabung menjadi satu.

**005 / Tugas 6 - Struktur test untuk Education**: https://chatgpt.com/share/6af18804-bdac-83ec-891c-8ec0954798ed
Membantu memahami bahwa test Education boleh digabung dengan test Experience dalam satu file ``tests_api.py`` selama berada di app yang sama, dengan memisahkannya per class, serta cara menjalankan test per file maupun per class.

**006 / Tugas 6 - Memahami mengapa JSON belum tentu RESTful**: https://chatgpt.com/share/6af18804-bdac-83ec-891c-8ec0954798ed
Membantu memahami bahwa JSON hanyalah format data, sedangkan REST adalah cara merancang API berbasis resource dan HTTP method, sehingga API yang mengembalikan JSON belum tentu mengikuti prinsip REST.

### **5. Evaluasi Kritis terhadap Penggunaan AI**
AI digunakan untuk membantu memahami konsep Django REST Framework, struktur pengujian API, dan prinsip REST, serta mengidentifikasi penyebab error saat implementasi. Setiap saran dari AI saya periksa dan sesuaikan dengan kondisi proyek. Implementasi, pengujian, dan keputusan akhir tetap dilakukan oleh saya, sehingga AI hanya berperan sebagai pendukung proses belajar dan pemecahan masalah.