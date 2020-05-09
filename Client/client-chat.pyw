from socket import AF_INET, socket, SOCK_STREAM, SHUT_RDWR  # Handles server connections
import tkinter as tk  # Handles GUI
import tkinter.font as tkfont  # Handles GUI fonts
from threading import Thread  # Handles multi-threading
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hashlib

HOST = '86.149.111.103'
PORT = 12345
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)




def receive():  # Handles receiving of messages
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")  # Receives and decodes message
            message = Fernet(app.key).decrypt(msg.encode()).decode()
            online = message.split("@#%")[1].split(", ")
            app.online_box.configure(state='normal')  # Makes the text editable
            app.online_box.delete(1.0, tk.END)
            for user in online:
                app.online_box.insert(tk.END, (" - " + user + "\n"))
            app.online_box.configure(state='disabled')  # Locks the text
            message = message.split("@#%")[0]
            app.msg_box.configure(state='normal')  # Makes the text editable
            app.msg_box.insert(tk.END, (message + "\n"))  # Adds it to the chat box
            app.msg_box.configure(state='disabled')  # Locks the text
            app.msg_box.yview_moveto(1)
        except OSError:   # Possibly client has left the chat.
            break


def send(event=None):   # Handles sending of messages
    msg = app.my_msg.get()  # Because it is a tkinter string var
    if app.name == "":
        app.name = msg
        client_socket.connect(app.ADDR)  # Creates initial connection
        receive_thread = Thread(target=receive)  # Creates separate thread for receiving messages
        receive_thread.start()  # Starts thread
    if msg != "":
        app.my_msg.set("")   # Clears input field
        message = Fernet(app.key).encrypt(msg.encode())
        client_socket.send(message)  # Sends new message to server
        if msg == "%quit%":
            client_socket.shutdown(SHUT_RDWR)  # Clear socket
            client_socket.close()  # Close server connection
            root.destroy()  # Clear all elements from window
            root.quit()  # Close window


def on_exit(event=None):
    if app.name != "":
        app.my_msg.set("%quit%")  # Set message box to quit command
        send()  # Run send function
    else:
        root.destroy()  # Clear all elements from window
        root.quit()  # Close window




