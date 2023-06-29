from scaledrivers import scale

def main():
    scale1 = scale.auto_connect_scale()
    if scale1 is None:
        print("No scale found")
        exit()
    print("Scale found: " + str(scale1))

    cin = input()
    while cin != 'q':
        print(scale1.send_receive(cin))
        cin = input()

if __name__ == "__main__":
    main()