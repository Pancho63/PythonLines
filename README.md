a small fullscreen app which draw 2 rectangles and 2 elipses (and a pixmap) in RGB via sACN.  
It responde to univers 7, channels :  
First rectangle :  
-1 : Master  
-2 : R  
-3 : G  
-4 : B  
-5 : thickness  
-6 : 360° rotation  
-7-8 : 16bit PAN  
-9-10 : 16Bit TILT  
-11-12 : 16Bit width  
-13-14 : 16Bit height  

15 - 28 : Rectangle 2  
29 - 42 : Elipse 1  
43 - 56 : Elipse 2  

Pimax  
-57 : Master  

-62 : 360° rotation 
-63-64 : 16bit PAN  
-65-66 : 16Bit TILT  
-67-68 : 16Bit width  
-69-70 : 16Bit height  
 
-71 : load image : 11 ranges : 1 : no image, 2 : image1 .... 11 : image10  

-------------------

INSTALL on raspberry

create a raspian legacy 64bit installation with desktop -  for example with pi imager

in raspian : 

git clone https://github.com/Pancho63/PythonLines

sudo apt install ola unclutter libxcb-cursor-dev xscreensaver

preferences/screensaver : deactivate (may need a reboot)  
in the web navigator  
http://localhost:9090/ola.html
create an input univers 7 sacn
stop ola (to record config)
sudo reboot

cd PythonLines  
python3 -m venv env  
source env/bin/activate  
pip install PyQt6 ola

Open :  
env/lib/python3.xx/site-packages/ola/OlaClient.py  
search and remplace twice :  
data.fromstring(request.data)  
by  
data.frombytes(request.data)  


to autostart the app and hide the cursor :

create a script /home/pi/lancement.bash  
with in it :  
#!/bin/bash  
sudo service olad restart  
unclutter -idle 0 &  
/home/pi/PythonLines/env/bin/python3.9 /home/pi/PythonLines/Lines.py  
pkill unclutter

sudo nano /etc/xdg/lxsession/LXDE-pi/autostart  
add at the end : @/home/pi/lancement.bash

enjoy


