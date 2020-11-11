# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 23:06:31 2020

@author: jpsil
"""


from matplotlib.pylab import *
from matplotlib import cm
import os
from calor_de_hidratacion import Calor_de_hidratacion
import datetime as dt
from numpy import *


time_format = "%d-%m-%y %H:%M:%S"

fname = 'caso_1_camara_de_curado.csv' #Caso 1: Camara de curado

archivo = open(fname) 

sensores=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

tiempo = []
primer_paso = True
contador = 0
for linea in archivo:
    lin = linea.split(',')
    sens = 0
    dia = lin[0]
    hora = lin[1]

    if primer_paso:
        t1 = dt.datetime.strptime(dia+" "+hora,time_format)
        primer_paso = False
    t2 = dt.datetime.strptime(dia+" "+hora,time_format)
    t = (t2 - t1).total_seconds()

    print(f"{dia} {hora} -->  t1 = {t1} t2 = {t2} dt = {t}")

    tiempo.append(t)

    for i in [3,5,7,9,11,13,15,17,19,21,23,25,27,29,31]:
        if i ==31:
            sensores[sens].append(float(lin[i][:-1]))
            sens+=1
        else:
            sensores[sens].append(float(lin[i]))
            sens+=1
    contador+=1  
    if contador == 2880:
        break
# Funcion

def imshowbien(u,Nx,Ny,Nz,coords,plano):
          
    
    xTicks_N=arange(0,Nx+1,3)
    yTicks_N=arange(0,Ny+1,3)
    zTicks_N=arange(0,Nz+1,3)
    
    if plano == "xy":
        
        xlabel('b')
        ylabel('a')
        imshow(u[:,::-1,Nz//2].T,cmap=cm.coolwarm, interpolation='bilinear')
        cbar=colorbar(extend='both', cmap=cm.coolwarm)
        ticks=arange(0,35,5)
        ticks_Text=["{}°".format(deg) for deg in ticks]
        cbar.set_ticks(ticks)
        cbar.set_ticklabels(ticks_Text)
        clim(0,30)
        xTicks=[coords(j,0,0)[0] for j in xTicks_N]
        yTicks=[coords(0,j,0)[1] for j in yTicks_N]
        suptitle("Plano X-Y en el centro del bloque")
        xTicks_Text=["{0:.2f}".format(tick) for tick in xTicks]
        yTicks_Text=["{0:.2f}".format(tick) for tick in yTicks]
        xticks(xTicks_N,xTicks_Text,rotation='vertical')
        yticks(yTicks_N,yTicks_Text)
        margins(0.2)
        subplots_adjust(bottom=0.15)
        
    if plano == "xz":
        
        xlabel('c')
        ylabel('b')
        imshow(u[:,Ny//2,:],cmap=cm.coolwarm, interpolation='bilinear')
        cbar=colorbar(extend='both', cmap=cm.coolwarm)
        ticks=arange(0,35,5)
        ticks_Text=["{}°".format(deg) for deg in ticks]
        cbar.set_ticks(ticks)
        cbar.set_ticklabels(ticks_Text)
        clim(0,30)
        xTicks=[coords(j,0,0)[0] for j in xTicks_N]
        zTicks=[coords(0,0,j)[2] for j in zTicks_N]
        suptitle("Plano X-Z en el centro del bloque")
        xTicks_Text=["{0:.2f}".format(tick) for tick in xTicks]
        zTicks_Text=["{0:.2f}".format(tick) for tick in zTicks]
        yticks(xTicks_N,xTicks_Text,rotation='vertical')
        xticks(zTicks_N,zTicks_Text)
        margins(0.2)
        subplots_adjust(bottom=0.15)
        
    if plano == "yz":
        
        xlabel('c')
        ylabel('a')
        imshow(u[Nx//2,::-1,:],cmap=cm.coolwarm, interpolation='bilinear')
        cbar=colorbar(extend='both', cmap=cm.coolwarm)
        ticks=arange(0,35,5)
        ticks_Text=["{}°".format(deg) for deg in ticks]
        cbar.set_ticks(ticks)
        cbar.set_ticklabels(ticks_Text)
        clim(0,30)
        yTicks=[coords(0,j,0)[1] for j in yTicks_N]
        zTicks=[coords(0,0,j)[2] for j in zTicks_N]
        suptitle("Plano Y-Z en el centro del bloque")
        yTicks_Text=["{0:.2f}".format(tick) for tick in yTicks]
        zTicks_Text=["{0:.2f}".format(tick) for tick in zTicks]
        yticks(yTicks_N,yTicks_Text,rotation='vertical')
        xticks(zTicks_N,zTicks_Text)
        margins(0.2)
        subplots_adjust(bottom=0.15)

def truncate(n,decimals=0):
    multiplier=10**decimals
    return int(n*multiplier)/multiplier

"""
HACER UNA FUNCION; ASI ES MAS FACIL DE EXPLICAR EN EL INFORME
"""
def temperatura_hormigon(a,b,c,Nx,Ny,Nz,Temperatura_inicial,T_S,T_IZ,T_IN,T_D,T_F,T_P,G_S,G_IZ,G_IN,G_D,G_F,G_P,Titulo_carpeta_1,Titulo_carpeta_2,Titulo_carpeta_3,Grafico):
    
    # Crea una carpeta para que sea más facil corregir, todos los frame del caso n estaran en la carpeta n
    os.mkdir(Titulo_carpeta_1)
    os.mkdir(Titulo_carpeta_2)
    os.mkdir(Titulo_carpeta_3)
    os.mkdir("Graficos_E7")
    # Definimos geometria
    
    
    dx = b/Nx # Discretización
    dy = a/Ny
    dz = c/Nz
    h=dx
    # Importante
    
    # Funcion de conveniencia para calcular las coordenadas depunto (i,j)
    coords = lambda i,j,k:(dx*i,dy*j,dz*k)
    """
    def coords(i,j):
        return dx*i,dy*j
    """
    # x,y=coords(4,2)
    
    # print(f"x: {x}")
    # print(f"y: {y}")
    
      
        
        
        
        
    
    u_k = zeros((Nx+1,Ny+1,Nz+1), dtype=double) #dtype es el tipo de dato
    u_km1 = zeros((Nx+1,Ny+1,Nz+1), dtype=double) #dtype es el tipo de dato
    
    # Condición de borde inicial
    u_k[:,:,:]=Temperatura_inicial # 20 grados en todas partes
    
    
    # Parametros del problema (hormigon)
    dt=0.01 # s
    K=0.0014958333 #kJ/mC°s
    c=1.023 #kJ/kg*C
    rho=2476. #kg/m^3
    alpha=K*dt/(c*rho*dx**2)
    
    # Informar cosas interesantes
    
    # Loop en el tiempo
    minuto=60.
    hora=3600.
    dia=24*3600.
    
    dt=1*minuto
    dnext_t=0.5*hora
    
    next_t=0
    framenum=0
    
    T=1*dia
    Days=2*T # Cuantos dias quiero simular
    
    # Vectores para acumular la temperatura en puntos interesantes
    P1 = zeros(int32(Days/dt))
    P2 = zeros(int32(Days/dt))
    P3 = zeros(int32(Days/dt))
    P4 = zeros(int32(Days/dt))
    P5 = zeros(int32(Days/dt))
    P6 = zeros(int32(Days/dt))
    P7 = zeros(int32(Days/dt))
    P8 = zeros(int32(Days/dt))
    P9 = zeros(int32(Days/dt))
    P10 = zeros(int32(Days/dt))
    P11 = zeros(int32(Days/dt))
    P12 = zeros(int32(Days/dt))
    P13 = zeros(int32(Days/dt))
    superficie = zeros(int32(Days/dt))
    
    
    
    
    
    # Loop en el tiempo
    for k in range(int32(Days/dt)):
        t = dt*(k+1)
        
        u_ambiente = sensores[T_S][k]
        
        dias = truncate(t/dia,0)
        horas = truncate((t-dias*dia)/hora,0)
        minutos = truncate((t-dias*dia-horas*hora)/minuto,0)
        titulo = "k = {0:05.0f}".format(k)+ "t = {0:02.0f}d {1:02.0f}h {2:02.0f}m".format(dias,horas,minutos)

        print(t)
        
        
        #CB esenciales, se repiten en cada iteración
        # gradiente=5.
        # u_k[0,:]=10. #Borde izquierdo.
        # u_k[:,0]=0. #Borde inferior.
        # u_k[:,-1]=u_k[:,-2]-0*dy #Borde superior
        # # (f(x+dx)-f(x))/dx = algo
        # # (u_k[-1,:]-u_k[-2,:])/dx=-10 #gradiente del lado derecho
        
        # u_k[-1,:]=u_k[-2,:]-gradiente*dx #Borde derecho, gradiente = -10
        
        # SUPERIOR
        if T_S!="@":
            u_k[:,-1,:]=u_ambiente
        else:
            u_k[:,-1,:]=u_k[:,-2,:]-G_S*dy #Borde superior
        # IZQUIERDO
        if T_IZ!="@":
            u_k[:,:,0]=T_IZ #Borde izquierdo.
        else:
            u_k[:,:,0]=u_k[:,:,-2]-G_IZ*dx
        # INFERIOR
        if T_IN!="@":
            u_k[:,0,:]=T_IN
        else:
            u_k[:,0,:]=u_k[:,-2,:]-G_IN*dy #Borde inferior
        # DERECHO
        if T_D!="@":
            u_k[:,:,-1]=T_D #Borde derecho.
        else:
            u_k[:,:,-1]=u_k[:,:,-2]-G_D*dx
        # FRONTAL
        if T_F!="@":
            u_k[0,:,:]=T_F #cara frontal
        else:
            u_k[0,:,:]=u_k[-2,:,:]-G_F*dx
        # POSTERIOR
        if T_P!="@":
            u_k[-1,:,:]=T_F #cara posterior.
        else:
            u_k[-1,:,:]=u_k[-2,:,:]-G_P*dx
            
        
        
        # Loop en el espacio i=1...
        for i in range(1,Nx):
            for j in range(1,Ny):
                for l in range (1,Nz):
                    # Algoritmo de diferencias finitas 2-D para difusión
                
                    # Laplaciano
                    nabla_u_k=(u_k[i-1,j,l] + u_k[i+1,j,l] + u_k[i,j-1,l] + u_k[i,j+1,l] + u_k[i,j,l+1] + u_k[i,j,l-1] - 6*u_k[i,j,l])
                
                    #Forward Euler
                    u_km1[i,j,l] = u_k[i,j,l]+alpha*nabla_u_k*1000 + Calor_de_hidratacion(t)*dt/2000 #ojo que el (t) del calor de hidratacion tiene que ir en segundos y ademas las unidades de hidratacion estan en kJ/m^3*s asi que ojo con el kJ, 
        
        # Avanza la solución a k+1
        u_k=u_km1
        
        # # CB de nuevo, para asegurar cumplimiento
        # gradiente=5.
        # u_k[0,:]=10. #Borde izquierdo.
        # u_k[:,0]=0. #Borde inferior.
        # u_k[:,-1]=u_k[:,-2]-0*dy #Borde superior
        # # (f(x+dx)-f(x))/dx = algo
        # # (u_k[-1,:]-u_k[-2,:])/dx=-10 #gradiente del lado derecho
        
        # u_k[-1,:]=u_k[-2,:]-gradiente*dx #Borde derecho, gradiente = -10
        
        
        # SUPERIOR
        if T_S!="@":
            u_k[:,-1,:]=u_ambiente
        else:
            u_k[:,-1,:]=u_k[:,-2,:]-G_S*dy #Borde superior
        # IZQUIERDO
        if T_IZ!="@":
            u_k[:,:,0]=T_IZ #Borde izquierdo.
        else:
            u_k[:,:,0]=u_k[:,:,-2]-G_IZ*dx
        # INFERIOR
        if T_IN!="@":
            u_k[:,0,:]=T_IN
        else:
            u_k[:,0,:]=u_k[:,-2,:]-G_IN*dy #Borde inferior
        # DERECHO
        if T_D!="@":
            u_k[:,:,-1]=T_D #Borde derecho.
        else:
            u_k[:,:,-1]=u_k[:,:,-2]-G_D*dx
        # FRONTAL
        if T_F!="@":
            u_k[0,:,:]=T_F #cara frontal
        else:
            u_k[0,:,:]=u_k[-2,:,:]-G_F*dx
        # POSTERIOR
        if T_P!="@":
            u_k[-1,:,:]=T_F #cara posterior.
        else:
            u_k[-1,:,:]=u_k[-2,:,:]-G_P*dx
            
        
        
        # Posiciones de los medidores de temperatura
        # superficie[k] = u_k[int(Nx/2),-1,0]
        # P1[k] = u_k[int(Nx/2),int(Ny/2),0]
        # P2[k] = u_k[int(Nx/2),int(3*Ny/4),0]
        # P3[k] = u_k[int(3*Nx/4),int(3*Ny/4),0]
        # Posiciones de los medidores de temperatura
        superficie[k] = u_k[int(Nx/2),int(Ny/2),-1]
        P1[k] = u_k[int(Nx/2),int(Ny/2),int(1*Nz/4)]
        P2[k] = u_k[int(Nx/2),int(Ny/2),0]
        P3[k] = u_k[int(Nx/2),0,int(Nz/2)]
        P4[k] = u_k[int(Nx/2),int(Ny/4),int(Nz/2)]
        P5[k] = u_k[int(Nx/2),int(Ny/2),int(Nz/2)]
        P6[k] = u_k[int(Nx/2),int(3*Ny/4),int(Nz/2)]
        P7[k] = u_k[int(Nx/2),int(4*Ny/4),int(Nz/2)]
        P8[k] = u_k[int(Nx/2),int(Ny/2),int(3*Nz/4)]
        P9[k] = u_k[int(Nx/2),int(Ny/2),-1]
        P10[k] = u_k[-1,int(Ny/2),int(Nz/2)]
        P11[k] = u_k[int(3*Nx/4),int(Ny/2),int(Nz/2)]
        P12[k] = u_k[int(1*Nx/4),int(Ny/2),int(Nz/2)]
        P13[k] = u_k[0,int(Ny/2),int(Nz/2)]

        
        
        #Grafico en d_next
        if t>=next_t:
            figure(1)
            imshowbien(u_k,Nx,Ny,Nz,coords,"xy")
            title(titulo)
            savefig(Titulo_carpeta_1+"/frame_{0:04.0f}.png".format(framenum))
            figure(2)
            imshowbien(u_k,Nx,Ny,Nz,coords,"xz")
            title(titulo)
            savefig(Titulo_carpeta_2+"/frame_{0:04.0f}.png".format(framenum))
            figure(3)
            imshowbien(u_k,Nx,Ny,Nz,coords,"yz")
            title(titulo)
            savefig(Titulo_carpeta_3+"/frame_{0:04.0f}.png".format(framenum))
            
            # la carpeta tiene que existir
            framenum+=1
            next_t+=dnext_t
            close(1)
            close(2)
            close(3)
    
    # Ploteo historia de temperaturas en los puntos de interes
    figure(4)
    plot(range(int32(Days/dt)), superficie, label='superficie',color='k',linestyle='--')
    plot(range(int32(Days/dt)), P1, label='P1')
    plot(range(int32(Days/dt)), P2, label='P2')
    plot(range(int32(Days/dt)), P3, label='P3')
    plot(range(int32(Days/dt)), P4, label='P4')
    plot(range(int32(Days/dt)), P5, label='P5')
    plot(range(int32(Days/dt)), P6, label='P6')
    plot(range(int32(Days/dt)), P7, label='P7')
    plot(range(int32(Days/dt)), P8, label='P8')
    plot(range(int32(Days/dt)), P9, label='P9')
    plot(range(int32(Days/dt)), P10, label='P10')
    plot(range(int32(Days/dt)), P11, label='P11')
    plot(range(int32(Days/dt)), P12, label='P12')
    plot(range(int32(Days/dt)), P13, label='P13')
    title("Evolucion de temperatura de sensores")
    xlabel("Tiempo [s]")
    ylabel("Temperatura [°C]")
    legend()
    savefig(f"Graficos_E7/Grafico_Evolucion_General")
    show()
    
    
    lista_pes = [P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11,P12,P13]
    
    for i in range (1,14):
        figure(i+4)
        plot(range(int32(Days/dt)), lista_pes[i-1], label=f'Sensor predicho {i}')
        plot(range(int32(Days/dt)),sensores[i-1],label=f'Sensor real {i}')
        title(f"Evolucion de temperatura de sensor {i}")
        xlabel("Tiempo [s]")
        ylabel("Temperatura [°C]")
        legend()
        savefig(f"Graficos_E7/Grafico_Sensor{i}")
        show()
        
    
    

"""
                    COSAS QUE CAMBIAR SI SE QUIERE OTRO RESULTADO O CASO
