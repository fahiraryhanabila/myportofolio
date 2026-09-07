Name    : Fahira Ryhanabila
NPM     : 2506623660
Class   : PBP E

## Tentang Proyek
Sebuah website portofolio personal yang interaktif dan responsif, guna memenuhi tugas individu (*Individual Assignment*) mata kuliah Pemograman Berbasis Platform (PBP).

Konten pada halaman portofolio ini meliputi:
- **Hero Section**: Menampilkan identitas utama (nama, program studi, NPM), tagline personal, serta tautan menuju GitHub, LinkedIn, dan Email, dengan latar belakang visual bertema kampus.
- **Credentials Section**: Menampilkan logo dan nama kepanitiaan yang pernah diikuti (Open House Fasilkom UI 2025, BETIS Fasilkom UI, COMPFEST 18, FUKI Fasilkom UI) dalam tata letak sejajar.
- **About Me Section**: Perkenalan singkat mengenai diri saya, dilengkapi highlight area keahlian (Product Management, UX & Research, Technology & Business) beserta ikon masing-masing.
- **Interactive Skills Section**: Tata letak 2 kolom (Hard Skills & Soft Skills) berbentuk kartu (*card*) yang dapat diklik untuk efek "terangkat" (*is-raised*), serta menampilkan deskripsi tambahan saat *hover*.
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
    pip install-r requirements.txt
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

## Assets & Credits
- Ikon menggunakan **[Lucide Icons](https://lucide.dev/)**, dimuat melalui CDN.
- Font **Poppins** dari [Google Fonts](https://fonts.google.com/specimen/Poppins).

## Progress Tugas Mingguan

### Tugas 1
1. Dalam pengerjaan Tutorial 1 dan Tugas 1, saya menggunakan beberapa elemen semantik HTML5 seperti `<header>`, `<nav>`, `<main>`, `<section>`, dan `<footer>` untuk menyusun struktur halaman. Elemen-elemen tersebut memudahkan saya dalam membuat static web terutama pada aspek keterbacaan dan aksesibilitas kode. Pada aspek keterbacaan, saya dapat dengan mudah mengidentifikasi satu-satu elemen kode sehingga akan sangat efisien dan efektif dalam melakukan debugging.  Elemen semantik juga membantu aksesibilitas, karena *screen reader* dan mesin pencari bisa lebih mudah memahami struktur dan hierarki.
Namun, dalam pengerjaan Tugas 1 ini, saya belum sepenuhnya konsisten menerapkan elemen semantik di semua bagian. Misalnya, untuk bagian *skill-card* atau *credential card* dimana saya masih menggunakan `<div>` biasa alih-alih `<article>`. karena pada saat itu saya fokus pada tampilan dari konten, padahal jika dipikirkan lebih dalam lagi, kedua hal tersebut lebih cocok dibungkus dengan <article>. Hal ini akan menjadi catatan perbaikan untuk iterasi berikutnya.

2. Tantangan utama yang saya temukan saat mengatur CSS agar *responsive* bukan hanya soal ukuran elemen yang mengecil, tapi juga soal perubahan layout dan urutan elemen antara desktop dan mobile. Contohnya, pada bagian Hero, saya awalnya menyusun identitas, foto, dan detail menggunakan CSS Grid dengan area yang saling bersebelahan (grid-template-columns), tapi di layar mobile susunan seperti itu jadi terlalu sempit dan berantakan. Saya kemudian menggunakan `@media (max-width: 600px)` untuk mengubah `grid-template-columns` menjadi satu kolom penuh.
Tantangan lain adalah menentukan elemen mana yang prioritas ukurannya harus fleksibel. Untuk judul-judul besar (seperti nama saya di Hero atau judul section), saya menggunakan fungsi `clamp()` pada `font-size` agar ukuran teks otomatis menyesuaikan lebar layar.
Evaluasi yang saya lakukan biasanya dengan langsung membuka *DevTools* dan mengecek tampilan di berbagai lebar layar, lalu menentukan breakpoint.

3. Website yang saya buat saat ini adalah *static web* murni, sehingga ada beberapa batasan yang saya rasakan saat mencoba menyajikan informasi secara optimal. Di awal saya berencana ingin menambahkan section *Experiences*. Namun, saya belum mengetahui cara untuk menyimpan dan menampilkan data secara dinamis menggunakan JavaSCript. Selain itu, interaktivitas yang sudah ada seperti *toggle* pada *skill-card* masih lumayan biasa.
Adapun Fungnsionalitas dinamis yang ingin saya tambahkan pada iterasi selanjutnya adalah:
    -Navigasi aktif dengan higlight modern
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