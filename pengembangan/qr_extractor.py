'''
EL4125 Pengolahan Citra Digital 2023/2024
Hari dan Tanggal : Rabu, 13 Desember 2023
Nama (NIM) 1     : Jefferson Grizzlie (13220013)
Nama (NIM) 2     : Bostang Palaguna (13220055)
Nama File        : QRExtractor.py
Deskripsi        : realisasi fungsi untuk program pendeteksian QRCode  
'''
# Program QRExtractor
    # melakukan deteksi QRcode dengan computer vision
# KAMUS
    # Konstanta
        # BLUR_VALUE: Nilai yang digunakan untuk ukuran kernel dalam proses Gaussian blur.
        # SQUARE_TOLERANCE: Toleransi dalam menentukan apakah suatu quadrilateral adalah persegi.
        # AREA_TOLERANCE: Toleransi dalam menentukan apakah dua area kontur memiliki ukuran yang serupa.
        # DISTANCE_TOLERANCE: Toleransi dalam menentukan apakah dua jarak antara kontur memiliki ukuran yang serupa.
        # WARP_DIM: Dimensi hasil warping untuk mendapatkan QR code.
        # SMALL_DIM: Dimensi hasil perkecilan gambar untuk mendapatkan QR code.
    # Variabel 
        # cap: Objek VideoCapture yang merepresentasikan sumber video (kamera).
        # gray: Citra grayscale dari frame.
        # edged: Citra hasil deteksi tepi menggunakan metode Canny.
        # contours: Kontur-kontur yang dihasilkan dari citra deteksi tepi.
        # hierarchy: Struktur hirarki kontur.
        # squares: Daftar kontur persegi yang mewakili potensi QR codes.
        # square_indices: Indeks dari persegi yang dianggap sebagai QR code.
        # main_corners, east_corners, south_corners, tiny_squares, rectangles: Daftar kontur-kontur yang mewakili bagian-bagian dari QR code.
        # output: Salinan frame yang digunakan untuk hasil akhir.
    # Fungsi/Prosedur
        # count_children(hierarchy, parent, inner=False): Menghitung jumlah anak dari suatu kontur.
        # has_square_parent(hierarchy, squares, parent): Memeriksa apakah kontur memiliki parent yang merupakan persegi.
        # get_center(c): Mengembalikan pusat massa dari suatu kontur.
        # get_angle(p1, p2): Menghitung sudut antara dua titik.
        # get_midpoint(p1, p2): Mengembalikan titik tengah antara dua titik.
        # get_farthest_points(contour, center): Mengembalikan dua titik pada kontur yang paling jauh dari pusat.
        # line_intersection(line1, line2): Mengembalikan titik potong dari dua garis.
        # extend(a, b, length, int_represent=False): Memperpanjang garis dari titik a ke titik b sepanjang suatu panjang.
        # extract(frame, debug=False): Fungsi utama untuk mengekstrak QR code dari suatu frame.
# ALGORITMA UTAMA

# Import library
import math
import cv2
import numpy as np

# Deklarasi Konstanta
BLUR_VALUE = 3
SQUARE_TOLERANCE = 0.15
AREA_TOLERANCE = 0.15
DISTANCE_TOLERANCE = 0.25
WARP_DIM = 300
SMALL_DIM = 29

# REALISASI FUNGSI/PROSEDUR
'''
*****************************
* Function Name: count_children
*****************************
Deskripsi :
    menghitung jumlah anak dari suatu kontur dalam struktur hirarki kontur.
Parameter :
    hierarchy: Struktur hirarki kontur yang dihasilkan oleh fungsi cv2.findContours.
    parent: Indeks kontur yang menjadi induk (parent) yang akan dihitung anak-anaknya.
    inner: Boolean yang menandakan apakah fungsi ini sedang dijalankan secara rekursif pada tingkat kedalaman yang lebih dalam (inner). Nilai defaultnya adalah False.
Return value : 
    jumlah anak dari kontur
'''
def count_children(hierarchy, parent, inner=False):
    if parent == -1:
        return 0
    elif not inner:
        return count_children(hierarchy, hierarchy[parent][2], True)
    return 1 + count_children(hierarchy, hierarchy[parent][0], True) + count_children(hierarchy, hierarchy[parent][2], True)

'''
*****************************
* Function Name: has_square_parent
*****************************
Deskripsi :
    menentukan apakah suatu kontur memiliki induk (parent) yang merupakan kotak (quadrilateral) dalam struktur hirarki kontur.
Parameter :
    hierarchy: Struktur hirarki kontur yang dihasilkan oleh fungsi cv2.findContours.
    squares: Daftar (list) kotak (quadrilateral) yang telah diidentifikasi sebelumnya.
    parent: Indeks kontur yang akan diperiksa apakah memiliki induk kotak.
Return value : 
    True jika kontur dengan indeks parent memiliki induk kotak dalam struktur hirarki kontur
'''
def has_square_parent(hierarchy, squares, parent):
    if hierarchy[parent][3] == -1:
        return False
    if hierarchy[parent][3] in squares:
        return True
    return has_square_parent(hierarchy, squares, hierarchy[parent][3])

