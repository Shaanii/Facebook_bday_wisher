import cv2
import cv2.cv as cv
import numpy
import os,sys
from facedetect import detect_and_draw

imagesFolder=r'/home/shivani/Desktop/Pictures'
images={}
imageCount=0
for image in os.listdir(imagesFolder):
    imagePath=os.path.join(imagesFolder,image)
    images[imageCount]=cv2.imread(imagePath)
    imageCount=imageCount+1


fps=10

file=open('theme.txt','r')
theme=file.readline()
if(theme=='1\n'):
    back=cv2.imread('background.jpg')
    back1=cv2.imread('background1.jpg')
    back2=cv2.imread('background2.jpg')
elif(theme=='2\n'):
    back=cv2.imread('flower1.jpg')
    back1=cv2.imread('flower2.jpg')
    back2=cv2.imread('flower3.jpg')
else:
    back=cv2.imread('heart1.jpg')
    back1=cv2.imread('heart2.jpg')
    back2=cv2.imread('heart3.jpg')
    


vheight, vwidth, vlayers=back.shape

for i in range(0,imageCount):
    print images[i].shape[0]

    

cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')


video =  cv2.VideoWriter('video1.avi',cv.CV_FOURCC('F', 'L', 'V', '1'),fps,(vwidth,vheight))
if not video:
    print "Error in creating video writer"


for i in range(0,imageCount):  
        newHeight=images[i].shape[0]
        newWidth=images[i].shape[1]
        hdiff=vheight-newHeight
        wdiff=vwidth-newWidth

        if(hdiff>0 and wdiff>0 and hdiff>wdiff):
            newWidth=vwidth
            ratio=float(float(vwidth)/images[i].shape[1])
            newHeight=int(images[i].shape[0]*ratio)
        elif(hdiff>0 and wdiff>0):
            newHeight=vheight
            ratio=float(float(vheight)/images[i].shape[0])
            newWidth=int(images[i].shape[1]*ratio)     
        if(newWidth>vwidth):
            newWidth=vwidth
            ratio=float(float(vwidth)/images[i].shape[1])
            newHeight=int(images[i].shape[0]*ratio)
        if(newHeight>vheight):
            newHeight=vheight
            ratio=float(float(vheight)/images[i].shape[0])
            newWidth=int(images[i].shape[1]*ratio)     
        images[i] = cv2.resize(images[i], (newWidth, newHeight), interpolation=cv2.INTER_AREA)



