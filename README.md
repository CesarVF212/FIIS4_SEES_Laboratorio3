# --- ENGLISH ---

# SFX Simulation — Lab 3 (Stable Fluids II)

This lab implements density advection for a 2D fluid simulation in Taichi Lang, using the semi-Lagrangian method with bilinear interpolation.
A static velocity field is initialized with horizontal stripes to visually verify that the density is transported correctly.

---

## SFX Simulation
### BSc in Software Engineering
#### U-tad — Academic Year 25/26 | Lab 3 (Stable Fluids II)

## § Instructions §

- The code for the lab must be organized in a properly documented Python script (.py).
- The use of code from references or language models (LLMs) such as ChatGPT or GitHub Copilot is not allowed.
- The lab can be done individually or in pairs; the video must be individual.
  - The first line of the Python script must include the names of the team members.

### Use of Libraries

The use of the Python standard libraries and the Taichi Lang library is allowed. NumPy may be used for auxiliary tasks, but the core logic of the simulation is expected to be implemented in Taichi. The use of other libraries requires prior authorization.

---

## Density Advection

The goal of this lab is to implement **density advection** in the base code (`etapa0.py`) or on top of the Lab 2 solution. Advection simulates how density is transported by the fluid's velocity field: concentrations of density move following the direction and magnitude of the local velocities.

To observe the effect of advection, a non-zero velocity field is required. In this lab, a static velocity field will be initialized so that the correct behavior of the implementation can be verified visually.

---

## Implementation

1. **Initialize the Velocity Field.** Add a velocity field (`vel_buffer`) to the base code and create a Taichi kernel (`init_vel_field`) that initializes it with a simple pattern. For example, the velocity field could be initialized with a horizontal stripe in the middle of the domain with left-to-right velocities, and two horizontal stripes (one above and one below) with right-to-left velocities, with each stripe being approximately 1/3 of the total size of the domain.

2. **Implement the `advect` function (Semi-Lagrangian Advection with Bilinear Interpolation).** Create a Taichi kernel `advect` that applies the advection step using the semi-Lagrangian method. For each cell, the kernel must trace the position backwards (*backtrace*) according to the velocity field and obtain the density value at that origin position. Since the resulting position will generally not coincide with a grid point, it will be necessary to implement an auxiliary function `bilerp` that performs **bilinear interpolation** from the four neighboring cells.

3. **Modify the `step` function.** Integrate the new `advect` function into the `step` function at the appropriate place.

> **Note on the graphical user interface (GUI):** If you experience problems using Taichi Lang's new GGUI user interface (based on Vulkan), you can use the previous version of the GUI. To make it easier to use the previous version, the alternative starter code `etapa0_no_vk.py` is provided.

**The deadline for Lab 3 (Stable Fluids II) is April 12, 2026 at 23:59.**

---

## Video Explanation

An explanatory video (**maximum 5 minutes**) detailing the **Semi-Lagrangian Advection method with Bilinear Interpolation**.

The video must:

- Explain concisely and clearly the implemented Semi-Lagrangian Advection method, highlighting its relevance for simulating density transport in fluids.
- Clearly explain the use of Bilinear Interpolation within the Semi-Lagrangian Advection method, thus demonstrating an understanding of its role in the implementation.
- Show the fluid simulation running with the implemented Semi-Lagrangian Advection method and explain how the effect of advection is visually observed in the density field. Demonstrate how the structure of the velocity field influences the movement of the fluid.

*The understanding demonstrated and the clarity of the Video Explanation will account for 50% of the lab grade. The absence of a Video Explanation will result in a 0 for the lab grade.*

# --- SPANISH ---

# Simulación de SFX
## Grado en Ingeniería del Software
### U-tad — Curso 25/26 | Laboratorio 3 (Stable Fluids II)

## § Instrucciones §

- El código correspondiente al laboratorio debe organizarse en un script de Python (.py) debidamente documentado.
- No está permitido el uso de código procedente de referencias o modelos de lenguaje (LLMs) como ChatGPT o Github Copilot.
- El laboratorio se puede hacer de forma individual o por parejas; el vídeo debe ser individual.
  - La primera línea del script de Python debe incluir el nombre de los integrantes.

### Uso de Librerías

Se permite el uso de las librerías estándar de Python y la librería Taichi Lang. Se puede usar NumPy para tareas auxiliares, pero se espera que la lógica central de la simulación se implemente en Taichi. El uso de otras librerías requiere autorización previa.

---

## Advección de la Densidad

El objetivo de este laboratorio es implementar la **advección de la densidad** en el código base (`etapa0.py`) o sobre la solución del Laboratorio 2. La advección simula cómo la densidad es transportada por el campo de velocidad del fluido: las concentraciones de densidad se mueven siguiendo la dirección y magnitud de las velocidades locales.

Para observar el efecto de la advección, será necesario disponer de un campo de velocidades no nulo. En este laboratorio, se inicializará un campo de velocidades estático que permita verificar visualmente el correcto funcionamiento de la implementación.

---

## Implementación

1. **Inicializar Campo de Velocidades.** Añade un campo de velocidades (`vel_buffer`) al código base y crea un kernel de Taichi (`init_vel_field`) que lo inicialice con un patrón simple. Por ejemplo, el campo de velocidades podría ser inicializado de manera que haya una franja horizontal en el medio del dominio con velocidades de izquierda a derecha y dos franjas horizontales (una arriba y otra abajo) con velocidades de derecha a izquierda, siendo el tamaño de cada franja aproximadamente 1/3 del tamaño total del dominio.

2. **Implementar la función `advect` (Advección Semi-Lagrangiana con Interpolación Bilineal).** Crea un kernel de Taichi `advect` que aplique el paso de advección usando el método semi-Lagrangiano. Para cada celda, el kernel deberá trazar hacia atrás (*backtrace*) la posición según el campo de velocidades y obtener el valor de densidad en esa posición de origen. Dado que la posición resultante generalmente no coincidirá con un punto de la malla, será necesario implementar una función auxiliar `bilerp` que realice la **interpolación bilineal** a partir de las cuatro celdas vecinas.

3. **Modificar la función `step`.** Integra la nueva función `advect` en la función `step` en el lugar correspondiente.

> **Nota sobre la interfaz gráfica (GUI):** Si experimentas problemas al utilizar la nueva interfaz de usuario GGUI de Taichi Lang (basada en Vulkan) puedes utilizar la versión anterior de la GUI. Para facilitar el uso de la versión anterior, se proporciona el código de inicio alternativo `etapa0_no_vk.py`.

**La fecha de entrega del laboratorio 3 (stable fluids ii) es el 12 de abril de 2026 a las 23:59.**

---

## Vídeo-Explicación

Vídeo explicativo (**máximo 5 minutos**) detallando el **método de Advección Semi-Lagrangiana con Interpolación Bilineal**.

En el vídeo se debe:

- Explicar de forma concisa y clara el método de Advección Semi-Lagrangiana implementado, destacando su relevancia para simular el transporte de la densidad en fluidos.
- Explicar claramente el uso de la Interpolación Bilineal dentro del método de Advección Semi-Lagrangiana, demostrando así la comprensión de su rol en la implementación.
- Mostrar la simulación de fluidos funcionando con el método de Advección Semi-Lagrangiana implementado y explicar cómo se observa visualmente el efecto de la advección en el campo de densidad. Demostrar cómo la estructura del campo de velocidades influye en el movimiento del fluido.

*La comprensión demostrada y la claridad en la Vídeo-Explicación corresponderá al 50% de la calificación del laboratorio. La ausencia de Vídeo-Explicación implicará un 0 en la calificación del laboratorio.*
