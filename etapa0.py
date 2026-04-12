# CÉSAR VIDAL FERNÁNDEZ.

# ----------------------
# --- IMPORTACIONES ---
# ----------------------

import numpy as np
import taichi as ti
# import matplotlib.pyplot as plt


# -------------------------------
# --- INICIALIACIÓN DE TAICHI ---
# -------------------------------

arch = ti.vulkan if ti._lib.core.with_vulkan() else ti.vulkan
ti.init(arch=arch)


# --------------------------------
# --- INICIALIZACIÓN DE PLANOS ---
# --------------------------------

# Puntos en el plano.
class FieldPair:
    def __init__(self, current_field, next_field):
        self.cur = current_field
        self.nxt = next_field

    def swap(self):
        self.cur, self.nxt = self.nxt, self.cur


# -----------------------------------
# --- PARÁMETROS DE LA SIMULACIÓN ---
# -----------------------------------

# Resolución del grid
res = 512  

# Tamaño de la celda
h = 1 / res 

# Tamaño del paso de tiempo
dt = 0.03 

# Cantidad de iteraciones de la difusión para cada step.
DIFFUSION_STEPS = 100
FIELD_SPEED = 15


# --------------------------
# --- PARÁMETROS FÍSICOS ---
# --------------------------

# Constante de difusión.
kappa = 0.0001


# -------------------------------------------
# --- PARÁMETROS DE LA FUENTE DE DENSIDAD ---
# -------------------------------------------

s_dens = 10.0
s_radius = res / 15.0


# ----------------------------
# --- ESTRUCTURAS DE DATOS ---
# ----------------------------

# Campos de densidad. PRACTICA 2: Creamos los campos fantasma del grid extendido.
_density_field_1 = ti.field(float, shape=(res + 2, res + 2))
_density_field_2 = ti.field(float, shape=(res + 2, res + 2))

dens = FieldPair(_density_field_1, _density_field_2)

# PRACTICA 3: Campos de velocidad. Se deben inicializar como vectores 2D.
vel_buffer = ti.Vector.field(n=2, dtype=float, shape=(res + 2, res + 2))


# ------------------------------
# --- FUNCIÓN: Añadir fluido ---
# ------------------------------

@ti.kernel
def add_sources(dens: ti.template(), input_data: ti.types.ndarray()):

    # PRACTICA 2: Cambiamos el bucle para que no itere por las "celdas extendidas"
    for i, j in ti.ndrange((1, res+1), (1, res+1)):
       
        densidad = input_data[2] * s_dens
        mx, my = input_data[0], input_data[1]
       
        # Centro casilla i,j
        cx = i + 0.5
        cy = j + 0.5
        
        # Distancia al centro de la casilla (al cuadrado)
        d2 = (cx - mx) ** 2 + (cy - my) ** 2
        
        # Decaimiento exponencial
        dens[i, j] += dt * densidad * ti.exp(-6 * d2 / s_radius**2)


# ------------------------------------------
# --- FUNCIÓN: Añadir campo de velocidad --- (PRACTICA 3).
# ------------------------------------------

@ti.kernel
def init_vel_field():

    # Queremos añadir una franja horizontal (en mitad) y dos verticales.

    # Estas franjas son siempre de 1/3 del dominio.
    gap_size = res / 3

    # Iteramos por todo, ya que tenemos que añadir los valores nulos.
    for i, j in ti.ndrange((1, res+1), (1, res+1)):

        if j < gap_size:        # Franja inferior.
            vel_buffer[i, j] = ti.Vector([ - FIELD_SPEED, 0.0 ])
        
        elif j < 2 * gap_size:  # Franja central.
            vel_buffer[i, j] = ti.Vector([ FIELD_SPEED, 0.0 ])
        
        elif j < 3 * gap_size:  # Franja superior.
            vel_buffer[i, j] = ti.Vector([ - FIELD_SPEED, 0.0 ])
        
        else:                   # Cualquier otra posición.
            vel_buffer[i, j] = ti.Vector([ 0.0, 0.0 ])


# ------------------------------------
# --- FUNCIÓN: Calculo de difusión --- (PRACTICA 2)
# ------------------------------------

@ti.kernel
def jacobi_iter(dens_cur: ti.template(), dens_nxt: ti.template()):
    
    a = kappa * dt / (h ** 2)

    # PRACTICA 2: Cambiamos el bucle para que no itere por las "celdas extendidas"
    for i, j in ti.ndrange((1, res+1), (1, res+1)):
        dens_nxt[i, j] = (dens_cur[i, j] + a * (dens_cur[i-1, j]  + dens_cur[i+1, j]  + dens_cur[i, j-1] + dens_cur[i, j+1])) / (1 + 4 * a)

