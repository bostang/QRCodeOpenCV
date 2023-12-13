'''
EL4125 Pengolahan Citra Digital 2023/2024
Hari dan Tanggal : Rabu, 13 Desember 2023
Nama (NIM) 1     : Jefferson Grizzlie (13220013)
Nama (NIM) 2     : Bostang Palaguna (13220055)
Nama File        : main.py
Deskripsi        : main program sourcecode implementasi pendeteksian QRCode  
'''

# Import library
import cv2
import qr_extractor as reader
from pyzbar.pyzbar import decode

# menyalakan kamera
cap = cv2.VideoCapture(0)

print("--Start Program--")
while True:
    _, frame = cap.read()
    # mulai ekstraksi QRCode
    codes, frame = reader.extract(frame, True)
    cv2.imshow("frame", frame)

    # menampilkan QRCode terbaca pada terminal 
        # Mencetak hasil pembacaan QR codes di terminal
    for code in codes:
        # print("QR Code:")
        if (decode(code) != []):
            print(decode(code))
            print("")
    #print(decode(codes))

    # Proses berhenti saat user menekan tombol `q`
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("--End Program--")
        break

# Akhiri proses
cap.release()
cv2.destroyAllWindows()
