from ast import Delete
import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageSequence
import webbrowser
import os

# Fetch API key from environment variable
API_KEY = os.getenv('NEWS_API_KEY')  # Ensure this is correctly set in your environment
URL = 'https://newsapi.org/v2/top-headlines'

def get_top_headlines(api_key, country, category):
    params = {
        'apiKey': api_key,
        'country': country,
        'category': category,
        'pageSize': 5
    }
    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(e)
        return None

def update_news():
    # country = country_var.get()
    selected_country = country_var.get().split(' - ')[0]  
    category = category_var.get()
    
    if not selected_country or not category:
        messagebox.showwarning("Input Error", "Please select both country and category.")
        return
    
    news_data = get_top_headlines(API_KEY, selected_country, category)
    if news_data and 'articles' in news_data:
        news_text = ""
        for article in news_data['articles']:
            news_text += f"Title: {article['title']}\n"
            news_text += f"Description: {article['description']}\n"
            news_text += f"URL: {article['url']}\n\n"
        news_display.config(state=tk.NORMAL)
        news_display.delete(1.0, tk.END)
        news_display.insert(tk.END, news_text)
        news_display.config(state=tk.DISABLED)
    else:
        messagebox.showerror("Error", "Failed to retrieve news or no articles found.")

def show_news_screen():
    menu_frame.pack_forget()
    url_frame.pack_forget()
    link_entry.delete(0, tk.END)
    news_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

def go_back_to_menu():
    news_frame.pack_forget()
    menu_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

def exit_program():
    root.quit()

def clear_screen():
    news_frame.pack_forget()
    url_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
def open_link_with_default_browser():
    link = link_entry.get()
    if link:
        try:
            print(f"Attempting to open link: {link}")
            webbrowser.open_new_tab(link)
            print("Link opened successfully.")
        except Exception as e:
            print(f"Error opening link: {e}")
            messagebox.showerror("Error", f"Could not open link: {e}")
    else:
        messagebox.showwarning("Input Error", "Please enter a URL.")

def initialize_ui():
    # Start with menu_frame only
    news_frame.pack_forget()
    url_frame.pack_forget()
    menu_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
# Function to handle GIF animation
def update_gif(frame_index):
    frame = gif_frames[frame_index]
    gif_label.config(image=frame)
    frame_index = (frame_index + 1) % len(gif_frames)
    menu_frame.after(50, update_gif, frame_index)  # Adjust the timing as needed
    


# Set up the main application window
root = tk.Tk()
root.title("NewsApp")
root.configure(background='light green')
root.geometry("800x600")

# Style configuration
style = ttk.Style()
style.configure('TButton', padding=6, relief='flat', background='#4CAF50', font=("Calibri", 14), foreground='light blue')
style.configure('TLabel', background='#F5F5F5', font=("Arial", 16))
style.configure('TCombobox', padding=5)
style.configure('TFrame', background='#E0F2F1')
style.configure('TText', padding=5, background='#FFFFFF', foreground='#000000')
style.configure('TEntry', padding=5,
                relief='flat',  # You can use 'flat', 'raised', 'sunken', 'groove', or 'ridge'
                foreground='#000000',  # Text color
                background='#FFFFFF',  # Background color
                borderwidth=1)  # Border width

# Menu Screen
menu_frame = tk.Frame(root, bg='#E0F2F1')

welcome_label = tk.Label(menu_frame, text="Welcome to our NEWS App", font=("Arial", 20, 'bold'), bg='#F5F5F5')
welcome_label.pack(pady=20)

find_news_button = ttk.Button(menu_frame, text="Find the Latest News", command=show_news_screen)
find_news_button.pack(pady=10)

exit_button = ttk.Button(menu_frame, text="Exit", command=exit_program)
exit_button.pack(pady=10)

menu_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Load and display the GIF
gif_path = "C:/Users/gtak2/source/repos/PythonApplication/breakingnews.gif"  # Replace with the path to your GIF
gif = Image.open(gif_path)
gif_frames = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(gif)]

gif_label = tk.Label(menu_frame, bg='#E0F2F1')
gif_label.pack(pady=20)  # Position the GIF below the buttons

# Start GIF animation
update_gif(0)

menu_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


# News Screen
news_frame = tk.Frame(root, bg='#E0F2F1')

# Expanded Country options
country_options = [
    'us - United States', 
    'gb - United Kingdom', 
    'ca - Canada', 
    'au - Australia', 
    'de - Germany', 
    'fr - France', 
    'it - Italy', 
    'es - Spain', 
    'nl - Netherlands', 
    'ru - Russia', 
    'cn - China', 
    'jp - Japan', 
    'in - India', 
    'kr - South Korea', 
    'br - Brazil', 
    'za - South Africa',
    'gr - Greece'  
]
tk.Label(news_frame, text="Select Country:", background='#F5F5F5').grid(row=0, column=0, padx=10, pady=5, sticky='w')
country_var = tk.StringVar()
country_combobox = ttk.Combobox(news_frame, textvariable=country_var, values=country_options)
country_combobox.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
country_combobox.set('us')

# Expanded Category options
category_options = ['general', 'business', 'entertainment', 'health', 'science', 'sports', 'technology', 'politics', 'environment', 'world']
tk.Label(news_frame, text="Select Category:", background='#F5F5F5').grid(row=1, column=0, padx=10, pady=5, sticky='w')
category_var = tk.StringVar()
category_combobox = ttk.Combobox(news_frame, textvariable=category_var, values=category_options)
category_combobox.grid(row=1, column=1, padx=10, pady=5, sticky='ew')
category_combobox.set('general')

# Fetch news button
fetch_button = ttk.Button(news_frame, text="Fetch News", command=update_news)
fetch_button.grid(row=2, column=0, columnspan=2, pady=10)

# News display area
news_display = tk.Text(news_frame, height=15, width=80, wrap=tk.WORD, state=tk.DISABLED)
news_display.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

# Back to Menu button
back_button = ttk.Button(news_frame, text="Back to Menu", command=go_back_to_menu)
back_button.grid(row=4, column=0, columnspan=2, pady=10)

# Make sure the news_frame expands properly
news_frame.grid_rowconfigure(3, weight=1)
news_frame.grid_columnconfigure(1, weight=1)

see_button = ttk.Button(news_frame, text="See URL results", command=clear_screen)
see_button.grid(row=4, column=2, columnspan=2, pady=10)

# Create a url frame
url_frame = tk.Frame(root, bg='#E0F2F1', padx=10, pady=10)
url_frame.pack(expand=True, fill=tk.BOTH)

# Add the label
link_label = ttk.Label(url_frame, text="Enter URL:", style='TLabel')
link_label.place(relx=0.5, rely=0.4, anchor='center')

# Add the entry widget
link_entry = ttk.Entry(url_frame, width=50, style='TEntry')
link_entry.place(relx=0.5, rely=0.5, anchor='center')

# Add the submit button
submit_button = ttk.Button(url_frame, text="Submit", style='TButton', command=open_link_with_default_browser)
submit_button.place(relx=0.5, rely=0.6, anchor='center')

# Create the back button
back_button_two = ttk.Button(url_frame, text="Back", style='TButton',command=show_news_screen)
back_button_two.place(relx=0.02, rely=0.98, anchor='sw')

# Initialize the UI with menu_frame only
initialize_ui()


# Run the application
root.mainloop()


