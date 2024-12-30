from flask import Flask, render_template, request
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import random

app = Flask(__name__)  # Flask app'ini doğru şekilde başlatma

# Model Eğitim Fonksiyonu
def train_model():
    try:
        # CSV dosyasından veri yükleme
        file_path = "HAZIRLIKYENİVERİ2.csv"
        data = pd.read_csv(file_path, sep=';')  # CSV'nin ayracı belirtildi

        # Sütun isimleri tanımlandı
        columns = ["ekran_suresi", "mola_suresi", "cihaz_turu", "kullanim_amaci", 
                   "goz_yorgunlugu", "uyku_suresi", "cinsiyet", "yas", "ortam"]
        data.columns = columns

        # Sayısal kolonları dönüştürme
        numerical_columns = ["ekran_suresi", "mola_suresi", "goz_yorgunlugu", "uyku_suresi", "yas"]
        data[numerical_columns] = data[numerical_columns].apply(pd.to_numeric, errors='coerce')

        # Kategorik verileri One-Hot Encoding ile dönüştürme
        categorical_columns = ["cihaz_turu", "kullanim_amaci", "cinsiyet"]
        data_encoded = pd.get_dummies(data, columns=categorical_columns, drop_first=True)

        # Giriş ve hedef değişkenleri ayırma
        X = data_encoded.drop(columns=["ortam"])
        y = data["ortam"]

        # Model özellik adlarını saklama
        global feature_names
        feature_names = X.columns

        # Veriyi eğitim ve test setine ayırma
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Model oluşturma ve eğitme
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)

        # Model doğruluğunu hesaplama
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        # Doğruluk oranını terminalde göster
        print(f"Model doğruluk oranı: {accuracy * 100:.2f}%")

        return model, accuracy

    except Exception as e:
        print(f"Model eğitiminde hata: {str(e)}")
        return None, None

# Modeli eğitme
model, accuracy = train_model()

# Rastgele öneriler (emoji eklenmiş)
suggestions = {
    "ev": [
        "20-20-20 KURALINI UYGULAYIN:\n Her 20 dakikada bir, 20 saniye boyunca 20 metre uzağa odaklanın. Bu, göz kaslarınızı gevşetir. 👀💪",
        "Ev işlerine yardım edin, bir hobi edinin veya pencereden dışarı bakıp gözlerinizi dinlendirin. Gözlerinizi sağa, sola, yukarı ve aşağı hareket ettirerek kasları rahatlatın. 🏡🎨🪟",
        "GÖZ EGZERSİZİ YAPIN:\n Gözlerinizi birkaç saniye sıkıca kapatıp açın. 👁‍🗨🧘",
        "Ekran başında uzun süre çalıştıktan sonra soğuk bir havluyu gözlerinize koyarak rahatlama sağlayın. ❄🧣"
    ],
    "ofis": [
        "10 dakikalık bir mola sırasında gözlerinizi kapatarak ve karanlık bir ortamda gevşeyerek dinlenin. 😌🛋",
        "Ekranınıza bakmayı bırakıp gözlerinizi dinlendirin ya da kahve molası verin. ☕👀",
        "5 dakika boyunca sırtınızı sandalyeye yaslayarak gözlerinizi kapatın. Bu sırada derin nefes alarak zihninizi ve gözlerinizi dinlendirin. 🧘‍♀💆",
        "Uzun süre klimalı bir ortamdaysanız göz kuruluğunu önlemek için yapay gözyaşı damlaları kullanabilirsiniz. 💧😌"
    ],
    "kütüphane": [
        "Kitap arası molalar verin ya da bahçeye inin. 📚🌳",
        "Düzenli nefes alıp verin ya da hava almak için bahçeye inin. Göz yorgunluğunu azaltmak için ekranla gözleriniz arasındaki mesafeyi koruyun. 🌬📖",
        "5 dakika boyunca sırtınızı sandalyeye yaslayarak gözlerinizi kapatın. Bu sırada derin nefes alarak zihninizi ve gözlerinizi dinlendirin. 🧘‍♂💆‍♂"
    ]
}

# Yorgunluk seviyesi hesaplama fonksiyonu
def calculate_fatigue_level(user_input):
    ekran_suresi = user_input["ekran_suresi"]
    mola_suresi = user_input["mola_suresi"]
    uyku_suresi = user_input["uyku_suresi"]
    yas=user_input["yas"]
    yas_faktor = (yas - 20) / 10  
    
    # Yorgunluk seviyesi hesaplama: Ekran süresi uzun, uyku süresi kısa ise yorgunluk yüksek olur
    fatigue_score = (ekran_suresi / 2) - (mola_suresi * 2) - (uyku_suresi / 3) + yas_faktor
    # Yorgunluk seviyesini normalize et
    fatigue_score = max(0, min(fatigue_score, 100))  # 0 ile 100 arasında tutalım

    # Yorgunluk seviyesini etiketle
    if fatigue_score > 70:
        fatigue_label = "Yüksek"
    elif fatigue_score > 40:
        fatigue_label = "Orta"
    else:
        fatigue_label = "Düşük"
    
    return f"{fatigue_score:.2f} ({fatigue_label})"

# Ana Sayfa Rotası
@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    suggestion = None
    fatigue_level = None
    environment = None  # Ortam bilgisini burada saklayacağız

    if request.method == "POST":
        try:
            # Kullanıcıdan gelen verileri al
            user_input = {
                "ekran_suresi": int(request.form.get("ekran_suresi", 0)),
                "mola_suresi": int(request.form.get("mola_suresi", 0)),
                "uyku_suresi": int(request.form.get("uyku_suresi", 0)),
                "yas": int(request.form.get("yas", 0)),
                "cihaz_turu_tablet": 1 if request.form.get("cihaz_turu") == "tablet" else 0,
                "cihaz_turu_telefon": 1 if request.form.get("cihaz_turu") == "telefon" else 0,
                "cihaz_turu_bilgisayar": 1 if request.form.get("cihaz_turu") == "bilgisayar" else 0,
                "kullanim_amaci_eğlence": 1 if request.form.get("kullanim_amaci") == "eğlence" else 0,
                "kullanim_amaci_iş": 1 if request.form.get("kullanim_amaci") == "iş" else 0,
                "kullanim_amaci_eğitim": 1 if request.form.get("kullanim_amaci") == "eğitim" else 0,
                "cinsiyet_kadın": 1 if request.form.get("cinsiyet") == "kadın" else 0
            }

            # Veriyi DataFrame'e dönüştürme
            input_df = pd.DataFrame([user_input])

            # Eğitim sırasında kullanılan sütunlarla aynı hale getirme
            input_df = input_df.reindex(columns=feature_names, fill_value=0)

            # Tahmin yap
            if model is not None:
                prediction = model.predict(input_df)[0]
                environment = prediction  # Ortam tahminini kaydet

                # Yorgunluk seviyesini hesapla
                fatigue_level = calculate_fatigue_level(user_input)

                # Öneri seçimi
                if environment in suggestions:
                    suggestion = random.choice(suggestions[environment])
            else:
                prediction = "Model yüklenemedi."

        except Exception as e:
            prediction = f"Girdi verilerinde hata: {str(e)}"  

    return render_template("index.html", accuracy=accuracy, prediction=prediction, suggestion=suggestion, fatigue_level=fatigue_level, environment=environment)

if __name__ == "_main_":
    app.run(debug=True)  # Flask uygulamasını başlatma
