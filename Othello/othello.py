EMPTY = "□"
WHITE = "○"
BLACK = "●"

banmen = [
    [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
    [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
    [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
    [EMPTY,EMPTY,EMPTY,WHITE,BLACK,EMPTY,EMPTY,EMPTY],
    [EMPTY,EMPTY,EMPTY,BLACK,WHITE,EMPTY,EMPTY,EMPTY],
    [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
    [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
    [EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
]

def show_banmen():
    for i in range(len(banmen) + 1):
        for j in range(len(banmen[0]) + 1):
            if i == 0:
                if j == 0:
                    print(" ", end="")
                else:
                    print(j - 1, end="")
            else:
                if j == 0:
                    print(i - 1, end="")
                else:
                    print(banmen[i - 1][j - 1], end="")
        print()

class ReversiBord(object):

    # 実際に盤面を変更（ひっくり返す）する処理
    def fllip_disk(self, x, y, color):
        fllippables = self.list_fllippable_disk(x, y, color)

        if len(fllippables) == 0:
            return False
        
        banmen[y][x] = color
        for pos in fllippables:
            banmen[pos[1]][pos[0]] = color

        return True

    # 配置を試してひっくり返す候補を取得する
    def list_fllippable_disk(self,x,y,color):
        direction = [
            (dir_x, dir_y)
            for dir_x in (-1, 0, 1)
            for dir_y in (-1, 0, 1)
            if not(dir_x == dir_y == 0)
        ]

        # 8方向を石がおけるか検査する
        fllippables = []
        for dir in direction:
            fllippables += self.list_fllippable_disk_one_line(x, y, dir[0], dir[1], color)
        
        return fllippables

    def list_fllippable_disk_one_line(self, x, y, dir_x, dir_y, color):

        reversed_color = BLACK if color == WHITE else WHITE
        reversed_list = []
        pos_x = x
        pos_y = y

        while True:
            pos_x += dir_x
            pos_y += dir_y

            # 返す石が存在しない場合は即時に空のリストを返却する
            if (pos_x < 0 or pos_y < 0) \
                or (len(banmen[0]) <= pos_x or len(banmen) <= pos_y) \
                or banmen[pos_y][pos_x] == EMPTY:
                return []

            # 相手の石がおかれていた場合は、リストに石の座標を追加する
            if banmen[pos_y][pos_x] == reversed_color:
                reversed_list.append((pos_x, pos_y))
            # 自分の石がおかれていた場合は、検査を終了する。
            else:
                break
            
        return reversed_list


def input_numeric(text):
    while True:
        ret = input(text)
        try:
            ret = int(ret)
            break
        except:
            print('[警告]：数値を入力してください')

    return ret


if __name__ == '__main__':
    
    # Plyaer は2人固定のため、ターンの判定は 0/1 で判定を行う
    # ＜定義＞ 0 : 黒 、 1 : 白
    turn = 0
    board = ReversiBord()

    while True:
        print("{0}のターンです".format('黒' if turn == 0 else '白'))
        color = BLACK if turn == 0 else WHITE

        # 盤面を描画
        show_banmen()

        # 盤面チェック
        skip = True
        gameover = True
        for y in range(len(banmen)):
            for x in range(len(banmen[y])):
                if banmen[y][x] != EMPTY:
                    continue
                if 0 < len(board.list_fllippable_disk(x, y, color)):
                    skip = False
                gameover = False

        if gameover:
            print('○○のかち')
            break

        if skip:
            print("{0}のおける場所が存在しないためスキップします".format('黒' if turn == 0 else '白'))
            turn = (turn + 1) % 2
            continue

        while True:
            pos_x = input_numeric('配置するＸ座標を入力してください')
            pos_y = input_numeric('配置するＹ座標を入力してください')

            if (pos_x < 0 or pos_y < 0) \
                or (len(banmen[0]) <= pos_x or len(banmen) <= pos_y):
                print('範囲内を入力してください')
            else:
                break
        
        if 0 < len(board.list_fllippable_disk(pos_x, pos_y, color)):
            board.fllip_disk(pos_x, pos_y, color)
            turn = (turn + 1) % 2
        else:
            print('その場所はおけません')
