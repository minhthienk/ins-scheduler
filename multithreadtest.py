 
import threading
import time


def mythread():
	time.sleep(2)

def main():
    threads = 0     #thread counter
    y = 2001     #a MILLION of 'em!
    x ={}
    for i in range(y):
        try:
            s = time.time()
            x[i] = threading.Thread(target=mythread, args = (), daemon=True)
            threads += 1    #thread counter
            x[i] .start()       #start each thread
            print(time.time()-s)
        except RuntimeError as e:    #too many throws RuntimeError
            print(e)
            break
    print("{} threads created.\n".format(threads))
    x[2000].join()
if __name__ == "__main__":
    main()