from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Original form URL (replace with your actual URL)
FORM_URL = "https://bmswellnest.com/BMS_Web_Live/CPTRegistration/Index"

@app.route('/')
def promocode_loader():
    # Fetch promocode from URL parameter
    promo_code = request.args.get('code', 'DEFAULT')
    
    # HTML template with script injection attempt
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Promocode Loader</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; text-align: center; }
            #promoCode { font-size: 28px; font-weight: bold; color: #333; margin: 20px 0; background: #f0f0f0; padding: 10px; }
            button { padding: 15px 30px; font-size: 18px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
            button:hover { background-color: #45a049; }
            pre { background: #f0f0f0; padding: 10px; }
        </style>
        <script>
            function tryAutofill() {
                // Open form in new tab
                window.open("{{ form_url }}?PromoCode={{ promo_code }}", "_blank");
                // Show fallback script after delay
                setTimeout(() => {
                    alert("If the promocode didn’t autofill, paste this into the address bar on the form page:\\njavascript:(function(){let promoField=document.querySelector('input[name=\\\"PromoCode\\\"]');if(promoField)promoField.value='{{ promo_code }}';})();");
                }, 2000);
            }
        </script>
    </head>
    <body>
        <h1>Your Promocode</h1>
        <p id="promoCode">{{ promo_code }}</p>
        <button onclick="tryAutofill()">Go to Form</button>
        <p>Tap to open the form. If the promocode doesn’t autofill, follow the alert instructions.</p>
    </body>
    </html>
    '''
    return render_template_string(html, promo_code=promo_code, form_url=FORM_URL)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)