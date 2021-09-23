import pygame
import random
import os
from pygame.constants import KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEWHEEL, NOEVENT
from pygame.key import set_repeat
from pygame.version import SDL



# 基本變數
FPS = 60
score = 0
Width = 500
Width_min = 0 
Height = 600

Black = (0,0,0)
White = (255,255,255)
Green = (0,255,0)
Red = (200,0,0)
bright_Red = (255,0,0)
Yellow = (255,255,0)
my_path="C:/Users/Kevin8799/OneDrive/桌面/程式語言/Python 練習/PY_game/img"
my_path2="C:/Users/Kevin8799/OneDrive/桌面/程式語言/Python 練習/PY_game/sound"

 #按鈕定位上下限
btn_width_right = Width/2-70
btn_width_left = Width/2-100+170
btn_width_top = Height/2+100
btn_width_bottom = Height/2+150

#遊戲初始化 and 創建視窗
pygame.init()  #pygame的初始化
pygame.mixer.init()  #音樂初始化
screen = pygame.display.set_mode((Width, Height))  #視窗大小設定
game_name = pygame.display.set_caption("太空火箭") #遊戲名稱
clock = pygame.time.Clock()  #計時物件


#載入圖片
icon_img = pygame.image.load(os.path.join(my_path, "icon.png")).convert()
icon_img = pygame.transform.scale(icon_img,(30,25))
icon_img.set_colorkey(Black)
game_icon = pygame.display.set_icon(icon_img) #遊戲圖示
background_img = pygame.image.load(os.path.join(my_path, "background.png")).convert()
background2_img = pygame.image.load(os.path.join(my_path, "background2.png")).convert()
player_img = pygame.image.load(os.path.join(my_path, "player.png")).convert()
player_mini_img = pygame.transform.scale(player_img,(25,25))
player_mini_img.set_colorkey(Black)
#rock_img = pygame.image.load(os.path.join("PY_game/img", "rock.png")).convert()
bullet_img = pygame.image.load(os.path.join(my_path, "bullet.png")).convert()
#7張石頭生成的圖片
rock_imgs = [] #設為陣列
for i in range(7):   #迴圈的方式加入陣列
    rock_imgs.append(pygame.image.load(os.path.join(my_path,f"rock{i}.png")).convert())

#石頭爆炸的圖片
expl_explode = {}     #將爆炸圖片存放在字典
expl_explode['lg'] = [] #大爆炸
expl_explode['sm'] = [] #小爆炸
expl_explode['player'] = []  #火箭的爆炸
for i in range(9):
   expl_img = pygame.image.load(os.path.join(my_path, f"expl{i}.png")).convert()
   expl_img.set_colorkey(Black)
   expl_explode['lg'].append(pygame.transform.scale(expl_img, (75,75))) #大爆炸分類，並丟入列表
   expl_explode['sm'].append(pygame.transform.scale(expl_img, (30,30))) #小爆炸分類，並丟入列表
   #火箭的部分
   player_expl_img = pygame.image.load(os.path.join(my_path, f"player_expl{i}.png")).convert()
   player_expl_img.set_colorkey(Black)
   expl_explode['player'].append(player_expl_img) #火箭分類，並丟入列表

#技能強化圖片
power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join(my_path,"shield.png")).convert()
power_imgs['gun'] = pygame.image.load(os.path.join(my_path,"gun.png")).convert()

#按鈕圖片
start_img = pygame.image.load(os.path.join(my_path, "game_start.png")).convert()


#載入音樂
pygame.mixer.music.load(os.path.join(my_path2, "background.ogg"))  #背景音樂
pygame.mixer.music.set_volume(0.2)  #音量大小
shoot_sound = pygame.mixer.Sound(os.path.join(my_path2, "shoot.wav"))  #射擊音樂
dead_sound = pygame.mixer.Sound(os.path.join(my_path2, "rumble.ogg"))  #死亡音樂
expl_sounds = [                                                               #石頭爆炸音樂
    pygame.mixer.Sound(os.path.join(my_path2, "expl0.wav")) ,
    pygame.mixer.Sound(os.path.join(my_path2, "expl1.wav"))
]
shield_sound = pygame.mixer.Sound(os.path.join(my_path2, "pow0.wav")) #補血音效
gun_sound = pygame.mixer.Sound(os.path.join(my_path2, "pow1.wav")) #子彈升級音效



#---------------------------------------------------------------------------#

