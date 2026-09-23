"""Generate the animated SVGs for the profile README (hero + terminal)."""
import html
import math
import random
import sys
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)
random.seed(73453971)  # GitHub user id — deterministic starfield

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"


def esc(s):
    return html.escape(s, quote=True)


# --------------------------------------------------------------------- hero
def hero():
    W, H = 1000, 320
    px, py, pr = 815, 165, 58  # planet
    orbit = 118

    stars = []
    for _ in range(140):
        x, y = random.uniform(0, W), random.uniform(0, H)
        r = random.choice([0.5, 0.6, 0.8, 1.0, 1.2, 1.5])
        d = random.uniform(0, 4)
        t = random.uniform(2.2, 5)
        stars.append(
            f'<circle class="s" cx="{x:.1f}" cy="{y:.1f}" r="{r}" '
            f'style="animation-delay:-{d:.2f}s;animation-duration:{t:.2f}s"/>'
        )

    shooting = []
    for i, (x, y, delay) in enumerate([(120, -20, 0), (520, -30, 4.5), (300, -40, 9)]):
        shooting.append(
            f'<g class="shoot" style="animation-delay:{delay}s">'
            f'<line x1="{x}" y1="{y}" x2="{x - 90}" y2="{y - 45}" stroke="url(#trail)" '
            f'stroke-width="2" stroke-linecap="round"/></g>'
        )

    techs = [
        ("React", "#61dafb"),
        ("TypeScript", "#3b82f6"),
        ("Node.js", "#6cc24a"),
        ("Next.js", "#e6edf3"),
        ("Django", "#44b78b"),
        ("AWS", "#ff9900"),
        ("PostgreSQL", "#7dd3fc"),
    ]
    orbiters = []
    for i, (name, color) in enumerate(techs):
        a = math.radians(i * 360 / len(techs) - 90)
        ox, oy = px + orbit * math.cos(a), py + orbit * math.sin(a)
        w = len(name) * 7.4 + 18
        orbiters.append(
            f'<g class="upright">'
            f'<rect x="{ox - w / 2:.1f}" y="{oy - 11:.1f}" width="{w:.1f}" height="22" rx="11" '
            f'fill="#0b1026" fill-opacity="0.85" stroke="{color}" stroke-opacity="0.9"/>'
            f'<circle cx="{ox - w / 2 + 10:.1f}" cy="{oy:.1f}" r="3" fill="{color}"/>'
            f'<text x="{ox + 5:.1f}" y="{oy + 4:.1f}" text-anchor="middle" fill="#e6edf3" '
            f'font-family="{MONO}" font-size="12">{name}</text></g>'
        )

    headline = "Hi, I'm Bahir Hakimi"
    fs = 44
    cw = fs * 0.6
    n = len(headline)
    type_start, per_char = 1.2, 0.09
    steps = ";".join(f"{i * cw:.1f}" for i in range(n + 1)) + f";{n * cw + 40:.1f}"
    keyt = ";".join(f"{i / (n + 1):.4f}" for i in range(n + 2))
    type_dur = per_char * (n + 1)
    type_end = type_start + type_dur

    roles = [
        "Senior Full Stack Engineer",
        "Building hr.jobs.af @ NETLINKS",
        "TypeScript × React × Node × Django",
        "Chess player · Space nerd",
    ]
    role_cycle = 3.2 * len(roles)
    role_texts = []
    for i, role in enumerate(roles):
        role_texts.append(
            f'<text class="role" x="62" y="208" style="animation-delay:{type_end + i * 3.2:.2f}s">'
            f'<tspan fill="#22d3ee">▸ </tspan>{esc(role)}</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Hi, I'm Bahir Hakimi — Full-Stack Developer from Kabul">
<title>Hi, I'm Bahir Hakimi</title>
<defs>
  <radialGradient id="bg" cx="30%" cy="20%" r="100%">
    <stop offset="0" stop-color="#141a3d"/><stop offset="0.55" stop-color="#080b1f"/><stop offset="1" stop-color="#03040b"/>
  </radialGradient>
  <radialGradient id="planet" cx="35%" cy="30%" r="75%">
    <stop offset="0" stop-color="#fcd34d"/><stop offset="0.45" stop-color="#f97316"/><stop offset="1" stop-color="#4c1d95"/>
  </radialGradient>
  <linearGradient id="trail" x1="1" y1="1" x2="0" y2="0">
    <stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="grad" x1="0" x2="1">
    <stop offset="0" stop-color="#a78bfa"/><stop offset="0.5" stop-color="#22d3ee"/><stop offset="1" stop-color="#34d399"/>
  </linearGradient>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="38"/></filter>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <clipPath id="typed"><rect x="60" y="100" height="70" width="0">
    <animate attributeName="width" begin="{type_start}s" dur="{type_dur:.2f}s" values="{steps}" keyTimes="{keyt}" calcMode="discrete" fill="freeze"/>
  </rect></clipPath>
  <clipPath id="ringFront"><rect x="{px - 120}" y="{py}" width="240" height="120"/></clipPath>
</defs>
<style>
  .s {{ fill:#fff; animation: tw 3s ease-in-out infinite alternate; }}
  @keyframes tw {{ from {{ opacity:.15 }} to {{ opacity:1 }} }}
  .neb {{ animation: drift 18s ease-in-out infinite alternate; transform-box: view-box; }}
  @keyframes drift {{ from {{ transform: translate(-20px,-10px) }} to {{ transform: translate(30px,15px) }} }}
  .shoot {{ opacity:0; animation: shoot 13.5s linear infinite; }}
  @keyframes shoot {{ 0% {{ opacity:0; transform:translate(0,0) }} 2% {{ opacity:1 }} 9% {{ opacity:0; transform:translate(260px,130px) }} 100% {{ opacity:0; transform:translate(260px,130px) }} }}
  .orbit {{ animation: spin 40s linear infinite; transform-box: view-box; transform-origin: {px}px {py}px; }}
  .upright {{ animation: spin 40s linear infinite reverse; transform-box: fill-box; transform-origin: center; }}
  @keyframes spin {{ to {{ transform: rotate(360deg) }} }}
  .float {{ animation: float 6s ease-in-out infinite alternate; }}
  @keyframes float {{ from {{ transform: translateY(-4px) }} to {{ transform: translateY(4px) }} }}
  .hud {{ animation: blink 1.6s steps(2, jump-none) infinite; }}
  @keyframes blink {{ 50% {{ opacity:.35 }} }}
  .cursor {{ animation: caret 1s steps(1) infinite; }}
  @keyframes caret {{ 50% {{ opacity:0 }} }}
  .wave {{ opacity:0; transform-box: fill-box; transform-origin: 70% 80%;
           animation: show .3s {type_end:.2f}s forwards, wave 2.4s {type_end:.2f}s ease-in-out infinite; }}
  @keyframes show {{ to {{ opacity:1 }} }}
  @keyframes wave {{ 0%,60%,100% {{ transform: rotate(0) }} 10%,30% {{ transform: rotate(16deg) }} 20%,40% {{ transform: rotate(-8deg) }} }}
  .role {{ opacity:0; font: 600 22px {SANS}; fill:url(#grad);
           animation: role {role_cycle:.1f}s linear infinite; }}
  @keyframes role {{ 0% {{ opacity:0; transform:translateY(8px) }} 4% {{ opacity:1; transform:translateY(0) }}
                    21% {{ opacity:1; transform:translateY(0) }} 25% {{ opacity:0; transform:translateY(-8px) }} 100% {{ opacity:0 }} }}
  .fade {{ opacity:0; animation: show 1s {type_end + 0.3:.2f}s forwards; }}
</style>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <g class="neb" filter="url(#blur)">
    <ellipse cx="640" cy="90" rx="190" ry="90" fill="#7c3aed" opacity=".45"/>
    <ellipse cx="880" cy="270" rx="170" ry="80" fill="#0ea5e9" opacity=".3"/>
    <ellipse cx="180" cy="300" rx="200" ry="70" fill="#db2777" opacity=".2"/>
  </g>
  {"".join(stars)}
  {"".join(shooting)}

  <!-- rocket on a lazy arc across the sky -->
  <g>
    <g transform="rotate(90)">
      <path d="M0,-11 C5,-6 5,4 4,8 L-4,8 C-5,4 -5,-6 0,-11 Z" fill="#e5e7eb"/>
      <circle cx="0" cy="-2" r="2" fill="#38bdf8"/>
      <path d="M-4,4 L-8,10 L-4,8 Z M4,4 L8,10 L4,8 Z" fill="#f43f5e"/>
      <path d="M-2.5,8 L0,16 L2.5,8 Z" fill="#fbbf24"><animate attributeName="d" dur="0.15s" repeatCount="indefinite" values="M-2.5,8 L0,16 L2.5,8 Z;M-2.5,8 L0,20 L2.5,8 Z;M-2.5,8 L0,16 L2.5,8 Z"/></path>
    </g>
    <animateMotion dur="16s" begin="3s" repeatCount="indefinite" rotate="auto" keyPoints="0;1;1" keyTimes="0;0.55;1" calcMode="linear"
      path="M-40,70 C200,10 420,20 560,60 S820,40 1060,10"/>
  </g>

  <!-- planet + orbiting stack -->
  <circle cx="{px}" cy="{py}" r="{orbit}" fill="none" stroke="#94a3b8" stroke-opacity=".25" stroke-dasharray="3 6"/>
  <g class="float">
    <circle cx="{px}" cy="{py}" r="{pr + 14}" fill="#f97316" opacity=".25" filter="url(#glow)"/>
    <ellipse cx="{px}" cy="{py}" rx="{pr + 36}" ry="14" fill="none" stroke="#fde68a" stroke-opacity=".55" stroke-width="5" transform="rotate(-18 {px} {py})"/>
    <circle cx="{px}" cy="{py}" r="{pr}" fill="url(#planet)"/>
    <path d="M{px - 45},{py - 20} q45,-14 90,0 M{px - 52},{py + 6} q52,-12 104,0 M{px - 40},{py + 30} q40,-10 80,0" stroke="#fff" stroke-opacity=".12" stroke-width="5" fill="none"/>
    <ellipse cx="{px}" cy="{py}" rx="{pr + 36}" ry="14" fill="none" stroke="#fde68a" stroke-opacity=".75" stroke-width="5" transform="rotate(-18 {px} {py})" clip-path="url(#ringFront)"/>
  </g>
  <g class="orbit">{"".join(orbiters)}</g>

  <!-- text -->
  <text class="hud" x="62" y="78" fill="#22d3ee" font-family="{MONO}" font-size="13" letter-spacing="1.5">&gt; INCOMING TRANSMISSION · KABUL 34.55°N 69.21°E</text>
  <g clip-path="url(#typed)">
    <text x="62" y="150" fill="#f8fafc" font-family="{MONO}" font-size="{fs}" font-weight="700">{esc(headline)}</text>
  </g>
  <rect class="cursor" x="62" y="114" width="4" height="44" fill="#22d3ee" opacity="0">
    <animate attributeName="x" begin="{type_start}s" dur="{type_dur:.2f}s" values="{';'.join(f'{62 + i * cw + 4:.1f}' for i in range(n + 1))};{62 + n * cw + 4:.1f}" keyTimes="{keyt}" calcMode="discrete" fill="freeze"/>
    <set attributeName="opacity" to="1" begin="0.2s"/>
    <set attributeName="opacity" to="0" begin="{type_end:.2f}s"/>
  </rect>
  <text class="wave" x="{62 + n * cw + 12:.0f}" y="148" font-size="38">👋</text>
  {"".join(role_texts)}
  <g class="fade" font-family="{MONO}" font-size="13" fill="#94a3b8">
    <text x="62" y="262">📍 Kabul, Afghanistan   ·   🌐 bahir.dev   ·   ♟️ scroll down, it's your move</text>
  </g>
  <!-- HUD corners -->
  <g stroke="#22d3ee" stroke-opacity=".6" stroke-width="2" fill="none">
    <path d="M22,44 V22 H44"/><path d="M{W - 44},22 H{W - 22} V44"/>
    <path d="M22,{H - 44} V{H - 22} H44"/><path d="M{W - 44},{H - 22} H{W - 22} V{H - 44}"/>
  </g>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="#30363d"/>
</svg>
'''


# ----------------------------------------------------------------- terminal
C = {
    "kw": "#ff7b72", "var": "#d2a8ff", "key": "#79c0ff", "str": "#a5d6ff",
    "pun": "#e6edf3", "com": "#8b949e", "ok": "#3fb950", "txt": "#e6edf3",
}


def tok(*parts):
    return parts


LINES = [
    ("cmd", [("ok", "➜ "), ("key", "~ "), ("txt", "whoami")]),
    ("out", [("txt", "bahir-hakimi · senior full stack engineer · kabul, afghanistan")]),
    ("cmd", [("ok", "➜ "), ("key", "~ "), ("txt", "cat bahir.js")]),
    ("out", [("kw", "const "), ("var", "bahir"), ("pun", " = {")]),
    ("out", [("key", "  role"), ("pun", ": "), ("str", '"Senior Full Stack Engineer @ NETLINKS"'), ("pun", ","),
             ("com", "  // 5+ years shipping")]),
    ("out", [("key", "  building"), ("pun", ": ["), ("str", '"hr.jobs.af"'), ("pun", ", "), ("str", '"jobs.af"'),
             ("pun", ", "), ("str", '"NGO HRMIS"'), ("pun", "],")]),
    ("out", [("key", "  stack"), ("pun", ": ["), ("str", '"TypeScript"'), ("pun", ", "), ("str", '"React"'), ("pun", ", "),
             ("str", '"Next.js"'), ("pun", ", "), ("str", '"Node.js"'), ("pun", ", "), ("str", '"Django"'), ("pun", ", "),
             ("str", '"AWS"'), ("pun", "],")]),
    ("out", [("key", "  passions"), ("pun", ": ["), ("str", '"cybersecurity"'), ("pun", ", "),
             ("str", '"human-centric design"'), ("pun", ", "), ("str", '"mentoring"'), ("pun", "],")]),
    ("out", [("key", "  askMeAbout"), ("pun", ": ["), ("str", '"Space"'), ("pun", ", "), ("str", '"Chess"'), ("pun", "],")]),
    ("out", [("key", "  challenge"), ("pun", ": "), ("str", '"beat me at chess below 👇"'), ("pun", ",")]),
    ("out", [("pun", "};")]),
]


def terminal():
    W = 1000
    fs, lh, x0, y0 = 15, 26, 28, 78
    cw = fs * 0.6
    H = y0 + lh * (len(LINES) + 1) + 10
    t = 0.6
    defs, rows = [], []
    for i, (kind, parts) in enumerate(LINES):
        text = "".join(p[1] for p in parts)
        n = len(text)
        y = y0 + i * lh
        spans = "".join(f'<tspan fill="{C[c]}">{esc(s)}</tspan>' for c, s in parts)
        if kind == "cmd":
            prefix = 4  # "➜ ~ " appears at once, then the command is typed
            per = 0.075
            t += 0.5
        else:
            prefix, per = 0, 0.012
        steps_n = n - prefix
        dur = max(per * (steps_n + 1), 0.05)
        widths = [(prefix + k) * cw for k in range(steps_n + 1)] + [W]
        keyt = ";".join(f"{k / (len(widths) - 1):.4f}" for k in range(len(widths)))
        defs.append(
            f'<clipPath id="l{i}"><rect x="{x0}" y="{y - fs - 4}" height="{lh}" width="0">'
            f'<animate attributeName="width" begin="{t:.2f}s" dur="{dur:.2f}s" values="{";".join(f"{w:.1f}" for w in widths)}" '
            f'keyTimes="{keyt}" calcMode="discrete" fill="freeze"/></rect></clipPath>'
        )
        rows.append(f'<text x="{x0}" y="{y}" clip-path="url(#l{i})" xml:space="preserve">{spans}</text>')
        t += dur + (0.25 if kind == "cmd" else 0.04)
    yl = y0 + len(LINES) * lh
    rows.append(
        f'<g opacity="0"><set attributeName="opacity" to="1" begin="{t:.2f}s"/>'
        f'<text x="{x0}" y="{yl}" xml:space="preserve"><tspan fill="{C["ok"]}">➜ </tspan><tspan fill="{C["key"]}">~ </tspan></text>'
        f'<rect class="cursor" x="{x0 + 4 * cw + 2}" y="{yl - fs + 1}" width="{cw}" height="{fs + 3}" fill="#e6edf3"/></g>'
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Terminal: about Bahir Hakimi">
<title>cat bahir.js</title>
<defs>{"".join(defs)}</defs>
<style>
  text {{ font-family: {MONO}; font-size: {fs}px; }}
  .cursor {{ animation: caret 1s steps(1) infinite; }}
  @keyframes caret {{ 50% {{ opacity:0 }} }}
</style>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="#0d1117" stroke="#30363d"/>
<path d="M.5,40 V12.5 a12,12 0 0 1 12,-12 H{W - 12.5} a12,12 0 0 1 12,12 V40 Z" fill="#161b22"/>
<line x1="0" y1="40" x2="{W}" y2="40" stroke="#30363d"/>
<circle cx="24" cy="20" r="6" fill="#ff5f56"/><circle cx="44" cy="20" r="6" fill="#ffbd2e"/><circle cx="64" cy="20" r="6" fill="#27c93f"/>
<text x="{W / 2}" y="25" text-anchor="middle" fill="#8b949e" style="font-size:13px">bahir@kabul: ~</text>
{"".join(rows)}
</svg>
'''


(OUT / "hero.svg").write_text(hero())
(OUT / "terminal.svg").write_text(terminal())
print("wrote", OUT / "hero.svg", OUT / "terminal.svg")
