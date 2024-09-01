# REGULA_FALSI_METHOD

def REGULA_FALSI_METHOD(xl,xu,func,y):
    Es = 10**-6
    i_max = 50
    # print(f"{func(xl)},{func(xu)}")
    if (func(xl)-y)*(func(xu)-y)>0:
        # print("if 1")
        xr=None
        Ea=None
        print("Choose other Interval\n This may be due to \n(i) either not roots lie inside the bracket \n(ii) or more then one root is there")
        return xr
    Ea = 100
    i=1
    xr=None
    while True:
        # print("while")
        if (i>i_max or Ea<Es):
            # print("while if")
            return xr
        else:
            # print("while else ")
            # print(f"{xl, func(xl)},{xu, func(xu)}")
            A = ( -(func(xu)-y)/((func(xl)-y) - (func(xu)-y)))
            B=1-A
            xr = A*xl + B*xu;           
            Ea = abs((y-func(xr))/y); # Ea shall be ab solute values otherwise if it becomes negative then loop will stop because negative value of Ea is always less then Es even if magnitude of error is large
            if (func(xr)-y)*(func(xl)-y)<0:
                xu=xr
            elif (func(xr)-y)*(func(xu)-y)<0:
                xl=xr
            elif (func(xr)-y)*(func(xl)-y)==0:
                return xr

        i=i+1