#分數的顯示函式
font_name = os.path.join("C:/Users/Kevin8799/OneDrive/桌面/程式語言/Python 練習/PY_game", "font.ttf")  #文字的字體
def draw_text(surf , text , size , x , y):
    font = pygame.font.Font(font_name, size)      #文字屬性
    text_surface = font.render(text, True, White)  #文字眩覽
    text_rect = text_surface.get_rect()          #文字定位
    text_rect.centerx = x 
    text_rect.top = y
    surf.blit(text_surface, text_rect)
 

#石頭生成函式
def new_rock():
    rock = Rock()
    all_sprite.add(rock)
    rocks.add(rock)

#血量要顯示在視窗的函式
def draw_health(surf, hp , x , y):
    if hp < 0:
        hp = 0
    BAR_Length = 100  #血條長度
    BAR_Height = 10   #血條寬度
    fill = (hp / 100) * BAR_Length  #血條的填滿,(hp/100) = 血量的幾%
    outline_rect = pygame.Rect(x, y, BAR_Length , BAR_Height)  #血條外框
    fill_rect = pygame.Rect( x , y, fill , BAR_Height)  #血條殘餘血量
    pygame.draw.rect(surf, Green, fill_rect)        #無加入第四個參數，會全部填滿
    pygame.draw.rect(surf, Black, outline_rect, 2)  #加入第四個參數，會只有外框

#復活次數
def draw_lives(surf, lives , img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()  #圖片定位
        img_rect.x = x + 30 *i     #間隔30公分 * i 張圖
        img_rect.y = y
        surf.blit(img , img_rect)

#遊戲開始的畫面顯示
def game_intro():
    screen.blit(background2_img,(0,0))
    btn_start = Button(Width/2-100,Height/2+50,start_img) #按鈕
    draw_text(screen , '太空火箭', 64, Width/2, Height/8)
    draw_text(screen , '當前分數為'+ str(score), 24, Width/2, Height/3)
    draw_text(screen , '操作說明：', 22, Width/2-120, Height/4+100)
    draw_text(screen , '← →為左右移動，空白鍵為射擊', 24, Width/2, Height/2)
    draw_text(screen , '製作者：許智煒', 20, Width-100, Height-50)
    btn_start.draw()  #畫出開始按鈕
    pygame.display.update()
    waiting =  True     #等待時間開始
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():     #取得正在操作的事件，並以列表方式存取
            if event.type == pygame.QUIT:    #如果點選X，跳出迴圈
                pygame.quit()
                return True
            elif event.type == MOUSEBUTTONDOWN:   #按下滑鼠的這項指令
                mouse = pygame.mouse.get_pos()    #抓出滑鼠按下的座標
                if btn_width_left > mouse[0] > btn_width_right and btn_width_bottom > mouse[1] > btn_width_top:  #設定按下的座標範圍來進行遊戲
                    waiting = False
                    return False


#---------------------------------------------------------------------------#


#火箭的部分
class Player(pygame.sprite.Sprite):   #創建一個Class，並繼承pygame裡內建的sprite函式
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #sprite內建的init()
        self.image = pygame.transform.scale(player_img ,(60,50))#圖片的大小
        self.image.set_colorkey(Black)  #將火箭的黑色部分變為透明
        self.radius = 20
        self.rect = self.image.get_rect()  #圖片位於視窗的定位設定
        # draw_circle = pygame.draw.circle(self.image,Red,self.rect.center,self.radius) #用來判斷碰撞範圍
        self.rect.center = (Width/2 , Height-50)  #火箭的位置
        self.speedx = 8    #移動速度
        self.health = 100 #血量
        self.lives = 3    #復活次數
        self.hidden =  False  #火箭復活是否隱藏
        self.hide_time = 0    #火箭復活的隱藏時間
        self.gun = 1            #子彈1發
        self.gun_time = 0   #技能的存在時間

    #火箭的左右移動
    def update(self):
        if self.gun >= 2 and pygame.time.get_ticks() - self.gun_time > 5000:        #子彈的升級時間
            self.gun -= 1
            self.gun_time = pygame.time.get_ticks()

        if self.hidden and pygame.time.get_ticks() - self.hide_time >1000 :        #檢查是否再隱藏期中，並且將update函式觸發時間 - 隱藏時間
            self.hidden = False
            self.rect.center = (Width/2 , Height-50)            #符合條件，將火箭呼叫回來

        Key_pressed = pygame.key.get_pressed() #檢查鍵盤是否有被案，並回傳布林值，有=True、沒=False
        if Key_pressed[pygame.K_RIGHT]:   #判斷右鍵
            self.rect.x += self.speedx 
            if self.rect.right > Width:    
                self.rect.right = Width

        if Key_pressed[pygame.K_LEFT]:   #判斷左鍵
            self.rect.x -= self.speedx 
            if self.rect.left < Width_min :    
                self.rect.left = Width_min
    #火箭的射擊            
    def shoot(self):
        if not(self.hidden):         #hidden為false的情況下才能射擊
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)   #傳入火箭的位置、頂部(子彈從頂部發射)
                all_sprite.add(bullet)   #加入all_sprite的群組
                bullets.add(bullet)
                shoot_sound.play()    #啟用音效
            elif self.gun >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery) 
                bullet2 = Bullet(self.rect.right, self.rect.centery)   
                all_sprite.add(bullet1,bullet2)   
                bullets.add(bullet1,bullet2)
                shoot_sound.play()

    #復活的隱藏期
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks() #紀錄時間
        self.rect.center = (Width/2 , Height+500) #讓火箭隱藏在視窗外

    #子彈等級
    def gunup(self):
        self.gun +=1
        self.gun_time = pygame.time.get_ticks()
  
