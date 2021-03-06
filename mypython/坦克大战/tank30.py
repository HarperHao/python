'''
新增功能：
   1.给游戏添加结束的场景
'''

import pygame, time, random
from pygame.sprite import Sprite

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
BG_COLOR = pygame.Color(0, 0, 0)
TEXT_COLOR = pygame.Color(255, 0, 0)


# 定义一个基类
class BaseItem(Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)


class MainGame():
    window = None
    my_tank = None
    blood = None
    # 存储敌方坦克的列表
    enemyTankList = []
    # 定义敌方坦克的数量
    enemyTankCount = 5
    # 定义我方坦克可以重生的次数
    myTankLives = 3
    # 存储我方子弹的列表
    myBulletList = []
    # 存储敌方子弹的列表
    enemyBulletList = []
    # 存储爆炸效果的列表
    explodeList = []
    # 存储墙壁的列表
    wallList = []

    # 设置游戏是否结束
    def __init__(self):
        pass

    # 开始游戏
    def startGame(self):
        # 初始化主窗口
        pygame.display.init()
        # 设置窗口的大小及显示
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        # 设置窗口的标题
        pygame.display.set_caption('坦克大战1.30')
        # 设置开始界面
        mode = self.gameStartInterface(MainGame.window)
        # 设置is_quit_game
        self.is_quit_game = False
        # 判断选择的是开始游戏还是退出游戏
        if mode == True:
            exit()
        # 初始化我方坦克
        self.createMytank()
        # 初始化敌方坦克，并将敌方坦克添加到列表中
        self.createEnemyTank()
        # 初始化墙壁
        self.createWall()
        # 初始化我方坦克血槽，这个可以和上面一样优化一下
        MainGame.blood = Blood(MainGame.my_tank)
        while True:
            # 使用坦克移动的速度慢一点
            time.sleep(0.03)
            # 给窗口设置填充色
            MainGame.window.fill(BG_COLOR)
            # 获取事件
            self.getEvent()
            # 绘制文字
            MainGame.window.blit(self.getTextSuface('敌方坦克剩余数量:%d' % len(MainGame.enemyTankList), 18), (10, 10))
            # 绘制血槽
            self.blitBlood()
            # 调用坦克显示的方法，如果我方坦克存活的话
            if MainGame.my_tank and MainGame.my_tank.live:
                MainGame.my_tank.displayTank()
            # 如果我方坦克不存活
            else:
                # 删除我方坦克
                del MainGame.my_tank
                MainGame.my_tank = None
            # 循环遍历敌方坦克列表，展示敌方坦克
            self.blitEnemyTank()
            # 循环遍历显示我方坦克的子弹
            self.blitMyBullet()
            # 循环遍历敌方子弹列表，展示敌方子弹
            self.blitEnemyBullet()
            # 循环遍历爆炸列表，展示爆炸效果
            self.blitExplode()
            # 循环遍历墙壁列表，展示墙壁
            self.blitWall()
            #  调用移动方法，如果坦克的开关是开启，才可以移动
            if MainGame.my_tank and MainGame.my_tank.live:
                if not MainGame.my_tank.stop:
                    MainGame.my_tank.move()
                    # 检测我方坦克是否与墙壁发生碰撞
                    MainGame.my_tank.hitWall()
                    # 检测我方坦克是否与敌方坦克发生 碰撞
                    MainGame.my_tank.myTank_hit_enemyTank()
            if len(MainGame.enemyTankList) == 0:
                self.is_quit_game = self.endGame(is_win=True)
                if self.is_quit_game == True:
                    exit()
                else:
                    self.startGame()

            if MainGame.myTankLives == 0:
                self.is_quit_game = self.endGame(is_win=False)
                if self.is_quit_game == True:
                    exit()
                else:
                    self.startGame()

            pygame.display.update()

    # 初始化墙壁
    def createWall(self):
        for i in range(6):
            # 初始化墙壁
            wall = Wall(i * 130, 220)
            # 将墙壁添加到列表中
            MainGame.wallList.append(wall)

    # 循环遍历墙壁列表，展示墙壁
    def blitWall(self):
        for wall in MainGame.wallList:
            # 判断墙壁是否存活
            if wall.live:
                # 调用墙壁的显示方法
                wall.displayWall()
            else:
                # 从墙壁列表移出
                MainGame.wallList.remove(wall)

    # 展示血槽，可以来个创建血槽
    def blitBlood(self):
        MainGame.blood.displayRedBlood()
        # MainGame.blood.displayGreenBlood()
        MainGame.blood.moveGreenBlood()

    # 创建我方坦克的方法
    def createMytank(self):
        MainGame.my_tank = MyTank(350, 300)
        # 创建Music对象
        music = Music('img/start.wav')
        # 播放音乐
        music.play()

    # 初始化敌方坦克，并将敌方坦克添加到列表中
    def createEnemyTank(self):
        top = 100
        # 循环生成敌方坦克
        for i in range(MainGame.enemyTankCount):
            left = random.randint(0, 600)
            speed = random.randint(1, 4)
            enemy = EnemyTank(left, top, speed)
            MainGame.enemyTankList.append(enemy)

    # 循环遍历敌方坦克列表，展示敌方坦克
    def blitEnemyTank(self):
        for enemyTank in MainGame.enemyTankList:
            # 判断当前敌方坦克是否活着
            if enemyTank.live:
                enemyTank.displayTank()
                enemyTank.randMove()
                # 调用检测是否与墙壁碰撞
                enemyTank.hitWall()
                # 检测敌方坦克是否与我方坦克发生碰撞
                if MainGame.my_tank and MainGame.my_tank.live:
                    enemyTank.enemyTank_hit_myTank()
                # 检测敌方坦克间是否发生碰撞
                enemyTank.enemyTank_hit_enemyTank()
                # 发射子弹
                enemyBullet = enemyTank.shot()
                # 敌方子弹是否是None，如果不为None则添加到敌方子弹列表中
                if enemyBullet:
                    # 将敌方子弹存储到敌方子弹列表中
                    MainGame.enemyBulletList.append(enemyBullet)
            else:  # 不活着，从敌方坦克列表中移除
                MainGame.enemyTankList.remove(enemyTank)

    # 循环展示爆炸效果
    def blitExplode(self):
        for explode in MainGame.explodeList:
            # 判断是否活着
            if explode.live:
                # 展示
                explode.displayExplode()
            else:
                # 在爆炸列表中移除
                MainGame.explodeList.remove(explode)

    # 循环遍历我方子弹存储列表
    def blitMyBullet(self):
        for myBullet in MainGame.myBulletList:
            # 判断当前的子弹是否是活着状态，如果是则进行显示及移动，
            if myBullet.live:
                myBullet.displayBullet()
                # 调用子弹的移动方法
                myBullet.move()
                # 调用检测我方子弹是否与敌方坦克发生碰撞
                myBullet.myBullet_hit_enemyTank()
                # 检测我方子弹是否与墙壁碰撞
                myBullet.hitWall()
            # 否则在列表中删除
            else:
                MainGame.myBulletList.remove(myBullet)

    # 循环遍历敌方子弹列表，展示敌方子弹
    def blitEnemyBullet(self):
        for enemyBullet in MainGame.enemyBulletList:
            if enemyBullet.live:  # 判断敌方子弹是否存活
                enemyBullet.displayBullet()
                enemyBullet.move()
                # 调用敌方子弹与我方坦克碰撞的方法
                enemyBullet.enemyBullet_hit_myTank()
                # 检测敌方子弹是否与墙壁碰撞
                enemyBullet.hitWall()
            else:
                MainGame.enemyBulletList.remove(enemyBullet)

    # 开始界面的绘制
    def gameStartInterface(self, screen):
        # 加载初始界面游戏背景
        background_img = pygame.image.load('img/background.png')
        background_img = pygame.transform.scale(background_img, (800, 500))
        color_white = (255, 255, 255)
        color_red = (255, 0, 0)
        # 设置字体
        pygame.font.init()
        font = pygame.font.Font('font/font.TTF', SCREEN_WIDTH // 12)
        # 设置logo图片和它的位置
        logo_img = pygame.image.load('img/logo.png')
        logo_img = pygame.transform.scale(logo_img, (450, 70))
        logo_rect = logo_img.get_rect()
        logo_rect.centerx, logo_rect.centery = SCREEN_WIDTH / 2, SCREEN_HEIGHT // 4
        # 设置坦克cursor
        tank_cursor = pygame.image.load('img/p1tankR.gif')
        tank_rect = tank_cursor.get_rect()
        # “开始游戏”这四个字
        player_render_white = font.render('START', True, color_white)
        player_render_red = font.render('START', True, color_red)
        # 设置这四个字的位置
        player_rect = player_render_white.get_rect()
        player_rect.left, player_rect.top = SCREEN_WIDTH / 2.8, SCREEN_HEIGHT / 2.5
        # 设置“退出游戏”这四个字
        players_render_white = font.render('EXIT', True, color_white)
        players_render_red = font.render('EXIT', True, color_red)
        players_rect = players_render_white.get_rect()
        players_rect.left, players_rect.top = SCREEN_WIDTH / 2.8, SCREEN_HEIGHT / 2
        # 游戏提示
        game_tip = font.render('press <Enter> to start', True, color_white)
        game_tip_rect = game_tip.get_rect()
        game_tip_rect.centerx, game_tip_rect.top = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.4
        # 设置提示字的闪烁参数
        game_tip_flash_time = 35
        game_tip_flash_count = 0
        game_tip_show_flag = True
        # 主循环
        clock = pygame.time.Clock()
        judge_mode = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    # 如果是回车键
                    if event.key == pygame.K_RETURN:
                        return judge_mode
                    # 如果是方向键
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                        judge_mode = not judge_mode
            # 将背景图片和logo绘制到screen上
            screen.blit(background_img, (0, 0))
            screen.blit(logo_img, logo_rect)
            # 设置闪烁效
            game_tip_flash_count += 1
            if game_tip_flash_count > game_tip_flash_time:
                game_tip_show_flag = not game_tip_show_flag
                game_tip_flash_count = 0
            if game_tip_show_flag:
                screen.blit(game_tip, game_tip_rect)
            # 设置Cursor的移动，红色的是选中，白色的是未选中
            if not judge_mode:
                tank_rect.right, tank_rect.top = player_rect.left, player_rect.top - 10
                screen.blit(tank_cursor, tank_rect)
                screen.blit(player_render_red, player_rect)
                screen.blit(players_render_white, players_rect)
            else:
                tank_rect.right, tank_rect.top = players_rect.left, players_rect.top - 10
                screen.blit(tank_cursor, tank_rect)
                screen.blit(player_render_white, player_rect)
                screen.blit(players_render_red, players_rect)
            pygame.display.update()
            clock.tick(100)

    # 结束游戏
    def endGame(self, is_win=True):
        print('结束游戏画面')
        background_img = pygame.image.load('img/background.png')
        background_img = pygame.transform.scale(background_img, (800, 500))
        color_white = (255, 255, 255)
        color_red = (255, 0, 0)
        font = pygame.font.Font('font/font.TTF', SCREEN_WIDTH // 12)
        # 游戏失败图
        gameover_img = pygame.image.load('img/gameover.png')
        gameover_img = pygame.transform.scale(gameover_img, (150, 75))
        gameover_img_rect = gameover_img.get_rect()
        gameover_img_rect.midtop = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 8
        # 游戏胜利与否的提示
        if is_win:
            font_render = font.render('Congratulations, You win!', True, color_white)
        else:
            font_render = font.render('Sorry, You fail!', True, color_white)
        font_rect = font_render.get_rect()
        font_rect.centerx, font_rect.centery = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3
        # 用于选择退出或重新开始
        tank_cursor = pygame.image.load('img/p1tankR.gif')
        tank_rect = tank_cursor.get_rect()
        restart_render_white = font.render('RESTART', True, color_white)
        restart_render_red = font.render('RESTART', True, color_red)
        restart_rect = restart_render_white.get_rect()
        restart_rect.left, restart_rect.top = SCREEN_WIDTH / 2.4, SCREEN_HEIGHT / 2
        quit_render_white = font.render('QUIT', True, color_white)
        quit_render_red = font.render('QUIT', True, color_red)
        quit_rect = quit_render_white.get_rect()
        quit_rect.left, quit_rect.top = SCREEN_WIDTH / 2.4, SCREEN_HEIGHT / 1.6
        is_quit_game = False
        # 主循环
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return is_quit_game
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                        is_quit_game = not is_quit_game
            # 放在主窗口
            MainGame.window.blit(background_img, (0, 0))
            MainGame.window.blit(font_render, font_rect)
            if not is_quit_game:
                tank_rect.right, tank_rect.top = restart_rect.left - 10, restart_rect.top
                MainGame.window.blit(tank_cursor, tank_rect)
                MainGame.window.blit(restart_render_red, restart_rect)
                MainGame.window.blit(quit_render_white, quit_rect)
            else:
                tank_rect.right, tank_rect.top = quit_rect.left - 10, quit_rect.top
                MainGame.window.blit(tank_cursor, tank_rect)
                MainGame.window.blit(restart_render_white, restart_rect)
                MainGame.window.blit(quit_render_red, quit_rect)
            pygame.display.update()
            clock.tick(60)

    # 左上角文字的绘制
    def getTextSuface(self, text, size):
        # 初始化字体模块
        pygame.font.init()
        # 查看所有的字体名称
        # print(pygame.font.get_fonts())
        # 获取字体Font对象
        font = pygame.font.SysFont('kaiti', size)
        # 绘制文字信息
        textSurface = font.render(text, True, TEXT_COLOR)
        return textSurface

    # 获取事件
    def getEvent(self):
        # 获取所有事件
        eventList = pygame.event.get()
        # 遍历事件
        for event in eventList:
            # 判断按下的键是关闭还是键盘按下
            # 如果按的是退出，关闭窗口
            if event.type == pygame.QUIT:
                exit()
                # self.endGame()
            # 如果是键盘的按下
            if event.type == pygame.KEYDOWN:
                # 当我方坦克死亡
                if not MainGame.my_tank and MainGame.myTankLives > 0:
                    # 判断按下的是Esc键，让坦克重生
                    if event.key == pygame.K_ESCAPE:
                        # 让我方坦克重生及调用创建坦克的方法
                        self.createMytank()
                if MainGame.my_tank and MainGame.my_tank.live:
                    # 判断按下的是上、下、左、右
                    if event.key == pygame.K_LEFT:
                        # 切换方向
                        MainGame.my_tank.direction = 'L'
                        # 修改坦克的开关状态
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()
                        print('按下左键，坦克向左移动')
                    elif event.key == pygame.K_RIGHT:
                        # 切换方向
                        MainGame.my_tank.direction = 'R'
                        # 修改坦克的开关状态
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()
                        print('按下右键，坦克向右移动')
                    elif event.key == pygame.K_UP:
                        # 切换方向
                        MainGame.my_tank.direction = 'U'
                        # 修改坦克的开关状态
                        MainGame.my_tank.stop = False
                        # MainGame.my_tank.move()
                        print('按下上键，坦克向上移动')
                    elif event.key == pygame.K_DOWN:
                        # 切换方向
                        MainGame.my_tank.direction = 'D'
                        # 修改坦克的开关状态
                        MainGame.my_tank.stop = False
                        print('按下左键，坦克向下移动')
                    elif event.key == pygame.K_SPACE:
                        print('发射子弹')
                        # 如果当前我方子弹列表的大小 小于2时候才可以创建
                        if len(MainGame.myBulletList) < 2:
                            # 创建我方坦克发射的子弹
                            myBullet = Bullet(MainGame.my_tank)
                            MainGame.myBulletList.append(myBullet)
                            # 我方坦克发射子弹添加音效
                            music = Music('img/hit.wav')
                            music.play()
            # 松开方向键，坦克停止移动，修改坦克的开关状态
            if event.type == pygame.KEYUP:
                # 判断松开的键是上、下、左、右时候才停止坦克移动
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if MainGame.my_tank and MainGame.my_tank.live:
                        MainGame.my_tank.stop = True


class Blood():
    def __init__(self, MyTank):
        self.MyTank_Hp = MyTank.myTankHp
        # 获取图片对象-
        self.red_blood = pygame.image.load('img/health_red.png')
        self.green_blood = pygame.image.load('img/health_green.png')

        self.green_rect = self.green_blood.get_rect()
        self.left = self.green_rect.left
        self.top = self.green_rect.top

    def displayRedBlood(self):
        MainGame.window.blit(self.red_blood, (600, 10))

    def displayGreenBlood(self):
        # 先将红色血条放上去，再将绿色血条放上去
        # MainGame.window.blit(self.red_blood, (600, 10))
        MainGame.window.blit(self.green_blood, (600, 10))
        # self.moveBlood()

    def moveGreenBlood(self):
        # print("Hp为{}".format(self.MyTank_Hp))
        self.distance = self.green_rect.width // 4
        # 如果我方坦克存在的话
        if MainGame.my_tank:
            if MainGame.my_tank.myTankHp == 4:
                MainGame.window.blit(self.green_blood, (600, 10))
            elif MainGame.my_tank.myTankHp == 3:
                MainGame.window.blit(self.green_blood, (600 + self.distance, 10))
            elif MainGame.my_tank.myTankHp == 2:
                MainGame.window.blit(self.green_blood, (600 + self.distance * 2, 10))
            elif MainGame.my_tank.myTankHp == 1:
                MainGame.window.blit(self.green_blood, (600 + self.distance * 3, 10))
            elif MainGame.my_tank.myTankHp == 0:
                MainGame.window.blit(self.green_blood, (600 + self.distance * 4, 10))


class Tank(BaseItem):
    # 添加距离左边left 距离上边top
    def __init__(self, left, top):
        # 保存加载的图片
        self.images = {
            'U': pygame.image.load('img/p1tankU.gif'),
            'D': pygame.image.load('img/p1tankD.gif'),
            'L': pygame.image.load('img/p1tankL.gif'),
            'R': pygame.image.load('img/p1tankR.gif'),
        }
        # 方向
        self.direction = 'L'
        # 根据当前图片的方向获取图片 surface
        self.image = self.images[self.direction]
        # 根据图片获取区域
        self.rect = self.image.get_rect()
        # 设置区域的left 和top
        self.rect.left = left
        self.rect.top = top
        # 速度  决定移动的快慢
        self.speed = 4
        # 坦克移动的开关
        self.stop = True
        # 是否活着
        self.live = True
        # 新增属性原来坐标
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top

    # 移动
    def move(self):
        # 移动后记录原始的坐标
        self.oldLeft = self.rect.left
        self.oldTop = self.rect.top
        # 判断坦克的方向进行移动
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed
        elif self.direction == 'R':
            if self.rect.left + self.rect.height < SCREEN_WIDTH:
                self.rect.left += self.speed

    # 射击
    def shot(self):
        return Bullet(self)

    # 保持原位
    def stay(self):
        self.rect.left = self.oldLeft
        self.rect.top = self.oldTop

    # 检测坦克是否与墙壁发生碰撞
    def hitWall(self):
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(self, wall):
                # 将坐标设置为移动之前的坐标
                self.stay()

    # 展示坦克的方法
    def displayTank(self):
        # 获取展示的对象
        self.image = self.images[self.direction]
        # 调用blit方法展示
        MainGame.window.blit(self.image, self.rect)


# 我方坦克
class MyTank(Tank):
    # 设置我方坦克的HP

    def __init__(self, left, top):
        super(MyTank, self).__init__(left, top)
        self.myTankHp = 4

    # 检测我方坦克与敌方坦克发生碰撞
    def myTank_hit_enemyTank(self):
        # 循环遍历敌方坦克列表
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(self, enemyTank):
                self.stay()


# 敌方坦克
class EnemyTank(Tank):
    def __init__(self, left, top, speed):
        # 调用父类的初始化方法
        super(EnemyTank, self).__init__(left, top)
        # 加载图片集
        self.images = {
            'U': pygame.image.load('img/enemy1U.gif'),
            'D': pygame.image.load('img/enemy1D.gif'),
            'L': pygame.image.load('img/enemy1L.gif'),
            'R': pygame.image.load('img/enemy1R.gif')
        }
        # 方向,随机生成敌方坦克的方向
        self.direction = self.randDirection()
        # 根据方向获取图片
        self.image = self.images[self.direction]
        # 区域
        self.rect = self.image.get_rect()
        # 对left和top进行赋值
        self.rect.left = left
        self.rect.top = top
        # 速度
        self.speed = speed
        # 移动开关键
        self.flag = True
        # 薪增加一个步数变量 step
        self.step = 60

    # 敌方坦克与我方坦克是否发生碰撞
    def enemyTank_hit_myTank(self):
        if pygame.sprite.collide_rect(self, MainGame.my_tank):
            self.stay()

    # 敌方坦克之间碰撞的检测
    def enemyTank_hit_enemyTank(self):
        for enemyTank in MainGame.enemyTankList:
            if enemyTank is not self:
                if pygame.sprite.collide_rect(self, enemyTank):
                    self.stay()

    # 随机生成敌方坦克的方向
    def randDirection(self):
        num = random.randint(1, 4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return "L"
        elif num == 4:
            return 'R'

    # 敌方坦克随机移动的方法
    def randMove(self):
        if self.step <= 0:
            # 修改方向
            self.direction = self.randDirection()
            # 让步数复位
            self.step = 45
        else:
            self.move()
            # 让步数递减
            self.step -= 1

    # 重写shot()
    def shot(self):
        # 随机生成100以内的数
        num = random.randint(1, 1000)
        if num < 20:
            return Bullet(self)


# 子弹类
class Bullet(BaseItem):
    def __init__(self, tank):
        # 加载图片
        self.image = pygame.image.load('img/enemymissile.gif')
        # 坦克的方向决定子弹的方向
        self.direction = tank.direction
        # 获取区域
        self.rect = self.image.get_rect()
        # 获取坦克对象
        self.tank = tank
        # 子弹的left和top与方向有关
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.height
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2 - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        # 子弹的速度
        self.speed = 6
        # 子弹的状态，是否碰到墙壁，如果碰到墙壁，修改此状态
        self.live = True

    # 移动
    def move(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                # 修改子弹的状态
                self.live = False
        elif self.direction == 'R':
            if self.rect.left + self.rect.width < SCREEN_WIDTH:
                self.rect.left += self.speed
            else:
                # 修改子弹的状态
                self.live = False
        elif self.direction == 'D':
            if self.rect.top + self.rect.height < SCREEN_HEIGHT:
                self.rect.top += self.speed
            else:
                # 修改子弹的状态
                self.live = False
        elif self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                # 修改子弹的状态
                self.live = False

    # 子弹是否碰撞墙壁
    def hitWall(self):
        # 循环遍历墙壁列表
        for wall in MainGame.wallList:
            if pygame.sprite.collide_rect(self, wall):
                # 修改子弹的生存状态，让子弹消失
                self.live = False
                # 墙壁的生命值减小
                wall.hp -= 1
                if wall.hp <= 0:
                    # 修改墙壁的生存状态
                    wall.live = False

    # 展示子弹的方法
    def displayBullet(self):
        # 将图片surface加载到窗口
        MainGame.window.blit(self.image, self.rect)

    # 我方子弹与敌方坦克的碰撞
    def myBullet_hit_enemyTank(self):
        # 循环遍历敌方坦克列表，判断是否发生碰撞
        for enemyTank in MainGame.enemyTankList:
            if pygame.sprite.collide_rect(enemyTank, self):
                # 修改敌方坦克和我方子弹的状态
                enemyTank.live = False
                self.live = False
                # 创建爆炸对象
                explode = Explode(enemyTank)
                # 将爆炸对象添加到爆炸列表中
                MainGame.explodeList.append(explode)

    # 敌方子弹与我方坦克的碰撞
    def enemyBullet_hit_myTank(self):
        if MainGame.my_tank and MainGame.my_tank.live:
            if pygame.sprite.collide_rect(MainGame.my_tank, self):
                # 产生爆炸对象
                explode = Explode(MainGame.my_tank)
                # 将爆炸对象添加到爆炸列表中
                MainGame.explodeList.append(explode)
                # 修改敌方子弹与我方坦克的状态和我方剩余坦克数量
                self.live = False
                # 修改我方坦克HP
                if MainGame.my_tank.myTankHp > 0:
                    MainGame.my_tank.myTankHp -= 1
                    print("修改成功")
                # 如果我方坦克HP为0，则myTankLives减1
                if MainGame.my_tank.myTankHp == 0:
                    MainGame.myTankLives -= 1
                    MainGame.my_tank.live = False


class Wall():
    def __init__(self, left, top):
        # 加载墙壁图片
        self.image = pygame.image.load('img/steels.gif')
        # 获取墙壁的区域
        self.rect = self.image.get_rect()
        # 设置位置left、top
        self.rect.left = left
        self.rect.top = top
        # 是否存活
        self.live = True
        # 设置生命值
        self.hp = 3

    # 展示墙壁的方法
    def displayWall(self):
        MainGame.window.blit(self.image, self.rect)


class Explode():
    def __init__(self, tank):
        # 爆炸的位置由当前子弹打中的坦克位置决定
        self.rect = tank.rect
        self.images = [
            pygame.image.load('img/blast0.gif'),
            pygame.image.load('img/blast1.gif'),
            pygame.image.load('img/blast2.gif'),
            pygame.image.load('img/blast3.gif'),
            pygame.image.load('img/blast4.gif'),
        ]
        self.step = 0
        self.image = self.images[self.step]
        # 是否活着
        self.live = True

    # 展示爆炸效果的方法
    def displayExplode(self):
        if self.step < len(self.images):
            # 根据索引获取爆炸对象
            self.image = self.images[self.step]
            self.step += 1
            # 添加到主窗口
            MainGame.window.blit(self.image, self.rect)
        else:
            # 修改活着的状态
            self.live = False
            self.step = 0


class Music():
    def __init__(self, filename):
        self.filename = filename
        # 初始化音乐混合器
        pygame.mixer.init()
        # 加载音乐
        pygame.mixer.music.load(self.filename)

    # 播放音乐
    def play(self):
        pygame.mixer.music.play()


if __name__ == '__main__':
    MainGame().startGame()
