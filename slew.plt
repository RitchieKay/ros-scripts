set multiplot layout 2, 2
set tmargin 2
#
#
set title "Wheel Angular Momentum"
set xlabel "Seconds (s)"
set ylabel "Angular Momentum (Nms)"
plot 'wheel.txt' using 1:2 title "RWA A", 'wheel.txt' using 1:3 title "RWA B", 'wheel.txt' using 1:4 title "RWA C", 'wheel.txt' using 1:5 title "RWA D"
#
#
set title "Solar Array Angles"
set xlabel "Seconds (s)"
set ylabel "Angles (rad)"
plot 'sade.txt' using 1:2 title "YP", 'sade.txt' using 1:3 title "YM"
#
#
set title "APME Elevation/Azimuth"
set xlabel "Seconds (s)"
set ylabel "Angles (rad)"
plot 'apme.txt' using 1:3 title "Elevation", 'apme.txt' using 1:4 title "Azimuth"
#
#
set title "APME Set"
set xlabel "Seconds (s)"
set ylabel "Set 1 / Set 2"
set yrange [0.5:2.5]
plot 'apme.txt' using 1:2 title "Set"
