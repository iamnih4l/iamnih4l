import sys
import re
import random

def check_win(b):
    for i in range(3):
        if b[i][0] == b[i][1] == b[i][2] and b[i][0] != ' ': return b[i][0]
        if b[0][i] == b[1][i] == b[2][i] and b[0][i] != ' ': return b[0][i]
    if b[0][0] == b[1][1] == b[2][2] and b[0][0] != ' ': return b[0][0]
    if b[0][2] == b[1][1] == b[2][0] and b[0][2] != ' ': return b[0][2]
    if all(b[r][c] != ' ' for r in range(3) for c in range(3)): return 'Draw'
    return None

def main():
    if len(sys.argv) < 2: return
    action = sys.argv[1]
    
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()

    board_pattern = re.compile(r'<!-- ttt_board_start -->(.*?)<!-- ttt_board_end -->', re.DOTALL)
    match = board_pattern.search(content)
    if not match: return
    
    board_text = match.group(1).strip().split('\n')
    lines = board_text[-3:] # The last 3 lines in the board_text should be the actual rows
    
    board = []
    for line in lines:
        cols = [c.strip() for c in line.split('|')[1:-1]]
        row = []
        for col in cols:
            if '❌' in col: row.append('X')
            elif '⭕' in col: row.append('O')
            else: row.append(' ')
        board.append(row)

    status = check_win(board)
    
    if action == 'ttt_reset':
        board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        status = None
    elif action.startswith('ttt|') and status is None:
        _, r, c = action.split('|')
        r, c = int(r), int(c)
        if 0 <= r < 3 and 0 <= c < 3 and board[r][c] == ' ':
            board[r][c] = 'X'
            status = check_win(board)
            if status is None:
                empty = [(ir, ic) for ir in range(3) for ic in range(3) if board[ir][ic] == ' ']
                if empty:
                    air, aic = random.choice(empty)
                    board[air][aic] = 'O'
                    status = check_win(board)

    def render_cell(r, c, val):
        if val == 'X': return '❌'
        if val == 'O': return '⭕'
        if status is not None: return '⬜'
        return f'<a href="https://github.com/iamnih4l/iamnih4l/issues/new?title=ttt%7C{r}%7C{c}&body=Just+submit+this+issue+to+play+your+move">⬜</a>'
    
    msg = ""
    if status == 'X': msg = "**🎉 You won! 🎉**"
    elif status == 'O': msg = "**💻 AI won! 💻**"
    elif status == 'Draw': msg = "**🤝 It's a draw! 🤝**"
    else: msg = "**Your turn! Click a white square to play.**"

    new_board_text = f"\n{msg}\n\n|   |   |   |\n|---|---|---|\n"
    for r in range(3):
        new_board_text += "| " + " | ".join(render_cell(r, c, board[r][c]) for c in range(3)) + " |\n"
    new_board_text += "\n"
    
    new_content = content[:match.start(1)] + new_board_text + content[match.end(1):]
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == '__main__':
    main()
