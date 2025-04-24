from flask import Flask, request, render_template_string
import os
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Original form URL (replace with your actual URL)
FORM_URL = "https://bmswellnest.com/BMS_Web_Live/CPTRegistration/Index"

@app.route('/')
def promocode_loader():
    promo_code = request.args.get('code', 'DEFAULT')
    
    try:
        # Fetch form page
        response = requests.get(FORM_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find promocode input and set value
        input_field = soup.find('input', {'name': 'PromoCode'})
        if input_field:
            input_field['value'] = promo_code
        
        # Add script to try autofill on page load
        script = soup.new_tag('script')
        script.string = f"""
            window.onload = function() {{
                let promoField = document.querySelector('input[name="PromoCode"]');
                if (promoField) promoField.value = '{promo_code}';
            }};
        """
        soup.head.append(script)
        
        return str(soup)
    except:
        # Fallback to landing page
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Promocode Loader</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; text-align: center; }
                #promoCode { font-size: 28px; font-weight: bold; color: #333; margin: 20px 0; background: #f0f0f0; padding: 10px; }
                a { display: inline-block; padding: 15px 30px; font-size: 18px; background-color: #4CAF50; color: white; text-decoration: none; }
                a:hover { background-color: #45a049; }
                pre { background: #f0f0f0; padding: 10px; }
            </style>
        </head>
        <body>
            <h1>Your Promocode</h1>
            <p id="promoCode">{{ promo_code }}</p>
            <a href="{{ form_url }}?promocode={{ promo_code }}" target="_blank">Go to Form</a>
            <p>Tap to open the form. If the promocode doesn’t autofill, copy this script and paste it into the address bar:</p>
            <pre>javascript:(function(){let promoField=document.querySelector('input[name="PromoCode"]');if(promoField)promoField.value='{{ promo_code }}';})();</pre>
        </body>
        </html>
        '''
        return render_template_string(html, promo_code=promo_code, form_url=FORM_URL)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)