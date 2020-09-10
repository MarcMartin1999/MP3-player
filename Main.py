from pygame import mixer_music as music
import pygame
import glob
import os
from tkinter import * 
import tkinter.ttk as ttk
from mutagen.mp3 import MP3


auxSlide = 0
playtime =0
window = Tk()
currentSong = 0
firstClick = 1
pausePlayClock = 0
shuffle = False
pathToFile = os.path.dirname(os.path.abspath(__file__)) + "\playlist"    
currentSongName=""



def createPlaylist() :
    global pathToFile 
    playlist = glob.glob(pathToFile + '**/*' ) #Creates a list of all mp3 songs on the folder playlist
    print(playlist)
    return playlist

def changeName(currentSongNameLabel):
    global currentSongName
    currentSongName = playlist[currentSong]
    currentSongName = currentSongName.replace(pathToFile,'')
    currentSongName = currentSongName.replace('-',' ')
    currentSongName = currentSongName.replace('.mp3','')
    currentSongNameLabel.configure(text= currentSongName)

def playSong() :
    global playtime
    global firstClick
    global pausePlayClock

    if firstClick ==1:
        music.play(0)
        playButton['text'] = 'Pause'
        firstClick = 0
    else:
        if(pausePlayClock == 1):
            music.play(0,playtime)   
            playButton['text'] = 'Pause'
            pausePlayClock = 0
        else :
            music.stop()
            playButton['text'] = 'Play!'
            pausePlayClock = 1
    window.after(1000,loopScale)
        
def previousSong():
    global auxSlide,playtime,currentSong,progressBar,currentSongNameLabel,pathToFile
    music.stop()
    playtime = 0
    progressBar.set(0)
    if currentSong == 0:
        music.load(playlist[len(playlist)-1])
        music.play(0,0)
        currentSong = len(playlist)-1
    else:
        music.load(playlist[currentSong-1])
        music.play(0,0)
        currentSong = currentSong-1
    changeName(currentSongNameLabel)
    audio =MP3(playlist[currentSong])
    auxSlide = audio.info.length
    progressBar.configure(to=auxSlide )

def nextSong():
    global playtime,auxSlide,currentSong,progressBar,currentSongNameLabel,pathToFile
    music.stop()
    playtime = 0
    progressBar.set(0)
    if currentSong == len(playlist)-1:
        music.load(playlist[0])
        music.play(0,0)
        currentSong = 0       
    else:
        music.load(playlist[currentSong+1])
        music.play(0,0)
        currentSong = currentSong+1
    changeName(currentSongNameLabel)
    audio =MP3(playlist[currentSong])
    auxSlide = audio.info.length
    progressBar.configure(to=auxSlide)

def sideController(event):
    global auxSlide,playtime,progressBar
    if music.get_busy():
        music.play(0,(event.x/450)*auxSlide)
        music.stop()
        playtime = (event.x/450)*auxSlide
        progressBar.set(playtime)
        music.load(playlist[currentSong])
        music.play(0,(event.x/450)*auxSlide)
    else:
        music.play(0,(event.x/450)*auxSlide)
        music.stop()
        playtime = (event.x/450)*auxSlide
        progressBar.set(playtime)
        music.load(playlist[currentSong])
def loopScale():
    global playtime,auxSlide
    if music.get_busy(): 
        progressBar.set(playtime)
        playtime +=1
        window.after(1000,loopScale)
    else :
        if auxSlide-1 <= playtime:
            nextSong()
            window.after(1000,loopScale)
        else:
            return
    
pygame.init()
playlist =createPlaylist()
print(pathToFile)
music.load(playlist[currentSong])
audio =MP3(playlist[currentSong])


programName = Label(window,text = "MP3-Player")
programName.grid(row = 0, column=0,columnspan=5,padx=80)
programName.config(font=("Courier", 44))

currentSongNameLabel = Label(window,text="",font=("Courier",10))
currentSongNameLabel.grid(row = 1, column=0,columnspan=5,padx=10)
changeName(currentSongNameLabel)

progressBar = Scale( window, orient = HORIZONTAL,variable=playtime, length=450,showvalue = 0)
progressBar.bind("<Button-1>", sideController)
progressBar.grid(row=2,column=0,columnspan=6,pady=30)
auxSlide = audio.info.length
progressBar.configure(to=auxSlide)

playButton = Button(window,text="Play!", command =playSong)
playButton.grid(row = 3, column=1,padx =20)
playButton.config(font=("Courier", 20))

previousButton= Button(window,text="Previous", command =previousSong)
previousButton.grid(row = 3,column=0,padx =20)
previousButton.config(font=("Courier", 20))

nextButton= Button(window,text="Next", command =nextSong)
nextButton.grid(row = 3,column=2 ,padx =20)
nextButton.config(font=("Courier", 20))

window.geometry("500x250")
window.mainloop()

