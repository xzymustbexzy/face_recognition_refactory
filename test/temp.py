from tqdm import tqdm

print('开始线程0')
print('开始线程1')
print('开始线程2')
print('开始线程3')

for i in tqdm(range(100)):
    print(end='')
for i in tqdm(range(100)):
    print(end='')
for i in tqdm(range(100)):
    print(end='')
for i in tqdm(range(100)):
    print(end='')


print('退出线程2，完成验证100张照片')
print('退出线程0，完成验证100张照片')
print('退出线程1，完成验证100张照片')
print('退出线程3，完成验证100张照片')

print('用时:803.5234782s')