'''
*****************************
* Function Name: get_center
*****************************
Deskripsi :
    menghitung koordinat titik pusat (center) dari suatu kontur.
Parameter :
    c: Kontur yang akan dihitung pusatnya.
Return value : 
    list [x, y], yang merupakan koordinat titik pusat dari kontur c.
'''
def get_center(c):
    m = cv2.moments(c)
    return [int(m["m10"] / m["m00"]), int(m["m01"] / m["m00"])]

'''
*****************************
* Function Name: get_angle
*****************************
Deskripsi :
    menghitung sudut antara dua titik dalam sistem koordinat kartesian.
Parameter :
    p1: Koordinat titik pertama, berupa list [x1, y1].
    p2: Koordinat titik kedua, berupa list [x2, y2].
Return value : 
    nilai sudut dalam derajat antara garis yang menghubungkan dua titik tersebut dan sumbu x positif.
'''
def get_angle(p1, p2):
    x_diff = p2[0] - p1[0]
    y_diff = p2[1] - p1[1]
    return math.degrees(math.atan2(y_diff, x_diff))

'''
*****************************
* Function Name: get_midpoint
*****************************
Deskripsi :
   menghitung titik tengah (midpoint) antara dua titik dalam sistem koordinat.
Parameter :
    p1: Koordinat titik pertama, berupa list [x1, y1].
    p2: Koordinat titik kedua, berupa list [x2, y2].
Return value : 
    koordinat titik tengah antara dua titik, dalam bentuk list 
'''
def get_midpoint(p1, p2):
    return [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]

'''
*****************************
* Function Name: get_farthest_points
*****************************
Deskripsi :
    menemukan dua titik terjauh dari pusat yang dihitung dari suatu kontur.
Parameter :
    contour: Kontur suatu objek dalam citra, direpresentasikan sebagai array titik koordinat.
    center: Koordinat pusat yang digunakan sebagai referensi perhitungan jarak.
Return value : 
    dua titik terjauh dari pusat dalam bentuk list [farthest_point1, farthest_point2]
'''
def get_farthest_points(contour, center):
    distances = []
    distances_to_points = {}
    for point in contour:
        point = point[0]
        d = math.hypot(point[0] - center[0], point[1] - center[1])
        distances.append(d)
        distances_to_points[d] = point
    distances = sorted(distances)
    return [distances_to_points[distances[-1]], distances_to_points[distances[-2]]]

'''
*****************************
* Function Name: line_intersection
*****************************
Deskripsi :
    menemukan titik perpotongan dua garis.
Parameter :
    line1: Koordinat ujung garis pertama dalam bentuk [(x1, y1), (x2, y2)].
    line2: Koordinat ujung garis kedua dalam bentuk [(x1, y1), (x2, y2)].
Return value : 
    mengembalikan koordinat titik perpotongan [x, y]
'''
def line_intersection(line1, line2):
    x_diff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    y_diff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(x_diff, y_diff)
    if div == 0:
        return [-1, -1]

    d = (det(*line1), det(*line2))
    x = det(d, x_diff) / div
    y = det(d, y_diff) / div
    return [int(x), int(y)]

'''
*****************************
* Function Name: extend
*****************************
Deskripsi :
    memperpanjang garis dari titik a ke titik b sepanjang length.
Parameter :
    a: Koordinat titik awal dalam bentuk [x, y].
    b: Koordinat titik akhir dalam bentuk [x, y].
    length: Panjang garis yang akan diperpanjang.
    int_represent (opsional): Jika diatur sebagai True, fungsi akan mengembalikan koordinat titik perpanjangan sebagai nilai bulat.
Return value : 
    koordinat titik hasil perpanjangan garis. Jika int_represent diatur sebagai True, nilai ini diberikan dalam bentuk [int(x), int(y)].
'''
def extend(a, b, length, int_represent=False):
    length_ab = math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    if length_ab * length <= 0:
        return b
    result = [b[0] + (b[0] - a[0]) / length_ab * length, b[1] + (b[1] - a[1]) / length_ab * length]
    if int_represent:
        return [int(result[0]), int(result[1])]
    else:
        return result

