from flask import abort, Flask, request
from os import urandom
from aes import AES

# NOTE: This server requires Python 2.7

# key is represented as a list of 16 byte ints
key = map(ord, urandom(16))

print(key)

aes = AES()

app = Flask(__name__)

@app.route("/")
def application():
    num = request.args.get('num', '')
    try:
        num = int(num)
    except ValueError:
        abort(400)
    if (num > 10000  or num < 0):
        abort(400)

    output = ""
    for i in range(num):
        m = map(ord, urandom(16))
        aes.clearOnesCount()
        cipher = aes.encrypt(m, key, 16)
        leak = int(aes.getOnesCount()/4)
        output += " ".join(map(str, m)) + ", " + " ".join(map(str, cipher)) + ", " + str(leak) + "; \n"

    return output


if __name__ == '__main__':
    app.run(port=3000)
