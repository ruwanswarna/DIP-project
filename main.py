from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import cv2 as cv
import numpy as np

fileLocation = "images/placeholder.jpg"
green_blue = "images/placeholder.jpg"


# fileLocation = "images/class.png"

def bgr_to_cmyk(image_bgr):
    # Normalize BGR channels
    b, g, r = cv.split(image_bgr.astype(np.float32) / 255.0)

    # Convert to CMY
    c = 1 - r
    m = 1 - g
    y = 1 - b

    # Find K (black)
    k = np.minimum(np.minimum(c, m), y)

    # Avoid division by zero
    with np.errstate(divide='ignore', invalid='ignore'):
        # Calculate C (cyan)
        c = (c - k) / (1 - k)
        # Calculate M (magenta)
        m = (m - k) / (1 - k)
        # Calculate Y (yellow)
        y = (y - k) / (1 - k)

    # Replace NaN values with 0
    c = np.nan_to_num(c)
    m = np.nan_to_num(m)
    y = np.nan_to_num(y)
    k = np.nan_to_num(k)

    # Scale to range [0, 255]
    c = (c * 255).astype(np.uint8)
    m = (m * 255).astype(np.uint8)
    y = (y * 255).astype(np.uint8)
    k = (k * 255).astype(np.uint8)

    # Merge CMYK channels
    cmyk_image = cv.merge((c, m, y, k))

    return cmyk_image


def adjust_histogram(img):
    # Split image channels
    b, g, r = cv.split(img)
    # Calculate histogram for the green channel
    hist = cv.calcHist([g], [0], None, [256], [0, 256])
    # Find the index of the maximum value in the histogram
    peak_index = np.argmax(hist)

    offset = 140 - peak_index

    adjusted_image = img + offset

    # Clip values to ensure they stay within the valid range [0, 255]
    adjusted_image = np.clip(adjusted_image, 0, 255).astype(np.uint8)

    return adjusted_image



def selectFile():
    global fileLocation
    global original_image_label
    global original_image
    global resized_original

    root.filename = filedialog.askopenfilename(initialdir="C:/Users", title="SElect a file",
                                               filetypes=(("png files", "*.png"), ("jpg files", "*.jpg"),
                                                          ("jpeg files", "*.jpeg"),
                                                          ("all files", "*.*")))
    fileLocation = root.filename
    original_image_label.grid_forget()
    original_image = Image.open(fileLocation)
    resized_original = original_image.resize((250, 250), Image.LANCZOS)
    resized_original = ImageTk.PhotoImage(resized_original)
    original_image_label = Label(originalImageFrame, image=resized_original)
    original_image_label.grid(row=0, column=0)

    subtract_blue_from_green()
    k_channel_of_cmyk()
    b_channel_of_cielab()
    h_channel_of_hsv()

    identify_nymphs()
    identify_adults()
    identify_exoskeletons()
    identify_lesions_fungi()


def selectFolder():
    print("Hello World!")


def subtract_blue_from_green():
    global resized_g_b
    global g_b_image_label

    g_b_image_label.grid_forget()
    img = cv.imread(fileLocation)
    blue, green, red = cv.split(img)
    green_blue = green - blue
    img = Image.fromarray(green_blue)

    img_resized = img.resize((250, 250))
    green_blue_resized = cv.resize(green_blue, (600, 600), interpolation=cv.INTER_AREA)

    cv.imshow('subtract_blue_from_green', green_blue_resized)
    resized_g_b = ImageTk.PhotoImage(img_resized)
    g_b_image_label = Label(g_bFrame, image=resized_g_b)

    g_b_image_label.grid(row=0, column=0)


