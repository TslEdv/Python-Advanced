import tkinter
from triangle_package_edvess import triangle


def main():
    window = tkinter.Tk()
    window.title("Triangle area calculator")
    window.geometry('350x200')

    tkinter.Label(window, text='Base').grid(row=0)
    tkinter.Label(window, text='Height').grid(row=1)
    tkinter.Label(window, text='Value').grid(row=2)

    txt = tkinter.Entry(window, width=15)
    txt.grid(column=1, row=0)
    txt.focus()

    txt2 = tkinter.Entry(window, width=15)
    txt2.grid(column=1, row=1)

    txt3 = tkinter.Entry(window, width=20)
    txt3.grid(column=1, row=2)

    def clicked():
        txt3.delete(0, tkinter.END)
        try:
            if float(txt.get()) < 0 or float(txt2.get()) < 0:
                txt3.insert(0, "No negative values!")
            else:
                txt3.insert(0, triangle.triangle_area(float(txt.get()), float(txt2.get())))
        except ValueError:
            txt3.insert(0, "Incorrect Inputs!")

    btn = tkinter.Button(window, text="Calculate", command=clicked)
    btn.grid(column=0, row=3)

    window.mainloop()


if __name__ == '__main__':
    main()
