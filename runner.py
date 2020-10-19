import sys, os, time, datetime, signal , re
from enum import Enum

pidfile = "runner.pid"
statusfilename = "runner.status"
configurationfile = "runner.conf"
class Weekday(Enum):
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7 

class Struct(object):           #数据结构

    def __init__(self):
        self.week = []
        self.every = False
        self.everyday = False
        self.time = []
        self.filename = ""
        self.parame = []
        self.last_run = datetime.datetime(2020,10,19,0,0,0)
        self.next_run = datetime.datetime(2020,10,19,0,0,0)
    def dis(self):
        print(self.week,end=' ')
        print(self.every,end=' ')
        print(self.everyday,end=' ')
        print(self.time,end=' ')
        print(self.filename,end=' ')
        print(self.parame,end=' ')
        print(self.last_run,end=' ')
        print(self.next_run)

def find_nextruntime(record , date):
    yearofnow = date.year
    monthofnow = date.month
    dayofnow = date.day
    hourofnow = date.hour
    minuteofnow = date.minute
    dayofweek = date.isoweekday()  #获取今天周几
    begindate = datetime.datetime(yearofnow,monthofnow,dayofnow)
    wantdate = date
    for day in record.week:
        for time_run in record.time:  #每个时间都判断一下
            if dayofweek <= Weekday[day].value: 
                t=datetime.timedelta(days=Weekday[day].value-dayofweek,
                hours=int(time_run)//100,minutes=int(time_run)%100)
            if dayofweek > Weekday[day].value and record.every: 
                t=datetime.timedelta(days=Weekday[day].value+7-dayofweek,
                hours=int(time_run)//100,minutes=int(time_run)%100)
            tmpdate = begindate + t #计算出的运行时间
            if tmpdate > date:  #如果大于当前时间
                if wantdate == date:  #如果第一次发现
                    wantdate = tmpdate
                elif wantdate > date: #之后发现的要和want比较
                    if tmpdate < wantdate:
                        wantdate = tmpdate
    if wantdate == date:
        return -1
    elif wantdate > date:
        return wantdate

# def receive_signal(signum, stack):
#     with open(statusfilename,'w') as fin:
#         for i in run:
#             fin.write(f"{i.filename} {i.next_run}")
#             f.flush()


run_pid = os.getpid()  #将pid写入$HOME /.runner.pid
fp = open(pidfile, 'w+')
fp.write(f"{run_pid}\n")
fp.close()

# with open(statusfilename,'w') as fin:


#
# open the configuration file and read the lines,
#    check for errors

one = r"every (.*?) at"
three = r"on (.*?) at"
two = r"at (.*?) run"
count = 0
recordlist = []
try:   #读取文件
    fp =open(configurationfile,'r')
    if os.path.getsize(configurationfile) == 0:
        raise Exception("configuration file empty")
    for line in fp:
        try:
            count += 1
            record = Struct()
            line=line.strip('\n')
            print(line)
            if line.startswith("every") or line.startswith("on"):
                if line.startswith("every"):
                    record.every = True
                    week = re.findall(one, line) #on  at
                elif line.startswith("on"):
                    week = re.findall(three, line) #on  at

                weekd = week[0].split(',')
                for i in weekd:
                    if i in Weekday.__members__:
                        record.week.append(i)
                    else:
                        raise Exception("error in configuration:")

                time = re.findall(two, line) #at  run
                timed = time[0].split(',')
                for i in timed:
                    if re.match("([0-1][0-9]|[2][0-3])[0-5][0-9]",i):
                        record.time.append(i)
                    else:
                        raise Exception("error in configuration:")         
                f = line.split("run ") #run  ..
                filepa = f[1].split(' ')
                record.filename = filepa[0]
                filepa.pop(0)
                for i in filepa:
                    record.parame.append(i)
            elif line.startswith("at"):
                record.everyday = True
                record.every = True
                for i in range(7):
                    record.week.append(Weekday(i+1).name)
                time = re.findall(two, line) #at  run
                timed = time[0].split(',')
                for i in timed:
                    if re.match("([0-1][0-9]|[2][0-3])[0-5][0-9]",i):
                        record.time.append(i)
                    else:
                        raise Exception("error in configuration:")
                
                f = line.split("run ")
                filepa = f[1].split(' ')
                record.filename = filepa[0]
                filepa.pop(0)
                for i in filepa:
                    record.parame.append(i)
            else:
                raise Exception("error in configuration:")
            recordlist.append(record)
        except Exception as e: 
            print(f"{e} +{count}")
        finally:
            continue
except IOError:
    print("configuration file not found")
    fp =open(statusfilename,'w')
except Exception as e: 
    print(e)
finally:
    fp.close()


run = []
date = datetime.datetime.now()
for i in recordlist: #每条数据判断一下  
    wantdate = find_nextruntime(i , date)
    if wantdate != -1:
        i.next_run = wantdate
        run.append(i)
run.sort(key=lambda x:x.next_run)

command = run[2].filename
for i in run[2].parame:
    command += ' '+ i
os.system(command)
for i in run:
    i.dis()

with open(statusfilename,'w') as fin:
    for i in run:
        fin.write(f"{i.filename} {i.next_run}\n")
        fin.flush()

command = run[2].filename
for i in run[2].parame:
    command += ' '+ i
print(command)
os.system(command)
# build a list of "run" records that specifies a time and program to run
#
#
# define up the function to catch the USR1 signal and print run records

#注册处理信号的事件，此处对用户定义信号1、用户定义信号2，绑定事件
# signal.signal(signal.SIGUSR1, receive_signal)
# #
# sort run records by time
# take the next record off the list and wait for the time, then run the program
# add a record to the "result" list
# if this was an "every" record", add an adjusted record to the "run" list 
#
# repeat until no more to records on the "run" list, then exit
#
# fp = open(status_file,"w") #检查statusfile是否存在
# fp.close()
# try:
#     fin = open(configuefile)
# except Exception as e:
#     print("configuration file not found")
# signal.signal(signal.SIGUSR1, receive_signal)
# ans = []
# with open(filename) as fin:  #打开文件
#     for line in fin:
#       ans.append(line.strip())
# if __name__ == '__main__':
#     if len(sys.argv) != 2:
#         ip_address =  '18.216.173.39'#'localhost' '18.216.173.39'
#     else:
#         ip_address = sys.argv[1]
#     if re.match("[A-Z][a-z]* ?([A-Z][a-z]*)?",message):  #