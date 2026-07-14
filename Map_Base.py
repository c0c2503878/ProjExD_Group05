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
# マップのデータ（シード値）を格納しているもの（0：道、移動可能, 1：障害物、移動不可, 2：敵）
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
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
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

# 敵のステータスデータ（モンスター図鑑のようなもの）
MONSTER_DATA = {
    "スライム": {"max_hp": 40, "atk": 10, "weight": 40}, 
    "ゴブリン": {"max_hp": 60, "atk": 20, "weight": 25},
    "ミミック": {"max_hp": 100, "atk": 30, "weight": 20},
    "ゴーレム": {"max_hp": 400, "atk": 30, "weight": 10},
    "ドラゴン": {"max_hp": 500, "atk": 60, "weight": 5} 
}
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
        seed = SEEDS[map_y][map_x]  # 指定された座標のマップのデータを取得
        for row in range(self.y_num):
            for col in range(self.x_num):
                if seed[row][col] == 1:  # 岩のマスか判定
                    rock = Rock(self.map_data[row][col]["coor"])  # 岩を生成
                    self.rocks.add(rock)  # 岩を岩グループに追加
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


class Rock(pg.sprite.Sprite):
    """
    岩に関するもの
    """
    def __init__(self, coor: tuple[int, int]):
        """
        引数：マスの中心座標tuple(x, y)
        """
        super().__init__()
        self.image = pg.image.load(f"img/rock.png").convert_alpha()   # 現時点仮の岩画像
        self.image = pg.transform.scale(self.image, (95, 110))
        self.rect = self.image.get_rect(center = coor)  # rect.centerにcoorを設定


class Enemy(pg.sprite.Sprite):
    """
    敵に関するもの
    """

    def __init__(self, coor: tuple[int, int], name=None):
        """
        引数：マスの中心座標tuple(x, y)
        """
        super().__init__()
        if name is None:
            names = list(MONSTER_DATA.keys())
            weights = [data["weight"] for data in MONSTER_DATA.values()]
            name = random.choices(names, weights=weights, k=1)[0]
        data = MONSTER_DATA[name]
        # 敵ステータス
        self.name = name
        self.max_hp = data["max_hp"]
        self.hp = self.max_hp
        self.atk = data["atk"]
        
        raw_image = pg.image.load(f"img/{self.name}.png").convert_alpha()
        self.battle_image = pg.transform.scale(raw_image, (600, 600)) # 戦闘時の画像サイズの変更
        self.map_image = pg.transform.scale(raw_image, (100, 100)) # 画像サイズの変更

        self.image = self.map_image
        self.rect = self.image.get_rect(center=coor)
        self.original_coor = coor
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
        # ステータス======
        self.name = "勇者"
        self.max_hp = 200
        self.hp = 200
        self.atk = 30
        #================

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


# ===↑関数定義↑===


