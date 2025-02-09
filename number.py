from flask import Flask, request, jsonify
from flask_cors import CORS 
import requests
from collections import OrderedDict
import json

app = Flask(__name__)

CORS(app)

# validate
def validate(number):
    num_str = request.args.get('number')

    try:
        number = int(num_str)
        return number, 200
    except ValueError:
        try:
            number = float(num_str)
            number = int(number)
            return number, 200
        except ValueError:
            return num_str, 400
    
    return number, 200

# check if prime
def is_prime(number):
    if number < 2 or type(number) is float:
        return False
    for x in range(2, (number//2) + 1):
        if number % x == 0:
            return False

    return True

# check if armstrong
def is_armstrong(number):
    number = abs(number)
    order = len(str(number))
    sum = 0
    temp = number

    while temp > 0:
        digit = temp % 10
        sum += digit ** order
        temp //= 10

    if number != sum:
        return False

    return True
    
# check if perfect
def is_perfect(number):
    if number == 0 or type(number) is float:
        return False

    sum = 0
    for x in range(1, number):
        if (number % x == 0):
            sum = sum + x
    
    if sum != number:
        return False

    return True

# calc sum
def calc_sum(number):
    number = abs(number)
    sum = 0
    temp = number

    while temp > 0:
        digit = temp % 10
        sum += digit
        temp //= 10

    return int(sum)

# get fun fact
def get_fun_fact(number):
    url = f"http://numbersapi.com/{number}/math"
    response = requests.get(url)

    if response.status_code != 200:
        return(f"Failed to retrieve data. Status code: 200")
    
    return str(response.text)

#  get properties
def get_properties(number):
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    return properties


@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')

    if not number:
        return jsonify({"error": True, "number": ""}), 400

    # Validate the number
    number, status_code = validate(number)

    if status_code == 400:
        return jsonify({"error": True, "number": number}), 400


    # response
    response_data = OrderedDict([
        ("number", number),
        ("is_prime", bool(is_prime(number))),
        ("is_perfect", bool(is_perfect(number))),
        ("properties", get_properties(number)),
        ("digit_sum", int(calc_sum(number))),
        ("fun_fact", str(get_fun_fact(number)))
    ])

    response_json = json.dumps(response_data)

    return response_json, 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    # Run the app on a publicly accessible address
    app.run(debug=False, host='0.0.0.0', port=5000)