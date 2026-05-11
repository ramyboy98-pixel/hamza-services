import os
import sys
import tkinter as tk

APP_NAME = "IDARA DZ"

# =========================
# مسارات الملفات
# =========================

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# =========================
# إعداد التطبيق
# =========================

root = tk.Tk()
root.title(APP_NAME)

try:
    root.state("zoomed")
except Exception:
    root.geometry("1400x820")

root.configure(bg="white")
root.minsize(1100, 700)

canvas = tk.Canvas(root, bg="white", highlightthickness=0)
canvas.pack(fill="both", expand=True)

current_page = "home"
page_history = []
images = {}


# =========================
# تحميل الصور
# =========================

def load_image(filename):
    if filename in images:
        return images[filename]

    path = resource_path(os.path.join("assets", filename))

    if not os.path.exists(path):
        return None

    try:
        img = tk.PhotoImage(file=path)
        images[filename] = img
        return img
    except Exception:
        return None


# =========================
# أدوات الرسم
# =========================

def clear_screen():
    canvas.delete("all")
    root.config(cursor="")


def rounded_rect(x1, y1, x2, y2, r=12, fill="#fff", outline="#ddd"):
    points = [
        x1+r, y1,
        x2-r, y1,
        x2, y1,
        x2, y1+r,
        x2, y2-r,
        x2, y2,
        x2-r, y2,
        x1+r, y2,
        x1, y2,
        x1, y2-r,
        x1, y1+r,
        x1, y1,
    ]

    return canvas.create_polygon(
        points,
        smooth=True,
        fill=fill,
        outline=outline
    )


def go_to(page_function):
    global current_page

    page_history.append(current_page)
    page_function()


def go_back():
    if not page_history:
        show_home()
        return

    last_page = page_history.pop()

    if last_page == "home":
        show_home(save_history=False)
    elif last_page == "documents":
        show_documents(save_history=False)
    elif last_page == "settings":
        show_settings(save_history=False)
    elif last_page == "about":
        show_about(save_history=False)
    else:
        show_home(save_history=False)


# =========================
# الشريط الجانبي
# =========================

def draw_sidebar(active="home"):
    h = root.winfo_height()

    canvas.create_rectangle(
        0, 0, 130, h,
        fill="#f7f7f7",
        outline="#e2e2e2"
    )

    canvas.create_text(
        65, 45,
        text="IDARA DZ",
        fill="#111",
        font=("Arial", 18, "bold")
    )

    menu = [
        ("home.png", "home", 150),
        ("settings.png", "settings", 280),
        ("info.png", "about", 410),
    ]

    for icon_file, page, y in menu:
        selected = active == page

        bg = "#000" if selected else "#f7f7f7"

        btn = rounded_rect(
            10, y-50,
            120, y+50,
            r=8,
            fill=bg,
            outline=bg
        )

        icon_img = load_image(icon_file)

        if icon_img:
            icon = canvas.create_image(65, y, image=icon_img)
        else:
            fallback = {
                "home": "⌂",
                "settings": "⚙",
                "about": "ⓘ"
            }.get(page, "●")

            fg = "#fff" if selected else "#000"
            icon = canvas.create_text(
                65, y,
                text=fallback,
                fill=fg,
                font=("Arial", 32, "bold")
            )

        def click(event, p=page):
            if p == "home":
                show_home()
            elif p == "settings":
                go_to(show_settings)
            elif p == "about":
                go_to(show_about)

        def hover_in(event, b=btn, sel=selected):
            if not sel:
                canvas.itemconfig(b, fill="#eeeeee", outline="#eeeeee")
            root.config(cursor="hand2")

        def hover_out(event, b=btn, sel=selected):
            if not sel:
                canvas.itemconfig(b, fill="#f7f7f7", outline="#f7f7f7")
            root.config(cursor="")

        for item in (btn, icon):
            canvas.tag_bind(item, "<Enter>", hover_in)
            canvas.tag_bind(item, "<Leave>", hover_out)
            canvas.tag_bind(item, "<Button-1>", click)

    # أيقونة الوضع الداكن
    moon_img = load_image("moon.png")
    if moon_img:
        moon = canvas.create_image(65, h - 140, image=moon_img)
    else:
        moon = canvas.create_text(
            65,
            h - 140,
            text="☾",
            fill="#000",
            font=("Arial", 28, "bold")
        )

    # أيقونة الرجوع
    back_img = load_image("back.png")
    if back_img:
        back = canvas.create_image(65, h - 60, image=back_img)
    else:
        back = canvas.create_text(
            65,
            h - 60,
            text="↩",
            fill="#000",
            font=("Arial", 25, "bold")
        )

    for item in (moon,):
        canvas.tag_bind(item, "<Enter>", lambda e: root.config(cursor="hand2"))
        canvas.tag_bind(item, "<Leave>", lambda e: root.config(cursor=""))

    for item in (back,):
        canvas.tag_bind(item, "<Enter>", lambda e: root.config(cursor="hand2"))
        canvas.tag_bind(item, "<Leave>", lambda e: root.config(cursor=""))
        canvas.tag_bind(item, "<Button-1>", lambda e: go_back())


# =========================
# بطاقات الرئيسية
# =========================

