import os
import random
import sys
import pygame as pg

# 画面大小
WIDTH, HEIGHT = 1100, 650

# 方向键对应的移动量
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

# 改变当前工作目录为代码所在目录（防止找不到素材）
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """判断对象是否超出画面边界

    参数：
        rct: 要判断的对象的Rect

    返回值：
        (是否在横向边界内, 是否在纵向边界内)
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def draw_timer(screen: pg.Surface, font: pg.font.Font, time_ms: int) -> None:
    """在画面左上角绘制经过时间（秒）

    参数：
        screen: 当前游戏画面 Surface
        font: 用于绘制的字体对象
        time_ms: 当前经过的时间（毫秒）
    """
    sec = time_ms // 1000  # 毫秒转秒
    timer_surf = font.render(f"Time: {sec}s", True, (0, 0, 0))
    screen.blit(timer_surf, (10, 10))


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    # 加载背景图片
    bg_img = pg.image.load("fig/pg_bg.jpg")

    # 载入并缩放こうかとん的图像
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200  # 初始位置

    # 创建红色圆形爆弹
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))  # 设置黑色为透明
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弹初速度

    # 定义字体用于显示时间
    font = pg.font.Font(None, 50)

    clock = pg.time.Clock()
    start_time = pg.time.get_ticks()  # 获取起始时间（毫秒）

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])  # 画背景

        # 检测碰撞：如果撞到爆弹，游戏结束
        if kk_rct.colliderect(bb_rct):
            print("Game Over")
            return

        # 计算こうかとん的移动
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        # 移动并反弹爆弹
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)

        # 显示计时器
        elapsed_time = pg.time.get_ticks() - start_time
        draw_timer(screen, font, elapsed_time)

        pg.display.update()
        clock.tick(50)  # 每秒最多50帧


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
