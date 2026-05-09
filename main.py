import tkinter as tk
from PIL import Image, ImageTk
import os
import sys


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
            font=("Arial", 28, "bold")
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


def show_job_request_form():
    global current_page, job_form_scroll, job_form_entries
    current_page = "job_request_form"
    clear_screen()

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    # Form background in the same identity colors
    canvas.create_rectangle(0, 0, width, height, fill="#121018", outline="#121018")

    panel_x1 = int(width * 0.08)
    panel_x2 = int(width * 0.92)
    panel_y1 = int(height * 0.04)
    panel_y2 = int(height * 0.84)

    canvas.create_rectangle(
        panel_x1,
        panel_y1,
        panel_x2,
        panel_y2,
        fill="#1d1b24",
        outline="#4f83ff",
        width=4
    )

    sections = [
        ("المعلومات الشخصية", [
            ("تاريخ الطلب", "date"),
            ("الاسم", "first_name"),
            ("اللقب", "last_name"),
            ("العنوان الكامل - المدينة", "address"),
            ("رقم الهاتف", "phone"),
            ("رقم بطاقة التعريف الوطنية", "id_card"),
        ]),
        ("معلومات مختلفة أخرى", [
            ("إلى السيد (المدير/الجهة المستقبلة/قابض البريد)", "recipient"),
            ("الرتبة المطلوبة / المنصب", "position"),
            ("الشهادة المتحصل عليها أو المستوى الدراسي", "degree"),
            ("التخصص", "specialty"),
        ])
    ]

    # Flatten fields for scrolling
    flattened = []
    for title, fields in sections:
        flattened.append(("__section__", title))
        for placeholder, key in fields:
            flattened.append((placeholder, key))

    visible_count = 6
    max_scroll = max(0, len(flattened) - visible_count)
    job_form_scroll = max(0, min(job_form_scroll, max_scroll))

    visible_items = flattened[job_form_scroll:job_form_scroll + visible_count]

    start_y = panel_y1 + 58
    row_h = int(height * 0.105)

    for index, (label, key) in enumerate(visible_items):
        y = start_y + index * row_h

        if key == label and label == "__section__":
            continue

        if label == "__section__":
            canvas.create_text(
                width // 2,
                y,
                text=key,
                fill="#f4f4f4",
                font=("Arial", 24, "bold")
            )
            continue

        entry_value = job_form_entries.get(key, "")

        entry_bg = canvas.create_rectangle(
            panel_x1 + 55,
            y - 10,
            panel_x2 - 55,
            y + 55,
            fill="#1d1b24",
            outline="#686874",
            width=2
        )

        entry = tk.Entry(
            root,
            font=("Arial", 20, "bold"),
            justify="right",
            bd=0,
            bg="#1d1b24",
            fg="#f4f4f4",
            insertbackground="#4f83ff"
        )

        entry.insert(0, entry_value)
        canvas.create_window(
            width // 2,
            y + 22,
            window=entry,
            width=panel_x2 - panel_x1 - 150,
            height=45
        )

        # Save on key release so scrolling does not lose values
        def save_entry(event, field_key=key, widget=entry):
            job_form_entries[field_key] = widget.get()

        entry.bind("<KeyRelease>", save_entry)

        placeholder_id = None
        if not entry_value:
            placeholder_id = canvas.create_text(
                panel_x2 - 85,
                y + 22,
                text=label,
                fill="#8d8b95",
                font=("Arial", 20, "bold"),
                anchor="e"
            )

            def focus_in(event, ph=placeholder_id):
                try:
                    canvas.itemconfig(ph, state="hidden")
                except:
                    pass

            def focus_out(event, ph=placeholder_id, widget=entry):
                if not widget.get().strip():
                    try:
                        canvas.itemconfig(ph, state="normal")
                    except:
                        pass

            entry.bind("<FocusIn>", focus_in)
            entry.bind("<FocusOut>", focus_out)

    if job_form_scroll > 0:
        canvas.create_text(
            width // 2,
            panel_y1 + 25,
            text="∧",
            fill="#4f83ff",
            font=("Arial", 28, "bold")
        )

    if job_form_scroll < max_scroll:
        canvas.create_text(
            width // 2,
            panel_y2 - 25,
            text="∨",
            fill="#4f83ff",
            font=("Arial", 28, "bold")
        )

    # Main button
    btn_x1 = panel_x1
    btn_x2 = panel_x2
    btn_y1 = int(height * 0.885)
    btn_y2 = int(height * 0.975)

    preview_btn = canvas.create_rectangle(
        btn_x1,
        btn_y1,
        btn_x2,
        btn_y2,
        fill="#2f6df0",
        outline="#2f6df0",
        width=2
    )

    preview_text = canvas.create_text(
        width // 2,
        (btn_y1 + btn_y2) // 2,
        text="معاينة و تعديل",
        fill="white",
        font=("Arial", 30, "bold")
    )

    def btn_enter(event):
        canvas.itemconfig(preview_btn, fill="#3f7dff", outline="#3f7dff")
        root.config(cursor="hand2")

    def btn_leave(event):
        canvas.itemconfig(preview_btn, fill="#2f6df0", outline="#2f6df0")
        root.config(cursor="")

    def btn_click(event):
        show_job_request_preview()

    for item in (preview_btn, preview_text):
        canvas.tag_bind(item, "<Enter>", btn_enter)
        canvas.tag_bind(item, "<Leave>", btn_leave)
        canvas.tag_bind(item, "<Button-1>", btn_click)

    draw_back_button(show_written_request)


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
    global current_page
    current_page = "job_request_preview"
    clear_screen()

    width = root.winfo_width()
    height = root.winfo_height()

    if width < 10 or height < 10:
        width, height = 1280, 720

    canvas.create_rectangle(0, 0, width, height, fill="#121018", outline="#121018")

    canvas.create_rectangle(
        int(width * 0.12),
        int(height * 0.10),
        int(width * 0.88),
        int(height * 0.82),
        fill="#1d1b24",
        outline="#4f83ff",
        width=3
    )

    canvas.create_text(
        width // 2,
        int(height * 0.18),
        text="معاينة طلب توظيف عام",
        fill="#f4f4f4",
        font=("Arial", 34, "bold")
    )

    full_name = f"{job_form_entries.get('first_name', '')} {job_form_entries.get('last_name', '')}".strip()

    preview = (
        f"الاسم واللقب: {full_name}\n"
        f"تاريخ الطلب: {job_form_entries.get('date', '')}\n"
        f"العنوان: {job_form_entries.get('address', '')}\n"
        f"رقم الهاتف: {job_form_entries.get('phone', '')}\n"
        f"رقم بطاقة التعريف: {job_form_entries.get('id_card', '')}\n\n"
        f"إلى: {job_form_entries.get('recipient', '')}\n"
        f"المنصب المطلوب: {job_form_entries.get('position', '')}\n"
        f"الشهادة / المستوى: {job_form_entries.get('degree', '')}\n"
        f"التخصص: {job_form_entries.get('specialty', '')}"
    )

    canvas.create_text(
        width // 2,
        int(height * 0.45),
        text=preview,
        fill="#e8e1d5",
        font=("Arial", 20, "bold"),
        justify="right",
        width=int(width * 0.65)
    )

    draw_back_button(show_job_request_form)


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
        elif current_page in ["honor_statement", "cv", "invoice"]:
            show_document_type(current_page)
        else:
            show_section(current_page)


root.bind("<Configure>", on_resize)
root.bind("<MouseWheel>", lambda event: scroll_job_form(event) if current_page == "job_request_form" else scroll_written_request(event))

show_home()
root.mainloop()
