BEGIN;


CREATE OR REPLACE VIEW
    analytics.vw_kpis_trimestrais
AS
SELECT
    empresa_id,
    empresa,
    ticker,
    setor,

    ano,
    trimestre,
    periodo,

    MAX(valor) FILTER (
        WHERE codigo_conta = 'RECEITA_LIQUIDA'
    ) AS receita_liquida,

    MAX(valor) FILTER (
        WHERE codigo_conta = 'MARGEM_BRUTA'
    ) AS margem_bruta,

    MAX(valor) FILTER (
        WHERE codigo_conta = 'EBITDA'
    ) AS ebitda,

    MAX(valor) FILTER (
        WHERE codigo_conta = 'MARGEM_EBITDA'
    ) AS margem_ebitda,

    MAX(valor) FILTER (
        WHERE codigo_conta = 'LUCRO_LIQUIDO'
    ) AS lucro_liquido,

    MAX(valor) FILTER (
        WHERE codigo_conta = 'MARGEM_LIQUIDA'
    ) AS margem_liquida

FROM analytics.vw_resultados_financeiros

WHERE
    tipo_demonstracao = 'DRE Pro Forma'

GROUP BY
    empresa_id,
    empresa,
    ticker,
    setor,
    ano,
    trimestre,
    periodo;


COMMENT ON VIEW
    analytics.vw_kpis_trimestrais
IS
    'Indicadores trimestrais preparados para os cards do dashboard.';


COMMIT;