import tkinter as tk
# [추가] messagebox : tkinter 안에 포함된 팝업창 모듈
# showwarning() → 경고 팝업  /  showinfo() → 정보 팝업
# 온도 범위 오류, 씬/톤 미선택 시 사용자에게 알림을 띄우기 위해 추가
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame

# [변경] 배경색을 따뜻한 크림색(#FFF8F0)에서 흰색(#FFFFFF)으로 변경
BG        = "#FFFFFF"
ACCENT    = "#9B6F3A"
TEXT_DARK = "#5C3D2E"
TEXT_MID  = "#7A5C44"
TEXT_GRAY = "#AAAAAA"
BTN_RED   = "#D4A5A5"


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
        # [추가] My Look 버튼 클릭 후 OUTFIT_DATA에서 조회한 상의 이름을 저장
        # show_outfit() 과 on_save_look() 에서 화면 표시 및 저장에 사용됨
        self.current_top    = ""
        # [추가] My Look 버튼 클릭 후 OUTFIT_DATA에서 조회한 하의 이름을 저장
        # show_outfit() 과 on_save_look() 에서 화면 표시 및 저장에 사용됨
        self.current_bottom = ""

        self.image_title         = None
        self.image_my_look       = None
        self.image_closet_btn    = None
        # [추가] 결과 화면의 Save Look 버튼에 사용할 이미지를 담는 변수
        # load_all_images()에서 save_look_btn.png 로드 후 저장됨
        self.image_save_look_btn = None
        # [추가] 결과 화면의 Reset 버튼에 사용할 이미지를 담는 변수
        # load_all_images()에서 reset_btn.png 로드 후 저장됨
        self.image_reset_btn     = None
        # [추가] 버튼 클릭 시 재생할 효과음 객체를 담는 변수
        # play_bgm()에서 Click.mp3 로드 후 저장되고, play_click_sound()에서 재생됨
        self.sfx_click           = None
        self.load_all_images()
        self.play_bgm()

        self.scene_btns = {}
        self.tone_btns  = {}

        self.show_start()

    # [변경1] BGM 파일명 변경 : sample.mp3 → dailystyling_bgm.mp3
    # [변경2] try/except 추가 : 사운드 파일이 없거나 환경 문제로 오류가 나도
    #         프로그램 전체가 종료되지 않고 오류 내용만 출력하고 계속 실행됨
    # [추가] 클릭 효과음(Click.mp3) 로드 추가
    #        pygame.mixer.init()은 한 번만 호출해야 하므로 BGM 로드와 같은 블록에서 처리
    def play_bgm(self):
        try:
            pygame.mixer.init()                                            # 사운드 시스템 초기화 (1회만 실행)
            self.bgm = pygame.mixer.Sound("sounds/dailystyling.mp3")  # BGM 파일 로드
            self.bgm.play(loops=-1)                                        # loops=-1 : 무한 반복 재생
            self.sfx_click = pygame.mixer.Sound("sounds/Click.mp3")       # [추가] 클릭 효과음 로드 (재생은 play_click_sound()에서)
        except Exception as e:
            print("Sound error:", e)

    # [추가] My Look 버튼 클릭 시 효과음을 재생하는 메서드
    # sfx_click이 None(로드 실패)이면 아무것도 하지 않아서 오류가 나지 않음
    def play_click_sound(self):
        if self.sfx_click:
            self.sfx_click.play()

    # [변경] 이미지 로딩 방식 변경 : resize() → thumbnail()
    #   resize()  : 지정한 크기로 강제 변환 → 이미지 비율이 찌그러질 수 있음
    #   thumbnail(): 지정한 크기(박스) 안에 들어오도록 비율을 유지하며 축소
    #                원본이 이미 작으면 확대하지 않고 그대로 유지
    #   예) thumbnail((400, 120)) → 가로 최대 400, 세로 최대 120 안에 비율 유지하며 맞춤
    # [추가] Save Look 버튼 이미지(save_look_btn.png), Reset 버튼 이미지(reset_btn.png) 로드 추가
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

            img = Image.open("images/reset_btn.png")      # [추가] Reset 버튼 이미지 로드
            img.thumbnail((160, 60))
            self.image_reset_btn = ImageTk.PhotoImage(img)

        except Exception as e:
            print("Image error:", e)

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

    # [추가] 화면 전환 시 현재 창에 올라가 있는 모든 위젯을 삭제하는 메서드
    # winfo_children() : root 창의 자식 위젯(라벨, 버튼, 입력창 등) 전체를 리스트로 반환
    # destroy()        : 위젯을 화면에서 완전히 제거
    # show_start() → show_outfit() 처럼 화면이 전환될 때 이전 화면의 위젯이
    # 남아서 새 화면과 겹치지 않도록 먼저 호출해서 깨끗하게 비워줌
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_start(self):
        # [추가] 시작 화면을 다시 그리기 전에 현재 화면의 모든 위젯을 삭제
        # Reset 버튼으로 결과 화면 → 시작 화면으로 돌아올 때 위젯이 겹치는 것을 방지
        self.clear_screen()
        self.scene = ""
        self.tone  = ""
        self.scene_btns = {}
        self.tone_btns  = {}

        self.make_closet_button()

        title_img = self.image_title
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
                    command=self.on_my_look_click).pack(pady=28)

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
        elif temp >= 17:
            temp_cat = "warm"
        elif temp >= 9:
            temp_cat = "cool"
        else:
            temp_cat = "cold"

        self.current_top, self.current_bottom = OUTFIT_DATA[(self.scene, self.tone, temp_cat)]

        self.play_click_sound()
        self.show_outfit()

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
    
        tk.Button(btn_frame, image=self.image_save_look_btn, bd=0, bg=BG, cursor="hand2",
                      command=self.on_save_look).pack(side="left", padx=10)

        tk.Button(btn_frame, image=self.image_reset_btn, bd=0, bg=BG, cursor="hand2",
                      command=self.show_start).pack(side="left", padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = DailyStylingApp(root)
    root.mainloop()
