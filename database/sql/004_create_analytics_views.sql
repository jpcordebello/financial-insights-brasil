BEGIN;


CREATE OR REPLACE VIEW
    analytics.vw_resultados_financeiros
AS
SELECT
    r.id AS resultado_id,

    e.id AS empresa_id,
    e.nome AS empresa,
    e.ticker,
    e.setor,

    c.id AS conta_financeira_id,
    c.tipo_demonstracao,
    c.codigo AS codigo_conta,
    c.nome_pt AS conta,
    c.nome_en AS conta_en,
    c.unidade,
    c.ordem_exibicao,

    p.id AS periodo_id,
    p.ano,
    p.trimestre,
    p.periodo,

    r.valor,

    i.id AS importacao_id,
    i.arquivo_origem,
    i.aba_origem,
    i.importado_em

FROM core.resultados_financeiros AS r

INNER JOIN core.empresas AS e
    ON e.id = r.empresa_id

INNER JOIN core.contas_financeiras AS c
    ON c.id = r.conta_financeira_id

INNER JOIN core.periodos AS p
    ON p.id = r.periodo_id

INNER JOIN core.importacoes AS i
    ON i.id = r.importacao_id

WHERE
    c.ativo = TRUE;


COMMENT ON VIEW
    analytics.vw_resultados_financeiros
IS
    'Resultados financeiros padronizados para consumo analítico.';


COMMIT;