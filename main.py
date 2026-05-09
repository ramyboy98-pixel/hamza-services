import tkinter as tk
from PIL import Image, ImageTk
import os
import sys
import subprocess
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import calendar
from datetime import date


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


root = tk.Tk()
root.title("IDARA DZ")
root.geometry("1280x720")
root.minsize(1000, 600)
root.configure(bg="black")

canvas = tk.Canvas(root, highlightthickness=0, bd=0)
canvas.pack(fill="both", expand=True)

background_photo = None
current_page = "home"
animation_running = False


def clear_screen():
    global animation_running
    animation_running = False
    canvas.delete("all")


def draw_image(path, width, height):
    global background_photo

    if os.path.exists(path):
        img = Image.open(path).convert("RGB")
        img = img.resize((width, height), Image.LANCZOS)
    else:
        img = Image.new("RGB", (width, height), "#173b38")

    background_photo = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, image=background_photo, anchor="nw")


def show_home():
    global current_page
    current_page = "home"
    clear_screen()

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_image(resource_path("assets/background.jpg"), width, height)

    right_x = int(width * 0.58)
    menu_center_x = right_x + (width - right_x) // 2

    menu_items = [
        ("وثائق", "documents"),
        ("خدمات إلكترونية", "electronic"),
        ("أرشيف", "archive"),
        ("حول البرنامج", "about"),
    ]

    start_y = int(height * 0.31)
    gap = int(height * 0.135)

    for index, (label, key) in enumerate(menu_items):
        y = start_y + index * gap

        text_id = canvas.create_text(
            menu_center_x,
            y,
            text=label,
            fill="#f4f4f4",
            font=("Arial", 30, "bold"),
            anchor="center"
        )

        hitbox = canvas.create_rectangle(
            right_x + 55,
            y - 35,
            width - 55,
            y + 35,
            fill="",
            outline=""
        )

        def on_enter(event, t=text_id):
            canvas.itemconfig(t, fill="#d7c28a")
            root.config(cursor="hand2")

        def on_leave(event, t=text_id):
            canvas.itemconfig(t, fill="#f4f4f4")
            root.config(cursor="")

        def on_click(event, k=key):
            if k == "about":
                show_about()
            elif k == "documents":
                show_documents()
            else:
                show_section(k)

        for item in (text_id, hitbox):
            canvas.tag_bind(item, "<Enter>", on_enter)
            canvas.tag_bind(item, "<Leave>", on_leave)
            canvas.tag_bind(item, "<Button-1>", on_click)


def draw_back_button(command):
    btn = canvas.create_rectangle(
        35,
        35,
        145,
        82,
        fill="#173b38",
        outline="#d7c28a",
        width=2
    )

    txt = canvas.create_text(
        90,
        58,
        text="رجوع",
        fill="#f4f4f4",
        font=("Arial", 16, "bold")
    )

    def enter(event):
        canvas.itemconfig(btn, fill="#21524d")
        root.config(cursor="hand2")

    def leave(event):
        canvas.itemconfig(btn, fill="#173b38")
        root.config(cursor="")

    def click(event):
        command()

    for item in (btn, txt):
        canvas.tag_bind(item, "<Enter>", enter)
        canvas.tag_bind(item, "<Leave>", leave)
        canvas.tag_bind(item, "<Button-1>", click)


