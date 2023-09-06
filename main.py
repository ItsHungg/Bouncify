# Bai 01
# print(*(lambda _, N: [len(set(N.copy())), "\n"+"\n".join([f"{i} {N.copy().count(i)}" for i in sorted(set(N))])])(input(), list(map(int, input().split()))))

# Bai 02
# print((lambda r, k: f'{r} {"la" if k else "khong phai"} so chinh phuong')(*(lambda x: [x, x**.5 == int(x**.5)])(int(input()))))

A = int(input())
result = 0
while A > 1:
    result += 1
    A /= 10
print(result)
