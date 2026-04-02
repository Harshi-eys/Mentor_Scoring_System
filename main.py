import csv
import math

def readf(file):
    with open(file,'r') as f:
        return list(csv.DictReader(f))

mentor=readf('mentors.csv')
mentees=readf('students.csv')
inter=readf('interactions.csv')
feedback=readf('feedbacks.csv')

ment_pro={}
for m in mentor:
    ment_pro.update({m['MentorID']:m['Projects'].split(',')})

pro_stud={}
for s in mentees:
    pro=s['ProjectID']
    if pro not in pro_stud:
        pro_stud[pro]=[]
    pro_stud[pro].append(s['StudentID'])

mentor_tee={}
for m,p in ment_pro.items():
    mentor_tee[m]=[]
    for i in p:
        if i in pro_stud:
            mentor_tee[m].extend(pro_stud[i])

def P(m):
    stud=mentor_tee[m]
    mile_comp=0
    mile_tot=0
    for i in stud:
        for j in mentees:
            if j['StudentID']==i:
                mile_comp+=int(j['MilestonesCompleted'])
                mile_tot+=int(j['TotalMilestones'])
                break
    if mile_tot==0:
        return 0
    return mile_comp/mile_tot

def R(m):
    time_tot=0
    n=0
    for i in inter:
        if i['MentorID']==m:
            time_tot+=float(i['AvgResponseTime'])
            n+=1
    if n==0:
        return 0
    t_avg=time_tot/n
    return math.exp(-t_avg/4)

def E(m):
    meet=0
    rev=0
    msg=0
    n=0
    for i in inter:
        if i['MentorID']==m:
            meet+=int(i['Meetings'])
            rev+=int(i['CodeReviews'])
            msg+=int(i['Messages'])
            n+=1
    if n==0:
        return 0
    meet_avg=meet/n
    rev_avg=rev/n
    msg_avg=msg/n
    meet_norm=min(meet_avg/5,1)
    rev_norm=min(rev_avg/5,1)
    msg_norm=min(msg_avg/15,1)
    return 0.35*meet_norm + 0.35*rev_norm + 0.3*msg_norm

def F(m):
    feed=0
    n=0
    for i in feedback:
        if i['MentorID']==m:
            feed+=min(4.5,max(int(i['Rating']),1.5))
            n+=1
    if n==0:
        return 0
    return (feed/(5*n))

def M(m):
    return 0.27*P(m) + 0.25*R(m) + 0.32*E(m) + 0.16*F(m)    

def score_time(curr,prev,alpha=0.7):
    return round(alpha*curr + (1-alpha)*prev,5)

def decay(curr,weeks,d=0.9):
    if weeks>=2:
        return round(curr*(1-d),5)
    return curr

ment_score=[]
n=1
for m in sorted(mentor, key=lambda m: M(m['MentorID']), reverse=True):
    ment_score.append(({'MentorID':m['MentorID'],'Name':m['Name'],'Final Mentor Score':round(M(m['MentorID']),5),'Rank':n}))
    n+=1

for i in range(len(ment_score)):
    if i > 0 :
        if M(ment_score[i]['MentorID']) == M(ment_score[(i-1)]['MentorID']):
            ment_score[i]['Rank'] =ment_score[(i-1)]['Rank']

with open('mentor_scores.csv','w') as f:
    f_name = ['MentorID', 'Name', 'Final Mentor Score', 'Rank']
    writer = csv.DictWriter(f, fieldnames=f_name)
    writer.writeheader()
    writer.writerows(ment_score)
