import pygame
import sys,math,random,time

#初始化界面
pygame.init()
screen = pygame.display.set_mode((800,600))
bgimg = pygame.image.load('static/bgimg.jpeg')
icon = pygame.image.load('static/aoligei.jpg')
pygame.display.set_caption('打飞机')
pygame.display.set_icon(icon)
#游戏结束，在show_enemy()中判断
is_over = False
#添加音效
pygame.mixer.music.load('static/bg.mp3')
pygame.mixer.music.play(-1)
def distance(x1,y1,x2,y2):
    d1 = x2-x1
    d2 = y2-y1
    return math.sqrt(d1*d1+d2*d2)
#显示分数
font = pygame.font.SysFont('宋体',32)
score = 0
def show_score():
    text = f"Score:{score}"
    score_render = font.render(text,True,(0,255,0))
    screen.blit(score_render,(10,10))
#飞机
plane = pygame.image.load('static/plane.jpg')
planeX = 400
planeY = 550
planeStep = 20
#敌人
class Enemy:
    def __init__(self):
        self.img = pygame.image.load('static/enemy.jpg')
        self.x = random.randrange(20,740)
        self.y = random.randrange(20,200)
        self.stepX = 1
        self.stepY = 1
        self.direction = random.randint(0,1)
enemys = []
for i in range(5):
    enemys.append(Enemy())
#子弹
bullet = pygame.image.load('static/bullet.jpg')
bullets = []
class Bullet:
    global planeX,planeY
    def __init__(self):
        self.img = pygame.image.load('static/bullet.jpg')
        self.x = planeX +10
        self.y = planeY +10
        self.step = 5
#显示飞机
def show_plane():
    global planeX,planeY
    screen.blit(plane,(planeX,planeY))
    if planeX > 750:
        planeX = 750
    if planeX < 20:
        planeX = 20
#显示敌人,plane和enemy碰撞检测
def show_enemy():
    global enemys,is_over
    for enemy in enemys:
        screen.blit(enemy.img, (enemy.x, enemy.y))
        enemy.y += enemy.stepY
        if enemy.direction == 0:
            enemy.x +=enemy.stepX
        else:
            enemy.x -=enemy.stepX
        if distance(enemy.x+20,enemy.y-20,planeX+20,planeY-20)<40:   #判断游戏是否结束
            is_over = True
            break
        if enemy.x>750:
            enemy.stepX = -enemy.stepX
        if enemy.x<0:
            enemy.stepX = -enemy.stepX
        if enemy.y>700:
            if enemy in enemys:
                enemys.remove(enemy)
#显示子弹,碰撞检测
def show_bullet():
    global bullets,score
    for bullet in bullets:
        screen.blit(bullet.img,(bullet.x,bullet.y))
        bullet.y -= bullet.step
        if bullet.y < -10:
            bullets.remove(bullet)
        for enemy in enemys:
            if bullet in bullets:
                if distance(enemy.x,enemy.y,bullet.x,bullet.y)<30:  #碰撞检测
                    bullets.remove(bullet)
                    if enemy in enemys:
                        enemys.remove(enemy)
                    score += 1

#键盘事件监控
running = True
def process_event():
    global running,planeX,planeY,is_over,score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            planeX = planeX - planeStep
        elif keys[pygame.K_RIGHT]:
            planeX = planeX + planeStep
        elif keys[pygame.K_SPACE]:
            bullets.append(Bullet())
        elif keys[pygame.K_r]:   # R键重新开始
            score = 0
            is_over = False

#定时10秒产生敌人
start_time = time.time()
def produce_enemys():
    global enemys,start_time,flag
    if time.time()-start_time>10:
        for i in range(10):
            enemys.append(Enemy())
        start_time = time.time()
#判断游戏是否结束显示Game Over
def show_game_over():
    text = "Game Over"
    font = pygame.font.SysFont('宋体', 100)
    score_render = font.render(text, True, (0, 255, 0))
    screen.blit(score_render, (200, 200))
#游戏循环
while running:
    screen.blit(bgimg,(0,0))
    process_event()
    show_enemy()
    show_score()
    show_plane()
    show_bullet()
    if not is_over:
        produce_enemys()
    if is_over:
        show_game_over()
    pygame.display.update()
