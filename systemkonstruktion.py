import numpy as np
import matplotlib.pyplot as plt

class hylla():
    def __init__(self, antal_hyllplan: int = 12, circ_percent: float = 10):
        self.hyllor = []
        self.antal = antal_hyllplan
        self.circ_percentage = circ_percent
        self.pos = []
        self.force_percent = []
        self.resolution = 0.01
        self.tot = []

        self.genHyllplan()
        
    # fördelar hyllplanen jämnt
    def offsett(self, forceArr, index):
        shift = int(len(forceArr)/self.antal*index)
        self.hyllor[index] = np.roll(forceArr, shift)

    # kör generatorn för kraft och poslista, sedan skapar den lista med hyllor med 
    # kraftprocentkurva som identitet. Kör sedan arrangehyllplan för att fördela hyllorna.
    def genHyllplan(self):
        self.genPosAndKraft()
        self.hyllor = [self.force_percent for i in range(self.antal)]
        self.arrangeHyllplan()

    # fördelar hyllplanen
    def arrangeHyllplan(self):
      for i in range(self.antal):
        self.offsett(self.hyllor[i], i)


    # räknar ut vikten på alla hyllplan och callar totForce
    def calcForce(self, weights: list):
        for i in range(self.antal):
            self.forceCalcIndividual(i, weights[i])
        self.totForce()
        
        
   # räknar ut den samanlagda kraften från hyllplanen och sparar i self.tot
    def totForce(self):
        tot = self.hyllor[self.antal-1]
        for i in range(self.antal-1):
            tot = np.add(tot, self.hyllor[i])
        tot.tolist()
        self.tot = tot
    
    # räknar ut vikten för enskilt hyllplan
    def forceCalcIndividual(self, index, weight: int = 10):
        self.weight = weight
        self.hyllor[index] = weight * self.hyllor[index] * 9.8
    
    # genererar en hylla, skapar positioner och motsvarande kraftprocent i dessa positioner
    def genPosAndKraft(self):
    
        lin_per = (100 - 4*self.circ_percentage)/2

        x = np.arange(0,100,self.resolution)

        x_circ = np.arange(0,self.circ_percentage,self.resolution)

        y = np.sin(x*np.pi/(self.circ_percentage*2))
        y_circ = -np.cos(x_circ*np.pi/(self.circ_percentage*2))+1
        y[x>self.circ_percentage] = np.sin(np.pi/2)

        inds = (x>=(self.circ_percentage+lin_per)) & (x<(2*self.circ_percentage+lin_per))

        y[inds] -= y_circ
        y[x>=(2*self.circ_percentage+lin_per)] = -y[0:int(len(y)/2)]
        # plt.plot(x,y)
        # plt.show()

        self.pos = x
        self.force_percent = y



    # få positionen för ett hyllplan baserat på dess index och "globala" positionen
    def getHyllPos(self, hyllIndex, pos):
        shift = int(len(self.pos)/self.antal*hyllIndex)
        return self.pos[pos+shift]

    # få kraften i en viss pos
    def getForce(self, x: float) -> float:
        x = x%100
        index = (np.abs(self.pos - x)).argmin()
        #print("Returned force:", round(self.tot[index],2), ", at", x, "% of revolution")
        return self.tot[index]

def plotter(weights):
    h = hylla(antal_hyllplan=len(weights))
    h.calcForce(weights)
    h.totForce()
  
    hyllor = h.hyllor
    totForce = h.tot
    plt.rcParams['figure.figsize'] = [12,5]
    fig, (ax1, ax2) = plt.subplots(1, 2)
  
    fig.suptitle('Horizontally stacked subplots')
  
    for i in range(len(weights)):
        ax1.plot(h.pos, h.hyllor[i])
    ax2.plot(h.pos, h.tot)
    plt.show()

def main():
    w1 = [10,2,0,0,5,6,4,8,0,1,1,1]
    h = hylla(len(w1))
    h.calcForce(w1)
    h.totForce
    
    m_tot = np.sum(w1)
    #print("hyllor: ",h.hyllor)
    #print("antal: ", h.antal)
    #print("circ_percentage: ",h.circ_percentage)
    #print("force_percent: ",h.force_percent)
    #print("resolution: ", h.resolution)
    x = h.pos
    y = h.tot
    k = 2500 #Omvandlingsfaktor (rad/m) påhittad
    d_T = h.resolution 
    t = 40
    n = round(t/d_T)
    

    v = np.zeros(n) 
    a = np.zeros(n)
    h = np.zeros(n)
    v[0] = 0 
    a[0] = 0
    h[0] = 0

    f_out = np.zeros(n)
    acc_load = np.zeros(n)
    
    acc_load[0:100] = 0.15
    acc_load[1010:1100]=-0.15
    acc_load[2010:2100]=-0.15
    acc_load[3010:3100]=0.15
    print(acc_load)
   

    for i in range(n):
        f_out[i] = y[i] + (m_tot * acc_load[i])
        #T_EM[i] = f_out[i]/k
        #w_EM[i] = v[i] * k


        if i<n-1:
            v[i+1] = v[i] + d_T * acc_load[i]
            h[i+1] = h[i] + d_T * v[i]
    plt.plot(x[0:(n-1)],v[0:(n-1)])
    plt.show()
