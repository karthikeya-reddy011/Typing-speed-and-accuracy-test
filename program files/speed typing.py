import pygame
from pygame.locals import *
import sys
import os
import time
import random
from essential_generators import DocumentGenerator

class Game:
   
    def __init__(self):
        self.w=1920
        self.h=1080
        self.reset=True
        self.active = False
        self.input_text=''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = 0
        self.results = 'Time:0 Accuracy:0 % Wpm:0 '
        self.results_1= 'adjusted wpm:0 errors:0'
        self.wpm = 0
        self.awpm = 0
        self.e = 0
        self.e1 = 0
        self.n=5
        self.end = False
        self.HEAD_C = (255,213,102)
        self.TEXT_C = (240,240,240)
        self.RESULT_C = (255,70,70)
        self.t = ''
        self.k = ''
        self.id=''
        self.passw=''
        self.rpassw=''
        self.stud=''
        self.fi=0
        pygame.init()
        self.open_img = pygame.image.load('type-speed-open.jpg')
        self.open_img = pygame.transform.scale(self.open_img, (self.w,self.h))

        self.bg2 = pygame.image.load('background3.jpg')
        self.bg2 = pygame.transform.scale(self.bg2, (1920,1080))
        
        self.bg = pygame.image.load('background.jpg')
        self.bg = pygame.transform.scale(self.bg, (1920,1080))

        self.back = pygame.image.load('back.png')
        self.back = pygame.transform.scale(self.back, (125,75))
        
        self.screen = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Type Speed test')
       
        
    def draw_text(self, screen, msg, y ,fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1,color)
        text_rect = text.get_rect(center=(self.w/2, y))
        screen.blit(text, text_rect)
        pygame.display.update()

    def draw_text1(self, screen, msg, x, y ,fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1,color)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)
        pygame.display.update()
        
    def get_sentence(self):
        f = open('sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence

    def calc(self, screen):
        if(not self.end):
            #Calculate time
            self.total_time += time.time() - self.time_start
               
            #Calculate accuracy
            '''count = 0
            for i,c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass'''
            
            #self.accuracy = count/len(self.word)*100
            
            self.error()      
            #Calculate words per minute
            self.wpm += len(self.input_text)*60/(5*self.total_time)

            self.accuracy += (len(self.word)-self.e)/len(self.word)*100
            if(len(self.input_text)==0):
               self.accuracy+=0
            self.end = True
            
            pygame.display.update()

    def show_results(self):
        self.total_time/=self.n
        self.wpm/=self.n
        self.accuracy/=self.n
        self.awpm=self.wpm-((self.e*60)/(self.total_time))
        
        self.results = 'Time:'+str(round(self.total_time)) +" secs   Accuracy:"+ str(round(self.accuracy)) + "%" + '   Wpm: ' + str(round(self.wpm))
        self.results_1= 'adjusted wpm: ' + str(round(self.awpm)) + '   errors:' + str(self.e1)

    def run(self):
        
        self.running=True
        self.reset=False
        self.end=False

        self.input_text=''
        msg = "Typing Speed Test"
        self.draw_text(self.screen, msg,80, 80,self.HEAD_C)
        self.screen.blit(self.back,(10,60))
        pygame.display.update()
        
        while(self.running):
            limit=0
            clock = pygame.time.Clock()
            self.screen.fill((0,0,0), (550,250,820,50))
            pygame.draw.rect(self.screen,self.HEAD_C, (550,250,820,50), 2)
            # update the text of user input
            self.draw_text(self.screen, self.input_text, 274, 26,(250,250,250))
            if(len(self.input_text)>70):
                limit=1
                pygame.display.update()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    pygame.display.quit()
                    pygame.quit()
                    quit()
                    #sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    # position of input box
                    if(x>=550 and x<=1370 and y>=250 and y<=300):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time() 
                     
                    if(x>=10 and x<=135 and y>=60 and y<=110):
                        self.start()

                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            self.calc(self.screen)
                            
                            self.end = True
                            self.running=False
                            break
                            
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                            limit=0
                        else:
                            if(limit!=1):
                                self.input_text += event.unicode
            
            pygame.display.update()
        clock.tick(60)

    def reset_game(self):
        self.screen.blit(self.open_img, (0,0))

        pygame.display.update()
        time.sleep(3)
        
        self.reset=False
        self.end = False
        self.active=False

        self.input_text=''
        self.word = ''
        
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))
        msg = "Typing Speed Test"
        self.draw_text(self.screen, msg,80, 80,self.HEAD_C)  
          
        pygame.draw.rect(self.screen,(255,192,25), (650,250,650,50), 2)  

        self.screen.blit(self.back,(10,60))
        pygame.display.update()


    def start(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg2,(0,0))
        self.draw_text(self.screen, "Create new test",125, 35,self.TEXT_C)
        self.draw_text(self.screen, "Start a random test",225, 35,self.TEXT_C)
        self.draw_text(self.screen, "Join with test ID",325, 35,self.TEXT_C)
        self.draw_text(self.screen, "View stats",425, 35,self.TEXT_C)
        self.draw_text(self.screen, "Create new student account",525, 35,self.TEXT_C)
        self.draw_text(self.screen, "Create new administrator",625, 35,self.TEXT_C)
        self.draw_text(self.screen, "Delete student account",725, 35,self.TEXT_C)
        self.draw_text(self.screen, "Exit",825, 35,self.TEXT_C)
        pygame.display.update()

        self.running=True
        while(self.running):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
    
                    if(x>=870 and x<=1060 and y>=100 and y<=150):    
                        self.create_test()

                    elif(x>=850 and x<=1080 and y>=200 and y<=250):
                        self.random()

                    elif(x>=870 and x<=1060 and y>=300 and y<=350):
                        self.join_id()

                    elif(x>=890 and x<=1040 and y>=400 and y<=450):
                        self.stats()

                    elif(x>=810 and x<=1120 and y>=500 and y<=550):
                        self.create_student()

                    elif(x>=820 and x<=1110 and y>=600 and y<=650):
                        self.create_admin()

                    elif(x>=820 and x<=1110 and y>=700 and y<=750):
                        self.delete_student()

                    elif(x>=900 and x<=990 and y>=800 and y<=850):
                        self.running = False
                        pygame.display.quit()
                        pygame.quit()
                        sys.exit()

    def delete_student(self):
        self.fi=0
        self.authorization()
        self.id=''
        self.passw=''
        
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))
        self.screen.blit(self.back,(10,60))
        self.draw_text1(self.screen, 'Enter student id to be deleted:',700, 250, 26,(250,250,250))
        self.displaying()
        
    
        try:
            with open('student.txt','r') as f1:
                lines = f1.readlines()
                
            with open('student.txt','w') as f1:
                for line in lines:
                    first=0
                    for word in line.split():
                        if(word==self.id and first==0):
                            first=-1
                            break
                        
                        first+=1
                    if(first!=-1):
                        f1.write(line)

                        first+=1
            with open('student.txt','r') as f1:
                lines = f1.readlines()
            with open('student.txt', 'w') as f1:
                for line in lines:
                    if line.strip("\n") != self.id:
                        f1.write(line)

            os.remove(self.id+'.txt')
            self.draw_text(self.screen,'Successfully removed',600, 28, self.RESULT_C)
            pygame.display.update()
            time.sleep(2)
            self.start()
        except FileNotFoundError:
            self.draw_text(self.screen,'User does not exist',600, 28, self.RESULT_C)
            pygame.display.update()
            time.sleep(2)
            self.start()
                        
    def create_test(self):
        self.fi=0
        self.authorization()
        self.id=''
        self.passw=''
 
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))
        self.screen.blit(self.back,(10,60))
        self.draw_text1(self.screen, 'Enter test id:',800, 250, 26,(250,250,250))
        pygame.display.update()
        self.displaying()
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))
        self.screen.blit(self.back,(10,60))
        f1=open(self.id+'.txt','a')
        self.draw_text1(self.screen, 'Enter length of the test:',800, 250, 26,(250,250,250))
        self.displaying()
        f1.write(self.id+'\n')
        try: 
            self.n=int(self.id)
        except ValueError:
            self.draw_text(self.screen,'Invalid! please enter a number',600, 28, self.RESULT_C)
            time.sleep(2)
            pygame.display.update()
            self.create_test()
        for i in range(self.n):
            self.screen.fill((0,0,0))
            self.screen.blit(self.bg,(0,0))
            self.screen.blit(self.back,(10,60))
            temp=str(i+1)
            if(i==0):
                self.draw_text(self.screen,'Enter '+temp+'st sentence:',200, 28, (250,250,250))
            elif(i==1):
                self.draw_text(self.screen,'Enter '+temp+'nd sentence:',200, 28, (250,250,250))
            elif(i==2):
                self.draw_text(self.screen,'Enter '+temp+'rd sentence:',200, 28, (250,250,250))
            else:
                self.draw_text(self.screen,'Enter '+temp+'th sentence:',200, 28, (250,250,250))

            self.displaying1()
            f1.write(self.id)
            f1.write('\n')
            
        self.draw_text(self.screen,'Test has been created successfully',800, 28, self.RESULT_C)
        time.sleep(2)
        f1.close()
        self.start()

    def displaying1(self):
        self.id=''
        self.running=True
        self.end=True
        while(self.running):
            limit=0
            self.screen.fill((0,0,0), (550,250,820,50))
            pygame.draw.rect(self.screen,(255,192,25), (550,250,820,50), 2) 
            self.draw_text(self.screen, self.id,274, 26,(250,250,250))
            if(len(self.id)>70):
                limit=1
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.running=False
                        self.end=False
                        
                    elif event.key == pygame.K_BACKSPACE:
                        limit=0
                        self.id = self.id[:-1]
                        
                    else:
                        if(limit!=1):
                            self.id += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if(x>=10 and x<=135 and y>=60 and y<=110):
                        self.start()
                        
                if self.end:
                    break
                
    def displaying(self):
        self.id=''
        self.running=True
        self.end=True
        while(self.running):
            limit=0
            self.screen.fill((0,0,0), (910,225,200,50))
            pygame.draw.rect(self.screen,self.HEAD_C, (910,225,200,50), 2)  
            self.draw_text1(self.screen, self.id,1010, 250, 26,(250,250,250))
            if(len(self.id)>16):
                limit=1
            pygame.display.update()
        
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.running=False
                        self.end=False
                        
                    elif event.key == pygame.K_BACKSPACE:
                        self.id = self.id[:-1]
                        limit=0
                        
                    else:
                        if(limit!=1):
                            self.id += event.unicode
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if(x>=10 and x<=135 and y>=60 and y<=110):
                        self.start()
                        
                if self.end:
                    break

    def random(self):        
        self.e1=0
        self.time_start = 0
        self.total_time = 0
        self.accuracy = 0
        self.wpm = 0
        self.awpm = 0
        self.e=0
        
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))
        self.screen.blit(self.back,(10,60))
        self.screen.fill((0,0,0), (910,250,100,50))
        self.n=5
        pygame.draw.rect(self.screen,(255,192,25), (910,250,100,50), 2)
        self.draw_text(self.screen, "Enter length of the test",200, 28,self.TEXT_C)
        self.running=True
        self.end=True
        while(self.running):
            self.screen.fill((0,0,0), (910,250,100,50))
            pygame.draw.rect(self.screen,self.HEAD_C, (910,250,100,50), 2)
            self.draw_text(self.screen, self.t, 274, 26,(250,250,250))
            pygame.display.update()

            for event in pygame.event.get(): 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.running=False
                        self.end=False
                            
                    elif event.key == pygame.K_BACKSPACE:
                        self.t = self.t[:-1]
                        
                    else:
                        self.t += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if(x>=10 and x<=135 and y>=60 and y<=110):
                        self.start()

                if self.end:
                    break

            pygame.display.update()
            
        try: 
            self.n=int(self.t)
        except ValueError:
            self.draw_text(self.screen,'Invalid! please enter a number',600, 28, self.RESULT_C)
            time.sleep(2)
            pygame.display.update()
            self.random()
        for i in range(self.n):
            self.reset_game()
            gen = DocumentGenerator()
            self.word = gen.sentence()
            if(len(self.word)>70):
                self.word=self.word[0:70]
            self.draw_text(self.screen, self.word,200, 28,self.TEXT_C)
            self.run()

        self.show_results()
        self.draw_text(self.screen, self.results,450, 28, self.RESULT_C)
        self.draw_text(self.screen, self.results_1,500, 28, self.RESULT_C)

        self.running=True
        while(self.running):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()

                    if(x>=10 and x<=135 and y>=60 and y<=110):
                        self.start()
            
    def join_id(self):
        self.fi=1
        self.authorization()
        f2=open(self.id+'.txt','a')
        self.id=''
        self.passw=''
        self.screen.blit(self.back,(10,60))
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))
        self.screen.blit(self.back,(10,60))
        self.draw_text1(self.screen, 'Enter test id:',800, 250, 26,(250,250,250))
        pygame.display.update()
        self.displaying()
        self.e1=0
        self.time_start = 0
        self.total_time = 0
        self.accuracy = 0
        self.wpm = 0
        self.awpm = 0
        self.e=0
        cc=0
        try:
            f1=open(self.id+'.txt')
            for line in f1:
                if(cc==0):
                    cc+=1
                    self.n=int(line)
                else:
                    self.screen.fill((0,0,0))
                    self.screen.blit(self.bg,(0,0))
                    self.screen.blit(self.back,(10,60))

                    line = line[:-1]
                    self.word=line
                    self.draw_text(self.screen,line,200, 28, (250,250,250))
                    self.reset=False
                    self.end = False
                    self.active=False
                    self.run()
            
            self.show_results()
            self.draw_text(self.screen, self.results,450, 28, self.RESULT_C)
            self.draw_text(self.screen, self.results_1,500, 28, self.RESULT_C)
            f2.write(self.results+'\n')
            f2.write(self.results_1+'\n')
            pygame.display.update()
            f1.close()
            f2.close()
            self.running=True
            while(self.running):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x,y = pygame.mouse.get_pos()

                        if(x>=10 and x<=135 and y>=60 and y<=110):
                            self.start()
            
                    
        except FileNotFoundError:
            self.draw_text(self.screen,'Invalid test id',600, 28, self.RESULT_C)
            pygame.display.update()
            time.sleep(2)
            self.start()

        self.start()

    def stats(self):
        self.fi=1
        self.authorization()
        f1=open(self.id+'.txt','r')
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))
        self.screen.blit(self.back,(10,60))
        
        c=150
        i=0
        d=1
        p=1
        f1.seek(0)
        for line in f1:
            line = line[:-1]
            if(i%2==0):
                c+=50
                temp=str(d)
                if(p>5):
                    self.draw_text(self.screen,'Press enter to continue',1000, 28, self.RESULT_C)
                    self.running=True
                    while(self.running):
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                x,y = pygame.mouse.get_pos()
                                if(x>=10 and x<=135 and y>=60 and y<=110):
                                    self.start()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                    self.running=False
                                    break
                            
                    self.screen.fill((0,0,0))
                    self.screen.blit(self.bg,(0,0))
                    self.screen.blit(self.back,(10,60))
                    c=200
                    p=1
                    
                if(d==1):
                    self.draw_text(self.screen,temp+'st test',c-50, 28, self.RESULT_C)
                elif(d==2):
                    self.draw_text(self.screen,temp+'nd test',c-50, 28, self.RESULT_C)
                elif(d==3):
                    self.draw_text(self.screen,temp+'rd test',c-50, 28, self.RESULT_C)
                else:
                    self.draw_text(self.screen,temp+'th test',c-50, 28, self.RESULT_C)
                d+=1
                p+=1

            
            self.draw_text(self.screen,line,c, 28, (250,250,250))
            c+=50
            i+=1
            
            pygame.display.update()
        pygame.display.update()
        self.running=True
        while(self.running):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if(x>=10 and x<=135 and y>=60 and y<=110):
                        self.start()
        f1.close()


    def login(self):
        self.screen.blit(self.back,(10,60))
        
        self.running=True
        self.end=True
        while(self.running):
            limit=0
            self.screen.fill((0,0,0), (910,225,200,50))
            self.screen.fill((0,0,0), (910,325,200,50))
            pygame.draw.rect(self.screen,self.HEAD_C, (910,225,200,50), 2)
            pygame.draw.rect(self.screen,self.HEAD_C, (910,325,200,50), 2)
            self.draw_text1(self.screen, self.id,1010, 250, 26,(250,250,250))
            pygame.display.update()
            if(len(self.id)>16):
                limit=1
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.running=False
                        self.end=False
                        
                    elif event.key == pygame.K_BACKSPACE:
                        self.id = self.id[:-1]
                        limit=1
                        
                    else:
                        if(limit!=1):
                            self.id += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if(x>=10 and x<=135 and y>=60 and y<=110):
                        self.start()
                        
                if self.end:
                    break

        self.running=True
        self.end=True
        self.k=''
        while(self.running):
            limit=0
            self.screen.fill((0,0,0), (910,325,200,50))
            pygame.draw.rect(self.screen,self.HEAD_C, (910,325,200,50), 2)
            self.draw_text1(self.screen,self.k,1010,350, 26,(250,250,250))
            if(len(self.k)>20):
                limit=1
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.running=False
                        self.end=False
                        
                    elif event.key == pygame.K_BACKSPACE:
                        self.passw = self.passw[:-1]
                        self.k = self.k[:-1]
                        limit=0
                    else:
                        if(limit!=1):
                            self.passw += event.unicode
                            self.k += '*'
                if self.end:
                    break

        pygame.display.update()

    def authorization(self):
        self.screen.blit(self.back,(10,60))
        
        self.running=True
        self.end=True
        self.id=''
        self.passw=''
        self.k=''
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))
        if(self.fi==0):
            self.draw_text(self.screen,'Admin authorization required',80, 80,self.HEAD_C)
        else:
            self.draw_text(self.screen,'Student login',80, 80,self.HEAD_C)
            
        self.draw_text1(self.screen, "Enter id:",800,250, 28,self.TEXT_C)
        self.draw_text1(self.screen, "Enter password:",800,350, 28,self.TEXT_C)
        pygame.draw.rect(self.screen,self.HEAD_C, (910,225,200,50), 2)
        pygame.draw.rect(self.screen,self.HEAD_C, (910,325,200,50), 2)
        self.login()
        
        f=0
        if(self.fi==1):
            tf='student.txt'
        else:
            tf='admin.txt'
        with open(tf,'r') as file:
            for line in file:
                f=0
                for word in line.split():
                    if(f==1):
                        if(word==self.passw):
                            self.draw_text(self.screen,'Authorization successfull!',600, 28, self.RESULT_C)
                            pygame.display.update()
                            time.sleep(2)
                            f=2
                            break
                        
                    if(word==self.id):
                        self.stud=word
                        f=1
                    else:
                        break
                    
                if(f==2):
                    break

        if(f!=2):
            self.draw_text(self.screen,'Invalid Details',600, 28, self.RESULT_C)
            pygame.display.update()
            time.sleep(2)
            self.start()
        pygame.display.update()

    def create_student(self):
        self.fi=0
        self.authorization()
        self.id=''
        self.passw=''
        self.rpassw=''
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))
        
        self.screen.fill((0,0,0), (910,250,100,50))
        f1=open('student.txt','a')
        self.draw_text(self.screen,'Student Details',80, 80,self.HEAD_C)
        self.draw_text1(self.screen, "Enter id:",800,250, 28,self.TEXT_C)
        self.draw_text1(self.screen, "Enter password:",800,350, 28,self.TEXT_C)
        self.draw_text1(self.screen, "Re-Enter password:",800,450, 28,self.TEXT_C)
        pygame.draw.rect(self.screen,self.HEAD_C, (910,425,200,50), 2)
        self.login()
        self.running=True
        self.end=True
        self.k = ''
    
        while(self.running):
            limit=0
            self.screen.fill((0,0,0), (910,425,200,50))
            pygame.draw.rect(self.screen,self.HEAD_C, (910,425,200,50), 2)
            self.draw_text1(self.screen, self.k, 1010,450, 26,(250,250,250))
            if(len(self.k)>20):
                limit=1
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.running=False
                        self.end=False
                        
                    elif event.key == pygame.K_BACKSPACE:
                        self.rpassw = self.rpassw[:-1]
                        self.k = self.k[:-1]
                        limit=0
                    else:
                        if(limit!=1):
                            self.rpassw += event.unicode
                            self.k += '*'
                        

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if(x>=10 and x<=135 and y>=60 and y<=110):
                        self.start()
                        
                if self.end:
                    break

        if(self.rpassw != self.passw):
            self.draw_text(self.screen,'Given password and re-entered password must match!',600, 28, self.RESULT_C)
            time.sleep(2)
            self.create_student()
        self.draw_text(self.screen,'data added successfully',600, 28, self.RESULT_C)
        f1.write(self.id+' '+self.passw)
        f1.write('\n')
        f1.close()
        f1=open(self.id+'.txt','a')
        f1.close()
        time.sleep(2)
        self.start()

    def create_admin(self):
        self.fi=0
        self.authorization()
        self.id=''
        self.passw=''
        self.rpassw=''
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))
        
        self.screen.fill((0,0,0), (910,250,100,50))

        f1=open('admin.txt','a')
        f1.write('\n')
        self.draw_text(self.screen,'Administrator Details',80, 80,self.HEAD_C)
        self.draw_text1(self.screen, "Enter id:",800,250, 28,self.TEXT_C)
        self.draw_text1(self.screen, "Enter password:",800,350, 28,self.TEXT_C)
        self.draw_text1(self.screen, "Re-Enter password:",800,450, 28,self.TEXT_C)
        pygame.draw.rect(self.screen,self.HEAD_C, (910,425,200,50), 2)
        self.login()
        
        self.running=True
        self.end=True
        self.k = ''
        
        while(self.running):
            limit=0
            self.screen.fill((0,0,0), (910,425,200,50))
            pygame.draw.rect(self.screen,self.HEAD_C, (910,425,200,50), 2)
            self.draw_text1(self.screen, self.k, 1010,450, 26,(250,250,250))
            if(len(self.k)>20):
                limit=1
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.running=False
                        self.end=False
                        
                    elif event.key == pygame.K_BACKSPACE:
                        self.rpassw = self.rpassw[:-1]
                        self.k = self.k[:-1]
                        limit=0
                    else:
                        if(limit!=1):
                            self.rpassw += event.unicode
                            self.k += '*'

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if(x>=10 and x<=135 and y>=60 and y<=110):
                        self.start()
                        
                if self.end:
                    break

        if(self.rpassw != self.passw):
            self.draw_text(self.screen,'Given password and re-entered password must match!',600, 28, self.RESULT_C)
            time.sleep(2)
            self.create_student()
        self.draw_text(self.screen,'data added successfully',600, 28, self.RESULT_C)
        f1.write(self.id+' '+self.passw)
        f1.close()
        time.sleep(2)
        self.start()
        f1.close()

    def error(self):
        j,f,a=660,0,0
        self.e=0
        for i in range(len(self.input_text)):
            j+=10

            if(i>=len(self.word)):
                f=1
                a=i
                break
            if(self.input_text[i]!=self.word[i]):
                self.draw_text1(self.screen, self.input_text[i], j, 350, 25, self.RESULT_C)
                self.e+=1
            else:
                self.draw_text1(self.screen, self.input_text[i], j, 350, 25, self.TEXT_C)

        if(i<len(self.word)-1):
            self.e+=len(self.word)-1-i

        if(f==1):
            for i in range(a,len(self.input_text)):
                j+=10
                self.e+=1
                self.draw_text1(self.screen, self.input_text[i], j, 350, 25, self.RESULT_C)

        self.e1+=self.e
        pygame.display.update()
        time.sleep(2)
Game().start()
