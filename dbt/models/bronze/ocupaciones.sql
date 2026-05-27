{{ config(alias='ocupaciones') }}

SELECT
    CAST(ocupacion AS CHAR) AS ocupacion,
    CAST(sexo AS CHAR) AS sexo,
    CAST(tipo_dato AS CHAR) AS tipo_dato,
    CAST(periodo AS SIGNED) AS periodo,
    CAST(numero_trabajadores AS FLOAT) AS numero_trabajadores
FROM {{ source('staging_ine', 'ocupaciones') }}