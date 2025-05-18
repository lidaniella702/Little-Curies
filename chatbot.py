from pygame import *
from pygame import time
from random import *
from pprint import *
from openai import OpenAI
import os
from api_key import OPENAI_API_KEY

font.init()
init()
client = OpenAI(api_key=OPENAI_API_KEY)

width,height=1000,700
screen_surface = display.set_mode((width, height))
RED = (255, 0, 0)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (228, 244, 243)
GREEN = (0, 255, 0)
DARKGREEN = (38, 72, 64)
BGGREEN = (146, 171, 167)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
myClock = time.Clock()
running = True
# IMAGES
marie = image.load("images/Little_Curies.jpg")
bigmarie = image.load("images/Big Curies.jpg")
search=image.load("images/search.png")
##marker = image.load("images/marker.png")
###marker1 = image.load("images/marker1.png")  
##highliter = image.load("images/highlighter.png")  
##stamp = image.load("images/stamp.png")  
##info   = image.load("images/info.png")  

# RECT
BGrect = Rect(0, 0, 1000, 700)
marieRect = Rect(250, 40, 500, 500)
bigmarieRect = Rect(225, 15, 550, 550)
Answerrect = Rect(150,100,700,500)
Eraserrect = Rect(150,620,700,30)
markerRect = Rect(50, 100, 100, 100)   
highlighterRect = Rect(150, 250, 100, 100)
stampRect = Rect(150, 400, 100, 100)
infoRect = Rect(600, 100, 100, 100)
Searchrect=Rect(150,50,700,30)
eraserButton=Rect(80,610,30,30)
zoomInRect=Rect(880,550,30,30)
zoomOutRect=Rect(880,600,30,30)

#TEXT
play_text=font.SysFont("Ariel",60)
# VARIABLES
screen_state = "intro"
#marker_hover = marker
output=""   

Type=False
p=False
pp=True
text=""
length = 150
erase=False
col=WHITE


#FUNCTIONS
def chat(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
def drawText(text,Font,size,color,x,y):
    myFont=font.SysFont(Font,size)
    text=myFont.render(text,True,color)
    screen_surface.blit(text,(x,y))
    return text
output=""

def drawBGGAME():

    draw.rect(screen_surface, DARKGREEN, BGrect)
    draw.rect(screen_surface,WHITE,Answerrect)
    draw.rect(screen_surface,WHITE,Eraserrect)
    draw.rect(screen_surface,WHITE,Searchrect)
    draw.rect(screen_surface,WHITE,eraserButton)
    draw.rect(screen_surface,BLACK,zoomInRect)
    screen_surface.blit(search,(150,50))
    drawText(output, "Times New Roman", 20, BLACK, 200, 150)


def eraser():
    global length
    global output
    draw.rect(screen_surface,WHITE,(150,100,length,500))
    draw.rect(screen_surface,BLACK,(length,620,30,30))
    output=""
    text=""
    screen_surface.blit(search, (150,50))

def drawBG():
    draw.rect(screen_surface, LIGHTBLUE, BGrect)
    screen_surface.blit(marie, (250, 40))

def zoomIn():
    drawText(output, "Times New Roman", 50, BLACK, 200, 150)

while running:
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()

    
    for evt in event.get():
        
        if evt.type == QUIT:
            running = False
        if evt.type == MOUSEBUTTONDOWN and evt.button == 1 and bigmarieRect.collidepoint(mx, my) and screen_state == "intro":
            screen_state = "game"
##        if markerRect.collidepoint(mx, my) and screen_state == "game":
##            marker_hover = marker1
        #else:
         #   marker_hover = marker
        if evt.type==KEYDOWN and Type:
            print("please")
            if evt.key==K_RETURN:
                print("sorry")
                pp=False
            elif evt.key==K_BACKSPACE:
                if len(text)>1:
                    text=text[0:-1]
                else:
                    text=""
            else:
                text+=evt.unicode
                p=True
            




   

    draw.rect(screen_surface, LIGHTBLUE, BGrect)
    if screen_state == "intro":
        screen_surface.blit(marie, (250, 40))
        play_text_surface = play_text.render("Press the Icon to Play", True, BLACK)
        if marieRect.collidepoint(mx, my):
            screen_surface.blit(bigmarie, (225, 15))

        # Animate the text moving left to right
        if not hasattr(drawBG, "text_x"):
            drawBG.text_x = 25  # initial x position
            drawBG.text_direction = 1  # 1 for right, -1 for left

        # Move text
        drawBG.text_x += 3 * drawBG.text_direction
        if drawBG.text_x > width - play_text_surface.get_width() - 25:
            drawBG.text_direction = -1
        elif drawBG.text_x < 25:
            drawBG.text_direction = 1

        screen_surface.blit(play_text_surface, (drawBG.text_x, 40))
    elif screen_state == "game":
        drawBGGAME()
        #screen_surface.blit(marker_hover, (25, 100)) 

    if p==True:
        drawText(text, "Times New Roman", 20, BLACK, 160, 50)

    if pp == False:
        drawText(output, "Times New Roman", 20, BLACK, 200, 150)
        if Type:
            output2=[]
            output3=[]
            output4=[]
            print("hi")
            output= chat(text + "say it like you're talking to a middle schooler")
            '''
                TAKE OUT OF THIS ONE
            '''
            
            output1 = output.split(" ")

            if len(output)%10 != 0:
                for i in range (len(output)//10):
                    output2.append(output1[0:10])
                    del output1[0:10]
            else:
                for i in range (len(output)//10):
                    if len(output1)>10:
                        output2.append(output1[0:10])
                        del output1[0:10]
                    else:
                        output2.append(output1)
            #print(output2)
            for j in range(len(output2)):
                line= " ".join(output2[j])
                output3.append(line)
            
            output3 = [m for m in output3 if m!=""]
            
            for k in range(len(output3)):
                print("nooo")
                #line=" ".join(output3[k])
                #output4.append(line)
##                print(output3[k])
##                print("kk")
##            print (output4)

            print(output3)
            pp=True

            
                
##            outputFile=open("output.txt","w")
##            for i in range (len(output)):
##                if output[i]=="":
##                    output1.append(output[0:i+1])
##                    output=output[i:]
##            #output1=output
##            for j in range (len(output1)//10+1):
##                
##                line=output1[0:10]
##                print(line)
##                output1=ouput[10:]
##                
##                outputFile.write(f"{output1[0:10]}\n")
##                output1=output1[10:]
##
##            outputFile.close()
##            outputFile=open("output.txt","r")
##            output2=outputFile.readlines()
##            print(output2)
##            outputFile.close()
            Type=False
                


    if eraserButton.collidepoint(mx,my) and mb[0]:
        erase=True

    if erase==True:
        eraser()
        length+=3
        if length >= 700:
            erase=False
    if Searchrect.collidepoint(mx,my) and mb[0]:
        Type=True

    if erase==False:
        length=150
        #col=BLACK
    if zoomInRect.collidepoint(mx,my):
        zoomIn()


    myClock.tick(60)
    display.flip()

quit()
