from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def validate(number):
    # validate number
    num_str = request.args.get('number')
    try:
        number = int(number)
    except ValueError:
        return jsonify({"number": number, "is not a number": True}), 200

# check if prime
def is_prime(number):
    if number < 2:
        return False
    for x in range(2, (number//2) + 1):
        if number % x == 0:
            return False
    else:
        return True

# check if armstrong
def is_armstrong(number):
    order = len(str(number))
    sum = 0
    temp = number

    while temp > 0:
        digit = temp % 10
        sum += digit ** order
        temp //= 10

    if number == sum:
        return True
    else:
        return False
    
# check if perfect
def is_perfect(number):
    sum = 0
    for x in range(1, number):
        if (number % x == 0):
            sum = sum + x
    
    if sum == number:
        return True
    else:
        return False

# calc sum
def calc_sum(number):
    sum = 0
    temp = number

    while temp > 0:
        digit = temp % 10
        sum += digit
        temp //= 10

    return sum

# get fun fact
def get_fun_fact(number):
    url = f"http://numbersapi.com/{number}/math"
    response = requests.get(url)

    if response.status_code != 200:
        return(f"Failed to retrieve data. Status code: {response.status_code}")
    
    return (f"{response.text}")

#  get properties
def get_properties(number):
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    
    if number // 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    return str(properties)


@app.route('/api/classify-number', methods=['GET'])
def classify_number(number):
    # response
    response_data = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": get_properties(number),
        "digit_sum": calc_sum(number),
        "fun_fact": get_fun_fact(number)
    }

    return jsonify(response_data), 200


if __name__ == '__main__':
    # Run the app on a publicly accessible address
    app.run(debug=False, host='0.0.0.0', port=5000)