if __name__ == "__main__":
    main()












###########STULET SKIT FRÅN MATLAB###########################
''' from sys import platform

#Init hyllsystem
w1 = [6,0,0,5,0,0,0,0,3,0,0,0]
h = hylla(len(w1))
h.calcForce(w1)
h.totForce
m_tot = np.sum(w1)



#Stulen kod från MATLAB exempel
#A_kolv=11.8*10**(-4)  # (m^2) Hydraulkolvens tvärsnittsarea
#V_pump=1.48*10**-6  # (m^3) slagvolym för hydraulpumpen
k_T=0.048  #(Nm/A), likströmsmotorns momentkonstant
k_e=k_T  # (Vs), likströmsmotorns spänningskonstant
R_EM=0.03  # (ohm), resistansen i motorns ankarlindning
T_frictEM = 0.5  #(Nm) friktionsmoment i elmotorn
eta_KraftEl = 1  # verkningsgrad för kraftelektroniken = 100%
U_Batt = 24  # (V) batterispänning (antas konstant oberoende av batteriström)

k = 2500 #Omvandlingsfaktor (rad/m) påhittad

##Exempel:
#% total omvandlingsfaktor mellan elmotorns varvtal och gaffelns hastighet:
#k1=2*pi*A_kolv/(2*V_pump) ;  % (1/m) 

d_T = h.resolution 
t = 40
n = round(t/d_T)

T_EM = np.zeros(n)
w_EM = np.zeros(n)
T_EMintern = np.zeros(n)
P_EM = np.zeros(n)
I_EM = np.zeros(n)
U_EM = np.zeros(n)
P_Batt = np.zeros(n)
I_Batt = np.zeros(n)

x = h.pos
y = h.tot

plt.plot(x[0:(n-1)], y[0:(n-1)])
plt.title("Total Force curve hyllplan")
plt.show()



v = np.zeros(n) 
a = np.zeros(n)
h = np.zeros(n)
W_Batt = np.zeros(n)
v[0] = 0 
a[0] = 0
h[0] = 0
W_Batt[0] = 0

f_out = np.zeros(n)
acc_load = np.zeros(n)
    
#Insignaler vald acceleration 
acc_load[0:10] = 0.15
acc_load[101:120]=-0.15
acc_load[201:210]=-0.15
acc_load[301:310]=0.15
  
for i in range(n):
    f_out[i] = y[i] + (m_tot * acc_load[i])
    T_EM[i] = f_out[i] / k ;
    # Glöm inte att lägga till förlusterna i växeln då ni beräknar
    # elmotorns vridmoment (här finns ingen växel.
    w_EM[i] = v[i] * k
    T_EMintern[i] = T_EM[i] + T_frictEM * np.sign(w_EM[i]) 
    #% Friktionsmomentet skall 
    # vara noll då lasten står still och negativ då de sänks
    P_EM[i] = w_EM[i] * T_EM[i]
    
    I_EM[i] = T_EMintern[i] / k_T
    U_EM[i] = w_EM[i] * k_e + R_EM * I_EM[i]
    P_Batt[i] = U_EM[i] * I_EM[i] / eta_KraftEl 
    I_Batt[i] = P_Batt[i] / U_Batt 
    
    
    if i<n-1:
      v[i+1] = v[i] + d_T * acc_load[i]
      h[i+1] = h[i] + d_T * v[i]
      W_Batt[i+1]= W_Batt[i]+ d_T * P_Batt[i]

plt.plot(x[0:(n-1)], f_out[0:(n-1)])
plt.title("F_out")
plt.show()

plt.plot(x[0:(n-1)],I_EM[0:(n-1)])
plt.title("Ström")
plt.show()

plt.plot(x[0:(n-1)],v[0:(n-1)])
plt.title("Tvingad hastighet")
plt.show()


plt.plot(x[0:(n-1)],U_EM[0:(n-1)])
plt.title("Spänning")
plt.show()''' 






