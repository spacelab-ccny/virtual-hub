#!/bin/bash
#xterm -title "App1" -hold -e "cat test.txt" &
#xterm -title "App 2" -hold -e "cat test.txt" &

#xdotool windowfocus --sync $(xdotool search --name App1) # set focus on xterm with title `node1`
#xdotool type "Hello, World!"
#xdotool key Return
#!/bin/bash
  
xterm -title node1 -hold -e 'cat test.txt' &
xterm -title node2 -hold -e 'cat test2.txt' &
sleep 1

name= xdotool search --name "node1"
xdotool getwindowfocus
xdotool windowfocus --sync $name # set focus on xterm with title `node1`
xdotool type cat test.txt
#xdotool key Return