chance=0
counter=0
for i in range(0,imageCount):
    if(i==7):
        continue
    for j in range(0,fps*6):       
        if(chance==0 and counter<4):
            base=back.copy()
            counter=counter+1
        elif(chance==0 and counter==4):
            counter=0
            base=back1.copy()
            chance=1
        elif(chance==1 and counter<4):
            base=back1.copy()
            counter=counter+1
        elif(chance==1 and counter==4):
            counter=0
            base=back2.copy()
            chance=2
        elif(chance==2 and counter<4):
            base=back2.copy()
            counter=counter+1
        elif(chance==2 and counter==4):
            counter=0
            base=back.copy()
            chance=0

              
        currentImage=images[i].copy()    
        newHeight=currentImage.shape[0]
        newWidth=currentImage.shape[1]

        x_offset=int((back.shape[1]-newWidth)/2)
        y_offset=int((back.shape[0]-newHeight)/2)

        if(i==0):
            cv2.putText(currentImage,'Today', (vwidth/5,(int)(vheight/1.5)),cv2.FONT_HERSHEY_TRIPLEX,7,(128,128,128),7)
        if(i==1):
            cv2.putText(currentImage,'Its a Special', (30,(int)(vheight/1.5)),cv2.FONT_HERSHEY_TRIPLEX,3,(128,128,128),6)
            cv2.putText(currentImage,'Day', (vwidth/3,(int)(vheight/1.5+120)),cv2.FONT_HERSHEY_TRIPLEX,3,(128,128,128),6)
            
        if(i<=1):      
            if(j>2*fps):
                
                x=(j-20)*0.025
                print x
                if(i+1<imageCount):
                    x2offset=int((back.shape[1]-images[i+1].shape[1])/2)
                    y2offset=int((back.shape[0]-images[i+1].shape[0])/2)
                    image1=base.copy()
                    image2=base.copy()
                    
                    image2[y2offset:y2offset+images[i+1].shape[0],x2offset:x2offset+images[i+1].shape[1]]=images[i+1]
                    image1[y_offset:y_offset+currentImage.shape[0],x_offset:x_offset+currentImage.shape[1]]=currentImage
    
                    currentImage=image1
                    currentImage=cv2.addWeighted(image1,1-x,image2,x,0)
           
                     
        elif(j<fps*2 and i!=2 and i!=3 and i!=6):
            if(i%2==0):
                k=(j*(currentImage.shape[1]+x_offset)/(fps*2))
                if(k<currentImage.shape[1]):   
                    base[y_offset:y_offset+images[i].shape[0], 0:k] = images[i][0:images[i].shape[0],currentImage.shape[1]-k:currentImage.shape[1]+x_offset]
                    
                else:
                    base[y_offset:y_offset+images[i].shape[0], k-currentImage.shape[1]:k] = images[i][0:images[i].shape[0],0:currentImage.shape[1]]
            else:
                wid=base.shape[1]
                k=(j*(currentImage.shape[1]+x_offset)/(fps*2))
                if(k<currentImage.shape[1]):   
                    base[y_offset:y_offset+images[i].shape[0], wid-k:wid] = images[i][0:images[i].shape[0],0:k]
                else:
                    base[y_offset:y_offset+images[i].shape[0], wid-k:wid-(k-currentImage.shape[1])] = images[i][0:images[i].shape[0],0:currentImage.shape[1]]
            currentImage=base
        else:
            base[y_offset:y_offset+currentImage.shape[0], x_offset:x_offset+currentImage.shape[1]] = currentImage
            currentImage=base

        if(i==3 and j>fps):
            rect=detect_and_draw(currentImage,cascade)
            try:
                cap=cv2.imread('cap.png',-1)
                cwidth=rect[0][2]-rect[0][0]
                cratio=float(float(cwidth)/cap.shape[1])
                cheight=rect[0][3]-rect[0][1]
                cap=cv2.resize(cap,(cwidth+20,cheight+30),interpolation=cv2.INTER_AREA)
                capxOffset=rect[0][0]-10
                capyOffset=rect[0][1]-cheight-30
                capyOffset=(j*capyOffset)/(3*fps)-capyOffset/3
                if(j>4*fps):
                    capyOffset=rect[0][1]-cheight-30
                for c in range(0,3):
                                currentImage[capyOffset:capyOffset+cap.shape[0], capxOffset:capxOffset+cap.shape[1], c] =  cap[:,:,c] * (cap[:,:,3]/255.0) +  currentImage[capyOffset:capyOffset+cap.shape[0], capxOffset:capxOffset+cap.shape[1], c] * (1.0 - cap[:,:,3]/255.0)
            except:
                pass
         
        if(i==2 and j>2*fps):
            glitter1=cv2.imread('glitter1.png',-1)
            glitter2=cv2.imread('glitter2.png',-1)
            glitter3=cv2.imread('glitter3.png',-1)
            glitter4=cv2.imread('glitter4.png',-1)
            x_offset=0
            y_offset=0
    
            display=glitter1
            if(j<2.5*fps):
                display=glitter1
            elif(j<3*fps):
                display=glitter2
            elif(j<3.5*fps):
                display=glitter3
            else:
                display=glitter4
            
            for c in range(0,3):
                currentImage[y_offset:y_offset+display.shape[0], x_offset:x_offset+display.shape[1], c] =  display[:,:,c] * (display[:,:,3]/255.0) +  currentImage[y_offset:y_offset+display.shape[0], x_offset:x_offset+display.shape[1], c] * (1.0 - display[:,:,3]/255.0)
            video.write(currentImage)
            
            
        elif(i==4 and j>2*fps):
            
            balloon=cv2.imread('baloons.png',-1)
            bwidth=int(currentImage.shape[1]/1.5)
            ratio=float(float(bwidth)/currentImage.shape[1])
            bheight=int(currentImage.shape[0]*ratio)
            balloon = cv2.resize(balloon, (bwidth, bheight), interpolation=cv2.INTER_AREA)

            
            print balloon.shape[1]
            x_offset=int((currentImage.shape[1]-balloon.shape[1])/2)
            factor=currentImage.shape[0]-balloon.shape[0]
            y_offset=factor-((factor*j)/(4*fps)-factor/2)
            if(y_offset<0):
                y_offset=0
            temp=currentImage.copy()

            for c in range(0,3):
                currentImage[y_offset:y_offset+balloon.shape[0], x_offset:x_offset+balloon.shape[1], c] =  balloon[:,:,c] * (balloon[:,:,3]/255.0) +  currentImage[y_offset:y_offset+balloon.shape[0], x_offset:x_offset+balloon.shape[1], c] * (1.0 - balloon[:,:,3]/255.0)
            video.write(currentImage)
            currentImage=temp

        elif(i==5 and j>2*fps):
            cake=cv2.imread('cake.png',-1)
            cwidth=int(currentImage.shape[1]/4)
            ratio=float(float(cwidth)/currentImage.shape[1])
            cheight=int(currentImage.shape[0]*ratio)
            cake = cv2.resize(cake, (cwidth, cheight), interpolation=cv2.INTER_AREA)

            
            print cake.shape[1]
            factor=currentImage.shape[1]-cake.shape[1]
            x_offset=(factor*j)/(4*fps)-factor/2
            y_offset=currentImage.shape[0]-cake.shape[0]
            temp=currentImage.copy()
            for c in range(0,3):
                currentImage[y_offset:y_offset+cake.shape[0], x_offset:x_offset+cake.shape[1], c] =  cake[:,:,c] * (cake[:,:,3]/255.0) +  currentImage[y_offset:y_offset+cake.shape[0], x_offset:x_offset+cake.shape[1], c] * (1.0 - cake[:,:,3]/255.0)
            video.write(currentImage)
            currentImage=temp

        elif(i==6):
            print "huaaaa"
            base=back.copy()
            image1=images[i].copy()
            
            image1 = cv2.resize(image1, (image1.shape[1]/2, image1.shape[0]/2), interpolation=cv2.INTER_AREA)
            image2=images[i+1].copy()
            image2 = cv2.resize(image2, (image2.shape[1]/2, image2.shape[0]/2), interpolation=cv2.INTER_AREA)

            x1offset=(base.shape[1]-(image1.shape[1]+image2.shape[1]))/2
            y1offset=(base.shape[0]-image1.shape[0])/2

            x2offset=x1offset+image1.shape[1]
            y2offset=(base.shape[0]-image2.shape[0])/2

            if(j<3*fps):
                k=(j*(image1.shape[1]+x1offset)/(fps*3))
                if(k<image1.shape[1]):   
                    base[y1offset:y1offset+image1.shape[0], 0:k] = image1[0:image1.shape[0],image1.shape[1]-k:image1.shape[1]+x1offset]
                else:
                    base[y1offset:y1offset+image1.shape[0], k-image1.shape[1]:k] = image1[0:image1.shape[0],0:image1.shape[1]]
                wid=base.shape[1]
                
                k=(j*(image2.shape[1]+x2offset-image1.shape[1])/(fps*3))
                if(k<image2.shape[1]):   
                    base[y2offset:y2offset+image2.shape[0], wid-k:wid] = image2[0:image2.shape[0],0:k]
                else:
                    base[y2offset:y2offset+image2.shape[0], wid-k:wid-(k-image2.shape[1])] = image2[0:image2.shape[0],0:image2.shape[1]]
                currentImage=base
            else:
                base[y1offset:y1offset+image1.shape[0], x1offset:x1offset+image1.shape[1]] = image1
                base[y2offset:y2offset+image2.shape[0], x2offset:x2offset+image2.shape[1]] = image2
                cv2.putText(base,'We are the', (base.shape[1]/5,(int)(vheight/2)),cv2.FONT_HERSHEY_COMPLEX_SMALL,3,(128,128,128),6)
                cv2.putText(base,'best buddies', (base.shape[1]/5,(int)(vheight/2+120)),cv2.FONT_HERSHEY_COMPLEX_SMALL,3,(128,128,128),6)
                cv2.putText(base,'From Saurabh', (base.shape[1]/2,(int)(vheight/2+240)),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(128,128,128),4)
                currentImage=base
            video.write(currentImage)
            


        else:
            video.write(currentImage)

        

cv2.destroyAllWindows()
video.release()

os.system('ffmpeg -i video1.avi -i audio.wav -vcodec copy -y -acodec copy finalVideo.avi')                       
                  
    

    
