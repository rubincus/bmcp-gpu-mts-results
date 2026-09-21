# GPU-MTS: resultados y evidencia reproducible para BMCP

Depósito público de **90 mejores soluciones factibles**, las **900 corridas** del banco (diez por instancia), y los datos y scripts utilizados en las figuras y tablas del estudio de GPU-MTS para el problema de cobertura máxima con presupuesto. Los costes pertenecen a los ítems y los beneficios a los elementos cubiertos una sola vez.

## Resultados

Frente a los mejores valores reportados por **Wei et al. (2026)**, [doi:10.1016/j.swevo.2026.102289](https://doi.org/10.1016/j.swevo.2026.102289), se mejoran cuatro valores y se igualan 86. Las diez corridas coinciden en el valor final de cada instancia; el promedio mejora sobre ANRMA en 25 casos. El alcance es esa comparación bibliográfica: no se afirma optimalidad. Los tiempos publicados de competidores usan otros equipos y protocolos.

Los 90 testigos se escogen por la menor semilla entre corridas con el mejor valor, sin seleccionar por tiempo. `summary.csv` conserva best, media, desviación, tiempo y referencia por instancia. `published_BKV` es el máximo entre la columna BKV y los mejores valores de los métodos de la referencia; `bkv_column` conserva la columna histórica original. `reference_best` en el análisis es R = max(published_BKV, GPU best), usado para brechas; no es una cota óptima.

## Verificar las soluciones

Python 3.10 o posterior. La descarga y certificación usan solo la biblioteca estándar:

```sh
python scripts/download_instances.py
python scripts/verify_solutions.py
```

Las instancias se obtienen de [Zequn-Wei/BMCP](https://github.com/Zequn-Wei/BMCP) y [JHL-HUST/VDLS](https://github.com/JHL-HUST/VDLS). Se verifican los hashes del archivo y de cada instancia. No se redistribuyen aquí. También se admiten `set1.zip` y `set2.zip` locales mediante `--archives-dir`.

Cada JSON en `solutions/` incluye `selected_items_0based`, su equivalente `selected_items_1based`, beneficio, coste, capacidad, hash de instancia, semilla y certificado. El auditor vuelve a calcular la unión de cobertura desde el texto de la instancia, independientemente del solver.

## Reconstruir análisis y figuras

```sh
python -m pip install -r requirements.txt
python scripts/analyze_results.py
python scripts/reproduce_figures.py --language es
python scripts/reproduce_figures.py --language en
```

Las salidas se escriben en `runs/`. El análisis recalcula las estadísticas desde las 900 corridas y los valores bibliográficos. Las figuras usan los datos congelados en `analysis/figures/`; los scripts no ejecutan búsquedas. Los archivos finales de todas las figuras y tablas, en ambos idiomas, están en `paper_assets/`. Las tablas de diagnóstico se incluyen con sus datos por etapa y protocolos. Los formatos decimales de presentación no sustituyen la precisión de los JSON.

## Contenido y trazabilidad

- `data/historical/`: 900 corridas, protocolos y auditoría; 56 instancias con 180 s y 34 con 90 s.
- `data/comparison/`: valores bibliográficos identificados por instancia y análisis actual de cinco métodos.
- `data/diagnostics/`: siete etapas; 1146 filas de etapa representan 1137 ejecuciones distintas por reutilización de nueve controles. Las 420 ablaciones incluyen las 126 piloto. Las exportaciones compactas omiten estados internos voluminosos, pero preservan calidad, testigos, trazas, parámetros y tiempos.
- `data/owner_lookup/`: experimento adicional de 60 ejecuciones con trabajo fijado. La única diferencia evaluada es consultar el propietario frente a la matriz de incidencias. Ambas variantes mantienen el XOR. Las parejas coinciden en estados finales y certificados; razones medias de tiempo 1.49, 1.45 y 1.38.
- `data/PUBLIC_EXPORT_MANIFEST.json`: hashes de origen y exportación; las rutas absolutas locales de metadatos se sustituyen por identificadores relativos. Los resultados numéricos no se alteran.
- `docs/REPRODUCIBILIDAD.md`: definiciones, relojes, alcance y costes de preparación.

El código del solver se mantiene en un repositorio privado. Este depósito contiene auditoría y análisis, no CUDA ni CPU/OpenMP del algoritmo, artículos ni credenciales. No se atribuye aquí una licencia a instancias o datos bibliográficos de terceros; se conservan sus fuentes.

## Correspondencia con las figuras del artículo

Las etiquetas **Base** (español) y **Baseline** (inglés) designan la configuración identificada como `original` o `base` en los registros experimentales. Los identificadores archivados y los datos numéricos permanecen intactos. Las figuras incluyen ejes, leyendas y anotaciones de datos; sus condiciones de comparación se desarrollan en los pies del manuscrito. Los archivos de `paper_assets/es` y `paper_assets/en` corresponden a la revisión narrativa de 21 de septiembre de 2026.