def show_documents():
    global current_page, animation_running
    current_page = "documents"
    clear_screen()
    animation_running = True

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_image(resource_path("assets/background.jpg"), width, height)

    right_x = int(width * 0.58)
    menu_center_x = right_x + (width - right_x) // 2

    title_start_y = int(height * 0.31)
    title_target_y = int(height * 0.15)

    title_id = canvas.create_text(
        menu_center_x,
        title_start_y,
        text="وثائق",
        fill="#f4f4f4",
        font=("Arial", 30, "bold"),
        anchor="center"
    )

    sub_items = [
        ("طلب خطي", "written_request"),
        ("تصريح شرفي", "honor_statement"),
        ("سيرة ذاتية", "cv"),
        ("فاتورة", "invoice"),
    ]

    sub_texts = []
    line_ids = []

    start_y = int(height * 0.31)
    gap = int(height * 0.135)

    for index, (label, key) in enumerate(sub_items):
        y = start_y + index * gap
        start_x = width + 240
        target_x = menu_center_x

        text_id = canvas.create_text(
            start_x,
            y,
            text=label,
            fill="#e8e1d5",
            font=("Arial", 24, "bold"),
            anchor="center"
        )

        line_id = canvas.create_line(
            width + 100,
            y + int(gap * 0.43),
            width + 520,
            y + int(gap * 0.43),
            fill="#8aa09c",
            width=1
        )

        sub_texts.append((text_id, key, target_x, y))
        line_ids.append((line_id, right_x + 70, width - 70, y + int(gap * 0.43)))

    def animate_title(step=0):
        if not animation_running or current_page != "documents":
            return

        total_steps = 8
        if step <= total_steps:
            current_y = title_start_y + (title_target_y - title_start_y) * step / total_steps
            size = int(30 + (54 - 30) * step / total_steps)
            canvas.coords(title_id, menu_center_x, current_y)
            canvas.itemconfig(title_id, font=("Arial", size, "bold"))
            root.after(8, lambda: animate_title(step + 1))
        else:
            animate_sub_items(0)

    def animate_sub_items(step=0):
        if not animation_running or current_page != "documents":
            return

        total_steps = 10
        if step <= total_steps:
            for text_id, key, target_x, y in sub_texts:
                start_x = width + 240
                current_x = start_x + (target_x - start_x) * step / total_steps
                canvas.coords(text_id, current_x, y)

            for line_id, x1, x2, y in line_ids:
                start_x1 = width + 100
                start_x2 = width + 520
                current_x1 = start_x1 + (x1 - start_x1) * step / total_steps
                current_x2 = start_x2 + (x2 - start_x2) * step / total_steps
                canvas.coords(line_id, current_x1, y, current_x2, y)

            root.after(6, lambda: animate_sub_items(step + 1))
        else:
            bind_document_items()

    def bind_document_items():
        for text_id, key, target_x, y in sub_texts:
            hitbox = canvas.create_rectangle(
                right_x + 55,
                y - 32,
                width - 55,
                y + 32,
                fill="",
                outline=""
            )

            def on_enter(event, t=text_id):
                canvas.itemconfig(t, fill="#d7c28a")
                root.config(cursor="hand2")

            def on_leave(event, t=text_id):
                canvas.itemconfig(t, fill="#e8e1d5")
                root.config(cursor="")

            def on_click(event, k=key):
                show_document_type(k)

            for item in (text_id, hitbox):
                canvas.tag_bind(item, "<Enter>", on_enter)
                canvas.tag_bind(item, "<Leave>", on_leave)
                canvas.tag_bind(item, "<Button-1>", on_click)

        draw_back_button(show_home)

    animate_title()


def show_document_type(doc_type):
    if doc_type == "written_request":
        show_written_request()
        return

    global current_page
    current_page = doc_type
    clear_screen()

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_image(resource_path("assets/background.jpg"), width, height)

    titles = {
        "honor_statement": "تصريح شرفي",
        "cv": "سيرة ذاتية",
        "invoice": "فاتورة",
    }

    canvas.create_rectangle(
        int(width * 0.18),
        int(height * 0.22),
        int(width * 0.82),
        int(height * 0.72),
        fill="#173b38",
        outline="#d7c28a",
        width=2
    )

    canvas.create_text(
        width // 2,
        int(height * 0.34),
        text=titles.get(doc_type, "وثيقة"),
        fill="#f4f4f4",
        font=("Arial", 44, "bold")
    )

    canvas.create_text(
        width // 2,
        int(height * 0.50),
        text="سنقوم ببناء هذه الوثيقة لاحقًا.",
        fill="#e8e1d5",
        font=("Arial", 24, "bold")
    )

    draw_back_button(show_documents)


written_request_scroll = 0
written_request_items = [
    "طلب توظيف عام"
]


