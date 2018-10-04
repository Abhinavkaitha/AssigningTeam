#!/usr/bin/env python3
#INITIAL_STATE:-
#we are starting with an initial state which contains individual memeber as a team and also its cost.

#GOAL STATE:-
#There will be multiple goal states.
#there is high chance that we might be missing the global minimum and stuck with the local minimum.(Since we have skipped some states, which is explained below)
#In our program we have colledted all the possible states with there heuristic value in CLOSED and popped the state with minimum cost as goal state.

#STATE_SPACE:-
#At any given time, the fringe will consist of possible combination of the parent state with its cost.

#We are adding  initial state to a fringe(Which is a priority queue)
#Every time we pop out an element from a priority queue, we are storing it in a CLOSED list, which contains, both the teams and their cost
#The whole group of teams(without the cost) from this popped state is passed to a successor function.

#SUCCESSOR_FUNCTION:-
#This is similar to the successor function in nrooks program
# generates the teams by combining two teams in all possible ways in the existing group of teams.
#Since a team with two members in a team will be passed in the further iterations, using the same successor function, we can generate all the possible teams

#Then we calculated the cost of each state using the heuristic function which is built based on the given conditions
#The set of teams which has cost more than its parents is eliminated. By doing this, we might miss some states. We did this inorder to reduce the size of CLOSED,
# from which we will be extracting the final optimal solution
#The successors with cost(heuristic value) less than that of parents are returned.
# From these states, the states which are not visited before are added to the CLOSED group.
#this is repeated till the list returned from successors is empty.
#Now we have all the possible states(whose heuristic less than thier parent's heuristic) stored in the CLOSED along with their cost
#Now we just pop the state with minimum cost.
#This might not be the optimal solution, since we have started from an arbitrary state and also skipped some stated to save some time and space.
import sys
from queue import PriorityQueue
def heuristic(state):
    cost=0
    team_size_cost=0
    prefer_team_cost=0
    not_prefer_team_cost=0
###### Calculating cost, if team size is different #######
    i=0
    while i <(len(state)):
        j=0
        while j <(len(state[i])):
            req_team_size=student_dict[state[i][j]][0]
            if req_team_size in [len(state[i]),0]:
                j+=1
            else:
#If the team size doesn't match the requested team size, we increase the counter by one.
                team_size_cost+=1
                j+=1
        i+=1
###### Calculating cost, if requested_team_mate is not assigned #######
    i=0

    while i <(len(state)):
        j=0
        while j <(len(state[i])):
            c=0
            l=0
            while l <(len(state[i])):
                if state[i][l] is not state[i][j]:
                    o=0
                    while o<len(student_dict[state[i][j]][1]):

                        if state[i][l] == student_dict[state[i][j]][1][o]:
# Here C counts the number of favorable team_mates of a particular student in his team
# say if there are 2 favorable team mates and size of team is 3, the he will complain(3-2) times.So, we have subtracted c from length(team)
                            c+=1
                        o+=1
                l+=1
            prefer_team_cost += len(student_dict[state[i][j]][1]) - c
            j+=1
        i+=1
###### Calculating cost, if un preferred_team_mate is assigned #######
    i=0
    while i in range(len(state)):
        j=0
        while j in range(len(state[i])):
            l=0
            while l in range(len(state[i])):
                if state[i][l] is not state[i][j]:
                    o=0
                    while o< len(student_dict[state[i][j]][2]):
                        if state[i][l] == student_dict[state[i][j]][2][o]:
#In this case its simple, if there any not preffered team mates of a particular student in his team, we increase the counter by one
                            not_prefer_team_cost+=1
                        o+=1
                l+=1
            j+=1
        i+=1
##### total cost for a particular team
    cost=(int(k)*len(state))+(team_size_cost)+(int(n)*prefer_team_cost)+(int(m)*not_prefer_team_cost)
    return cost


# In[72]:


def GenerateTeams(state):
    list5=[]
    all_teams=[]
    i=0
    while i < len(state):
        all_teams.append(state[i])
        i+=1
    i=0
#Reference: draft of nrooks program
    while i<len(all_teams)-1:
        j=i+1
        while j<len(all_teams):
            if len(state[i])+len(state[j])<=3:
                #existing_group1 or null
                existing_group1=all_teams[0:i][:]
                new_group=[all_teams[i]+all_teams[j]]
                # existing_group2 or null
                existing_group2=all_teams[i+1:j][:]
                # existing_group3 or null
                existing_group3=all_teams[j+1:][:]
                list5.append(tuple(existing_group1+new_group+existing_group2+existing_group3))
            j+=1
        i+=1
    return list5

def successors(state):
    
    successors1=GenerateTeams(state)
    
    heuristic_values=[]
    list1=[]
    i=0

    while i <(len(successors1)):
#storing the heuristic value of successeors whose, heuristic value is less than that of their parent
        if heuristic(state)>heuristic(successors1[i]):
            heuristic_values.append(heuristic(successors1[i]))
            list1.append(i)
        i+=1
#Storing the successors whose heuristic value is less than that of their parent
    list3=[]
    i=0
    while i <(len(successors1)):
        if i in list1:
            list3.append(successors1[i])
        i+=1
#Appending the heuristic value and the corresponding state
    list2=[]
    i=0
    while i <(len(list1)):

        list2.append((heuristic_values[i],list3[i]))
        i+=1
    return list2          
                


# In[74]:


def solve(initial_state):
    
    fringe1 = [initial_state]
    
    fringe_q = PriorityQueue()
    i=0
    while i <len(fringe1):
        fringe_q.put(fringe1[i])
        i+=1
        
    global CLOSED    
    CLOSED=[]
    while fringe_q.empty()==False:
        
        (cost, state) = fringe_q.get()
        
        CLOSED.append((cost,state))
        ll = successors(state)
#If successors list is empty, the program terminates
        if(len(ll)!=0):
            for (cost, succ) in ll:
                if succ not in CLOSED:
                    fringe_q.put((cost,succ))
                else:
                    continue
        else: 
            return min(CLOSED)
    return min(CLOSED)


# In[76]:


input_file=sys.argv[1]
k=sys.argv[2]
m=sys.argv[3]
n=sys.argv[4]
given_list=[]

with open(input_file) as file:
    for line in file:
        line=line.rstrip("\n")
        given_list.append(line.split())

student_dict={}
student_list=[]
team_size=[]
prefer=[]
not_prefer=[]

#storing the given information in a dictionary, so that it will be easy to retrieve the information given by each student
i=0
while i <(len(given_list)):
    student_list.append(given_list[i][0])
    team_size.append(int(given_list[i][1]))
    prefer.append(given_list[i][2].split(","))
    not_prefer.append(given_list[i][3].split(","))
    student_dict[student_list[i]]=[team_size[i],prefer[i],not_prefer[i]]
    i+=1

for key,value in student_dict.items():
    for element in value:
        for i in range(len(value[1])):
            if value[1][i] == "_":
                del(value[1][i])
        for i in range(len(value[2])):
            if value[2][i] == "_":
                del(value[2][i])

initial_state=[]
# choosing the initial state  : each student in an individual team
i=0
while i <(len(student_list)):
    initial_state.append([student_list[i]])
    i+=1
initial_state=tuple(initial_state)


optimal_teams=solve((heuristic(initial_state), initial_state))

i=0
while i <len(optimal_teams[1]):
    j=0
    while j< len(optimal_teams[1][i]):
        print(optimal_teams[1][i][j],end=" ")
        j+=1
    print("")
    i+=1
print(optimal_teams[0])
