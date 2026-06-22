import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import os

# añadimos la base de datos de Ghia para comparación

ghia_y_u = np.array([1.0000, 0.9766, 0.9688, 0.9609, 0.9531, 0.8516, 0.7344, 0.6172, 
                     0.5000, 0.4531, 0.2813, 0.1719, 0.1016, 0.0703, 0.0625, 0.0547, 0.0000])

ghia_u = {
    100:  [1.0, 0.84123, 0.78871, 0.73722, 0.68717, 0.23151, 0.00332, -0.13641, -0.20581, -0.21090, -0.15662, -0.10150, -0.06434, -0.04775, -0.04192, -0.03717, 0.0],
    400:  [1.0, 0.75837, 0.68439, 0.61756, 0.55892, 0.29093, 0.16256, 0.02135, -0.11477, -0.17119, -0.32726, -0.24299, -0.14612, -0.10338, -0.09266, -0.08186, 0.0],
    1000: [1.0, 0.65928, 0.57492, 0.51117, 0.46604, 0.33304, 0.18719, 0.05702, -0.06080, -0.10648, -0.27805, -0.38289, -0.29730, -0.22220, -0.20196, -0.18109, 0.0],
    3200: [1.0, 0.53236, 0.48296, 0.46547, 0.46101, 0.34682, 0.19791, 0.07156, -0.04272, -0.08663, -0.24427, -0.34323, -0.41933, -0.37827, -0.35344, -0.32407, 0.0],
    5000: [1.0, 0.48223, 0.46120, 0.45992, 0.46036, 0.33556, 0.20087, 0.08183, -0.03039, -0.07404, -0.22855, -0.33050, -0.40435, -0.43643, -0.42901, -0.41165, 0.0]
}

ghia_x_v = np.array([1.0000, 0.9688, 0.9609, 0.9531, 0.9453, 0.9063, 0.8594, 0.8047, 
                     0.5000, 0.2344, 0.2266, 0.1563, 0.0938, 0.0781, 0.0703, 0.0625, 0.0000])

ghia_v = {
    100:  [0.0, -0.05906, -0.07391, -0.08864, -0.10313, -0.16914, -0.22445, -0.24533, 0.05454, 0.17527, 0.17507, 0.16077, 0.12317, 0.10890, 0.10091, 0.09233, 0.0],
    400:  [0.0, -0.12146, -0.15663, -0.19254, -0.22847, -0.23827, -0.44993, -0.38598, 0.05186, 0.30174, 0.30203, 0.28124, 0.22965, 0.20920, 0.19713, 0.18360, 0.0],
    1000: [0.0, -0.21388, -0.27669, -0.33714, -0.39188, -0.51550, -0.42665, -0.31966, 0.02526, 0.32235, 0.33075, 0.37095, 0.32627, 0.30353, 0.29012, 0.27485, 0.0],
    3200: [0.0, -0.39017, -0.47425, -0.52357, -0.54053, -0.44307, -0.37401, -0.31184, 0.00999, 0.28188, 0.29030, 0.37119, 0.42768, 0.41906, 0.40917, 0.39560, 0.0],
    5000: [0.0, -0.49774, -0.55069, -0.55408, -0.52876, -0.41442, -0.36214, -0.30018, 0.00945, 0.27280, 0.28066, 0.35368, 0.42951, 0.43648, 0.43329, 0.42447, 0.0]
}

ghia_x_w = np.array([0.0625, 0.1250, 0.1875, 0.2500, 0.3125, 0.3750, 0.4375, 0.5000, 
                     0.5625, 0.6250, 0.6875, 0.7500, 0.8125, 0.8750, 0.9375])

ghia_w = {
    100:  [40.0110, 22.5378, 16.2862, 12.7844, 10.4199, 8.69628, 7.43218, 6.57451, 6.13973, 6.18946, 6.82674, 8.22110, 10.7414, 15.6591, 30.7923],
    400:  [53.6863, 34.6351, 26.5825, 21.0985, 16.8900, 13.7040, 11.4537, 10.0545, 9.38889, 9.34599, 9.88979, 11.2018, 13.9068, 19.6859, 35.0773],
    1000: [75.5980, 51.0557, 40.5437, 32.2953, 25.4341, 20.2666, 16.8350, 14.8901, 14.0928, 14.1374, 14.8061, 16.0458, 18.3120, 23.8707, 42.1124],
    3200: [126.670, 89.3391, 75.6401, 61.7864, 47.1443, 35.8795, 28.9413, 25.3889, 24.1457, 24.4639, 25.8572, 27.9514, 30.4779, 34.2327, 49.9664],
    5000: [146.702, 103.436, 91.5682, 77.9509, 60.0065, 45.8622, 37.3609, 33.0115, 31.3793, 31.5791, 33.0486, 35.3504, 38.0436, 41.3394, 56.7091]
}

#tipografia tipo latex para las figuras del informe
plt.rcParams.update({
    "text.usetex": False,                     
    "mathtext.fontset": "cm",                 
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman", "DejaVu Serif"], 
    "font.size": 10,
    "axes.labelsize": 10,
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8
})

#separamos en regimenes viscoso e inercial y calculamos las normas con respecto a la base de datos
regimenes = {
    'Viscoso/Transicional': [100, 400, 1000],
    'Inercial': [3200, 5000]
}

marcadores = {100: 'o', 400: 's', 1000: '^', 3200: 'D', 5000: 'v'}
colores = {100: 'blue', 400: 'green', 1000: 'red', 3200: 'purple', 5000: 'orange'}