def show_written_request():
    global current_page, written_request_scroll
    current_page = "written_request"
    clear_screen()

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_image(resource_path("assets/background.jpg"), width, height)

    right_x = int(width * 0.58)
    menu_center_x = right_x + (width - right_x) // 2

    canvas.create_text(
        menu_center_x,
        int(height * 0.12),
        text="طلب خطي",
        fill="#f4f4f4",
        font=("Arial", 50, "bold"),
        anchor="center"
    )

    visible_count = 10
    max_scroll = max(0, len(written_request_items) - visible_count)
    written_request_scroll = max(0, min(written_request_scroll, max_scroll))

    start_y = int(height * 0.24)
    row_gap = int(height * 0.065)

    visible_items = written_request_items[written_request_scroll:written_request_scroll + visible_count]

    for index, label in enumerate(visible_items):
        y = start_y + index * row_gap

        line_id = canvas.create_line(
            right_x + 70,
            y - 18,
            width - 70,
            y - 18,
            fill="#8aa09c",
            width=1
        )

        text_id = canvas.create_text(
            menu_center_x,
            y,
            text=label,
            fill="#e8e1d5",
            font=("Arial", 23, "bold"),
            anchor="center"
        )

        hitbox = canvas.create_rectangle(
            right_x + 55,
            y - 25,
            width - 55,
            y + 25,
            fill="",
            outline=""
        )

        def on_enter(event, t=text_id):
            canvas.itemconfig(t, fill="#d7c28a")
            root.config(cursor="hand2")

        def on_leave(event, t=text_id):
            canvas.itemconfig(t, fill="#e8e1d5")
            root.config(cursor="")

        def on_click(event, name=label):
            show_written_request_template(name)

        for item in (text_id, hitbox, line_id):
            canvas.tag_bind(item, "<Enter>", on_enter)
            canvas.tag_bind(item, "<Leave>", on_leave)
            canvas.tag_bind(item, "<Button-1>", on_click)

    if written_request_scroll < max_scroll:
        canvas.create_text(
            menu_center_x,
            height - 42,
            text="∨",
            fill="#777777",
            font=("Arial", 34, "bold")
        )

    if written_request_scroll > 0:
        canvas.create_text(
            menu_center_x,
            int(height * 0.18),
            text="∧",
            fill="#777777",
            font=("Arial", 23, "bold")
        )

    draw_back_button(show_documents)


def scroll_written_request(event):
    global written_request_scroll

    if current_page != "written_request":
        return

    if event.delta < 0:
        written_request_scroll += 1
    else:
        written_request_scroll -= 1

    max_scroll = max(0, len(written_request_items) - 10)
    written_request_scroll = max(0, min(written_request_scroll, max_scroll))
    show_written_request()


def show_written_request_template(name):
    if name == "طلب توظيف عام":
        show_job_request_form()
        return

    global current_page
    current_page = "written_request_template"
    clear_screen()

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_image(resource_path("assets/background.jpg"), width, height)

    canvas.create_rectangle(
        int(width * 0.18),
        int(height * 0.22),
        int(width * 0.82),
        int(height * 0.72),
        fill="#173b38",
        outline="#d7c28a",
        width=2
    )

    canvas.create_text(
        width // 2,
        int(height * 0.34),
        text=name,
        fill="#f4f4f4",
        font=("Arial", 38, "bold")
    )

    canvas.create_text(
        width // 2,
        int(height * 0.50),
        text="سنقوم ببناء نموذج هذا الطلب في الخطوة القادمة.",
        fill="#e8e1d5",
        font=("Arial", 22, "bold")
    )

    draw_back_button(show_written_request)


job_form_scroll = 0
job_form_entries = {}

REQUEST_TYPE_OPTIONS = [
    "مسابقة على أساس الشهادة",
    "مسابقة على أساس الاختبار",
    "طلب استخلاف",
    "مسابقة الحماية المدنية",
    "مسابقة الشرطة",
    "مسابقة الجمارك",
    "طلب توظيف (عام)",
    "طلب استقالة",
    "طلب سكن",
    "طلب شهادة عمل",
    "طلب تربص ميداني",
    "طلب عطلة سنوية",
    "طلب تحويل إداري",
    "طلب تسوية وضعية",
]

request_type_dropdown_open = False
request_type_scroll = 0
request_type_selected_index = 6


def rounded_rect(x1, y1, x2, y2, r=24, fill="#f3eeee", outline="#f3eeee", width=1):
    points = [
        x1 + r, y1,
        x2 - r, y1,
        x2, y1,
        x2, y1 + r,
        x2, y2 - r,
        x2, y2,
        x2 - r, y2,
        x1 + r, y2,
        x1, y2,
        x1, y2 - r,
        x1, y1 + r,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, fill=fill, outline=outline, width=width)