def k_channel_of_cmyk():
    global resized_k_channel
    global k_channel_image_label

    k_channel_image_label.grid_forget()
    img = cv.imread(fileLocation)
    rgb_image = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    # Normalize RGB values to range [0, 1]
    rgb_image = rgb_image.astype(np.float32) / 255.0

    # Convert RGB to k channel
    k = np.min(rgb_image, axis=2)  # black channel
    img = Image.fromarray((k * 255).astype(np.uint8))

    img_resized = img.resize((250, 250))
    k_channel_resized = cv.resize(k, (600, 600), interpolation=cv.INTER_AREA)

    cv.imshow('k Channel of CMYK Color Space', k_channel_resized)
    resized_k_channel = ImageTk.PhotoImage(img_resized)
    k_channel_image_label = Label(k_channelFrame, image=resized_k_channel)

    k_channel_image_label.grid(row=0, column=0)


def b_channel_of_cielab():
    global resized_b_channel
    global b_channel_image_label

    b_channel_image_label.grid_forget()
    img = cv.imread(fileLocation)
    cielab_image = cv.cvtColor(img, cv.COLOR_BGR2Lab)
    l, a, b = cv.split(cielab_image)
    img = Image.fromarray(b)

    img_resized = img.resize((250, 250))
    b_channel_resized = cv.resize(b, (600, 600), interpolation=cv.INTER_AREA)

    cv.imshow('b Channel of CIELAB Color Space', b_channel_resized)
    resized_b_channel = ImageTk.PhotoImage(img_resized)
    b_channel_image_label = Label(b_channelFrame, image=resized_b_channel)

    b_channel_image_label.grid(row=0, column=0)


def h_channel_of_hsv():
    global resized_h_channel
    global h_channel_image_label

    h_channel_image_label.grid_forget()
    img = cv.imread(fileLocation)
    hsv_image = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv_image)
    img = Image.fromarray(h)

    img_resized = img.resize((250, 250))
    h_channel_resized = cv.resize(h, (600, 600), interpolation=cv.INTER_AREA)

    cv.imshow('h Channel of HSV Color Space', h_channel_resized)
    resized_h_channel = ImageTk.PhotoImage(img_resized)
    h_channel_image_label = Label(h_channelFrame, image=resized_h_channel)

    h_channel_image_label.grid(row=0, column=0)


def create_threshold_image_1(img):
    global ThresholdImageFrame1_image_label
    t, thresh_img = cv.threshold(img, 230, 255, cv.THRESH_BINARY)
    thresh_img_opencv = thresh_img
    thresh_img_resized = cv.resize(thresh_img, (600, 600), interpolation=cv.INTER_AREA)
    cv.imshow('RGB-LAB-XYZ(Z-channel)-Thresholded Image', thresh_img_resized)

    ThresholdImageFrame1_image_label.grid_forget()
    thresh_img = Image.fromarray(thresh_img)
    thresh_img_resized = thresh_img.resize((300, 300))
    thresh_img_resized = ImageTk.PhotoImage(thresh_img_resized)

    ThresholdImageFrame1_image_label = Label(ThresholdImageFrame1, image=thresh_img_resized)
    ThresholdImageFrame1_image_label.image = thresh_img_resized
    ThresholdImageFrame1_image_label.grid(row=0, column=0)

    return thresh_img_opencv


def create_threshold_image_2(img):
    global ThresholdImageFrame2_image_label
    t, thresh_img = cv.threshold(img, 13, 255, cv.THRESH_BINARY_INV)
    thresh_img_opencv = thresh_img
    thresh_img_resized = cv.resize(thresh_img, (600, 600), interpolation=cv.INTER_AREA)
    cv.imshow('RGB-XYZ-XYZ-CMYK(C-channel)-Thresholded Image', thresh_img_resized)

    ThresholdImageFrame2_image_label.grid_forget()
    thresh_img = Image.fromarray(thresh_img)
    thresh_img_resized = thresh_img.resize((300, 300))
    thresh_img_resized = ImageTk.PhotoImage(thresh_img_resized)

    ThresholdImageFrame2_image_label = Label(ThresholdImageFrame2, image=thresh_img_resized)
    ThresholdImageFrame2_image_label.image = thresh_img_resized
    ThresholdImageFrame2_image_label.grid(row=0, column=0)

    return thresh_img_opencv


