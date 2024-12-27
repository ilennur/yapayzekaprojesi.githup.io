from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Modeli yüklemek için fonksiyon
def load_model():
    try:
        model = joblib.load('model.pkl')  # Burada modelin doğru yolda olduğundan emin olun
        return model
    except FileNotFoundError:
        return None

# Tahmin yapma fonksiyonu
def make_prediction(data):
    model = load_model()
    if model:
        prediction = model.predict([data])
        return prediction
    else:
        return "Model yüklenemedi."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # HTML formundan gelen verileri al
        ekran_suresi = int(request.form['ekran_suresi'])
        mola_suresi = int(request.form['mola_suresi'])
        uyku_suresi = int(request.form['uyku_suresi'])
        yas = int(request.form['yas'])
        cihaz_turu = request.form['cihaz_turu']
        kullanim_amaci = request.form['kullanim_amaci']

        # Verileri işleyin ve modele uygun hale getirin (Örnek olarak veri düzenleme)
        input_data = [ekran_suresi, mola_suresi, uyku_suresi, yas]

        # Modelle tahmin yap
        prediction = make_prediction(input_data)

        # Tahmin sonucu ve öneri
        if prediction == 1:
            fatigue_level = "Yüksek Yorgunluk"
            suggestion = "Daha fazla dinlenmelisiniz!"
        else:
            fatigue_level = "Düşük Yorgunluk"
            suggestion = "İyi durumda görünüyorsunuz."

        return render_template('index.html', prediction=prediction, fatigue_level=fatigue_level, suggestion=suggestion)
    except Exception as e:
        return f"Hata: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
