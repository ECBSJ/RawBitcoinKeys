from flask import Flask, render_template, request, redirect, url_for
import hashlib
import base58


app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def input_binary():
    if request.method == "POST":
        binary = request.form["binary"]
        decimal = int(binary,2)
        return render_template("decimal.html", dec=decimal)
        # return redirect(url_for("show_decimal", bin=binary))
    else:
        return render_template("binary.html")

# @app.route('/<bin>', methods=['POST','GET'])
# def show_decimal(bin):
#     if request.method == "POST":
#         decimal = request.form["decimal"]
#         hexadecimal_string = hex(int(decimal))
#         return render_template("hex.html", h=hexadecimal_string)
#     else:
#         decimal = int(bin,2) 
#         return render_template("decimal.html", dec=decimal)

@app.route('/elliptic.html', methods=['POST','GET'])
def teach_elliptic():
    if request.method == "POST":
        privkeydecimalform = request.form["decimalform"]
        Pcurve = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 -1 # The proven prime
        Acurve = 0; Bcurve = 7 # These two defines the elliptic curve. y^2 = x^3 + Acurve * x + Bcurve
        Gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
        Gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
        GPoint = (Gx,Gy) # Generator Point
        N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 # Number of points in the field
        privKey = int(privkeydecimalform) # need to find the correct hexa format here

        def modinv(a,b=Pcurve): #Extended Euclidean Algorithm/'division' in elliptic curves
            lm, hm = 1,0
            low, high = a%b,b
            while low > 1:
                ratio = high//low
                nm, new = hm-lm*ratio, high-low*ratio
                lm, low, hm, high = nm, new, lm, low
            return lm % b

        def ECAdd(a,b): # Point addition, invented for EC.
            LambdaAdd = ((b[1] - a[1]) * modinv(b[0] - a[0],Pcurve)) % Pcurve
            x = (LambdaAdd * LambdaAdd - a[0] - b[0]) % Pcurve
            y = (LambdaAdd * (a[0] - x) - a[1]) % Pcurve
            return (x,y)

        def ECDouble(a): # Point Doubling, also invented for EC.
            LamdaDouble = ((3 * a[0] * a[0] + Acurve) * modinv((2 * a[1]), Pcurve)) % Pcurve
            x = (LamdaDouble * LamdaDouble - 2 * a[0]) % Pcurve
            y = (LamdaDouble * (a[0] - x) - a[1]) % Pcurve
            return (x,y)

        def ECMultiply(GenPoint,privKeyHex): #Double & add. Not true multiplication
            if privKeyHex == 0 or privKeyHex >= N: raise Exception("Invalid Private Key")
            privKeyBin = str(bin(privKeyHex))[2:]
            Q=GenPoint
            for i in range (1, len(privKeyBin)):
                Q=ECDouble(Q)
                if privKeyBin[i] == "1":
                    Q=ECAdd(Q,GenPoint)
            return (Q)

        publicKey = ECMultiply(GPoint,privKey)
        # print ("Private Key:")
        # print (privKey)
        # print ("Public Key (uncompressed):")
        # print (publicKey)
        # print ("Public Key (compressed):")

        oddcompressedpubkey = 0
        evencompressedpubkey = 0
        compressedpubkey = 0
        if publicKey[1] % 2 == 1: # If the Y coordinate of the Public Key is odd.
            oddcompressedpubkey = "03"+str(hex(publicKey[0])[2:]).zfill(64)
        else: # If the Y coordinate is even.
            evencompressedpubkey = "02"+str(hex(publicKey[0])[2:]).zfill(64)
        if evencompressedpubkey == 0:
            compressedpubkey = oddcompressedpubkey
        else:
            compressedpubkey = evencompressedpubkey
        return render_template('pubkey.html', pubk=publicKey, comppk=compressedpubkey)
    else:
        return render_template("elliptic.html")

@app.route('/topubadd.html', methods=['POST','GET'])
def convert_to_pubadd():
    if request.method == "POST":
        thepubkey = request.form["pubkey"]
        pubkey = thepubkey
        compress_pubkey = False

        def hash160(hex_str):
            sha = hashlib.sha256()
            rip = hashlib.new('ripemd160')
            sha.update(hex_str)
            rip.update( sha.digest() )
            # print ( "key_hash = \t" + rip.hexdigest() )
            return rip.hexdigest()  # .hexdigest() is hex ASCII


        if (compress_pubkey):
            if (ord(bytearray.fromhex(pubkey[-2:])) % 2 == 0):
                pubkey_compressed = '02'
            else:
                pubkey_compressed = '03'
            pubkey_compressed += pubkey[2:66]
            hex_str = bytearray.fromhex(pubkey_compressed)
        else:
            hex_str = bytearray.fromhex(pubkey)

        # Obtain key:

        key_hash = '00' + hash160(hex_str)

        # Obtain signature:

        sha = hashlib.sha256()
        sha.update( bytearray.fromhex(key_hash) )
        checksum = sha.digest()
        sha = hashlib.sha256()
        sha.update(checksum)
        checksum = sha.hexdigest()[0:8]

        # print ( "checksum = \t" + sha.hexdigest() )
        # print ( "key_hash + checksum = \t" + key_hash + ' ' + checksum )
        # print ( "bitcoin address = \t" + (base58.b58encode( bytes(bytearray.fromhex(key_hash + checksum)) )).decode('utf-8') )
        finalpublickey = ''
        # "bitcoin address = \t" + 
        finalpublickey = (base58.b58encode( bytes(bytearray.fromhex(key_hash + checksum)) )).decode('utf-8')
        return render_template("finalpubadd.html", finalpubadd=finalpublickey)
    else:
        return render_template("topubadd.html")


if __name__=="__main__":
    app.run(debug=True)


