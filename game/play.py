"""Community chess for the GitHub profile README.

Triggered by .github/workflows/chess.yml when someone opens an issue titled
``chess|move|e2e4`` or ``chess|new``. Applies the move, redraws the board and
rewrites the chess section of README.md.

Local use:
    python game/play.py --render            # redraw README from state.json
    TITLE='chess|move|e2e4' PLAYER=you python game/play.py
"""
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import chess
import chess.svg

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "game" / "state.json"
BOARD = ROOT / "game" / "board.svg"
README = ROOT / "README.md"
START, END = "<!-- CHESS:START -->", "<!-- CHESS:END -->"

REPO = os.environ.get("REPO", "BahirHakimy/BahirHakimy")
OWNER = os.environ.get("OWNER", REPO.split("/")[0])

PIECE = {
    chess.KING: ("♔", "♚", "King"),
    chess.QUEEN: ("♕", "♛", "Queen"),
    chess.ROOK: ("♖", "♜", "Rook"),
    chess.BISHOP: ("♗", "♝", "Bishop"),
    chess.KNIGHT: ("♘", "♞", "Knight"),
    chess.PAWN: ("♙", "♟︎", "Pawn"),
}
COLORS = {
    "square light": "#e9e4f7",
    "square dark": "#7b68b5",
    "square light lastmove": "#fde68a",
    "square dark lastmove": "#f59e0b",
    "margin": "#0b1026",
    "coord": "#cbd5e1",
}
ISSUE_BODY = "Just press Create. A bot plays your move within a minute."


# ------------------------------------------------------------------ state
def new_state(prev=None):
    prev = prev or {}
    return {
        "game": prev.get("game", 0) + 1,
        "fen": chess.STARTING_FEN,
        "moves": [],
        "players": prev.get("players", {}),
        "history": prev.get("history", []),
        "started": now(),
    }


def load():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return new_state()


def save(state):
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def board_of(state):
    board = chess.Board()
    for m in state["moves"]:
        board.push_uci(m["uci"])
    return board


# ---------------------------------------------------------------- actions
def play(state, title, player):
    """Return (reply_markdown, changed, commit_message)."""
    board = board_of(state)
    parts = [p.strip().lower() for p in title.split("|")]

    if parts[:2] == ["chess", "new"]:
        if not board.is_game_over() and player.lower() != OWNER.lower():
            return (f"Game #{state['game']} is still going! Jump in and play a move instead 😉\n\n{readme_link()}", False, None)
        if not board.is_game_over() and state["moves"]:
            state["history"].append(summary(state, board, "abandoned"))
        fresh = new_state(state)
        state.clear()
        state.update(fresh)
        return (f"♟️ Game #{state['game']} has started — White to move.\n\n{readme_link()}", True, f"♟️ new game #{state['game']} by @{player}")

    if parts[:2] != ["chess", "move"] or len(parts) < 3:
        return ("I couldn't read that. Titles look like `chess|move|e2e4`; the easiest way is to click a move in the README.\n\n" + readme_link(), False, None)

    if board.is_game_over():
        return (f"This game is over ({result_text(board)}). [Start a new one]({issue_url('chess|new')}) 🎉", False, None)

    last = state["moves"][-1]["player"] if state["moves"] else None
    if last and last.lower() == player.lower():
        return ("You played the last move, so let someone else answer it. Share the board with a friend 😄\n\n" + readme_link(), False, None)

    uci = re.sub(r"[^a-h1-8qrbn]", "", parts[2])
    try:
        move = chess.Move.from_uci(uci)
    except ValueError:
        move = None
    if move is None or move not in board.legal_moves:
        return (f"`{parts[2]}` isn't a legal move in this position. Pick one from the list in the README.\n\n{readme_link()}", False, None)

    san = board.san(move)
    color = "white" if board.turn == chess.WHITE else "black"
    board.push(move)
    state["moves"].append({"uci": move.uci(), "san": san, "player": player, "color": color, "date": now()})
    state["fen"] = board.fen()
    state["players"][player] = state["players"].get(player, 0) + 1

    reply = f"You played **{san}** as {'⚪ White' if color == 'white' else '⚫ Black'}. Thanks for playing! ♟️"
    if board.is_game_over():
        state["history"].append(summary(state, board, result_text(board)))
        reply += f"\n\n🏁 **Game over: {result_text(board)}.** [Start a new game]({issue_url('chess|new')})"
    elif board.is_check():
        reply += " Check! 😱"
    reply += f"\n\n{readme_link()}"
    return reply, True, f"♟️ @{player}: {san}"


def summary(state, board, result):
    return {
        "game": state["game"],
        "result": result,
        "moves": len(state["moves"]),
        "players": len({m["player"] for m in state["moves"]}),
        "ended": now(),
    }


