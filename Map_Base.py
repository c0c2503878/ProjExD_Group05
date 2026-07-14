import math
import os
import random
import sys
import time
import pygame as pg

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # この.pyファイルがあるフォルダをカレントディレクトリにするもの

# ======↓定数定義↓======

WIDTH = 1240  # 横幅(x)
HEIGHT = 680  # 縦幅(y)
FPS = 60  # フレーム数
# マップのデータ（シード値）を格納しているもの（0：道、移動可能, 1：障害物、移動不可, 2：敵, 4:ミニゲーム）
SEEDS =[
    [  # 最上段
        [  # マップ番号(0, 0) 左上
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0],
            [1, 1, 0, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 2, 0, 0, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        [  # マップ番号(0, 1) 真ん中上
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
            [1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 2, 0, 0, 0, 0, 1, 1, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 1, 1, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
            [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        [  # マップ番号(0, 2) 右上
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 2, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 2, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1],
            [1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 2, 1, 1, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
    ],
    [  # 中央段
        [  # マップ番号(1, 0) 真ん中左
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
            [1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1],
            [1, 0, 0, 1, 1, 1, 2, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 2, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        [  # 初期位置 マップ番号(1, 1) 中心
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
            [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        [  # マップ番号(1, 2) 真ん中右
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
            [1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 2, 1, 1],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1],
            [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
    ],
    [  # 最下段
        [  # マップ番号(2, 0) 左下
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 2, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0],
            [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 2, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        [  # マップ番号(2, 1) 真ん中下
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1],
            [0, 0, 2, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        [  # マップ番号(2, 2) 右下
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
            [0, 2, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
    ],
]

# 色
# ===↓色定義↓===
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# ===↑色定義↑===

# ======↑定数定義↑======


# ===↓class定義↓===

class GameMap:
    """
    マップを作成するもの
    """
    def __init__(self, y_num: int, x_num: int):
        """
        マップを作成し、データを初期化する
        引数：縦の分割数int, 横の分割数int
        y_numはHEIGHTを割り切れる値が好ましい, x_numはWIDTHを割り切れる値が好ましい
        """

        self.x_num = x_num
        self.y_num = y_num
        self.wid = WIDTH // x_num
        self.hei = HEIGHT // y_num
        self.map_data = self._create_map_data()
        self.rocks = pg.sprite.Group()  # 岩のグループ作成
        self.minigame_tiles=pg.sprite.Group() #ミニゲームマス表示用のグループ作成

    def _create_map_data(self) -> list[list[dict]]:
        """
        二次元リストを作成する隠しメソッド
        戻り値：二次元リストマップデータ（list[[データ]]、アクセスlist[縦][横]["データ"]）
        """

        map_data = []  # 大元の二次元リストになるもの
        for row in range(self.y_num):
            row_lis = []  # そのマスのデータを格納するもの
            for col in range(self.x_num):
                cell_data = {
                    # マスの番号
                    "id": (row, col),
                    # マスの中心座標（オブジェクト用）
                    "coor": (self.wid * col + (self.wid // 2), self.hei * row + (self.hei // 2)),
                    # マスのステータス（0：移動可能, 1：移動不可, 2：敵とのバトルイベント）
                    "type": 0
                }
                row_lis.append(cell_data)
            map_data.append(row_lis)
        return map_data
    
    def update_line(self, screen: pg.Surface):
        """
        マップに線を描画するもの
        デバッグ用
        """
        for i in range(1, self.x_num):
            pg.draw.line(screen, RED, (self.wid * i, 0), (self.wid * i, HEIGHT), 1)
        for i in range(1, self.y_num):
            pg.draw.line(screen, RED, (0, self.hei * i), (WIDTH, self.hei * i), 1)

    def get_cell(self, row: int, col: int) -> dict:
        """
        指定した座標のデータを取得するもの
        引数：縦番号int, 横番号int
        返り値：マスの情報（データ）, マスが存在しない場合None
        """
        if 0 <= col < self.x_num and 0 <= row < self.y_num:
            return self.map_data[row][col]
        return None

    def load_map(self, map_y: int, map_x: int):
        """
        マップを生成するもの
        引数：読み込みたいマップの番号map_y(0, 1, 2), map_x(0, 1, 2)
        """
        self.rocks.empty()  # 前のマップの岩を全て削除
        self.minigame_tiles.empty() #前のマップのミニゲームマスをすべて削除
        seed = SEEDS[map_y][map_x]  # 指定された座標のマップのデータを取得
        for row in range(self.y_num):
            for col in range(self.x_num):
                if seed[row][col] == 1:  # 岩のマスか判定
                    rock = Rock(self.map_data[row][col]["coor"])  # 岩を生成
                    self.rocks.add(rock)  # 岩を岩グループに追加
                elif seed[row][col] ==4:
                    minigame_tile=MinigameTile(self.map_data[row][col]["coor"]) #ミニゲームマスの見た目生成
                    self.minigame_tiles.add(minigame_tile)
                self.map_data[row][col]["type"] = seed[row][col]  # seedに沿ってtypeを上書（マップ形成）
    def check_move(self, row: int, col: int) -> int:
        """
        移動できるのかを判定するもの
        引数：移動先の縦番号int, 移動先の横番号int
        戻り値：移動先のマスの"type"int（0：移動可能, 1：移動不可, 2：敵）
        """
        cell = self.get_cell(row, col)  # 移動先のマスのデータを取得
        if cell is None:
            return 1  # マップ外は壁扱いにする
        return cell["type"]  # 移動先のマスのtypeを返す

    def get_enemy_positions(self) -> list[tuple[int, int]]:
        """
        敵が配置されているマスの中心座標を取得する
        戻り値：敵が配置されているマスの中心座標tupleが格納されたlist
        """
        positions = []  # 敵がいるマスの中心座標を格納するもの
        for row in range(self.y_num):
            for col in range(self.x_num):
                if self.map_data[row][col]["type"] == 2:
                    positions.append(self.map_data[row][col]["coor"])
        return positions
    
    def get_id(self, x: int, y: int) -> tuple[int, int]:
        """
        座標からマス目idを求めるもの
        引数：オブジェクトの中心のx座標, y座標
        戻り値：tuple(行, 列)
        """
        col = x // self.wid
        row = y // self.hei
        return row, col
    
    def update(self, screen: pg.Surface):
        """
        画面に岩などを描画するもの
        引数：画像Surface
        """
        self.rocks.draw(screen)
        self.minigame_tiles.draw(screen)


class Rock(pg.sprite.Sprite):
    """
    岩に関するもの
    """
    def __init__(self, coor: tuple[int, int]):
        """
        引数：マスの中心座標tuple(x, y)
        """
        super().__init__()
        self.image = pg.Surface((55, 55))  # 現時点仮の岩画像
        self.image.fill(BLACK)  # 現時点仮の岩
        self.rect = self.image.get_rect(center = coor)  # rect.centerにcoorを設定


class MinigameTile(pg.sprite.Sprite):
    """
    ミニゲームマスの見た目に関するもの
    """
    def __init__(self,coor:tuple[int,int]):
        """
        引数:マスの中心座標,tuple(x,y)
        """
        super().__init__()
        self.image=pg.image.load("img/mark_exclamation.png")  #イベントマス画像
        self.image=pg.transform.scale(self.image,(52,52))
        self.rect = self.image.get_rect(center = coor)  # rect.centerにcoorを設定

    

class Enemy(pg.sprite.Sprite):
    """
    敵に関するもの
    """

    def __init__(self, coor: tuple[int, int]):
        """
        引数：マスの中心座標tuple(x, y)
        """
        super().__init__()
        self.image = pg.Surface((40, 40))  # 現時点仮の敵画像
        self.image.fill(RED)  # 現時点仮の敵
        self.rect = self.image.get_rect(center = coor)  # rect.centerにcoorを設定


class Player(pg.sprite.Sprite):
    """
    プレイヤーに関するもの
    """
    def __init__(self, coor: tuple[int, int], game_map: GameMap):
        """
        引数：初期配置の中心座標tuple(x, y), GameMapのインスタンス
        """
        super().__init__()
        self.image = pg.Surface((40, 40))  # 現時点仮のプレイヤー画像
        self.image.fill(GREEN)  # 現時点仮のプレイヤー
        self.rect = self.image.get_rect(center = coor)  # rect.centerにcoorを設定
        self.game_map = game_map
        self.row, self.col = self.game_map.get_id(coor[0], coor[1])  # プレイヤーのいるマスのidを取得

    def move(self, move_row: int, move_col: int) -> str | None:
        """
        指定された方向へ1マス移動する(idを参照して移動)
        引数：縦の移動量, 横の移動量
        戻り値：マップ外に出た場合は外に出た方向の文字列、それ以外はNone
        """
        next_row = self.row + move_row
        next_col = self.col + move_col

        # 画面外への移動判定（マップ移動）
        if next_row < 0:
            return "UP"
        if next_row >= self.game_map.y_num:
            return "DOWN"
        if next_col < 0:
            return "LEFT"
        if next_col >= self.game_map.x_num:
            return "RIGHT"
        # 移動先の判定（岩ではない場合）
        if self.game_map.check_move(next_row, next_col) != 1:
            self.row = next_row
            self.col = next_col
            self.rect.center = self.game_map.get_cell(self.row, self.col)["coor"]
        return None
    
# ===↑class定義↑===


# ===↓関数定義↓===

def get_japanese_font(size: int) -> pg.font.Font:
    """
    日本語表示に対応したフォントを取得するもの
    （pg.font.Font(None, ...)のデフォルトフォントは日本語グリフを持たないため、システムにインストールされている日本語フォントを探して使う）
    引数：フォントサイズint
    戻り値：pg.font.Fontオブジェクト
    """
    candidates = [
        "Yu Gothic", "Meiryo", "MS Gothic", "MS UI Gothic",  # Windows
        "Hiragino Sans", "Hiragino Kaku Gothic ProN",  # Mac
        "Noto Sans CJK JP", "Noto Sans JP", "IPAGothic", "IPAexGothic", "TakaoGothic",  # Linux
    ]
    for name in candidates:
        font_path = pg.font.match_font(name)
        if font_path:
            return pg.font.Font(font_path, size)
    # どれも見つからなかった場合はデフォルトフォント（日本語は文字化けする可能性あり）
    return pg.font.Font(None, size)

def draw_center_text(screen: pg.Surface, font: pg.font.Font, text: str, color: tuple, y_offset: int = 0):
    """
    画面中央（縦方向にy_offsetずらした位置）に文字列を描画するもの
    引数：画面Surface, フォント, 表示文字列, 色tuple, 縦方向のずらし量int
    """
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(surf, rect)


def show_instruction(screen: pg.Surface, clock: pg.time.Clock, title: str, subtitle: str, duration: int = 1200):
    """
    ミニゲーム開始前の「お題」演出を表示するもの（メイドインワリオ風）
    引数：画面Surface, Clock, 大見出し文字列, 補足文字列, 表示時間ミリ秒int
    """
    font_title = get_japanese_font(110)
    font_sub = get_japanese_font(40)
    start_time = pg.time.get_ticks()
    while pg.time.get_ticks() - start_time < duration:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        screen.fill(BLACK)
        draw_center_text(screen, font_title, title, WHITE, -30)
        draw_center_text(screen, font_sub, subtitle, WHITE, 60)
        pg.display.update()
        clock.tick(FPS)


def show_result(screen: pg.Surface, clock: pg.time.Clock, is_clear: bool, duration: int = 1000):
    """
    ミニゲーム終了後の「CLEAR!/MISS...」演出を表示するもの
    引数：画面Surface, Clock, クリアしたかbool, 表示時間ミリ秒int
    """
    font = get_japanese_font(100)
    text = "CLEAR!" if is_clear else "MISS..."
    color = GREEN if is_clear else RED
    start_time = pg.time.get_ticks()
    while pg.time.get_ticks() - start_time < duration:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        screen.fill(BLACK)
        draw_center_text(screen, font, text, color)
        pg.display.update()
        clock.tick(FPS)


def microgame_mash(screen: pg.Surface, clock: pg.time.Clock) -> bool:
    """
    スペースキーを連打するミニゲーム
    制限時間内に規定回数スペースキーを押せたらクリア
    戻り値：クリアしたかどうかbool
    """
    show_instruction(screen, clock, "連打！", "スペースキーを連打しろ！")

    font_big = get_japanese_font(90)
    font_small = get_japanese_font(40)
    TIME_LIMIT = 3000  # 制限時間（ミリ秒）
    NEED_COUNT = 25  # 必要な連打回数
    count = 0

    start_time = pg.time.get_ticks()
    while True:
        elapsed = pg.time.get_ticks() - start_time
        if elapsed >= TIME_LIMIT or count >= NEED_COUNT:
            break

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                count += 1

        screen.fill(BLACK)
        draw_center_text(screen, font_big, f"{count} / {NEED_COUNT}", WHITE, -60)
        draw_center_text(screen, font_small, f"残り {(TIME_LIMIT - elapsed) / 1000:.1f}秒", WHITE, 60)
        pg.display.update()
        clock.tick(FPS)

    return count >= NEED_COUNT


def microgame_dodge(screen: pg.Surface, clock: pg.time.Clock) -> bool:
    """
    ←→キーで落下してくるブロックを避けるミニゲーム
    制限時間の間ブロックに当たらなければクリア
    戻り値：クリアしたかどうかbool
    """
    show_instruction(screen, clock, "よけろ！", "←→キーでブロックを避けろ！")

    TIME_LIMIT = 9000  # 制限時間（ミリ秒）
    SPEED = 6  # プレイヤーの移動速度
    BLOCK_SPEED = 6  # ブロックの落下速度
    SPAWN_INTERVAL = 50  # ブロック生成間隔（ミリ秒）

    player_rect = pg.Rect(0, 0, 40, 40)
    player_rect.centerx = WIDTH // 2
    player_rect.bottom = HEIGHT - 20
    blocks: list[pg.Rect] = []
    spawn_timer = 0

    start_time = pg.time.get_ticks()
    while pg.time.get_ticks() - start_time < TIME_LIMIT:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        # プレイヤー移動
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            player_rect.x -= SPEED
        if keys[pg.K_RIGHT]:
            player_rect.x += SPEED
        player_rect.x = max(0, min(WIDTH - player_rect.width, player_rect.x))

        # ブロック生成
        spawn_timer += clock.get_time()
        if spawn_timer >= SPAWN_INTERVAL:
            spawn_timer = 0
            block_x = random.randint(0, WIDTH - 40)
            blocks.append(pg.Rect(block_x, -40, 40, 40))

        # ブロック移動と画面外削除
        for block in blocks:
            block.y += BLOCK_SPEED
        blocks = [block for block in blocks if block.top < HEIGHT]

        # 当たり判定
        hitbox = player_rect.inflate(-10, -10)
        for block in blocks:
            if hitbox.colliderect(block):
                return False  # 当たったら即失敗

        screen.fill(BLACK)
        pg.draw.rect(screen, GREEN, player_rect)
        for block in blocks:
            pg.draw.rect(screen, RED, block)
        pg.display.update()
        clock.tick(FPS)

    return True  # 制限時間を耐えきったらクリア


MINIGAMES = [microgame_mash, microgame_dodge]  # ミニゲーム一覧（増やす場合はここに追加）


def run_minigame(screen: pg.Surface, clock: pg.time.Clock) -> bool:
    """
    MINIGAMESからランダムに1つ選んで実行し、結果演出まで行うもの
    引数：画面Surface, Clock
    戻り値：クリアしたかどうかbool
    """
    game_func = random.choice(MINIGAMES)
    is_clear = game_func(screen, clock)
    show_result(screen, clock, is_clear)
    return is_clear

# ===↑関数定義↑===


def main():
    pg.display.set_caption("ゲーム(仮)")

    # ===↓変数定義↓===
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    game_map = GameMap(10, 20)  # マップ作成 
    current_map_x = 1  # マップ初期x座標 
    current_map_y = 1  # マップ初期y座標 
    # マップ番号(1, 1) 中心
    game_map.load_map(current_map_y, current_map_x)  # マップロード
    enemys = pg.sprite.Group()  # 敵のグループ作成
    # 敵の座標読み込み
    for coor in game_map.get_enemy_positions():
        enemys.add(Enemy(coor))
    start_coor = game_map.get_cell(5, 10)["coor"]  # 初期位置
    player = Player(start_coor, game_map)  # プレイヤー定義
    players = pg.sprite.GroupSingle(player)  # プレイヤー用グループ（単体）
    # ===↑変数定義↑===

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return # 終了判定

            # プレイヤー移動処理
            if event.type == pg.KEYDOWN:
                move: str | None = None  # マップ移動の詳細を格納する変数
                if event.key == pg.K_UP:
                    move = player.move(-1, 0)
                elif event.key == pg.K_DOWN:
                    move = player.move(1, 0)
                elif event.key == pg.K_LEFT:
                    move = player.move(0, -1)
                elif event.key == pg.K_RIGHT:
                    move = player.move(0, 1)
                # マップ移動処理
                if move:
                    if move == "UP" and current_map_y > 0:
                        current_map_y -= 1
                        player.row = game_map.y_num - 1  # 下端
                    elif move == "DOWN" and current_map_y < 2:
                        current_map_y += 1
                        player.row = 0  # 上端
                    elif move == "LEFT" and current_map_x > 0:
                        current_map_x -= 1
                        player.col = game_map.x_num - 1  # 右端
                    elif move == "RIGHT" and current_map_x < 2:
                        current_map_x += 1
                        player.col = 0  # 左端
                    else:
                        continue
                    # 新しいマップをロード
                    game_map.load_map(current_map_y, current_map_x)
                    enemys.empty()  # 移動前のマップに表示されている敵を削除
                    # 敵の座標読み込み
                    for coor in game_map.get_enemy_positions():
                        enemys.add(Enemy(coor))
                    # プレイヤーを更新
                    player.rect.center = game_map.get_cell(player.row, player.col)["coor"]
                if game_map.check_move(player.row, player.col) == 2:  # 移動した先が敵かの判定
                    pass  # ここにバトルイベントなどを追加
                elif game_map.check_move(player.row,player.col) ==4: #移動した先がミニゲームマスかの判定
                    run_minigame(screen,clock) #ミニゲーム実行

        screen.fill(WHITE)  # 背景仮(一番最初に描画)
        game_map.update_line(screen)  # 枠線表示（デバッグ用）

        game_map.update(screen)  # 岩を描画
        enemys.draw(screen)  # 敵を描画
        players.draw(screen)  # プレイヤーを描画


        pg.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()