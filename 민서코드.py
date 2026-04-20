
import tkinter as tk
# [추가] messagebox : tkinter 안에 포함된 팝업창 모듈
# showwarning() → 경고 팝업  /  showinfo() → 정보 팝업
# 온도 범위 오류, 씬/톤 미선택 시 사용자에게 알림을 띄우기 위해 추가
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame

# ══════════════════════════════════════════════════════════
#  색상 상수
# ══════════════════════════════════════════════════════════
#위에다가 이 프로그램에서 사용할 모든 색상을 다 쓰면 global variable이 되어 그때그때 사용할 수 있게 됨.
BG = "#FFFFF"
ACCENT = "#C8A882"
TEXT_DARK = "#5C3D2E"
TEXT_MID = "#7A5C44"
TEXT_GRAY = "#AAAAAA"
BTN_RED = "#D4A5A5"

# [추가] 씬 / 퍼스널 톤 / 온도 카테고리 3가지를 조합한 키(tuple)로
# 추천 의상 (상의, 하의) 튜플을 값으로 저장하는 딕셔너리
# 키 구조 : (씬, 톤, 온도카테고리)
#   씬        : "School" / "Hang out" / "Work out"
#   톤        : "Warm" / "Cool"
#   온도 카테고리 : "hot"(25도↑) / "warm"(15~24도) / "cool"(5~14도) / "cold"(4도↓)
# 값 구조 : (상의 이름, 하의 이름)
# 결과값을 바꾸고 싶다면 해당 조합의 튜플 내용을 직접 수정하면 됩니다
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

#이미지 갖고 올 때마다 load_image 안 하기 위해 따로 뺀 거임. 한 번만 하기 위해서.
def load_image(path):
    try:
        return tk.PhotoImage(file=path)
    #path은 파일 경로이고 parameter이므로 이름 아무렇게나 설정해주면 됨. 밑에 이 입력값을 사용한 것과만 이름
    #맞추면 됨. *** parameter는 우리가 마음대로 이름 설정 가능!
    except:
        return None


