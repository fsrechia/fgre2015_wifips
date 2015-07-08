sudo iwlist wlan0 scan > scan_output.txt ; grep ESSID scan_output.txt | cut -d\" -f2 > a1 ;  grep Signal scan_output.txt | cut -d= -f3 > a2 ; paste a1 a2 | gawk {' print systime() "\t" $2 "\t" $1; '}

