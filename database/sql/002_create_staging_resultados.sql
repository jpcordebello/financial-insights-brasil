CREATE TABLE IF NOT EXISTS staging.resultados_financeiros (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    empresa VARCHAR(150) NOT NULL,
    tipo_demonstracao VARCHAR(100) NOT NULL,
    arquivo_origem VARCHAR(255) NOT NULL,
    aba_origem VARCHAR(100) NOT NULL,

    ordem_linha INTEGER NOT NULL,
    conta_pt VARCHAR(255) NOT NULL,
    conta_en VARCHAR(255),

    ano SMALLINT NOT NULL,
    trimestre SMALLINT NOT NULL,
    periodo VARCHAR(10) NOT NULL,

    unidade VARCHAR(30) NOT NULL,
    valor NUMERIC(20, 6) NOT NULL,

    carregado_em TIMESTAMP WITH TIME ZONE
        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT ck_staging_trimestre
        CHECK (trimestre BETWEEN 1 AND 4),

    CONSTRAINT ck_staging_unidade
        CHECK (unidade IN ('BRL_MILLIONS', 'RATIO'))
);