def diffuse(dens):
    for _ in range(DIFFUSION_STEPS):  # Iteraciones de Jacobi
    
        jacobi_iter(dens.cur, dens.nxt)

        # Tras cada iteración revisamos las fronteras.
        set_boundaries(dens.cur)
        dens.swap()


# ----------------------------------------------
# --- FUNCIÓN AUXILIAR: Interpolación lineal --- (PRACTICA 3)
# ----------------------------------------------

@ti.func
def bilerp(field: ti.template(), x: float, y: float) -> float:
    
    # Obtenemos puntos y vecinos proximos.
    i0 = int(ti.floor(x))
    j0 = int(ti.floor(y))
    i1 = i0 + 1
    j1 = j0 + 1

    # Y la diferencia entre el desplazamiento. Esto nos indica cuanto caso le hacemos a cada elemento.
    s = x - i0
    t = y - j0

    # Devolvemos la interpolación por distancia.
    interpolation = (1-s)*(1-t) * field[i0, j0] +  s *(1-t) * field[i1, j0] +  (1-s) * t * field[i0, j1] +   s * t * field[i1, j1]
    return  interpolation


# -------------------------------------
# --- FUNCIÓN: Calculo de advección --- (PRACTICA 3)
# -------------------------------------

@ti.kernel
def advect(dens_cur: ti.template(), dens_nxt: ti.template(), vel: ti.template()):
    
    for i, j in ti.ndrange((1, res+1), (1, res+1)):
        x0 = i - vel[i, j].x * dt
        y0 = j - vel[i, j].y * dt

        # Tratamos los elementos que se salen del plano.
        x0 = ti.max(0.5, ti.min(res + 0.5, x0))
        y0 = ti.max(0.5, ti.min(res + 0.5, y0))

        # Interpolación lineal de los 4 vecinos próximos.
        dens_nxt[i, j] = bilerp(dens_cur, x0, y0)


    
# --------------------------
# --- FUNCIÓN: Contornos --- (PRACTICA 2 + 3)
# --------------------------

@ti.kernel
def set_boundaries(field: ti.template()):

    # Podemos iterar de una vez ya que nuestro grid siempre es cuadrado.
    for i in range(res + 2):
        field[i, 0]         = field[i, 1]      # Abajo.
        field[i, res + 1]   = field[i, res]    # Arriba.
        field[0, i]         = field[1, i]      # Izquierda.
        field[res + 1, i]   = field[res, i]    # Derecha.

    # Caso especial: esquinas. Hacemos el promedio de sus vecinos (sin diagonales).
    field[0, 0]             = (field[1, 0]          + field[0, 1])          / 2
    field[res + 1, 0]       = (field[res, 0]        + field[res + 1, 1])    / 2
    field[0, res + 1]       = (field[1, res+1]      + field[0, res])        / 2
    field[res + 1, res + 1] = (field[res, res+1]    + field[res + 1, res])  / 2

# -------------------------------
# --- FUNCIÓN: Inicialización ---
# -------------------------------

def init():
    dens.cur.fill(0)
    dens.nxt.fill(0)
    init_vel_field()


# --------------------------------------
# --- FUNCIÓN: Paso de la simulación ---
# --------------------------------------

def step(input_data):
    add_sources(dens.cur, input_data)
    set_boundaries(dens.cur)
    diffuse(dens)

    advect(dens.cur, dens.nxt, vel_buffer)
    dens.swap()                            
    set_boundaries(dens.cur) 


# -------------------------
# --- FUNCIÓN PRINCIPAL ---
# -------------------------

def main():

    # Abrimos una nueva ventana donde ocurre la simulación.
    paused = False
    window = ti.ui.Window("Stable Fluids", (res, res), vsync=True)
    canvas = window.get_canvas()

    # Inicialización
    init()

    # Bucle Principal
    while window.running:

        # 0: mouse_x 1: mouse_y 2: source_active
        input_data = np.zeros(3, dtype=np.float32)

        # Interacciones de teclado.
        if window.get_event(ti.ui.PRESS):
            e = window.event

            if e.key == ti.ui.ESCAPE:  # ESC para salir
                break
            
            elif e.key == "r":  # 'r' para resetear
                paused = False
                init()
            
            elif e.key == "p":  # 'p' para pausar/reanudar
                paused = not paused

        # Interacciones del ratón. Se ha cambiado a Left-Mouse-Button para evitar problemas en MACOS.
        if window.is_pressed(ti.ui.LMB):

            mouse_xy = window.get_cursor_pos()
            input_data[0] = mouse_xy[0] * res
            input_data[1] = mouse_xy[1] * res
            input_data[2] = 1.0

        # Llamamos al step.
        if not paused:
            step(input_data)

        # Renderizado
        canvas.set_image(dens.cur)
        window.show()


if __name__ == "__main__":
    main()