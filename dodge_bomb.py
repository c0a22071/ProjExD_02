import sys
import pygame as pg
import random
import math

WIDTH, HEIGHT = 1600, 900

# 押下キーと移動量の対応を持つ辞書
dalta = {
    pg.K_UP: (0, -5),    # 上矢印キー：上に5ピクセル移動
    pg.K_DOWN: (0, +5),   # 下矢印キー：下に5ピクセル移動
    pg.K_LEFT: (-5, 0),  # 左矢印キー：左に5ピクセル移動
    pg.K_RIGHT: (5, 0)   # 右矢印キー：右に5ピクセル移動
}

def cheak_bound(obj_rct: pg.Rect):
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = (900,400) # 初期座標

    kk_img_right = pg.transform.flip(kk_img, True, False)
    kk_img_left = pg.transform.rotozoom(kk_img, 0, 1.0)
    kk_img_up = pg.transform.rotate(kk_img,270)
    kk_img_down = pg.transform.rotate(kk_img,90)
    kk_img_dori = pg.transform.rotate(kk_img_right,-45)
    kk_img_dole = pg.transform.rotate(kk_img,45)
    kk_img_upri = pg.transform.rotate(kk_img_right,45)
    kk_img_uple = pg.transform.rotate(kk_img,-45)


    # 爆弾のSurfaceを作成
    bomb_surface = pg.Surface((20, 20), pg.SRCALPHA)
    pg.draw.circle(bomb_surface, (255, 0, 0), (10, 10), 10)

    # 爆弾のRectの位置をランダムに設定
    bomb_rect = bomb_surface.get_rect()
    bomb_rect.x = random.randint(0, WIDTH - bomb_rect.width)
    bomb_rect.y = random.randint(0, HEIGHT - bomb_rect.height)

    # 爆弾の速度を設定
    vx, vy = 5, 5 

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        # 爆弾の位置を速度に応じて移動
        bomb_rect.move_ip(vx, vy)
        yoko,tate = cheak_bound(bomb_rect)
        if not yoko :
            vx *= -1
        if not tate :
            vy *= -1

        screen.blit(bg_img, [0, 0])

        # キーイベントを処理してこうかとんを移動
        keys = pg.key.get_pressed()
        move_amount = [0, 0]
        for key, mv in dalta.items():
            if keys[key]:
                move_amount[0] += mv[0] #　横方向合計移動量
                move_amount[1] += mv[1] #　縦方向合計移動量


        kk_rct.move_ip(move_amount[0],move_amount[1])

        if cheak_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-move_amount[0],-move_amount[1])

        #１．飛ぶ方向にしたがって画像切り替え
        #右
        if keys[pg.K_RIGHT]:
            kk_img = kk_img_right
        #上
        if keys[pg.K_UP]:
            kk_img = kk_img_up
        #下
        if keys[pg.K_DOWN]:
            kk_img = kk_img_down
        #左
        if keys[pg.K_LEFT]:
            kk_img = kk_img_left
        #右下
        if keys[pg.K_DOWN] and keys[pg.K_RIGHT]:
            kk_img = kk_img_dori
        #左下
        if keys[pg.K_DOWN] and keys[pg.K_LEFT]:
            kk_img = kk_img_dole
        #右上
        if keys[pg.K_UP] and keys[pg.K_RIGHT]:
            kk_img = kk_img_upri
        #左上
        if keys[pg.K_UP] and keys[pg.K_LEFT]:
            kk_img = kk_img_uple

           
        screen.blit(kk_img,kk_rct) 

        # こうかとんの位置を更新
        kk_img_rect = kk_img.get_rect(center=(900, 400))
        kk_img_rect.move_ip(move_amount[0], move_amount[1])



        # 衝突判定
        if kk_rct.colliderect(bomb_rect):
            print("ゲームオーバー")
            return  # こうかとんと爆弾が衝突したらreturn


         # 爆弾を画面に描画
        screen.blit(bomb_surface, bomb_rect.topleft)

        pg.display.update()
        tmr += 1
        clock.tick(100)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()