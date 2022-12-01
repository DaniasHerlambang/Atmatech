# ATMATECH_Test

Simple Rest API Python Framework Flask, JWT 

****Brief****
>  *  Database: PostgreSQL
>  *  JWT for auth
>  *  CRUD Book
>  *  TDD/BDD
>  *  Menggunakan container

****Available URL****

1.  `localhost:5000/login` => GET
2.  `localhost:5000/books` => GET,POST
3.  `localhost:5000/books/<book_id>` => GET,PUT,DELETE

**Setup Database Configuration**

Pada models.py gunakan settingan database sesuai dengan kebutuhan yang dijalankan
> ![db_config](https://i.ibb.co/DW49fZM/settingan-jwt.png)

****Step by step menjalankan aplikasi****
*  pastikan dipc sudah terinstall python3
*  Buat virtual environment
  `python3 -m venv nama-env` on linux , 
  `virtualenv nama-env` on windows
*  Jalankan environment
  `source nama-env/bin/activate`
*  Install requirements yang dibutuhkan
  `pip install -r requirements.txt`
*  Jalankan inisialisasi awal (hanya perlu sekali untuk menggenerate database)
  `python initialize.py`
*  export app flask yang akan dijalankan
  `export FLASK_APP=app.py`
*  Jalankan server
  `flask run` atau `python app.py`
*  Gunakan aplikasi postman atau sejenisnya


****Docker****

setup docker: `docker-compose up`

