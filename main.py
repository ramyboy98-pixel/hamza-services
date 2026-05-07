import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
import sys
import shutil
import json


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


APP_DATA_DIR = os.path.join(os.path.expanduser("~"), "HamzaServices")
SETTINGS_FILE = os.path.join(APP_DATA_DIR, "settings.json")
CUSTOM_BACKGROUND = os.path.join(APP_DATA_DIR, "background.jpg")

DEFAULT_SETTINGS = {
    "username": "admin",
    "password": "1234",
    "background": ""
}

os.makedirs(APP_DATA_DIR, exist_ok=True)


def save_settings(data):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        for key, value in DEFAULT_SETTINGS.items():
            data.setdefault(key, value)

        return data
    except:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()


settings = load_settings()

root = tk.Tk()
root.title("HAMZA SERVICES")
root.geometry("1280x720")
root.minsize(1000, 600)
root.configure(bg="black")

canvas = tk.Canvas(root, highlightthickness=0, bd=0)
canvas.pack(fill="both", expand=True)

background_photo = None
login_photo = None
normal_icons = {}
large_icons = {}
current_page = "login"
entry_widgets = []


def clear_entries():
    global entry_widgets
    for widget in entry_widgets:
        try:
            widget.destroy()
        except:
            pass
    entry_widgets = []


def load_icon(path, size):
    image = Image.open(resource_path(path)).convert("RGBA")
    image = image.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(image)


def get_background_path():
    if settings.get("background") and os.path.exists(settings["background"]):
        return settings["background"]
    return resource_path("assets/background.jpg")


def draw_background(width, height):
    global background_photo

    bg = Image.open(get_background_path()).convert("RGB")
    bg = bg.resize((width, height), Image.LANCZOS)

    dark_layer = Image.new("RGBA", (width, height), (0, 0, 0, 170))
    bg = bg.convert("RGBA")
    bg.alpha_composite(dark_layer)

    background_photo = ImageTk.PhotoImage(bg)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")


def draw_login_background(width, height):
    global login_photo

    path = resource_path("assets/login_background.jpg")

    if not os.path.exists(path):
        path = resource_path("assets/background.jpg")

    bg = Image.open(path).convert("RGB")
    bg = bg.resize((width, height), Image.LANCZOS)

    dark_layer = Image.new("RGBA", (width, height), (0, 0, 0, 85))
    bg = bg.convert("RGBA")
    bg.alpha_composite(dark_layer)

    login_photo = ImageTk.PhotoImage(bg)
    canvas.create_image(0, 0, image=login_photo, anchor="nw")


def change_background():
    file_path = filedialog.askopenfilename(
        title="اختر صورة خلفية",
        filetypes=[("Images", "*.png *.jpg *.jpeg")]
    )

    if not file_path:
        return

    shutil.copy(file_path, CUSTOM_BACKGROUND)
    settings["background"] = CUSTOM_BACKGROUND
    save_settings(settings)
    show_customize()


def draw_top_back(title, back_command):
    width = root.winfo_width()

    canvas.create_text(
        35, 28,
        text="HAMZA SERVICES",
        fill="#eeeeee",
        font=("Arial", 14, "bold"),
        anchor="w"
    )

    back_box = canvas.create_rectangle(
        35, 60, 125, 105,
        fill="#242428",
        outline="#34343a",
        width=1
    )

    back_text = canvas.create_text(
        80, 82,
        text="←  رجوع",
        fill="white",
        font=("Arial", 16, "bold")
    )

    canvas.create_text(
        width // 2,
        82,
        text=title,
        fill="white",
        font=("Arial", 38, "bold")
    )

    def enter(event):
        canvas.itemconfig(back_box, fill="#303036")
        root.config(cursor="hand2")

    def leave(event):
        canvas.itemconfig(back_box, fill="#242428")
        root.config(cursor="")

    def click(event):
        back_command()

    for item in (back_box, back_text):
        canvas.tag_bind(item, "<Enter>", enter)
        canvas.tag_bind(item, "<Leave>", leave)
        canvas.tag_bind(item, "<Button-1>", click)


