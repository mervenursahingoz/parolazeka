from flask import Flask, render_template, request
from core.password_utils import hesapla_entropi, tahmini_kirilma_suresi, zayif_sifre_mi, güçlü_şifre_öner, hesapla_sifre_gucu

# Flask uygulamasını başlat
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    önerilen_şifre = None  # Başlangıçta önerilen şifre boş
    güç_skoru = ""
    strength_percent = 0
    strength_color = ""
    
    if request.method == "POST":
        parola = request.form["parola"]  # Kullanıcıdan parola al
        entropi = hesapla_entropi(parola)  # Entropi hesapla
        kirilma_suresi = tahmini_kirilma_suresi(entropi)  # Kırılma süresi tahmini
        zayif = zayif_sifre_mi(parola)  # Zayıf şifre kontrolü
        
        # Şifre gücü skoru hesaplama
        güç_skoru, entropi = hesapla_sifre_gucu(parola)
        if güç_skoru == "Çok Güçlü":
            strength_percent = 100
            strength_color = "green"
        elif güç_skoru == "Güçlü":
            strength_percent = 80
            strength_color = "lightgreen"
        elif güç_skoru == "Orta":
            strength_percent = 60
            strength_color = "yellow"
        elif güç_skoru == "Zayıf":
            strength_percent = 40
            strength_color = "orange"
        else:
            strength_percent = 20
            strength_color = "red"
        
        if zayif:
            önerilen_şifre = güçlü_şifre_öner()  # Güçlü şifre önerisini al

        return render_template("index.html", parola=parola, entropi=entropi, kirilma_suresi=kirilma_suresi, 
                               zayif=zayif, önerilen_şifre=önerilen_şifre, güç_skoru=güç_skoru, 
                               strength_percent=strength_percent, strength_color=strength_color)

    return render_template("index.html", parola=None)

if __name__ == "__main__":
    app.run(debug=True, port=5001)

