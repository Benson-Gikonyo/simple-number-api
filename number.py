from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import math
import asyncio
import aiohttp

app = Flask(__name__)
CORS(app)

# In-memory cache
fun_fact_cache = {}
prime_cache = {}
armstrong_cache = {}
perfect_cache = {}

# Validate number
def validate(number):
    try:
        num_str = request.args.get('number')
        number = int(num_str)
        return number, 200
    except (ValueError, TypeError):
        return num_str, 400

# Prime check with cache
def is_prime(number):
    if number in prime_cache:
        return prime_cache[number]
    
    if number < 2 or type(number) is float:
        prime_cache[number] = False
        return False
    for x in range(2, int(math.sqrt(number)) + 1):
        if number % x == 0:
            prime_cache[number] = False
            return False
    
    prime_cache[number] = True
    return True

# Armstrong check with cache
def is_armstrong(number):
    if number in armstrong_cache:
        return armstrong_cache[number]

    number = abs(number)
    order = len(str(number))
    sum = 0
    temp = number

    while temp > 0:
        digit = temp % 10
        sum += digit ** order
        temp //= 10
        if sum > number:
            armstrong_cache[number] = False
            return False

    armstrong_cache[number] = (number == sum)
    return armstrong_cache[number]

# Perfect number check with cache
def is_perfect(number):
    if number in perfect_cache:
        return perfect_cache[number]
    
    if number <= 0 or type(number) is float:
        perfect_cache[number] = False
        return False

    sum = 1  # Start from 1 as it's always a divisor
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            sum += i
            if i != number // i:  # Avoid adding square roots twice
                sum += number // i

    perfect_cache[number] = (sum == number)
    return perfect_cache[number]

# Async version of fun fact
async def get_fun_fact_async(number):
    if number in fun_fact_cache:
        return fun_fact_cache[number]
    
    async with aiohttp.ClientSession() as session:
        url = f"http://numbersapi.com/{number}/math"
        async with session.get(url) as response:
            if response.status != 200:
                return "Failed to retrieve data. Status code: 200"
            fact = await response.text()
            fun_fact_cache[number] = fact
            return fact

# Wrapper for async function
def get_fun_fact(number):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(get_fun_fact_async(number))

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')

    if not number:
        return jsonify({"error": True, "number": ""}), 400

    number, status_code = validate(number)

    if status_code == 400:
        return jsonify({"error": True, "number": number}), 400

    response_data = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": ["even" if number % 2 == 0 else "odd", "armstrong" if is_armstrong(number) else "not_armstrong"],
        "digit_sum": calc_sum(number),
        "fun_fact": get_fun_fact(number)
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)