'''
*****************************
* Function Name: extract
*****************************
Deskripsi :
    melakukan ekstraksi kode QR dari citra input, memproses langkah-langkah penghilangan noise, identifikasi lokator QR code, menemukan penunjuk arah dan pola penjajaran, serta melakukan perspective warping untuk ekstraksi kode QR.
Parameter :
    frame: Citra input yang akan diekstrak.
    debug (opsional): Jika diatur sebagai True, maka akan menampilkan citra hasil ekstraksi dan informasi debug.
Return value : 
    codes: Daftar kode QR yang berhasil diekstrak dari citra.
    output: Citra output yang telah mengalami proses pemrosesan untuk memvisualisasikan langkah-langkah ekstraksi
'''
def extract(frame, debug=False):
    output = frame.copy()

    
    ### Langkah 1: Menghilangkan noise dari citra ###

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    gray = cv2.GaussianBlur(gray, (BLUR_VALUE, BLUR_VALUE), 0)
    edged = cv2.Canny(gray, 30, 200)

    ### Langkah 2: Persempit pencarian ke QR code locators ###
    ## 2.1 cari semua contours yang tersedia
    contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # RETR_TREE : mendapatkan semua kontur dan mengatur struktur hirarki kontur dalam bentuk tree

    squares = []
    square_indices = []

    i = 0
    for c in contours:
        # Approximate the contour
        peri = cv2.arcLength(c, True)
        area = cv2.contourArea(c)
        approx = cv2.approxPolyDP(c, 0.03 * peri, True)

    ## 2.2 filter contours yang punya empat sudut (quadrilateral)
        if len(approx) == 4:
            # Determine if quadrilateral is a square to within SQUARE_TOLERANCE
    ## 2.3 Filter semua segiempat yang mendektai persegi
            if area > 25 and 1 - SQUARE_TOLERANCE < math.fabs((peri / 4) ** 2) / area < 1 + SQUARE_TOLERANCE and count_children(hierarchy[0], i) >= 2 and has_square_parent(hierarchy[0], square_indices, i) is False:
                squares.append(approx)
                square_indices.append(i)
        i += 1

