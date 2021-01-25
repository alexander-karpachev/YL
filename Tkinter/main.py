import tkinter


canvas = None
oval = None


def key_pressed(event):
    canvas.move(oval, 10, 10)


def main():
    master = tkinter.Tk()
    canvas = tkinter.Canvas(master, bg='blue', height=600, width=600)
    oval = canvas.create_oval((300, 300), (310, 310), fill='red')
    canvas.pack()
    master.bind("<KeyPress>", key_pressed)
    master.mainloop()


if __name__ == '__main__':
    main()