def make_placeholder_entry(x, y, w, h, placeholder, field_key):
    value = job_form_entries.get(field_key, "")

    rounded_rect(
        x - w // 2,
        y - h // 2,
        x + w // 2,
        y + h // 2,
        r=28,
        fill="#f3eeee",
        outline="#d9d1d1",
        width=2
    )

    entry = tk.Entry(
        root,
        font=("Arial", 21, "bold"),
        justify="right",
        bd=0,
        bg="#f3eeee",
        fg="#111111",
        insertbackground="#173b38"
    )

    if value:
        entry.insert(0, value)
        entry.config(fg="#111111")
    else:
        entry.insert(0, placeholder)
        entry.config(fg="#777777")

    def focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg="#111111")

    def focus_out(event):
        if not entry.get().strip():
            entry.delete(0, "end")
            entry.insert(0, placeholder)
            entry.config(fg="#777777")
            job_form_entries[field_key] = ""

    def save_value(event=None):
        val = entry.get()
        if val == placeholder:
            job_form_entries[field_key] = ""
        else:
            job_form_entries[field_key] = val

    entry.bind("<FocusIn>", focus_in)
    entry.bind("<FocusOut>", focus_out)
    entry.bind("<KeyRelease>", save_value)

    canvas.create_window(x, y, window=entry, width=w - 46, height=h - 16)
    return entry


def open_request_type_dropdown():
    global request_type_dropdown_open
    request_type_dropdown_open = True
    show_job_request_form()


def close_request_type_dropdown():
    global request_type_dropdown_open
    request_type_dropdown_open = False
    show_job_request_form()


def choose_request_type(value):
    global request_type_dropdown_open
    job_form_entries["request_type"] = value
    request_type_dropdown_open = False
    show_job_request_form()


def scroll_request_type_dropdown(direction):
    global request_type_scroll

    max_visible = 6
    max_scroll = max(0, len(REQUEST_TYPE_OPTIONS) - max_visible)

    if direction > 0:
        request_type_scroll += 1
    else:
        request_type_scroll -= 1

    request_type_scroll = max(0, min(request_type_scroll, max_scroll))
    show_job_request_form()


def move_request_type_selection(direction):
    global request_type_selected_index, request_type_scroll, request_type_dropdown_open

    if not request_type_dropdown_open:
        return

    request_type_selected_index += direction
    request_type_selected_index = max(0, min(request_type_selected_index, len(REQUEST_TYPE_OPTIONS) - 1))

    max_visible = 6
    if request_type_selected_index < request_type_scroll:
        request_type_scroll = request_type_selected_index
    elif request_type_selected_index >= request_type_scroll + max_visible:
        request_type_scroll = request_type_selected_index - max_visible + 1

    show_job_request_form()


def confirm_request_type_selection():
    global request_type_dropdown_open

    if not request_type_dropdown_open:
        return

    choose_request_type(REQUEST_TYPE_OPTIONS[request_type_selected_index])


