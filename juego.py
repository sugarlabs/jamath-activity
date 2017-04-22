import pygame, random, os
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((1200,900))
pygame.display.set_caption("PyMath")
clock = pygame.time.Clock()

fuente = pygame.font.Font("./data/fuente.ttf",60)
fuente2 = pygame.font.Font("./data/fuente.ttf",130)

class number(pygame.sprite.Sprite):
    
    def __init__(self,x,y,image,answer=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = Rect((x,y),(self.image.get_width(),self.image.get_height()))
        self.answer = answer

    def update(self,time,vel,level):
        incremento_nivel = {"facil":1,"medio":2,"dificil":3}
        self.rect.move_ip(0,time*vel*incremento_nivel[level])

class expresion:
    
    def __init__(self,level):

        incremento_nivel = {"facil":9,"medio":20,"dificil":50}
        operacion = {1:"+",2:"-",3:"*",4:"/"}
        simbolo = {1:"+",2:"-",3:"X",4:":"}
        operador = random.randint(2,3)
        self.primero = str(random.randint(0,incremento_nivel[level]))
        self.segundo = str(random.randint(0,incremento_nivel[level]))
        self.expresion = fuente.render(self.primero + simbolo[operador] + self.segundo + " = ? ",True,(255,0,0))
        self.resultado = str(eval(self.primero+operacion[operador]+self.segundo))
        self.vida = 0
                                           
        self.preguntas = pygame.sprite.Group()
        self.preguntas.add(number(random.randint(100,640),random.randint(-50,-10),fuente.render(self.resultado,True,(random.randint(0,255),random.randint(0,255),random.randint(0,255))),True))
        for i in range(random.randint(5,10)):
            if random.randint(0,1) == 0:
                wrong = str(int(self.resultado) - random.randint(1,10))
            else:
                wrong = str(int(self.resultado) + random.randint(1,10))
            image_wrong = fuente.render(wrong,True,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            self.preguntas.add(number(random.randint(300,1000),random.randint(-0,-0),image_wrong,False))  
    
def cargar_imagen(nombre,trasnparent=False):
     try: imagen = pygame.image.load(nombre)
     except pygame.error, message:
          raise SystemExit, message
     imagen = imagen.convert()
     return imagen

fondo = cargar_imagen('data/1.jpg')
screen.blit(fondo, (0, 0))

pygame.display.flip()

def main(screen,clock):
    sonido_menu = load_sound("./data/menu.ogg")
    jugar = fuente2.render("JUGAR",True,(0,0,255))
    level = fuente2.render("NIVEL",True,(0,0,255))
    quit = fuente2.render("SALIR",True,(0,0,255))
    fondo = cargar_imagen('data/1.jpg')
    chosen_level = "facil"

    while 1:
        screen.fill((0,0,0))
	screen.blit(fondo, (0, 0))
        screen.blit(jugar,(450,100))
        screen.blit(level,(450,200))
        screen.blit(quit,(450,300))
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == MOUSEMOTION:
                if event.pos[0] > 550 and event.pos[0] < 450 + jugar.get_width() and event.pos[1] > 100 and event.pos[1] < 100 + jugar.get_height():
                     jugar = fuente2.render("JUGAR",True,(0,0,255))
                     if sonido_menu != None: 
                         sonido_menu.play()
                elif event.pos[0] > 550 and event.pos[0] < 450 + level.get_width() and event.pos[1] > 200 and event.pos[1] < 200 + level.get_height():
                     level = fuente2.render("NIVEL",True,(0,0,255))   
                     if sonido_menu != None: 
                         sonido_menu.play()
                elif event.pos[0] > 550 and event.pos[0] < 450 + quit.get_width() and event.pos[1] > 300 and event.pos[1] < 300 + quit.get_height():
                     quit = fuente2.render("SALIR",True,(0,0,255)) 
                     if sonido_menu != None: 
                         sonido_menu.play()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if event.pos[0] > 450 and event.pos[0] < 450 + jugar.get_width() and event.pos[1] > 100 and event.pos[1] < 100 + jugar.get_height():
                        return chosen_level
                    elif event.pos[0] > 450 and event.pos[0] < 450 + level.get_width() and event.pos[1] > 200 and event.pos[1] < 200 + level.get_height():
                        chosen_level = choose_level(screen)
                    elif event.pos[0] > 450 and event.pos[0] < 450 + quit.get_width() and event.pos[1] > 300 and event.pos[1] < 300 + quit.get_height():
                        exit()   
        pygame.display.update()




def choose_level(screen):
    pygame.font.Font("./data/fuente.ttf",130)
    sonido_menu = load_sound("./data/menu.ogg")
    facil = fuente2.render("facil",True,(0,0,255))
    medio = fuente2.render("medio",True,(0,0,255))
    dificil = fuente2.render("dificil",True,(0,0,255))
    fondo = cargar_imagen('data/1.jpg')
    level = "facil"
    while 1:
        screen.fill((0,0,0))
	screen.blit(fondo, (0, 0))
        screen.blit(facil,(450,100))
        screen.blit(medio,(450,200))
        screen.blit(dificil,(450,300))
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == MOUSEMOTION:
                if event.pos[0] > 450 and event.pos[0] < 450 + facil.get_width() and event.pos[1] > 100 and event.pos[1] < 100 + facil.get_height():
                     facil = fuente2.render("facil",True,(0,0,255)) 
                     if sonido_menu != None: 
                         sonido_menu.play()
                elif event.pos[0] > 450 and event.pos[0] < 450 + medio.get_width() and event.pos[1] > 200 and event.pos[1] < 200 + medio.get_height():
                     medio = fuente2.render("medio",True,(0,0,255))  
                     if sonido_menu != None: 
                         sonido_menu.play() 
                elif event.pos[0] > 450 and event.pos[0] < 450 + dificil.get_width() and event.pos[1] > 300 and event.pos[1] < 300 + dificil.get_height():
                     dificil =fuente2.render("dificil",True,(0,0,255)) 
                     if sonido_menu != None: 
                         sonido_menu.play()
                else:
                     facil = fuente2.render("facil",True,(0,0,255))
                     medio = fuente2.render("medio",True,(0,0,255))
                     dificil = fuente2.render("dificil",True,(0,0,255))
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if event.pos[0] > 450 and event.pos[0] < 450 + facil.get_width() and event.pos[1] > 100 and event.pos[1] < 100 + facil.get_height():
                        pass
                        return level
                    elif event.pos[0] > 450 and event.pos[0] < 450 + medio.get_width() and event.pos[1] > 200 and event.pos[1] < 200 + medio.get_height():
                        level = "medio"
                        return level
                    elif event.pos[0] > 450 and event.pos[0] < 450 + dificil.get_width() and event.pos[1] > 300 and event.pos[1] < 300 + dificil.get_height():
                        level = "dificil"
                        return level   
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    level = "facil"
                    return level
        pygame.display.update()
 

def play(screen,level,clock):
    die_point = {"facil":200,"medio":100,"dificil":60}
    fuente2 = pygame.font.Font("data/fuente.ttf",32)

    another_quest = True

    right_sound = load_sound("./data/right.ogg")
    wrong_sound = load_sound("./data/wrong.ogg")
    fondo = [load_image(str(i)+".jpg") for i in range(1,7)]
    numero_fondos = random.randint(0,2)
    score = 0
    puntuacionalta = load_puntuacionalta()

    while True: 
        time = clock.tick(30) / 1000.
        if another_quest:
            nueva_expresion = expresion(level)
            another_quest = False

        nueva_expresion.vida +=1
        if nueva_expresion.vida > die_point[level]:
            if wrong_sound != None:
                wrong_sound.play()
            another_quest = True
	    score -= 7

        nueva_expresion.preguntas.update(time,random.randint(80,155),level)

        screen.fill((0,0,0))   
        screen.blit(fondo[numero_fondos],(0,0)) 
        screen.blit(fuente2.render("Puntaje: " + str(score),True,(0,0,0)),(410,0))
        screen.blit(fuente2.render("Puntaje Mas Alto: " + str(puntuacionalta),True,(0,0,0)),(600,0))
        screen.blit(nueva_expresion.expresion,(600,800))
        nueva_expresion.preguntas.draw(screen) 

        for event in pygame.event.get():
            if event.type == QUIT:
                save_puntuacionalta(score)
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in nueva_expresion.preguntas.sprites():
                        if event.pos[0] > i.rect.x and event.pos[0] < i.rect.x + i.image.get_width() and event.pos[1] > i.rect.y and event.pos[1] < i.rect.y + i.image.get_height():
                            if i.answer: 
                                if right_sound != None:
                                    right_sound.play()
                                another_quest = True
                                score += 7
                            else:
                                if right_sound != None: 
                                    wrong_sound.play()
                                another_quest = True
                                score -= 3
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return 0
        pygame.display.update()

# Funcion para cargar imagenes
def load_image(name):
    path = os.path.join('data',name)
    return pygame.image.load(path).convert_alpha()

# Funcion para cargar Sonidos
def load_sound(name):
    path = os.path.join('data',name)
    try:
        sound = pygame.mixer.Sound(path)
        return sound
    except:
        print 'Warning, unable to load: ',path

# Funcion para guardar puntuaciones altas
def save_puntuacionalta(score):
    if os.path.exists("PuntajeAlto"):
        File = open("PuntajeAlto","r")
	puntuacionaltas = File.readlines()
	if int(puntuacionaltas[0]) > score: 
	    File.close()
	else:
	    File.close()
	    File = open("PuntajeAlto","w")
	    File.write(str(score))
    else:
	File = open("PuntajeAlto","w")
	File.write(str(score))
    	File.close()

def load_puntuacionalta():
    if os.path.exists("PuntajeAlto"):
        try:
            File = open("PuntajeAlto","r")
            puntuacionalta = int(File.readlines()[0])
            File.close()
            return puntuacionalta
        except:
            return 0
    else: 
        return 0

while 1:
    level = main(screen,clock)
    play(screen,level,clock)


