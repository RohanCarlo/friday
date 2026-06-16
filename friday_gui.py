# friday_gui.py - JARVIS-style GUI for FRIDAY
# Place this in G:\friday\friday_gui.py
# Run this instead of main.py directly

import tkinter as tk
import threading
import math
import time
import random

class FridayGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("F.R.I.D.A.Y.")
        self.root.configure(bg="#000000")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Try to remove window borders for full sci-fi look
        self.root.overrideredirect(False)

        # Colors
        self.CYAN       = "#00d4ff"
        self.CYAN_DIM   = "#005566"
        self.CYAN_DARK  = "#001a22"
        self.WHITE      = "#e0f7ff"
        self.GREEN      = "#00ff88"
        self.RED        = "#ff4444"
        self.BG         = "#000000"
        self.PANEL      = "#030d12"

        # State
        self.status_text   = "INITIALIZING..."
        self.listening     = False
        self.speaking      = False
        self.last_heard    = ""
        self.last_response = ""
        self.angle         = 0
        self.pulse         = 0
        self.ring_angles   = [0, 120, 240]
        self.particles     = [(random.randint(0,800), random.randint(0,600), random.random()) for _ in range(40)]
        self.bars          = [random.random() for _ in range(32)]
        self.running       = True

        self._build_ui()
        self._animate()

    def _build_ui(self):
        # ── Main canvas ──────────────────────────────────────────
        self.canvas = tk.Canvas(
            self.root, width=800, height=600,
            bg=self.BG, highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # ── Bottom status bar ─────────────────────────────────────
        self.bar_frame = tk.Frame(self.root, bg="#000d12", height=36)
        self.bar_frame.pack(fill="x", side="bottom")

        self.status_label = tk.Label(
            self.bar_frame, text="● SYSTEM ONLINE",
            font=("Courier New", 9, "bold"),
            fg=self.GREEN, bg="#000d12", padx=12
        )
        self.status_label.pack(side="left")

        self.time_label = tk.Label(
            self.bar_frame, text="",
            font=("Courier New", 9),
            fg=self.CYAN_DIM, bg="#000d12", padx=12
        )
        self.time_label.pack(side="right")

        # ── Last heard / last response labels ────────────────────
        self.heard_var    = tk.StringVar(value="")
        self.response_var = tk.StringVar(value="")

    # ─────────────────────────────────────────────────────────────
    def _animate(self):
        if not self.running:
            return
        c = self.canvas
        c.delete("all")

        W, H = 800, 600
        cx, cy = 400, 280

        # ── Starfield ────────────────────────────────────────────
        for i, (px, py, spd) in enumerate(self.particles):
            px = (px + spd * 0.4) % W
            self.particles[i] = (px, py, spd)
            alpha = int(spd * 180)
            col = f"#{alpha:02x}{min(alpha+40,255):02x}{min(alpha+60,255):02x}"
            c.create_oval(px-1, py-1, px+1, py+1, fill=col, outline="")

        # ── Outer decorative rings ───────────────────────────────
        for r, col, dash in [
            (240, self.CYAN_DIM, (4,8)),
            (220, "#003344", (2,12)),
        ]:
            c.create_oval(cx-r, cy-r, cx+r, cy+r,
                          outline=col, width=1, dash=dash)

        # ── Rotating arc segments ────────────────────────────────
        self.angle = (self.angle + 1.2) % 360
        for i, base in enumerate(self.ring_angles):
            self.ring_angles[i] = (base + [0.8, -1.1, 0.6][i]) % 360
            a = self.ring_angles[i]
            for radius, extent, col, w in [
                (200, 55, self.CYAN, 2),
                (185, 30, "#007799", 1),
                (170, 70, "#004455", 1),
            ]:
                c.create_arc(
                    cx-radius, cy-radius, cx+radius, cy+radius,
                    start=a, extent=extent,
                    outline=col, width=w, style="arc"
                )

        # ── Pulse ring ───────────────────────────────────────────
        self.pulse = (self.pulse + 0.05) % (2 * math.pi)
        pulse_r = 155 + math.sin(self.pulse) * 8
        alpha   = int(120 + math.sin(self.pulse) * 100)
        pc = f"#00{alpha:02x}{min(alpha+55,255):02x}"
        c.create_oval(cx-pulse_r, cy-pulse_r, cx+pulse_r, cy+pulse_r,
                      outline=pc, width=2)

        # ── Core circle ──────────────────────────────────────────
        core_r = 110
        c.create_oval(cx-core_r, cy-core_r, cx+core_r, cy+core_r,
                      fill=self.CYAN_DARK, outline=self.CYAN, width=2)

        # ── FRIDAY text inside core ───────────────────────────────
        c.create_text(cx, cy-28, text="F.R.I.D.A.Y.",
                      font=("Courier New", 14, "bold"),
                      fill=self.CYAN)
        c.create_text(cx, cy-6, text="ARTIFICIAL INTELLIGENCE",
                      font=("Courier New", 7),
                      fill=self.CYAN_DIM)

        # Status dot + text
        dot_col = self.GREEN if not self.speaking else self.CYAN
        if self.listening:
            dot_col = "#ffaa00"
        c.create_oval(cx-28, cy+12, cx-20, cy+20,
                      fill=dot_col, outline="")
        c.create_text(cx+8, cy+16,
                      text=self.status_text,
                      font=("Courier New", 8, "bold"),
                      fill=dot_col, anchor="w")

        # ── Audio visualizer bars ────────────────────────────────
        bar_w   = 6
        bar_gap = 3
        total   = len(self.bars) * (bar_w + bar_gap)
        bx      = cx - total // 2
        by      = cy + 50

        for i, h in enumerate(self.bars):
            # Animate bars
            if self.listening or self.speaking:
                self.bars[i] = min(1.0, max(0.05,
                    h + random.uniform(-0.15, 0.15)))
            else:
                self.bars[i] = max(0.03, h * 0.92)

            bar_h  = int(h * 55) + 3
            x0     = bx + i * (bar_w + bar_gap)
            bright = int(100 + h * 155)
            bc     = f"#00{bright:02x}{min(bright+55,255):02x}"
            c.create_rectangle(x0, by - bar_h, x0 + bar_w, by,
                                fill=bc, outline="")

        # ── Corner HUD decorations ───────────────────────────────
        for (x1,y1,x2,y2) in [(10,10,60,10),(10,10,10,60),
                                (740,10,790,10),(790,10,790,60),
                                (10,540,10,590),(10,590,60,590),
                                (740,590,790,590),(790,540,790,590)]:
            c.create_line(x1,y1,x2,y2, fill=self.CYAN, width=2)

        # ── Heard / response text area ───────────────────────────
        if self.last_heard:
            c.create_text(400, 430,
                          text=f"YOU  ›  {self.last_heard[:70]}",
                          font=("Courier New", 9),
                          fill="#ffaa00", anchor="center")

        if self.last_response:
            # Word wrap at 80 chars
            words  = self.last_response.split()
            lines  = []
            line   = ""
            for w in words:
                if len(line) + len(w) + 1 > 80:
                    lines.append(line)
                    line = w
                else:
                    line += (" " if line else "") + w
            if line:
                lines.append(line)
            for i, ln in enumerate(lines[:3]):
                c.create_text(400, 458 + i*18,
                              text=f"FRIDAY  ›  {ln}" if i == 0 else f"           {ln}",
                              font=("Courier New", 9),
                              fill=self.CYAN, anchor="center")

        # ── Scan line effect ─────────────────────────────────────
        scan_y = int((time.time() * 80) % H)
        c.create_line(0, scan_y, W, scan_y,
                      fill="#00ffff", width=1,
                      stipple="gray25")

        # ── Bottom grid lines ────────────────────────────────────
        for i in range(0, W, 40):
            c.create_line(i, 540, i, 560,
                          fill=self.CYAN_DIM, width=1, dash=(2,6))

        # ── Time ─────────────────────────────────────────────────
        self.time_label.config(
            text=time.strftime("  %H:%M:%S  |  %d %b %Y  ")
        )

        self.root.after(33, self._animate)   # ~30 fps

    # ─────────────────────────────────────────────────────────────
    # Public methods called by main.py
    # ─────────────────────────────────────────────────────────────
    def set_sleeping(self):
        self.status_text = "SLEEPING  —  SAY 'HI FRIDAY'"
        self.listening   = False
        self.speaking    = False

    def set_listening(self):
        self.status_text = "LISTENING..."
        self.listening   = True
        self.speaking    = False

    def set_speaking(self, text=""):
        self.status_text   = "SPEAKING..."
        self.speaking      = True
        self.listening     = False
        if text:
            self.last_response = text

    def set_processing(self):
        self.status_text = "PROCESSING..."
        self.listening   = False
        self.speaking    = False

    def set_heard(self, text):
        self.last_heard = text

    def stop(self):
        self.running = False
        self.root.destroy()

    def run(self):
        self.root.mainloop()


# ── Standalone test ───────────────────────────────────────────────
if __name__ == "__main__":
    gui = FridayGUI()
    gui.set_sleeping()
    gui.run()