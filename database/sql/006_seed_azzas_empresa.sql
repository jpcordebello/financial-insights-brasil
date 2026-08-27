BEGIN;


INSERT INTO core.empresas (
    nome,
    ticker,
    cnpj,
    codigo_cvm,
    setor
)
VALUES (
    'Azzas 2154',
    'AZZA3',
    '16590234000176',
    22349,
    'Consumo Cíclico / Comércio / Tecidos, Vestuário e Calçados'
)

ON CONFLICT (nome)
DO UPDATE SET
    ticker = EXCLUDED.ticker,
    cnpj = EXCLUDED.cnpj,
    codigo_cvm = EXCLUDED.codigo_cvm,
    setor = EXCLUDED.setor;


COMMIT;