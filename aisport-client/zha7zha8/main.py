from Utils import every_move_init_before

one = every_move_init_before.init_before('up', 'tiaoshenCSV')
count,time=one.move_before_init_and_run()
print(count,time)