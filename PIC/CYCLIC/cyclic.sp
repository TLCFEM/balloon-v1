node 1 0 0
node 2 1 0

material Subloading1D 1 2E5 \
200 8E3 0 0 \
0 0 0 0 \
1E3 0 200 0.7

element T2D2 1 1 2 1 1

plainrecorder 1 Element HIST 1
plainrecorder 2 Element S 1
plainrecorder 3 Element E 1

fix2 1 1 1
fix2 2 2 1 2

amplitude Tabular 1 cyclic

cload 1 1 50 1 2

step static 1 49
set fixed_step_size 1
set ini_step_size 5E-3
set symm_mat 0

converger RelIncreDisp 1 1E-10 10 1

analyze

save recorder 1 2 3

reset
clear
exit