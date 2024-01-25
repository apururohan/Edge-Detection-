import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import time

def apply_operator(operator_name, image):
    start_time = time.time()
    if operator_name == "Roberts":
        operator = np.array([[1, 0], [0, -1]])
        gradient_image = cv2.filter2D(image, -1, operator)
    elif operator_name == "Sobel":
        sobel_x = cv2.getDerivKernels(1, 0, 3, normalize=True)[0]
        sobel_y = cv2.getDerivKernels(0, 1, 3, normalize=True)[0]
        operator = np.dot(sobel_x, sobel_y.T)
        gradient_image = cv2.filter2D(image, -1, operator)
    elif operator_name == "Prewitt":
        operator = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        gradient_image = cv2.filter2D(image, -1, operator)
    elif operator_name == "Canny":
        gradient_image = cv2.Canny(image, 100, 200)
    elif operator_name == "Laplacian of Gaussian":
        blurred = cv2.GaussianBlur(image, (3, 3), 0)
        gradient_image = cv2.Laplacian(blurred, cv2.CV_64F)
        

    execution_time = time.time() - start_time
    return gradient_image, execution_time

def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        return image
    else:
        return None

def apply_operator_and_display(operator_name):
    global image
    if image is None:
        return
    
    gradient_image, execution_time = apply_operator(operator_name, image)
    
    # Display the gradient image in a new window
    window = tk.Toplevel(root)
    window.title(operator_name + " Operator")
    tk.Label(window, text=f"Execution Time: {execution_time:.6f} seconds").pack()
    if operator_name!="Laplacian of Gaussian":
        gradient_image_rgb = cv2.cvtColor(gradient_image, cv2.COLOR_BGR2RGB)
    else:
        gradient_image_rgb=gradient_image
    img = Image.fromarray(gradient_image_rgb)
    img_tk = ImageTk.PhotoImage(image=img)
    label = tk.Label(window, image=img_tk)
    label.image = img_tk
    label.pack()

def main():
    global image
    image = None

    def select_image_callback():
        global image
        image = select_image()

    global root
    root = tk.Tk()
    root.title("Edge Detection")
    root.geometry("400x200")  # Set window size

    # Title bar
    title_frame = tk.Frame(root)
    title_frame.pack(side="top", fill="x")
    title_label = tk.Label(title_frame, text="Edge Detection", font=("Arial", 12, "bold"))
    title_label.pack()

    select_image_button = tk.Button(root, text="Select Image", command=select_image_callback)
    select_image_button.pack(pady=10)

    operators_row1 = ["Roberts", "Sobel", "Prewitt"]
    button_frame_row1 = tk.Frame(root)
    button_frame_row1.pack()
    for operator in operators_row1:
        button = tk.Button(button_frame_row1, text=operator, command=lambda op=operator: apply_operator_and_display(op))
        button.pack(side="left", padx=5, pady=5)

    operators_row2 = ["Canny", "Laplacian of Gaussian"]
    button_frame_row2 = tk.Frame(root)
    button_frame_row2.pack()
    for operator in operators_row2:
        button = tk.Button(button_frame_row2, text=operator, command=lambda op=operator: apply_operator_and_display(op))
        button.pack(side="left", padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
