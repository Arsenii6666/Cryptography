def generate_matrix(height):
    """Generate Hemming matrix
    >>> generate_matrix(4)
    ['11111111',
     '00011110',
     '01100110',
     '10101010']"""
    width=2**(height-1)
    matrix=[]
    matrix.append('1'*width)
    width//=2
    num_of_printing=1
    for _ in range(height-1):
        to_list=(width*'0'+width*'1')*num_of_printing
        num_of_printing*=2
        width//=2
        to_list=to_list[1:]+to_list[0]
        matrix.append(to_list)
    return matrix

def code_number(num):
    """Get int, positive number of of any size.
    Return it encoded for transportation with risk of errors."""
    num=bin(num)[2:]
    height=4
    usefull_num=2**(height-1)-height   # num of symbols, which can be encoded
    while usefull_num<len(num):
        height+=1
        usefull_num=2**(height-1)-height
    num=((usefull_num-len(num))*'0')+num
    num=[int(i) for i in num]
    for j in range(0, height):
        num.insert(2**j-1, 0)
    checks=generate_matrix(height)
    for check, j in zip(checks[::-1], range(height)):
        xor_sum=0
        for i in range(len(num)):
            if check[i]=='1':
                xor_sum^=num[i]
        if xor_sum==1:
            num[(2**j)-1]=num[2**j-1]^1
    output=''
    for i in num:
        output+=str(i)
    return output

def check_and_decode_num(num):
    """Decode massege, encoded for transportation. Also can find mistake, if it have.
    Can not find more than 1 mistake"""
    height=4
    while 2**(height-1)!=len(num):
        height+=1
    num=[int(i) for i in num]
    checks=generate_matrix(height)
    error_code=''
    for check in checks:
        xor_sum=0
        for i in range(len(num)):
            if check[i]=='1':
                xor_sum^=num[i]
        error_code+=str(xor_sum)
    can_decode=False
    if error_code.count('1')==0:
        can_decode=True
    else:
        for i in range(len(num)):
            check_error_code=''
            for check in checks:
                check_error_code+=check[i]
            if check_error_code==error_code:
                num[i]^=1
                can_decode=True
                break
    if can_decode:
        for j in range(0, height)[::-1]:
            num.pop(2**j-1)
        output=0
        for i in range(len(num)):
            output+=num[i]*2**(len(num)-i-1)
        return output
    return "Error. There are to much errors to decode it."
