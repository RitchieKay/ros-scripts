set title "Wheel Angular Momentum"
set xlabel "Seconds (s)"
set ylabel "Angular Momentum (Nms)"
plot 'wheel.txt' using 1:2 title "RWA A", 'wheel.txt' using 1:3 title "RWA B", 'wheel.txt' using 1:4 title "RWA C", 'wheel.txt' using 1:5 title "RWA D"
