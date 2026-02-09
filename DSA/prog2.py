s = input()
low = 0
high = 0

for ch in s:
    
    if ch == "(":
        low += 1
        high += 1
        
    elif ch == ")":
        low -= 1
        high -= 1
        
    else:
        low -= 1
        high += 1
    
    if high < 0:
        print("false")
        exit()
    
    low = max(low, 0)

print("true" if low == 0 else "false")
