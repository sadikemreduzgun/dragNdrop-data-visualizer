import time
import tkinter
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from tkinter import messagebox


class DataFrameVisualizer:

    def __init__(self):
        self.created = False

        self.button_font = 15
        self.img_x = 1280
        self.img_y = 600

        self.res_opts = ["400x300", "600x450", "720x480", "800x520", "800x600", "1280x600", "1280x620", "1280x720"]
        self.columns = []
        self.root = TkinterDnD.Tk()

        self.root.title("Dosya Görselleştirici")
        self.root.geometry("1280x720")
        # '#856ff8'
        self.root['background'] = '#cdc1c5'
        # #FF1493'
        """self.text_widget = tk.Text(self.root, wrap=tk.WORD, bg='#FF1493')
        self.text_widget.insert(tk.END, "Please drop your csv file on me.")
        self.text_widget.config(state=tk.DISABLED)"""

        # fill=tk.BOTH, expand=True
        # self.text_widget.pack()

        self.container = tk.Frame(self.root, bg='#FFFFE0')  # Lila renkli arka plan
        self.container.pack(fill=tk.BOTH, expand=True)

        self.text_widget = tk.Label(self.container, text="➥\n Please drop your csv file on me. ", wraplength=500, font=("Arial", 18, "bold"),
                                    bg='#eee0e5', fg='black')
        self.text_widget.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.text_widget.drop_target_register(DND_FILES)
        self.text_widget.dnd_bind('<<Drop>>', self.handle_drop)

        # Hover effect eklemek için olay bağlamaları
        self.text_widget.bind("<Enter>", self.on_enter)
        self.text_widget.bind("<Leave>", self.on_leave)

        # self.text_widget.drop_target_register(DND_FILES)
        #self.text_widget.dnd_bind('<<Drop>>', self.handle_drop)

        self.back_button = tk.Button(text="Go Back", command=self.go_back, bg='blue', fg='white')
        self.back_button_initial = tk.Button(text="Go Back", command=self.handle_change_csv, bg='blue', fg='white')

        self.stvar_x = tk.StringVar(self.root, "index or x axis")
        self.stvar_y = tk.StringVar(self.root, "y axis")

        self.stvar_res = tk.StringVar(self.root, f"{self.img_x}x{self.img_y}")

        self.stvar_hue = tk.StringVar(self.root, "empty hue")
        self.hue = ""

        self.stvar_data_num = tk.StringVar(self.root, "2")
        self.datanum = list(range(1,21))
        self.one_data_num = 2

        self.stvar_charts = tk.StringVar(self.root, "Chart")

        self.x_ax = "counter"
        self.y_ax = ""
        self.plots_2_data = ["pairplot", "relplot", "lmplot", "displot", "jointplot", "boxplot", "lineplot"]
        self.selected_chart = "pairplot"

    def on_enter(self, event):
        self.text_widget.config(bg='#cdc1c5')  # Arka plan rengini maviye değiştir

    def on_leave(self, event):
        self.text_widget.config(bg='#eee0e5')  # Arka plan rengini tekrar pembe yap

    def change_datanum(self, selection):
        self.one_data_num = int(selection)

    def handle_res(self, selection: str):
        self.img_x = int(selection.split("x")[0])
        self.img_y = int(selection.split("x")[1])
        self.stvar_res = tk.StringVar(self.root, f"{self.img_x}x{self.img_y}")

    def set_hue(self, selection):
        self.hue = selection

    def set_x(self, selection):
        self.x_ax = selection

    def set_y(self, selection):
        print(selection)
        self.y_ax = selection

    def handle_vis(self):
        self.option_y.pack_forget()
        self.option_x.pack_forget()
        self.option_button.pack_forget()
        # self.num_label.pack_forget()
        self.option_charts.pack_forget()
        # self.option_hue.pack_forget()
        self.option_data_num.pack_forget()
        self.option_image.pack_forget()
        self.back_button_initial.pack_forget()

        plot_path = self.create_seaborn_plot(self.df)
        self.display_plot(plot_path)

    def handle_change_csv(self):

        self.option_y.pack_forget()
        self.option_x.pack_forget()
        self.option_button.pack_forget()
        # self.num_label.pack_forget()
        self.option_charts.pack_forget()
        # self.option_hue.pack_forget()
        self.option_data_num.pack_forget()
        self.option_image.pack_forget()
        self.back_button_initial.pack_forget()
        # self.container.pack(fill=tk.BOTH, expand=True)
        self.container.pack(fill=tk.BOTH, expand=True)
        self.text_widget.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    """def set_charts(self):
        self.plots_2_data = {"pairplot": sns.pairplot(self.df[[self.x_ax, self.y_ax]]),
                        "relplot": sns.relplot(data=self.df[[self.x_ax, self.y_ax]]),
                        "lmplot": sns.lmplot(data=self.df, x=self.x_ax, y=self.y_ax),
                        "displot": sns.displot(data=self.df, x=self.x_ax, y=self.y_ax),
                        "ecdf displot": sns.displot(data=self.df, x=self.x_ax, y=self.y_ax, kind="ecdf"),
                        "jointplot": sns.jointplot(data=self.df, x=self.x_ax, y=self.y_ax),
                        "boxplot": sns.boxplot(data=self.df, x=self.x_ax, y=self.y_ax, dodge=True)
                        }"""

    def select_chart(self, selection):
        self.selected_chart = selection

    def back_first_page(self):

        self.back_button_initial.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)
        self.option_image.pack(side=tk.TOP, pady=20)
        self.option_button.pack(side=tk.BOTTOM, pady=10)

        # self.option_hue.pack(side=tk.BOTTOM, pady=10)

        self.option_data_num.pack(side=tk.BOTTOM, pady=5)

        # self.num_label.pack(side=tk.BOTTOM)
        self.option_charts.pack(side=tk.BOTTOM, pady=5)

        self.option_y.pack(side=tk.LEFT, padx=20)
        self.option_x.pack(side=tk.RIGHT, padx=20)
        # self.set_charts()

    def handle_drop(self, event):
        file = event.data

        if file:
            try:

                self.df = pd.read_csv(file)
            except:
                messagebox.showerror(title="file error", message="please give me a csv file")
                exit(1)

            self.df["counter"] = list(range(1, len(self.df)+1))

            self.text_widget.pack_forget()

            self.columns = self.df.columns
            self.columns = self.columns.insert(0, "power")
            self.columns = self.columns.insert(0, "counter")

            # no categorical
            # 2 data
            self.root.update_idletasks()
            self.root_width = self.root.winfo_width()

            self.back_button_initial.pack(side=tk.TOP, anchor=tk.NW, pady=5, padx=5)

            self.option_image = tk.OptionMenu(self.root, self.stvar_res, *self.res_opts, command=self.handle_res)
            self.option_image.config(bg='black', fg='white', font=("Arial", self.button_font, "bold"))
            self.option_image.pack(side=tk.TOP, pady=60)

            self.option_button = tk.Button(text="Next", command=self.handle_vis)
            self.option_button.config(bg='blue', fg='white', font=("Arial", self.button_font, "bold"))
            self.option_button.pack(side=tk.BOTTOM, pady=60)

            self.option_hue = tk.OptionMenu(self.root, self.stvar_hue, *self.columns)
            self.option_hue.config(bg='orange', fg='white', font=("Arial", self.button_font, "bold"))
            # self.option_hue.pack(side=tk.BOTTOM, pady=10)

            # func yaz
            self.option_data_num = tk.OptionMenu(self.root, self.stvar_data_num, *self.datanum, command=self.change_datanum)
            self.option_data_num.config(bg='#ADD8E6', fg='black', font=("Arial", self.button_font, "bold"))
            self.option_data_num.pack(side=tk.BOTTOM, pady=5)

            self.num_label = tk.Label(text="Column Number")
            self.num_label.config(bg='#ADD8E6', fg='white', font=("Arial", self.button_font, "bold"))
            # self.num_label.pack(side=tk.BOTTOM)

            # self.set_charts()
            self.option_charts = tk.OptionMenu(self.root, self.stvar_charts, *self.plots_2_data, command=self.select_chart)
            self.option_charts.config(bg='#ADD8E6', fg='black', font=("Arial", self.button_font, "bold"))
            self.option_charts.pack(side=tk.BOTTOM, pady=50)

            self.option_y = tk.OptionMenu(self.root, self.stvar_y, *self.columns, command=self.set_y)
            self.option_y.config(bg='#ADD8E6', fg='black', font=("Arial", self.button_font, "bold"))
            self.option_y.pack(padx=70, side='left') # side=tk.LEFT,
            #self.option_y.place(x=self.root_width+100)

            self.option_x = tk.OptionMenu(self.root, self.stvar_x, *self.columns, command=self.set_x)
            self.option_x.config(bg='#ADD8E6', fg='black', font=("Arial", self.button_font, "bold"))
            self.option_x.pack(padx=70, side='right')
            # self.option_x.place(x=self.root_width-100)

            self.container.pack_forget()

    def set_labels(self, plot, joint=False):
        if self.x_ax == "counter":
            title = self.y_ax + " over time"
            xlabel = "time"
        else:
            title = self.x_ax + " vs. " + self.y_ax
            xlabel = self.x_ax

        # plot = plt.tight_layout()

        if joint:
            # Change the labels of the axes
            plot.set_axis_labels(xlabel, self.y_ax)
            # Set the title
            plot.fig.suptitle(title, y=1.02)  # Adjust y position for title
        else:
            plot.set(title=title, xlabel=xlabel, ylabel=self.y_ax)

        return plot

    def create_seaborn_plot(self, dataframe):

        sns.set(style="whitegrid")

        plots_2_data_h = []

        # dont want to invoke charts so commented out
        """plots = {"pairplot": sns.pairplot(self.df[[self.x_ax, self.y_ax]]),
                             "relplot": sns.relplot(data=self.df[[self.x_ax, self.y_ax]]),
                             "lmplot": sns.lmplot(data=self.df, x=self.x_ax, y=self.y_ax),
                             "displot": sns.displot(data=self.df, x=self.x_ax, y=self.y_ax),
                             "jointplot": sns.jointplot(data=self.df, x=self.x_ax, y=self.y_ax),
                             "boxplot": sns.boxplot(data=self.df, x=self.x_ax, y=self.y_ax, dodge=True)}"""

        if not self.x_ax:
            self.x_ax = 'counter'

        if self.x_ax == 'index':
            self.x_ax = 'counter'

        if self.y_ax == 'index':
            self.y_ax = 'counter'

        # there was no better way below
        if self.selected_chart == "pairplot":
            plot = sns.pairplot(dataframe[[self.x_ax, self.y_ax]])
            plot = self.set_labels(plot)
        elif self.selected_chart == "relplot":
            plot = sns.relplot(data=dataframe[[self.x_ax, self.y_ax]])
            plot = self.set_labels(plot)

        elif self.selected_chart == "lmplot":
            plot = sns.lmplot(data=dataframe, x=self.x_ax, y=self.y_ax)
            plot = self.set_labels(plot)
        elif self.selected_chart == "displot":
            plot = sns.displot(data=dataframe, x=self.x_ax, y=self.y_ax)
            plot = self.set_labels(plot)
        elif self.selected_chart == "jointplot":
            plot = sns.jointplot(data=dataframe, x=self.x_ax, y=self.y_ax)
            # plot = self.set_labels(plot)
            self.set_labels(plot, joint=True)
        elif self.selected_chart == "boxplot":
            plot = sns.boxplot(dataframe[self.y_ax])
            plot = self.set_labels(plot)
            plot = plot.get_figure()
        elif self.selected_chart == "lineplot":
            plot = sns.lineplot(data=dataframe, x=self.x_ax, y=self.y_ax)
            # Create a Figure object
            plot = self.set_labels(plot)
            # plt.figure(figsize=(6, 3))
            plot = plot.get_figure()

        # plot = plots[self.selected_chart]
        # plot = sns.pairplot(dataframe[[self.x_ax, self.y_ax]])

        # plt.show()
        plot_path = "seaborn_plot.png"

        print("saved")
        # plt.figure(figsize=(4,2))
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        # plt.show()
        plt.tight_layout()
        plt.savefig(plot_path, bbox_inches='tight', dpi=100)
        plt.close()

        return plot_path

    def display_plot(self, plot_path):

        img = Image.open(plot_path)
        img = img.resize((self.img_x, self.img_y))  # Use Image.ANTIALIAS directly
        img_tk = ImageTk.PhotoImage(img)
        img.close()
        self.text_widget.pack_forget()
        self.label = tk.Label(self.root, image=img_tk)
        self.label.config(bg='#856ff8')
        self.label.image = img_tk
        # img.show()

        self.label.pack(fill=tk.BOTH, expand=True, side=tk.BOTTOM)
        self.back_button.pack(side=tk.LEFT, pady=5, padx=5)

    def go_back(self):
        self.label.pack_forget()
        # self.text_widget.pack()
        self.back_first_page()
        self.back_button.pack_forget()

    def run(self):
        self.root.mainloop()