def draw_request_type_field(x, y, w, h):
    selected_value = job_form_entries.get("request_type", "")

    rounded_rect(
        x - w // 2,
        y - h // 2,
        x + w // 2,
        y + h // 2,
        r=28,
        fill="#f3eeee",
        outline="#d9d1d1",
        width=2
    )

    arrow_x = x - w // 2 + 45
    arrow = canvas.create_text(
        arrow_x,
        y,
        text="▼",
        fill="#555555",
        font=("Arial", 26, "bold")
    )

    text = canvas.create_text(
        x + w // 2 - 48,
        y,
        text=selected_value if selected_value else "نوع الطلب",
        fill="#173b38" if selected_value else "#777777",
        font=("Arial", 21, "bold"),
        anchor="e"
    )

    hitbox = canvas.create_rectangle(
        x - w // 2,
        y - h // 2,
        x + w // 2,
        y + h // 2,
        fill="",
        outline=""
    )

    def enter(event):
        root.config(cursor="hand2")

    def leave(event):
        root.config(cursor="")

    def click(event):
        open_request_type_dropdown()

    for item in (arrow, text, hitbox):
        canvas.tag_bind(item, "<Enter>", enter)
        canvas.tag_bind(item, "<Leave>", leave)
        canvas.tag_bind(item, "<Button-1>", click)

    if request_type_dropdown_open:
        draw_request_type_dropdown(x, y + h // 2 + 8, w)


def draw_request_type_dropdown(x, y, w):
    global request_type_selected_index

    max_visible = 6
    row_h = 44
    visible = REQUEST_TYPE_OPTIONS[request_type_scroll:request_type_scroll + max_visible]

    box_x1 = x - w // 2
    box_x2 = x + w // 2
    box_y1 = y
    box_y2 = y + len(visible) * row_h + 14

    rounded_rect(
        box_x1,
        box_y1,
        box_x2,
        box_y2,
        r=22,
        fill="#f3eeee",
        outline="#d9d1d1",
        width=2
    )

    for index, value in enumerate(visible):
        real_index = request_type_scroll + index
        item_y = box_y1 + 18 + index * row_h + row_h // 2

        is_selected = real_index == request_type_selected_index
        if is_selected:
            selected_bg = rounded_rect(
                box_x1 + 12,
                item_y - 18,
                box_x2 - 12,
                item_y + 18,
                r=16,
                fill="#d7c28a",
                outline="#d7c28a",
                width=1
            )

        item_text = canvas.create_text(
            box_x2 - 35,
            item_y,
            text=value,
            fill="#173b38",
            font=("Arial", 17, "bold"),
            anchor="e"
        )

        hitbox = canvas.create_rectangle(
            box_x1 + 10,
            item_y - 20,
            box_x2 - 10,
            item_y + 20,
            fill="",
            outline=""
        )

        def enter(event, idx=real_index):
            global request_type_selected_index
            request_type_selected_index = idx
            root.config(cursor="hand2")

        def leave(event):
            root.config(cursor="")

        def click(event, chosen=value):
            choose_request_type(chosen)

        for item in (item_text, hitbox):
            canvas.tag_bind(item, "<Enter>", enter)
            canvas.tag_bind(item, "<Leave>", leave)
            canvas.tag_bind(item, "<Button-1>", click)

    if request_type_scroll > 0:
        canvas.create_text(x, box_y1 + 10, text="▲", fill="#777777", font=("Arial", 12, "bold"))

    if request_type_scroll + max_visible < len(REQUEST_TYPE_OPTIONS):
        canvas.create_text(x, box_y2 - 9, text="▼", fill="#777777", font=("Arial", 12, "bold"))



def set_run_font(run, size=16, bold=False):
    run.font.name = "Arial"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    run.font.size = Pt(size)
    run.bold = bold


def add_doc_paragraph(doc, text, size=16, bold=False, align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=10):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold)
    return p


def open_generated_file(path):
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception as e:
        try:
            from tkinter import messagebox
            messagebox.showinfo("تم", f"تم إنشاء الملف:\n{path}")
        except:
            pass


