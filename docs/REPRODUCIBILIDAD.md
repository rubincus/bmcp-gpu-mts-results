# Evidencia y reproducción

La comparación vigente usa PLTS, VDLS, IHS y ANRMA según Wei et al. (2026), Tables C.1–C.2, doi:10.1016/j.swevo.2026.102289. Para PLTS e IHS, el contexto temporal pequeño usa Wei y Hao (2023), identificado en las tablas. Los registros individuales de competidores no están disponibles: los contrastes usan medias por instancia, sin tratarlas como corridas individuales.

## Registros

Banco: 90 instancias × 10 semillas = 900. Los presupuestos originales son 180 s en 56 instancias y 90 s en 34. Los registros conservan el horizonte nominal y el resultado posterior al último lote en campos distintos. Las selecciones verificadas del análisis corresponden al horizonte observado según el protocolo; no se reetiquetan como nuevas ejecuciones.

Diagnóstico: 420 ablaciones (incluyen 126 piloto), 162 OFAT, 45 nuevas de combinaciones dirigidas, 180 confirmaciones, 180 validaciones reservadas, 60 trabajo/tiempo y 90 plataformas = 1137 distintas. Nueve controles OFAT se reutilizan en la tabla de combinaciones; por eso hay 1146 filas exportadas por etapa. Se añaden 60 nuevas de propietario/incidencia: 1197 ejecuciones distintas en total, aparte de las 900 del banco. Calentamientos y calibración no forman parte de estos tamaños muestrales.

Las exportaciones compactas omiten el campo de estados internos por bloque `diagnostics`; sus hashes originales se documentan. No equivalen byte por byte a los archivos instrumentados íntegros. Sí permiten reconstruir los resultados, tiempos, aciertos y gráficos aquí usados. Las observaciones acumuladas de trabajo están además congeladas en los datos de figuras. El depósito público normaliza solo rutas locales en metadatos y registra hashes de exportación.

## Relojes y unidades

- `time_to_best_seconds`: primera observación del mejor resultado incluido en el horizonte; incluye búsqueda y observación, excluye preparación.
- `elapsed_seconds`: pared de búsqueda, con despacho, sincronización y observación. Puede superar el horizonte en el último lote; no se suma a un tiempo de alcance para calcular coste total.
- Preparación: lectura, transferencias y compilación del solver nuevo según protocolo. En el estudio de plataformas la GPU requiere aproximadamente 1.11 s y la carga CPU 0.0015 s.
- Certificación: verificación final fuera del reloj de búsqueda. El solver completo incluye preparación, búsqueda completa y certificación; no mide parada temprana.
- Procedencia del trabajador: comprobaciones de hashes y archivos añaden alrededor de 24 s antes de cada solve del estudio de plataformas. Es coste del arnés de investigación, excluido del reloj del algoritmo. La construcción del binario CPU ocurre una vez antes de la campaña, no por corrida.
- Las campañas históricas usan observación por lotes; la comparación de plataformas y la de propietario usan un paso por lote. Un paso por trayectoria y un candidato evaluado son unidades distintas.

Los fallos al objetivo aportan el horizonte al tiempo acotado, no se interpretan como llegadas al final. Las medias condicionales incluyen el número de aciertos. Los cocientes CPU/GPU promedian diez razones pareadas por caso, no cocientes de medias. Las comparaciones con ANRMA son descriptivas por equipos, presupuestos y protocolos distintos.

## Experimento adicional de propietario

Se conservan mantenimiento XOR, orden de candidatos, disposición de memoria y decisiones. El cambio es la consulta de restauración cuando c[e]=1: propietario almacenado o incidencia del elemento en cada saliente. Los casos D1/D3/D5 ejecutan 139/512/512 pasos, 128 trayectorias y diez nuevas semillas pareadas. El protocolo fija el orden aleatorio y diez pasos de calentamiento por variante y caso. Se comprueban hashes de todos los arreglos devueltos, memoria por bloque, secuencias de incumbentes y certificados. Las medias de razón incidencia/propietario son 1.4940/1.4467/1.3785; intervalos bootstrap pareados de 20000 remuestreos se conservan en JSON.

## Figuras y tablas

Seis figuras: arquitectura, brechas finales, llegada al objetivo, ablaciones, trabajo/tiempo y CPU/GPU. El color identifica datos (método o instancia), no revisiones. Cada generador incorpora los datos congelados empleados. Los CSV/JSON retienen precisión; el manuscrito muestra decimales legibles. Las tablas completas incluyen mejores valores y medias, con empates en negrita. La fila Average/Promedio agrega 30 instancias.

La fuente instalable privada conserva los núcleos .cu/.cpp históricos. Los cambios de rutas, importaciones y descubrimiento de CUDA no se atribuyen retroactivamente a las corridas. Los análisis anteriores del archivo privado no definen la comparación actual.
