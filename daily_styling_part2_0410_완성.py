import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame

# ══════════════════════════════════════════════════════════
#  Color constants
# ══════════════════════════════════════════════════════════
BG        = "#FFFFFF"
ACCENT    = "#9B6F3A"
TEXT_DARK = "#5C3D2E"
TEXT_MID  = "#7A5C44"
TEXT_GRAY = "#AAAAAA"
BTN_RED   = "#D4A5A5"



# ══════════════════════════════════════════════════════════
#  Outfit recommendation data  (scene, tone, temp_range) -> (top, bottom)
#  Temp range: "hot"=25°C+ / "warm"=15~24°C / "cool"=5~14°C / "cold"=4°C-
# ══════════════════════════════════════════════════════════
OUTFIT_DATA = {
    ("School",   "Warm", "hot"):  ("Sleeveless Blouse",      "Linen Slacks"),
    ("School",   "Warm", "warm"): ("Beige Knit Top",         "Khaki Cotton Pants"),
    ("School",   "Warm", "cool"): ("Mustard Sweatshirt",     "Corduroy Pants"),
    ("School",   "Warm", "cold"): ("Camel Wool Coat",        "Brown Slacks"),
    ("School",   "Cool", "hot"):  ("White Linen Shirt",      "Light Denim Shorts"),
    ("School",   "Cool", "warm"): ("Gray Stripe Shirt",      "Slim Jeans"),
    ("School",   "Cool", "cool"): ("Navy Hood Zip-up",       "Gray Slacks"),
    ("School",   "Cool", "cold"): ("Charcoal Duffle Coat",   "Black Slim Pants"),
    ("Hang out", "Warm", "hot"):  ("Ivory Off-shoulder Top", "Wide Linen Pants"),
    ("Hang out", "Warm", "warm"): ("Terracotta Knit Top",    "Beige Wide Pants"),
    ("Hang out", "Warm", "cool"): ("Burgundy Turtleneck",    "Camel Long Skirt"),
    ("Hang out", "Warm", "cold"): ("Brown Padded Vest",      "Mustard Knit Skirt"),
    ("Hang out", "Cool", "hot"):  ("Sky Blue Crop Tee",      "White Shorts"),
    ("Hang out", "Cool", "warm"): ("Mint Oversized Shirt",   "Light Denim Pants"),
    ("Hang out", "Cool", "cool"): ("Gray Hoodie",            "Blue Jogger Pants"),
    ("Hang out", "Cool", "cold"): ("Navy Long Puffer",       "Black Skinny Pants"),
    ("Work out", "Warm", "hot"):  ("Peach Tank Top",         "Terracotta Leggings"),
    ("Work out", "Warm", "warm"): ("Apricot Zip-up Hoodie",  "Beige Jogger Pants"),
    ("Work out", "Warm", "cool"): ("Orange Long-sleeve Top", "Khaki Training Pants"),
    ("Work out", "Warm", "cold"): ("Wine Fleece Zip-up",     "Brown Fleece Jogger"),
    ("Work out", "Cool", "hot"):  ("White Tank Top",         "Black Shorts"),
    ("Work out", "Cool", "warm"): ("Light Gray T-shirt",     "Dark Gray Jogger"),
    ("Work out", "Cool", "cool"): ("Black Long-sleeve Top",  "Navy Training Pants"),
    ("Work out", "Cool", "cold"): ("Charcoal Fleece Zip-up", "Black Fleece Leggings"),
}


