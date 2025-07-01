import math
import string
import random
import re

# Karakter grupları
LOWER = set(string.ascii_lowercase)
UPPER = set(string.ascii_uppercase)
DIGITS = set(string.digits)
SYMBOLS = set(string.punctuation)
TURKISH = set("çğıöşüÇĞİÖŞÜ")

# Entropi (karmaşıklık) hesaplama
def hesapla_entropi(parola):
    karakterler = string.ascii_letters + string.digits + string.punctuation + "".join(TURKISH)
    karakter_kumesi = len(karakterler)
    uzunluk = len(parola)

    if uzunluk < 6:
        return 0  # Kısa şifreler zayıf kabul edilir
    
    entropi = uzunluk * math.log2(karakter_kumesi)  # Şifre uzunluğu ve karakter kümesi büyüklüğü ile entropi hesaplanır.
    return entropi

def hesapla_sifre_gucu(parola):
    entropi = hesapla_entropi(parola)
    if entropi >= 120:
        return "Çok Güçlü", entropi
    elif 90 <= entropi < 120:
        return "Güçlü", entropi
    elif 60 <= entropi < 90:
        return "Orta", entropi
    elif 30 <= entropi < 60:
        return "Zayıf", entropi
    else:
        return "Çok Zayıf", entropi


# Şifrenin kırılma süresini tahmin et
def tahmini_kirilma_suresi(entropi):
    if entropi == 0:
        return "Anında Kırılabilir"  # Yaygın şifreler için anında kırılma

    saniye = 2 ** entropi / 1_000_000_000  # Basit tahmin
    return format_sure(saniye)

def format_sure(saniye):
    if saniye < 60:
        return f"{saniye:.2f} saniye"
    elif saniye < 3600:
        return f"{saniye/60:.2f} dakika"
    elif saniye < 86400:
        return f"{saniye/3600:.2f} saat"
    elif saniye < 31536000:
        return f"{saniye/86400:.2f} gün"
    else:
        return f"{saniye/31536000:.2f} yıl"



# Zayıf şifreler listesinde mi kontrol et
def zayif_sifre_mi(parola, zayif_liste_yolu="data/weak_passwords.txt"):
    if len(parola) < 8:
        print(f"[DEBUG] Şifre çok kısa: {parola}")  # Şifre uzunluğu kontrolü
        return True  # 8 karakterden kısa şifreler zayıf kabul edilir

    # Şifrede büyük harf, küçük harf, rakam ve özel karakter olmalı
    if not any(c.isupper() for c in parola):  
        print(f"[DEBUG] Şifre büyük harf içermiyor: {parola}")
        return True
    if not any(c.islower() for c in parola):  
        print(f"[DEBUG] Şifre küçük harf içermiyor: {parola}")
        return True
    if not any(c.isdigit() for c in parola):  
        print(f"[DEBUG] Şifre rakam içermiyor: {parola}")
        return True
    if not any(c in string.punctuation for c in parola):  
        print(f"[DEBUG] Şifre özel karakter içermiyor: {parola}")
        return True

    # Yaygın şifreler listesinde kontrol et (kucuk/buyuk harf duyarsız)
    if contains_common_words(parola, zayif_liste_yolu):
        print(f"[DEBUG] Şifre yaygın şifreler listesinde bulundu: {parola}")
        return True

    return False

# Şifredeki kelimeleri tespit etmek için
def contains_common_words(parola, zayif_liste_yolu="data/weak_passwords.txt"):
    try:
        with open(zayif_liste_yolu, "r", encoding="latin1") as f:
            for line in f:
                # Küçük harf duyarsız karşılaştırma yapmak için her iki tarafı da küçük harfe çeviriyoruz
                if parola.strip().lower() == line.strip().lower():
                    print(f"[DEBUG] Zayıf şifre bulundu: {parola}")  # Debug bilgisi ekledik
                    return True
        return False
    except FileNotFoundError:
        print("[ERROR] Zayıf şifreler listesi bulunamadı.")
        return False


# Parola geçmişini kontrol et
def parola_gecmisi_kontrol(parola, eski_parolalar):
    if parola in eski_parolalar:
        return True

# password_utils.py içeriği
def güçlü_şifre_öner(güç_seviyesi="orta"):
    if güç_seviyesi == "orta":
        karakterler = string.ascii_letters + string.digits
        uzunluk = 12
    elif güç_seviyesi == "güçlü":
        karakterler = string.ascii_letters + string.digits + string.punctuation
        uzunluk = 16
    else:
        karakterler = string.ascii_letters + string.digits + string.punctuation
        uzunluk = 20  # Çok güçlü şifreler için 20 karakter

    şifre = ''.join(random.choice(karakterler) for i in range(uzunluk))
    return şifre
