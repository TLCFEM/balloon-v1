node 1 0 0
node 2 1 0

material Balloon1D 1 \
2E5 1E6 1E0 1E3 4 \
200 2E2 0 0 \ ! hf
0 0 0 0 \ ! ha
2 1E0 0 0 \ ! hb
200 6E3 0 0 \ ! hd
5E3 0 \ ! alpha
1E1 0 \ ! beta
5E3 0 ! d

element T2D2 1 1 2 1 1

plainrecorder 1 Element HIST 1
plainrecorder 2 Element S 1
plainrecorder 3 Element E 1

fix2 1 1 1
fix2 2 2 1 2

# expression SimpleScalar 1 t t<100?0.5-0.5*cos(2pi*t):1-cos(2pi*t)
expression SimpleScalar 1 t t<100?sin(2pi*t):2sin(2pi*t)

amplitude Custom 3 1

# cload 1 3 200 1 2
disp 1 3 2e-3 1 2

step static 1 200
set fixed_step_size 1
set ini_step_size 1E-2
set symm_mat 0

converger RelIncreDisp 1 1E-10 10 1

analyze

save recorder 1 2 3

exit