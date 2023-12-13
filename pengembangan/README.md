# QR Code Extractor
Pengekstrak kode QR berbasis Python yang menggunakan OpenCV untuk mendeteksi dan mengekstrak kode QR dalam berbagai orientasi.

## Fitur
  - Mampu mendeteksi beberapa kode QR dengan cepat dari gambar atau video
  - Mampu mengompensasi perspektif dan menyederhanakan kode
  - Kompatibel dengan kode Model 1, Model 2, dan SQRC
## Catatan Penting
  - Implementasi program ini **tidak** men-_decode_ kode QR dengan sendirinya. Penguraian kode harus ditangani oleh program luar (seperti ZBar)
 - Implementasi program ini memiliki beberapa keterbatasan : tidak dapat mengekstrak kode QR dengan warna yang berbeda, hiasan, dan kode QR dengan lebih dari satu _aligntment locator_.
 - 
# Metodologi - Cara kerja sistem
  ### Langkah 1: Menghilangkan _noise_ dari citra
  - _Convert_ citra awal menjadi _greyscale_
  - Menerapkan _Gaussian blur_ untuk mengurangi _noise_
  - Menerapkan _Canny edge filter_ untuk mengeleminasi distractions
  ### Langkah 2: Persempit pencarian ke QR code locators
  - cari semua _contours_ yang tersedia
  - _Filter_ semua contours dengan _vertex count_ sebanyak empat (quadrilateral)
  - _Filter_ semua segiempat yang kira-kira persegi dan punya sejumlah _children_
  ### Langkah 3: Temukan _locators_
 - untuk semua kotak:
    - Temukan semua kotak yang memiliki ukuran yang sama dengan kotak saat ini
  - Jika dua kotak terdekat dengan kotak saat ini memiliki jarak yang sama, perkirakan bahwa kotak ini adalah penunjuk arah kiri atas
  - Dengan kotak lainnya, cari sudut dari titik kiri atas untuk menentukan orientasi kode QR
  ### Langkah 4: Cari kotak _alignment pattern_ ("tiny square" pada `my code`)
  - Saat mencari melalui kotak pada langkah sebelumnya, simpan kotak yang berukuran kurang dari setengah ukuran kotak pelacak
  - Setelah menentukan orientasi pelacak, hitung titik tengah kode QR
  - Pilih dari kemungkinan pola penjajaran kotak yang paling dekat dengan titik tengah yang juga berada di dalam batas-batas kode itu sendiri
  - Jika pola penjajaran ditemukan:
    - Tentukan sudut keempat dari kode QR sebagai jarak yang rasional dari pola perataan (dalam arah yang berlawanan dengan titik tengah)
  - Jika tidak ada pola penjajaran yang ditemukan (kode QR yang lebih kecil tidak memiliki pola ini, atau kamera mungkin tidak dapat mendeteksinya):
    - Tentukan tepi pencari lokasi yang berada di sepanjang tepi seluruh kode QR yang akan berpotongan untuk membentuk sudut keempat
    - Temukan perpotongan garis dan tentukan titik tersebut sebagai sudut keempat
  ### Langkah 5: Kompensasi _perspective warping_ dan ekstrak code
  - Untuk setiap kode, putar simpul menjadi persegi untuk memperbaiki keselarasan
  - Perkecil dengan interpolasi kubik menjadi persegi 29x29 piksel (ubah dimensi untuk berbagai jenis kode)
  - Ubah menjadi satu bit hitam dan putih dengan melakukan thresholding pada gambar
  - Kembalikan kode yang diformat dalam daftar

## Referensi

[Contour](https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html)

[Canny detector](https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html)

[Sumber Kode](https://github.com/MikhailGordeev/QR-Code-Extractor/tree/master)