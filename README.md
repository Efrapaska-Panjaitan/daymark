# Daymark

Daymark adalah aplikasi Simple Task Tracker untuk mencatat tugas, mengubah detail dan statusnya, serta menghapus tugas. Aplikasi ini dibuat sebagai technical assessment REST API, integrasi PostgreSQL, frontend Vue, dan manajemen state.

## Fitur

- Melihat daftar tugas.
- Membuat tugas.
- Mengubah title, description, dan status tugas.
- Menghapus tugas dengan konfirmasi.
- Mempertahankan data PostgreSQL menggunakan Docker volume.

Status yang tersedia: `Todo`, `In Progress`, dan `Done`.

## Tech stack

- Frontend: Vue 3 Composition API, JavaScript, Vite, CSS biasa, Fetch API.
- Backend: Python 3.12, FastAPI, Pydantic, SQLAlchemy, Psycopg 3.
- Database: PostgreSQL 16.
- Container: Docker, Docker Compose, Nginx untuk menyajikan production build frontend.

## Struktur proyek

```text
daymark/
├── backend/
│   ├── app/
│   │   ├── api/routes/tasks.py
│   │   ├── core/config.py
│   │   ├── db/session.py
│   │   ├── models/task.py
│   │   ├── schemas/task.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── frontend/
│   ├── src/
│   │   ├── assets/styles.css
│   │   ├── components/
│   │   │   ├── TaskForm.vue
│   │   │   ├── TaskItem.vue
│   │   │   └── TaskList.vue
│   │   ├── services/taskService.js
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   ├── package-lock.json
│   ├── Dockerfile
│   └── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```
## Prasyarat

Untuk menjalankan aplikasi dengan Docker:

- Docker Engine.
- Docker Compose plugin.

Untuk menjalankan aplikasi tanpa Docker:

- Python 3.12 dan PostgreSQL 16.
- Node.js 24 dan npm.

## Konfigurasi environment

Salin .env.example menjadi .env di root repository jika file .env belum tersedia:

cp .env.example .env

Jika .env sudah berisi konfigurasi lokal, jangan menimpanya. Tambahkan atau sesuaikan variabel yang diperlukan. Jangan commit .env.

Variabel yang dipakai:

| Variabel | Fungsi |
|---|---|
| POSTGRES_DB | Nama database untuk service PostgreSQL Compose. |
| POSTGRES_USER | User database lokal. |
| POSTGRES_PASSWORD | Password database lokal. |
| DATABASE_URL | URL database untuk backend yang dijalankan langsung di host; host biasanya localhost. |
| DATABASE_URL_DOCKER | URL database untuk backend di Compose; hostname database adalah db dan port internalnya 5432. |
| CORS_ORIGINS | Daftar origin frontend yang diizinkan backend, dipisahkan dengan koma. |
| VITE_API_BASE_URL | URL API yang ditanam ke bundle frontend saat build; untuk Compose lokal, gunakan http://localhost:8000. |

Contoh format URL Docker:

postgresql+psycopg://<user>:<password>@db:5432/<database>

Jika password mengandung karakter khusus URL, encode karakter tersebut pada URL database. DBeaver menggunakan password mentahnya.

Untuk menjalankan Vite tanpa Docker, salin frontend/.env.example menjadi frontend/.env. File environment frontend hanya berisi konfigurasi publik seperti VITE_API_BASE_URL; jangan masukkan credential database ke sana.

## Menjalankan dengan Docker Compose

Dari root repository:

docker compose up --build -d

Periksa status service:

docker compose ps

Akses aplikasi:

- Frontend: http://localhost:5173
- FastAPI Swagger UI: http://localhost:8000/docs

Lihat log service:

docker compose logs -f db backend frontend

Compose menjalankan service db, backend, dan frontend. Backend tersambung ke PostgreSQL melalui hostname internal db:5432. Browser mengakses API melalui localhost:8000.

Database tidak perlu memublikasikan port agar aplikasi bekerja. Untuk koneksi lokal DBeaver, konfigurasi Compose Daymark memetakan port host 55432 ke port container 5432:

