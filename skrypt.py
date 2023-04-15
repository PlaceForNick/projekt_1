

def flh2xyz(f,l,h,a,e2):
    N = Np(f,a,e2)
    x = (N+h)*np.cos(f)*np.cos(l)
    y = (N+h)*np.cos(f)*np.sin(l)
    z = ((N*(1-e2)+h))*np.sin(f)
    return x,y,z 