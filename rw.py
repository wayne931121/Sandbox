while 1:
    try:
        a = input("Input 1 to exit, type any to test (example: ./sandbox_root/1.txt): ")
        if a=="1":break
        try:
            with open (a,"wb") as f:
                f.write(b"5")
            print("sccess W")
        except Exception as e:
            print("failed W",e)
        try:
            with open (a,"rb") as f:
                f.read()
            print("sccess R")
        except Exception as e:
            print("failed R",e)
    except Exception as e:
        print(e)
        break
