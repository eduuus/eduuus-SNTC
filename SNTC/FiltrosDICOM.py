from tkinter import filedialog, ttk, Grid
import os
import numpy as np
import pydicom as dicom
import PIL.Image
import PIL.ImageTk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import cv2
from tkinter import *

#imgdicom = dicom.dcmread('/home/jailton/PycharmProjects/pythonProject1/case5/case5a_004.dcm')


# imgdicom2 = dicom.dcmread('/home/jailton/PycharmProjects/pythonProject1/case5/case5a_001.dcm')
# img = imgdicom.pixel_array


class Application(Frame):
    Cposition = 1
    Rposition = 0
    path = ''
    name = ''
    array = []

    def set_path(self, path1):
        self.path = path1
        return self.path

    def get_window(self, path1):
        self.path = path1
        return self.path

    def set_name(self, name1):
        self.name = name1
        return self.name

    def set_Cposition(self, Cposition):
        self.Cposition = Cposition
        return self.Cposition

    def set_Rposition(self, Rposition):
        self.Rposition = Rposition
        return self.Rposition

    def set_array(self, image_array):
        self.array = image_array
        return self.array

    def __init__(self):
        super().__init__()
        self.interface()

    def interface(self):
        self.master.title('Dicom')
        frame1 = Frame(self.master)
        frame1.grid(row=0, column=0, sticky='NW', pady=10)

        def open_files():

            files = file_path()
            self.images = tkinter_image(paths=files[0])
            for i in range(len(files[1])):
                Button(frame1, text=files[1][i], highlightthickness=0, image=self.images[i], compound=LEFT,
                       command=lambda j=i: plot(dicom_path=files[0][j], name=files[1][j])).grid(row=i, column=0,
                                                                                                sticky='NW')
                ttk.Separator(frame1, orient=VERTICAL).grid(column=1, row=i, ipadx=10, rowspan=1, sticky=E)

        def tkinter_image(paths):
            img = []
            for i in range(len(paths)):
                dicom_image = dicom.dcmread(paths[i])
                dicom_array = dicom_image.pixel_array
                PIL_image = PIL.Image.fromarray(dicom_array)
                PIL_image = PIL_image.resize((30, 30), PIL.Image.ANTIALIAS)
                print(PIL_image)
                print(type(PIL_image))
                self.image = PIL.ImageTk.PhotoImage(PIL_image)
                img.append(self.image)

            return img

        def plot(dicom_path=None, name=None):
            dicom_array = dicom.dcmread(dicom_path)
            dicom_image = dicom_array.pixel_array

            try:
                if dicom_image.shape[2] == 3:
                    print('plot')
                    dicom_image = dicom_image[:, :, 0]
            except:
                pass

            self.set_path(path1=dicom_path)
            self.set_name(name)
            self.set_array(dicom_image)

            f = Figure(figsize=(5.5, 5.5), dpi=80, frameon=False)

            plot1 = f.add_subplot(1, 1, 1)
            plot1.set_title(name)
            plot1.imshow(dicom_image)

            plot1.plot()

            Label(self.master, text='Original').grid(row=1,column=1,sticky='N')

            canvas = FigureCanvasTkAgg(f, self.master)
            canvas.draw()
            toolbar = NavigationToolbar2Tk(canvas, self.master, pack_toolbar=False)
            toolbar.grid(row=2, column=1)
            canvas.get_tk_widget().grid(row=0, column=1, sticky=W)

        def mediana(filter_size):
            temp = []
            data = self.array

            try:
                if data.shape[2] == 3:
                    print('mediana')
                    data = data[:, :, 0]
            except:
                pass

            indexer = filter_size // 2
            data_final = []
            data_final = np.zeros((len(data), len(data[0])))
            for i in range(len(data)):

                for j in range(len(data[0])):

                    for z in range(filter_size):
                        if i + z - indexer < 0 or i + z - indexer > len(data) - 1:
                            for c in range(filter_size):
                                temp.append(0)
                        else:
                            if j + z - indexer < 0 or j + indexer > len(data[0]) - 1:
                                temp.append(0)
                            else:
                                for k in range(filter_size):
                                    temp.append(data[i + z - indexer][j + k - indexer])
                    print(type(temp))
                    temp.sort()
                    data_final[i][j] = temp[len(temp) // 2]
                    temp = []

            f = Figure(figsize=(5.5, 5.5), dpi=80, frameon=False)

            plot1 = f.add_subplot(1, 1, 1)
            plot1.set_title(self.name)
            plot1.imshow(data_final)
            plot1.plot()
            Label(self.master, text='Filtro Mediana').grid(row=1, column=2, sticky='N')
            canvas = FigureCanvasTkAgg(f, self.master)
            canvas.draw()
            toolbar = NavigationToolbar2Tk(canvas, self.master, pack_toolbar=False)
            toolbar.grid(row=2, column=2)
            canvas.get_tk_widget().grid(row=0, column=2, sticky='E')

        def media():

            # janela = window_size.get()

            blur = cv2.blur(self.array, (7, 7))

            f = Figure(figsize=(5.5, 5.5), dpi=80, frameon=False)

            plot1 = f.add_subplot(1, 1, 1)
            plot1.set_title(self.name)
            plot1.imshow(blur)
            plot1.plot()
            Label(self.master, text='Filtro Média').grid(row=4, column=2, sticky='N')
            canvas = FigureCanvasTkAgg(f, self.master)
            canvas.draw()
            toolbar = NavigationToolbar2Tk(canvas, self.master, pack_toolbar=False)
            toolbar.grid(row=5, column=2)
            canvas.get_tk_widget().grid(row=3, column=2, sticky='E')


        def gaussiano(filter_size):


            image = self.array

            image = cv2.GaussianBlur(image, (7,7), 0)

            f = Figure(figsize=(5.5, 5.5), dpi=80, frameon=False)

            plot1 = f.add_subplot(1, 1, 1)
            plot1.set_title(self.name)
            plot1.imshow(image)
            plot1.plot()

            Label(self.master, text='Filtro Gaussiano').grid(row=4, column=1, sticky='N')

            canvas = FigureCanvasTkAgg(f, self.master)
            canvas.draw()
            toolbar = NavigationToolbar2Tk(canvas, self.master, pack_toolbar=False)
            toolbar.grid(row=5, column=1)
            canvas.get_tk_widget().grid(row=3, column=1, sticky='E')

        def onExit():
            self.quit()

        def file_path():
            paths = filedialog.askopenfilenames(
                initialdir='/home/usr', title='select a file', filetypes=(('dicom files', '*.dcm'),
                                                                          ('png files', '*.png'),
                                                                          ('all files', '*.*')))
            filenames = []
            for i in range(len(paths)):
                filenames.append(os.path.basename(paths[i]))
            return paths, filenames

        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        menu = Menu(menubar, tearoff=0)

        menu.add_command(label='Abrir Arquivos', command=open_files)

        menu.add_separator()
        menu.add_command(label='Sair', command=onExit)
        menubar.add_cascade(label='Arquivos', menu=menu)

        menu2 = Menu(menubar, tearoff=0)
        menu2.add_command(label='Filtro Mediana', command=lambda: mediana( filter_size=5))
        menu2.add_command(label='Filtro Média', command=lambda:media())
        menu2.add_command(label='Filtro Gaussiano', command=lambda: gaussiano(filter_size=5))
        menubar.add_cascade(label='Filtros', menu=menu2)


def main():
    root = Tk()
    root.geometry('300x400')
    Application()
    root.mainloop()


main()
