node 1 0 0
node 2 1 0

material Subloading1D 1 2E5 \
232 0 70 30 \
209 0 63 30 \
2E3 2 143 0.7

element T2D2 1 1 2 1 1

plainrecorder 1 Element HIST 1
plainrecorder 2 Element S 1
plainrecorder 3 Element E 1

fix2 1 1 1
fix2 2 2 1 2

amplitude Tabular 1 cyclic

cload 1 1 50 1 2

step static 1 20
set fixed_step_size 1
set ini_step_size 2E-3
set symm_mat 0

converger RelIncreDisp 1 1E-10 10 1

analyze

save recorder 1 2 3

reset
clear
exit