import pygame
from random import randrange, randint
 
PUNAINEN   = (255, 0, 0)
VIHREA = (70,166,147)
VIOLETTI = (111, 44, 145)

class Pelaaja(pygame.sprite.Sprite): #pelaaja eli robotti
    def __init__(self, leveys, korkeus):
        self.leveys = leveys
        self.korkeus = korkeus
        self.image = pygame.image.load("robo.png") #50x86
        self.rleveys = self.image.get_width()
        self.x = 50
        self.y = 320
        self.rect = self.image.get_rect()
        self.pseudo_rect = self.rect.inflate(-20,-30)
        self.pseudo_rect.x = self.x
        self.pseudo_rect.y = self.y

    def liiku(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT] and self.x > 0:
            self.x -= 5
        if pressed_keys[pygame.K_RIGHT] and self.x < (640 - self.rleveys):
            self.x += 5

        self.pseudo_rect.x = self.x
        self.pseudo_rect.y = self.y

    def piirra(self, naytto):
        naytto.blit(self.image, (self.x, self.y))
                    

class Vihollinen(pygame.sprite.Sprite): # luo vihollisen eli mörön ja sen random-liikkeen
    def __init__(self, leveys, korkeus):
        self.leveys = leveys
        self.korkeus = korkeus
        self.image = pygame.image.load("hirvio.png") #50x70
        self.x = 640 - self.image.get_width()
        self.y = randrange(self.korkeus-self.image.get_height())-self.korkeus #arvotaan alkuarvo y
        self.modex = "RIGHT"
        self.modey = "DOWN"
        self.rect = self.image.get_rect()
        self.pseudo_rect = self.rect.inflate(-20,-30)
        self.pseudo_rect.x = self.x
        self.pseudo_rect.y = self.y

    def piirra(self, naytto):
        naytto.blit(self.image, (self.x,self.y))
    

    def liiku(self, rahaa):
        if rahaa <= 5:
            nopeusx = 2
            nopeusy = 1
        if 5 < rahaa <= 10:
            nopeusx = 3
            nopeusy = 2
        if 10 < rahaa <= 15:
            nopeusx = 4
            nopeusy = 3
        if 15 < rahaa:
            nopeusx = 5
            nopeusy = 4
       
       #vasen-oikea
        if self.x + self.image.get_width() >= 740:
            self.modex ="LEFT"
        if self.x <= -100:
            self.modex ="RIGHT"

        if self.modex =="RIGHT":
            self.x += nopeusx

        if self.modex =="LEFT":
            self.x -= nopeusx

        #alas-ylös
        if self.y + self.image.get_height() >= 550:
            self.modey = "UP"
        if self.y <= -100:
            self.modey = "DOWN"
        
        if self.modey == "DOWN":
            self.y += nopeusy

        if self.modey == "UP":
            self.y -= nopeusy

        self.pseudo_rect.x = self.x
        self.pseudo_rect.y = self.y

class Raha(pygame.sprite.Sprite):
    def __init__(self, leveys, korkeus):
        self.leveys = leveys
        self.korkeus = korkeus
        self.image = pygame.image.load("kolikko.png") #40x40
        self.rect = self.image.get_rect()
        self.ohi = 0
        self.alusta()

    def alusta(self):
        self.x = randrange(self.leveys-self.image.get_width()) #arvotaan alkuarvo x
        self.y = randrange(self.korkeus-self.image.get_height())-self.korkeus #arvotaan alkuarvo y
        self.rect.x = self.x
        self.rect.y = self.y

    def liiku(self, rahaa):
        if rahaa <= 3:
            self.y += 2
        if 3 < rahaa <= 6:
            self.y += 3
        if 6 < rahaa <= 9:
            self.y += 4
        if 9 < rahaa <= 12:
            self.y += 5
        if 12 < rahaa:
            self.y += 6
        self.rect.y = self.y
        if self.y > self.korkeus:
            self.ohi += 1
            self.alusta()
    
    def piirra(self, naytto):
        naytto.blit(self.image, (self.x,self.y))