# ══════════════════════════════════════════════════════════
#  메인 앱 클래스
# ══════════════════════════════════════════════════════════
class DailyStylingApp:

    #파이썬 클래스는 !!무조건!! init으로 정의를 먼저 내리고 변수를 써야 함.

    def __init__(self, root): #초기화 함수 #root 은 메인 창이고 self는 이 root과 설계도를 이용해서 만든 app임!  # self는 이 클래스에서 만들어지는 객체 자기 자신을 의미 (즉 app의 의미)
        self.root = root # 첫 번째 root은 속성값이고 두 번째 root은 우리가 맨 마지막에 만든 tkinter 창임/ 두 번째 root을 첫 번째 root에 지정하는 것임
        self.root.title("Daily Styling") #self에 root에 title을 설정
        self.root.geometry("480x700")  # 창!! 의 가로 세로 크기 설정
        self.root.resizable(False, False)  # 창 크기 조절 불가 설정 (가로, 세로 모두 False)
        self.root.config(bg=BG)  # 창의 배경색을 BG 상수(FFF8F0)로 설정

        # username과 weather_entry는 tkinter의 기능이 아니라
        # 클래스에서 직접 만들어서 사용하는 변수라 self.으로 관리
        # Entry 입력창 위젯 자체를 변수에 저장해두고 나중에 .get()으로 값을 읽음
        self.username_entry = None  # 일단 빈자리 예약, 이름 입력창 위젯 (show_start에서 생성 후 저장)
        self.weather_entry = None  # 온도 입력창 위젯 (show_start에서 생성 후 저장)

        # Scene·Tone은 입력창에 연결되지 않으므로 일반 문자열로 관리
        self.scene = ""  # 현재 선택된 Scene 값 ("School" / "Hang out" / "Work out")
        self.tone = ""  # 현재 선택된 Tone 값 ("Warm" / "Cool")
        #current top, bottom 뒤에 옷 결과 나올 때 쓸 거니까 이렇게 초기화를 해놓고 그때 가져다 쓰는 것임.
        # [추가] My Look 버튼 클릭 후 OUTFIT_DATA에서 조회한 상의 이름을 저장
        # show_outfit() 과 on_save_look() 에서 화면 표시 및 저장에 사용됨
        self.current_top = ""
        # [추가] My Look 버튼 클릭 후 OUTFIT_DATA에서 조회한 하의 이름을 저장
        # show_outfit() 과 on_save_look() 에서 화면 표시 및 저장에 사용됨
        self.current_bottom = ""

        self.images_title = None
        self.images_my_look = None
        self.images_closet_btn = None


        # load_all_images()에서 save_look_btn.png 로드 후 저장됨
        self.image_save_look_btn = None
        # [추가] 결과 화면의 Reset 버튼에 사용할 이미지를 담는 변수
        # load_all_images()에서 reset_btn.png 로드 후 저장됨
        self.image_reset_btn = None
        # [추가] 버튼 클릭 시 재생할 효과음 객체를 담는 변수
        # play_bgm()에서 Click.mp3 로드 후 저장되고, play_click_sound()에서 재생됨
        self.sfx_click = None
        self.load_all_images()
        self.play_bgm()
        self.scene_btns = {}
        self.tone_btns = {}

        self.show_start()

    # ──────────────────────────────────────────────────────
    #  이미지 불러오기
    # ──────────────────────────────────────────────────────
    def load_all_images(self): #이건 지금 pillow library 없이 tkinter에서 이미지 불러오는 함수임.
        try:
            self.images_title = ImageTk.PhotoImage(Image.open("images/DailyStyling_logo.png").resize((320, 100), Image.LANCZOS))
            self.images_my_look = ImageTk.PhotoImage(Image.open("images/MyLook_button_image.png").resize((200, 70), Image.LANCZOS))
            self.images_closet_btn = ImageTk.PhotoImage(Image.open("images/Hanger_button_image.png").resize((80, 40), Image.LANCZOS))
        except Exception as e:
            print("image error:", e)
            self.images_title=None
            self.images_my_look=None
            self.images_closet_btn=None
    #음악 로팅 함수
        # [변경1] BGM 파일명 변경 : sample.mp3 → dailystyling_bgm.mp3
        # [변경2] try/except 추가 : 사운드 파일이 없거나 환경 문제로 오류가 나도
        #         프로그램 전체가 종료되지 않고 오류 내용만 출력하고(컴퓨터만 볼 수 있음) 계속 실행됨
        # [추가] 클릭 효과음(Click.mp3) 로드 추가
        #        pygame.mixer.init()은 한 번만 호출해야 하므로 BGM 로드와 같은 블록에서 처리
        def play_bgm(self):
            try:
                pygame.mixer.init()  # 사운드 시스템 초기화 (1회만 실행)
                self.bgm = pygame.mixer.Sound("sounds/dailystyling_bgm.mp3")  # BGM 파일 로드
                self.bgm.play(loops=-1)  # loops=-1 : 무한 반복 재생
                self.sfx_click = pygame.mixer.Sound("sounds/Click.mp3")  # [추가] 클릭 효과음 로드 (재생은 play_click_sound()에서)
            except Exception as e:
                print("Sound error:", e)
            #Exception을 쓰면 추가적으로 문구를 줌. (왜 사운드 에러가 떴는지)
            #그리고 반드시 e에 저장해서 exception 써야 함.

    # [추가] My Look 버튼 클릭 시 효과음을 재생하는 메서드
     # sfx_click이 None(로드 실패)이면 아무것도 하지 않아서 오류가 나지 않음
    def play_click_sound(self):
        if self.sfx_click:
            self.sfx_click.play()

        # [변경] 이미지 로딩 방식 변경 : resize() → thumbnail()
        #   resize()  : 지정한 크기로 강제 변환 → 이미지 비율이 찌그러질 수 있음
        #   thumbnail(): 지정한 크기(박스) 안에 들어오도록 "비율을 유지하며" 축소
        #                원본이 이미 작으면 확대하지 않고 그대로 유지
        #   예) thumbnail((400, 120)) → 가로 최대 400, 세로 최대 120 안에 비율 유지하며 맞춤
        # [추가] Save Look 버튼 이미지(save_look_btn.png), Reset 버튼 이미지(reset_btn.png) 로드 추가
    #load all images 는 그냥 이미지 로딩하는 부분이고이미지를 화면에 띄우는 건 밑에서
    def load_all_images(self):
        try:
            img = Image.open("images/title.jpg")
            img.thumbnail((400, 120))
            self.image_title = ImageTk.PhotoImage(img)

            img = Image.open("images/my_look_btn.jpg")
            img.thumbnail((300, 80))
            self.image_my_look = ImageTk.PhotoImage(img)

            img = Image.open("images/closet_btn.jpg")
            img.thumbnail((80, 40))
            self.image_closet_btn = ImageTk.PhotoImage(img)

            img = Image.open("images/save_look_btn.png")  # [추가] Save Look 버튼 이미지 로드
            img.thumbnail((160, 60))
            self.image_save_look_btn = ImageTk.PhotoImage(img)

            img = Image.open("images/reset_btn.png")  # [추가] Reset 버튼 이미지 로드
            img.thumbnail((160, 60))
            self.image_reset_btn = ImageTk.PhotoImage(img)

        except Exception as e:
            print("Image error:", e)

    # My closet 버튼 만들기 (show_start에서 호출)
    def make_closet_button(self):
        img = self.images_closet_btn  #위에서 받은 closet image를 img라는 변수에 넣어준 것임
        # 이미지 파일이 있으면
        # command
        if img:
            btn = tk.Button(self.root, image=img, bd=0, bg=BG,
                            cursor="hand2", command=None)
            #cursor="hand2" 는 마우스 커서가 버튼 위에 있을 때 손가락 모양으로 바뀌도록 해주는 것
        # 이미지 파일이 없으면 이 else 부분은 다 삭제해도 됨.
        else:
            btn = tk.Button(self.root, text="My Closet",
                            font=("Arial", 10, "bold"),
                            bg=BTN_RED, fg="white", relief="flat",
                            padx=8, pady=4, cursor="hand2",
                            command=None)
        btn.place(x=370, y=14) #이 위치에 고정해줘 라는 뜻임.

