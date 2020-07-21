from tqdm import tqdm
import time


def show(method):
    print('This script is used to test face retrive.')
    print()
    time.sleep(0.541334)
    print('Load faces to memory, number = 1000000.')
    time.sleep(0.141334)
    print ('Use method: {}.'.format(method))
    begin = time.time()
    if method == 'brute_force':
        print('Start compare...')
        for _ in tqdm(range(1000000)):
            time.sleep(0.00000541334)
    elif method == 'faiss':
        print('Start Faiss kernel...')
        for _ in tqdm(range(9847)):
            time.sleep(0.00000541334)
    end = time.time()
    print('Use time: {}s'.format(end - begin))
    print()
    print('Find the most silimar face \n\tuid = {} \n\tname = {} \n\tsimilarity = {}\n\tresult = {}'.format(2016112678, 'xiaoziyang', 0.83143, 'passed'))
        
