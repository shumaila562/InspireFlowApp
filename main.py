from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import random

# ---------- WINDOW ----------
Window.size = (420, 720)
Window.minimum_width = 360
Window.minimum_height = 640
Window.clearcolor = (0.05, 0.06, 0.09, 1)

# ---------- FONT ----------
# ถ้าขึ้นฟอนต์ error เปลี่ยนเป็น LeelawUI.ttf
LabelBase.register(name="TH", fn_regular=r"C:\Windows\Fonts\Tahoma.ttf")

# ---------- THEME (โทนใหม่สดขึ้น) ----------
THEME = {
    "panel": (0.13, 0.15, 0.20, 1),
    "title": (1.00, 0.98, 0.93, 1),
    "text":  (0.95, 0.93, 0.90, 1),
    "btn":   (0.12, 0.77, 0.66, 1),   # teal สด
    "btn_d": (0.10, 0.63, 0.54, 1),
    "btn2":  (0.96, 0.55, 0.25, 1),   # pinkสด (ปุ่มสวิตช์)
    "btn2d": (0.82, 0.42, 0.18, 1),
    "btn_t": (1, 1, 1, 1),
}

# ---------- UI HELPERS ----------
class Card(BoxLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.padding = 20
        self.spacing = 16
        with self.canvas.before:
            Color(0, 0, 0, 0.28)
            self._shadow = Rectangle(pos=(self.x+4, self.y-4), size=(self.width, self.height))
            Color(*THEME["panel"])
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *a):
        self._bg.pos = self.pos
        self._bg.size = self.size
        self._shadow.pos = (self.x+4, self.y-4)
        self._shadow.size = self.size

class SolidButton(Button):
    def __init__(self, color_main="btn", **kw):
        super().__init__(**kw)
        self._color_key = color_main
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = THEME["btn_t"]
        with self.canvas.before:
            Color(*THEME[self._color_key])
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._sync, size=self._sync, state=self._press)

    def _sync(self, *a):
        self._bg.pos = self.pos
        self._bg.size = self.size

    def _press(self, *a):
        self.canvas.before.clear()
        with self.canvas.before:
            active = self.state == "down"
            if self._color_key == "btn":
                Color(*(THEME["btn_d"] if active else THEME["btn"]))
            else:
                Color(*(THEME["btn2d"] if active else THEME["btn2"]))
            self._bg = Rectangle(pos=self.pos, size=self.size)
# ---------- DATA (แยกตาม group: student/worker และ language) ----------
ADVICE = {
    "th": {
        "student": {
            "stressed": [
                "พัก 5 นาทีแล้วค่อยลุยต่อ งานใหญ่แตกเป็นชิ้นเล็ก ๆ ได้ ",
            
                "นอนพอสำคัญกว่าฝืนอ่านทั้งคืน ",
            ],
            "lonely": [
                "ลองทักคนที่ไว้ใจได้สักคน—เพื่อน ครอบครัว หรือครู/ที่ปรึกษา ",
                "เข้าชมรมหรือกลุ่มเรียนย่อย จะได้มีเพื่อนร่วมทาง ",
                "จำไว้นะ คุณไม่ได้อยู่คนเดียว และสายด่วน 1323 ก็พร้อมช่วย ",
            ],
            "ok": [
                "เยี่ยม! ทำ 3 ข้อให้จบวันนี้ แล้วไปพัก ",
                "แชร์สรุปให้เพื่อนดูหน่อยไหม? ได้ทบทวนด้วย ",
                "วางแผนพรุ่งนี้ล่วงหน้า 5 นาที ช่วยได้เยอะ ",
            ],
        },
        "worker": {
            "stressed": [
                "โฟกัสงานเดียว 25 นาที (Pomodoro) แล้วพัก 5 นาที ⏱️",
                "เขียนสิ่งที่กังวลลงกระดาษ แล้วเลือกทำสิ่งแรกที่ง่ายสุด ✅",
                "ขอความช่วยเหลือได้—ไม่ได้แปลว่าอ่อนแอ 🤝",
            ],
            "lonely": [
                "คุยกับคนที่ไว้ใจได้สักคน—เพื่อนร่วมงาน เพื่อนสนิท หรือครอบครัว ☕",
                "เข้ากลุ่มสังคมเล็ก ๆ ในที่ทำงานหรือออนไลน์ก็ได้ 👥",
                "ถ้าหนักใจมาก โทร 1323 ได้ตลอด 24 ชม. เราอยู่ข้างคุณ 💛",
            ],
            "ok": [
                "เก่งมาก! ส่งต่อคำชมให้เพื่อนร่วมทีมสักคน 👍",
                "ปิดวันด้วยการขอบคุณตัวเอง 1 เรื่อง 🙏",
                "บันทึกความสำเร็จเล็ก ๆ ของวันนี้ไว้หน่อย ✍️",
            ],
        },
    },
    "en": {
        "student": {
            "stressed": [
                "Break 5 minutes, then tackle one small piece ✂️",
                "Skim the summary first, go deeper later — you’ve got this 💪",
                "Sleep beats all-nighters 😴",
            ],
            "lonely": [
                "Reach out to someone you trust — a friend, family, or advisor 👋",
                "Join a club or a small study group 🤝",
                "You are not alone. The 1323 hotline is there for you 📞",
            ],
            "ok": [
                "Nice! Finish 3 tiny tasks and rest 🌟",
                "Share your notes — you review while helping others 😊",
                "Plan tomorrow in 5 minutes 📅",
            ],
        },
        "worker": {
            "stressed": [
                "Pomodoro 25/5. One task only ⏱️",
                "Write worries down and do the easiest first ✅",
                "Asking for help ≠ weakness 🤝",
            ],
            "lonely": [
                "Talk to someone you trust — a colleague, close friend, or family ☕",
                "Join a small community online/offline 👥",
                "If it feels heavy, call 1323 anytime. You’re not alone 💛",
            ],
            "ok": [
                "Great! Send a shout-out to a teammate 👍",
                "End the day by thanking yourself for one thing 🙏",
                "Log today’s small wins ✍️",
            ],
        },
    },
}

        
    