def create_threshold_image_3(img):
    global ThresholdImageFrame3_image_label
    t, thresh_img = cv.threshold(img, 64, 255, cv.THRESH_BINARY_INV)
    thresh_img_opencv = thresh_img
    thresh_img_resized = cv.resize(thresh_img, (600, 600), interpolation=cv.INTER_AREA)
    cv.imshow('RGB-CMYK-XYZ(Z-channel)-Thresholded Image', thresh_img_resized)

    ThresholdImageFrame3_image_label.grid_forget()
    thresh_img = Image.fromarray(thresh_img)
    thresh_img_resized = thresh_img.resize((300, 300))
    thresh_img_resized = ImageTk.PhotoImage(thresh_img_resized)

    ThresholdImageFrame3_image_label = Label(ThresholdImageFrame3, image=thresh_img_resized)
    ThresholdImageFrame3_image_label.image = thresh_img_resized
    ThresholdImageFrame3_image_label.grid(row=0, column=0)

    return thresh_img_opencv


def create_threshold_image_4(img):
    global ThresholdImageFrame4_image_label
    t, thresh_img = cv.threshold(img, 128, 255, cv.THRESH_BINARY_INV)
    thresh_img_opencv = thresh_img
    thresh_img_resized = cv.resize(thresh_img, (600, 600), interpolation=cv.INTER_AREA)
    cv.imshow('RGB-LAB-CMYK(M-channel)-Thresholded Image', thresh_img_resized)

    ThresholdImageFrame4_image_label.grid_forget()
    thresh_img = Image.fromarray(thresh_img)
    thresh_img_resized = thresh_img.resize((300, 300))
    thresh_img_resized = ImageTk.PhotoImage(thresh_img_resized)

    ThresholdImageFrame4_image_label = Label(ThresholdImageFrame4, image=thresh_img_resized)
    ThresholdImageFrame4_image_label.image = thresh_img_resized
    ThresholdImageFrame4_image_label.grid(row=0, column=0)

    return thresh_img_opencv


