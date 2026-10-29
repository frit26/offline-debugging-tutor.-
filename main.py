__version__ = "0.1.0"
"""Offline Debugging Tutor - Kivy Android MVP.
This app analyzes code statically; it deliberately does not execute user code.
"""
from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from diagnostics import analyze_code

NAVY = (0.05, 0.14, 0.28, 1)
BLUE = (0.10, 0.43, 0.86, 1)
PALE = (0.93, 0.96, 1, 1)
WHITE = (1, 1, 1, 1)

SAMPLE = '''def add(a, b):\n    return a + b\n\nprint(add("5", 10))\n'''

class DebugTutorApp(App):
    title = "Offline Debugging Tutor"

    def build(self):
        Window.clearcolor = PALE
        self.hint_level = 0
        self.current_finding = None
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))
        header = Label(text="[b]Debug Tutor[/b]\n[color=4477bb]Learn • Debug • Improve • Offline[/color]", markup=True,
                       color=NAVY, size_hint_y=None, height=dp(65), font_size="20sp")
        root.add_widget(header)
        root.add_widget(Label(text="Paste Python code below. This MVP analyzes code but does not run it.",
                              color=NAVY, size_hint_y=None, height=dp(42), halign="left", valign="middle"))
        self.editor = TextInput(text=SAMPLE, multiline=True, size_hint_y=0.42, font_size="15sp",
                                background_color=WHITE, foreground_color=(0.08,0.1,0.15,1),
                                cursor_color=BLUE, padding=dp(10))
        root.add_widget(self.editor)
        buttons = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        analyze_btn = Button(text="Analyze Code", background_normal="", background_color=BLUE)
        analyze_btn.bind(on_release=self.analyze)
        sample_btn = Button(text="Load Example", background_normal="", background_color=NAVY)
        sample_btn.bind(on_release=self.load_example)
        buttons.add_widget(analyze_btn); buttons.add_widget(sample_btn)
        root.add_widget(buttons)
        self.results = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(6), padding=dp(4))
        self.results.bind(minimum_height=self.results.setter("height"))
        scroll = ScrollView(size_hint_y=0.58, do_scroll_x=False)
        scroll.add_widget(self.results)
        root.add_widget(scroll)
        self.show_welcome()
        return root

    def show_welcome(self):
        self.results.clear_widgets()
        self.add_text("Welcome!", 18, True)
        self.add_text("1. Enter or paste a Python snippet.\n2. Tap Analyze Code.\n3. Read the explanation and reveal hints one at a time.\n\nOffline rule-based analysis is active. Optional local AI is not included in this MVP yet.", 15)

    def add_text(self, text, size=14, bold=False):
        label = Label(text=(f"[b]{text}[/b]" if bold else text), markup=True, color=NAVY,
                      size_hint_y=None, halign="left", valign="top", font_size=f"{size}sp")
        label.bind(width=lambda inst, width: setattr(inst, "text_size", (width, None)))
        label.bind(texture_size=lambda inst, value: setattr(inst, "height", value[1] + dp(8)))
        self.results.add_widget(label)
        return label

    def add_button(self, text, callback):
        btn = Button(text=text, size_hint_y=None, height=dp(44), background_normal="", background_color=BLUE)
        btn.bind(on_release=callback)
        self.results.add_widget(btn)

    def load_example(self, *_):
        self.editor.text = SAMPLE

    def analyze(self, *_):
        self.results.clear_widgets()
        findings = analyze_code(self.editor.text)
        self.current_finding = findings[0]
        self.hint_level = 0
        f = self.current_finding
        self.add_text(f"{f['title']}" + (f" — line {f['line']}" if f.get('line') else ""), 18, True)
        self.add_text(f"Diagnostic type: {f['confidence']}", 12)
        self.add_text(f"Details: {f['message']}")
        self.add_text("Verified explanation library", 15, True)
        self.add_text(f["explanation"])
        self.add_text("Suggested next step", 15, True)
        self.add_text(f["fix"])
        self.add_button("Show next hint", self.next_hint)
        self.add_button("Show all hints", self.show_all_hints)
        self.add_text("Limitations: this is a beginner prototype. Heuristic findings may be false positives. It does not execute submitted code and cannot detect every logical or runtime error.", 12)

    def next_hint(self, *_):
        if not self.current_finding:
            return
        hints = self.current_finding["hints"]
        if self.hint_level >= len(hints):
            self.popup("Hints complete", "You have viewed all available hints for this finding.")
            return
        self.hint_level += 1
        self.add_text(f"Hint {self.hint_level} of {len(hints)}", 15, True)
        self.add_text(hints[self.hint_level - 1])

    def show_all_hints(self, *_):
        if not self.current_finding:
            return
        self.add_text("All hints", 15, True)
        for index, hint in enumerate(self.current_finding["hints"], 1):
            self.add_text(f"{index}. {hint}")
        self.hint_level = len(self.current_finding["hints"])

    def popup(self, title, message):
        content = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))
        content.add_widget(Label(text=message, color=NAVY))
        close = Button(text="Close", size_hint_y=None, height=dp(44))
        content.add_widget(close)
        pop = Popup(title=title, content=content, size_hint=(0.85, 0.4))
        close.bind(on_release=pop.dismiss)
        pop.open()

if __name__ == "__main__":
    DebugTutorApp().run()