def result_text(board):
    outcome = board.outcome()
    if outcome is None:
        return "in progress"
    if outcome.winner is None:
        return f"draw ({outcome.termination.name.replace('_', ' ').lower()})"
    return f"{'White' if outcome.winner else 'Black'} wins by {outcome.termination.name.lower()}"


# ----------------------------------------------------------------- render
def issue_url(title):
    return f"https://github.com/{REPO}/issues/new?title={quote(title, safe='')}&body={quote(ISSUE_BODY, safe='')}"


def readme_link():
    return f"[Back to the board ↩](https://github.com/{OWNER})"


def render(state):
    board = board_of(state)
    last = board.peek() if board.move_stack else None
    check = board.king(board.turn) if board.is_check() else None
    BOARD.write_text(chess.svg.board(board, lastmove=last, check=check, size=440, colors=COLORS))

    out = [START, "", "## ♟️ Community Chess", ""]
    out.append("One game, played by everyone who visits. **Click a move below** to open an issue, then hit *Create*. "
               "A GitHub Action plays it and redraws the board. You can't move twice in a row, so bring a friend.")
    out.append("")

    n = len(state["moves"])
    if board.is_game_over():
        status = f"🏁 **Game #{state['game']} is over: {result_text(board)}.** [**Start a new game →**]({issue_url('chess|new')})"
    else:
        turn = "⚪ White" if board.turn == chess.WHITE else "⚫ Black"
        status = f"**Game #{state['game']}**, move {board.fullmove_number}: **{turn}** to play"
        status += " and they're in **check**! 😱" if board.is_check() else ""
    out += [f'<p align="center">{status_html(status)}</p>', ""]
    out += ['<p align="center"><img src="game/board.svg" width="420" alt="Current chess position"></p>', ""]

    if not board.is_game_over():
        out += ["<details open>", f"<summary><b>Pick a move ({board.legal_moves.count()} legal)</b></summary>", "",
                "| Piece | From | Moves |", "| :-- | :-: | :-- |"]
        by_square = {}
        for mv in board.legal_moves:
            by_square.setdefault(mv.from_square, []).append(mv)
        for sq in sorted(by_square, key=lambda s: (-board.piece_type_at(s), s)):
            p = board.piece_at(sq)
            white_icon, black_icon, name = PIECE[p.piece_type]
            icon = white_icon if p.color == chess.WHITE else black_icon
            links = " · ".join(
                f"[{board.san(m)}]({issue_url('chess|move|' + m.uci())})"
                for m in sorted(by_square[sq], key=lambda m: m.to_square)
            )
            out.append(f"| {icon} {name} | `{chess.square_name(sq)}` | {links} |")
        out += ["", "</details>", ""]

    if n:
        out += ["**Last moves**", "", "| # | Move | Player |", "| :-: | :-: | :-- |"]
        for i in range(n - 1, max(n - 6, -1), -1):
            m = state["moves"][i]
            num = f"{i // 2 + 1}{'.' if m['color'] == 'white' else '…'}"
            out.append(f"| {num} | {'⚪' if m['color'] == 'white' else '⚫'} **{m['san']}** | [@{m['player']}](https://github.com/{m['player']}) |")
        out.append("")

    if state["players"]:
        top = sorted(state["players"].items(), key=lambda kv: (-kv[1], kv[0].lower()))[:5]
        medals = ["🥇", "🥈", "🥉", "4.", "5."]
        out += ["**Hall of fame**, all-time moves: " + " · ".join(
            f"{medals[i]} [@{u}](https://github.com/{u}) ({c})" for i, (u, c) in enumerate(top)), ""]

    if state["history"]:
        out += ["**Past games:** " + " · ".join(
            f"#{g['game']} {g['result']} in {g['moves']} moves" for g in state["history"][-3:][::-1]), ""]

    out.append(END)
    text = README.read_text()
    block = "\n".join(out)
    if START in text:
        text = re.sub(re.escape(START) + ".*?" + re.escape(END), lambda _: block, text, flags=re.S)
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    README.write_text(text)


def status_html(md):
    # GitHub renders markdown inside <p> only when separated by blank lines; convert the bits we use.
    html = re.sub(r"\[\*\*(.+?)\*\*\]\((.+?)\)", r'<a href="\2"><b>\1</b></a>', md)
    html = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html)
    return re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', html)


def set_output(**kw):
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        for k, v in kw.items():
            print(f"{k}={v}")
        return
    with open(path, "a") as f:
        for k, v in kw.items():
            f.write(f"{k}<<EOF\n{v}\nEOF\n")


if __name__ == "__main__":
    state = load()
    if "--render" in sys.argv:
        save(state)
        render(state)
        sys.exit(0)

    reply, changed, message = play(state, os.environ["TITLE"], os.environ["PLAYER"])
    if changed:
        save(state)
        render(state)
    (ROOT / "game" / ".reply.md").write_text(reply)
    set_output(changed=str(changed).lower(), message=message or "")
