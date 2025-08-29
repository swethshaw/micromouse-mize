import tkinter as tk
from tkinter import messagebox
from collections import deque

WIDTH, HEIGHT = 0, 0
CELL_SIZE = 0
start_point = None
end_point = None
visited_original_values = {}
maze = None

button_options = {
        "font": ("Helvetica", 12, "bold"),
        "bg": "#4CAF50",
        "fg": "white",
        "activebackground": "#45a049",
        "activeforeground": "black",
        "width": 15,
        "height": 2,
        "bd": 3,
        "relief": "raised",
        "padx": 10,
        "pady": 5
    }

def initialize_maze():
    return [["white" if 0 < row < HEIGHT - 1 and 0 < col < WIDTH - 1 else "black"
             for col in range(WIDTH)] for row in range(HEIGHT)]

def start_main_app():
    global maze, canvas, start_point, end_point, visited_original_values, WIDTH, HEIGHT, CELL_SIZE,frame

    width_value = width_input.get()
    height_value = height_input.get()

    # Validate the inputs
    if not width_value or not height_value:
        messagebox.showerror("Input Error", "Width and Height cannot be empty.")
        return

    try:
        WIDTH = int(width_value)
        HEIGHT = int(height_value)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values for width and height.")
        return

    if WIDTH <= 2 or HEIGHT <= 2:
        messagebox.showerror("Input Error", "Width and Height must be larger than 2.")
        return

    maze = initialize_maze()

    frame.pack_forget()
    canvas = tk.Canvas(root, width=600, height=600)
    canvas.pack()
    CELL_SIZE = 600 // max(WIDTH, HEIGHT)

    def draw_maze():
        canvas.delete("all")
        for row in range(HEIGHT):
            for col in range(WIDTH):
                color = maze[row][col]
                if isinstance(color, int):
                    canvas.create_rectangle(col * CELL_SIZE, row * CELL_SIZE,
                                            (col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE,
                                            fill="white", outline="gray")
                    text_color = "green" if (row, col) == start_point or maze[row][col] == "visited" else "red"
                    canvas.create_text(col * CELL_SIZE + CELL_SIZE // 2,
                                       row * CELL_SIZE + CELL_SIZE // 2,
                                       text=str(color), fill=text_color)
                elif color == "visited":
                    canvas.create_rectangle(col * CELL_SIZE, row * CELL_SIZE,
                                            (col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE,
                                            fill="white", outline="gray")

                    original_value = visited_original_values.get((row, col), "")
                    canvas.create_text(col * CELL_SIZE + CELL_SIZE // 2,
                                       row * CELL_SIZE + CELL_SIZE // 2,
                                       text=str(original_value), fill="green")
                elif color == "green":
                    canvas.create_rectangle(col * CELL_SIZE, row * CELL_SIZE,
                                            (col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE,
                                            fill="green", outline="gray")
                    canvas.create_text(col * CELL_SIZE + CELL_SIZE // 2,
                                       row * CELL_SIZE + CELL_SIZE // 2,
                                       text="Reached", fill="blue")
                else:
                    canvas.create_rectangle(col * CELL_SIZE, row * CELL_SIZE,
                                            (col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE,
                                            fill=color, outline="gray")

        if start_point:
            row, col = start_point
            canvas.create_rectangle(col * CELL_SIZE, row * CELL_SIZE,
                                    (col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE,
                                    fill="red", outline="gray")
            canvas.create_text(col * CELL_SIZE + CELL_SIZE // 2,
                               row * CELL_SIZE + CELL_SIZE // 2,
                               text="Start", fill="blue")

        if end_point:
            row, col = end_point
            canvas.create_rectangle(col * CELL_SIZE, row * CELL_SIZE,
                                    (col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE,
                                    fill="green", outline="gray")
            canvas.create_text(col * CELL_SIZE + CELL_SIZE // 2,
                               row * CELL_SIZE + CELL_SIZE // 2,
                               text="Finish", fill="blue")

    def toggle_cell(event):
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        if 0 < row < HEIGHT - 1 and 0 < col < WIDTH - 1:
            if maze[row][col] == "white":
                maze[row][col] = "black"
            elif maze[row][col] == "black":
                maze[row][col] = "white"
            draw_maze()

    def set_start_point():
        def on_click(event):
            col = event.x // CELL_SIZE
            row = event.y // CELL_SIZE
            if maze[row][col] == "white" and maze[row][col] != "blue":
                global start_point
                if start_point:
                    maze[start_point[0]][start_point[1]] = "white"
                start_point = (row, col)
                maze[row][col] = "red"
                draw_maze()
                canvas.unbind("<Button-1>")
            else:
                messagebox.showwarning("Warning", "Please click on any white box!")
            btn_set_start.config(state=tk.DISABLED)

        canvas.bind("<Button-1>", on_click)

    def set_end_point():
        def on_click(event):
            col = event.x // CELL_SIZE
            row = event.y // CELL_SIZE
            if maze[row][col] == "white" and maze[row][col] != "red":
                global end_point
                if end_point:
                    maze[end_point[0]][end_point[1]] = "white"
                end_point = (row, col)
                maze[row][col] = "blue"
                draw_maze()
                canvas.unbind("<Button-1>")
            else:
                messagebox.showwarning("Warning", "Please click on any white box!")

            btn_set_end.config(state=tk.DISABLED)

        canvas.bind("<Button-1>", on_click)

    def flood_fill_number(x, y):
        queue = deque([(x, y, 0)])
        visited = set()
        while queue:
            cx, cy, number = queue.popleft()
            if (cx, cy) in visited or maze[cx][cy] == "black":
                continue
            if (cx, cy) == start_point:
                maze[cx][cy] = "red"
                draw_maze()
                break
            elif (cx, cy) == end_point:
                maze[cx][cy] = 0
            else:
                maze[cx][cy] = number
            draw_maze()
            root.update_idletasks()
            visited.add((cx, cy))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < HEIGHT and 0 <= ny < WIDTH and (nx, ny) not in visited:
                    queue.append((nx, ny, number + 1))

    def move_mouse(x, y):
        global end_point
        if maze[x][y] == 0:
            maze[x][y] = "green"
            draw_maze()
            root.update_idletasks()
            end_point = None
            draw_maze()
            messagebox.showinfo("Destination Reached",
                                "The mouse reached its destination (Chill Guy got his coffee)")  # Show the message
            return

        if (x, y) != start_point:
            if (x, y) not in visited_original_values:
                visited_original_values[(x, y)] = maze[x][y]
            maze[x][y] = "visited"
            draw_maze()
            root.update_idletasks()

        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        min_value = min(
            int(maze[nx][ny]) for nx, ny in neighbors
            if maze[nx][ny] != "black" and isinstance(maze[nx][ny], int)
        )
        for nx, ny in neighbors:
            if maze[nx][ny] != "black" and isinstance(maze[nx][ny], int) and maze[nx][ny] == min_value:
                root.after(200, move_mouse, nx, ny)
                break

    def start_flood_fill():
        if not end_point:
            messagebox.showwarning("Warning", "Please set the end point!")
        if not start_point:
            messagebox.showwarning("Warning", "Please set the start point!")
            return
        flood_fill_number(end_point[0], end_point[1])

    def start_mouse_movement():
        global start_point
        global end_point

        if not start_point or not end_point:
            messagebox.showwarning("Warning", "Please set both start and end points!")
            return
        btn_flood_fill.config(state=tk.DISABLED)
        btn_start_mouse.config(state=tk.DISABLED)
        temp_start = start_point
        draw_maze()
        move_mouse(temp_start[0], temp_start[1])

    def restart_maze():
        global start_point, end_point, visited_original_values, maze
        start_point = None
        end_point = None
        visited_original_values = {}
        maze = initialize_maze()
        draw_maze()
        canvas.bind("<Button-1>", toggle_cell)
        btn_set_start.config(state=tk.NORMAL)
        btn_set_end.config(state=tk.NORMAL)
        btn_flood_fill.config(state=tk.NORMAL)
        btn_start_mouse.config(state=tk.NORMAL)

    frame = tk.Frame(root)
    frame.pack(pady=10)

    btn_set_start = tk.Button(frame, text="Set Start Point", command=set_start_point, **button_options)
    btn_set_start.grid(row=0, column=0, padx=5, pady=10)

    btn_set_end = tk.Button(frame, text="Set End Point", command=set_end_point, **button_options)
    btn_set_end.grid(row=0, column=2, padx=5, pady=10)

    btn_flood_fill = tk.Button(frame, text="Start Flood Fill", command=start_flood_fill, **button_options)
    btn_flood_fill.grid(row=1, column=0, padx=5, pady=10)

    btn_start_mouse = tk.Button(frame, text="Start Mouse Movement", command=start_mouse_movement, **button_options)
    btn_start_mouse.grid(row=1, column=2, padx=5, pady=10)

    btn_restart = tk.Button(frame, text="Restart", command=restart_maze, **button_options)
    btn_restart.grid(row=2, column=1, padx=5, pady=10)

    canvas.bind("<Button-1>", toggle_cell)

    draw_maze()

root = tk.Tk()
root.title("Micromouse Maze Solver with Flood Fill Algorithm")
root.minsize(600, 800)
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Width:").grid(row=0, column=0, padx=5, pady=5)
width_input = tk.Entry(frame)
width_input.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Height:").grid(row=1, column=0, padx=5, pady=5)
height_input = tk.Entry(frame)
height_input.grid(row=1, column=1, padx=5, pady=5)



tk.Button(frame, text="start", command=start_main_app, **button_options).grid(row=2, column=0, columnspan=2, pady=10)
root.mainloop()


