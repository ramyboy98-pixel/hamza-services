from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title("IDARA DZ")
root.geometry("1400x900")
root.configure(bg="#f5f5f5")
root.state("zoomed")

# =========================
# تحميل الصور
# =========================

images = {}

def load_icon(path, size):
    img = Image.open(path)
    img = img.resize(size)
    photo = ImageTk.PhotoImage(img)
    images[path] = photo
    return photo

# القائمة الجانبية
home_icon = load_icon("assets/home.png", (42, 42))
settings_icon = load_icon("assets/settings.png", (42, 42))
info_icon = load_icon("assets/info.png", (42, 42))
moon_icon = load_icon("assets/moon.png", (36, 36))
back_icon = load_icon("assets/back.png", (30, 30))

# الصفحة الرئيسية
documents_icon = load_icon("assets/documents.png", (130, 130))
electronic_icon = load_icon("assets/electronic.png", (130, 130))
archive_icon = load_icon("assets/archive.png", (130, 130))

# صفحة الوثائق
written_icon = load_icon("assets/written_request.png", (110, 110))
honor_icon = load_icon("assets/honor_statement.png", (110, 110))
cv_icon = load_icon("assets/cv.png", (110, 110))
invoice_icon = load_icon("assets/invoice.png", (110, 110))

# =========================
# CANVAS
# =========================

canvas = Canvas(root, bg="#f5f5f5", highlightthickness=0)
canvas.pack(fill=BOTH, expand=True)

# =========================
# صفحات
# =========================

current_page = "home"

# =========================
# القائمة الجانبية
# =========================

def draw_sidebar():
    canvas.create_rectangle(0, 0, 140, 900, fill="white", outline="#dddddd")

    canvas.create_text(
        70,
        35,
        text="IDARA DZ",
        font=("Arial", 20, "bold"),
        fill="black"
    )

    # الرئيسية
    canvas.create_rectangle(
        20, 70, 120, 170,
        fill="#111111",
        outline=""
    )

    canvas.create_image(70, 105, image=home_icon)

    canvas.create_text(
        70,
        145,
        text="الرئيسية",
        font=("Arial", 12, "bold"),
        fill="white"
    )

    # الإعدادات
    canvas.create_image(70, 240, image=settings_icon)

    canvas.create_text(
        70,
        285,
        text="الإعدادات",
        font=("Arial", 11, "bold"),
        fill="black"
    )

    # حول البرنامج
    canvas.create_image(70, 380, image=info_icon)

    canvas.create_text(
        70,
        425,
        text="حول البرنامج",
        font=("Arial", 11, "bold"),
        fill="black"
    )

    # الوضع الداكن
    canvas.create_image(70, 720, image=moon_icon)

    canvas.create_text(
        70,
        760,
        text="الوضع الداكن",
        font=("Arial", 11, "bold"),
        fill="black"
    )

    # رجوع
    canvas.create_image(70, 830, image=back_icon)

# =========================
# بطاقة
# =========================

def draw_card(x1, y1, x2, y2, title, desc, icon_img, command=None):

    card = canvas.create_rectangle(
        x1,
        y1,
        x2,
        y2,
        fill="white",
        outline="#e0e0e0",
        width=1
    )

    canvas.create_image(
        (x1 + x2) // 2,
        y1 + 90,
        image=icon_img
    )

    canvas.create_text(
        (x1 + x2) // 2,
        y1 + 210,
        text=title,
        font=("Arial", 28, "bold"),
        fill="black"
    )

    canvas.create_text(
        (x1 + x2) // 2,
        y1 + 265,
        text=desc,
        font=("Arial", 13),
        fill="#444444",
        width=250,
        justify="center"
    )

    if command:
        canvas.tag_bind(card, "<Button-1>", command)

# =========================
# الصفحة الرئيسية
# =========================

def show_home(event=None):

    global current_page
    current_page = "home"

    canvas.delete("all")

    draw_sidebar()

    canvas.create_text(
        770,
        120,
        text="IDARADZ",
        font=("Arial", 60, "bold"),
        fill="#2d3748"
    )

    canvas.create_text(
        770,
        180,
        text="خدمات إدارية بكل احترافية",
        font=("Arial", 24),
        fill="#666666"
    )

    draw_card(
        260, 260, 560, 600,
        "وثائق",
        "إنشاء و تعديل مختلف الوثائق الإدارية بسهولة",
        documents_icon,
        open_documents
    )

    draw_card(
        620, 260, 920, 600,
        "خدمات الكترونية",
        "الوصول إلى الخدمات الإلكترونية والمنصات الرسمية",
        electronic_icon
    )

    draw_card(
        980, 260, 1280, 600,
        "ارشيف",
        "إدارة و أرشفة الملفات والوثائق والوصول إليها بسهولة",
        archive_icon
    )

# =========================
# صفحة الوثائق
# =========================

def open_documents(event=None):

    global current_page
    current_page = "documents"

    canvas.delete("all")

    draw_sidebar()

    canvas.create_text(
        760,
        100,
        text="وثائق",
        font=("Arial", 56, "bold"),
        fill="black"
    )

    canvas.create_text(
        760,
        150,
        text="إنشاء و تعديل مختلف الوثائق الإدارية",
        font=("Arial", 20),
        fill="#555555"
    )

    draw_card(
        220, 260, 470, 560,
        "طلب خطي",
        "",
        written_icon
    )

    draw_card(
        530, 260, 780, 560,
        "تصريح شرفي",
        "",
        honor_icon
    )

    draw_card(
        840, 260, 1090, 560,
        "سيرة ذاتية",
        "",
        cv_icon
    )

    draw_card(
        1150, 260, 1400, 560,
        "فاتورة",
        "",
        invoice_icon
    )

# =========================
# رجوع
# =========================

def back_page(event=None):

    if current_page == "documents":
        show_home()

# =========================
# ربط الأزرار
# =========================

canvas.bind("<Button-1>", lambda e: None)

# زر الرجوع
def check_back(event):

    x = event.x
    y = event.y

    if 40 <= x <= 100 and 810 <= y <= 850:
        back_page()

    if 20 <= x <= 120 and 70 <= y <= 170:
        show_home()

canvas.bind("<Button-1>", check_back)

# =========================
# تشغيل
# =========================

show_home()

root.mainloop()
