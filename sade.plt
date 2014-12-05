set title "Solar Array Angles"
set xlabel "Seconds (s)"
set ylabel "Angles (rad)"
plot 'sade.txt' using 1:2 title "YP", 'sade.txt' using 1:3 title "YM"
