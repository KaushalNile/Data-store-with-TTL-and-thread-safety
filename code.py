import json
import sys
import os
import pprint
import time
import threading

dict = {}
i = 0
def create(rg, name, col, prc, ttl=None):
    global dict
    global i
    values = {}
    flag = 1
    open("AutomobileAccidentDB.json", "w")

    if os.stat('AutomobileAccidentDB.json').st_size and i<1:
        i += 1
        with open('AutomobileAccidentDB.json', 'r') as f:
            dict = json.load(f)
    else:
        pass

    check_ttl()

    for key in dict.keys():
        if key == rg:
            flag = 0
            break
        else:
            flag = 1
    if flag == 1:
        values['Registration No.'] = rg
        values['Name'] = name
        values['Colour'] = col
        values['Showroom Price'] = prc
        values['Insertion Time'] = time.time()
        values['TTL'] = ttl
        dict[rg] = values
    else:
        print("!!! Record not added. Vehicle of this Registration No. already present in Database !!!\n")

def read(rg_read):
    global dict
    with open('AutomobileAccidentDB.json', 'r') as f:
        dict = json.load(f)

    check_ttl()
    if rg_read in dict.keys():
        pprint.pprint(dict[rg_read] , width = 5, indent = 3, sort_dicts = False)
        print("\n")
    else:
        print("!!! Record does not exist in Database !!!\n")

def delete(rg_del):
    global dict
    with open('AutomobileAccidentDB.json', 'r') as f:
        dict = json.load(f)

    if rg_del in dict:
        del dict[rg_del]
    else:
        print("!!! Vehicle of this Registration No. does not exist in Database !!!\n")

    json_object = json.dumps(dict, indent = 6)
    with open("AutomobileAccidentDB.json", "w") as f:
        f.write(json_object)
        f.write("\n")
        f.close()

def check_ttl():
    global dict
    for key,values in dict.items():
        if values['TTL'] != None:
            if values['Insertion Time']+values['TTL'] < time.time():
                delete(key)
            else:
                pass
        else:
            pass


def menu(lock):

    while True:
        lock.acquire()
        flag = 1
        print("****Automobile Database****\n")
        print("1.Create Record\n")
        print("2.Read Record\n")
        print("3.Delete Record\n")
        print("4.Exit\n")
        print("***************************\n")
        choice = int(input("Enter your choice :"))
        if choice == 1:
            while True:
                rg = input("Enter Registration number :")
                name = input("Enter the name of vehicle :")
                col = input("Enter colour of vehicle :")
                prc = float(input("Enter price :"))
                chc = input("Do you want to set Time-to-Live for this record(y/n) :")
                if chc=='n' or chc=='N' or chc=='no' or chc=='No' or chc=='NO':
                    create(rg, name, col, prc)
                else:
                    ttl = float(input("Enter Time-to-Live for this record :"))
                    create(rg, name, col, prc, ttl)
                ch = input("Add one more record? (y/n) :")
                if ch=='n' or ch=='N' or ch=='no' or ch=='No' or ch=='NO':
                    obj = json.dumps(dict, indent = 6)
                    with open("AutomobileAccidentDB.json", "w") as f:
                        f.write(obj)
                        f.write("\n")
                        f.close()
                    flag = 1
                    break

        elif choice == 2:
            rg_read = input("Enter Reg. No. for details :")
            read(rg_read)

        elif choice == 3:
            rg_del = input("Enter Reg. No. for deleting the record :")
            delete(rg_del)

        elif choice == 4:
            if threading.current_thread().getName() == 'MainThread' :
                sys.exit("Records Updated Successfully in Database\n")
            else:
                lock.release()
        else:
            print("Wrong choice!\n")
        if flag==1:
            lock.release()
        else:
            pass


def main():
    lock = threading.Lock()
    numThreads = int(input("Enter the number of threads :"))
    threads = [0] * numThreads

    for i in range(0, numThreads):
        threads[i] = threading.Thread(target=menu, args=(lock,))

    for i in range(0, numThreads):
        threads[i].start()
        threads[i].join()


if __name__ == "__main__":
    main()
