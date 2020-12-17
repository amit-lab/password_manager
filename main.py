from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letters_lst = [choice(letters) for _ in range(randint(8, 10))]
    symbols_lst = [choice(symbols) for _ in range(randint(2, 4))]
    numbers_lst = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = letters_lst + symbols_lst + numbers_lst
    shuffle(password_list)

    password = ''.join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)  # copy to clipboard


# ---------------------------- SAVE PASSWORD ------------------------------- #

def insert_data():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning(title="Warning", message="Some of the fields are empty")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \n"
                                                              f"Email: {email} \nPassword: {password} \n"
                                                              f"Is it ok?")

        if is_ok:
            try:
                with open("data.json") as data_file:
                    # Reading old data
                    data = json.load(data_file)

            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    # Saving data in json form
                    json.dump(new_data, data_file, indent=4)

            else:
                # Update old data with new data
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    # Saving data in json form
                    json.dump(data, data_file, indent=4)

            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ----------------------------  Search  ------------------------------- #
def search_entry():
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        pass
    else:
        website = website_entry.get()
        if len(website) == 0:
            return
        elif website in data:
            messagebox.showinfo(title=website, message=f"email: {data[website]['email']}\n"
                                                       f"password: {data[website]['password']}")
        else:
            messagebox.showerror(title="error", message=f"There is no email and password is saved for '{website}'")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
window.resizable(0, 0)

# logo image
logo_img = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200, highlightthickness=0)
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# labels
website_label = Label(text="Website:")
email_label = Label(text="Email/Username:")
password_label = Label(text="Password:")
website_label.grid(column=0, row=1)
email_label.grid(column=0, row=2)
password_label.grid(column=0, row=3)

# Buttons
generate_pass_btn = Button(text="Generate", command=generate_password)
generate_pass_btn.grid(column=2, row=3)
add_btn = Button(text="Add", width=35, command=insert_data)
add_btn.grid(column=1, row=4, columnspan=2)
search_btn = Button(text="Search", command=search_entry)
search_btn.grid(column=2, row=1)

# Entries
website_entry = Entry(width=23)
email_entry = Entry(width=35)
email_entry.insert(0, "amitdongarwar1810@gmail.com")
password_entry = Entry(width=23)
website_entry.grid(column=1, row=1)
email_entry.grid(column=1, row=2, columnspan=3)
password_entry.grid(column=1, row=3)

window.mainloop()
