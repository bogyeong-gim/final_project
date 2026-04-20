import tkinter as tk                # GUI 창/위젯을 만드는 기본 라이브러리
from tkinter import messagebox      # 경고·알림 팝업창 모듈
import json                         # 데이터를 JSON 파일로 읽고 쓰기 위해 사용
import os                           # 파일 존재 여부 확인 등 운영체제 기능 사용

# ══════════════════════════════════════════════════════════
#  색상 상수  (전역변수로 한 곳에서 관리해야 나중에 관리가 편리함)
# ══════════════════════════════════════════════════════════
BG        = "#FFF8F0"   # 배경색
ACCENT    = "#C8A882"   # 강조색 (선택된 버튼 등)
TEXT_DARK = "#5C3D2E"   # 진한 글자색
TEXT_MID  = "#7A5C44"   # 중간 글자색
TEXT_GRAY = "#AAAAAA"   # 회색 글자
CARD_BG   = "#EDE0D4"   # 카드 배경색
BTN_GRAY  = "#B0B0B0"   # 회색 버튼
BTN_RED   = "#D4A5A5"   # 붉은 계열 버튼

# 저장 파일 이름 / 최대 저장 개수
CLOSET_FILE = "closet.json"         # 클로짓 데이터를 저장할 JSON 파일 이름
MAX_LOOKS   = 3                     # 클로짓에 저장 가능한 최대 룩 수

# ══════════════════════════════════════════════════════════
#  코디 데이터베이스
#  key  : (온도구간, scene, tone)
#  value: (상의 이름, 하의 이름)
# ══════════════════════════════════════════════════════════
OUTFIT_DB = {                       # 딕셔너리: (온도구간, 상황, 톤) → (상의, 하의) 매핑
    # ── cool (21-25°C) ─────────────────────────────────
    ("cool", "School",   "Warm"): ("Beige Knit Sweater",    "Camel Slacks"),
    ("cool", "School",   "Cool"): ("Gray Hoodie",            "Dark Straight Jeans"),
    ("cool", "Hang out", "Warm"): ("Cream Oversized Jacket", "Light Brown Trousers"),
    ("cool", "Hang out", "Cool"): ("Navy Windbreaker",       "Black Jogger Pants"),
    ("cool", "Work out", "Warm"): ("Peach Zip-up Hoodie",   "Beige Leggings"),
    ("cool", "Work out", "Cool"): ("Gray Sports Hoodie",     "Dark Training Pants"),
    # ── mild (26-30°C) ─────────────────────────────────
    ("mild", "School",   "Warm"): ("White Linen Shirt",      "Beige Wide Pants"),
    ("mild", "School",   "Cool"): ("Light Blue Denim Shirt", "Gray Slim Jeans"),
    ("mild", "Hang out", "Warm"): ("Pastel Stripe T-shirt",  "Ivory Linen Pants"),
    ("mild", "Hang out", "Cool"): ("White Graphic Tee",      "Light Wash Jeans"),
    ("mild", "Work out", "Warm"): ("Light Pink Sports Tee",  "White Biker Shorts"),
    ("mild", "Work out", "Cool"): ("Mint Sports Tank",       "Black Running Shorts"),
    # ── warm (31-37°C) ─────────────────────────────────
    ("warm", "School",   "Warm"): ("Yellow Cropped Tee",     "Beige Linen Shorts"),
    ("warm", "School",   "Cool"): ("White Sleeveless Top",   "Light Denim Shorts"),
    ("warm", "Hang out", "Warm"): ("Orange Halter Top",      "Cream Linen Shorts"),
    ("warm", "Hang out", "Cool"): ("Striped Crop Top",       "Blue Denim Shorts"),
    ("warm", "Work out", "Warm"): ("Coral Sports Bra",       "Beige Biker Shorts"),
    ("warm", "Work out", "Cool"): ("Sky Blue Tank Top",      "Black Shorts"),
    # ── hot (38-44°C) ──────────────────────────────────
    ("hot",  "School",   "Warm"): ("White Spaghetti-strap",  "Beige Micro Shorts"),
    ("hot",  "School",   "Cool"): ("Ice Blue Tube Top",      "White Mini Skirt"),
    ("hot",  "Hang out", "Warm"): ("Lemon Halter Top",       "White Linen Shorts"),
    ("hot",  "Hang out", "Cool"): ("Baby Blue Crop Top",     "Light Denim Mini Skirt"),
    ("hot",  "Work out", "Warm"): ("Nude Sports Bra",        "Beige Micro Shorts"),
    ("hot",  "Work out", "Cool"): ("White Sports Crop Top",  "Lavender Biker Shorts"),
}


