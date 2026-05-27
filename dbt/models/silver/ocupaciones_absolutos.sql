{{ config(alias='ocupaciones_absolutos') }}

SELECT
    ocupacion,
    sexo,
    tipo_dato,
    periodo,
    numero_trabajadores
FROM {{ ref('ocupaciones') }} -- Hacemos referencia al modelo Bronze
WHERE sexo = 'Ambos sexos'
  AND tipo_dato = 'Personas'
  -- Usamos NOT LIKE '%Total%' para asegurar que excluye cualquier fila que contenga la palabra Total
  AND ocupacion NOT LIKE '%Total%'