def draw_list(items, on_click_func):
    width = root.winfo_width()

    list_x1 = int(width * 0.10)
    list_x2 = int(width * 0.90)
    start_y = 130
    row_h = 74
    gap = 8

    for i, (symbol, color, title, desc, key) in enumerate(items):
        y1 = start_y + i * (row_h + gap)
        y2 = y1 + row_h

        card = canvas.create_rectangle(
            list_x1, y1, list_x2, y2,
            fill="#202024",
            outline="#34343a",
            width=1
        )

        icon_bg = canvas.create_rectangle(
            list_x1 + 28, y1 + 12,
            list_x1 + 78, y1 + 62,
            fill=color,
            outline=color
        )

        icon_text = canvas.create_text(
            list_x1 + 53,
            y1 + 37,
            text=symbol,
            fill="white",
            font=("Arial", 23, "bold")
        )

        title_text = canvas.create_text(
            list_x1 + 115,
            y1 + 25,
            text=title,
            fill="white",
            font=("Arial", 19, "bold"),
            anchor="w"
        )

        desc_text = canvas.create_text(
            list_x1 + 115,
            y1 + 52,
            text=desc,
            fill="#bdbdbd",
            font=("Arial", 12),
            anchor="w"
        )

        arrow = canvas.create_text(
            list_x2 - 38,
            y1 + 37,
            text="›",
            fill="#cfcfcf",
            font=("Arial", 42, "bold")
        )

        def on_enter(event, c=card):
            canvas.itemconfig(c, fill="#29292f")
            root.config(cursor="hand2")

        def on_leave(event, c=card):
            canvas.itemconfig(c, fill="#202024")
            root.config(cursor="")

        def click(event, k=key):
            on_click_func(k)

        for item in (card, icon_bg, icon_text, title_text, desc_text, arrow):
            canvas.tag_bind(item, "<Enter>", on_enter)
            canvas.tag_bind(item, "<Leave>", on_leave)
            canvas.tag_bind(item, "<Button-1>", click)


def show_login():
    global current_page
    clear_entries()
    current_page = "login"
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_login_background(width, height)

    center_x = width // 2

    canvas.create_text(
        center_x,
        int(height * 0.19),
        text="Hamza services",
        fill="black",
        font=("Segoe Script", 58, "bold")
    )

    canvas.create_text(
        center_x,
        int(height * 0.30),
        text="user name",
        fill="white",
        font=("Courier New", 25, "bold")
    )

    username_entry = tk.Entry(
        root,
        font=("Courier New", 26, "bold"),
        justify="center",
        bd=0,
        bg="#ffa51f",
        fg="black",
        insertbackground="black"
    )

    username_entry.insert(0, settings.get("username", "admin"))

    canvas.create_window(
        center_x,
        int(height * 0.37),
        window=username_entry,
        width=360,
        height=48
    )

    canvas.create_text(
        center_x,
        int(height * 0.45),
        text="password",
        fill="white",
        font=("Courier New", 25, "bold")
    )

    password_entry = tk.Entry(
        root,
        font=("Courier New", 26, "bold"),
        justify="center",
        show="*",
        bd=0,
        bg="#ffa51f",
        fg="black",
        insertbackground="black"
    )

    canvas.create_window(
        center_x,
        int(height * 0.52),
        window=password_entry,
        width=360,
        height=48
    )

    entry_widgets.extend([username_entry, password_entry])

    login_btn = canvas.create_rectangle(
        center_x - 170,
        int(height * 0.64),
        center_x + 170,
        int(height * 0.64) + 62,
        fill="#ffa51f",
        outline="#ff8a00",
        width=3
    )

    login_text = canvas.create_text(
        center_x,
        int(height * 0.64) + 31,
        text="LOGIN",
        fill="black",
        font=("Courier New", 27, "bold")
    )

    error_text = canvas.create_text(
        center_x,
        int(height * 0.75),
        text="",
        fill="#ff4b4b",
        font=("Arial", 16, "bold")
    )

    forgot_text = canvas.create_text(
        center_x,
        int(height * 0.81),
        text="نسيت كلمة السر؟",
        fill="#ffffff",
        font=("Arial", 17, "bold")
    )

    canvas.create_line(
        int(width * 0.18),
        int(height * 0.88),
        int(width * 0.82),
        int(height * 0.88),
        fill="#777777"
    )

    canvas.create_text(
        center_x,
        int(height * 0.94),
        text="🔒 الرجاء إدخال اسم المستخدم وكلمة المرور للدخول",
        fill="white",
        font=("Arial", 18, "bold")
    )

    def login_enter(event):
        canvas.itemconfig(login_btn, fill="#ffb640")
        root.config(cursor="hand2")

    def login_leave(event):
        canvas.itemconfig(login_btn, fill="#ffa51f")
        root.config(cursor="")

    def do_login(event=None):
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if username == settings.get("username") and password == settings.get("password"):
            show_home()
        else:
            canvas.itemconfig(error_text, text="اسم المستخدم أو كلمة المرور غير صحيحة")

    def forgot_enter(event):
        canvas.itemconfig(forgot_text, fill="#ffa51f")
        root.config(cursor="hand2")

    def forgot_leave(event):
        canvas.itemconfig(forgot_text, fill="#ffffff")
        root.config(cursor="")

    def forgot_click(event):
        show_forgot_password()

    for item in (login_btn, login_text):
        canvas.tag_bind(item, "<Enter>", login_enter)
        canvas.tag_bind(item, "<Leave>", login_leave)
        canvas.tag_bind(item, "<Button-1>", do_login)

    canvas.tag_bind(forgot_text, "<Enter>", forgot_enter)
    canvas.tag_bind(forgot_text, "<Leave>", forgot_leave)
    canvas.tag_bind(forgot_text, "<Button-1>", forgot_click)

    username_entry.bind("<Return>", do_login)
    password_entry.bind("<Return>", do_login)


