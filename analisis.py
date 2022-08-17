import tkinter
from turtle import width
from webbrowser import get
import pandas
import numpy
import statistics
import scipy.stats
from tkinter import ttk
from matplotlib import pyplot

# System Variables
abalone = pandas.read_csv("./abalone.csv")

columns = (
    "Sex",
    "Length",
    "Diameter",
    "Height",
    "Whole-weight",
    "Shucked-weight",
    "Viscera-weight",
    "Shell-weight",
    "Rings"
)
numeric_columns = (
    "Length",
    "Diameter",
    "Height",
    "Whole-weight",
    "Shucked-weight",
    "Viscera-weight",
    "Shell-weight",
    "Rings"
)
scatter_columns = (
    "Length",
    "Diameter",
    "Height"
)
vs_columns = (
    "Whole-weight",
    "Shucked-weight",
    "Viscera-weight",
    "Shell-weight",
    "Rings"
)

def remover_atipicos():
    nuevo = abalone.copy()
    filas_atipicas = set()
    for column in numeric_columns:
        column_data = abalone[column]
        q1 = numpy.percentile(column_data, 25)
        q3 = numpy.percentile(column_data, 75)
        iqr = q3 - q1
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr
        for index, value in enumerate(column_data):
            if value < limite_inferior or limite_superior < value:
                filas_atipicas.add(index)
    filas_atipicas = list(filas_atipicas)
    filas_atipicas.sort()
    nuevo = nuevo.drop(index=filas_atipicas)
    return nuevo

sin_atipicos = remover_atipicos()

# UI Variables
app = tkinter.Tk()
remover_atipicos_var = tkinter.IntVar()
hist_column = tkinter.StringVar()
boxplot_column = tkinter.StringVar()
normal_dist_column = tkinter.StringVar()
probplot_column = tkinter.StringVar()
scatter_column = tkinter.StringVar()
scatter_vs_column = tkinter.StringVar()
## Conclusiones
conclusiones_column = tkinter.StringVar()
media_variable = tkinter.StringVar()
mediana_variable = tkinter.StringVar()
moda_variable = tkinter.StringVar()
kurtosis_variable = tkinter.StringVar()

mmm_conclusion = tkinter.StringVar()
k_conclusion = tkinter.StringVar()


def get_data():
    if remover_atipicos_var.get():
        return sin_atipicos
    return abalone


def correlation():
    data = get_data()
    # Correlation
    fig, ax = pyplot.subplots()
    cax = ax.matshow(data.corr())
    fig.colorbar(cax)
    ax.set_xticklabels(['']+data.columns, rotation='vertical')
    ax.set_yticklabels(['']+data.columns)
    pyplot.show()
    pyplot.cla()
    pyplot.clf()


def histogram():
    column_name = hist_column.get()
    column = get_data()[column_name]
    # Historgram
    pyplot.hist(column)
    pyplot.show()
    pyplot.cla()
    pyplot.clf()


def boxplot():
    column_name = boxplot_column.get()
    column = get_data()[column_name]
    # Boxplot
    pyplot.boxplot(column)
    pyplot.show()
    pyplot.cla()
    pyplot.clf()


def normal_distribution():
    column_name = normal_dist_column.get()
    column = get_data()[column_name]
    # Normal distribution
    mean = numpy.mean(column)
    std = numpy.std(column)
    x = sorted(list(set(column)))
    normal = scipy.stats.norm.pdf(x, mean, std)
    pyplot.plot(x, normal, )
    pyplot.show()
    pyplot.cla()
    pyplot.clf()


def probability_plot():
    column_name = probplot_column.get()
    column = get_data()[column_name]
    # Probability plot
    fig = pyplot.figure()
    ax = fig.add_subplot(111)
    scipy.stats.probplot(column, dist=scipy.stats.norm,plot=ax)
    pyplot.show()
    pyplot.cla()
    pyplot.clf()


def scatter():
    target_data = get_data()
    column_name = scatter_column.get()
    column = target_data[column_name]
    vs_name = scatter_vs_column.get()
    vs_column = target_data[vs_name]
    # Scatter
    # fig = pyplot.figure()
    pyplot.title(f"Scatter: {column_name} vs {vs_column}")
    # ax = fig.add_subplot(111)
    pyplot.scatter(column, vs_column)
    pyplot.show()
    pyplot.close()
    pyplot.cla()
    pyplot.clf()


