import numpy as np
import matplotlib.pyplot as plt
import random as rnd

################################################################################################################################################

class Process:
    def __init__(self, sigma, time, price, freq):
        self.sigma = sigma
        self.time = time
        self.price = price
        self.freq = freq

################################################################################################################################################

    def rand_walk(self):
        results = []
        results.append(self.price)
        t=0
        while t < self.time:
            p = np.random.normal(results[-1],self.sigma)
            results.append(p)
            t += 1/self.freq
        return results

################################################################################################################################################

    def drift_rand(self, i):
        results = []
        results.append(self.price)
        t=0
        while t < self.time:
            p = np.random.normal(results[-1]*(1 + i/self.freq),self.sigma)
            while p < 0:
               p = np.random.normal(results[-1]*(1+i/self.freq),self.sigma)
            results.append(p)
            t += 1/self.freq
        return results

################################################################################################################################################

    def montecarlo(self, simulations, lmb_market, lmb_individual, drift):
        sim = []
        t = 0
        g = 0.2
        if drift == True:
            print("Add Drift:")
            x = float(input())/100
            depr_times = []
            for n in range(self.time):
                dpr = self.tfr(lmb_market)
                depr_times.append(dpr)
            while t < simulations:
                s = self.drift_event(x, lmb_individual, depr_times)
                sim.append(s)
                t += 1
        else:
            while t < simulations:
                s = self.rand_walk()
                sim.append(s)
                t += 1
        return np.array(sim).transpose()

################################################################################################################################################

    def drift_event(self, i, lmb, depr_times):
        results = []
        results.append(self.price)
        t=0
        st=0
        dt=0
        d=0 # crisis factor
        de = 0
        r=0.7 # recovery rate
        check=False
        n=0
        while t < self.time:
            if depr_times != None:
                if depr_times[n] < dt:
                    n+=1
                    de=0.2
                    dt=0
                    dep = self.time*self.freq
            if check == False:
                t1 = self.tfr(lmb)
                check == True
            if t1 < st:
                st=0
                check=False
                d+=0.2
            p = np.random.normal((results[-1]*(1 + i/self.freq-d-de)),self.sigma)
            #while p < 0:
            #   p = np.random.normal(results[-1]*(1+i/self.freq-d),self.sigma)
            results.append(p)
            d = d*(1-r)
            de = de*(1-r)
            st+=1/self.freq
            dt+=1/self.freq
            t += 1/self.freq
        return results

    def tfr(self, lmb):
        inst = Event(lmb)
        x = inst.get_time()
        return x

################################################################################################################################################
################################################################################################################################################

class Event:
    def __init__(self, lmb):
        self.lmb = lmb

################################################################################################################################################

    def frequency(self):
        k=1
        distr = []
        np.array(distr)
        v = 151
        while k < v:
            k += 1
            i = k
            fct = k
            while i > 1:
                i = i-1
                fct = fct*(i)
            freq = (self.lmb**(k))*(np.e**(-self.lmb))/fct
            distr.append(freq)
        return distr

################################################################################################################################################

    def cml(self):
        cml = []
        distr = self.frequency()
        for i in range(len(distr)):
            if i == 0:
                val = distr[i]
            else:
                val = distr[i] + cml[i-1]
            cml.append(val)
        return cml

################################################################################################################################################

    def rand(self):
        x = rnd.random()
        distr = self.cml()
        k = 1
        for i in range(len(distr)):
            if x > distr[i]:
                pos = i
        return pos

################################################################################################################################################

    def get_time(self):
        pos = None
        while pos == None:
            x = rnd.random()
            distr = self.cml()
            k = 1
            for i in range(len(distr)):
                if x > distr[i]:
                    fut = distr[i-1]
                    prs = distr[i]
                    if (fut-x)**2>=(prs-x)**2:
                        pos = i
                    else:
                        pos = i - 1
        return pos

################################################################################################################################################

tstE = Event(70)
plt.figure(1)
plt.plot(tstE.cml())
plt.figure(2)
plt.plot(tstE.frequency())

tstMC = Process(2,12,100,12)
tstSIM = tstMC.montecarlo(10,10,10,False)
plt.figure(3)
plt.plot(tstSIM)
