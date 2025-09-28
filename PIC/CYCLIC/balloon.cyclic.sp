node 1 0 0
node 2 1 0

material Balloon1D 1 \
2E5 5E3 .999 1 \
200 1E3 0 0 \
0 -2E2 0 0 \
0 0 0 0 \
5E3 1. \
100 0.7

element T2D2 1 1 2 1 1

plainrecorder 1 Element HIST 1
plainrecorder 2 Element S 1
plainrecorder 3 Element E 1

fix2 1 1 1
fix2 2 2 1 2

expression SimpleScalar 1 t 0.5-0.5*cos(6.28318530718*t)

amplitude Tabular 1 cyclic

amplitude Sine 2 1 1

amplitude Custom 3 1

# cload 1 2 200 1 2
disp 1 2 2e-3 1 2

step static 1 1000
set fixed_step_size 1
set ini_step_size 1E-2
set symm_mat 0

converger RelIncreDisp 1 1E-10 10 1

analyze

save recorder 1 2 3

exit