class MainWindow:
    def __init__(self, master):
        self.master = master  # Base window for GUI
        
        self.customFontA = tkfont.Font(family="Arial Light", size=14)  # Custom fonts
        self.customFontB = tkfont.Font(family="Arial", size=12, weight="bold")
        self.customFontC = tkfont.Font(family="Arial", size=16)
        self.customFontD = tkfont.Font(family="Courier", size=40)
        self.customFontE = tkfont.Font(family="Courier", size=25)

        self.name = ""
        self.my_msg = tk.StringVar()

        self.chatFrame = tk.Frame(self.master, height=550, width=400, bg='#ffffff')  # Frame for chat
        self.sendFrame = tk.Frame(self.master, bg='#ffffff')  # Frame for message box
        self.onlineFrame = tk.Frame(self.master, width=350, bg='#ffffff')  # Frame for people online

        self.online_box = tk.Text(self.onlineFrame, wrap=tk.WORD, bg="#505a66", fg="#ffffff", bd=0,
                                  font=self.customFontA, state='disabled', padx=8, pady=6, spacing3=3, width=27,
                                  height=8)

        self.password()

    def checkPassword(self, event=None):
        password = self.passInput.get()
        hashedPassword = hashlib.sha256(password.encode()).digest()
        hash = b'\x02\xf5\x14\x82\xf5r\xa4p\xb4;\xb2j\xe9y\x15\x95\x8b\x9f,(\xbe\xfa\xcc\xa9+\xd2A|6i4!'
        if hashedPassword == hash:
            self.passFrame.grid_forget()
            salt = b'\x15\x95\xd1{/\xec\x99\xac\x90\x99>\xa5\nw\xfb\xe3'
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            self.key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            self.ip()
        else:
            self.passInput.set("")

    def password(self):
        self.passFrame = tk.Frame(self.master, bg='#ffffff', height=550, width=750)  # Frame for message box
        self.passFrame.grid(column=0, row=0, rowspan=1, sticky='NSEW')
        self.passFrame.grid_propagate(0)

        self.passInput = tk.StringVar()

        self.pass_entry_field = tk.Entry(self.passFrame, width=35, font=self.customFontC, textvariable=self.passInput,
                                         bg="#a1afb8", fg="#505a66", relief="flat", show="\u2022")  # Entry box for new messages
        self.pass_entry_field.bind("<Return>", self.checkPassword)
        self.pass_entry_field.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.pass_entry_field.focus()

        self.pass_button = tk.Button(self.passFrame, text="Check", command=self.checkPassword, bg='#505a66', fg='#ffffff',
                                     activebackground='#3c4652', activeforeground='#d9d9d9', width=10,
                                     font=self.customFontB, bd=0)  # Send button
        self.pass_button.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

        self.passTitle = tk.Label(self.passFrame, text="Password:", bg='#ffffff', fg='#4b5059', font=self.customFontD)
        self.passTitle.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

    def setIP(self, event=None):
        ip = self.ipInput.get()
        if ip.count('.') == 3:
            self.ADDR = (ip, PORT)
            fileip = open("ip.txt", "w+")
            self.ipInput.set(fileip.write(ip))
            fileip.close()
            self.ipFrame.grid_forget()
            self.username()
        else:
            self.ipInput.set("")

    def ip(self):
        self.ipFrame = tk.Frame(self.master, bg='#ffffff', height=550, width=750)  # Frame for message box
        self.ipFrame.grid(column=0, row=0, rowspan=1, sticky='NSEW')
        self.ipFrame.grid_propagate(0)

        self.ipInput = tk.StringVar()
        try:
            fileip = open("ip.txt", "x")
            fileip.close()
        except:
            fileip = open("ip.txt", "r+")
            self.ipInput.set(fileip.read())
            fileip.close()

        self.ip_entry_field = tk.Entry(self.ipFrame, width=35, font=self.customFontC, textvariable=self.ipInput,
                                         bg="#a1afb8", fg="#505a66", relief="flat")  # Entry box for new messages
        self.ip_entry_field.bind("<Return>", self.setIP)
        self.ip_entry_field.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.ip_entry_field.focus()
        self.ip_entry_field.icursor(tk.END)

        self.ip_button = tk.Button(self.ipFrame, text="Set", command=self.setIP, bg='#505a66', fg='#ffffff',
                                     activebackground='#3c4652', activeforeground='#d9d9d9', width=10,
                                     font=self.customFontB, bd=0)  # Send button
        self.ip_button.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

        self.ipTitle = tk.Label(self.ipFrame, text="Host IP:", bg='#ffffff', fg='#4b5059', font=self.customFontD)
        self.ipTitle.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

    def sendusername(self, event=None):
        send()
        self.nameFrame.grid_forget()
        self.main()

    def username(self):
        self.nameFrame = tk.Frame(self.master, bg='#ffffff', height=550, width=750)  # Frame for message box
        self.nameFrame.grid(column=0, row=0, rowspan=1, sticky='NSEW')
        self.nameFrame.grid_propagate(0)

        self.nameInput = tk.StringVar()

        self.name_entry_field = tk.Entry(self.nameFrame, width=35, font=self.customFontC, textvariable=self.my_msg,
                                         bg="#a1afb8", fg="#505a66", relief="flat")  # Entry box for new messages
        self.name_entry_field.bind("<Return>", self.sendusername)
        self.name_entry_field.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.name_entry_field.focus()

        self.name_button = tk.Button(self.nameFrame, text="Submit", command=self.sendusername, bg='#505a66', fg='#ffffff',
                                     activebackground='#3c4652', activeforeground='#d9d9d9', width=10,
                                     font=self.customFontB, bd=0)  # Send button
        self.name_button.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

        self.nameTitle = tk.Label(self.nameFrame, text="Name:", bg='#ffffff', fg='#4b5059', font=self.customFontD)
        self.nameTitle.place(relx=0.5, rely=0.35, anchor=tk.CENTER)

    def main(self):
        self.master.protocol("WM_DELETE_WINDOW", on_exit)


        self.chatFrame.grid(column=1, row=0, rowspan=2, sticky='NSEW')
        self.chatFrame.pack_propagate(0)

        self.onlineFrame.grid(column=0, row=0, rowspan=1, sticky='NSEW')
        self.onlineFrame.grid_propagate(0)

        self.sendFrame.grid(column=0, row=1, rowspan=1, sticky='NSEW')
        self.sendFrame.grid_propagate(0)

        self.my_msg.set("")  # Default text for entry field

        self.scrollbar = tk.Scrollbar(self.chatFrame)  # Scrollbar for chat box
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.msg_box = tk.Text(self.chatFrame, yscrollcommand=self.scrollbar.set, wrap=tk.WORD, bg="#505a66", fg="#ffffff", bd=0, font=self.customFontA, state='disabled', padx=8, pady=6, spacing3=3)  # Chat box
        self.msg_box.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.entry_field = tk.Entry(self.sendFrame, textvariable=self.my_msg, width=27,
                                    font=self.customFontC,
                                         bg="#a1afb8", fg="#505a66", relief="flat")  # Entry box for new messages
        self.entry_field.bind("<Return>", send)
        self.entry_field.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.entry_field.focus()

        self.send_button = tk.Button(self.sendFrame, text="Send", command=send, bg='#505a66', fg='#ffffff',
                                     activebackground='#3c4652', activeforeground='#d9d9d9', width=10,
                                     font=self.customFontB, bd=0)  # Send button
        self.send_button.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

        self.onlineTitle = tk.Label(self.onlineFrame, text="Online:", bg='#ffffff', fg='#4b5059', font=self.customFontE)
        self.onlineTitle.place(relx=0.25, rely=0.1, anchor=tk.CENTER)


        self.online_box.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

if __name__ == '__main__':
    root = tk.Tk()  # Initialises tKinter
    root.title("CryptoBabble")  # Gives window a title
    root.geometry('750x550')  # Sets window dimensions
    root.configure(bg='#ffffff')
    root.resizable(width=False, height=False)  # Makes window not resizable
    root.iconbitmap('logo.ico')

    app = MainWindow(root)

    root.mainloop()  # Starts GUI
