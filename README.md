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
