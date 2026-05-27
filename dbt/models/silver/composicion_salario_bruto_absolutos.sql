{{ config(alias='composicion_salario_bruto') }}

SELECT
    sexo,
    cno11,
    componentes_salario,
    salario
FROM {{ ref('composicion_salario_bruto') }}
WHERE sexo = 'Total'
  AND componentes_salario = 'Salario neto'
  AND cno11 NOT LIKE '%Total%'