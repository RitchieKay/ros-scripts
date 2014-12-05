set title "APME Elevation/Azimuth"
set xlabel "Seconds (s)"
set ylabel "Angles (rad)"
plot 'apme.txt' using 1:3 title "Elevation", 'apme.txt' using 1:4 title "Azimuth"
