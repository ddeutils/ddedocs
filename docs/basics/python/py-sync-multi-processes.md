# Synchronizing Multi-Processes

```python
import multiprocessing
import time


def increase_counter(counter, lock):
    for _ in range(20):
        lock.acquire()
        counter.value() += 10
        lock.release()
        time.sleep(0.1)


def decrease_counter(counter, lock):
    for _ in range(20):
        with lock:
            counter.value() -= 10
        time.sleep(0.1)

counter = multiprocessing.Value('i', 0)
lock = multiprocessing.Lock()

increase = []
decrease = []

for _ in range(5):
    p = multiprocessing.Process(target=increase_counter, args=(counter, lock, ))
    p.start()
    increase.append(p)

for _ in range(5):
    p = multiprocessing.Process(target=decrease_counter, args=(counter, lock, ))
    p.start()
    decrease.append(p)

for p in increase:
    p.join()

for p in decrease:
    p.join()

print(counter)
```
