from tkinter import *
from tkinter import filedialog
import os
import numpy as np
import math

def open_file(title):
    file_path = filedialog.askopenfilename(title=f"Select {title} File")
    return process_file(file_path)

def open_folder(title):
    folder_path = filedialog.askdirectory(title=f"Select {title} Folder")
    return process_folder(folder_path)

def process_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        return np.array(content.split(), dtype=float)

def process_folder(folder_path):
    files_contents = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            content = process_file(file_path)
            files_contents.append(content)

    samples = get_samples(files_contents)
    return samples

def get_samples(files_contents):
    max_samples = max(len(content) for content in files_contents)
    get_samples = np.zeros(max_samples)

    for content in files_contents:
        get_samples[:len(content)] += content

    get_samples /= len(files_contents)
    return get_samples

def cross_correlation(x1, x2):
    N = len(x1)
    results = []

    for n in range(N+len(x2)-1):
        sum = 0
        for j in range(N):
            if n - j >= 0 and n - j < len(x2):
                sum += x1[j] * x2[(j-n)]
        results.append(((1/N)*sum))

    return results

def normalize_correlation(x1, x2, corr):
    N = len(x1)
    results = []
    for n in range(N):
        n1_sum = 0
        n2_sum = 0
        for j in range(N):
            n1_sum += x1[j]**2
            n2_sum += x2[j]**2
        results.append(corr[n] / ((1/N)*math.sqrt(n1_sum*n2_sum)))

    return results

# def calculate_mean_correlation(test_file, class_content):
#     num_samples = min(len(test_file), len(class_content))
#     correlation = cross_correlation(test_file[:num_samples], class_content[:num_samples])
#     normalized_corr = normalize_correlation(test_file, class_content, correlation)
#     return np.mean(normalized_corr)

def calculate_mean_correlation(test_file, class_content):
    num_samples = min(len(test_file), len(class_content))
    correlation = np.corrcoef(test_file[:num_samples], class_content[:num_samples])[0, 1]
    return correlation

def open_test_file():
    global test_file
    test_file = open_file("Test")

def open_class1_folder():
    global class1_content
    class1_content = open_folder("Class 1")

def open_class2_folder():
    global class2_content
    class2_content = open_folder("Class 2")

def decide_correlation():
    global test_file, class1_content, class2_content

    if test_file is None or class1_content is None or class2_content is None:
        result_label.config(text="Please open all files and folders.")
        return

    correlation_class1 = calculate_mean_correlation(test_file, class1_content)
    correlation_class2 = calculate_mean_correlation(test_file, class2_content)

    result_text = f"Average Correlation with Class 1: {correlation_class1:.4f}\nAverage Correlation with Class 2: {correlation_class2:.4f}"

    if correlation_class1 > correlation_class2:
        result_text += "\ndown movement of EOG signal."
    else:
        result_text += "\nup movement of EOG signal"

    result_label.config(text=result_text)

root = Tk()
root.geometry("350x400")
root.title("Template Matching for Signal Classification")
root.configure(bg="white")

test_file = None
class1_content = None
class2_content = None

Label(root, text="Template Matching", font=("Arial", 16), bg="white").pack(pady=10)

Button(root, text="Open Class 1 Folder", command=open_class1_folder, width=40, height=3).pack(pady=1)
Button(root, text="Open Class 2 Folder", command=open_class2_folder, width=40, height=3).pack(pady=1)
Button(root, text="Open Test File", command=open_test_file, width=40, height=3).pack(pady=1)
Button(root, text="Calculate Correlation", command=decide_correlation, width=40, height=3).pack(pady=2)

result_label = Label(root, text="", bg="white", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()