- Host: 127.0.0.1
- Port: 55432
- Database: nilai POSTGRES_DB
- Username: nilai POSTGRES_USER
- Password: nilai POSTGRES_PASSWORD

DBeaver menggunakan port host. Backend container tetap menggunakan db:5432.

### Menghentikan dan menjalankan kembali

Menghentikan service:

docker compose stop

Menjalankan kembali container yang sudah ada:

docker compose start

Menghapus container dan network tetapi mempertahankan named volume database:

docker compose down

Setelah down, gunakan docker compose up -d untuk membuat dan menjalankan container kembali.

Peringatan: docker compose down -v menghapus named volume PostgreSQL beserta datanya. Gunakan hanya jika memang ingin menghapus database lokal secara permanen.

## Database

Docker Compose memakai PostgreSQL 16 dengan named volume agar data tetap tersedia setelah container dihentikan atau dibuat ulang.

Backend menjalankan Base.metadata.create_all() saat aplikasi dimulai. Mekanisme tersebut membuat tabel yang belum ada di database; ia tidak membuat server PostgreSQL atau database target, dan tidak memperbarui struktur tabel yang telah ada. Proyek ini tidak menggunakan Alembic.

## REST API

Base URL backend lokal: http://localhost:8000.

| Method | Endpoint | Fungsi | Response sukses |
|---|---|---|---|
| GET | /tasks | Mengambil daftar task. | 200 OK, array task atau []. |
| POST | /tasks | Membuat task. | 201 Created, task beserta ID. |
| PUT | /tasks/{id} | Memperbarui title, description, dan status. | 200 OK, task terbaru. |
| DELETE | /tasks/{id} | Menghapus task. | 204 No Content, tanpa response body. |

Contoh payload POST:

{
  "title": "Menyelesaikan REST API",
  "description": "Membuat endpoint CRUD menggunakan FastAPI",
  "status": "Todo"
}

PUT menerima seluruh representasi task:

{
  "title": "Menyelesaikan Backend API",
  "description": "Memperbarui implementasi endpoint CRUD",
  "status": "In Progress"
}

Task yang tidak ditemukan menghasilkan 404. Input yang tidak valid menghasilkan 422.

## Menjalankan tanpa Docker

Pastikan PostgreSQL lokal aktif, database sudah tersedia, dan DATABASE_URL di .env root menunjuk ke database host, biasanya localhost.

Jalankan backend dari direktori backend:

source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload

Di terminal terpisah, jalankan frontend:

cd frontend
npm ci
npm run dev

Vite tersedia di http://localhost:5173. Swagger UI tersedia di http://localhost:8000/docs. Jika mengubah environment variable Vite, restart development server.

Jangan menjalankan mode lokal dan Compose bersamaan jika keduanya memakai port host yang sama.

## Pengujian dasar

1. Buka frontend dan pastikan daftar task tampil.
2. Buat, edit, dan hapus task melalui UI.
3. Muat ulang halaman untuk memeriksa persistence.
4. Gunakan Swagger UI untuk menguji endpoint secara langsung.
5. Gunakan query berikut di DBeaver untuk memeriksa data:

   SELECT id, title, description, status
FROM tasks
ORDER BY id;

## Troubleshooting

- Port sudah dipakai: pilih port host lain yang kosong pada sisi kiri mapping Compose, lalu gunakan port tersebut di browser atau DBeaver. Port container PostgreSQL tetap 5432.
- Backend tidak menemukan db: jalankan service dari Compose yang sama dan periksa log backend. Di dalam Compose, gunakan hostname db, bukan localhost.
- DBeaver melihat database berbeda: gunakan 127.0.0.1 dan port host Compose, bukan port server PostgreSQL lokal atau hostname db.
- Password ditolak: PostgreSQL hanya memakai POSTGRES_PASSWORD saat volume pertama kali diinisialisasi. Perubahan .env berikutnya tidak otomatis mengganti password role pada volume yang sudah ada.
- Frontend tidak dapat mengakses API: pastikan backend tersedia di localhost:8000, origin frontend termasuk dalam CORS_ORIGINS, dan VITE_API_BASE_URL sudah diberikan saat build frontend.
- Perubahan VITE_API_BASE_URL tidak terlihat: nilai tersebut tertanam pada build Vite; bangun ulang image frontend.
- Data database tidak muncul: pastikan Compose menggunakan named volume yang sama dan jangan menghapus volume saat menjalankan down.

