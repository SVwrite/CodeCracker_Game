#!/use/bin/python3
#Shreynash 05-04-2021

#The objective of this program is to create a game akin Mastermind
#Link = http://codebreaker.creativitygames.net/

import random
import re
import time
import csv
import os
import traceback


flag = 1

seconds = 0


def homepage():
    op = 1

    print("\t\t##############################")  # 30 hashes
    print("\t\t#\t\t\t     #")
    print("\t\t#\tCODE BREAKER\t     #")
    print("\t\t#\t\t\t     #")
    print("\t\t##############################\n\n\n\t\t")
    print("\t\t1. PLAY\t\t\t2.HOW TO PLAY\n\n\t\t3.LEADER BOARD\t\t4.QUIT")
    # print("\n\n\t\tSelect any option to continue : ")
    while 0 < op < 5:
        op = input("\n\t\tSelect any option to continue : ")
        match = re.search(r"^[1-4]$", op)
        if match is None:
            print("\t\tInvalid Input, try again")
            op = 1
            continue

        op = int(op)
        break
    if op == 1:
        game()
    if op == 2:
        exit()
    if op == 3:
        leaderBoardRead()
    if op == 4:
        exit()

def game():
    iniprompt()
    code, s = codeMaker()
    AttemptCounter(code, s)

def iniprompt():
    print("Welcome to the Code Breaker.\nYou has 8 attempts to guess a 5 digit code")
    print("The code consists of digits between 1 to 8 (non recurring)")

def codeMaker():  #Generating the code. The code has to consist of numbers between 1 and 8 (non recurring)
    code=[]
    while len(code)<5:
        r=random.randint(1,8)
        s=set(code)
        if r not in s:
            code.append(r)
    print ("Code: ",code)
    return code, set(code)

def UserAttempt(): #Now we take input from user. Can't have GUI, so we make them enter the code as whole.
    global flag
    global seconds

    while flag < 9:
        print("Attempt {}".format(flag) )
        if seconds == 0:
            timer(True)
        attempt= input(" Enter a 5 digit number : ")
        #Starting timer

        att=[]
        #Check if the input is purely
        match = re.search(r"^[1-8]{5}$", attempt)
        #print(match)
        
        if match == None:
            print ("Invalid input, try again.")
            continue
        attempt.split()
        print(attempt)
        for a in attempt:
            #print (a)
            if 1<=int(a)<=8:
                att.append(int(a))
            else :
                print("Values out of range. Please enter digits between 1 and 8 only")
                continue
        flag+=1
        return att

def playAgain():
    global flag
    global seconds
    con = 'n'
    while con == 'n':
        con = input("\n\tPlay Again? (y/n): ")
        match = re.search(r"^[yYnN]$", con)
        if match == None:
            print("\n\n\tInvalid input, try again")
            con = 'n'
            continue
        if con == 'Y' or con == 'y':
            flag = 0
            seconds = 0
            game()
        else:
            exit(0)

def AttemptCounter(code, s):
    global flag
    res = 1
    while flag <= 9 and res == 1:
        print("____________________________________________________")
        if flag > 8:
            print("\tYou have exhausted all your attempts.")

                   #Stopping timer at exhaustion of all attempts.
            t = timer(False)
            print("\tTime Taken: {}".format(t))
            playAgain()

            
        else:
            print("\n\tThis is attempt number {}.".format(flag))
            a = UserAttempt()
            res = comparison(a, code, s)

def comparison(att, code, s):           
    #print (att)
    i = -1
    countN=0
    countP=0
    #print(att)
    #print(s)
    for a in att:
        i += 1
        if a in s:
            countN += 1
            #print("a :",a)
            #print("code[{}] : {}".format(i, code[i]))
            if a == code[i]:
                countP += 1
        
    
    #print (i, countN, countP)
    if countP == 5 and countN == 5:
        print("Congrats! Code Cracked\n\tThe code was {}".format(code))
        t = timer(False)
        print("Time Taken: ", t)
        name = ""
        name = input("\n\tPlease Enter your name :")
        if name == "":
            name = "Anonymous"
        leaderBoardWrite(name, t)
        return 0
    else:
        print("There are {} matching digits.\n\t{} are in correct places".format(countN, countP))
        return 1

def timer(run):
    global seconds
    e=0
    if run == True:
        seconds= time.time()
        return 0
    if run == False:
        e = time.time()
    if e!=0:
        t=timeformatter(e-seconds)
        seconds=0
        #print("\n\t1")
        #print (seconds,e,t)
        return t

def timeformatter(t):
    #print("\n\t2")
    #print(type(t))
    #print (t)
    date = time.gmtime(t)

    #print("\n\t3")
    #print(type(date))
    #print(date)
    #h=m=s=10
    h = int( time.strftime("%H",date))
    m = int(time.strftime("%M",date))
    s = int(time.strftime("%S",date))
    return h*3600+m*60+s


def leaderBoardWrite(name, t):
    fileExists = os.path.isfile("leaderboard.csv")
    if fileExists == False:
        with open("leaderboard.csv", "w", newline="") as file:
            w = csv.writer(file)
            w.writerow(["Name", "Time"])

    with open("leaderboard.csv", "a", newline="") as file:
        w = csv.writer(file)
        w.writerow([name, t])

def leaderBoardRead():
    try:
        #print("here21")
        fileExists = os.path.isfile("leaderboard.csv")
        if fileExists is False:
            print("here22")
            with open("leaderboard.csv", "w", newline="") as file:
                w = csv.writer(file)
                w.writerow(["Name", "Time"])

        sorter = []
        with open("leaderboard.csv", "r")as file:
            reader = csv.DictReader(file)
            #print(type(reader))
            for row in reader:
                #print(type(row))
                #print(row)
                sorter.append([row["Time"], row["Name"]])
                sorter.sort()
       #print(sorter)
        print("\n\n\t\t###########################")
        print("\t\t#\tLEADERBOARD\t  #")
        print("\t\t###########################")
        print("\n\t\tRANK\tNAME\tTIME\n")
        n=0
        for a in sorter:
            n += 1
            print("\t\t{}\t{}\t{}".format(n, a[1], a[0]))

        choice = input("\nContinue to Main Menu? (y/n) :")
        match = re.search(r"^[yYnN]", choice)
        if match is not None:
            if choice == 'y' or choice == 'Y':
                homepage()
        else:
            exit()
    except Exception as e:
        print(e)
        traceback.print_exc()

        input("\nContinue to Main Menu? (y/n) :")
        



def main():
   homepage()

if __name__=="__main__":
   
#    try:
 #       f = os.open('tab.txt', os.O_WRONLY|os.O_CREAT)
  #      print("File opened")
   #     os.close(f)
    #except Exception as e:
     #   print(e)
      #  traceback.print_exc()
     #   w.write("new")
    main()