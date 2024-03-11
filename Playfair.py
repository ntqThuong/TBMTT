from tkinter import *

# Hàm để tạo ma trận khóa từ khóa
def generate_key_matrix(key):
    key = key.replace(" ", "").upper()  # Chuyển đổi khóa thành chữ in hoa và loại bỏ khoảng trắng
    key_matrix = []

    # Tạo một list chứa tất cả các ký tự không trùng lặp trong khóa
    unique_chars = []
    for char in key:
        if char not in unique_chars and char.isalpha():
            unique_chars.append(char)

    # Xây dựng ma trận 5x5 từ list ký tự không trùng lặp
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # Bỏ qua "J" vì không sử dụng trong Playfair
    for char in unique_chars:
        alphabet = alphabet.replace(char, "")
    key_matrix = [list(key)]
    for char in alphabet:
        if len(key_matrix[-1]) == 5:
            key_matrix.append([])
        key_matrix[-1].append(char)
    return key_matrix

# Hàm để mã hóa cặp ký tự
def encode_pair(pair, key_matrix):
    char1, char2 = pair
    row1, col1 = find_char(char1, key_matrix)
    row2, col2 = find_char(char2, key_matrix)

    # Nếu cùng hàng, thì lấy ký tự ở bên phải, nếu cùng cột, thì lấy ký tự ở phía dưới
    if row1 == row2:
        return key_matrix[row1][(col1 + 1) % 5] + key_matrix[row2][(col2 + 1) % 5]
    elif col1 == col2:
        return key_matrix[(row1 + 1) % 5][col1] + key_matrix[(row2 + 1) % 5][col2]
    else:
        return key_matrix[row1][col2] + key_matrix[row2][col1]

# Hàm để tìm vị trí của ký tự trong ma trận
def find_char(char, key_matrix):
    for i in range(5):
        for j in range(5):
            if key_matrix[i][j] == char:
                return i, j

# Hàm chính để mã hóa văn bản
def encode(plaintext, key):
    plaintext = plaintext.replace(" ", "").upper()  # Chuyển đổi văn bản thành chữ in hoa và loại bỏ khoảng trắng
    key_matrix = generate_key_matrix(key)
    encoded_text = ""
    i = 0
    while i < len(plaintext):
        if i == len(plaintext) - 1 or plaintext[i] == plaintext[i + 1]:  # Đảm bảo cặp ký tự không giống nhau
            plaintext = plaintext[:i + 1] + 'X' + plaintext[i + 1:]
        encoded_text += encode_pair(plaintext[i:i + 2], key_matrix)
        i += 2
    return encoded_text

# Hàm chính để tạo giao diện và xử lý sự kiện
def main():
    def encode_text():
        plaintext = plaintext_entry.get()
        key = key_entry.get()
        encoded_text = encode(plaintext, key)
        encoded_text_display.delete(1.0, END)
        encoded_text_display.insert(END, encoded_text)

    root = Tk()
    root.title("Playfair Cipher")

    Label(root, text="Plaintext:").grid(row=0, column=0)
    Label(root, text="Key:").grid(row=1, column=0)
    Label(root, text="Encoded Text:").grid(row=2, column=0)

    plaintext_entry = Entry(root)
    plaintext_entry.grid(row=0, column=1)
    key_entry = Entry(root)
    key_entry.grid(row=1, column=1)
    encoded_text_display = Text(root, height=5, width=30)
    encoded_text_display.grid(row=2, column=1)

    encode_button = Button(root, text="Encode", command=encode_text)
    encode_button.grid(row=3, column=1, sticky=W)

    root.mainloop()

if __name__ == "__main__":
    main()