## Status proyek

Daymark mencakup CRUD task dengan frontend Vue dan REST API FastAPI yang menggunakan PostgreSQL. Docker Compose disediakan untuk penggunaan lokal. Dokumentasi ini tidak mencakup deployment cloud.

Lisensi proyek belum ditentukan.


### Pemeriksaan sebelum README dianggap final

Cocokkan project tree, nama variabel pada `.env.example`, port database DBeaver, serta Docker commands dengan file aktual. Secara khusus, pastikan Docker Compose memang memetakan host port `55432` ke container port `5432`. Isi bagian pengujian hanya dengan klaim yang sesuai hasil aktual.

Setelah kamu memasukkan dan memeriksa README, checkpoint lokalnya dapat dibuat dengan:

```bash
git status
git add README.md
git diff --staged
git commit -m "docs(project): finalize Docker documentation"

Jangan push ke GitHub pada tahap ini. Saya berhenti di 11.6 dan menunggu konfirmasi bahwa isi README sudah sesuai implementasi aktualmu.
  Worked for 1m 38s • 8:02 AM

Pastikan file
README.md di halaman utama sudah dilengkapi instruksi setup yang komprehensif.

Benar, README root perlu memandu setup dari awal sampai aplikasi dapat diuji. Saya tidak mengubah workspace secara langsung; berikut isi lengkap yang bisa kamu salin ke README.md di root repository. Isinya mencakup Docker Compose dan setup manual, tanpa instruksi deployment cloud.

# Daymark

Daymark adalah aplikasi Simple Task Tracker untuk mencatat tugas, mengubah detail dan statusnya, serta menghapus tugas. Proyek ini dibuat sebagai technical assessment REST API, integrasi PostgreSQL, frontend Vue, dan pengelolaan state.

## Fitur

- Menampilkan daftar task dari backend.
- Membuat task tanpa reload halaman penuh.
- Mengubah title, description, dan status task.
- Menghapus task setelah konfirmasi.
- Menyimpan data task di PostgreSQL.

Status yang tersedia: `Todo`, `In Progress`, dan `Done`.

## Tech stack

- Frontend: Vue 3 Composition API, JavaScript, Vite, CSS biasa, Fetch API.
- Backend: Python 3.12, FastAPI, Pydantic, SQLAlchemy, Psycopg 3.
- Database: PostgreSQL 16.
- Container: Docker, Docker Compose, Nginx untuk menyajikan production build frontend.

Dependency backend tercantum di `backend/requirements.txt`. Dependency frontend dikunci melalui `frontend/package-lock.json`.

## Struktur proyek

```text
daymark/
├── backend/
│   ├── app/
│   │   ├── api/routes/tasks.py
│   │   ├── core/config.py
│   │   ├── db/session.py
│   │   ├── models/task.py
│   │   ├── schemas/task.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── frontend/
│   ├── src/
│   │   ├── assets/styles.css
│   │   ├── components/
│   │   │   ├── TaskForm.vue
│   │   │   ├── TaskItem.vue
│   │   │   └── TaskList.vue
│   │   ├── services/taskService.js
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   ├── package-lock.json
│   ├── Dockerfile
│   └── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```
## Prasyarat

### Menjalankan dengan Docker Compose

- Docker Engine.
- Docker Compose plugin.

Python dan Node.js tidak diperlukan pada host untuk menjalankan seluruh aplikasi lewat Docker.

### Menjalankan dalam mode pengembangan lokal

- Python 3.12.
- Node.js 24 dan npm.
- PostgreSQL 16.

Pemeriksaan versi:

python3 --version
node --version
npm --version
docker --version
docker compose version

## Konfigurasi environment

Jangan commit file .env aktual. Repository menyediakan .env.example sebagai template.

Jika belum memiliki .env aktual, dari root repository jalankan:

cp .env.example .env

Jika .env sudah ada, edit file tersebut tanpa menimpanya. Isi nilai lokalmu; jangan menggunakan credential asli pada file contoh yang di-commit.

Variabel root .env:

| Variabel | Fungsi |
|---|---|
| POSTGRES_DB | Nama database untuk PostgreSQL Compose. |
| POSTGRES_USER | User PostgreSQL Compose. |
| POSTGRES_PASSWORD | Password PostgreSQL Compose. |
| DATABASE_URL | URL database untuk backend yang dijalankan langsung di host; hostname biasanya localhost. |
| DATABASE_URL_DOCKER | URL database untuk backend di Compose; gunakan hostname db dan port container 5432. |
| CORS_ORIGINS | Origin frontend yang diizinkan backend, misalnya http://localhost:5173. |
| VITE_API_BASE_URL | URL API yang ditanam ke bundle frontend saat build, untuk browser lokal http://localhost:8000. |

Contoh format URL:

# Backend langsung di host
postgresql+psycopg://<user>:<password>@localhost:5432/<database>

# Backend di Docker Compose
postgresql+psycopg://<user>:<password>@db:5432/<database>

Jika password mengandung karakter khusus URL, encode karakter tersebut pada URL database. DBeaver menggunakan password mentahnya.

Untuk frontend mode pengembangan, siapkan frontend/.env dari frontend/.env.example:

cp frontend/.env.example frontend/.env

File tersebut berisi konfigurasi publik seperti VITE_API_BASE_URL. Jangan masukkan password atau credential database ke variabel VITE_*.

## Menjalankan dengan Docker Compose

Dari root repository, bangun image dan jalankan semua service:

docker compose up --build -d

Periksa status:

docker compose ps

Harapkan service db berstatus Up (healthy), serta service backend dan frontend berstatus Up.

Akses aplikasi:

- Frontend: http://localhost:5173
- FastAPI Swagger UI: http://localhost:8000/docs

Lihat log:

docker compose logs -f db backend frontend

Compose menjalankan PostgreSQL, FastAPI, dan frontend production build. Backend mengakses PostgreSQL melalui hostname internal db:5432. Browser mengakses API melalui localhost:8000; hostname db tidak dapat digunakan oleh browser.

### Mengakses database melalui DBeaver

Pada konfigurasi Compose lokal, port host PostgreSQL dipetakan ke 55432. Gunakan:

- Host: 127.0.0.1
- Port: 55432
- Database: nilai POSTGRES_DB
- Username: nilai POSTGRES_USER
- Password: nilai POSTGRES_PASSWORD

Jika port host itu diubah karena bentrok, gunakan port host yang tercantum di docker-compose.yml. Port container PostgreSQL tetap 5432.

### Menghentikan dan menjalankan kembali

Menghentikan container tanpa menghapusnya:

docker compose stop

Menyalakan kembali container yang sudah ada:

docker compose start

Menghapus container dan network Compose, tetapi mempertahankan volume database:

docker compose down

Setelah down, jalankan kembali dengan docker compose up -d. Perintah start hanya menyalakan container yang sudah ada; perintah itu tidak membangun atau membuat ulang container.

Peringatan: docker compose down -v menghapus named volume PostgreSQL beserta datanya. Gunakan hanya jika memang ingin menghapus database lokal secara permanen.

## Menjalankan tanpa Docker

Mode ini memerlukan PostgreSQL yang berjalan pada host. Buat user dan database terlebih dahulu jika belum tersedia. Hubungkan ke PostgreSQL sebagai admin, lalu jalankan SQL berikut dengan password lokal:

CREATE USER daymark_user WITH PASSWORD 'ganti_dengan_password_lokal';
CREATE DATABASE daymark_db OWNER daymark_user;

Pastikan DATABASE_URL di .env root menggunakan hostname localhost, port PostgreSQL host, database, dan user yang sesuai.

### Menjalankan backend

Dari root repository:

cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload

Backend tersedia di http://localhost:8000; Swagger UI tersedia di http://localhost:8000/docs.

### Menjalankan frontend

Di terminal lain, dari root repository:

cd frontend
npm ci
npm run dev

Vite tersedia di http://localhost:5173. Pastikan frontend/.env berisi VITE_API_BASE_URL=http://localhost:8000.

Vite membaca VITE_* ketika development server atau build dijalankan. Setelah mengubah variabel tersebut, restart Vite. Jangan menjalankan mode lokal dan Docker Compose bersamaan jika keduanya menggunakan port host yang sama.

## Database dan persistence

Docker Compose menggunakan PostgreSQL 16 dan named volume daymark_postgres_data. Volume tersebut mempertahankan data saat container dihentikan atau dibuat ulang.

Backend menjalankan Base.metadata.create_all() saat startup. Mekanisme itu membuat tabel yang belum ada di database, tetapi tidak membuat server atau database PostgreSQL dan tidak mengubah struktur tabel yang sudah ada. Proyek ini tidak menggunakan Alembic.

Untuk memeriksa task secara read-only melalui DBeaver:

SELECT id, title, description, status
FROM tasks
ORDER BY id;

## REST API

Base URL lokal: http://localhost:8000.

| Method | Endpoint | Fungsi | Response sukses |
|---|---|---|---|
| GET | /tasks | Mengambil semua task. | 200 OK, array task atau []. |
| POST | /tasks | Membuat task. | 201 Created, task beserta ID. |
| PUT | /tasks/{id} | Memperbarui seluruh field task. | 200 OK, task terbaru. |
| DELETE | /tasks/{id} | Menghapus task. | 204 No Content, tanpa response body. |

Contoh request POST:

{
  "title": "Menyelesaikan REST API",
  "description": "Membuat endpoint CRUD menggunakan FastAPI",
  "status": "Todo"
}

PUT menerima seluruh field yang diperlukan:

{
  "title": "Menyelesaikan Backend API",
  "description": "Memperbarui implementasi endpoint CRUD",
  "status": "In Progress"
}

Task yang tidak ditemukan menghasilkan 404 Not Found. Input tidak valid menghasilkan 422 Unprocessable Entity.

## Pengujian dasar

1. Buka frontend dan pastikan daftar task dimuat.
2. Buat task, edit detail dan statusnya, lalu hapus task.
3. Muat ulang halaman untuk memeriksa konsistensi data.
4. Gunakan Swagger UI untuk menguji endpoint secara langsung.
5. Bandingkan data pada UI dengan hasil query tabel tasks.

## Troubleshooting

- Port tidak dapat digunakan: pilih port host yang kosong pada sisi kiri mapping Compose. Gunakan port tersebut di browser atau DBeaver.
- Backend tidak menemukan db: pastikan service dijalankan melalui Compose yang sama. Backend di Compose memakai db; backend langsung di host memakai localhost.
- DBeaver menampilkan database berbeda: pastikan koneksi memakai host 127.0.0.1 dan port host Compose, bukan port PostgreSQL lokal lainnya.
- Autentikasi PostgreSQL gagal: POSTGRES_PASSWORD hanya dipakai saat volume pertama kali diinisialisasi. Mengubah .env tidak otomatis mengubah password role yang tersimpan.
- Frontend tidak dapat mengakses API: pastikan backend tersedia di localhost:8000, CORS_ORIGINS mencakup http://localhost:5173, dan bundle frontend dibangun dengan VITE_API_BASE_URL yang benar.
- Perubahan VITE_API_BASE_URL tidak terlihat dalam Docker: bangun ulang image frontend karena Vite memasukkan variabel tersebut ke bundle saat build.
- Data hilang: pastikan Compose menggunakan named volume yang sama. Jangan gunakan docker compose down -v jika ingin mempertahankan database.

## Batasan proyek

Daymark dibuat sebagai Simple Task Tracker untuk penggunaan lokal dan technical assessment. Proyek ini tidak mencakup autentikasi, pencarian/filter task, atau deployment cloud.


Sebelum menyebut README final, cocokkan port PostgreSQL `55432` dan daftar variabel dengan konfigurasi Compose serta `.env.example` aktual. Setelah kamu meninjau README dan mengonfirmasi isinya sesuai, checkpoint lokalnya:

```bash
git status
git add README.md
git diff --staged
git commit -m "docs(project): finalize Docker documentation"

Jangan masukkan .env aktual dan jangan push ke GitHub pada tahap ini.