def show_forgot_password():
    global current_page
    clear_entries()
    current_page = "forgot"
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()

    draw_login_background(width, height)

    canvas.create_text(
        width // 2,
        120,
        text="استرجاع كلمة السر",
        fill="white",
        font=("Arial", 40, "bold")
    )

    canvas.create_text(
        width // 2,
        260,
        text="بيانات الدخول الافتراضية عند إعادة الضبط:",
        fill="white",
        font=("Arial", 22, "bold")
    )

    canvas.create_text(
        width // 2,
        320,
        text="اسم المستخدم: admin",
        fill="#dddddd",
        font=("Arial", 20)
    )

    canvas.create_text(
        width // 2,
        365,
        text="كلمة المرور: 1234",
        fill="#dddddd",
        font=("Arial", 20)
    )

    reset_btn = canvas.create_rectangle(
        width // 2 - 170,
        440,
        width // 2 + 170,
        500,
        fill="#ffa51f",
        outline="#ff8a00",
        width=3
    )

    reset_text = canvas.create_text(
        width // 2,
        470,
        text="إعادة ضبط الدخول",
        fill="black",
        font=("Arial", 20, "bold")
    )

    def reset_enter(event):
        canvas.itemconfig(reset_btn, fill="#ffb640")
        root.config(cursor="hand2")

    def reset_leave(event):
        canvas.itemconfig(reset_btn, fill="#ffa51f")
        root.config(cursor="")

    def reset_click(event):
        settings["username"] = "admin"
        settings["password"] = "1234"
        save_settings(settings)
        messagebox.showinfo("تم", "تمت إعادة ضبط بيانات الدخول.")
        show_login()

    for item in (reset_btn, reset_text):
        canvas.tag_bind(item, "<Enter>", reset_enter)
        canvas.tag_bind(item, "<Leave>", reset_leave)
        canvas.tag_bind(item, "<Button-1>", reset_click)

    draw_back_button(show_login)