def calcular_normas(num_val, ref_val):
    """Calcula las normas L2 (global) y L_inf (máximo absoluto)."""
    num_val, ref_val = np.array(num_val), np.array(ref_val)
    
    # Tolerancia para evitar división por cero si ref_val es exactamente el vector nulo
    denom_l2 = np.sum(ref_val**2) if np.sum(ref_val**2) != 0 else 1e-16
    denom_linf = np.max(np.abs(ref_val)) if np.max(np.abs(ref_val)) != 0 else 1e-16
    
    err_L2 = np.sqrt(np.sum((num_val - ref_val)**2) / denom_l2)
    err_Linf = np.max(np.abs(num_val - ref_val)) / denom_linf
    return err_L2, err_Linf

# Iteramos sobre cada régimen y sus casos de Reynolds y generamos las figuras correspondientes

for nombre_regimen, casos_re in regimenes.items():
    # Dimensión (7.16, 3.0) pulgadas corresponde al ancho estandar de 2 columnas
    fig, axs = plt.subplots(1, 3, figsize=(7.69, 2.5), constrained_layout=True)  # Ajuste automático de layout para optimizar el espacio
    
    print(f"\n--- Análisis Cuantitativo: Régimen {nombre_regimen} ---")
    print(f"{'Re':<6} | {'L2 (u)':<10} | {'L_inf (u)':<10} | {'L2 (v)':<10} | {'L_inf (v)':<10}")
    print("-" * 65)
    
    for Re in casos_re:
        archivo = f"Datos_cavidad_Re{Re}.npz"
        if not os.path.exists(archivo):
            continue
            
        datos = np.load(archivo)
        u_final, v_final = datos['historial_u'][-1], datos['historial_v'][-1]
        
        imax, jmax = u_final.shape[0] - 1, v_final.shape[1] - 1
        Lx, Ly = 1.0, 1.0
        dx, dy = Lx / imax, Ly / jmax
        
        y_u = np.linspace(0, Ly, u_final.shape[1])
        x_v = np.linspace(0, Lx, v_final.shape[0])
        
        # Extracción colocalizada
        idx_c_x = int(imax / 2)
        u_perfil = 0.5 * (u_final[idx_c_x, :] + u_final[idx_c_x + 1, :])
        
        idx_c_y = int(jmax / 2)
        v_perfil = 0.5 * (v_final[:, idx_c_y] + v_final[:, idx_c_y + 1])
        
        # Corrección de vorticidad en la tapa
        u_tapa = 1.0
        u_interna_top = u_final[:, -2] 
        w_perfil = -2.0 * (u_tapa - u_interna_top) / dy
        w_coloc = 0.5 * (w_perfil[:-1] + w_perfil[1:])
        x_w = np.linspace(0, Lx, len(w_coloc) + 2)
        
        # Interpolación cúbica para evaluar en los nodos de Ghia
        f_u = interp1d(y_u, u_perfil, kind='cubic')
        f_v = interp1d(x_v, v_perfil, kind='cubic')
        
        u_eval = f_u(ghia_y_u)
        v_eval = f_v(ghia_x_v)
        
        # Cálculo de errores
        L2_u, Linf_u = calcular_normas(u_eval, ghia_u[Re])
        L2_v, Linf_v = calcular_normas(v_eval, ghia_v[Re])
        
        print(f"{Re:<6} | {L2_u:.4e} | {Linf_u:.4e} | {L2_v:.4e} | {Linf_v:.4e}")
        
        color, marcador = colores[Re], marcadores[Re]
        
        
        axs[0].plot(u_perfil, y_u, color=color, linestyle='-', linewidth=1.2, label=f'Num. Re={Re}')
        axs[1].plot(x_v, v_perfil, color=color, linestyle='-', linewidth=1.2, label=f'Num. Re={Re}')
        axs[2].plot(x_w[1:-1], -w_coloc, color=color, linestyle='-', linewidth=1.2, label=f'Num. Re={Re}')
        
        
        axs[0].plot(ghia_u[Re], ghia_y_u, color=color, marker=marcador, fillstyle='none', linestyle='none')
        axs[1].plot(ghia_x_v, ghia_v[Re], color=color, marker=marcador, fillstyle='none', linestyle='none')
        axs[2].plot(ghia_x_w, ghia_w[Re], color=color, marker=marcador, fillstyle='none', linestyle='none')

    for i in range(3):
        axs[i].grid(True, linestyle=':', alpha=0.7)
        if i < 3: 
            axs[i].legend(
                loc='best',          # Algoritmo de evasión de colisiones
                fontsize=7,          # Reducción estricta de fuente
                markerscale=0.7,     # Reduce el tamaño de los símbolos en la leyenda al 70%
                labelspacing=0.3,    # Comprime el interlineado vertical
                borderpad=0.3,       # Reduce el margen interno de la caja
                framealpha=0.6       # Alta transparencia para visibilizar datos de fondo
            )
    axs[0].set_title(r'$u(0.5, y)$ vs $y$')
    axs[0].set_ylabel(r'$y$')
    axs[0].set_xlabel(r'$u$')

    axs[1].set_title(r'$v(x, 0.5)$ vs $x$')
    axs[1].set_ylabel(r'$v$')
    axs[1].set_xlabel(r'$x$')

    axs[2].set_title(r'$\omega(x, 1.0)$ vs $x$')
    axs[2].set_ylabel(r'$\omega$')
    axs[2].set_xlabel(r'$x$')
    
    plt.tight_layout(pad=0.5, w_pad=1.0, h_pad=1.0)
    
    plt.savefig(f"Validacion_Regimen_{nombre_regimen.replace('/', '_')}.pdf", format='pdf', bbox_inches='tight')
    plt.show()