#隕石的部分
class Rock(pygame.sprite.Sprite):   
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image_ori = random.choice(rock_imgs)  #隨機選擇石頭(無轉動)
        self.image_ori.set_colorkey(Black)
        self.image = self.image_ori.copy() #石頭已轉動
        self.rect = self.image.get_rect() 
        self.radius = int((self.rect.width *0.8) / 2)      #半徑為物件的寬度*0.8後再除於2
        #draw_circle = pygame.draw.circle(self.image,Red,self.rect.center,self.radius)  #用來判斷碰撞範圍
        self.rect.x = random.randrange(0 , Width - self.rect.width) #寬度寬度-石頭寬度
        self.rect.y = random.randrange(-200 , -100) #從視窗看不到的地方生成並掉落
        self.speedy = random.randrange(1 , 3)        #垂直掉落速度
        self.speedx = random.randrange(-3 , 3)        #水平掉落速度
        self.total_degree = 0                   #石頭總幅度初始化
        self.rot_degree = random.randrange(-3 , 3)   #石頭轉動幅度

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360  #限制轉動超過360度
        self.image = pygame.transform.rotate(self.image_ori , self.total_degree)
        center = self.rect.center   #設置中心點
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom > Height or self.rect.left > Width or self.rect.right < Width_min :  #石頭超出視窗的下面及左右兩邊就立刻重製
            self.rect.x = random.randrange(0 , Width - self.rect.width) 
            self.rect.y = random.randrange(-100 , -50) 
            self.speedy = random.randrange(2 , 10)       
            self.speedx = random.randrange(-3 , 3)        

#子彈的部分
class Bullet(pygame.sprite.Sprite):   
    def __init__(self, x, y):  #傳入火箭的X,Y座標
        pygame.sprite.Sprite.__init__(self) 
        self.image = bullet_img  #子彈大小
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect() 
        self.rect.centerx = x      #子彈頂部為戰機的X
        self.rect.bottom = y  #子彈底部為戰機的Y
        self.speedy = -10 #子彈往上射

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:  #子彈底部小於0，表示超出視窗頂端
            self.kill()   #將子彈移除    

#爆炸的部分
class Explosion(pygame.sprite.Sprite):   
    def __init__(self, center, size):  #傳入爆炸得中心點、大小
        pygame.sprite.Sprite.__init__(self) 
        self.size = size  #爆炸大小
        self.image = expl_explode[self.size][0] #大小爆炸的第1張圖片
        self.rect = self.image.get_rect() 
        self.rect.center = center     #爆炸的中心點
        self.frame = 0  #當前更新到的圖片
        self.last_update = pygame.time.get_ticks() #圖片最後的更新時間
        self.frame_rate = 50  #圖片更新時間

    def update(self):
       now = pygame.time.get_ticks()  #現在的時間
       if now - self.last_update > self.frame_rate:    #現在時間 - 最後更新的時間 是否超過 原先預定的更新時間
           self.last_update = now 
           self.frame += 1
           if self.frame == len(expl_explode[self.size]):       #如果更新到最後一張，就刪掉
               self.kill()
           else: 
               self.image = expl_explode[self.size][self.frame]   #接續下一張
               center = self.rect.center
               self.rect = self.image.get_rect()   #重新定位
               self.rect.center = center