def show_home():
    global current_page, normal_icons, large_icons
    clear_entries()
    current_page = "home"
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_background(width, height)

    canvas.create_text(
        width // 2,
        int(height * 0.12),
        text="HAMZA SERVICES",
        fill="#f2f2f2",
        font=("Arial", 52, "bold")
    )

    normal_icons = {
        "documents": load_icon("assets/documents.png", (145, 145)),
        "electronic": load_icon("assets/electronic.png", (145, 145)),
        "archive": load_icon("assets/archive.png", (145, 145)),
        "settings": load_icon("assets/settings.png", (145, 145)),
    }

    large_icons = {
        "documents": load_icon("assets/documents.png", (160, 160)),
        "electronic": load_icon("assets/electronic.png", (160, 160)),
        "archive": load_icon("assets/archive.png", (160, 160)),
        "settings": load_icon("assets/settings.png", (160, 160)),
    }

    items = [
        ("documents", "وثائق"),
        ("electronic", "خدمات\nإلكترونية"),
        ("archive", "أرشيف"),
        ("settings", "إعدادات"),
    ]

    positions = [width * 0.20, width * 0.40, width * 0.60, width * 0.80]
    icon_y = height * 0.43
    text_y = height * 0.64

    for index, (key, label) in enumerate(items):
        x = positions[index]

        image_id = canvas.create_image(x, icon_y, image=normal_icons[key], anchor="center")

        text_id = canvas.create_text(
            x,
            text_y,
            text=label,
            fill="#f2f2f2",
            font=("Arial", 32, "bold"),
            justify="center"
        )

        def on_enter(event, k=key, img=image_id):
            canvas.itemconfig(img, image=large_icons[k])
            root.config(cursor="hand2")

        def on_leave(event, k=key, img=image_id):
            canvas.itemconfig(img, image=normal_icons[k])
            root.config(cursor="")

        def on_click(event, k=key):
            if k == "settings":
                show_settings()
            else:
                show_placeholder(k)

        for item in (image_id, text_id):
            canvas.tag_bind(item, "<Enter>", on_enter)
            canvas.tag_bind(item, "<Leave>", on_leave)
            canvas.tag_bind(item, "<Button-1>", on_click)


def show_settings():
    global current_page
    clear_entries()
    current_page = "settings"
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()

    draw_background(width, height)
    draw_top_back("الإعدادات", show_home)

    settings_items = [
        ("🔐", "#2f7df6", "الحساب والأمان", "تغيير اسم المستخدم وكلمة المرور وإعدادات الأمان", "account"),
        ("🎨", "#8d3ff2", "تخصيص الواجهة", "تغيير الخلفية والألوان والخطوط والمظهر العام", "customize"),
        ("🖨", "#55b72c", "الطباعة", "إعدادات الطابعة ومعاينة قبل الطباعة", "printer"),
        ("📄", "#ff8a18", "إدارة الوثائق", "إعدادات حفظ الوثائق والقوالب والتنسيقات", "documents_settings"),
        ("🛡", "#25b7b1", "النسخ الاحتياطي والحماية", "النسخ الاحتياطي واسترجاع البيانات وإعدادات الحماية", "backup"),
        ("👥", "#e03c78", "قاعدة بيانات الزبائن", "إعدادات قاعدة البيانات والبحث والتصدير والاستيراد", "clients_db"),
        ("⚡", "#ffcf00", "الذكاء والسرعة", "الخيارات الذكية والاختصارات والاقتراحات", "smart"),
        ("ℹ", "#2da7ff", "معلومات البرنامج", "معلومات الإصدار والتحديثات والمطور", "info"),
    ]

    def click_setting(k):
        if k == "customize":
            show_customize()
        elif k == "account":
            show_account_security()
        else:
            show_setting_placeholder(k)

    draw_list(settings_items, click_setting)


def show_account_security():
    global current_page
    clear_entries()
    current_page = "account"
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()

    draw_background(width, height)
    draw_top_back("الحساب والأمان", show_settings)

    account_items = [
        ("👤", "#2f7df6", "تغيير اسم المستخدم", "تعديل اسم المستخدم الذي تستعمله للدخول إلى البرنامج", "change_username"),
        ("🔑", "#8d3ff2", "تغيير كلمة المرور", "تحديث كلمة مرور الدخول وحماية البرنامج", "change_password"),
        ("🔒", "#55b72c", "قفل البرنامج", "إغلاق الوصول إلى البرنامج حتى يتم إدخال كلمة المرور", "lock_app"),
        ("♻", "#ff8a18", "إعادة ضبط بيانات الدخول", "إرجاع اسم المستخدم وكلمة المرور إلى القيم الافتراضية", "reset_login"),
    ]

    draw_list(account_items, lambda k: show_account_form(k))


def draw_save_button(text, y, command):
    width = root.winfo_width()

    btn = canvas.create_rectangle(
        width // 2 - 130,
        y,
        width // 2 + 130,
        y + 55,
        fill="#2f7df6",
        outline="#2f7df6"
    )

    txt = canvas.create_text(
        width // 2,
        y + 28,
        text=text,
        fill="white",
        font=("Arial", 18, "bold")
    )

    def enter(event):
        canvas.itemconfig(btn, fill="#4b91ff")
        canvas.itemconfig(btn, outline="#4b91ff")
        root.config(cursor="hand2")

    def leave(event):
        canvas.itemconfig(btn, fill="#2f7df6")
        canvas.itemconfig(btn, outline="#2f7df6")
        root.config(cursor="")

    def click(event):
        command()

    for item in (btn, txt):
        canvas.tag_bind(item, "<Enter>", enter)
        canvas.tag_bind(item, "<Leave>", leave)
        canvas.tag_bind(item, "<Button-1>", click)


