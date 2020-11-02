import tkinter as tk, logging
from cv2 import cv2
from PIL import Image, ImageTk
from time import gmtime, strftime

logging.basicConfig(level=logging.INFO, format='{asctime}: {levelname}: {message}', style='{', datefmt='%d-%b-%Y %H:%M:%S')

class StockApp(tk.Frame):
    def __init__(self, window=None):
        # Initialize main window and title
        self.window = window
        self.window.title('Testing Window')        

        # Initialize webcam video
        # Change int to select video source, default 0
        self.webcam = cv2.VideoCapture(0)
        # Set cam and frame width and height
        self.width = self.webcam.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.webcam.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # Initialize window widgets
        # Label describing app
        self.desc_label = tk.Label(text='Simple program to maintain item stock', bg='white')
        self.desc_label.pack()

        # Canvas to display webcam image    
        self.cam_window = tk.Canvas(bg='black', width=self.width, height=self.height)
        self.cam_window.pack(side='left', padx=10, pady=10)

        # Button to add item to db
        self.add_button = tk.Button(text='Add', width=10, bg='white', command=self.take_screenshot)
        self.add_button.pack()

        # Button to remove item from db
        self.remove_button = tk.Button(text='Remove', width=10, bg='white')
        self.remove_button.pack()

        # Button to check on current stock
        self.stock_button = tk.Button(text='Stock', width=10, bg='white')
        self.stock_button.pack()

        # Button to exit app
        self.exit = tk.Button(text='Exit', width=8, fg='red', bg='white', command=self.window.destroy)
        self.exit.pack()
        
        # Add update delay in milliseconds
        self.delay = 15
        self.update_canvas()

        # Loop window
        self.window.mainloop()

    def get_vid_frame(self):
        if self.webcam.isOpened():
            # logging.info('Reading webcam video')
            _, frame = self.webcam.read()

            # logging.info('Returning webcam frame')
            return frame
        else:
            raise Exception('Unable to open video source')

    def update_canvas(self):
        # logging.info('Retrieving webcam frame')
        frame = self.get_vid_frame()

        # logging.info('Adjusting color space')
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # logging.info('Generating canvas image')
        self.image = ImageTk.PhotoImage(Image.fromarray(image))
        self.cam_window.create_image(0, 0, image=self.image, anchor=tk.NW)

        self.window.after(self.delay, self.update_canvas)

    def take_screenshot(self):
        logging.info('Taking screenshot')
        logging.info('Retrieving webcam frame')
        frame = self.get_vid_frame()
        image = cv2.resize(frame, (200, 200))

        logging.info('Saving image')
        cv2.imwrite('../data/' + strftime("%Y-%m-%d-%H-%M-%S", gmtime()) + '-image.jpg', image)

    def __del__(self):
        if self.webcam.isOpened():
            logging.info('Releasing webcam')
            self.webcam.release()

main = tk.Tk()
StockApp(main)