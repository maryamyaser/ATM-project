from tkinter import *
from tkinter import messagebox
from accounts import Account , BankAccount , SavingsAccount , CurrentAccount
from tkinter import ttk, simpledialog
from datetime import date 

current_user = None
ACCOUNT_TYPES = {'Savings': SavingsAccount, 'Current': CurrentAccount}
ADMIN_PASSWORD = 'admin123'

BG = '#fff0f6'          
CARD = '#ffffff'        
PRIMARY = '#ec4899'     
PRIMARY_DARK = '#be185d'
SOFT = '#fbcfe8'        
TEXT = '#831843'       
FONT = ('Comic Sans MS', 15)
TITLE_FONT = ('Comic Sans MS', 28, 'bold')

def make_label(parent, text, title=False):
    return Label(parent, text=('♡ ' + text + ' ♡') if title else text,
                 bg=CARD, fg=PRIMARY if title else TEXT,
                 font=TITLE_FONT if title else FONT)

def make_entry(parent, show=None):
    return Entry(parent, font=FONT, show=show, width=24, justify='center',
                 relief='flat', bg='#fff7fb', fg=TEXT,
                 highlightthickness=2, highlightbackground=SOFT,
                 highlightcolor=PRIMARY, insertbackground=PRIMARY)

def make_button(parent, text, command, width=20):
    b = Button(parent, text=text, command=command, font=FONT,
               bg=PRIMARY, fg='white', relief='flat', cursor='hand2',
               activebackground=PRIMARY_DARK, activeforeground='white',
               width=width, pady=6)
    b.bind('<Enter>', lambda e: b.config(bg=PRIMARY_DARK))
    b.bind('<Leave>', lambda e: b.config(bg=PRIMARY))
    return b

def make_screen(window):
    outer = Frame(window, bg=BG)
    card = Frame(outer, bg=CARD, padx=50, pady=35,
                 highlightthickness=3, highlightbackground=SOFT)
    card.pack(expand=True)
    return outer, card

def show_frame(frame):
    for f in (login_frame, create_frame, menu_frame, transfer_frame, admin_frame):
        f.pack_forget()
    frame.pack(expand=True, fill='both')


def load_accounts():
    accounts = []
    try:
        with open('data.txt' , 'r') as f :
            for line in f :
                line = line.strip()
                if line =='':
                    continue
                parts = line.split()
                if len(parts) == 4:              
                    parts.append('Savings')
                account_number, name, password, balance, acc_type = parts
                accounts.append(ACCOUNT_TYPES[acc_type](account_number, name, password, balance))
    except FileNotFoundError :
        return []
    return accounts

def save_accounts(accounts):
    with open('data.txt' , 'w') as f :
        for acc in accounts :
            f.write(f'{acc.account_number} {acc.name} {acc.get_password()} {acc.get_balance()} {acc.account_type}\n')

def refresh_balance():
    amount_label.config(
        text=f'ACCOUNT NO. {current_user.account_number}\nBALANCE = {current_user.get_balance()}'
    )

def login():
    global current_user
    username = login_entry.get().strip()
    password = password_entry.get().strip()
    for acc in accounts :
        if username == acc.name and password == acc.get_password():
            current_user = acc
            refresh_balance()
            show_frame(menu_frame)

            return

    messagebox.showinfo('ERROR' , 'USERNAME OR PASSWORD ARE NOT ACCURATE')


def deposit():
    try:
        amount = int(amount_entry.get())
        if amount <= 0 :
            messagebox.showinfo('ERROR' , ' AMOUNT CAN NOT BE NEGATIVE NOR ZERO.')
            return
        current_user.deposit(amount)
        save_accounts(accounts)
        transaction(f'{current_user.name.upper()} DEPOSITED {amount} AT {date.today()} ')
        messagebox.showinfo('STATUS' , 'DEPOSIT SUCCESSFUL!')
        refresh_balance()
        amount_entry.delete(0,END)

    except:
        messagebox.showinfo('ERROR' , 'ENTER VALID NUMBER')
        amount_entry.delete(0,END)

def withdraw():
    try :
        amount = int(amount_entry.get())
        if amount <= 0 :
            messagebox.showinfo('ERROR' , ' AMOUNT CAN NOT BE NEGATIVE NOR ZERO.')
            return
        result = messagebox.askyesno('CONFIRM WITHDRAW' , ' ARE YOU SURE?')
        if not result :
            amount_entry.delete(0,END)
            return
        success = current_user.withdraw(amount)
        if success :
            save_accounts(accounts)
            transaction(f'{current_user.name.upper()} WITHDREW {amount} AT {date.today()} ')
            messagebox.showinfo('STATUS' , 'WITHDRAW SUCCESSFUL!')
            refresh_balance()
            amount_entry.delete(0,END)
        else:
            messagebox.showinfo(
                'ERROR',
                'BALANCE NOT ENOUGH'
            )

    except:
        messagebox.showinfo('ERROR' , 'ENTER VALID NUMBER')
        amount_entry.delete(0,END)

def transfer_money(): 
    show_frame(transfer_frame)

