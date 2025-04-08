import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from stegano import lsb  # Importing the stegano library for LSB steganography

def select_file():
    filepath = filedialog.askopenfilename(title="Select Cover Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if filepath:
        file_label.config(text=filepath)
        show_image(filepath)

def show_image(filepath):
    try:
        img = Image.open(filepath)
        img = img.resize((200, 200), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk
    except Exception as e:
        messagebox.showerror("Error", f"Unable to load image: {e}")

def cancel_image():
    file_label.config(text="No file selected")
    image_label.config(image="")

def embed_data():
    filepath = file_label.cget("text")
    if filepath == "No file selected":
        messagebox.showwarning("Warning", "Please select an image first.")
        return

    secret_message = embed_entry.get()
    if not secret_message:
        messagebox.showwarning("Warning", "Please enter the data to hide.")
        return

    try:
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")], title="Save Stego Image")
        if not output_path:
            return

        lsb.hide(filepath, message=secret_message).save(output_path)
        messagebox.showinfo("Success", "Data embedded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to embed data: {e}")

def extract_data():
    filepath = file_label.cget("text")
    if filepath == "No file selected":
        messagebox.showwarning("Warning", "Please select an image first.")
        return

    try:
        extracted_message = lsb.reveal(filepath)
        if extracted_message:
            messagebox.showinfo("Extracted Data", f"Hidden Message: {extracted_message}")
        else:
            messagebox.showinfo("No Data", "No hidden message found in the image.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to extract data: {e}")

# Create the main window
root = tk.Tk()
root.title("Steganography Tool")
root.geometry("600x400")
root.configure(bg="dark grey")

# Left Panel (Image Display)
left_frame = tk.Frame(root, width=300, height=400, bg="dark grey")
left_frame.pack(side="left", fill="both", expand=True)

image_label = tk.Label(left_frame, bg="dark grey")
image_label.pack(pady=20)

# Right Panel (Controls)
right_frame = tk.Frame(root, width=300, height=400, bg="lightcyan3")
right_frame.pack(side="right", fill="both", expand=True)

file_label = tk.Label(right_frame, text="No file selected", bg="light blue", wraplength=250)
file_label.pack(pady=10)

select_file_button = tk.Button(right_frame, text="Select Cover Image", bg="deep sky blue", command=select_file)
select_file_button.pack(pady=5)

embed_label = tk.Label(right_frame, text="Data to hide:", bg="light blue")
embed_label.pack(pady=5)

embed_entry = tk.Entry(right_frame, width=30)
embed_entry.pack(pady=5)

embed_button = tk.Button(right_frame, text="Embed Data", bg="lime green", command=embed_data)
embed_button.pack(pady=10)

extract_button = tk.Button(right_frame, text="Extract Data", bg="yellow", command=extract_data)
extract_button.pack(pady=10)

cancel_button = tk.Button(right_frame, text="Cancel", bg="firebrick1", command=cancel_image)
cancel_button.pack(pady=10)

# Run the application
root.mainloop()
