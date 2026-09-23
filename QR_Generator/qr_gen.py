import qrcode

print("--Python QR Code Generator--")

data = input("Enter the link or text convert into a QR code: ")

file_name = input("Enter the filename to save the QR code (with .png extension): ")

print("\nGenerating QR code...")

qr_image = qrcode.make(data)

full_file_name = f"{file_name}.png"

qr_image.save(full_file_name)

print(f"Success!QR code generated and saved as {full_file_name}")

print("Check your project folder to view the image!")