Name    : Fahira Ryhanabila
NPM     : 2506623660
Class   : PBP E

## Tentang Proyek
Sebuah website portofolio personal yang interaktif dan responsif, guna memenuhi tugas individu (*Individual Assignment*) mata kuliah Pemrograman Berbasis Platform (PBP).

Konten pada halaman portofolio ini meliputi:
- **Hero Section**: Menampilkan identitas utama (nama, program studi, NPM), tagline personal, serta tautan menuju GitHub, LinkedIn, dan Email, dengan latar belakang visual bertema kampus.
- **Credentials Section**: Menampilkan logo dan nama kepanitiaan yang pernah diikuti (Open House Fasilkom UI 2025, BETIS Fasilkom UI, COMPFEST 18, FUKI Fasilkom UI) dalam tata letak sejajar.
- **About Me Section**: Perkenalan singkat mengenai diri saya, dilengkapi highlight area keahlian (Product Management, UX & Research, Technology & Business) beserta ikon masing-masing.
- **Interactive Skills Section**: Tata letak 2 kolom (Hard Skills & Soft Skills) berbentuk kartu (*card*) yang dapat diklik untuk efek "terangkat" (*is-raised*), serta menampilkan deskripsi tambahan saat *hover*.
- **Experience Page**: Menampilkan riwayat pengalaman kepanitiaan, organisasi, dan volunteer dalam bentuk kartu, lengkap dengan kategori kegiatan (*part-time*, *internship*, *volunteer*, dsb.), status keberlangsungan (sedang berlangsung/selesai), dan gambar pendukung. Dilengkapi fitur pencarian berdasarkan nama kegiatan, serta fitur tambah, ubah, dan hapus data melalui form.
- **Education Page**: Menampilkan jenjang pendidikan yang pernah/sedang ditempuh dalam format *timeline*, mencakup jenjang pendidikan, tahun mulai dan selesai, deskripsi, serta daftar *skill* yang diperoleh pada tiap jenjang. Dilengkapi fitur pencarian, serta fitur tambah, ubah, dan hapus data melalui form.
- **Form & Data Delivery**: Data pada halaman Experience dan Education dikelola menggunakan `ModelForm` Django, dengan validasi otomatis dan proteksi CSRF pada setiap form. Data juga dapat diakses dalam format JSON melalui endpoint API (`/api/experience/` dan `/api/education/`), yang mendukung *query parameter* untuk pencarian berdasarkan judul.
- **Responsive Layout**: Tata letak menyesuaikan otomatis antara tampilan desktop dan mobile menggunakan CSS Grid, Flexbox, `clamp()` untuk ukuran font, dan `@media` *query* untuk perubahan susunan elemen.

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
    - Mengurangi duplikasi kode, terutama untuk Constraint yang banyak dipakai di beberapa file tanpa menulis ulang di HTML.
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

Alasan diperlukannya proses serialization pada model Django sebelum data dikembalikan, antara lain:
- Objek Python yang hidup di memori server tidak bisa dikirimkan secara langsung melalui protokol HTTP yang berbasis teks/byte.
- Mengubah objek internal Python menjadi format standar berbasis teks (JSON) agar dapat dibaca dan diproses oleh berbagai bahasa pemrograman atau platform lain (seperti *frontend* JavaScript, aplikasi *mobile*, dll).

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
