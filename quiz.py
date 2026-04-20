import tkinter as tk

BG        = "#FFF8F0"
ACCENT    = "#C8A882"
TEXT_DARK = "#5C3D2E"
TEXT_MID  = "#7A5C44"
TEXT_GRAY = "#AAAAAA"
BTN_RED   = "#D4A5A5"


def load_image(path):
    try:
        return tk.______(file=path)     # (8)
    except:
        return None


class DailyStylingApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Daily Styling")
        self.root.______("480x700")     # (7)
        self.root.______(False, False)  # (6)
        self.root.______(bg=BG)         # (5)

        self.username_entry = None
        self.weather_entry  = None
        self.scene = ""
        self.tone  = ""

        self.images = {}
        self.load_all_images()

        self.scene_btns = {}
        self.tone_btns  = {}

        self.show_start()

    def load_all_images(self):
        self.images["title"]      = load_image("images/title.png")
        self.images["my_look"]    = load_image("images/my_look_btn.png")
        self.images["closet_btn"] = load_image("images/closet_btn.png")

    def make_closet_button(self):
        img = self.images["closet_btn"]
        if img:
            btn = ______(self.root, image=img, bd=0, bg=BG,     # (12)
                            cursor="hand2", command=None)
        else:
            btn = ______(self.root, text="My Closet",            # (12)
                            font=("Arial", 10, "bold"),
                            bg=BTN_RED, fg="white", relief="flat",
                            padx=8, pady=4, cursor="hand2",
                            command=None)
        btn.______(x=370, y=14)     # (9)

    def show_start(self):
        self.scene = ""
        self.tone  = ""
        self.scene_btns = {}
        self.tone_btns  = {}

        self.make_closet_button()

        title_img = self.images["title"]
        if title_img:
            ______(self.root, image=title_img, bg=BG).pack(pady=(50, 6))    # (2)
        else:
            ______(self.root, text="Daily Styling",                          # (2)
                     font=("Georgia", 30, "bold"),
                     bg=BG, fg=TEXT_DARK).______(pady=(60, 6))               # (4)
            ______(self.root, text="— Find Your Look —",                     # (2)
                     font=("Arial", 11, "italic"),
                     bg=BG, fg=TEXT_MID).______(pady=(0, 10))                # (4)

        frame_name = ______(self.root, bg=BG)                                # (1)
        frame_name.______(pady=6)                                            # (4)
        ______(frame_name, text="Your Name :",                               # (2)
                 font=("Arial", 12), bg=BG, fg=TEXT_DARK).______(side="left")   # (4)
        self.username_entry = ______(frame_name,                             # (3)
                                       font=("Arial", 12), width=14,
                                       relief="groove", bd=2)
        self.username_entry.______(0, "user")                                # (10)
        self.username_entry.______(side="left", padx=6)                      # (11)

        frame_weather = ______(self.root, bg=BG)                             # (1)
        frame_weather.______(pady=6)                                         # (4)
        ______(frame_weather, text="Temperature (°C) :",                     # (2)
                 font=("Arial", 12), bg=BG, fg=TEXT_DARK).______(side="left")   # (4)
        self.weather_entry = ______(frame_weather,                           # (3)
                                      font=("Arial", 12), width=6,
                                      relief="groove", bd=2)
        self.weather_entry.______(side="left", padx=6)                       # (11)

        ______(self.root, text="Scene",                                      # (2)
                 font=("Arial", 13, "bold"),
                 bg=BG, fg=TEXT_DARK).______(pady=(20, 5))                   # (4)

        frame_scene = ______(self.root, bg=BG)                               # (1)
        frame_scene.______()                                                 # (4)

        btn_school = ______(frame_scene, text="School",                      # (14)
                               font=("Arial", 11), width=10,
                               relief="groove", cursor="hand2",
                               command=self.on_scene_school)
        btn_school.______(side="left", padx=5)                               # (13)
        self.scene_btns["School"] = btn_school

        btn_hangout = ______(frame_scene, text="Hang out",                   # (14)
                                font=("Arial", 11), width=10,
                                relief="groove", cursor="hand2",
                                command=self.on_scene_hangout)
        btn_hangout.______(side="left", padx=5)                              # (13)
        self.scene_btns["Hang out"] = btn_hangout

        btn_workout = ______(frame_scene, text="Work out",                   # (14)
                                font=("Arial", 11), width=10,
                                relief="groove", cursor="hand2",
                                command=self.on_scene_workout)
        btn_workout.______(side="left", padx=5)                              # (13)
        self.scene_btns["Work out"] = btn_workout

        ______(self.root, text="Personal Tone",                              # (2)
                 font=("Arial", 13, "bold"),
                 bg=BG, fg=TEXT_DARK).______(pady=(16, 4))                   # (4)

        frame_tone = ______(self.root, bg=BG)                                # (1)
        frame_tone.______()                                                  # (4)

        btn_warm = ______(frame_tone, text="Warm",                           # (14)
                             font=("Arial", 11), width=10,
                             relief="groove", cursor="hand2",
                             command=self.on_tone_warm)
        btn_warm.______(side="left", padx=5)                                 # (15)
        self.tone_btns["Warm"] = btn_warm

        btn_cool = ______(frame_tone, text="Cool",                           # (14)
                             font=("Arial", 11), width=10,
                             relief="groove", cursor="hand2",
                             command=self.on_tone_cool)
        btn_cool.______(side="left", padx=5)                                 # (15)
        self.tone_btns["Cool"] = btn_cool

        my_look_img = self.images["my_look"]
        if my_look_img:
            ______(self.root, image=my_look_img, bd=0, bg=BG,               # (12)
                      cursor="hand2",
                      command=lambda: None).______(pady=28)                  # (4)
        else:
            ______(self.root, text="✨  My Look  ✨",                        # (12)
                      font=("Arial", 14, "bold"),
                      bg=ACCENT, fg="white",
                      width=18, height=2, relief="flat",
                      cursor="hand2",
                      command=lambda: None).______(pady=28)                  # (4)

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

    def select_scene(self, selected):
        self.scene = selected
        for name, btn in self.scene_btns.______():  # (17)
            if name == selected:
                btn.______(bg=ACCENT, fg="white", relief="sunken")          # (16)
            else:
                btn.______(bg="SystemButtonFace", fg="black", relief="groove")  # (18)

    def select_tone(self, selected):
        self.tone = selected
        for name, btn in self.tone_btns.______():   # (17)
            if name == selected:
                btn.______(bg=ACCENT, fg="white", relief="sunken")          # (16)
            else:
                btn.______(bg="SystemButtonFace", fg="black", relief="groove")  # (18)


if __name__ == "__main__":
    root = tk.Tk()
    app = DailyStylingApp(root)
    root.______()               # (19)