def draw_main_card(x, y, title, desc, icon_file, command):
    card_w = 290
    card_h = 255

    x1 = x - card_w//2
    y1 = y - card_h//2
    x2 = x + card_w//2
    y2 = y + card_h//2

    rounded_rect(
        x1+8,
        y1+10,
        x2+8,
        y2+10,
        r=12,
        fill="#e6e6e6",
        outline="#e6e6e6"
    )

    card = rounded_rect(
        x1,
        y1,
        x2,
        y2,
        r=12,
        fill="#fff",
        outline="#ddd"
    )

    icon_img = load_image(icon_file)

    if icon_img:
        icon = canvas.create_image(x, y1 + 75, image=icon_img)
    else:
        icon = canvas.create_text(
            x,
            y1 + 75,
            text="▣",
            fill="#000",
            font=("Arial", 56, "bold")
        )

    title_id = canvas.create_text(
        x,
        y1 + 150,
        text=title,
        fill="#000",
        font=("Arial", 27, "bold")
    )

    desc_id = canvas.create_text(
        x,
        y1 + 205,
        text=desc,
        fill="#555",
        font=("Arial", 13, "bold"),
        justify="center"
    )

    def hover_in(event):
        canvas.itemconfig(card, fill="#fafafa")
        root.config(cursor="hand2")

    def hover_out(event):
        canvas.itemconfig(card, fill="#fff")
        root.config(cursor="")

    def click(event):
        command()

    for item in (card, icon, title_id, desc_id):
        canvas.tag_bind(item, "<Enter>", hover_in)
        canvas.tag_bind(item, "<Leave>", hover_out)
        canvas.tag_bind(item, "<Button-1>", click)


# =========================
# بطاقات الوثائق
# =========================

def draw_doc_card(x, y, title, icon_file):
    card_w = 220
    card_h = 240

    x1 = x - card_w//2
    y1 = y - card_h//2
    x2 = x + card_w//2
    y2 = y + card_h//2

    rounded_rect(
        x1+8,
        y1+12,
        x2+8,
        y2+12,
        r=8,
        fill="#dddddd",
        outline="#dddddd"
    )

    card = rounded_rect(
        x1,
        y1,
        x2,
        y2,
        r=8,
        fill="#fff",
        outline="#eee"
    )

    icon_img = load_image(icon_file)

    if icon_img:
        icon = canvas.create_image(x, y1 + 75, image=icon_img)
    else:
        icon = canvas.create_text(
            x,
            y1 + 75,
            text="▣",
            fill="#000",
            font=("Arial", 52, "bold")
        )

    txt = canvas.create_text(
        x,
        y1 + 175,
        text=title,
        fill="#000",
        font=("Arial", 24, "bold")
    )

    def hover_in(event):
        canvas.itemconfig(card, fill="#fafafa")
        root.config(cursor="hand2")

    def hover_out(event):
        canvas.itemconfig(card, fill="#fff")
        root.config(cursor="")

    for item in (card, icon, txt):
        canvas.tag_bind(item, "<Enter>", hover_in)
        canvas.tag_bind(item, "<Leave>", hover_out)


# =========================
# الصفحة الرئيسية
# =========================

def show_home(save_history=True):
    global current_page

    current_page = "home"

    clear_screen()

    w = root.winfo_width()
    h = root.winfo_height()

    draw_sidebar("home")

    center_x = 130 + (w - 130)//2

    canvas.create_text(
        center_x,
        160,
        text="IDARADZ",
        fill="#222",
        font=("Arial", 58, "bold")
    )

    canvas.create_text(
        center_x,
        225,
        text="خدمات إدارية بكل احترافية",
        fill="#555",
        font=("Arial", 18, "bold")
    )

    y = h//2 + 40

    draw_main_card(
        center_x - 350,
        y,
        "وثائق",
        "إنشاء وتعديل مختلف الوثائق\nالإدارية بسهولة",
        "documents.png",
        lambda: go_to(show_documents)
    )

    draw_main_card(
        center_x,
        y,
        "خدمات الكترونية",
        "الوصول إلى الخدمات الإلكترونية\nوالمنصات الرسمية",
        "electronic.png",
        lambda: None
    )

    draw_main_card(
        center_x + 350,
        y,
        "ارشيف",
        "إدارة وأرشفة الملفات والوثائق\nوالوصول إليها بسهولة",
        "archive.png",
        lambda: None
    )


# =========================
# صفحة الوثائق
# =========================

def show_documents(save_history=True):
    global current_page

    current_page = "documents"

    clear_screen()

    w = root.winfo_width()
    h = root.winfo_height()

    draw_sidebar("home")

    center_x = 130 + (w - 130)//2

    canvas.create_text(
        center_x,
        110,
        text="وثائق",
        fill="#000",
        font=("Arial", 52, "bold")
    )

    canvas.create_text(
        center_x,
        155,
        text="— إنشاء و تعديل مختلف الوثائق الإدارية —",
        fill="#000",
        font=("Arial", 14, "bold")
    )

    y = h//2 + 40

    draw_doc_card(center_x - 420, y, "طلب خطي", "written_request.png")
    draw_doc_card(center_x - 140, y, "تصريح شرفي", "honor_statement.png")
    draw_doc_card(center_x + 140, y, "سيرة ذاتية", "cv.png")
    draw_doc_card(center_x + 420, y, "فاتورة", "invoice.png")


# =========================
# الإعدادات
# =========================

def show_settings(save_history=True):
    global current_page

    current_page = "settings"

    clear_screen()

    draw_sidebar("settings")


# =========================
# حول البرنامج
# =========================

def show_about(save_history=True):
    global current_page

    current_page = "about"

    clear_screen()

    draw_sidebar("about")


# =========================
# تحديث الحجم
# =========================

def on_resize(event=None):
    if event and event.widget != root:
        return

    if current_page == "home":
        show_home(save_history=False)

    elif current_page == "documents":
        show_documents(save_history=False)

    elif current_page == "settings":
        show_settings(save_history=False)

    elif current_page == "about":
        show_about(save_history=False)


root.bind("<Configure>", on_resize)

show_home()

root.mainloop()