def create_job_request_word():
    output_dir = os.path.join(os.path.expanduser("~"), "IDARA_DZ_Outputs")
    os.makedirs(output_dir, exist_ok=True)

    first_name = job_form_entries.get("first_name", "").strip()
    last_name = job_form_entries.get("last_name", "").strip()
    full_name = f"{last_name} {first_name}".strip()

    request_date = job_form_entries.get("date", "").strip()
    address = job_form_entries.get("address", "").strip()
    phone = job_form_entries.get("phone", "").strip()
    recipient = job_form_entries.get("recipient", "").strip()
    position = job_form_entries.get("position", "").strip()
    degree = job_form_entries.get("degree", "").strip()
    specialty = job_form_entries.get("specialty", "").strip()
    request_type = job_form_entries.get("request_type", "").strip() or "طلب توظيف (عام)"

    safe_name = full_name if full_name else "بدون_اسم"
    safe_name = safe_name.replace("/", "-").replace("\\", "-").replace(":", "-")
    file_name = f"{request_type}_{safe_name}.docx".replace(" ", "_")
    output_path = os.path.join(output_dir, file_name)

    doc = Document()

    section = doc.sections[0]
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.right_margin = Cm(2.0)
    section.left_margin = Cm(2.0)

    # Top date
    add_doc_paragraph(
        doc,
        f"في: {request_date}",
        size=16,
        bold=False,
        align=WD_ALIGN_PARAGRAPH.LEFT,
        space_after=36
    )

    # Personal info block
    add_doc_paragraph(doc, f"الاسم واللقب: {full_name}", size=16, align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=8)
    add_doc_paragraph(doc, f"العنوان: {address}", size=16, align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=8)
    add_doc_paragraph(doc, f"الهاتف: {phone}", size=16, align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=38)

    # Recipient
    add_doc_paragraph(
        doc,
        f"إلى السيد: {recipient}",
        size=20,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=45
    )

    # Subject
    subject = "طلب توظيف"
    if request_type and request_type != "طلب توظيف (عام)":
        subject = request_type

    add_doc_paragraph(
        doc,
        f"الموضوع: {subject}",
        size=18,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=42
    )

    body_1 = (
        f"يشرفني أن أتقدم بطلبي هذا من أجل الحصول على منصب {position} "
        f"يتوافق مع مؤهلاتي العلمية وخبراتي المهنية في مؤسستكم الموقرة."
    )

    body_2 = (
        f"أنا {full_name}، متحصل على شهادة {degree}، تخصص {specialty}. "
        "أتمتع بروح المسؤولية والانضباط، وأطمح للمساهمة في تطوير أداء مؤسستكم."
    )

    add_doc_paragraph(doc, body_1, size=17, align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=28)
    add_doc_paragraph(doc, body_2, size=17, align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=80)

    add_doc_paragraph(
        doc,
        "توقيع المعني:",
        size=18,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.LEFT,
        space_after=10
    )

    doc.save(output_path)
    return output_path


def show_job_request_form():
    global current_page, job_form_entries
    current_page = "job_request_form"
    clear_screen()

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    canvas.create_rectangle(0, 0, width, height, fill="#173b38", outline="#173b38")

    right_col_x = int(width * 0.78)
    left_col_x = int(width * 0.30)

    title_y = int(height * 0.08)

    canvas.create_text(
        right_col_x,
        title_y,
        text="المعلومات الشخصية",
        fill="#f4f4f4",
        font=("Arial", 25, "bold")
    )

    canvas.create_text(
        left_col_x,
        title_y,
        text="معلومات مختلفة أخرى",
        fill="#f4f4f4",
        font=("Arial", 25, "bold")
    )

    field_w = int(width * 0.34)
    field_h = 60

    right_fields = [
        ("الاسم", "first_name"),
        ("اللقب", "last_name"),
        ("العنوان الكامل", "address"),
        ("رقم الهاتف", "phone"),
        ("رقم بطاقة التعريف", "id_card"),
    ]

    left_fields = [
        ("إلى السيد [ المدير / الجهة المستقبلة ]", "recipient"),
        ("المنصب المطلوب", "position"),
        ("الشهادة / المؤهلات", "degree"),
        ("التخصص", "specialty"),
        ("تاريخ الطلب", "date"),
        ("نوع الطلب", "request_type"),
    ]

    start_y = int(height * 0.16)
    gap = int(height * 0.115)

    for index, (placeholder, key) in enumerate(right_fields):
        make_placeholder_entry(right_col_x, start_y + index * gap, field_w, field_h, placeholder, key)

    for index, (placeholder, key) in enumerate(left_fields):
        y = start_y + index * gap

        if key == "date":
            make_placeholder_entry(left_col_x + 25, y, field_w - 60, field_h, placeholder, key)

            cal_box = rounded_rect(
                left_col_x - field_w // 2,
                y - field_h // 2,
                left_col_x - field_w // 2 + 58,
                y + field_h // 2,
                r=20,
                fill="#f3eeee",
                outline="#d9d1d1",
                width=2
            )

            cal_text = canvas.create_text(
                left_col_x - field_w // 2 + 29,
                y,
                text="📅",
                fill="#111111",
                font=("Arial", 28, "bold")
            )

            def open_cal(event):
                show_calendar_picker()

            for item in (cal_box, cal_text):
                canvas.tag_bind(item, "<Enter>", lambda e: root.config(cursor="hand2"))
                canvas.tag_bind(item, "<Leave>", lambda e: root.config(cursor=""))
                canvas.tag_bind(item, "<Button-1>", open_cal)

        elif key == "request_type":
            draw_request_type_field(left_col_x, y, field_w, field_h)

        else:
            make_placeholder_entry(left_col_x, y, field_w, field_h, placeholder, key)

    btn_y = int(height * 0.84)
    btn_w = 190
    btn_h = 62

    btn_center_x = int(width * 0.16)

    preview_btn = rounded_rect(
        btn_center_x - btn_w // 2,
        btn_y - btn_h // 2,
        btn_center_x + btn_w // 2,
        btn_y + btn_h // 2,
        r=30,
        fill="#f3eeee",
        outline="#d9d1d1",
        width=2
    )

    preview_text = canvas.create_text(
        btn_center_x,
        btn_y,
        text="معاينة",
        fill="#173b38",
        font=("Arial", 28, "bold")
    )

    def btn_enter(event):
        canvas.itemconfig(preview_btn, fill="#ffffff", outline="#ffffff")
        root.config(cursor="hand2")

    def btn_leave(event):
        canvas.itemconfig(preview_btn, fill="#f3eeee", outline="#d9d1d1")
        root.config(cursor="")

    def btn_click(event):
        show_job_request_preview()

    for item in (preview_btn, preview_text):
        canvas.tag_bind(item, "<Enter>", btn_enter)
        canvas.tag_bind(item, "<Leave>", btn_leave)
        canvas.tag_bind(item, "<Button-1>", btn_click)

    draw_back_button(show_written_request)


