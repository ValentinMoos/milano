ssh k1 'rm /home/mov57924/work/artemide/hpd_setup_3/milano2.cc /home/mov57924/work/artemide/hpd_setup_3/milano2.py /home/mov57924/work/artemide/hpd_setup_3/run.sh -f'
scp -C milano2.py k1:/home/mov57924/work/artemide/hpd_setup_3/
scp -C milano2.cc k1:/home/mov57924/work/artemide/hpd_setup_3/
scp -C run.sh k1:/home/mov57924/work/artemide/hpd_setup_3/
scp -C milano.py k1:/home/mov57924/work/artemide/pythonlib/
scp -C milano2_toy.py k1:/home/mov57924/work/artemide/hpd_setup_3/
