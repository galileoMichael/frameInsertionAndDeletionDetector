from tkinter import Tk, Canvas, Button, filedialog, PhotoImage, Toplevel
from pathlib import Path
from threading import Thread
from queue import Queue
from PIL import Image, ImageTk
import time
import os
import sys

from main import main  

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Sistem Pendeteksi Penghapusan dan Penyisipan Frame\Sistem Pendeteksi Penghapusan dan Penyisipan Frame\assets\mainScreen")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

video_path = None
gui_queue = Queue()

def choose_video():
    global video_path, video_title, success_image, title
    video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mkv")])
    base_name = os.path.basename(video_path)
    title, _ = os.path.splitext(base_name)
    if video_path:
        upload_button.place_forget()
        image_success_upload = PhotoImage(file=relative_to_assets("image_5.png"))
        canvas.create_image(
            962.0,
            300.0,
            image=image_success_upload,
            tags="success_image"
        )
        canvas.create_text(
            967.0,
            430.0,
            text=f"Selected Video: {title}",
            fill="black",
            font=("Arial", 18),
            tags="video_title"
        )
        cancel_button.place(
            x=927.0,
            y=445.0
        )
        window.processing_image = image_success_upload
        canvas.delete("warning_image")

def process_queue():
    while not gui_queue.empty():
        message = gui_queue.get()
        if isinstance(message, str) and message.startswith('show_image_'):
            start_button.place_forget()
            canvas.delete("success_image")
            image_number = message.split('_')[2]
            processing_image = PhotoImage(file=relative_to_assets(f"loading_{image_number}.png"))
            canvas.create_image(
                640.0,  
                0.0,  
                image=processing_image,
                tags="processing_image",
                anchor="nw"
            )
            window.processing_image = processing_image 
            canvas.create_text(
                960.0,
                320.0,
                text=f"Selected Video: {title}",
                fill="black",
                font=("Arial", 18),
                tags="video_title"
            )    
        elif message == 'restart_app':
            canvas.delete("processing_image")
            reset_application()
        elif isinstance(message, tuple) and message[0] == 'show_results':
            _, deletion_locations, deleted_frames, insertion_locations = message
            show_results_screen(deletion_locations, deleted_frames, insertion_locations)
        gui_queue.task_done()
    window.after(100, process_queue)

def start_research():
    if video_path:
        research_thread = Thread(target=main, args=(video_path, gui_queue))
        research_thread.start()
        canvas.delete("video_title")
        cancel_button.place_forget()        
    else:
        warning_image = PhotoImage(file=relative_to_assets("image_6.png"))
        canvas.create_image(
            975.0,
            500.0,
            image=warning_image,
            tags="warning_image"
        )
        window.processing_image = warning_image
        print("Please select a video first.")

def reset_application():
    global video_path
    video_path = None
    reset_gui_state()
    print("Application state reset.")

def reset_gui_state():
    canvas.delete("success_image")
    canvas.delete("video_title")
    cancel_button.place_forget()
    upload_button.place(
        x=770.0,
        y=250.0
    )
    start_button.place(
        x=840.0,
        y=550.0
    )