class RahaSade:
    def __init__(self):        
        pygame.init()
        pygame.display.set_caption("Rahasade")
        self.mode = 0
        self.rahaa = 0
        self.FPS = 60
        self.FramePerSec = pygame.time.Clock()
        self.leveys = 640 
        self.korkeus = 480 
        self.naytto = pygame.display.set_mode((self.leveys , self.korkeus))
        self.naytto.fill(VIHREA)
        self.P1 = Pelaaja(self.leveys, self.korkeus)
        self.E1 = Vihollinen(self.leveys, self.korkeus)
        self.R1 = Raha(self.leveys, self.korkeus)
        self.silmukka()

    def info(self):
        self.ruutu = pygame.draw.rect(self.naytto, VIOLETTI, (140,100,380,240))
        self.fontti = pygame.font.SysFont("Arial", 24)
        self.teksti = self.fontti.render("Liiku rahan alle", True , (VIHREA))
        self.naytto.blit(self.teksti, (220,140))
        self.teksti = self.fontti.render("Varo mörköä ", True , (VIHREA))
        self.naytto.blit(self.teksti, (220,160))
        self.teksti = self.fontti.render("Paina S = aloita peli", True, (VIHREA))
        self.naytto.blit(self.teksti, (220, 200))
        self.teksti = self.fontti.render("Esc = sulje peli", True, (VIHREA))
        self.naytto.blit(self.teksti, (220, 220))
        self.image = pygame.image.load("robo.png") #50x86
        self.naytto.blit(self.image, (150, 150))        

    def tapahtumat(self):
        for event in pygame.event.get():              
            if event.type == pygame.QUIT:
                exit()

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_s]: #aloittaa pelin
            self.mode = 1
        if pressed_keys[pygame.K_F2]: #aloittaa uuden pelin
            self.uusi_peli()
        if pressed_keys[pygame.K_ESCAPE]: #sulkee pelin
            exit()  
        
    def uusi_peli(self):
        self.rahaa = 0
        self.naytto.fill(VIHREA)
        self.P1 = Pelaaja(self.leveys, self.korkeus)
        self.E1 = Vihollinen(self.leveys, self.korkeus)
        self.R1 = Raha(self.leveys, self.korkeus)

    def keraa(self): # raha osuu roboon
        collide = pygame.Rect.colliderect(self.P1.pseudo_rect, self.R1.rect)
        if collide == True:
            self.R1.alusta()
            self.rahaa += 1      
        return self.rahaa

    def kuole(self): # mörkö osuu roboon tai rahaa ohi yli rajan
        collide = pygame.Rect.colliderect(self.P1.pseudo_rect, self.E1.pseudo_rect)
        if collide == True:
            mode = 0
            return True
        if  self.R1.ohi >= 5:
            mode = 0
            return True
        return False

    def silmukka(self):
        while True:     
            self.tapahtumat()
            if self.mode == 0:
                self.info()
            else:        
                if self.kuole() == True:
                    self.fontti = pygame.font.SysFont("Arial", 24)
                    self.teksti = self.fontti.render("*Game Over*", True, (255,0,0))
                    self.naytto.blit(self.teksti, (200,200))
                    if self.rahaa == 1:
                        self.teksti = self.fontti.render("Keräsit "+str(self.keraa())+ " rahan", True, (VIOLETTI))
                        self.naytto.blit(self.teksti, (200,240))
                    if self.rahaa != 1:
                        self.teksti = self.fontti.render("Keräsit "+str(self.keraa())+ " rahaa", True, (VIOLETTI))
                        self.naytto.blit(self.teksti, (200,240))

                else:
                    self.P1.liiku()
                    self.E1.liiku(self.rahaa)
                    self.R1.liiku(self.rahaa) 
                    self.naytto.fill(VIHREA)
                    self.fontti = pygame.font.SysFont("Arial", 24)
                    self.teksti = self.fontti.render("Rahat: " + str(self.keraa()), True , (VIOLETTI))
                    self.naytto.blit(self.teksti, (50,440))
                    self.teksti = self.fontti.render("Sallitut hudit: " + "*"* (5-int(self.R1.ohi)), True , (VIOLETTI))
                    self.naytto.blit(self.teksti, (150,440))
                    self.teksti = self.fontti.render("F2 = uusi peli", True, (VIOLETTI))
                    self.naytto.blit(self.teksti, (350, 440))
                    self.teksti = self.fontti.render("Esc = sulje peli", True, (VIOLETTI))
                    self.naytto.blit(self.teksti, (480, 440))
                    self.P1.piirra(self.naytto)
                    self.E1.piirra(self.naytto)
                    self.R1.piirra(self.naytto)
                    
            pygame.display.update()
            self.FramePerSec.tick(self.FPS)

if __name__ == "__main__":
    RahaSade()