# 온도 숫자를 구간 문자열로 변환하는 함수
def get_temp_range(temp):
    if temp <= 25:          # 25도 이하 → cool 구간
        return "cool"
    elif temp <= 30:        # 26~30도 → mild 구간
        return "mild"
    elif temp <= 37:        # 31~37도 → warm 구간
        return "warm"
    else:                   # 38도 이상 → hot 구간
        return "hot"


# 이미지 파일 불러오기 (파일이 없으면 None 반환)
def load_image(path):
    try:
        return tk.PhotoImage(file=path)     # PNG 이미지를 tkinter 이미지 객체로 로드
    except:
        return None                         # 파일이 없거나 오류 시 None 반환


# ══════════════════════════════════════════════════════════
#  메인 앱 클래스
# ══════════════════════════════════════════════════════════
class DailyStylingApp:

    def __init__(self, root):
        self.root = root                            # tkinter 루트 창 참조 저장
        self.root.title("Daily Styling")            # 창 제목 설정
        self.root.geometry("480x700")               # 창 크기: 너비480 × 높이700
        self.root.resizable(False, False)           # 창 크기 조절 비활성화 (가로, 세로)
        self.root.configure(bg=BG)                  # 창 배경색 설정

        # 입력 상태 변수 (tkinter 전용 변수 – 입력창과 연결됨)
        self.username    = tk.StringVar(value="user")   # 이름 입력값, 기본값 "user"
        self.weather_var = tk.StringVar()               # 온도 입력값
        self.scene       = tk.StringVar()   # "School" / "Hang out" / "Work out"
        self.tone        = tk.StringVar()   # "Warm" / "Cool"

        # 현재 추천된 코디
        self.current_top    = ""    # 현재 추천 상의 이름
        self.current_bottom = ""    # 현재 추천 하의 이름

        # My Closet 뒤로가기용 – 어느 화면에서 왔는지 기억
        self.from_screen = "start"  # 클로짓 진입 전 화면 이름 ("start" 또는 "outfit")

        # 저장된 룩 목록 (파일에서 불러옴)
        self.saved_looks = self.load_closet()       # JSON 파일에서 저장된 룩 목록 로드

        # 이미지 저장 딕셔너리 (변수에 저장해 두지 않으면 이미지가 사라짐)
        self.images = {}                # 이미지 객체를 이름으로 관리하는 딕셔너리
        self.load_all_images()          # 모든 이미지 파일 미리 로드

        # Scene / Tone 버튼 저장 (선택 시 색상 바꾸려고)
        self.scene_btns = {}    # Scene 버튼 객체들을 이름으로 저장 {"School": btn, ...}
        self.tone_btns  = {}    # Tone 버튼 객체들을 이름으로 저장 {"Warm": btn, ...}

        # 첫 화면 표시
        self.show_start()       # 앱 시작 시 Start Screen 바로 표시


    # ──────────────────────────────────────────────────────
    #  이미지 불러오기
    #  이미지 인식 못하도록 잠시 폴더 경로 변경 
    # ──────────────────────────────────────────────────────
    def load_all_images(self):
        self.images["title"]      = load_image("images_1/title.png")       # 타이틀 이미지
        self.images["my_look"]    = load_image("images_1/my_look_btn.png") # My Look 버튼 이미지
        self.images["closet_btn"] = load_image("images_1/closet_btn.png")  # My Closet 버튼 이미지
        self.images["back"]       = load_image("images_1/back_btn.png")    # 뒤로가기 버튼 이미지

    # ──────────────────────────────────────────────────────
    #  클로짓 저장 / 불러오기
    # ──────────────────────────────────────────────────────
    def load_closet(self):
        # 저장 파일이 있으면 읽어옴, 없으면 빈 리스트 반환
        if os.path.exists(CLOSET_FILE):         # closet.json 파일이 존재하는지 확인
            try:
                with open(CLOSET_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)         # JSON 파일을 파이썬 리스트로 변환해서 반환
            except:
                return []                       # 파일이 손상됐거나 읽기 실패 시 빈 리스트
        return []                               # 파일 자체가 없으면 빈 리스트

    def save_closet(self):
        with open(CLOSET_FILE, "w", encoding="utf-8") as f:
            json.dump(self.saved_looks, f, ensure_ascii=False, indent=2)
            # ensure_ascii=False: 한글 등 유니코드 그대로 저장 / indent=2: 보기 좋게 들여쓰기

    # ──────────────────────────────────────────────────────
    #  공통: 화면 초기화 / My Closet 버튼
    # ──────────────────────────────────────────────────────
    def clear_screen(self):
        # 화면에 있는 모든 위젯 삭제
        for widget in self.root.winfo_children():   # 현재 창의 모든 자식 위젯 순회
            widget.destroy()                        # 위젯 하나씩 제거 (화면 전환 전 초기화)

    def make_closet_button(self):
        # 우측 상단의 My Closet 버튼 (이미지 있으면 이미지, 없으면 텍스트)
        img = self.images["closet_btn"]
        if img:                                     # 이미지 파일이 있으면 이미지 버튼 생성
            btn = tk.Button(self.root, image=img, bd=0, bg=BG,
                            cursor="hand2", command=self.show_closet)
        else:                                       # 이미지 없으면 텍스트 버튼으로 대체
            btn = tk.Button(self.root, text="My Closet",
                            font=("Arial", 10, "bold"),
                            bg=BTN_RED, fg="white", relief="flat",
                            padx=8, pady=4, cursor="hand2",
                            command=self.show_closet)
        btn.place(x=370, y=14)                      # 절대 좌표로 우측 상단에 배치

    # ══════════════════════════════════════════════════════
    #  1. Start Screen
    # ══════════════════════════════════════════════════════
    def show_start(self):
        self.from_screen = "start"      # 현재 화면을 "start"로 기록
        self.clear_screen()             # 기존 위젯 전부 삭제 후 새로 그리기

        # 버튼 선택 초기화
        self.scene.set("")              # Scene 선택값 초기화
        self.tone.set("")               # Tone 선택값 초기화
        self.scene_btns = {}            # Scene 버튼 딕셔너리 초기화
        self.tone_btns  = {}            # Tone 버튼 딕셔너리 초기화

        self.make_closet_button()       # 우측 상단 My Closet 버튼 배치

        # ── 타이틀 ──────────────────────────────────────
        title_img = self.images["title"]
        if title_img:                   # 타이틀 이미지가 있으면 이미지로 표시
            tk.Label(self.root, image=title_img, bg=BG).pack(pady=(50, 6))
        else:                           # 없으면 텍스트 타이틀로 대체
            tk.Label(self.root, text="Daily Styling",
                     font=("Georgia", 30, "bold"),
                     bg=BG, fg=TEXT_DARK).pack(pady=(60, 6))
            tk.Label(self.root, text="— Find Your Look —",
                     font=("Arial", 11, "italic"),
                     bg=BG, fg=TEXT_MID).pack(pady=(0, 10))

        # ── 유저 이름 입력 ──────────────────────────────
        frame_name = tk.Frame(self.root, bg=BG)     # 이름 입력 영역을 묶는 프레임
        frame_name.pack(pady=6)
        tk.Label(frame_name, text="Your Name :",
                 font=("Arial", 12), bg=BG, fg=TEXT_DARK).pack(side="left")
        tk.Entry(frame_name, textvariable=self.username,    # 입력 내용이 self.username에 연결됨
                 font=("Arial", 12), width=14,
                 relief="groove", bd=2).pack(side="left", padx=6)

        # ── 온도 입력 ───────────────────────────────────
        frame_weather = tk.Frame(self.root, bg=BG)  # 온도 입력 영역을 묶는 프레임
        frame_weather.pack(pady=6)
        tk.Label(frame_weather, text="Temperature (°C) :",
                 font=("Arial", 12), bg=BG, fg=TEXT_DARK).pack(side="left")
        tk.Entry(frame_weather, textvariable=self.weather_var,  # 입력 내용이 self.weather_var에 연결됨
                 font=("Arial", 12), width=6,
                 relief="groove", bd=2).pack(side="left", padx=6)

        # ── Scene 선택 버튼 3개 ─────────────────────────
        tk.Label(self.root, text="Scene",
                 font=("Arial", 13, "bold"),
                 bg=BG, fg=TEXT_DARK).pack(pady=(16, 4))

        frame_scene = tk.Frame(self.root, bg=BG)    # Scene 버튼 3개를 가로로 묶는 프레임
        frame_scene.pack()

        # Scene 버튼 3개를 각각 직접 생성
        btn_school = tk.Button(frame_scene, text="School",
                               font=("Arial", 11), width=10,
                               relief="groove", cursor="hand2",
                               command=self.on_scene_school)    # 클릭 시 on_scene_school 실행
        btn_school.pack(side="left", padx=5)
        self.scene_btns["School"] = btn_school

        btn_hangout = tk.Button(frame_scene, text="Hang out",
                                font=("Arial", 11), width=10,
                                relief="groove", cursor="hand2",
                                command=self.on_scene_hangout)  # 클릭 시 on_scene_hangout 실행
        btn_hangout.pack(side="left", padx=5)
        self.scene_btns["Hang out"] = btn_hangout

        btn_workout = tk.Button(frame_scene, text="Work out",
                                font=("Arial", 11), width=10,
                                relief="groove", cursor="hand2",
                                command=self.on_scene_workout)  # 클릭 시 on_scene_workout 실행
        btn_workout.pack(side="left", padx=5)
        self.scene_btns["Work out"] = btn_workout

        # ── Personal Tone 선택 버튼 2개 ────────────────
        tk.Label(self.root, text="Personal Tone",
                 font=("Arial", 13, "bold"),
                 bg=BG, fg=TEXT_DARK).pack(pady=(16, 4))

        frame_tone = tk.Frame(self.root, bg=BG)     # Tone 버튼 2개를 가로로 묶는 프레임
        frame_tone.pack()

        # Tone 버튼 2개를 각각 직접 생성
        btn_warm = tk.Button(frame_tone, text="Warm",
                             font=("Arial", 11), width=10,
                             relief="groove", cursor="hand2",
                             command=self.on_tone_warm)         # 클릭 시 on_tone_warm 실행
        btn_warm.pack(side="left", padx=5)
        self.tone_btns["Warm"] = btn_warm

        btn_cool = tk.Button(frame_tone, text="Cool",
                             font=("Arial", 11), width=10,
                             relief="groove", cursor="hand2",
                             command=self.on_tone_cool)         # 클릭 시 on_tone_cool 실행
        btn_cool.pack(side="left", padx=5)
        self.tone_btns["Cool"] = btn_cool

        # ── My Look 버튼 ────────────────────────────────
        my_look_img = self.images["my_look"]
        if my_look_img:                             # My Look 이미지가 있으면 이미지 버튼
            tk.Button(self.root, image=my_look_img, bd=0, bg=BG,
                      cursor="hand2",
                      command=self.on_my_look).pack(pady=28)
        else:                                       # 없으면 텍스트 버튼으로 대체
            tk.Button(self.root, text="✨  My Look  ✨",
                      font=("Arial", 14, "bold"),
                      bg=ACCENT, fg="white",
                      width=18, height=2, relief="flat",
                      cursor="hand2",
                      command=self.on_my_look).pack(pady=28)

    # ── Scene / Tone 버튼별 전용 메서드 ────────────────
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

    # Scene 버튼 클릭 – 선택된 버튼 색상 변경
    def select_scene(self, selected):
        self.scene.set(selected)                    # 선택된 Scene 값을 StringVar에 저장
        for name, btn in self.scene_btns.items():
            if name == selected:                    # 선택된 버튼: 강조색으로 변경
                btn.config(bg=ACCENT, fg="white", relief="sunken")
            else:                                   # 나머지 버튼: 기본 스타일로 초기화
                btn.config(bg="SystemButtonFace", fg="black", relief="groove")

    # Tone 버튼 클릭 – 선택된 버튼 색상 변경
    def select_tone(self, selected):
        self.tone.set(selected)                     # 선택된 Tone 값을 StringVar에 저장
        for name, btn in self.tone_btns.items():
            if name == selected:                    # 선택된 버튼: 강조색으로 변경
                btn.config(bg=ACCENT, fg="white", relief="sunken")
            else:                                   # 나머지 버튼: 기본 스타일로 초기화
                btn.config(bg="SystemButtonFace", fg="black", relief="groove")

    # My Look 버튼 클릭 → 유효성 검사 후 코디 화면으로 이동
    def on_my_look(self):
        # 1) 온도 숫자 확인
        temp_str = self.weather_var.get().strip()   # 입력값 앞뒤 공백 제거
        try:
            temp = int(temp_str)                    # 문자열을 정수로 변환
        except ValueError:                          # 숫자가 아닌 값이 입력된 경우
            messagebox.showwarning("Invalid Input",
                                   "Please enter a valid temperature.")
            return                                  # 함수 종료 (화면 전환 안 함)

        # 2) 온도 범위 확인 (-20 허용)
        if temp < -20 or temp > 45:                # DB에 없는 범위 차단
            messagebox.showwarning("Out of Range",
                                   "Temperature out of range.\nPlease check again.")
            return

        # 3) Scene 과 Tone 을 모두 선택했는지 확인
        if self.scene.get() == "" or self.tone.get() == "":    # 빈 문자열이면 미선택 상태
            messagebox.showwarning("Incomplete",
                                   "Please complete all sections.")
            return

        # 4) 코디 결정
        temp_range = get_temp_range(temp)                       # 온도 → 구간 문자열 변환
        key = (temp_range, self.scene.get(), self.tone.get())   # DB 조회 키 생성
        top, bottom = OUTFIT_DB.get(key, ("White T-shirt", "Blue Jeans"))
        # OUTFIT_DB에 키가 없을 경우 기본값 ("White T-shirt", "Blue Jeans") 사용
        self.current_top    = top       # 추천 상의 저장
        self.current_bottom = bottom    # 추천 하의 저장

        self.show_outfit()              # 코디 결과 화면으로 전환

    # ══════════════════════════════════════════════════════
    #  2. Outfit Screen
    # ══════════════════════════════════════════════════════
    def show_outfit(self):
        self.from_screen = "outfit"     # 현재 화면을 "outfit"으로 기록 (클로짓 뒤로가기용)
        self.clear_screen()             # 기존 위젯 삭제

        self.make_closet_button()       # 우측 상단 My Closet 버튼 배치

        # ── 제목 ────────────────────────────────────────
        name = self.username.get().strip() or "user"    # 이름이 비어 있으면 "user"로 대체
        tk.Label(self.root, text=f"{name}'s OOTD",      # f-string으로 이름 포함한 제목 생성
                 font=("Georgia", 24, "bold"),
                 bg=BG, fg=TEXT_DARK).pack(pady=(52, 18))

        # ── 상의 / 하의 카드 ────────────────────────────
        frame_outfit = tk.Frame(self.root, bg=BG)   # 상의·하의 카드를 나란히 배치할 프레임
        frame_outfit.pack(pady=6)

        tk.Label(frame_outfit, text="TOP",
                 font=("Arial", 11, "bold"),
                 bg=BG, fg=TEXT_GRAY).grid(row=0, column=0, padx=24)   # grid: 격자 배치
        tk.Label(frame_outfit, text="BOTTOM",
                 font=("Arial", 11, "bold"),
                 bg=BG, fg=TEXT_GRAY).grid(row=0, column=1, padx=24)

        tk.Label(frame_outfit, text=self.current_top,   # 추천 상의 이름 표시
                 font=("Arial", 11), bg=CARD_BG, fg=TEXT_DARK,
                 width=16, height=9, wraplength=130,     # wraplength: 130px 넘으면 줄바꿈
                 relief="groove").grid(row=1, column=0, padx=24, pady=8)

        tk.Label(frame_outfit, text=self.current_bottom,    # 추천 하의 이름 표시
                 font=("Arial", 11), bg="#D4C5B0", fg=TEXT_DARK,
                 width=16, height=9, wraplength=130,
                 relief="groove").grid(row=1, column=1, padx=24, pady=8)

        # ── 코디 이름 텍스트 ────────────────────────────
        tk.Label(self.root,
                 text=f"{self.current_top}  &  {self.current_bottom}",  # 상의 & 하의 한 줄 요약
                 font=("Arial", 12, "italic"),
                 bg=BG, fg=TEXT_MID,
                 wraplength=420).pack(pady=10)           # 420px 넘으면 자동 줄바꿈

        # ── 버튼 2개 ────────────────────────────────────
        btn_frame = tk.Frame(self.root, bg=BG)           # Save / Restart 버튼을 묶는 프레임
        btn_frame.pack(pady=22)

        tk.Button(btn_frame, text="💾  Save Look",
                  font=("Arial", 12, "bold"),
                  bg=ACCENT, fg="white",
                  width=13, height=2, relief="flat",
                  cursor="hand2",
                  command=self.save_look).pack(side="left", padx=10)    # 클릭 시 save_look 호출

        tk.Button(btn_frame, text="↩  Restart",
                  font=("Arial", 12),
                  bg=BTN_GRAY, fg="white",
                  width=13, height=2, relief="flat",
                  cursor="hand2",
                  command=self.show_start).pack(side="left", padx=10)   # 클릭 시 Start 화면으로

    # Save Look 버튼 클릭
    def save_look(self):
        # 클로짓이 꽉 찬 경우
        if len(self.saved_looks) >= MAX_LOOKS:          # 저장된 룩이 최대치(3개) 이상이면 차단
            messagebox.showinfo("Closet Full",
                                "Your closet is full.\n"
                                "Reset your closet to save more looks.")
            return

        # 룩 데이터를 딕셔너리로 만들어 리스트에 추가
        look = {
            "name":   self.username.get().strip() or "user",   # 이름 (빈값이면 "user")
            "top":    self.current_top,                         # 저장할 상의 이름
            "bottom": self.current_bottom,                      # 저장할 하의 이름
            "scene":  self.scene.get(),                         # 선택한 상황
            "tone":   self.tone.get(),                          # 선택한 톤
        }
        self.saved_looks.append(look)   # 리스트에 룩 추가
        self.save_closet()              # 변경된 리스트를 JSON 파일에 기록
        messagebox.showinfo("Saved!", "Your look is saved.")

    # ══════════════════════════════════════════════════════
    #  3. My Closet Screen
    # ══════════════════════════════════════════════════════
    def show_closet(self):
        prev = self.from_screen         # 뒤로가기할 화면 이름 저장 (show_closet 진입 전 화면)
        self.clear_screen()             # 기존 위젯 삭제

        # ── 뒤로가기 버튼 (좌측 상단) ──────────────────
        back_img = self.images["back"]
        if back_img:                    # 뒤로가기 이미지가 있으면 이미지 버튼
            tk.Button(self.root, image=back_img, bd=0, bg=BG,
                      cursor="hand2",
                      command=lambda: self.go_back(prev)).place(x=14, y=14)
        else:                           # 없으면 텍스트 버튼으로 대체
            tk.Button(self.root, text="← Back",
                      font=("Arial", 10, "bold"),
                      bg=BTN_GRAY, fg="white", relief="flat",
                      padx=8, pady=4, cursor="hand2",
                      command=lambda: self.go_back(prev)).place(x=14, y=14)
            # lambda: self.go_back(prev): prev 값을 캡처해서 클릭 시 전달

        # ── 제목 ────────────────────────────────────────
        tk.Label(self.root, text="My Closet",
                 font=("Georgia", 22, "bold"),
                 bg=BG, fg=TEXT_DARK).pack(pady=(52, 20))

        # ── 저장된 룩 목록 ──────────────────────────────
        if len(self.saved_looks) == 0:      # 저장된 룩이 없으면 안내 문구 표시
            tk.Label(self.root,
                     text="Your closet is empty.\nSave some looks first!",
                     font=("Arial", 13),
                     bg=BG, fg=TEXT_GRAY,
                     justify="center").pack(pady=60)
        else:
            for i in range(len(self.saved_looks)):  # 저장된 룩 개수만큼 카드 반복 생성
                look = self.saved_looks[i]          # i번째 룩 딕셔너리

                # 카드 프레임
                card = tk.Frame(self.root, bg=CARD_BG, bd=1, relief="groove")  # 룩 1개를 담는 카드
                card.pack(padx=40, pady=8, fill="x")    # fill="x": 가로로 꽉 채움

                tk.Label(card,
                         text=f"Look {i + 1}  ·  {look['scene']}  ·  {look['tone']}",
                         # 카드 헤더: 번호·상황·톤 표시
                         font=("Arial", 11, "bold"),
                         bg=CARD_BG, fg=TEXT_DARK).pack(anchor="w", padx=12, pady=(8, 2))
                         # anchor="w": 왼쪽 정렬
                tk.Label(card,
                         text=f"TOP     :  {look['top']}",      # 저장된 상의 이름
                         font=("Arial", 10),
                         bg=CARD_BG, fg=TEXT_MID).pack(anchor="w", padx=12)
                tk.Label(card,
                         text=f"BOTTOM :  {look['bottom']}",    # 저장된 하의 이름
                         font=("Arial", 10),
                         bg=CARD_BG, fg=TEXT_MID).pack(anchor="w", padx=12, pady=(0, 8))

        # ── Reset All 버튼 (하단) ────────────────────────
        tk.Button(self.root, text="Reset All",
                  font=("Arial", 12, "bold"),
                  bg=BTN_RED, fg="white",
                  width=14, height=2, relief="flat",
                  cursor="hand2",
                  command=self.reset_closet).pack(side="bottom", pady=28)
                  # side="bottom": 창 하단에 고정 배치

    # 뒤로가기 – 이전 화면으로 돌아감
    def go_back(self, screen):
        if screen == "outfit":      # 클로짓 진입 전 화면이 outfit이면 outfit으로
            self.show_outfit()
        else:                       # 아니면 start 화면으로
            self.show_start()

    # Reset All 버튼 클릭 – 확인 후 전체 삭제
    def reset_closet(self):
        answer = messagebox.askyesno(       # 예/아니오 확인 팝업 표시
            "Reset Closet",
            "Are you sure you want to delete all your looks?\n"
            "This action cannot be undone."
        )
        if answer:                          # 사용자가 "예"를 클릭한 경우에만 삭제
            self.saved_looks = []           # 메모리의 룩 목록 초기화
            self.save_closet()              # 빈 리스트를 파일에 덮어써서 영구 삭제
            self.show_closet()              # 화면 새로고침 (빈 클로짓 화면 재표시)


# ══════════════════════════════════════════════════════════
#  프로그램 실행
# ══════════════════════════════════════════════════════════
if __name__ == "__main__":          # 이 파일을 직접 실행할 때만 아래 코드 동작
    root = tk.Tk()                  # tkinter 루트 창 생성
    app = DailyStylingApp(root)     # 앱 객체 생성 (자동으로 __init__ 실행)
    root.mainloop()                 # GUI 이벤트 루프 시작 (창을 닫을 때까지 실행 유지)
