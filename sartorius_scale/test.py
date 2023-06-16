from scaledrivers import scale, mettlertoledo

scale = mettlertoledo.MettlerToledo("COM5")
cin = input()
while cin != 'q':
    print(scale.send_receive(cin))
    cin = input()