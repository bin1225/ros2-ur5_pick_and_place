import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/bin1225/ur_ws/install/my_pick_and_place_pkg'
