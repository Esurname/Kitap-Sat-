import datetime
import json

def adminGiris():
    adminAd = "admin"
    adminSifre = "123456689"
    
    print("Admin Girişi")
    girilenAd = input("Admin Adınızı Girin: ")
    girilenSifre = input("Admin Şifrenizi Girin: ")
    
    if girilenAd == adminAd and girilenSifre == adminSifre:
        print("Başarılı giriş! Admin paneline hoş geldiniz.")
        return True
    else:
        print("Hatalı giriş! Admin paneline erişim reddedildi.")
        return False

def kitapFiyat(sayfaSayisi):
    if sayfaSayisi < 200:
        return 150
    else:
        return 170

def adminPanel(kullaniciSepetleri):
    while True:
        print("Admin Paneli:")
        print("1. Kullanıcıların sepetteki ürünlerini görüntüle")
        print("2. Kullanıcıların seçimlerini değiştir")
        print("3. Çıkış")
        secim = input("Bir işlem seçin (1, 2, 3) : ")
        
        if secim == "1":
            if not kullaniciSepetleri:
                print("Henüz kullanıcı yok.")
            else:
                for idx, (kullanici, sepet) in enumerate(kullaniciSepetleri.items()):
                    print(f"\nKullanıcı {idx+1} - {kullanici}:")
                    for i, kitap in enumerate(sepet['kitaplar']):
                        print(f"  {i+1}. Kitap adı: {kitap['ad']}, Sayfa sayısı: {kitap['sayfa_sayisi']},
                               Fiyat: {kitap['fiyat']} TL")
                    print(f"  Toplam fiyat: {sepet['toplam_fiyat']} TL")
        elif secim == "2":
            if not kullaniciSepetleri:
                print("Henüz kullanıcı yok.")
            else:
                kullaniciIndex = int(input("Değiştirmek istediğiniz kullanıcının numarasını girin: ")) - 1
                kullaniciAdi = list(kullaniciSepetleri.keys())[kullaniciIndex]
                yeniKitapAd = input(f"{kullaniciAdi} kullanıcısının sepete yeni bir kitap eklemek istiyor
                                     musunuz? Kitap adı girin (yoksa çıkış): ")
                
                if yeniKitapAd.lower() == "çıkış":
                    print("Admin paneline dönülüyor....")
                    break
                yeniSayfaSayisi = int(input("Yeni kitap için sayfa sayısı girin: "))
                yeniFiyat = kitapFiyat(yeniSayfaSayisi)
                kullaniciSepetleri[kullaniciAdi]['kitaplar'].append({"ad": yeniKitapAd, 
                                                        "sayfa_sayisi": yeniSayfaSayisi, "fiyat": yeniFiyat})
                
                toplamFiyat = sum([kitap['fiyat'] for kitap in kullaniciSepetleri[kullaniciAdi]['kitaplar']])
                kullaniciSepetleri[kullaniciAdi]['toplam_fiyat'] = toplamFiyat
                print(f"Yeni kitap eklendi. {kullaniciAdi}'nin yeni toplam fiyatı: {toplamFiyat} TL")
        elif secim == "3":
            print("Admin panelinden çıkılıyor.")
            break
        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")

def kargoUcreti(fiyat):
    if fiyat < 100:
        return "Müşteri kargo ücretini öder"
    elif fiyat >= 100:
        return "Kargo ücretine %10 indirim yapılır"


def sepetIndirim(toplamFiyat):
    if 300 <= toplamFiyat <= 500:
        return toplamFiyat * 0.95  
    elif 500 <= toplamFiyat <= 1000:
        return toplamFiyat * 0.93  
    elif toplamFiyat > 1000:
        return toplamFiyat * 0.90  
    return toplamFiyat


def ekstraIndirim(sepetFiyat, teslimTarihi):
    bugun = datetime.date.today()
    fark = (teslimTarihi - bugun).days

    if fark <= 2:
        return sepetFiyat * 0.95  
    elif fark <= 7:
        return sepetFiyat * 0.98  
    return sepetFiyat

def kargoIndirim(toplamFiyat):
    if 100 <= toplamFiyat < 300:
        return "Kargo ücretine %40 indirim yapılır"
    elif toplamFiyat >= 300:
        return "Kargo ücreti alınmaz"
    return "Kargo ücreti alınır"

def kitapEkle():
    kitapAd = input("Kitap adını girin: ")
    sayfaSayisi = int(input("Kitap sayfa sayısını girin: "))
    fiyat = kitapFiyat(sayfaSayisi)
    print(f"Kitap adı: {kitapAd}, Sayfa sayısı: {sayfaSayisi}, Fiyat: {fiyat} TL")
    return {'ad': kitapAd, 'sayfa_sayisi': sayfaSayisi, 'fiyat': fiyat}

def sepetSatinAl(kullaniciSepetleri):
    adSoyad = input("Ad ve Soyadınızı girin: ")
    ePosta = input("E-posta adresinizi girin: ")
    
    sepetFiyat = 0
    kitaplar = []
    
    while True:
        kitap = kitapEkle()
        kitaplar.append(kitap)
        secim = input("Kitap eklemeye devam etmek istiyor musunuz? (E/H): ")
        if secim.lower() != 'e':
            break
    
    for kitap in kitaplar:
        sepetFiyat += kitap['fiyat']
    sepetFiyat = sepetIndirim(sepetFiyat)

    teslimGunu = int(input("Kitapları kaç gün içerisinde teslim almayı planlıyorsunuz? : "))
    teslimTarihi = datetime.date.today() + datetime.timedelta(days=teslimGunu)
    sepetFiyat = ekstraIndirim(sepetFiyat, teslimTarihi)

    print(kargoIndirim(sepetFiyat))
    
    kullaniciSepetleri[adSoyad] = {
        'kitaplar': kitaplar,
        'toplam_fiyat': sepetFiyat
    }

    print(f"Sepetinizde {len(kitaplar)} kitap var. Toplam fiyat: {sepetFiyat} TL")

    with open('kullaniciVerileri.json', 'w') as dosya:
        json.dump(kullaniciSepetleri, dosya, indent=4)

def kullaniciVerileriniYukle():
    try:
        with open('kullaniciVerileri.json', 'r') as dosya:
            return json.load(dosya)
    except FileNotFoundError:
        return {}

def anaProgram():
    kullaniciSepetleri = kullaniciVerileriniYukle()
    
    if adminGiris():
        adminPanel(kullaniciSepetleri)
    
    sepetSatinAl(kullaniciSepetleri)

anaProgram()