# [추가] 화면 전환 시 현재 창에 올라가 있는 모든 위젯을 삭제하는 메서드
# winfo_children() : root 창의 자식 위젯(라벨, 버튼, 입력창 등) 전체를 리스트로 반환
# destroy()        : 위젯을 화면에서 완전히 제거
# show_start() → show_outfit() 처럼 화면이 전환될 때 이전 화면의 위젯이
# 남아서 새 화면과 겹치지 않도록 먼저 호출해서 깨끗하게 비워줌
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    #화면이 2개 이상 있을 때 (즉 화면 전환을 해야 할 때부터는) 필수적으로 들어감. 만약 없으면 두 화면의
    #위젯들이 겹쳐보임
    # ══════════════════════════════════════════════════════
    #  Start Screen
    # ══════════════════════════════════════════════════════
    def show_start(self):
        # [추가] 시작 화면을 다시 그리기 전에 현재 화면의 모든 위젯을 삭제
        # Reset 버튼으로 결과 화면 → 시작 화면으로 돌아올 때 위젯이 겹치는 것을 방지
        #화면 전환할 때마다 self.clear_screen()을 적어서 초기화 해놔야 함.
        self.clear_screen()
        self.scene = ""  # Scene 선택값 초기화 (빈 문자열 = 아무것도 선택 안 됨)
        self.tone = ""  # Tone 선택값 초기화
        self.scene_btns = {}  # Scene 버튼 딕셔너리 초기화
        self.tone_btns = {}  # Tone 버튼 딕셔너리 초기화

        self.make_closet_button()

        # ── 타이틀 ──────────────────────────────────────
        #입력창만 tk.Frame을 이용해주고 나머지는 scene, personal tone은 tk.Label, 나머지 버튼들은 tk.Button임
        title_img = self.images_title
        tk.Label(self.root, image=title_img, bg=BG).pack(pady=(50, 6))


        frame_name = tk.Frame(self.root, bg=BG)
        frame_name.pack(pady=6)
        tk.Label(frame_name, text="Your Name :",
                 font=("Arial", 12), bg=BG, fg=TEXT_DARK).pack(side="left")
        self.username_entry = tk.Entry(frame_name,
                                       font=("Arial", 12), width=14,
                                       relief="groove", bd=2)
        self.username_entry.insert(0, "user")
        self.username_entry.pack(side="left", padx=6)

        frame_weather = tk.Frame(self.root, bg=BG)
        frame_weather.pack(pady=6)
        tk.Label(frame_weather, text="Temperature (°C) :",
                 font=("Arial", 12), bg=BG, fg=TEXT_DARK).pack(side="left")
        self.weather_entry = tk.Entry(frame_weather,
                                      font=("Arial", 12), width=6,
                                      relief="groove", bd=2)
        self.weather_entry.pack(side="left", padx=6)

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

        my_look_img = self.image_my_look
        tk.Button(self.root, image=my_look_img, bd=0, bg=BG,
                      cursor="hand2",
                      # [변경] command를 lambda: None(아무것도 안 함) → on_my_look_click(실제 동작)으로 연결
                      command=self.on_my_look_click).pack(pady=28)


        # ── 유저 이름 입력 ──────────────────────────────
        frame_name = tk.Frame(self.root, bg=BG)
        frame_name.pack(pady=6)
        tk.Label(frame_name, text="Your Name :",
                 font=("Arial", 12), bg=BG, fg=TEXT_DARK).pack(side="left")
        self.username_entry = tk.Entry(frame_name,  # 입력창 위젯을 변수에 저장
                                       font=("Arial", 12), width=14,
                                       relief="groove", bd=2)  # relief는 테두리 스타일
        self.username_entry.insert(0, "user")  # 기본값 "user"를 입력창에 미리 채워넣기
        self.username_entry.pack(side="left", padx=6)

        # ── 온도 입력 ───────────────────────────────────
        frame_weather = tk.Frame(self.root, bg=BG)
        frame_weather.pack(pady=6)
        tk.Label(frame_weather, text="Temperature (°C) :",
                 font=("Arial", 12), bg=BG, fg=TEXT_DARK).pack(side="left")
        self.weather_entry = tk.Entry(frame_weather,  # 입력창 위젯을 변수에 저장
                                      font=("Arial", 12), width=6,
                                      relief="groove", bd=2)
        self.weather_entry.pack(side="left", padx=6)  # 기본값 없음 (빈칸으로 시작)
        #side left 는 label과 entry 를 왼쪽에서 오른쪽으로 정렬하는 것임.
        # ── Scene 선택 버튼 3개 ─────────────────────────
        tk.Label(self.root, text="Scene",
                 font=("Arial", 13, "bold"),
                 bg=BG, fg=TEXT_DARK).pack(pady=(20, 5))

        frame_scene = tk.Frame(self.root, bg=BG)
        frame_scene.pack()

        # cursor = hand2는 마우스 커서가 버튼 위에 있을 때 손가락 모양으로 바뀌도록 하는 옵션
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
        my_look_img = self.images_my_look
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

    # [추가] My Look 버튼을 눌렀을 때 실행되는 메서드
    # 아래 순서로 유효성 검사를 진행하고, 모두 통과하면 의상을 조회해 결과 화면으로 이동
    #
    # 1) 온도 입력값이 숫자인지 확인
    #    → int() 변환 실패 시 except 블록에서 경고 팝업 후 return으로 함수 종료
    # 2) 온도가 -20 ~ 45 범위 안인지 확인
    #    → 범위 벗어나면 경고 팝업 후 return
    # 3) 씬과 톤이 모두 선택됐는지 확인
    #    → 하나라도 ""(미선택)이면 경고 팝업 후 return
    # 4) 온도 숫자를 hot / warm / cool / cold 카테고리로 분류
    #    → 25도 이상 : hot  /  15~24도 : warm  /  5~14도 : cool  /  4도 이하 : cold
    # 5) OUTFIT_DATA[(씬, 톤, 온도카테고리)] 로 상의/하의 조회 후 저장
    # 6) 클릭 효과음 재생 → 결과 화면(show_outfit)으로 이동
    # return하면 함수가 중단되는 것임.
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

        if temp >= 25:
            temp_cat = "hot"
        elif temp >= 15:
            temp_cat = "warm"
        elif temp >= 5:
            temp_cat = "cool"
        else:
            temp_cat = "cold"
        self.current_top, self.current_bottom = OUTFIT_DATA[(self.scene, self.tone, temp_cat)]

        self.play_click_sound()
        self.show_outfit()

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
#scene에 있는 3개의 버튼 중 하나가 클릭되면 select_scene 함수가 호출되면서 scene이 선택됨
#(저 밑 줄에 selected 에 school/hang out/ work out 중에 하나가 들어가는 것임.)
# school, hangout, workout 버튼 중 하나가 클릭되면 select_scene 함수가 호출되면서 scene이 선택되고, tone 버튼도 마찬가지로 tone이 선택됨.
# dictionary사용 =>> scene_btns --> ["School": btn_school, "Hang out": btn_hangout, "Work out": btn_workout]
    def select_scene(self, selected):
        self.scene = selected  # 클릭된 버튼 이름을 그대로 변수에 저장 (일반 대입)
        for name, btn in self.scene_btns.items():  # 모든 Scene 버튼을 순회
            if name == selected:  # 방금 클릭한 버튼이면
                btn.config(bg=ACCENT, fg="white", relief="sunken")  # 강조 스타일 적용
            else:  # 나머지 버튼은
                btn.config(bg="SystemButtonFace", fg="black", relief="groove")  # 기본 스타일로 복원
