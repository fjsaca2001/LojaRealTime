import requests

url = "https://www.ktaxifacilsegurorapido.kradac.com/api/utpl/ultimaPosicion"

payload='idCompania=7862254145&idCiudad=1&desde=1&hasta=1000&checksum=e43c681452041b00d393c1ac1a75da0e&token=4d4a8f40b9850decda9ab84dbed309c5c7e692591f97d76347fe019804b568d9'
headers = {
  'version': '1.0.0',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Authorization': 'Basic ZDRUMFN1VFBMOjNya1F3UDJ1NTNwdGxPZUJ5T3A1bQ=='
}

response = requests.request("POST", url, headers=headers, data=payload)
dic = response.json()

print(len(dic['lD']))




"""
<script type="module">
  // Import the functions you need from the SDKs you need
  import { initializeApp } from "https://www.gstatic.com/firebasejs/9.9.3/firebase-app.js";
  import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.9.3/firebase-analytics.js";
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  const firebaseConfig = {
    apiKey: "AIzaSyB_3NtWDjh-EXBpqx-zAKYk1DdA4Uyu7DA",
    authDomain: "lojarealtime-b480a.firebaseapp.com",
    databaseURL: "https://lojarealtime-b480a-default-rtdb.firebaseio.com",
    projectId: "lojarealtime-b480a",
    storageBucket: "lojarealtime-b480a.appspot.com",
    messagingSenderId: "892103784621",
    appId: "1:892103784621:web:1960109f370d8f0c51ee24",
    measurementId: "G-3T15P7QS0Y"
  };
  

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const analytics = getAnalytics(app);
</script>
"""