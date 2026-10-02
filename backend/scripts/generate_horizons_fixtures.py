"""
Extracción de vectores de efemérides heliocéntricos desde JPL Horizons usando Astroquery.

Este script consulta la base de datos de JPL Horizons para obtener los vectores de estado
(posición, velocidad, tiempo-luz, distancia y tasa de distancia) de todos los planetas del
Sistema Solar, tanto para sus baricentros de sistema como para los cuerpos físicos individuales.
Los resultados se formatean y escriben en un archivo de texto con la convención Major Body.
"""

from __future__ import annotations

import logging
import sys
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Final, List, Optional

from astropy.table import Table
from astropy.time import Time
from astropy.utils.exceptions import AstropyDeprecationWarning
from astroquery.jplhorizons import Horizons

# Configuración de registro y advertencias
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger: logging.Logger = logging.getLogger("HorizonsExtractor")

# Suprimir advertencia de deprecación de id_type='majorbody' en astroquery
# para mantener compatibilidad estricta con el parámetro solicitado
warnings.filterwarnings("ignore", category=AstropyDeprecationWarning)

# Constantes de configuración
HEADER_SEPARATOR: Final[str] = "*" * 79
OBSERVER_LOCATION: Final[str] = "500@10"  # Sun (body center)
ID_TYPE: Final[str] = "majorbody"
DEFAULT_OUTPUT_FILE: Final[str] = "horizons_vectores_planetas.txt"
DISCRETE_EPOCHS: Final[List[str]] = [
    "2000-01-01 12:00",
    "2010-01-01 12:00",
]


@dataclass(frozen=True)
class TargetBody:
    """Representa un cuerpo celeste u objetivo para consulta en JPL Horizons."""

    name: str
    id: str

    @property
    def formatted_name(self) -> str:
        """Devuelve el nombre formateado bajo la convención 'MB: <nombre>'."""
        clean_name = self.name.removeprefix("MB: ").strip()
        return f"MB: {clean_name}"


# Catálogo ordenado de los 16 objetivos (Baricentro y Planeta individual)
PLANETARY_TARGETS: Final[List[TargetBody]] = [
    # Mercurio
    TargetBody(name="Mercury Barycenter", id="1"),
    TargetBody(name="Mercury", id="199"),
    # Venus
    TargetBody(name="Venus Barycenter", id="2"),
    TargetBody(name="Venus", id="299"),
    # Tierra
    TargetBody(name="Earth-Moon Barycenter [EMB]", id="3"),
    TargetBody(name="Earth", id="399"),
    # Marte
    TargetBody(name="Mars Barycenter", id="4"),
    TargetBody(name="Mars", id="499"),
    # Júpiter
    TargetBody(name="Jupiter Barycenter", id="5"),
    TargetBody(name="Jupiter", id="599"),
    # Saturno
    TargetBody(name="Saturn Barycenter", id="6"),
    TargetBody(name="Saturn", id="699"),
    # Urano
    TargetBody(name="Uranus Barycenter", id="7"),
    TargetBody(name="Uranus", id="799"),
    # Neptuno
    TargetBody(name="Neptune Barycenter", id="8"),
    TargetBody(name="Neptune", id="899"),
]


def convert_epochs_to_jd(epochs: List[str], scale: str = "tdb") -> List[float]:
    """
    Convierte una lista de fechas discretas (strings ISO) a fechas julianas (JD).

    JPL Horizons requiere valores numéricos JD para consultas de épocas discretas
    en tablas de vectores.
    """
    t = Time(epochs, scale=scale)
    return t.jd.tolist()


def fetch_target_vectors(
    target: TargetBody,
    location: str,
    epochs_jd: List[float],
    id_type: str = ID_TYPE,
) -> Optional[Table]:
    """
    Consulta la API de JPL Horizons para obtener la tabla de vectores de estado.

    Retorna la tabla de astropy si la consulta fue exitosa, o None en caso de fallo.
    """
    try:
        horizons_query = Horizons(
            id=target.id,
            location=location,
            epochs=epochs_jd,
            id_type=id_type,
        )
        vector_table: Table = horizons_query.vectors()
        return vector_table
    except Exception as exc:
        logger.error(
            "Fallo al consultar '%s' (ID: %s): %s",
            target.formatted_name,
            target.id,
            exc,
        )
        return None