#技能的部分
class Power(pygame.sprite.Sprite):   
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self) 
        self.type = random.choice(['shield','gun'])  #技能的類型，以隨機的方式
        self.image = power_imgs[self.type]
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect() 
        self.rect.center = center      
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > Height:
            self.kill()    

#按鈕的部分
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(start_img,(200,150))  #按鈕圖片
        self.image.set_colorkey(Black)
        self.rect = self.image.get_rect()  #按鈕位置
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        screen.blit(self.image,(self.rect.x,self.rect.y))  #畫出按鈕
  
#---------------------------------------------------------------------------#

#遊戲執行迴圈
show_init = True  #判斷初始化面
running = True  #程式是否運作
pygame.mixer.music.play(-1) #背景音樂-1代表循環播放
while running:
    clock.tick(FPS) #螢幕刷新率 
    if show_init :
        colse = game_intro()
        if colse == True:
            break
        show_init = False
        #創建角色(sprite)的群組
        all_sprite = pygame.sprite.Group()  #全部物件的群組
        rocks = pygame.sprite.Group()  #石頭的群組
        bullets = pygame.sprite.Group()  #子彈的群組
        powers = pygame.sprite.Group()   #戰機吃到技能的群組
        player = Player() 
        all_sprite.add(player)
       #用迴圈去生成石頭
        for i in range (8):
           new_rock()
        score = 0
    #取得輸入
    for event in pygame.event.get():     #取得正在操作的事件，並以列表方式存取
        if event.type == pygame.QUIT:    #如果點選X，跳出迴圈
            running = False
        elif event.type == pygame.KEYDOWN:   #按下鍵盤的這項指令
            if event.key == pygame.K_SPACE:   #確認是按下空白鍵
                player.shoot()                 #火箭的射擊


    #更新遊戲
    all_sprite.update() #執行這個群組的update函式 
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)  #sprite內建函式，偵測子彈碰到石頭並把子彈跟石頭一起銷毀
    for hit in hits:        #銷毀後，重新生成石頭
        random.choice(expl_sounds).play()
        score += hit.radius  #碰撞後，加分數(看石頭的半徑大小)
        expl = Explosion(hit.rect.center ,'lg')
        all_sprite.add(expl)
        if random.random() > 0.9:           #random.random()會回傳0~1隨機一個值
            pow = Power(hit.rect.center)    #傳入子彈跟石頭碰撞的中心點 
            all_sprite.add(pow)
            powers.add(pow)   
        new_rock()

    hits_player = pygame.sprite.spritecollide(player , rocks ,True ,pygame.sprite.collide_circle)  #機體撞到石頭的判斷範圍，True是決定撞到後石頭是否要刪掉
    for hit_rock in hits_player:
        player.health -= hit_rock.radius   #機體血量減掉石頭的半徑
        expl = Explosion(hit_rock.rect.center ,'sm')
        all_sprite.add(expl)
        new_rock()
        if player.health <= 0 :
            dead_expl = Explosion(player.rect.center , 'player')  #機體爆炸的效果
            all_sprite.add(dead_expl)
            dead_sound.play()   #爆炸音效
            player.lives -= 1   #生命次數減一
            player.health = 100   #血條回滿
            player.hide()        #復活的隱藏期
    
    hits_power = pygame.sprite.spritecollide(player , powers ,True)
    for hit_pow in hits_power:
        if hit_pow.type == 'shield':             #補血的
            shield_sound.play()
            player.health +=10
            if player.health > 100:
                player.health = 100
        if hit_pow.type == 'gun':              #雙倍子彈
            gun_sound.play()
            player.gunup()

    if player.lives == 0 and not(dead_expl.alive()):   #三條命用完，結束遊戲 ,alive為判斷die這個的判定是否存在
        show_init = True
     

    #畫面顯示
    screen.fill((Black))  #視窗畫面的調色盤
    screen.blit(background_img,(0,0))   #畫入視窗的圖片
    all_sprite.draw(screen)  #將all_sprite裡的角色畫入視窗裡
    draw_text(screen, str(score), 18, Width/2, 15)  #分數顯示在視窗
    draw_health(screen , player.health , 5 ,15)  #血條顯示在視窗
    draw_lives(screen , player.lives , player_mini_img ,Width/2+150, 15)
    pygame.display.update() #視窗的畫面更新

pygame.quit() #關閉視窗