# ══════════════════════════════════════════════════════════
#  Main app class
# ══════════════════════════════════════════════════════════
class DailyStylingApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Daily Styling")
        self.root.geometry("480x700")
        self.root.resizable(False, False)
        self.root.config(bg=BG)

        self.username_entry = None
        self.weather_entry  = None

        self.scene = ""
        self.tone  = ""
        self.current_top    = ""
        self.current_bottom = ""

        self.image_title         = None
        self.image_my_look       = None
        self.image_closet_btn    = None
        self.image_save_look_btn = None
        self.image_reset_btn     = None
        self.sfx_click           = None
        self.load_all_images()
        self.play_bgm()

        self.scene_btns = {}
        self.tone_btns  = {}

        self.show_start()

    # ──────────────────────────────────────────────────────
    #  Background music
    # ──────────────────────────────────────────────────────
    def play_bgm(self):
        try:
            pygame.mixer.init()
            self.bgm = pygame.mixer.Sound("sounds/dailystyling_bgm.mp3")
            self.bgm.play(loops=-1)  # -1 = loop forever
            self.sfx_click = pygame.mixer.Sound("sounds/Click.mp3")
        except Exception as e:
            print("Sound error:", e)

    def play_click_sound(self):
        if self.sfx_click:
            self.sfx_click.play()

    # ──────────────────────────────────────────────────────
    #  Load images
    #  PIL Image.open() loads the image, thumbnail() resizes it
    #  while preserving aspect ratio, ImageTk.PhotoImage() converts
    #  it to a Tkinter-compatible image object.
    #  If a file is missing, None is assigned so the app keeps running.
    # ──────────────────────────────────────────────────────
    def load_all_images(self):
        try:
            img = Image.open("images/title.jpg")
            img.thumbnail((400, 120), Image.LANCZOS)
            self.image_title = ImageTk.PhotoImage(img)

            img = Image.open("images/my_look_btn.jpg")
            img.thumbnail((300, 80), Image.LANCZOS)
            self.image_my_look = ImageTk.PhotoImage(img)

            img = Image.open("images/closet_btn.jpg")
            img.thumbnail((80, 40), Image.LANCZOS)
            self.image_closet_btn = ImageTk.PhotoImage(img)

            img = Image.open("images/save_look_btn.png")
            img.thumbnail((160, 60), Image.LANCZOS)
            self.image_save_look_btn = ImageTk.PhotoImage(img)

            img = Image.open("images/reset_btn.png")
            img.thumbnail((160, 60), Image.LANCZOS)
            self.image_reset_btn = ImageTk.PhotoImage(img)

        except Exception as e:
            print("Image error:", e)
            self.image_title         = None
            self.image_my_look       = None
            self.image_closet_btn    = None
            self.image_save_look_btn = None
            self.image_reset_btn     = None

    # Build the My Closet button
    def make_closet_button(self):
        img = self.image_closet_btn
        if img:
            btn = tk.Button(self.root, image=img, bd=0, bg=BG,
                            cursor="hand2", command=None)
        else:
            btn = tk.Button(self.root, text="My Closet",
                            font=("Arial", 10, "bold"),
                            bg=BTN_RED, fg="white", relief="flat",
                            padx=8, pady=4, cursor="hand2",
                            command=None)
        btn.place(x=370, y=14)

    # ──────────────────────────────────────────────────────
    #  Clear all widgets from the screen
    # ──────────────────────────────────────────────────────
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ══════════════════════════════════════════════════════
    #  Start Screen
    # ══════════════════════════════════════════════════════
    def show_start(self):
        self.clear_screen()
        self.scene = ""
        self.tone  = ""
        self.scene_btns = {}
        self.tone_btns  = {}

        self.make_closet_button()

        # -- Title --
        title_img = self.image_title
        if title_img:
            tk.Label(self.root, image=title_img, bg=BG).pack(pady=(50, 6))
        else:
            tk.Label(self.root, text="Daily Styling",
                     font=("Georgia", 30, "bold"),
                     bg=BG, fg=TEXT_DARK).pack(pady=(60, 6))
            tk.Label(self.root, text="— Find Your Look —",
                     font=("Arial", 11, "italic"),
                     bg=BG, fg=TEXT_MID).pack(pady=(0, 10))

        # -- Name input --
        frame_name = tk.Frame(self.root, bg=BG)
        frame_name.pack(pady=6)
        tk.Label(frame_name, text="Your Name :",
                 font=("Arial", 12), bg=BG, fg=TEXT_DARK).pack(side="left")
        self.username_entry = tk.Entry(frame_name,
                                       font=("Arial", 12), width=14,
                                       relief="groove", bd=2)
        self.username_entry.insert(0, "user")  # default value
        self.username_entry.pack(side="left", padx=6)

        # -- Temperature input --
        frame_weather = tk.Frame(self.root, bg=BG)
        frame_weather.pack(pady=6)
        tk.Label(frame_weather, text="Temperature (°C) :",
                 font=("Arial", 12), bg=BG, fg=TEXT_DARK).pack(side="left")
        self.weather_entry = tk.Entry(frame_weather,
                                      font=("Arial", 12), width=6,
                                      relief="groove", bd=2)
        self.weather_entry.pack(side="left", padx=6)

        # -- Scene buttons --
        tk.Label(self.root, text="Scene",
                 font=("Arial", 13, "bold"),
                 bg=BG, fg=TEXT_DARK).pack(pady=(20, 5))

        frame_scene = tk.Frame(self.root, bg=BG)
        frame_scene.pack()

        btn_school = tk.Button(frame_scene, text="School",
                               font=("Arial", 11), width=10,
                               relief="groove", cursor="hand2",
                               command=self.on_scene_school)
        btn_school.pack(side="left", padx=5)
        self.scene_btns["School"] = btn_school

        btn_hangout = tk.Button(frame_scene, text="Hang out",
                                font=("Arial", 11), width=10,
                                relief="groove", cursor="hand2",
                                command=self.on_scene_hangout)
        btn_hangout.pack(side="left", padx=5)
        self.scene_btns["Hang out"] = btn_hangout

        btn_workout = tk.Button(frame_scene, text="Work out",
                                font=("Arial", 11), width=10,
                                relief="groove", cursor="hand2",
                                command=self.on_scene_workout)
        btn_workout.pack(side="left", padx=5)
        self.scene_btns["Work out"] = btn_workout

        # -- Personal Tone buttons --
        tk.Label(self.root, text="Personal Tone",
                 font=("Arial", 13, "bold"),
                 bg=BG, fg=TEXT_DARK).pack(pady=(16, 4))

        frame_tone = tk.Frame(self.root, bg=BG)
        frame_tone.pack()

        btn_warm = tk.Button(frame_tone, text="Warm",
                             font=("Arial", 11), width=10,
                             relief="groove", cursor="hand2",
                             command=self.on_tone_warm)
        btn_warm.pack(side="left", padx=5)
        self.tone_btns["Warm"] = btn_warm

        btn_cool = tk.Button(frame_tone, text="Cool",
                             font=("Arial", 11), width=10,
                             relief="groove", cursor="hand2",
                             command=self.on_tone_cool)
        btn_cool.pack(side="left", padx=5)
        self.tone_btns["Cool"] = btn_cool

        # -- My Look button --
        my_look_img = self.image_my_look
        if my_look_img:
            tk.Button(self.root, image=my_look_img, bd=0, bg=BG,
                      cursor="hand2",
                      command=self.on_my_look_click).pack(pady=28)
        else:
            tk.Button(self.root, text="My Look",
                      font=("Arial", 14, "bold"),
                      bg=ACCENT, fg="white",
                      width=18, height=2, relief="flat",
                      cursor="hand2",
                      command=self.on_my_look_click).pack(pady=28)

    # -- My Look button handler --
    def on_my_look_click(self):
        try:
            temp = int(self.weather_entry.get())
        except:
            messagebox.showwarning("Warning", "Temperature out of range.\nPlease check again.")
            return

        if not (-20 <= temp <= 45):
            messagebox.showwarning("Warning", "Temperature out of range.\nPlease check again.")
            return

        if self.scene == "" or self.tone == "":
            messagebox.showwarning("Warning", "Please complete all sections.")
            return

        # Determine temperature range
        if temp >= 25:
            temp_cat = "hot"
        elif temp >= 15:
            temp_cat = "warm"
        elif temp >= 5:
            temp_cat = "cool"
        else:
            temp_cat = "cold"

        # Look up outfit from data
        self.current_top, self.current_bottom = OUTFIT_DATA[(self.scene, self.tone, temp_cat)]

        self.play_click_sound()
        self.show_outfit()

    # -- Scene / Tone button handlers --
    def on_scene_school(self):
        self.select_scene("School")

    def on_scene_hangout(self):
        self.select_scene("Hang out")

    def on_scene_workout(self):
        self.select_scene("Work out")

    def on_tone_warm(self):
        self.select_tone("Warm")

    def on_tone_cool(self):
        self.select_tone("Cool")

    # Highlight the selected scene button and reset the others
    def select_scene(self, selected):
        self.scene = selected
        for name, btn in self.scene_btns.items():
            if name == selected:
                btn.config(bg=ACCENT, fg="white", relief="sunken")
            else:
                btn.config(bg="SystemButtonFace", fg="black", relief="groove")

    def select_tone(self, selected):
        self.tone = selected
        for name, btn in self.tone_btns.items():
            if name == selected:
                btn.config(bg=ACCENT, fg="white", relief="sunken")
            else:
                btn.config(bg="SystemButtonFace", fg="black", relief="groove")

    def on_save_look(self):
        messagebox.showinfo("Saved!", f"Your look has been saved!\n\nTOP : {self.current_top}\nBOTTOM : {self.current_bottom}")

    # ══════════════════════════════════════════════════════
    #  2. Outfit Screen
    # ══════════════════════════════════════════════════════
    def show_outfit(self):
        self.from_screen = "outfit"
        name = self.username_entry.get().strip() or "user"  # save before clearing screen
        self.clear_screen()

        self.make_closet_button()
        tk.Label(self.root, text=f"{name}'s OOTD",
                 font=("Georgia", 24, "bold"),
                 bg=BG, fg=TEXT_DARK).pack(pady=(52, 18))

        frame_outfit = tk.Frame(self.root, bg=BG)
        frame_outfit.pack(pady=6)

        tk.Label(frame_outfit, text="TOP",
                 font=("Arial", 11, "bold"),
                 bg=BG, fg=TEXT_GRAY).grid(row=0, column=0, padx=24)
        tk.Label(frame_outfit, text="BOTTOM",
                 font=("Arial", 11, "bold"),
                 bg=BG, fg=TEXT_GRAY).grid(row=0, column=1, padx=24)

        tk.Label(frame_outfit, text=self.current_top,
                 font=("Arial", 11), bg=BG, fg=TEXT_DARK,
                 width=16, height=9, wraplength=130,
                 relief="groove").grid(row=1, column=0, padx=24, pady=8)

        tk.Label(frame_outfit, text=self.current_bottom,
                 font=("Arial", 11), bg=BG, fg=TEXT_DARK,
                 width=16, height=9, wraplength=130,
                 relief="groove").grid(row=1, column=1, padx=24, pady=8)

        tk.Label(self.root,
                 text=f"{self.current_top}  &  {self.current_bottom}",
                 font=("Arial", 12, "italic"),
                 bg=BG, fg=TEXT_MID,
                 wraplength=420).pack(pady=10)

        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(pady=22)

        if self.image_save_look_btn:
            tk.Button(btn_frame, image=self.image_save_look_btn, bd=0, bg=BG,
                      cursor="hand2",
                      command=self.on_save_look).pack(side="left", padx=10)
        else:
            tk.Button(btn_frame, text="Save Look",
                      font=("Arial", 12), bg=ACCENT, fg="white",
                      width=13, height=2, relief="flat",
                      cursor="hand2",
                      command=self.on_save_look).pack(side="left", padx=10)

        if self.image_reset_btn:
            tk.Button(btn_frame, image=self.image_reset_btn, bd=0, bg=BG,
                      cursor="hand2",
                      command=self.show_start).pack(side="left", padx=10)
        else:
            tk.Button(btn_frame, text="Reset",
                      font=("Arial", 12), bg=BTN_RED, fg="white",
                      width=13, height=2, relief="flat",
                      cursor="hand2",
                      command=self.show_start).pack(side="left", padx=10)


# ══════════════════════════════════════════════════════════
#  Run the program
# ══════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    app = DailyStylingApp(root)
    root.mainloop()
