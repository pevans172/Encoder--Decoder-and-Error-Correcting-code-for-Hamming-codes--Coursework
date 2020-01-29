def hammingGeneratorMatrix(r):
    n = 2**r-1

    #construct permutation pi
    pi = []
    for i in range(r):
        pi.append(2**(r-i-1))
    for j in range(1,r):
        for k in range(2**j+1,2**(j+1)):
            pi.append(k)

    #construct rho = pi^(-1)
    rho = []
    for i in range(n):
        rho.append(pi.index(i+1))

    #construct H'
    H = []
    for i in range(r,n):
        H.append(decimalToVector(pi[i],r))

    #construct G'
    GG = [list(i) for i in zip(*H)]
    for i in range(n-r):
        GG.append(decimalToVector(2**(n-r-i-1),n-r))

    #apply rho to get Gtranpose
    G = []
    for i in range(n):
        G.append(GG[rho[i]])

    #transpose
    G = [list(i) for i in zip(*G)]

    return G
def decimalToVector(n,r):
    v = []
    for s in range(r):
        v.insert(0,n%2)
        n //= 2
    return v
def vectorAddition(v, e):
    # in binary
    total = 0
    output = []
    for i in range(len(v)):
        total = (v[i] + e[i])%2
        output.append(total)
    return output
# https://stackoverflow.com/questions/28253102/python-3-multiply-a-vector-by-a-matrix-without-numpy
# Function below used from url above since numpy doesn't seem to work
def matrixMultiplyWithVector(v, G):
    result = []
    for i in range(len(G[0])): #this loops through columns of the matrix
        total = 0
        for j in range(len(v)): #this loops through vector coordinates & rows of matrix
            total = total + (v[j] * G[j][i])
            # make sure we do binary maths
            total = total%2
        result.append(total)
    return result

# Question 1
# DONE
def message(a):
    l = len(a)
    r = 2
    while True:
        if  (2**r -2*r -1) >= l:
            break
        r = r+1
    k = (2**r - r -1)
    outcome = []
    # now put l in binary form
    binL = bin(l)
    # pad out the result with zeros at the front if needed
    if len(binL) < r+2:
        for i in range((r+2)-len(binL)):
            outcome.append(0)
    # adding the binary number
    for i in range(2, len(binL)):
        outcome.append(int(binL[i]))
    # adding a to the result
    for i in range(l):
        outcome.append(a[i])
    # pad out zeros till end
    if r+l < k:
        for i in range(k-(r+l)):
            outcome.append(0)
    return outcome

# Question 2
# DONE
def hammingEncoder(m):
    r = 2
    while True:
        if len(m) == (2**r -r -1):
            G = hammingGeneratorMatrix(r)
            return matrixMultiplyWithVector(m, G)
        elif r >= 50:
            return []
        r = r+1

# Question 3
# DONE
def hammingDecoder(v):
    r = 2
    n = len(v)
    while r <= 50:
        if n == (2**r)-1:
            break
        r = r+1
    if r >= 50:
        return []
    hT = []
    # r bit representation of all binary numbers length r up to value n
    # in order
    # add them to hT
    for i in range(1, n+1):
        x = bin(i)
        row = []
        # pad out the result with zeros at the front if needed
        if len(x) < r+2:
            for i in range((r+2)-len(x)):
                row.append(0)
        # adding the binary number
        for i in range(2, len(x)):
            row.append(int(x[i]))
        hT.append(row)
    # hT has now been made
    # check = vhT
    check = matrixMultiplyWithVector(v, hT)
    # see if all elements here are zeros
    allZero = []
    for i in range(len(check)):
        allZero.append(0)
    if allZero == check:
        return v
    # Make the e vector
    # first make a master for loop that will everytime wipe clean e
    # and add a single 1
    # then for each e check if we get all zeros out
    e = []
    z = 0
    c = []
    for i in range(n):
        # fill e with zeros
        for i in range(n):
            e.append(0)
        # put the one in the right spot
        e[z] = 1
        # now we do the e multiplacation
        checker = matrixMultiplyWithVector(e, hT)
        if checker == check:
                c = vectorAddition(v, e)
                break
        else:
            e = []
            z = z+1
    return c

# Question 4
# DONE
def messageFromCodeword(c):
    m = c
    r = 2
    n = len(c)
    while True:
        if n == 2**r-1:
            break
        r = r+1
        if r >= 50:
            return []
    for i in range(r):
        x = 2**(r-1-i)-1
        del m[x]
    return m

# Question 5
# DONE
def dataFromMessage(m):
    message = m
    k = len(m)
    r = 2
    outcome = []
    while True:
        if  (2**r -r -1) == k:
            break
        r = r+1
        if r >= 50:
            return outcome
    l = 0
    for i in range(r):
        l = l+( message[i]*(2**(r-1-i)) )
    if r+l > k:
        return outcome
    elif r+l < k:
        for i in range(r+l, k):
            if message[i] != 0:
                return outcome
    for i in range(r, r+l):
            outcome.append(message[i])
    return outcome

# Question 6
# DONE
def repetitionEncoder(m,n):
    x = m[0]
    outcome = []
    for i in range(n):
            outcome.append(x)
    return outcome

# Question 7
# DONE
def repetitionDecoder(v):
    zeroCount = v.count(0)
    oneCount = v.count(1)
    if zeroCount < oneCount:
        outcome = [1]
    elif oneCount < zeroCount:
        outcome = [0]
    else:
        outcome = []
    return outcome
