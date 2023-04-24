from pyschedule import Scenario, solvers, plotters, alt


 

# İnşa İşi
S = Scenario('Bina_insa_etme', horizon=250)


# the planning horizon has 10 periods
Hafriyat, Temel, TemelKurutma = S.Resource('Hafriyat_Kaynağı', size=3, cost_per_period=1), S.Resource('Temel_Kaynağı', size=6, cost_per_period=1), S.Resource('TemelKurutma_Kaynağı', size=3, cost_per_period=1)
Blok_Sayısı = 8

H = S.Tasks('Hafriyat', num=Blok_Sayısı ,length=7, delay_cost = 1)
H += Hafriyat

G = S.Tasks('Grobeton', num=Blok_Sayısı , length=2, delay_cost = 1)
G += Temel
S += H < G

TAI = S.Tasks('Temel_Altı_İzolasyon', num=Blok_Sayısı, length=2, delay_cost = 1)
TAI += alt(Temel)
S += G < TAI

T = S.Tasks('Temel', num=Blok_Sayısı, length=7, delay_cost = 1)
T += alt(Temel)
S += TAI < T


BK = S.Tasks('2.Bodrum_Kat', num=Blok_Sayısı, length=5, delay_cost = 1)
BK += alt(TemelKurutma)
S += T < BK 

FBK = S.Tasks('1.Bodrum_Kat',num=Blok_Sayısı, length=2, delay_cost = 1)
FBK += alt(TemelKurutma)
S += BK < FBK 

ZK = S.Tasks('Zemin_Kat', num=Blok_Sayısı, length=2, delay_cost = 1)
ZK += alt(TemelKurutma)
S += FBK < ZK

FNK = S.Tasks('1.Normal_Kat', num=Blok_Sayısı, length=2, delay_cost = 1)
FNK += alt(TemelKurutma)
S += ZK < FNK

SNK= S.Tasks('2.Normal_Kat', num=Blok_Sayısı, length=2, delay_cost = 1)
SNK += alt(TemelKurutma)
S += FNK < SNK

TNK= S.Tasks('3.Normal_Kat', num=Blok_Sayısı, length=2, delay_cost = 1)
TNK += alt(TemelKurutma)
S += SNK < TNK

FNK= S.Tasks('4.Normal_Kat', num=Blok_Sayısı, length=2, delay_cost = 1)
FNK += alt(TemelKurutma)
S += TNK < FNK




# # two resources: Alice and Bob
# Alice, Bob = S.Resource('Alice'), S.Resource('Bob', cost_per_period=1)

# # three tasks: cook, wash, and clean
# cook = S.Task('cook',length=1,delay_cost=1)
# wash = S.Task('wash',length=2,delay_cost=1)
# clean = S.Task('clean',length=3,delay_cost=2)

# # every task can be done either by Alice or Bob
# cook += Alice | Bob
# wash += Alice | Bob
# clean += Alice | Bob

# compute and print a schedule
solvers.mip.solve(S,msg=1)
print(S.solution())

plotters.matplotlib.plot(S,img_filename='household.png')