def show_account_form(key):
    global current_page, settings
    clear_entries()
    current_page = key
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()

    draw_background(width, height)

    titles = {
        "change_username": "تغيير اسم المستخدم",
        "change_password": "تغيير كلمة المرور",
        "lock_app": "قفل البرنامج",
        "reset_login": "إعادة ضبط بيانات الدخول",
    }

    draw_top_back(titles.get(key, "الحساب والأمان"), show_account_security)

    if key == "change_username":
        canvas.create_text(width // 2, 210, text="اسم المستخدم الحالي:", fill="#dddddd", font=("Arial", 18, "bold"))
        canvas.create_text(width // 2, 245, text=settings["username"], fill="white", font=("Arial", 24, "bold"))

        entry = tk.Entry(root, font=("Arial", 18), justify="center", bd=0)
        entry_widgets.append(entry)
        canvas.create_window(width // 2, 330, window=entry, width=360, height=45)

        def save_username():
            value = entry.get().strip()
            if not value:
                messagebox.showerror("خطأ", "اكتب اسم مستخدم جديد.")
                return
            settings["username"] = value
            save_settings(settings)
            messagebox.showinfo("تم", "تم تغيير اسم المستخدم بنجاح.")
            show_account_security()

        draw_save_button("حفظ اسم المستخدم", 395, save_username)

    elif key == "change_password":
        old_entry = tk.Entry(root, font=("Arial", 16), justify="center", show="*", bd=0)
        new_entry = tk.Entry(root, font=("Arial", 16), justify="center", show="*", bd=0)
        confirm_entry = tk.Entry(root, font=("Arial", 16), justify="center", show="*", bd=0)

        entry_widgets.extend([old_entry, new_entry, confirm_entry])

        canvas.create_text(width // 2, 190, text="كلمة المرور الحالية", fill="white", font=("Arial", 16, "bold"))
        canvas.create_window(width // 2, 230, window=old_entry, width=360, height=42)

        canvas.create_text(width // 2, 285, text="كلمة المرور الجديدة", fill="white", font=("Arial", 16, "bold"))
        canvas.create_window(width // 2, 325, window=new_entry, width=360, height=42)

        canvas.create_text(width // 2, 380, text="تأكيد كلمة المرور الجديدة", fill="white", font=("Arial", 16, "bold"))
        canvas.create_window(width // 2, 420, window=confirm_entry, width=360, height=42)

        def save_password():
            old = old_entry.get()
            new = new_entry.get()
            confirm = confirm_entry.get()

            if old != settings["password"]:
                messagebox.showerror("خطأ", "كلمة المرور الحالية غير صحيحة.")
                return
            if len(new) < 4:
                messagebox.showerror("خطأ", "كلمة المرور يجب أن تكون 4 أحرف أو أكثر.")
                return
            if new != confirm:
                messagebox.showerror("خطأ", "كلمة المرور الجديدة غير متطابقة.")
                return

            settings["password"] = new
            save_settings(settings)
            messagebox.showinfo("تم", "تم تغيير كلمة المرور بنجاح.")
            show_account_security()

        draw_save_button("حفظ كلمة المرور", 485, save_password)

    elif key == "reset_login":
        canvas.create_text(width // 2, 250, text="سيتم إرجاع بيانات الدخول إلى:", fill="white", font=("Arial", 22, "bold"))
        canvas.create_text(width // 2, 305, text="اسم المستخدم: admin", fill="#dddddd", font=("Arial", 20))
        canvas.create_text(width // 2, 345, text="كلمة المرور: 1234", fill="#dddddd", font=("Arial", 20))

        def reset_login():
            settings["username"] = "admin"
            settings["password"] = "1234"
            save_settings(settings)
            messagebox.showinfo("تم", "تمت إعادة ضبط بيانات الدخول.")
            show_account_security()

        draw_save_button("إعادة الضبط", 420, reset_login)

    elif key == "lock_app":
        canvas.create_text(width // 2, 270, text="تم قفل البرنامج.", fill="white", font=("Arial", 24, "bold"))
        canvas.create_text(width // 2, 320, text="سيتم الرجوع إلى شاشة تسجيل الدخول.", fill="#dddddd", font=("Arial", 18))
        root.after(1000, show_login)


def show_customize():
    global current_page
    clear_entries()
    current_page = "customize"
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()

    draw_background(width, height)
    draw_top_back("تخصيص الواجهة", show_settings)

    customize_items = [
        ("🖼", "#2f7df6", "تغيير صورة الخلفية", "اختر صورة من الحاسوب واستعملها كخلفية للبرنامج", "change_bg"),
        ("♻", "#ff8a18", "إعادة ضبط المصنع", "إرجاع إعدادات البرنامج إلى الوضع الافتراضي دون حذف البيانات", "factory_reset"),
    ]

    def click_customize(k):
        if k == "change_bg":
            change_background()
        else:
            show_setting_placeholder(k)

    draw_list(customize_items, click_customize)


def show_setting_placeholder(key):
    global current_page
    clear_entries()
    current_page = key
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()

    draw_background(width, height)

    titles = {
        "printer": "الطباعة",
        "documents_settings": "إدارة الوثائق",
        "backup": "النسخ الاحتياطي والحماية",
        "clients_db": "قاعدة بيانات الزبائن",
        "smart": "الذكاء والسرعة",
        "info": "معلومات البرنامج",
        "factory_reset": "إعادة ضبط المصنع",
    }

    canvas.create_text(width // 2, 120, text=titles.get(key, "قسم الإعدادات"), fill="white", font=("Arial", 40, "bold"))
    canvas.create_text(width // 2, 300, text="سنقوم ببناء هذا القسم لاحقًا.", fill="#dddddd", font=("Arial", 24, "bold"))

    draw_back_button(show_settings)


def show_placeholder(section):
    global current_page
    clear_entries()
    current_page = section
    canvas.delete("all")

    width = root.winfo_width()
    height = root.winfo_height()

    draw_background(width, height)

    titles = {
        "documents": "واجهة الوثائق",
        "electronic": "واجهة الخدمات الإلكترونية",
        "archive": "واجهة الأرشيف",
    }

    canvas.create_text(width // 2, 140, text=titles.get(section, "واجهة جديدة"), fill="white", font=("Arial", 46, "bold"))
    canvas.create_text(width // 2, 320, text="هذه واجهة مؤقتة، سنبني تفاصيلها لاحقًا.", fill="#dddddd", font=("Arial", 24, "bold"))

    draw_back_button(show_home)


def draw_back_button(command):
    width = root.winfo_width()
    height = root.winfo_height()

    btn = canvas.create_rectangle(
        width // 2 - 90,
        height - 82,
        width // 2 + 90,
        height - 32,
        fill="#404040",
        outline="#666666",
        width=1
    )

    txt = canvas.create_text(
        width // 2,
        height - 57,
        text="رجوع",
        fill="white",
        font=("Arial", 18, "bold")
    )

    def enter(event):
        canvas.itemconfig(btn, fill="#555555")
        root.config(cursor="hand2")

    def leave(event):
        canvas.itemconfig(btn, fill="#404040")
        root.config(cursor="")

    def click(event):
        command()

    for item in (btn, txt):
        canvas.tag_bind(item, "<Enter>", enter)
        canvas.tag_bind(item, "<Leave>", leave)
        canvas.tag_bind(item, "<Button-1>", click)


def on_resize(event):
    if event.widget == root:
        if current_page == "login":
            show_login()
        elif current_page == "forgot":
            show_forgot_password()
        elif current_page == "home":
            show_home()
        elif current_page == "settings":
            show_settings()
        elif current_page == "customize":
            show_customize()
        elif current_page == "account":
            show_account_security()
        elif current_page in ["change_username", "change_password", "lock_app", "reset_login"]:
            show_account_form(current_page)
        elif current_page in ["printer", "documents_settings", "backup", "clients_db", "smart", "info", "factory_reset"]:
            show_setting_placeholder(current_page)
        else:
            show_placeholder(current_page)


root.bind("<Configure>", on_resize)

show_login()
root.mainloop()
