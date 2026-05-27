{{ config(alias='salarios_n_ocupaciones_2022') }}

SELECT 
    c.cno11,
    ABS(c.salario) AS salario,
    o.numero_trabajadores
FROM {{ ref('composicion_salario_bruto_absolutos') }} c
LEFT JOIN {{ ref('ocupaciones_absolutos') }} o
    ON c.cno11 = o.ocupacion
WHERE o.periodo = 2022