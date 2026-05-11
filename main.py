import os
import sys
import tkinter as tk

APP_NAME = "IDARA DZ"

# =========================
# إعداد التطبيق
# =========================

root = tk.Tk()
root.title(APP_NAME)

try:
    root.state("zoomed")
except:
    root.geometry("1400x820")

root.configure(bg="white")
root.minsize(1100, 700)

canvas = tk.Canvas(root, bg="white", highlightthickness=0)
canvas.pack(fill="both", expand=True)

current_page = "home"
previous_page = "home"

# =========================
# أدوات الرسم
# =========================

def clear_screen():
    canvas.delete("all")

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

# =========================
# الرجوع
# =========================

def go_back():

    global previous_page

    if previous_page == "home":
        show_home()

    elif previous_page == "documents":
        show_documents()

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
        65,
        45,
        text="IDARA DZ",
        fill="#111",
        font=("Arial", 18, "bold")
    )

    menu = [
        ("🏠", 150, "home"),
        ("🔧", 280, "settings"),
        ("ℹ️", 410, "about")
    ]

    for icon, y, page in menu:

        selected = active == page

        bg = "#000" if selected else "#f7f7f7"
        fg = "#fff" if selected else "#000"

        btn = rounded_rect(
            10,
            y-50,
            120,
            y+50,
            r=8,
            fill=bg,
            outline=bg
        )

        text = canvas.create_text(
            65,
            y,
            text=icon,
            fill=fg,
            font=("Arial", 34)
        )

        def click(event, p=page):

            global previous_page

            previous_page = current_page

            if p == "home":
                show_home()

            elif p == "settings":
                show_settings()

            else:
                show_about()

        for item in (btn, text):
            canvas.tag_bind(item, "<Button-1>", click)

    # الوضع الداكن
    canvas.create_text(
        65,
        h - 120,
        text="🌙",
        fill="#000",
        font=("Arial", 28)
    )

    # رجوع
    back_btn = canvas.create_text(
        65,
        h - 50,
        text="↩️",
        fill="#000",
        font=("Arial", 28)
    )

    canvas.tag_bind(back_btn, "<Button-1>", lambda e: go_back())

# =========================
# بطاقات الرئيسية
# =========================

def draw_main_card(x, y, title, desc, command):

    rounded_rect(
        x-145+8,
        y-120+10,
        x+145+8,
        y+120+10,
        r=12,
        fill="#e6e6e6",
        outline="#e6e6e6"
    )

    card = rounded_rect(
        x-145,
        y-120,
        x+145,
        y+120,
        r=12,
        fill="#fff",
        outline="#ddd"
    )

    icons_map = {
        "وثائق": "📄",
        "خدمات الكترونية": "🌐",
        "ارشيف": "🗂️"
    }

    icon = canvas.create_text(
        x,
        y-40,
        text=icons_map.get(title, "📄"),
        fill="#000",
        font=("Arial", 62)
    )

    title_id = canvas.create_text(
        x,
        y+35,
        text=title,
        fill="#000",
        font=("Arial", 28, "bold")
    )

    desc_id = canvas.create_text(
        x,
        y+82,
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

def draw_doc_card(x, y, title):

    rounded_rect(
        x-110+8,
        y-120+10,
        x+110+8,
        y+120+10,
        r=8,
        fill="#dddddd",
        outline="#dddddd"
    )

    card = rounded_rect(
        x-110,
        y-120,
        x+110,
        y+120,
        r=8,
        fill="#fff",
        outline="#eee"
    )

    doc_icons = {
        "طلب خطي": "📄",
        "تصريح شرفي": "📝",
        "سيرة ذاتية": "👤",
        "فاتورة": "🧾"
    }

    icon = canvas.create_text(
        x,
        y-40,
        text=doc_icons.get(title, "📄"),
        fill="#000",
        font=("Arial", 58)
    )

    txt = canvas.create_text(
        x,
        y+60,
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

def show_home():

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
        show_documents
    )

    draw_main_card(
        center_x,
        y,
        "خدمات الكترونية",
        "الوصول إلى الخدمات الإلكترونية\nوالمنصات الرسمية",
        lambda: None
    )

    draw_main_card(
        center_x + 350,
        y,
        "ارشيف",
        "إدارة وأرشفة الملفات والوثائق\nوالوصول إليها بسهولة",
        lambda: None
    )

# =========================
# صفحة الوثائق
# =========================

def show_documents():

    global current_page
    global previous_page

    previous_page = current_page
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

    draw_doc_card(center_x - 420, y, "طلب خطي")
    draw_doc_card(center_x - 140, y, "تصريح شرفي")
    draw_doc_card(center_x + 140, y, "سيرة ذاتية")
    draw_doc_card(center_x + 420, y, "فاتورة")

# =========================
# الإعدادات
# =========================

def show_settings():

    global current_page
    current_page = "settings"

    clear_screen()

    draw_sidebar("settings")

# =========================
# حول البرنامج
# =========================

def show_about():

    global current_page
    current_page = "about"

    clear_screen()

    draw_sidebar("about")

# =========================
# تحديث الحجم
# =========================

resize_after = None

def redraw():

    if current_page == "home":
        show_home()

    elif current_page == "documents":
        show_documents()

    elif current_page == "settings":
        show_settings()

    elif current_page == "about":
        show_about()

def smart_resize(event=None):

    global resize_after

    if resize_after:
        root.after_cancel(resize_after)

    resize_after = root.after(120, redraw)

root.bind("<Configure>", smart_resize)

show_home()

root.mainloop()
