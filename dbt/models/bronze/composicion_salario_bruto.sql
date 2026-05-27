{{ config(alias='composicion_salario_bruto') }}

SELECT
    CAST(sexo AS CHAR) AS sexo,
    CAST(cno11 AS CHAR) AS cno11,
    CAST(componentes_salario AS CHAR) AS componentes_salario,
    CAST(salario AS FLOAT) AS salario
FROM {{ source('staging_ine', 'composicion_salario_bruto') }}