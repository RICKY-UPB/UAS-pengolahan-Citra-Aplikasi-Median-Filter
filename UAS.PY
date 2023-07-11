import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import cv2

original_img = None  # Tambahkan variabel untuk menyimpan citra asli


def histogram_equalization(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_eq = cv2.equalizeHist(img_gray)
    img_eq_color = cv2.cvtColor(img_eq, cv2.COLOR_GRAY2RGB)
    return img_eq_color


def median_filter(img):
    img_median = cv2.medianBlur(img, 5)
    return img_median


def calculate_mse(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    return mse


def calculate_psnr(mse):
    max_pixel = 255.0
    psnr = 10 * np.log10((max_pixel**2) / mse)
    return psnr


def browse_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        global original_img  # Gunakan variabel global
        img = Image.open(file_path)
        img.thumbnail((300, 300))  # Resize image to fit in the display box
        img_tk = ImageTk.PhotoImage(img)
        original_image_canvas.create_image(0, 0, anchor="nw", image=img_tk)
        original_image_canvas.image = img_tk
        original_img = img  # Simpan citra asli ke variabel global


def apply_filter():
    if original_img is None:  # Periksa apakah ada citra asli yang dipilih
        return

    selected_filter = filter_var.get()
    if selected_filter == 1:
        filtered_img = histogram_equalization(np.array(original_img))
        filtered_image_label.config(text="Citra Histogram Equalizer")
    elif selected_filter == 2:
        filtered_img = median_filter(np.array(original_img))
        filtered_image_label.config(text="Citra Median Filter")

    filtered_img = Image.fromarray(filtered_img)
    # Resize image to fit in the display box
    filtered_img.thumbnail((300, 300))
    filtered_img_tk = ImageTk.PhotoImage(filtered_img)
    filtered_image_canvas.create_image(
        0, 0, anchor="nw", image=filtered_img_tk)
    filtered_image_canvas.image = filtered_img_tk

    mse = calculate_mse(np.array(original_img), np.array(filtered_img))
    psnr = calculate_psnr(mse)
    mse_label.configure(text="MSE: {:.2f}".format(mse))
    psnr_label.configure(text="PSNR: {:.2f}".format(psnr))


# Create the main window
window = tk.Tk()
window.title("Image Processing")
window.geometry("800x600")
window.resizable(False, False)  # Mengatur jendela agar ukurannya permanen

# Create the canvas
canvas = tk.Canvas(window, width=800, height=600)
canvas.pack()

# Create the top section with green pastel background
top_canvas = tk.Canvas(canvas, width=800, height=300, bg="#c3e6c0")
top_canvas.place(x=0, y=0)

# Create the original image canvas and label
original_image_canvas = tk.Canvas(top_canvas, width=300, height=300)
original_image_canvas.place(x=10, y=10)
original_image_label = tk.Label(top_canvas, text="Citra Asli")
original_image_label.place(x=10, y=320)

# Create thefiltered image canvas and label
filtered_image_canvas = tk.Canvas(top_canvas, width=300, height=300)
filtered_image_canvas.place(x=490, y=10)
filtered_image_label = tk.Label(top_canvas, text="Citra Hasil")
filtered_image_label.place(x=490, y=320)

# Create the bottom section with bright orange background
bottom_canvas = tk.Canvas(canvas, width=800, height=300, bg="#ffa726")
bottom_canvas.place(x=0, y=300)

# Create the file browse button
browse_button = tk.Button(
    bottom_canvas, text="Browse Image", command=browse_image)
browse_button.place(relx=0.2, rely=0.3, anchor="center")

# Create the filter radio buttons
filter_var = tk.IntVar()
histogram_button = tk.Radiobutton(
    bottom_canvas, text="Histogram Equalizer", variable=filter_var, value=1)
histogram_button.place(relx=0.5, rely=0.3, anchor="center")

median_button = tk.Radiobutton(
    bottom_canvas, text="Median Filter", variable=filter_var, value=2)
median_button.place(relx=0.5, rely=0.4, anchor="center")

# Create the apply filter button
apply_button = tk.Button(bottom_canvas, text="Apply", command=apply_filter)
apply_button.place(relx=0.8, rely=0.3, anchor="center")

# Create the MSE label
mse_label = tk.Label(bottom_canvas, text="MSE: ")
mse_label.place(relx=0.5, rely=0.6, anchor="center")

# Create the PSNR label
psnr_label = tk.Label(bottom_canvas, text="PSNR: ")
psnr_label.place(relx=0.5, rely=0.5, anchor="center")

# Create the text labels at the bottom
text_label1 = tk.Label(
    canvas, text="RIKI SUPRIYATNA 312110025", font=("Arial", 12, "bold"))
text_label1.place(relx=0.5, rely=0.9, anchor="center")

text_label2 = tk.Label(
    canvas, text="UNIVERSITAS PELITA BANGSA", font=("Arial", 12, "bold"))
text_label2.place(relx=0.5, rely=0.95, anchor="center")

# Create the dividing line
dividing_line = tk.Canvas(canvas, width=2, height=280,
                          bg="black", highlightthickness=0)
dividing_line.place(x=400, y=10)

# Run the GUI
window.mainloop()