def main():
    pg.display.set_caption("ゲーム(仮)")

    # ===↓変数定義↓===
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    bg_image = pg.image.load("img/back1.png").convert_alpha()  # 背景画像
    map_background = pg.transform.scale(bg_image, (WIDTH, HEIGHT))  # 背景画像を画面サイズに合わせる
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
    game_state = "MAP"
    battle_phase = "COMMAND"
    battle_message = ""
    next_turn = "PLAYER"
    battle_cursor = 0
    current_enemy = None
    font = pg.font.SysFont("msgothic", 40)
    # ===↑変数定義↑===

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return # 終了判定

            # プレイヤー移動処理
            if game_state == "MAP":
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
                        
                        # ここにバトルイベントなどを追加
                        game_state = "BATTLE"
                        battle_phase = "COMMAND"
                        # 現在戦う敵を取得
                        current_enemy = pg.sprite.spritecollideany(player, enemys)
                        if current_enemy:
                            current_enemy.image = current_enemy.battle_image
                            current_enemy.rect = current_enemy.image.get_rect(center=(640, 300))
            elif game_state == "BATTLE":
                if event.type == pg.KEYDOWN:
                    # 1. コマンド選択フェーズ
                    if battle_phase == "COMMAND":
                        if event.key == pg.K_UP: battle_cursor = 0
                        elif event.key == pg.K_DOWN: battle_cursor = 1
                        elif event.key == pg.K_RETURN:
                            if battle_cursor == 0: # たたかう
                                current_enemy.image = current_enemy.battle_image
                                current_enemy.rect = current_enemy.image.get_rect(center=(640, 300))
                                # プレイヤー攻撃計算
                                is_crit = random.random() < 0.08
                                dmg = int(player.atk * random.uniform(0.9, 1.1) * (1.5 if is_crit else 1.0))
                                current_enemy.hp = max(0, current_enemy.hp - dmg)
                                battle_message = f"クリティカル！" if is_crit else f"{player.name}の攻撃！"
                                battle_message += f" {dmg}のダメージ！"
                                battle_phase = "MESSAGE"
                                next_turn = "WIN" if current_enemy.hp <= 0 else "ENEMY"
                            else: # にげる
                                battle_message = "無事に逃げ切った！"
                                battle_phase = "MESSAGE"
                                next_turn = "ESCAPE"

                    # 2. メッセージ送りフェーズ
                    elif battle_phase == "MESSAGE":
                        if event.key == pg.K_RETURN:
                            if next_turn == "ENEMY":
                                # 敵の攻撃計算
                                is_crit = random.random() < 0.08
                                dmg = int(current_enemy.atk * random.uniform(0.9, 1.1) * (1.5 if is_crit else 1.0))
                                player.hp = max(0, player.hp - dmg)
                                battle_message = f"クリティカル！" if is_crit else f"{current_enemy.name}の攻撃！"
                                battle_message += f" {dmg}のダメージ！"
                                next_turn = "LOSE" if player.hp <= 0 else "PLAYER"
                            elif next_turn == "PLAYER":
                                battle_phase = "COMMAND"
                            elif next_turn == "WIN":
                                row, col = game_map.get_id(current_enemy.original_coor[0], current_enemy.original_coor[1])
                                game_map.map_data[row][col]["type"] = 0  # 敵を倒したのでマスのtypeを0に変更
                                game_state = "MAP"
                                current_enemy.kill()
                            elif next_turn == "ESCAPE":
                                current_enemy.image = current_enemy.map_image
                                current_enemy.rect = current_enemy.image.get_rect(center=current_enemy.original_coor)
                                game_state = "MAP"
                            elif next_turn == "LOSE":
                                print("GAME OVER"); return

        # --- 描画処理 ---
        screen.fill(BLACK if game_state == "BATTLE" else WHITE) # バトル中は黒背景に

        if game_state == "MAP":
            screen.blit(map_background, (0, 0))
            game_map.update_line(screen)  # 枠線表示（デバッグ用）
            game_map.update(screen)  # 岩を描画
            enemys.draw(screen)  # 敵を描画
            players.draw(screen)  # プレイヤーを描画
            
        elif game_state == "BATTLE":
            # バトルUIの描画
            if current_enemy:
                screen.blit(current_enemy.image, current_enemy.rect)
            
            if current_enemy:
                enemy_name_txt = font.render(f"{current_enemy.name}", True, WHITE)
                enemy_hp_txt = font.render(f"HP: {current_enemy.hp}/{current_enemy.max_hp}", True, WHITE)
                screen.blit(enemy_name_txt, (800, 100))
                screen.blit(enemy_hp_txt, (800, 150))

            # プレイヤーの情報を表示
            pg.draw.rect(screen, WHITE, (50, 500, 1140, 150), 3)
            player_hp_txt = font.render(f"{player.name} HP: {player.hp}/{player.max_hp}", True, WHITE)
            screen.blit(player_hp_txt, (100, 520))
            
            
            if battle_phase == "COMMAND":
                screen.blit(font.render("たたかう", True, WHITE), (800, 520))
                screen.blit(font.render("にげる", True, WHITE), (800, 580))
                # カーソル
                y = 520 if battle_cursor == 0 else 580
                pg.draw.polygon(screen, WHITE, [(750, y), (750, y+30), (780, y+15)])
            elif battle_phase == "MESSAGE":
                # メッセージの描画
                msg_txt = font.render(battle_message, True, WHITE)
                screen.blit(msg_txt, (100, 580))
                # メッセージ送り案内
                guide_txt = font.render("Press Enter", True, (200, 200, 200))
                screen.blit(guide_txt, (1000, 630))



        pg.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()