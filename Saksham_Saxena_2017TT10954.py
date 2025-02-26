#!/usr/bin/env python
# coding: utf-8

# In[8]:


import matplotlib.pyplot as plt
import math
strain = [0.001*x for x in range(1,301)]
modulus = []
beta = [0,10,20,30,40,50,60,70,80]
phi = [0.0693, 0.1360, 0.1360, 0.1226 , 0.1146, 0.1054, 0.0974, 0.0920, 0.0880]
cos_sq = [math.cos(i*(math.pi)/180)**2 for i in beta]
for i in strain:
    ef = [x*i*100 for x in cos_sq]
    qf = [5.25*i for i in ef]
    qf_cos_sq = [i*j for i,j in zip(qf,cos_sq)]
    qf_cos_sq_phi = [i*j for i,j in zip(qf_cos_sq,phi)]
    net = sum(qf_cos_sq_phi)
    modulus.append(net)

plt.plot(strain, modulus)
plt.xlabel('Strain')
plt.ylabel('Stress')
plt.show()


# In[9]:


import matplotlib.pyplot as plt
import math
strain = [0.001*x for x in range(1,301)]
modulus = []
vf=0.1
beta = [0,10,20,30,40,50,60,70,80]
phi = [0.0693, 0.1360, 0.1360, 0.1226 , 0.1146, 0.1054, 0.0974, 0.0920, 0.0880]
cos_sq = [math.cos(i*(math.pi)/180)**2 for i in beta]
for i in strain:
    ef = [x*i*100*vf for x in cos_sq]
    qf = [5.25*i for i in ef]
    qf_cos_sq = [i*j for i,j in zip(qf,cos_sq)]
    qf_cos_sq_phi = [i*j for i,j in zip(qf_cos_sq,phi)]
    net = sum(qf_cos_sq_phi)
    modulus.append(net)

plt.plot(strain, modulus)
plt.xlabel('Strain')
plt.ylabel('Stress')
plt.show()


# In[ ]:




