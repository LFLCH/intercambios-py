import qrcode

# This script will be used in the future (it is not for now)
# It will be used in order to generate a QR code from the server indicating the ip and port that are used
# allowing the user not to have to copy those values by hand 

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def display_qr_code(img):
    img.show()

# Example usage
string_data = '{"ip":"196.1.14", "port":"8080"}'
qr_code = generate_qr_code(string_data)

# Display the QR code image
display_qr_code(qr_code)
