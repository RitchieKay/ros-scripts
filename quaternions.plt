set title "Quaternion Profiles"
set xlabel "Seconds (s)"
plot 'quaternions.txt' using 1:2 title "Q1", 'quaternions.txt' using 1:3 title "Q2", 'quaternions.txt' using 1:4 title "Q3", 'quaternions.txt' using 1:5 title "Q4"
