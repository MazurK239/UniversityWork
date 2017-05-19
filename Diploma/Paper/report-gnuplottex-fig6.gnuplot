set terminal latex
set output 'report-gnuplottex-fig6.tex'
set terminal epslatex color size 16cm,7cm
  set xzeroaxis lt -1
  set yzeroaxis lt -1
  set style line 1 lt 1 lw 4 lc rgb '#4682b4' pt -1
  set grid ytics lc rgb '#555555' lw 1 lt 0
  set grid xtics lc rgb '#555555' lw 1 lt 0
  set xrange [38:366]
  set format y "%.2f"
  set xlabel '$t$, DOY'
  set ylabel '$Z$, м'
  plot '../vstk/xyz.dat' using 1:4 title ''
 
