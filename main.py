""" Flexible Job Shop Scheduling Problem solved with Genetic Algorithms (C) Raducanu Tiberiu """

import random
import numpy as np

OS = [1,3,1,2,2,3]
MS = [2,1,3,1,2,3]

op_times = [[5, 4, 4], [4, 2, 3], [2, 2, 1], [3, 4, 3], [5, 4, 5], [2, 9, 2]]

OS_P1 = [1, 1, 2, 2, 3, 3]
OS_P2 = [2, 3, 1, 3, 1, 2]
MS_P1 = [2, 1, 3, 1, 2, 2]
MS_P2 = [1, 3, 2, 3, 3, 1]

def DecodeChromosomes(nb_jobs, nb_machines, nb_op, OS, MS, op_times):
    job_start_time = [0] * nb_jobs   # the time when you can start a new job from a specific category
    machine_start_time = [0] * nb_machines # the time when a machine becomes available
    current_op = [0] * nb_jobs # the current opperation for each job
    sol = [[]] * nb_machines
    lately = 0
    #print(sol)

    for n_job in OS:
        job = n_job - 1
        op = current_op[job]
        
        #todo each job may have different number of operations
        ms_pos = nb_op * job + op
        machine = MS[ms_pos] - 1
        time = max(job_start_time[job], machine_start_time[machine])
        j_t = op_times[nb_op * job + op][machine]

        for i in range(machine_start_time[machine], time):
            sol[machine] = sol[machine] + [0]

        #todo must also check available slots 
        # k > machine_start_time[machine]
        # sol[k][machine] == [0], ... sol[k + j_t - 1][machine] == [0]
            
            
        for i in range(time, time + j_t):
            sol[machine] = sol[machine] + ['J{}'.format((job + 1) * 10 + current_op[job] + 1)]

        """
        print("Op:", op + 1, "Job:", job + 1, "Machine:", machine + 1)
        print(sol[0])
        print(sol[1])
        print(sol[2])
        print("*******")
        """

        machine_start_time[machine] = len(sol[machine])
        job_start_time[job] = len(sol[machine])
        current_op[job] += 1

    for machine in range(nb_machines):
        lately = max(lately, len(sol[machine]))

    return (lately, sol)

def OS_Crossover(OS_P1, OS_P2):
    n = len(OS_P1)
    cross_boundary = n // 2 - 1

    OS_C1 = [0] * n
    OS_C2 = [0] * n

    for i in range(n):
        if(OS_P1[i] < cross_boundary):
            OS_C1[i] = OS_P1[i]

        if (OS_P2[i]  < cross_boundary):
            OS_C2[i] = OS_P2[i]

    index = 0
    for i in range(n):
        if(OS_P2[i] >= cross_boundary):
            while OS_C1[index] != 0:
                index += 1
            OS_C1[index] = OS_P2[i]

    index = 0
    for i in range(n):
        if (OS_P1[i] >= cross_boundary):
            while OS_C2[index] != 0:
                index += 1
            OS_C2[index] = OS_P1[i]

    return OS_C1, OS_C2


def MS_Crossover(MS_P1, MS_P2):
    n = len(MS_P1)
    cross_boundary = n // 2

    MS_C1 = [0] * n
    MS_C2 = [0] * n

    for i in range(n):
        if i < cross_boundary:
            MS_C1[i] = MS_P1[i]
            MS_C2[i] = MS_P2[i]
        else:
            MS_C1[i] = MS_P2[i]
            MS_C2[i] = MS_P1[i]

    return MS_C1, MS_C2


def OS_Mutation(OS_c, pos):
    OS = OS_c.copy()
    n = len(OS)

    found = pos
    while found == pos or OS[pos] == OS[found]:
        found = random.randrange(n)

    OS[pos], OS[found] = OS[found], OS[pos]
    return OS

def MS_Mutation(MS_c, pos):
    MS = MS_c.copy()
    n = len(MS)

    found = pos
    while found == pos or OS[pos] == OS[found]:
        found = random.randrange(n)

    MS[pos], MS[found] = MS[found], MS[pos]
    return MS