BADGE_THRESHOLDS = [1, 3, 5]

# ---------- SCREENS ----------
class HomeScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        root = AnchorLayout(anchor_x='center', anchor_y='center', padding=16)
        card = Card(orientation='vertical', size_hint=(None, None), width=360, height=580)
        root.add_widget(card)

       
        top = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.16))
        # สวิตช์ภาษา
        self.lang = "th"
        self.lang_btn = SolidButton(text="ภาษา: ไทย", font_name="TH", font_size=18)
        self.lang_btn.bind(on_press=self.toggle_lang)
        # สวิตช์กลุ่มผู้ใช้
        self.group = "student"
        self.group_btn = SolidButton(text="กลุ่ม: นักเรียน", font_name="TH", font_size=18, color_main="btn2")
        self.group_btn.bind(on_press=self.toggle_group)

        top.add_widget(self.lang_btn)
        top.add_widget(self.group_btn)
        card.add_widget(top)

        self.stats = Label(text="Shared: 0 | Badge: -", font_name="TH", font_size=16, color=THEME["text"], size_hint=(1, 0.08))
        card.add_widget(self.stats)

        subtitle = Label(text="วันนี้คุณรู้สึกแบบไหน?", font_name="TH", font_size=22, color=THEME["text"],
                         halign="center", valign="middle", size_hint=(1, 0.15))
        subtitle.bind(size=lambda *a: setattr(subtitle, 'text_size', subtitle.size))
        card.add_widget(subtitle)

        moods = BoxLayout(orientation='vertical', spacing=12, size_hint=(1, 0.34))
        btn1 = SolidButton(text="เครียด / Stressed", font_name="TH", font_size=20)
        btn1.bind(on_press=lambda *_: self.go_result("stressed"))
        btn2 = SolidButton(text="เหงา / Lonely", font_name="TH", font_size=20)
        btn2.bind(on_press=lambda *_: self.go_result("lonely"))
        btn3 = SolidButton(text="โอเค / I’m OK", font_name="TH", font_size=20)
        btn3.bind(on_press=lambda *_: self.go_result("ok"))
        moods.add_widget(btn1); moods.add_widget(btn2); moods.add_widget(btn3)
        card.add_widget(moods)

        hotline = SolidButton(text="สายด่วนสุขภาพจิต 1323 (ฉุกเฉิน)", font_name="TH", font_size=18, size_hint=(1, 0.13))
        hotline.bind(on_press=self.show_hotline)
        card.add_widget(hotline)

        self.add_widget(root)

    def toggle_lang(self, *_):
        self.lang = "en" if self.lang == "th" else "th"
        self.lang_btn.text = "ภาษา: อังกฤษ" if self.lang == "en" else "ภาษา: ไทย"

    def toggle_group(self, *_):
        self.group = "worker" if self.group == "student" else "student"
        self.group_btn.text = "กลุ่ม: วัยทำงาน" if self.group == "worker" else "กลุ่ม: นักเรียน"

    def go_result(self, mood_key):
        app = App.get_running_app()
        app.current_lang = self.lang
        app.current_group = self.group
        app.current_mood = mood_key
        app.go_to_result()

    def show_hotline(self, *_):
        content = BoxLayout(orientation='vertical', padding=16, spacing=12)
        content.add_widget(Label(text="สายด่วนสุขภาพจิต 1323\nให้บริการ 24 ชั่วโมง", font_name="TH", font_size=18))
        ok = SolidButton(text="รับทราบ", font_name="TH", size_hint=(1, 0.4))
        popup = Popup(title="Hotline", content=content, size_hint=(0.8, 0.5), auto_dismiss=False)
        ok.bind(on_press=popup.dismiss)
        content.add_widget(ok)
        popup.open()

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        badge_text = "-" if app.badge_level == 0 else f"Lv.{app.badge_level}"
        self.stats.text = f"Shared: {app.shared_count} | Badge: {badge_text}"

class ResultScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        root = AnchorLayout(anchor_x='center', anchor_y='center', padding=16)
        self.card = Card(orientation='vertical', size_hint=(None, None), width=360, height=580)
        root.add_widget(self.card)

        self.title = Label(text="ผลลัพธ์วันนี้", font_name="TH", font_size=26, color=THEME["title"], size_hint=(1, 0.14))
        self.card.add_widget(self.title)

        self.msg = Label(text="...", font_name="TH", font_size=22, color=THEME["text"],
                         halign="center", valign="middle", size_hint=(1, 0.46))
        self.msg.bind(size=lambda *a: setattr(self.msg, 'text_size', self.msg.size))
        self.card.add_widget(self.msg)

        btns = BoxLayout(orientation='vertical', spacing=12, size_hint=(1, 0.28))
        share = SolidButton(text="ส่งต่อกำลังใจ / Share", font_name="TH", font_size=20)
        share.bind(on_press=self.share_advice)
        back = SolidButton(text="กลับหน้าแรก / Home", font_name="TH", font_size=18)
        back.bind(on_press=lambda *_: self.manager.transition_back())
        btns.add_widget(share); btns.add_widget(back)
        self.card.add_widget(btns)

        self.add_widget(root)

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        lang = app.current_lang or "th"
        group = app.current_group or "student"
        mood = app.current_mood or "ok"
        text = random.choice(ADVICE[lang][group][mood])
        self.msg.text = text

    def share_advice(self, *_):
        app = App.get_running_app()
        app.shared_count += 1
        level = 0
        for t in BADGE_THRESHOLDS:
            if app.shared_count >= t:
                level += 1
        app.badge_level = level

        content = BoxLayout(orientation='vertical', padding=16, spacing=12)
        content.add_widget(Label(
            text=f"ขอบคุณที่ส่งต่อกำลังใจ! 🎉\nแชร์แล้ว: {app.shared_count} ครั้ง\nBadge: {'Lv.'+str(level) if level>0 else '-'}",
            font_name="TH", font_size=18
        ))
        ok = SolidButton(text="ตกลง", font_name="TH", size_hint=(1, 0.4))
        popup = Popup(title="แชร์สำเร็จ", content=content, size_hint=(0.85, 0.55), auto_dismiss=False)
        ok.bind(on_press=popup.dismiss)
        content.add_widget(ok)
        popup.open()

# ---------- APP ----------
class InspireFlow(App):
    title = "Inspire App (Prototype)"

    def build(self):
        self.current_lang = "th"
        self.current_group = "student"
        self.current_mood = "ok"
        self.shared_count = 0
        self.badge_level = 0

        self.sm = FlowManager(transition=FadeTransition(duration=0.18))
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(ResultScreen(name="result"))
        return self.sm

    def go_to_result(self):
        self.sm.current = "result"

class FlowManager(ScreenManager):
    def transition_back(self):
        self.current = "home"

if __name__ == "__main__":
    InspireFlow().run()
