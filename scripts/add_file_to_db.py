import requests
from tqdm import tqdm
import time
from multiprocessing import Pool
def add_combo(combo):
    request = requests.post('https://127.0.0.1:8000/api/email/add_combo/', data={'combo': combo}, headers={'Authorization': 'Token    20f6582c008e8efe54055e80b8871e2264e42b07'})
if __name__ == '__main__':
    start_time = time.time()
    lines = []
    with open('../test/1.49M_HQ_Email_Pass.txt') as f:
        lines = f.read().splitlines()
    p = Pool(20)
    print(lines)
    p.map(add_combo, lines)
    p.close()
    p.join()
    elapsed_time = time.time() - start_time
    print('added ' + str(len(lines)) + ' combos in' +  '\nelapsed time: ' + str(elapsed_time))