def trans_submit():
    target_user = target_entry.get().strip()
    target_account = None
    for acc in accounts :
        if target_user == acc.account_number :
            target_account = acc
            break
    if target_account == None :
        messagebox.showinfo('ERROR' , 'ACCOUNT NOT FOUND')
        target_entry.delete(0,END)
        transamount_entry.delete(0,END)
        return
    try :
        amount = int(transamount_entry.get())
    except :
        messagebox.showinfo('ERROR' , 'ENTER VALID NUMBER')
        transamount_entry.delete(0,END)
        return
    if amount <= 0 :
        messagebox.showinfo('ERROR' , ' AMOUNT CAN NOT BE NEGATIVE NOR ZERO.')
        return
    if target_account == current_user :
        messagebox.showinfo('ERROR' , ' CAN NOT TRANSFER TO YOUR OWN ACCOUNT.')
        return

    success = current_user.withdraw(amount)
    if success :
        target_account.deposit(amount)
        save_accounts(accounts)
        transaction(f'{current_user.name.upper()} TRANSFERED {amount} TO {target_account.name.upper()} AT {date.today()}')
        messagebox.showinfo('TRANSFER' , ' TRANSFER SUCCESSFUL!')
        target_entry.delete(0,END)
        transamount_entry.delete(0 ,END)
        refresh_balance()
        return
    messagebox.showinfo('ERROR' , ' BALANCE NOT ENOUGH')
def back():
    show_frame(menu_frame)


def show_history():
    with open('transaction.txt' , 'r') as f :
       lines = f.readlines()
    user_history = []
    for line in lines :
        if line.startswith(current_user.name.upper() + ' '):
            user_history.append(line)
    history_text = ''.join(user_history)
    if not user_history :
        history_text = ' NO TRANSACTIONS YET.'
    messagebox.showinfo('HISTORY' , history_text)
       

def logout():
    global current_user
    current_user = None
    login_entry.delete(0, END)
    password_entry.delete(0, END)
    show_frame(login_frame)

def create_account():
    login_entry.delete(0, END)
    password_entry.delete(0, END)
    show_frame(create_frame)

def submit():
    username = create_entry.get().strip()
    password = crepass_entry.get()
    if username == '' or password == '' or ' ' in username or ' ' in password:
        messagebox.showinfo("ERROR", 'USERNAME AND PASSWORD CAN NOT BE EMPTY OR CONTAIN SPACES.')
        return
    try:
        balance = int(balance_entry.get())
    except :
        messagebox.showinfo("ERROR" , 'ENTER VALID NUMBER .')
        return
    for acc in accounts :
        if username == acc.name :
            messagebox.showinfo("ERROR" , 'ACCOUNT ALREADY EXISTS.')
            return
    account_number = max([int(a.account_number) for a in accounts], default=0) + 1
    accounts.append(ACCOUNT_TYPES[type_combo.get()](account_number, username, password, balance))
    save_accounts(accounts)
    messagebox.showinfo("STATUS" , 'ACCOUNT CREATED SUCCESSFULY.')
    create_entry.delete(0,END)
    crepass_entry.delete(0,END)
    balance_entry.delete(0,END)
    show_frame(login_frame)
def create_back():
    show_frame(login_frame)

def open_admin():
    pw = simpledialog.askstring('ADMIN', 'Enter admin password:', show='*')
    if pw != ADMIN_PASSWORD:
        if pw is not None:
            messagebox.showinfo('ERROR', 'WRONG PASSWORD')
        return
    refresh_table()
    show_frame(admin_frame)

def refresh_table(items=None):
    tree.delete(*tree.get_children())
    for acc in (accounts if items is None else items):
        tree.insert('', END, values=(acc.account_number, acc.name,
                                     acc.account_type, acc.get_balance()))

def search_accounts():
    word = search_entry.get().strip().lower()
    refresh_table([a for a in accounts
                   if word in a.name.lower() or word in a.account_number])

def selected_account():
    sel = tree.selection()
    if not sel:
        messagebox.showinfo('ERROR', 'SELECT AN ACCOUNT FIRST')
        return None
    number = str(tree.item(sel[0])['values'][0])
    for acc in accounts:
        if acc.account_number == number:
            return acc

def edit_account():
    acc = selected_account()
    if acc is None:
        return
    new_name = simpledialog.askstring('EDIT', 'New name:', initialvalue=acc.name)
    if new_name is None:
        return
    new_name = new_name.strip()
    if new_name == '' or ' ' in new_name:
        messagebox.showinfo('ERROR', 'INVALID NAME')
        return
    for other in accounts:
        if other is not acc and other.name == new_name:
            messagebox.showinfo('ERROR', 'NAME ALREADY EXISTS')
            return
    new_pass = simpledialog.askstring('EDIT', 'New password (leave empty to keep):', show='*')
    acc.set_name(new_name)
    if new_pass and ' ' not in new_pass:
        acc.set_password(new_pass)
    save_accounts(accounts)
    refresh_table()

def delete_account():
    acc = selected_account()
    if acc is None:
        return
    if messagebox.askyesno('CONFIRM', f'Delete account {acc.name}?'):
        accounts.remove(acc)
        save_accounts(accounts)
        refresh_table()