def remove_noisy_objects(thresh_img, num):
    global ThresholdImageFrame5_image_label
    global ThresholdImageFrame6_image_label
    global ThresholdImageFrame7_image_label
    global ThresholdImageFrame8_image_label
    # Find contours
    contours, _ = cv.findContours(thresh_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Compute contour areas
    contour_areas = [cv.contourArea(contour) for contour in contours]
    print(contour_areas)
    # Find the largest contour
    largest_contour_index = np.argmax(contour_areas)
    largest_contour_area = contour_areas[largest_contour_index]

    # Define a threshold for filtering small contours (e.g., 10% of the largest contour area)
    threshold_area = 0.1 * largest_contour_area

    # Filter out small contours
    filtered_contours = [contour for contour, area in zip(contours, contour_areas) if area >= threshold_area]

    # Create a blank image to draw the remaining contours
    result_img = np.zeros_like(thresh_img)

    # Draw remaining contours on the result image
    cv.drawContours(result_img, filtered_contours, -1, 255, thickness=cv.FILLED)

    thresh_img_resized = cv.resize(result_img, (600, 600), interpolation=cv.INTER_AREA)
    if num == 5:
        cv.imshow('RGB-LAB-CMYK(M-channel)-Thresholded Image Without Noisy Objects', thresh_img_resized)

        ThresholdImageFrame5_image_label.grid_forget()
        thresh_img = Image.fromarray(thresh_img)
        thresh_img_resized = thresh_img.resize((300, 300))
        thresh_img_resized = ImageTk.PhotoImage(thresh_img_resized)

        ThresholdImageFrame5_image_label = Label(ThresholdImageFrame5, image=thresh_img_resized)
        ThresholdImageFrame5_image_label.image = thresh_img_resized
        ThresholdImageFrame5_image_label.grid(row=0, column=0)

    elif num == 6:
        ThresholdImageFrame6_image_label.grid_forget()
        thresh_img = Image.fromarray(thresh_img)
        thresh_img_resized = thresh_img.resize((300, 300))
        thresh_img_resized = ImageTk.PhotoImage(thresh_img_resized)

        ThresholdImageFrame6_image_label = Label(ThresholdImageFrame6, image=thresh_img_resized)
        ThresholdImageFrame6_image_label.image = thresh_img_resized
        ThresholdImageFrame6_image_label.grid(row=0, column=0)

    elif num == 7:
        ThresholdImageFrame7_image_label.grid_forget()
        thresh_img = Image.fromarray(thresh_img)
        thresh_img_resized = thresh_img.resize((300, 300))
        thresh_img_resized = ImageTk.PhotoImage(thresh_img_resized)

        ThresholdImageFrame7_image_label = Label(ThresholdImageFrame7, image=thresh_img_resized)
        ThresholdImageFrame7_image_label.image = thresh_img_resized
        ThresholdImageFrame7_image_label.grid(row=0, column=0)

    elif num == 8:
        ThresholdImageFrame8_image_label.grid_forget()
        thresh_img = Image.fromarray(thresh_img)
        thresh_img_resized = thresh_img.resize((300, 300))
        thresh_img_resized = ImageTk.PhotoImage(thresh_img_resized)

        ThresholdImageFrame8_image_label = Label(ThresholdImageFrame8, image=thresh_img_resized)
        ThresholdImageFrame8_image_label.image = thresh_img_resized
        ThresholdImageFrame8_image_label.grid(row=0, column=0)

    return result_img

def identify_nymphs():
    global resized_transformation1
    global transformation1_image_label

    transformation1_image_label.grid_forget()
    img = cv.imread(fileLocation)
    img = adjust_histogram(img)
    cielab_image = cv.cvtColor(img, cv.COLOR_BGR2LAB)
    xyz_image = cv.cvtColor(cielab_image, cv.COLOR_BGR2XYZ)
    x, y, z = cv.split(xyz_image)
    img = Image.fromarray(z)

    img_resized = img.resize((250, 250))
    transformation1_resized = cv.resize(z, (600, 600), interpolation=cv.INTER_AREA)
    cv.imshow('RGB-LAB-XYZ(Z-channel)', transformation1_resized)
    resized_transformation1 = ImageTk.PhotoImage(img_resized)
    transformation1_image_label = Label(transformation1_Frame, image=resized_transformation1)

    transformation1_image_label.grid(row=0, column=0)

    thresh_img = create_threshold_image_1(z)
    thresh_img_without_noise = remove_noisy_objects(thresh_img, 5)

def identify_adults():
    global resized_transformation2
    global transformation2_image_label

    transformation2_image_label.grid_forget()
    img = cv.imread(fileLocation)
    img = adjust_histogram(img)
    xyz_image = cv.cvtColor(img, cv.COLOR_BGR2XYZ)
    xyz_image = cv.cvtColor(xyz_image, cv.COLOR_BGR2XYZ)
    cmyk_image = bgr_to_cmyk(xyz_image)
    c, m, y, k = cv.split(cmyk_image)
    img = Image.fromarray(c)

    img_resized = img.resize((250, 250))
    transformation2_resized = cv.resize(c, (600, 600), interpolation=cv.INTER_AREA)
    cv.imshow('RGB-XYZ-XYZ-CMYK(C-channel)', transformation2_resized)
    resized_transformation2 = ImageTk.PhotoImage(img_resized)
    transformation2_image_label = Label(transformation2_Frame, image=resized_transformation2)

    transformation2_image_label.grid(row=0, column=0)

    thresh_img = create_threshold_image_2(c)
    thresh_img_without_noise = remove_noisy_objects(thresh_img, 6)


def identify_exoskeletons():
    global resized_transformation3
    global transformation3_image_label

    transformation3_image_label.grid_forget()
    img = cv.imread(fileLocation)
    img = adjust_histogram(img)
    cmyk_image = bgr_to_cmyk(img)
    c, m, y, k = cv.split(cmyk_image)
    cmy_image = cv.merge((c, m, y))
    xyz_image = cv.cvtColor(cmy_image, cv.COLOR_BGR2XYZ)
    x, y, z = cv.split(xyz_image)
    img = Image.fromarray(z)

    img_resized = img.resize((250, 250))
    transformation3_resized = cv.resize(z, (600, 600), interpolation=cv.INTER_AREA)
    cv.imshow('RGB-XYZ-XYZ-CMYK(C-channel)', transformation3_resized)
    resized_transformation3 = ImageTk.PhotoImage(img_resized)
    transformation3_image_label = Label(transformation3_Frame, image=resized_transformation3)

    transformation3_image_label.grid(row=0, column=0)

    thresh_img = create_threshold_image_3(z)
    thresh_img_without_noise = remove_noisy_objects(thresh_img, 7)


def identify_lesions_fungi():
    global resized_transformation4
    global transformation4_image_label

    transformation4_image_label.grid_forget()
    img = cv.imread(fileLocation)
    img = adjust_histogram(img)
    cielab_image = cv.cvtColor(img, cv.COLOR_BGR2LAB)
    cmyk_image = bgr_to_cmyk(cielab_image)
    c, m, y, k = cv.split(cmyk_image)
    img = Image.fromarray(m)

    img_resized = img.resize((250, 250))
    transformation4_resized = cv.resize(m, (600, 600), interpolation=cv.INTER_AREA)
    cv.imshow('RGB-XYZ-XYZ-CMYK(C-channel)', transformation4_resized)
    resized_transformation4 = ImageTk.PhotoImage(img_resized)
    transformation4_image_label = Label(transformation4_Frame, image=resized_transformation4)

    transformation4_image_label.grid(row=0, column=0)

    thresh_img = create_threshold_image_4(m)
    thresh_img_without_noise = remove_noisy_objects(thresh_img, 8)


root = Tk()
root.title("white flies detection")
root.iconbitmap('images/bug_icon.ico')

# ---------------------info Frame------------------------------

infoFrame = Frame(root, padx=10, pady=10)
infoFrame.grid(row=0, column=0, padx=1, pady=1)

inputFileLabel = Label(infoFrame, text="Select image file: ")
inputFolderLabel = Label(infoFrame, text="Select image directory: ")
inputFileLabel.grid(row=0, column=0, padx=1, pady=1)
inputFolderLabel.grid(row=1, column=0, padx=1, pady=1)

selectFolderButton = Button(infoFrame, text="Select", command=selectFolder)

selectFolderButton.grid(row=1, column=1, padx=1, pady=1)

Label1 = Label(infoFrame, text="Nymphs: ")
Label2 = Label(infoFrame, text="Adults: ")
Label3 = Label(infoFrame, text="Exoskeletons: ")
Label4 = Label(infoFrame, text="Leisions/Fungi: ")
Label1.grid(row=2, column=0, padx=1, pady=1)
Label2.grid(row=3, column=0, padx=1, pady=1)
Label3.grid(row=4, column=0, padx=1, pady=1)
Label4.grid(row=5, column=0, padx=1, pady=1)

Label5 = Label(infoFrame, text="--")
Label6 = Label(infoFrame, text="--")
Label7 = Label(infoFrame, text="--")
Label8 = Label(infoFrame, text="--")
Label5.grid(row=2, column=1, padx=1, pady=1)
Label6.grid(row=3, column=1, padx=1, pady=1)
Label7.grid(row=4, column=1, padx=1, pady=1)
Label8.grid(row=5, column=1, padx=1, pady=1)

Label9 = Label(infoFrame, text="Nymphs %: ")
Label10 = Label(infoFrame, text="Adults %: ")
Label11 = Label(infoFrame, text="Exoskeletons %: ")
Label12 = Label(infoFrame, text="Leisions/Fungi %: ")
Label9.grid(row=6, column=0, padx=1, pady=1)
Label10.grid(row=7, column=0, padx=1, pady=1)
Label11.grid(row=8, column=0, padx=1, pady=1)
Label12.grid(row=9, column=0, padx=1, pady=1)

Label13 = Label(infoFrame, text="--")
Label14 = Label(infoFrame, text="--")
Label15 = Label(infoFrame, text="--")
Label16 = Label(infoFrame, text="--")
Label13.grid(row=6, column=1, padx=1, pady=1)
Label14.grid(row=7, column=1, padx=1, pady=1)
Label15.grid(row=8, column=1, padx=1, pady=1)
Label16.grid(row=9, column=1, padx=1, pady=1)
# -------------------end info Frame------------------------------

placeholder = Image.open("images/placeholder.jpg")
resized_placeholder = placeholder.resize((250, 250), Image.LANCZOS)
resized_placeholder = ImageTk.PhotoImage(resized_placeholder)

# ------------------------original image Frame---------------------------

originalImageFrame = LabelFrame(root, text="Original Image", padx=1, pady=1)
originalImageFrame.grid(row=0, column=1, padx=5, pady=5)
original_image_label = Label(originalImageFrame, image=resized_placeholder)
original_image_label.grid(row=0, column=0)

# ------------------------end original image Frame---------------------------


# ------------------------Subtracting blue channel from green channel image Frame---------------------------
g_bFrame = LabelFrame(root, text="Subtracting blue channel from green channel", padx=1, pady=1)
g_bFrame.grid(row=0, column=2, padx=5, pady=5)
g_b_image_label = Label(g_bFrame, image=resized_placeholder)
g_b_image_label.grid(row=0, column=0)
# ------------------------end Subtracting blue channel from green channel image Frame---------------------------


# ------------------------K channel of CMYK image Frame---------------------------
k_channelFrame = LabelFrame(root, text="K channel of CMYK", padx=1, pady=1)
k_channelFrame.grid(row=0, column=3, padx=5, pady=5)
k_channel_image_label = Label(k_channelFrame, image=resized_placeholder)
k_channel_image_label.grid(row=0, column=0)
# ------------------------end K channel of CMYK image Frame---------------------------


# ------------------------b channel of CIELAB image Frame---------------------------
b_channelFrame = LabelFrame(root, text="b channel of CIELAB", padx=1, pady=1)
b_channelFrame.grid(row=0, column=4, padx=1, pady=1)
b_channel_image_label = Label(b_channelFrame, image=resized_placeholder)
b_channel_image_label.grid(row=0, column=0)
# ------------------------end b channel of CIELAB image Frame---------------------------


# ------------------------h channel of HSV image Frame---------------------------
h_channelFrame = LabelFrame(root, text="h channel of HSV", padx=1, pady=1)
h_channelFrame.grid(row=1, column=0, padx=1, pady=1)
h_channel_image_label = Label(h_channelFrame, image=resized_placeholder)
h_channel_image_label.grid(row=0, column=0)
# ------------------------end h channel of HSV image Frame---------------------------


# ------------------------color space transformation 1 image Frame---------------------------
transformation1_Frame = LabelFrame(root, text="RGB-LAB-XYZ(Z-channel)", padx=1, pady=1)
transformation1_Frame.grid(row=1, column=1, padx=1, pady=1)
transformation1_image_label = Label(transformation1_Frame, image=resized_placeholder)
transformation1_image_label.grid(row=0, column=0)
# ------------------------end color space transformation 1 image Frame---------------------------


# ------------------------color space transformation 2 image Frame---------------------------
transformation2_Frame = LabelFrame(root, text="RGB-XYZ-XYZ-CMYK(C-channel)", padx=1, pady=1)
transformation2_Frame.grid(row=1, column=2, padx=1, pady=1)
transformation2_image_label = Label(transformation2_Frame, image=resized_placeholder)
transformation2_image_label.grid(row=0, column=0)
# ------------------------end color space transformation 2 image Frame---------------------------


# ------------------------color space transformation 3 image Frame---------------------------
transformation3_Frame = LabelFrame(root, text="RGB-CMYK-XYZ(Z-channel)", padx=1, pady=1)
transformation3_Frame.grid(row=1, column=3, padx=1, pady=1)
transformation3_image_label = Label(transformation3_Frame, image=resized_placeholder)
transformation3_image_label.grid(row=0, column=0)
# ------------------------end color space transformation 2 image Frame---------------------------


# ------------------------color space transformation 4 image Frame---------------------------
transformation4_Frame = LabelFrame(root, text="RGB-LAB-CMYK(M-channel)", padx=1, pady=1)
transformation4_Frame.grid(row=1, column=4, padx=1, pady=1)
transformation4_image_label = Label(transformation4_Frame, image=resized_placeholder)
transformation4_image_label.grid(row=0, column=0)
# ------------------------end color space transformation 2 image Frame---------------------------

top = Toplevel()
top.title("----Images After Thresholding----")
top.iconbitmap('images/bug_icon.ico')

ThresholdImageFrame1 = LabelFrame(top, text="RGB-LAB-XYZ(Z-channel)-Thresh Img", padx=1, pady=1)
ThresholdImageFrame1.grid(row=0, column=0, padx=1, pady=1)
ThresholdImageFrame1_image_label = Label(ThresholdImageFrame1, image=resized_placeholder)
ThresholdImageFrame1_image_label.grid(row=0, column=0)

ThresholdImageFrame2 = LabelFrame(top, text="RGB-XYZ-XYZ-CMYK(C-channel)-Thresh Img", padx=1, pady=1)
ThresholdImageFrame2.grid(row=0, column=1, padx=1, pady=1)
ThresholdImageFrame2_image_label = Label(ThresholdImageFrame2, image=resized_placeholder)
ThresholdImageFrame2_image_label.grid(row=0, column=0)

ThresholdImageFrame3 = LabelFrame(top, text="RGB-CMYK-XYZ(Z-channel)-Thresh Img", padx=1, pady=1)
ThresholdImageFrame3.grid(row=0, column=2, padx=1, pady=1)
ThresholdImageFrame3_image_label = Label(ThresholdImageFrame3, image=resized_placeholder)
ThresholdImageFrame3_image_label.grid(row=0, column=0)

ThresholdImageFrame4 = LabelFrame(top, text="RGB-LAB-CMYK(M-channel)-Thresh Img", padx=1, pady=1)
ThresholdImageFrame4.grid(row=0, column=3, padx=1, pady=1)
ThresholdImageFrame4_image_label = Label(ThresholdImageFrame4, image=resized_placeholder)
ThresholdImageFrame4_image_label.grid(row=0, column=0)

ThresholdImageFrame5 = LabelFrame(top, text="RGB-LAB-XYZ(Z-channel)-Thresh Img WO Noisy Objects", padx=1, pady=1)
ThresholdImageFrame5.grid(row=1, column=0, padx=1, pady=1)
ThresholdImageFrame5_image_label = Label(ThresholdImageFrame5, image=resized_placeholder)
ThresholdImageFrame5_image_label.grid(row=0, column=0)

ThresholdImageFrame6 = LabelFrame(top, text="RGB-XYZ-XYZ-CMYK(C-channel)-Thresh Img WO Noisy Objects", padx=1, pady=1)
ThresholdImageFrame6.grid(row=1, column=1, padx=1, pady=1)
ThresholdImageFrame6_image_label = Label(ThresholdImageFrame6, image=resized_placeholder)
ThresholdImageFrame6_image_label.grid(row=0, column=0)

ThresholdImageFrame7 = LabelFrame(top, text="RGB-CMYK-XYZ(Z-channel)-Thresh Img WO Noisy Objects", padx=1, pady=1)
ThresholdImageFrame7.grid(row=1, column=2, padx=1, pady=1)
ThresholdImageFrame7_image_label = Label(ThresholdImageFrame7, image=resized_placeholder)
ThresholdImageFrame7_image_label.grid(row=0, column=0)

ThresholdImageFrame8 = LabelFrame(top, text="RGB-LAB-CMYK(M-channel)-Thresh Img WO Noisy Objects", padx=1, pady=1)
ThresholdImageFrame8.grid(row=1, column=3, padx=1, pady=1)
ThresholdImageFrame8_image_label = Label(ThresholdImageFrame8, image=resized_placeholder)
ThresholdImageFrame8_image_label.grid(row=0, column=0)

selectFileButton = Button(infoFrame, text="Select", command=selectFile)
selectFileButton.grid(row=0, column=1, padx=1, pady=1)

root.mainloop()
