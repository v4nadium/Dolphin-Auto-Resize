#! /bin/bash
#

echo "/!\\ DISCLAIMER /!\\"
echo "I am not an expert. Please check that the files that you have downloaded do execute as intended."
echo "Continue <Enter> \t Quit: <Ctrl-C>"
read
echo

echo "Exec=/home/$USER/bin/dolphin_resize.py" >> ./autoresize.desktop

mv ./autoresize.desktop /home/$USER/.local/share/kservices5/ServiceMenus

mv ./dolphin_resize.py /home/$USER/bin/

echo"#! /bin/bash

while [ true ] ;
    do
    python /home/$USER/bin/dolphin_resize.py
    sleep 1
    done" > ./dolphin_auto_resize.sh

mv ./dolphin_auto_resize.sh /home/$USER/bin/

echo "Please manually go to the Dolphin Preferences and check the \"Show full path inside location bar\" box in the Startup tab."
read
echo "Ok I guess it is now installed.."
sleep 1


echo "A Dolphin Service has been created. Right-click inside a Dolphin window and select Automatic Resize to... well... resize automatically."
read
echo "You can run the /home/$USER/bin/dolphin_auto_resize.sh script in the background. It will resize any Dolphin window instantaneously (every 1 sec actually)."
read
echo "You can tweak the first lines of your /home/$USER/bin/dolphin_resize.py to fit your current screen settings, or even the entire file if you feel like optimising it."
echo