def calc():
    data = get_data()[conclusiones_column.get()]
    # Media
    mean = numpy.mean(data)
    media_variable.set(f"{mean}")
    # Mediana
    median = statistics.median(data)
    mediana_variable.set(f"{median}")
    # Moda
    mode = statistics.mode(data)
    moda_variable.set(f"{mode}")
    # Kurtosis
    k = scipy.stats.kurtosis(data)
    kurtosis_variable.set(f"{k}")
    # Conclusiones
    ## Media, mediana y moda
    if mode < median < mean:
        mmm_conclusion.set("Sesgada a la Izquierda") # Izquierda
    elif mode > median > mean:
        mmm_conclusion.set("Sesgada a la Derecha")  # Derecha
    # Curtosis
    if k == 0:
        k_conclusion.set("Mesocurtica")  # Mesocurtica
    elif k > 0:
        k_conclusion.set("Leptocurtica") # Leptocurtica
    else: # k < 0
        k_conclusion.set("Platicurtica") # Platicurtica


def main():    
    # APP
    app.geometry("500x800")
    # Atipicos
    ttk.Checkbutton(app, text="Remover atipicos", variable=remover_atipicos_var).pack()
    ttk.Separator(app).pack(fill='x')
    # Histograma
    tkinter.Label(app, text="Histograma").pack()
    ttk.Combobox(app, values=columns, textvariable=hist_column).pack()
    tkinter.Button(app, text="Graph", command=histogram).pack()
    ttk.Separator(app).pack(fill='x')
    # Box plot
    tkinter.Label(app, text="Boxplot").pack()
    ttk.Combobox(app, values=numeric_columns, textvariable=boxplot_column).pack()
    tkinter.Button(app, text="Graph", command=boxplot).pack()
    ttk.Separator(app).pack(fill='x')
    # Normal distribution
    tkinter.Label(app, text="Distribucion normal").pack()
    ttk.Combobox(app, values=numeric_columns, textvariable=normal_dist_column).pack()
    tkinter.Button(app, text="Graph", command=normal_distribution).pack()
    ttk.Separator(app).pack(fill='x')
    # Probability plot
    tkinter.Label(app, text="Probability plot").pack()
    ttk.Combobox(app, values=numeric_columns, textvariable=probplot_column).pack()
    tkinter.Button(app, text="Graph", command=probability_plot).pack()
    ttk.Separator(app).pack(fill='x')
    # Correlation
    tkinter.Label(app, text="Correlation plot").pack()
    tkinter.Button(app, text="Graph", command=correlation).pack()
    ttk.Separator(app).pack(fill='x')
    # Scatter
    tkinter.Label(app, text="Scatter").pack()
    ttk.Combobox(app, values=scatter_columns, textvariable=scatter_column).pack()
    tkinter.Label(app, text="VS:").pack()
    ttk.Combobox(app, values=vs_columns, textvariable=scatter_vs_column).pack()
    tkinter.Button(app, text="Graph", command=scatter).pack()
    ttk.Separator(app).pack(fill='x')
    # Media, Mediana, Moda, Kurtosis
    ttk.Combobox(app, values=numeric_columns, textvariable=conclusiones_column).pack()
    tkinter.Button(app, text="Calc", command=calc).pack()
    ttk.Separator(app).pack(fill='x')
    ## Media
    tkinter.Label(app, text="Media").pack()
    tkinter.Label(app, textvariable=media_variable).pack()
    ttk.Separator(app).pack(fill='x')
    ## Mediana
    tkinter.Label(app, text="Mediana").pack()
    tkinter.Label(app, textvariable=mediana_variable).pack()
    ttk.Separator(app).pack(fill='x')
    ## Moda
    tkinter.Label(app, text="Moda").pack()
    tkinter.Label(app, textvariable=moda_variable).pack()
    ttk.Separator(app).pack(fill='x')
    ## Kurtosis
    tkinter.Label(app, text="Kurtosis").pack()
    tkinter.Label(app, textvariable=kurtosis_variable).pack()
    ttk.Separator(app).pack(fill='x')
    # Conclusiones
    tkinter.Label(app, text="Conclusiones").pack()
    tkinter.Label(app, textvariable=mmm_conclusion).pack()
    tkinter.Label(app, textvariable=k_conclusion).pack()
    # Mainloop
    app.mainloop()


if __name__ == "__main__":
    main()