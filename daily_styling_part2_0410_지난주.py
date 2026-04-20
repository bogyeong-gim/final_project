import tkinter as tk
from PIL import Image, ImageTk
import pygame

# ══════════════════════════════════════════════════════════
#  색상 상수
# ══════════════════════════════════════════════════════════
BG        = "#FFF8F0"
ACCENT    = "#9B6F3A"
TEXT_DARK = "#5C3D2E"
TEXT_MID  = "#7A5C44"
TEXT_GRAY = "#AAAAAA"
BTN_RED   = "#D4A5A5"




# ══════════════════════════════════════════════════════════
#  메인 앱 클래스
# ══════════════════════════════════════════════════════════
class DailyStylingApp:

    def __init__(self, root): # 초기화 함수 
        # self는 이 클래스에서 만들어지는 객체 자기 자신을 의미 (즉 app을 의미)
        self.root = root 
        self.root.title("Daily Styling")
        self.root.geometry("480x700") 
        self.root.resizable(False, False) 
        self.root.config(bg=BG) 

        self.username_entry = None 
        self.weather_entry  = None  

        self.scene = ""     
        self.tone  = ""    

        self.image_title      = None
        self.image_my_look    = None
        self.image_closet_btn = None
        self.load_all_images()
        self.play_bgm()

        self.scene_btns = {}
        self.tone_btns  = {}

        self.show_start()

    # ──────────────────────────────────────────────────────
    #  이미지 불러오기
    #  PILLOW 라이브러리리의 Image.open()으로 이미지를 불러오고, resize()로 크기를 조정한 후, 
    # # ImageTk.PhotoImage()로 Tkinter에서 사용할 수 있는 이미지 객체로 변환
    # 만약 이미지 파일이 없거나 오류가 발생하면 예외 처리로 None을 할당하여 프로그램이 계속 실행되도록 함
    # 참고 ) LANCZOS는 고품질 리샘플링 필터로, 이미지 크기를 줄일 때 선명도를 유지하는 데 도움을 줌
    # ──────────────────────────────────────────────────────
    def load_all_images(self):
        try:
            self.image_title      = ImageTk.PhotoImage(Image.open("images/title.png").resize((320, 100), Image.LANCZOS))
            self.image_my_look    = ImageTk.PhotoImage(Image.open("images/my_look_btn.png").resize((200, 70), Image.LANCZOS))
            self.image_closet_btn = ImageTk.PhotoImage(Image.open("images/closet_btn.png").resize((80, 40), Image.LANCZOS))
                          
        except Exception as e:
            print("image error:", e)
            self.image_title      = None
            self.image_my_look    = None
            self.image_closet_btn = None
    
    # 음악 로딩 함수
    def play_bgm(self):
        pygame.mixer.init() # pygame 음향 시스템을 시작
        # self.bgm = pygame.mixer.Sound("sounds/sample.mp3") # BGM 파일을 Sound 객체로 로드
        self.bgm.play(loops = -1)

    # My closet 버튼 만들기
    def make_closet_button(self):
        img = self.image_closet_btn
        if img:
            btn = tk.Button(self.root, image=img, bd=0, bg=BG,
                            cursor="hand2", command=None) 
            # cursor="hand2"는 마우스 커서가 버튼 위에 있을 때 손가락 모양으로 바뀌도록 하는 옵션
        else:
            btn = tk.Button(self.root, text="My Closet",
                            font=("Arial", 10, "bold"),
                            bg=BTN_RED, fg="white", relief="flat",
                            padx=8, pady=4, cursor="hand2",
                            command=None)
        btn.place(x=370, y=14)

    # ══════════════════════════════════════════════════════
    #  Start Screen
    # ══════════════════════════════════════════════════════
    def show_start(self):
        self.scene = ""       
        self.tone  = ""         
        self.scene_btns = {}    
        self.tone_btns  = {}    

        self.make_closet_button()

        # ── 타이틀 ──────────────────────────────────────
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

        # ── 유저 이름 입력 ──────────────────────────────
        frame_name = tk.Frame(self.root, bg=BG)
        frame_name.pack(pady=6)
        tk.Label(frame_name, text="Your Name :",
                 font=("Arial", 12), bg=BG, fg=TEXT_DARK).pack(side="left")
        self.username_entry = tk.Entry(frame_name,          
                                       font=("Arial", 12), width=14,
                                       relief="groove", bd=2) 
        self.username_entry.insert(0, "user")  # 기본값 설정       
        self.username_entry.pack(side="left", padx=6)

        # ── 온도 입력 ───────────────────────────────────
        frame_weather = tk.Frame(self.root, bg=BG)
        frame_weather.pack(pady=6)
        tk.Label(frame_weather, text="Temperature (°C) :",
                 font=("Arial", 12), bg=BG, fg=TEXT_DARK).pack(side="left")
        self.weather_entry = tk.Entry(frame_weather,       
                                      font=("Arial", 12), width=6,
                                      relief="groove", bd=2)
        self.weather_entry.pack(side="left", padx=6)       

        # ── Scene 선택 버튼 3개 ─────────────────────────
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

        # ── Personal Tone 선택 버튼 2개 ────────────────
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

        # ── My Look 버튼 ────────────────────────────────
        my_look_img = self.image_my_look
        if my_look_img:
            tk.Button(self.root, image=my_look_img, bd=0, bg=BG,
                      cursor="hand2",
                      command=lambda: None).pack(pady=28)
        else:
            tk.Button(self.root, text="✨  My Look  ✨",
                      font=("Arial", 14, "bold"),
                      bg=ACCENT, fg="white",
                      width=18, height=2, relief="flat",
                      cursor="hand2",
                      command=lambda: None).pack(pady=28)

    # ── Scene / Tone 버튼 핸들러 ────────────────────────
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

    # school, hangout, workout 버튼 중 하나가 클릭되면 select_scene 함수가 호출되면서 scene이 선택되고, tone 버튼도 마찬가지로 tone이 선택됨.
    # scene_btns --> ["School": btn_school, "Hang out": btn_hangout, "Work out": btn_workout]
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


# ══════════════════════════════════════════════════════════
#  프로그램 실행
# ══════════════════════════════════════════════════════════
if __name__ == "__main__": # 이 파일이 직접 실행될때만 아래 코드가 실행
    root = tk.Tk() # Tikinter의 메인 창을 생성했는데, 그 이름이 root  
    app = DailyStylingApp(root) # DailyStylingApp 클래스 (설계도)을 이용해서 app을 생성  

    # GUI 프로그램을 계속 실행상태로 유지 
    root.mainloop()