calendar_month = date.today().month
calendar_year = date.today().year


def show_calendar_picker():
    global current_page
    current_page = "calendar_picker"
    clear_screen()

    width = root.winfo_width()
    height = root.winfo_height()

    canvas.create_rectangle(0, 0, width, height, fill="#173b38", outline="#173b38")

    panel_x1 = int(width * 0.22)
    panel_x2 = int(width * 0.78)
    panel_y1 = int(height * 0.12)
    panel_y2 = int(height * 0.82)

    rounded_rect(
        panel_x1,
        panel_y1,
        panel_x2,
        panel_y2,
        r=30,
        fill="#1d1b24",
        outline="#4f83ff",
        width=3
    )

    month_name = calendar.month_name[calendar_month]

    canvas.create_text(
        width // 2,
        panel_y1 + 55,
        text=f"{month_name} {calendar_year}",
        fill="#f4f4f4",
        font=("Arial", 28, "bold")
    )

    prev_btn = canvas.create_text(panel_x1 + 70, panel_y1 + 55, text="‹", fill="#4f83ff", font=("Arial", 42, "bold"))
    next_btn = canvas.create_text(panel_x2 - 70, panel_y1 + 55, text="›", fill="#4f83ff", font=("Arial", 42, "bold"))

    def prev_month(event):
        global calendar_month, calendar_year
        calendar_month -= 1
        if calendar_month < 1:
            calendar_month = 12
            calendar_year -= 1
        show_calendar_picker()

    def next_month(event):
        global calendar_month, calendar_year
        calendar_month += 1
        if calendar_month > 12:
            calendar_month = 1
            calendar_year += 1
        show_calendar_picker()

    for item, cmd in [(prev_btn, prev_month), (next_btn, next_month)]:
        canvas.tag_bind(item, "<Enter>", lambda e: root.config(cursor="hand2"))
        canvas.tag_bind(item, "<Leave>", lambda e: root.config(cursor=""))
        canvas.tag_bind(item, "<Button-1>", cmd)

    days_header = ["Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"]
    grid_x1 = panel_x1 + 70
    grid_x2 = panel_x2 - 70
    col_w = (grid_x2 - grid_x1) // 7
    start_y = panel_y1 + 120
    row_h = 58

    for i, d in enumerate(days_header):
        canvas.create_text(
            grid_x1 + i * col_w + col_w // 2,
            start_y,
            text=d,
            fill="#d7c28a",
            font=("Arial", 14, "bold")
        )

    cal = calendar.Calendar(firstweekday=5)
    days = list(cal.itermonthdays(calendar_year, calendar_month))

    for index, day in enumerate(days):
        row = index // 7
        col = index % 7
        x = grid_x1 + col * col_w + col_w // 2
        y = start_y + 45 + row * row_h

        if day == 0:
            continue

        day_box = rounded_rect(
            x - 22,
            y - 20,
            x + 22,
            y + 20,
            r=12,
            fill="#f3eeee",
            outline="#f3eeee",
            width=1
        )

        day_text = canvas.create_text(
            x,
            y,
            text=str(day),
            fill="#111111",
            font=("Arial", 15, "bold")
        )

        def choose_day(event, selected_day=day):
            job_form_entries["date"] = f"{selected_day:02d}/{calendar_month:02d}/{calendar_year}"
            show_job_request_form()

        for item in (day_box, day_text):
            canvas.tag_bind(item, "<Enter>", lambda e: root.config(cursor="hand2"))
            canvas.tag_bind(item, "<Leave>", lambda e: root.config(cursor=""))
            canvas.tag_bind(item, "<Button-1>", choose_day)

    draw_back_button(show_job_request_form)

