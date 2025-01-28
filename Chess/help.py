import tkinter as tk

root = tk.Tk()


canvas = tk.Canvas(root, width=100, height=100, bg="white")
canvas.pack()


square_size = 50
x1, y1 = 10, 10
x2, y2 = x1 + square_size, y1 + square_size

# invisible rectangle
invisible_rect = canvas.create_rectangle(x1, y1, x2, y2, outline="", fill="")
# the visible rectangle
visible_rect = canvas.create_rectangle(
    x1, y1, x2, y2, outline="black", width=1)


def on_rectangle_click(event):
    print("Rectangle clickED")


canvas.tag_bind(invisible_rect, "<Button-1>", on_rectangle_click)

# Red circle
circle_raidus = 10
circle_x = (x1+x2)/2
circle_y = (y1+y2)/2
canvas.create_oval(
    circle_x - circle_raidus,
    circle_y - circle_raidus,
    circle_x + circle_raidus,
    circle_y + circle_raidus,
    fill='red',
    outline=""
)

a = [(3, 6), (3, 2), (3, 3)]
a = [(3, 7)]


# root.mainloop()
