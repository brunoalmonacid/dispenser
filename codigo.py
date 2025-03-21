import mercadopago
import time
import serial  
import qrcode


ACCESS_TOKEN = "APP_USR-8292040283316653-112418-58a2d29f2c56b0aba83e122eb42681c4-241085073"  
sdk = mercadopago.SDK(ACCESS_TOKEN)


arduino = serial.Serial('COM7', 9600) 


pagos_procesados = set()  

def crear_qr_fijo():
   
    preference_data = {
        "items": [
            {
                "title": "Pago de prueba",
                "quantity": 1,
                "unit_price": 1.0 
            }
        ],
        "auto_return": "approved",
        "external_reference": "REF-TEST-01"
        
     
    }

   
    preference_response = sdk.preference().create(preference_data)

    if preference_response["status"] != 201:
        print("Error al crear la preferencia:", preference_response.get("message", "Error desconocido"))
        return


    preference_id = preference_response["response"]["id"]
    print(f"Preferencia creada con ID: {preference_id}")

    qr_url = f"https://www.mercadopago.com.ar/checkout/v1/redirect?pref_id={preference_id}"
    print("URL del QR para escanear:", qr_url)


    generar_qr_png(qr_url)

def generar_qr_png(url):

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")


    img_path = "codigo_qr.png"
    img.save(img_path)
    print(f"Código QR guardado como: {img_path}")
crear_qr_fijo()

def verificar_pago():
  
    result = sdk.payment().search({
        "external_reference": "REF-TEST-01",  
    })


    pagos = result["response"]["results"]
    for pago in pagos:
        
        if pago["id"] in pagos_procesados:
            continue
        
     
        if pago["status"] == "approved":
            print("¡Llegó la plata!: $", pago["transaction_details"]["total_paid_amount"])

            
            pagos_procesados.add(pago["id"])

       
            arduino.write(b'1')  
            time.sleep(5) 

            arduino.write(b'0') 
          
    
    print("No se recibió nada todavía.")
    return False


print("Esperando que llegue el pago...")
while True:
    if verificar_pago():
        break
    time.sleep(5)  