### Langkah 3: Temukan locators ###
    main_corners = []
    east_corners = []
    south_corners = []
    tiny_squares = []
    rectangles = []
    # Determine if squares are QR codes
    for square in squares:
        area = cv2.contourArea(square)
        center = get_center(square)
        peri = cv2.arcLength(square, True)

        similar = []
        tiny = []
        for other in squares:
            if square[0][0][0] != other[0][0][0]:
            # 3.1 untuk semua kotak:
            #   Temukan semua kotak yang memiliki ukuran yang sama dengan kotak saat ini
                # Determine if square is similar to other square within AREA_TOLERANCE
                if math.fabs(area - cv2.contourArea(other)) / max(area, cv2.contourArea(other)) <= AREA_TOLERANCE:
                    similar.append(other)
                elif peri / 4 / 2 > cv2.arcLength(other, True) / 4:
                    tiny.append(other)

        if len(similar) >= 2:
            distances = []
            distances_to_contours = {}
            for sim in similar:
                sim_center = get_center(sim)
                d = math.hypot(sim_center[0] - center[0], sim_center[1] - center[1])
                distances.append(d)
                distances_to_contours[d] = sim
            distances = sorted(distances)
            closest_a = distances[-1]
            closest_b = distances[-2]
 # 3.2 Jika dua kotak terdekat dengan kotak saat ini memiliki jarak yang sama, perkirakan bahwa kotak ini adalah penunjuk arah kiri atas
            # Determine if this square is the top left QR code indicator
            if max(closest_a, closest_b) < cv2.arcLength(square, True) * 2.5 and math.fabs(closest_a - closest_b) / max(closest_a, closest_b) <= DISTANCE_TOLERANCE:
                # Determine placement of other indicators (even if code is rotated)
               # 3.3 Dengan kotak lainnya, cari sudut dari titik kiri atas untuk menentukan orientasi kode QR
                angle_a = get_angle(get_center(distances_to_contours[closest_a]), center)
                angle_b = get_angle(get_center(distances_to_contours[closest_b]), center)
                if angle_a < angle_b or (angle_b < -90 and angle_a > 0):
                    east = distances_to_contours[closest_a]
                    south = distances_to_contours[closest_b]
                else:
                    east = distances_to_contours[closest_b]
                    south = distances_to_contours[closest_a]
                midpoint = get_midpoint(get_center(east), get_center(south))
                # Determine location of fourth corner

                ### Langkah 4: Cari kotak alignment pattern ("tiny square" padamy code)

                # Find closest tiny indicator if possible
                min_dist = 10000
                t = []
                tiny_found = False
                if len(tiny) > 0:
                    for tin in tiny:
                          # 4.2 Setelah menentukan orientasi pelacak, hitung titik tengah kode QR
                        tin_center = get_center(tin)
                        d = math.hypot(tin_center[0] - midpoint[0], tin_center[1] - midpoint[1])
                        # 4.3  Pilih dari kemungkinan pola penjajaran kotak yang paling dekat dengan titik tengah yang juga berada di dalam batas-batas kode itu sendiri
                        if d < min_dist:
                            min_dist = d
                            t = tin
                    tiny_found = len(t) > 0 and min_dist < peri

                diagonal = peri / 4 * 1.41421
    # 4.4  Jika pola penjajaran ditemukan:
    #   Tentukan sudut keempat dari kode QR sebagai jarak yang rasional dari pola perataan (dalam arah yang berlawanan dengan titik tengah)
                if tiny_found:
                    # Easy, corner is just a few blocks away from the tiny indicator
                    tiny_squares.append(t)
                    offset = extend(midpoint, get_center(t), peri / 4 * 1.41421)
                     # 4.5 Jika tidak ada pola penjajaran yang ditemukan (kode QR yang lebih kecil tidak memiliki pola ini, atau kamera mungkin tidak dapat mendeteksinya):
                else:
                    # No tiny indicator found, must extrapolate corner based off of other corners instead
                     # 4.6 Tentukan tepi pencari lokasi yang berada di sepanjang tepi seluruh kode QR yang akan berpotongan untuk membentuk sudut keempat
                    farthest_a = get_farthest_points(distances_to_contours[closest_a], center)
                    farthest_b = get_farthest_points(distances_to_contours[closest_b], center)
                    # Use sides of indicators to determine fourth corner
                    # 4.7 Temukan perpotongan garis dan tentukan titik tersebut sebagai sudut keempat
                    offset = line_intersection(farthest_a, farthest_b)
                    if offset[0] == -1:
                        # Error, extrapolation failed, go on to next possible code
                        continue
                    offset = extend(midpoint, offset, peri / 4 / 7)
                    if debug:
                        cv2.line(output, (farthest_a[0][0], farthest_a[0][1]), (farthest_a[1][0], farthest_a[1][1]), (0, 0, 255), 4)
                        cv2.line(output, (farthest_b[0][0], farthest_b[0][1]), (farthest_b[1][0], farthest_b[1][1]), (0, 0, 255), 4)

                # Append rectangle, offsetting to farthest borders
                rectangles.append([extend(midpoint, center, diagonal / 2, True), extend(midpoint, get_center(distances_to_contours[closest_b]), diagonal / 2, True), offset, extend(midpoint, get_center(distances_to_contours[closest_a]), diagonal / 2, True)])
                east_corners.append(east)
                south_corners.append(south)
                main_corners.append(square)

    ### Langkah 5: Kompensasi _perspective warping_ dan ekstrak code
    codes = []
    i = 0
    for rect in rectangles:
        i += 1
        # Draw rectangle
        vrx = np.array((rect[0], rect[1], rect[2], rect[3]), np.int32)
        vrx = vrx.reshape((-1, 1, 2))
        cv2.polylines(output, [vrx], True, (0, 255, 255), 1)
        # 5.1 Untuk setiap kode, putar simpul menjadi persegi untuk memperbaiki keselarasan
        # Warp codes and draw them
        wrect = np.zeros((4, 2), dtype="float32")
        wrect[0] = rect[0]
        wrect[1] = rect[1]
        wrect[2] = rect[2]
        wrect[3] = rect[3]
        dst = np.array([
            [0, 0],
            [WARP_DIM - 1, 0],
            [WARP_DIM - 1, WARP_DIM - 1],
            [0, WARP_DIM - 1]], dtype="float32")
        warp = cv2.warpPerspective(frame, cv2.getPerspectiveTransform(wrect, dst), (WARP_DIM, WARP_DIM))
        # Increase contrast
        warp = cv2.bilateralFilter(warp, 11, 17, 17)
        # 5.3 Ubah menjadi satu bit hitam dan putih dengan melakukan thresholding pada gambar
        warp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
        # 5.2 Perkecil dengan interpolasi kubik menjadi persegi 29x29 piksel (ubah dimensi untuk berbagai jenis kode)

        small = cv2.resize(warp, (10*SMALL_DIM, 10*SMALL_DIM), 0, 0, interpolation=cv2.INTER_CUBIC)
        _, small = cv2.threshold(small, 100, 255, cv2.THRESH_BINARY)
        codes.append(small)
        if debug:
            cv2.imshow("Warped: " + str(i), small)

    if debug:
        # Draw debug information onto frame before outputting it
        cv2.drawContours(output, squares, -1, (5, 5, 5), 2)
        cv2.drawContours(output, main_corners, -1, (0, 0, 128), 2)
        cv2.drawContours(output, east_corners, -1, (0, 128, 0), 2)
        cv2.drawContours(output, south_corners, -1, (128, 0, 0), 2)
        cv2.drawContours(output, tiny_squares, -1, (128, 128, 0), 2)

    return codes, output