def show_results_screen(deletion_locations, deleted_frames, insertion_locations):
    results_window = Toplevel(window)
    results_window.title("Aplikasi Pendeteksi Penghapusan dan Penyisipan Frame - Results Screen")
    results_window.geometry("1280x720")
    results_window.configure(bg="#FFFFFF")
    
    results_canvas = Canvas(
        results_window,
        bg="#FFFFFF",
        height=720,
        width=1280,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    
    results_canvas.place(x=0, y=0)

    image_image_10 = PhotoImage(file=relative_to_assets("image_10.png"))
    results_canvas.create_image(
        640.0, 
        22.0, 
        image=image_image_10
    )

    results_canvas.create_text(
        640.0,
        60.0,
        text=f"Selected Video: {title}",
        fill="black",
        font=("Arial", 18),
        tags="video_title"
    )    

    image_image_11 = PhotoImage(file=relative_to_assets("image_11.png"))
    results_canvas.create_image(
        640.0, 
        700.0, 
        image=image_image_11
    )

    image_deletion_label = PhotoImage(file=relative_to_assets("image_8.png"))
    results_canvas.create_image(
        320.0, 
        504.0, 
        image=image_deletion_label
    )

    image_insertion_label = PhotoImage(file=relative_to_assets("image_9.png"))
    results_canvas.create_image(
        960.0, 
        504.0, 
        image=image_insertion_label
    )

    results_canvas.create_text(
        320.0, 
        580.0,
        text=f"Deletion Frames: {deletion_locations} , {deleted_frames}",
        fill="black",
        font=("Arial", 16)
    )

    results_canvas.create_text(
        960.0, 
        580.0,
        text=f"Insertion Frames: {insertion_locations}",
        fill="black",
        font=("Arial", 16)
    )

    results_window.image_image_10 = image_image_10
    results_window.image_image_11 = image_image_11
    results_window.image_deletion_label = image_deletion_label
    results_window.image_insertion_label = image_insertion_label

    frame_directory = r"C:\Sistem Pendeteksi Penghapusan dan Penyisipan Frame\Sistem Pendeteksi Penghapusan dan Penyisipan Frame\data\frames"

    x_position = 160
    y_position = 180
    if isinstance(deletion_locations, list) and deletion_locations[0] != "No deletions detected":
        for idx, frame_num in enumerate(deletion_locations):
            if isinstance(frame_num, int):
                prev_frame_num = frame_num - 1
                if prev_frame_num >= 0:
                    prev_frame_path = os.path.join(frame_directory, f"frame{prev_frame_num}.jpg")
                    frame_path = os.path.join(frame_directory, f"frame{frame_num}.jpg")
                
                    if os.path.exists(prev_frame_path):
                        prev_img = Image.open(prev_frame_path)
                        prev_img = prev_img.resize((240, 135), Image.LANCZOS)  
                        prev_img = ImageTk.PhotoImage(prev_img)
                        results_canvas.create_image(
                            x_position,
                            y_position, 
                            image=prev_img,
                        )
                        results_canvas.create_text(
                            x_position,
                            y_position - 75,  
                            text=f"Frame {prev_frame_num}",
                            font=("Arial", 16)
                        )
                        results_window.__setattr__(f"prev_deletion_img_{idx}", prev_img)  
                        x_position += 320  

                    if os.path.exists(frame_path):
                        img = Image.open(frame_path)
                        img = img.resize((240, 135), Image.LANCZOS)  
                        img = ImageTk.PhotoImage(img)
                        results_canvas.create_image(
                            x_position,
                            y_position,  
                            image=img,
                        )
                        results_canvas.create_text(
                            x_position,
                            y_position - 75,  
                            text=f"Frame {frame_num}",
                            font=("Arial", 16)
                        )
                        results_window.__setattr__(f"deletion_img_{idx}", img)  
                        x_position += 320  

        
            if x_position >= 800:  
                x_position = 160
                y_position += 200  

    x_position = 800
    y_position = 180
    if isinstance(insertion_locations, list) and insertion_locations[0] != "No insertions detected":
        for idx, (start_frame, end_frame) in enumerate(insertion_locations):
            prev_frame = start_frame - 1
            frame_path = os.path.join(frame_directory, f"frame{prev_frame}.jpg")
            if os.path.exists(frame_path):
                img = Image.open(frame_path)
                img = img.resize((240, 135), Image.LANCZOS)  
                img = ImageTk.PhotoImage(img)
                results_canvas.create_image(
                    x_position,  
                    y_position,  
                    image=img,
                )
                results_canvas.create_text(
                    x_position,
                    y_position - 75,  
                    text=f"Frame {prev_frame}",
                    font=("Arial", 16)
                )
                results_window.__setattr__(f"insertion_prev_img_{idx}", img)  
                x_position += 320

            frame_path = os.path.join(frame_directory, f"frame{start_frame}.jpg")
            if os.path.exists(frame_path):
                img = Image.open(frame_path)
                img = img.resize((240, 135), Image.LANCZOS)  
                img = ImageTk.PhotoImage(img)
                results_canvas.create_image(
                    x_position,  
                    y_position,  
                    image=img,
                )
                results_canvas.create_text(
                    x_position,
                    y_position - 75,  
                    text=f"Frame {start_frame}",
                    font=("Arial", 16)
                )
                results_window.__setattr__(f"insertion_start_img_{idx}", img)  
                x_position = 800
                y_position += 200

            frame_path = os.path.join(frame_directory, f"frame{end_frame}.jpg")
            if os.path.exists(frame_path):
                img = Image.open(frame_path)
                img = img.resize((240, 135), Image.LANCZOS)  
                img = ImageTk.PhotoImage(img)
                results_canvas.create_image(
                    x_position,  
                    y_position,  
                    image=img,
                )
                results_canvas.create_text(
                    x_position,
                    y_position - 75,
                    text=f"Frame {end_frame}",
                    font=("Arial", 16)
                )
                results_window.__setattr__(f"insertion_end_img_{idx}", img)  
                x_position += 320

            next_frame = end_frame + 1
            frame_path = os.path.join(frame_directory, f"frame{next_frame}.jpg")
            if os.path.exists(frame_path):
                img = Image.open(frame_path)
                img = img.resize((240, 135), Image.LANCZOS)  
                img = ImageTk.PhotoImage(img)
                results_canvas.create_image(
                    x_position,  
                    y_position,  
                    image=img,
                )
                results_canvas.create_text(
                    x_position,
                    y_position - 75,
                    text=f"Frame {next_frame}",                        
                    font=("Arial", 16)
                )
                results_window.__setattr__(f"insertion_next_img_{idx}", img)  
                x_position += 320

def show_main_screen():
    global window, canvas, start_button, upload_button, cancel_button

    window = Tk()
    window.geometry("1280x720")
    window.configure(bg="#FFFFFF")
    window.title("Aplikasi Pendeteksi Penghapusan dan Penyisipan Frame - Main Screen")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=720.0,
        width=1280.0,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    start_button = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=start_research,
        relief="flat"
    )
    start_button.place(
        x=840.0,
        y=550.0
    )

    upload_button_image = PhotoImage(file=relative_to_assets("button_2.png"))
    upload_button = Button(
        image=upload_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=choose_video,  
        relief="flat"
    )
    upload_button.place(
        x=768.0,
        y=250.0
    )

    cancel_button_image = PhotoImage(file=relative_to_assets("cancel_button.png"))
    cancel_button = Button(
        image=cancel_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=reset_application,
        relief="flat"
    )

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        0.0,
        0.0,
        image=image_image_1,
        anchor="nw"
    )

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        25.0,
        550.0,
        image=image_image_2,
        anchor="nw"
    )

    image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        25.0,
        220.0,
        image=image_image_3,
        anchor="nw"
    )

    image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        25.0,
        25.0,
        image=image_image_4,
        anchor="nw"
    )

    image_main_icon = PhotoImage(file=relative_to_assets("iconMainScreen.png"))
    main_icon = canvas.create_image(
        300.0,
        400.0,
        image=image_main_icon
    )
    window.resizable(False, False)

    window.after(100, process_queue)
    window.mainloop()

def show_loading_screen():
    loading_window = Tk()
    loading_window.geometry("1280x720")
    loading_window.configure(bg="#FFFFFF")
    loading_window.title("Aplikasi Pendeteksi Penghapusan dan Penyisipan Frame - Loading Screen")

    loading_canvas = Canvas(
        loading_window,
        bg="#FFFFFF",
        height=720,
        width=1280,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    loading_canvas.place(x=0, y=0)

    title_loading = PhotoImage(file=relative_to_assets("titleLoadingScreen.png"))
    loading_canvas.create_image(
        640.0,
        150.0,
        image=title_loading
    )

    logo_loading = PhotoImage(file=relative_to_assets("iconLoadingScreen.png"))
    loading_canvas.create_image(
        640.0,
        360.0,
        image=logo_loading
    )

    loading_window.update()
    time.sleep(3)  
    loading_window.destroy()

    show_main_screen()

show_loading_screen()