def scroll_job_form(event):
    global job_form_scroll

    if current_page != "job_request_form":
        return

    if event.delta < 0:
        job_form_scroll += 1
    else:
        job_form_scroll -= 1

    job_form_scroll = max(0, min(job_form_scroll, 6))
    show_job_request_form()


def show_job_request_preview():
    selected_type = job_form_entries.get("request_type", "").strip()

    if selected_type and selected_type != "طلب توظيف (عام)":
        try:
            messagebox.showinfo(
                "تنبيه",
                "حاليًا تم تجهيز نموذج Word لطلب توظيف (عام) فقط.\nسنضيف بقية النماذج واحدًا واحدًا لاحقًا."
            )
        except:
            pass

    try:
        output_path = create_job_request_word()
        open_generated_file(output_path)
    except Exception as e:
        try:
            messagebox.showerror("خطأ", f"تعذر إنشاء ملف Word:\n{e}")
        except:
            pass


def show_section(section):
    global current_page
    current_page = section
    clear_screen()

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_image(resource_path("assets/background.jpg"), width, height)

    titles = {
        "electronic": "خدمات إلكترونية",
        "archive": "أرشيف",
    }

    canvas.create_rectangle(
        int(width * 0.18),
        int(height * 0.22),
        int(width * 0.82),
        int(height * 0.72),
        fill="#173b38",
        outline="#d7c28a",
        width=2
    )

    canvas.create_text(
        width // 2,
        int(height * 0.34),
        text=titles.get(section, "صفحة"),
        fill="#f4f4f4",
        font=("Arial", 44, "bold")
    )

    canvas.create_text(
        width // 2,
        int(height * 0.50),
        text="سنقوم ببناء هذا القسم لاحقًا.",
        fill="#e8e1d5",
        font=("Arial", 24, "bold")
    )

    draw_back_button(show_home)


def show_about():
    global current_page
    current_page = "about"
    clear_screen()

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    draw_image(resource_path("assets/about.jpg"), width, height)

    draw_back_button(show_home)


def on_resize(event):
    if event.widget == root:
        if current_page == "home":
            show_home()
        elif current_page == "about":
            show_about()
        elif current_page == "documents":
            show_documents()
        elif current_page == "written_request":
            show_written_request()
        elif current_page == "written_request_template":
            show_written_request()
        elif current_page == "job_request_form":
            show_job_request_form()
        elif current_page == "job_request_preview":
            show_job_request_preview()
        elif current_page == "calendar_picker":
            show_calendar_picker()
        elif current_page in ["honor_statement", "cv", "invoice"]:
            show_document_type(current_page)
        else:
            show_section(current_page)



def on_request_type_key(event):
    if current_page != "job_request_form" or not request_type_dropdown_open:
        return

    if event.keysym == "Down":
        move_request_type_selection(1)
    elif event.keysym == "Up":
        move_request_type_selection(-1)
    elif event.keysym == "Return":
        confirm_request_type_selection()
    elif event.keysym == "Escape":
        close_request_type_dropdown()


root.bind("<Configure>", on_resize)
root.bind("<Up>", on_request_type_key)
root.bind("<Down>", on_request_type_key)
root.bind("<Return>", on_request_type_key)
root.bind("<Escape>", on_request_type_key)
root.bind("<MouseWheel>", lambda event: scroll_request_type_dropdown(1 if event.delta < 0 else -1) if (current_page == "job_request_form" and request_type_dropdown_open) else (scroll_job_form(event) if current_page == "job_request_form" else scroll_written_request(event)))

show_home()
root.mainloop()