"""


# temperatura_hormigon(a,   b,    c,  Nx, Ny, Nz,Temperatura_inicial,T_S,T_IZ,T_IN,T_D,T_F,T_P, G_S, G_IZ,G_IN, G_D,G_F,G_P,Titulo_carpeta,Grafico):
temperatura_hormigon(0.5, 0.5, 1. ,15, 15,30,       20.,         -1, "@", "@", "@", "@","@", 0.,   0.,  0., 0.,   0.,  0., "Caso_XY","Caso_XZ","Caso_YZ",7)


# GIF
import glob
from PIL import Image

import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

# FRAME
fp_in = "Caso_XY/frame_*.png"
fp_out = "Caso_XY/GIF_caso_XY.gif"


listaImagenes=sorted(glob.glob(fp_in))

#print("sorted(glob.glob(fp_in)): ", listaImagenes)
listaImagenes.sort(key=natural_keys)
#print("listaImagenes: ", listaImagenes)
img, *imgs = [Image.open(f) for f in listaImagenes]
img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=150, loop=0)

fp_in = "Caso_XZ/frame_*.png"
fp_out = "Caso_XZ/GIF_caso_XZ.gif"


listaImagenes=sorted(glob.glob(fp_in))

#print("sorted(glob.glob(fp_in)): ", listaImagenes)
listaImagenes.sort(key=natural_keys)
#print("listaImagenes: ", listaImagenes)
img, *imgs = [Image.open(f) for f in listaImagenes]
img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=150, loop=0)

fp_in = "Caso_YZ/frame_*.png"
fp_out = "Caso_YZ/GIF_caso_YZ.gif"


listaImagenes=sorted(glob.glob(fp_in))

#print("sorted(glob.glob(fp_in)): ", listaImagenes)
listaImagenes.sort(key=natural_keys)
#print("listaImagenes: ", listaImagenes)
img, *imgs = [Image.open(f) for f in listaImagenes]
img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=150, loop=0)