def format_vector_block(target: TargetBody, table: Table) -> str:
    """
    Construye el bloque de texto para un cuerpo celeste con encabezado y vectores.

    Formato especificado:
    *******************************************************************************
    Target: MB: [Nombre] (ID: [id])
    *******************************************************************************
    {datetime_jd} = {datetime_str}
     X ={x:1.15E} Y ={y:1.15E} Z ={z:1.15E}
     VX={vx:1.15E} VY={vy:1.15E} VZ={vz:1.15E}
     LT={lighttime:1.15E} RG={range:1.15E} RR={range_rate:1.15E}
    """
    lines: List[str] = [
        HEADER_SEPARATOR,
        f"Target: {target.formatted_name} (ID: {target.id})",
        HEADER_SEPARATOR,
    ]

    for row in table:
        datetime_jd = row["datetime_jd"]
        datetime_str = row["datetime_str"]
        x: float = float(row["x"])
        y: float = float(row["y"])
        z: float = float(row["z"])
        vx: float = float(row["vx"])
        vy: float = float(row["vy"])
        vz: float = float(row["vz"])
        lighttime: float = float(row["lighttime"])
        range_val: float = float(row["range"])
        range_rate: float = float(row["range_rate"])

        lines.append(f"{datetime_jd} = {datetime_str}")
        lines.append(f" X ={x:1.15E} Y ={y:1.15E} Z ={z:1.15E}")
        lines.append(f" VX={vx:1.15E} VY={vy:1.15E} VZ={vz:1.15E}")
        lines.append(
            f" LT={lighttime:1.15E} RG={range_val:1.15E} RR={range_rate:1.15E}")

    return "\n".join(lines)


def generate_ephemerides_file(
    targets: List[TargetBody],
    output_path: Path,
    epochs: List[str] = DISCRETE_EPOCHS,
    location: str = OBSERVER_LOCATION,
) -> int:
    """
    Itera sobre la lista de objetivos, obtiene los vectores y escribe el archivo final.

    Retorna la cantidad de objetivos procesados con éxito.
    """
    epochs_jd: List[float] = convert_epochs_to_jd(epochs)
    logger.info("Épocas convertidas a JD: %s", epochs_jd)

    blocks: List[str] = []
    successful_count: int = 0
    failed_count: int = 0

    total_targets = len(targets)
    logger.info(
        "Iniciando extracción para %d objetivos desde JPL Horizons...", total_targets)

    for idx, target in enumerate(targets, start=1):
        logger.info(
            "[%d/%d] Consultando %s (ID: %s)...",
            idx,
            total_targets,
            target.formatted_name,
            target.id,
        )

        table = fetch_target_vectors(
            target=target,
            location=location,
            epochs_jd=epochs_jd,
        )

        if table is not None and len(table) > 0:
            block_text = format_vector_block(target, table)
            blocks.append(block_text)
            successful_count += 1
            logger.info("  -> Éxito: %d épocas extraídas.", len(table))
        else:
            failed_count += 1
            logger.warning(
                "  -> Omitiendo '%s' por error en la consulta.", target.formatted_name)

    # Escritura en archivo de salida
    full_content = "\n\n".join(blocks) + "\n"
    output_path.write_text(full_content, encoding="utf-8")
    logger.info("Archivo generado con éxito: %s", output_path.resolve())
    logger.info(
        "Resumen: %d exitosos, %d fallidos de un total de %d.",
        successful_count,
        failed_count,
        total_targets,
    )

    return successful_count


def main() -> None:
    """Punto de entrada principal para la ejecución del script."""
    output_file = Path(DEFAULT_OUTPUT_FILE)
    logger.info("Iniciando proceso de extracción de efemérides JPL Horizons.")
    logger.info("Ubicación del observador: Sol (%s)", OBSERVER_LOCATION)
    logger.info("Épocas objetivo: %s", DISCRETE_EPOCHS)
    logger.info("Archivo de salida: %s", output_file.name)

    success_count = generate_ephemerides_file(
        targets=PLANETARY_TARGETS,
        output_path=output_file,
    )

    if success_count == len(PLANETARY_TARGETS):
        logger.info("Proceso completado al 100%% sin errores.")
    else:
        logger.warning(
            "El proceso finalizó con algunas advertencias (%d/%d procesados).",
            success_count,
            len(PLANETARY_TARGETS),
        )


if __name__ == "__main__":
    main()
