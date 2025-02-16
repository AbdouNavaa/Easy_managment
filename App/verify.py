# import tkinter as tk
# from tkinter import messagebox

# def on_button_click():
#     label.config(text="تم النقر على الزر!")

# def on_key_press(event):
#     label.config(text=f"تم الضغط على المفتاح: {event.char}")

# def on_mouse_enter(event):
#     label.config(text="الفأرة فوق الزر!")

# def on_mouse_leave(event):
#     label.config(text="الفأرة خارج الزر!")

# def on_window_close():
#     if messagebox.askyesno("إغلاق", "هل تريد حقًا إغلاق النافذة؟"):
#         root.destroy()

# # إنشاء نافذة
# root = tk.Tk()
# root.title("أحداث متعددة")

# # إضافة عنصر Label
# label = tk.Label(root, text="جرب الأحداث المختلفة")
# label.pack(pady=20)

# # إضافة عنصر Button
# button = tk.Button(root, text="انقر هنا", command=on_button_click)
# button.pack(pady=10)

# # ربط أحداث الفأرة
# button.bind("<Enter>", on_mouse_enter)
# button.bind("<Leave>", on_mouse_leave)

# # ربط حدث الضغط على مفتاح
# root.bind("<Key>", on_key_press)

# # ربط حدث إغلاق النافذة
# root.protocol("WM_DELETE_WINDOW", on_window_close)

# # تشغيل النافذة
# root.mainloop()