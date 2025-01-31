import tkinter as tk  # for creating the GUI

def inspect_script():  # Function to inspect the script
    script = file_path_entry.get()  # Get the file path from the Entry widget
    if script:
        try:
            with open(script, 'r') as f:  # Open the provided file in read mode
                lines = f.readlines()  # Read all lines from the file
                file_content = ''.join(lines)  # Join all lines into a single string
                text_box.delete(1.0, tk.END)  # Clear previous content in the text box
                text_box.insert(tk.END, file_content)  # Insert the file content into the text box
        except FileNotFoundError:
            text_box.delete(1.0, tk.END)  # Clear previous content in case of an error using the text_box object
            text_box.insert(tk.END, f"File not found: {script}")
        except Exception as e:
            text_box.delete(1.0, tk.END)  # Clear previous content in case of an error
            text_box.insert(tk.END, f"Error reading file: {e}")

# Create the main window
window = tk.Tk()
window.title("Script Inspector")

# Create a label to guide the user to enter the file path
file_path_label = tk.Label(window, text="Enter script file path including directory:")
file_path_label.pack(pady=5)

# Create an Entry widget where the user will input the script file path
file_path_entry = tk.Entry(window, width=60)
file_path_entry.pack(pady=5)

# Create a button to trigger the script inspection
button = tk.Button(window, text="Inspect Script", command=inspect_script)
button.pack(pady=10)

# Create a Text widget to display the file contents
text_box = tk.Text(window, height=20, width=80)
text_box.pack(pady=10)

# Start the GUI event loop
window.mainloop()