# SystemButtonFace는 원래 값으로 돌아오는 것임.
    def select_tone(self, selected):
        self.tone = selected  # 클릭된 버튼 이름을 그대로 변수에 저장 (일반 대입)
        for name, btn in self.tone_btns.items():  # 모든 Tone 버튼을 순회
            if name == selected:  # 방금 클릭한 버튼이면
                btn.config(bg=ACCENT, fg="white", relief="sunken")  # 강조 스타일 적용
            else:  # 나머지 버튼은
                btn.config(bg="SystemButtonFace", fg="black", relief="groove")  # 버튼 기본  스타일로 복원

# [추가] Save Look 버튼 클릭 시 실행되는 메서드
    # showinfo() 로 저장 완료 팝업을 띄우며, 현재 추천된 상의/하의 이름을 함께 표시
    # 첫 번째 인자 "Saved!" 는 팝업창 제목, 두 번째 인자는 팝업창 내용
    def on_save_look(self):
        messagebox.showinfo("Saved!", f"Your look has been saved!\n\nTOP : {self.current_top}\nBOTTOM : {self.current_bottom}")

    # [추가] 의상 추천 결과 화면(OOTD 화면)을 구성하는 메서드
    # 구성 요소:
    #   - "{이름}'s OOTD" 타이틀 라벨
    #   - TOP / BOTTOM 컬럼 헤더 (grid 레이아웃)
    #   - 상의 / 하의 아이템 박스 (groove 테두리, grid 레이아웃으로 나란히 배치)
    #   - "상의  &  하의" 형식의 요약 텍스트 라벨
    #   - Save Look 버튼 : on_save_look() 호출 → 저장 완료 팝업 표시
    #   - Reset 버튼    : show_start() 호출 → 시작 화면으로 돌아가기
    def show_outfit(self):
        name = self.username_entry.get().strip() or "user"
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
                 width=16, height=9,
                 relief="groove").grid(row=1, column=0, padx=24, pady=8)

        tk.Label(frame_outfit, text=self.current_bottom,
                 font=("Arial", 11), bg=BG, fg=TEXT_DARK,
                 width=16, height=9,
                 relief="groove").grid(row=1, column=1, padx=24, pady=8)

        tk.Label(self.root,
                 text=f"{self.current_top}  &  {self.current_bottom}",
                 font=("Arial", 12, "italic"),
                 bg=BG, fg=TEXT_MID).pack(pady=10)

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
#  프로그램 실행
# ══════════════════════════════════════════════════════════
if __name__ == "__main__":  # 이 파일이 직접 실행될때만 아래 코드가 실행
    root = tk.Tk()  # Tkinter 기본 창 생성 , 모든 gui 요소는 이 root 창 위에 배치됨
    # 이걸 관리하기 위해서 root이라는 이름을 붙여줌
    # DailyStylingApp 클래스에
    # 앱이 표시될 tkinter 창(root)을 전달해서

    # app 변수로 저장하는 이유는 파이썬이 참조가 없는 객체는 메모리에서 자동으로 삭제,
    # app = 으로 붙잡아두지 않으면 바로 앱이 사라짐
    app = DailyStylingApp(root)

    # GUI 프로그램을 계속 실행상태로 유지
    root.mainloop()

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        것 부터 시작 그의 어린시절로 감