"""
end_time, rez = DecodeChromosomes(3, 3, 2, OS, MS, op_times)
for i in range(3):
    print(rez[i])
print(end_time)

c1, c2 = OS_Crossover(OS_P1, OS_P2)
print(c1)
print(c2)

m1, m2 = MS_Crossover(MS_P1, MS_P2)
print(m1)
print(m2)

O1 = OS_Mutation(OS_P1, 4)
print(O1)

M1 = MS_Mutation(MS_P1, 4)
print(M1)
"""


def genetics():
    population_length = 20
    ephocs = 100
    cross_rate = 30
    mutation_rate = 3
    op_times = [[5, 4, 4], [4, 2, 3], [2, 2, 1], [3, 4, 3], [5, 4, 5], [2, 9, 2]]
    n_jobs = 3
    n_machines = 3
    n_op = 2

    chroms = []

    print("\n\n\nStarting to populate the first epoch: \n****************************")
    for i in range(population_length):
        OS = []
        for i in range(n_jobs):
            OS = OS + [i + 1] * n_op
        random.shuffle(OS)

        MS = []
        
        #todo each operation has a different list of available machines
        # op_time = [[5,math.inf, 7],[math.inf, 3, 4], ... ]
        # o_1_1 available machines 1 and 3, o_1_2 available machines 2 and 3
        for i in range(n_jobs * n_op):
            nr = random.randrange(3) + 1
            MS = MS + [nr]

        #print((OS,MS))
        chroms.append((OS,MS))



    minTime = 1000000
    best_gene = ()

    for ephoc in range(ephocs):
        print("Ephoc {}:".format(ephoc + 1))


        """ Roulete wheel selection """

        total_time = 0.0
        interval = [0]

        for (OS, MS) in chroms: # compute total time
            time, _ = DecodeChromosomes(n_jobs, n_machines, n_op, OS, MS, op_times)
            time = 1 / time
            total_time += time

        for (OS, MS) in chroms: # set intervals
            time, _ = DecodeChromosomes(n_jobs, n_machines, n_op, OS, MS, op_times)
            time = 1 / time
            prob = time / total_time
            interval = interval + [interval[-1] + prob]
            #print(interval[-1])

        #### Selection
        cnt = 0

        selected = []
        for i in range(population_length):
            nr = random.uniform(0,1)

            for i in range(len(interval) - 1):
                if interval[i] < nr and nr < interval[i + 1]:
                    break

            selected.append(i)

        #print(selected)

        """ Crossover """

        prev = 0
        paired = 0
        crossed = []

        for i in range(population_length):
            nr = random.randrange(100)

            if nr < cross_rate:
                paired ^= 1

                if(paired == 0):
                    OS1, MS1 = chroms[selected[prev]]
                    OS2, MS2 = chroms[selected[i]]

                    OS_C1, OS_C2 = OS_Crossover(OS1, OS2)
                    MS_C1, MS_C2 = MS_Crossover(MS1, MS2)

                    crossed.append((OS_C1, MS_C1))
                    crossed.append((OS_C2, MS_C2))

                prev = i

            else:
                crossed.append(chroms[selected[i]])

        if paired == 1:
            crossed.append(chroms[selected[prev]])


        """ Mutation """

        mutated = []

        for i in range(population_length):
            OS, MS = crossed[i]

            OS_nr = random.randrange(100)
            MS_nr = random.randrange(100)

            if(OS_nr < mutation_rate):
                OS_pos = random.randrange(len(OS))
                OS = OS_Mutation(OS, OS_pos)

            if (MS_nr < mutation_rate):
                MS_pos = random.randrange(len(MS))
                MS = MS_Mutation(MS, MS_pos)

            mutated.append((OS,MS))

        chroms = mutated
        #print(np.shape(chroms))

        """ Compute Maximum """

        ep_min_time = 10000000000000
        best_sol = ()

        for i in range(population_length):
            OS, MS = chroms[i]
            time, _ = DecodeChromosomes(n_jobs, n_machines, n_op, OS, MS, op_times)
            if time < ep_min_time:
                ep_min_time = time
                best_sol = (OS, MS)

        OS, MS = best_sol
        time , rez = DecodeChromosomes(n_jobs, n_machines, n_op, OS, MS, op_times)

        print("Best time is {}".format(time))
        print("Decoding Gant Chartt:")
        for i in range(n_machines):
            print(rez[i])

        print()

genetics()
