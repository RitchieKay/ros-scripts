set title "Wheel Angular Momentum"
set xlabel "Seconds (s)"
set ylabel "Angular Momentum (Nms)"
plot 'wheels.txt' using 1:2 title "RWA A", 'wheels.txt' using 1:3 title "RWA B", 'wheels.txt' using 1:4 title "RWA C", 'wheels.txt' using 1:5 title "RWA D"