def admin_back():
    show_frame(login_frame)

def transaction(text):
    with open ('transaction.txt' , 'a' ) as f :
        f.write(text + '\n' )

accounts = load_accounts()
window = Tk()
window.title("ATM SYSTEM")
window.geometry('750x700')
window.configure(bg=BG)

login_frame, login_card = make_screen(window)
create_frame, create_card = make_screen(window)
menu_frame, menu_card = make_screen(window)
transfer_frame, transfer_card = make_screen(window)

# ---------- Login ----------
make_label(login_card, 'ATM SYSTEM', title=True).pack(pady=(0, 25))
login_label = make_label(login_card, 'Username')
login_entry = make_entry(login_card)     
password_label = make_label(login_card, 'Password')
password_entry = make_entry(login_card, show='*')
login_button = make_button(login_card, 'LOGIN', login)
create_button = make_button(login_card, 'CREATE ACCOUNT', create_account)
login_label.pack(); login_entry.pack(pady=(0, 10))
password_label.pack(); password_entry.pack(pady=(0, 20))
login_button.pack(pady=5)
create_button.pack(pady=5)
admin_button = make_button(login_card, 'ADMIN', open_admin)
admin_button.pack(pady=5)

# ---------- Create account ----------
make_label(create_card, 'NEW ACCOUNT', title=True).pack(pady=(0, 25))
create_label = make_label(create_card, 'Username')
create_entry = make_entry(create_card)
crepass_label = make_label(create_card, 'Password')
crepass_entry = make_entry(create_card, show='*')
balance_label = make_label(create_card, 'Starting balance')
balance_entry = make_entry(create_card)
submitcreate_button = make_button(create_card, 'CREATE', submit)
createback_button = make_button(create_card, 'BACK', create_back)
create_label.pack(); create_entry.pack(pady=(0, 10))
crepass_label.pack(); crepass_entry.pack(pady=(0, 10))
balance_label.pack(); balance_entry.pack(pady=(0, 20))
type_label = make_label(create_card, 'Account type')
type_combo = ttk.Combobox(create_card, values=['Savings', 'Current'],
                          state='readonly', font=FONT, width=22, justify='center')
type_combo.set('Savings')
type_label.pack()
type_combo.pack(pady=(0, 20))
submitcreate_button.pack(pady=5)
createback_button.pack(pady=5)

# ---------- Menu (after login) ----------
amount_label = Label(menu_card, text='ACCOUNT BALANCE', bg=CARD, fg=PRIMARY,
                     font=('Comic Sans MS', 20, 'bold'))
amount_entry = make_entry(menu_card)
deposit_button = make_button(menu_card, 'DEPOSIT', deposit)
withdraw_button = make_button(menu_card, 'WITHDRAW', withdraw)
transfer_button = make_button(menu_card, 'TRANSFER MONEY', transfer_money)
show_button = make_button(menu_card, 'SHOW HISTORY', show_history)
logout_button = make_button(menu_card, 'LOGOUT', logout)
amount_label.pack(pady=(0, 20))
make_label(menu_card, 'Amount').pack()
amount_entry.pack(pady=(0, 20))
for b in (deposit_button, withdraw_button, transfer_button, show_button, logout_button):
    b.pack(pady=5)

# ---------- Transfer ----------
make_label(transfer_card, 'TRANSFER', title=True).pack(pady=(0, 25))
target_label = make_label(transfer_card, 'Target account number')
target_entry = make_entry(transfer_card)
transamount_label = make_label(transfer_card, 'Amount')
transamount_entry = make_entry(transfer_card)
submittrans_button = make_button(transfer_card, 'SUBMIT TRANSFER', trans_submit)
back_button = make_button(transfer_card, 'BACK', back)
target_label.pack(); target_entry.pack(pady=(0, 10))
transamount_label.pack(); transamount_entry.pack(pady=(0, 20))
submittrans_button.pack(pady=5)
back_button.pack(pady=5)

# ---------- Admin ----------
admin_frame, admin_card = make_screen(window)
make_label(admin_card, 'ADMIN', title=True).pack(pady=(0, 15))
search_entry = make_entry(admin_card)
search_entry.pack(pady=5)
make_button(admin_card, 'SEARCH', search_accounts).pack(pady=5)

columns = ('No', 'Name', 'Type', 'Balance')
tree = ttk.Treeview(admin_card, columns=columns, show='headings', height=8)
for c in columns:
    tree.heading(c, text=c)
    tree.column(c, width=100, anchor='center')
tree.pack(pady=10)

btn_row = Frame(admin_card, bg=CARD)
btn_row.pack()
make_button(btn_row, 'EDIT', edit_account, width=8).pack(side=LEFT, padx=4)
make_button(btn_row, 'DELETE', delete_account, width=8).pack(side=LEFT, padx=4)
make_button(btn_row, 'ALL', refresh_table, width=8).pack(side=LEFT, padx=4)
make_button(btn_row, 'BACK', admin_back, width=8).pack(side=LEFT, padx=4)

show_frame(login_frame)

window.mainloop()