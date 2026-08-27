BEGIN;
CREATE TABLE IF NOT EXISTS core.empresas (
    id BIGINT GENERATED ALWAYS AS IDENTITY
        PRIMARY KEY,

    nome VARCHAR(150) NOT NULL,
    ticker VARCHAR(10),
    cnpj VARCHAR(14),
    codigo_cvm INTEGER,
    setor VARCHAR(100),

    criado_em TIMESTAMP WITH TIME ZONE
        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_core_empresas_nome
        UNIQUE (nome),

    CONSTRAINT uq_core_empresas_ticker
        UNIQUE (ticker),

    CONSTRAINT uq_core_empresas_cnpj
        UNIQUE (cnpj),

    CONSTRAINT uq_core_empresas_codigo_cvm
        UNIQUE (codigo_cvm)
);


CREATE TABLE IF NOT EXISTS core.contas_financeiras (
    id BIGINT GENERATED ALWAYS AS IDENTITY
        PRIMARY KEY,

    codigo VARCHAR(60) NOT NULL,
    tipo_demonstracao VARCHAR(100) NOT NULL,

    nome_pt VARCHAR(255) NOT NULL,
    nome_en VARCHAR(255),

    unidade VARCHAR(30) NOT NULL,
    ordem_exibicao INTEGER NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT uq_core_contas_codigo
        UNIQUE (tipo_demonstracao, codigo),

    CONSTRAINT uq_core_contas_ordem
        UNIQUE (
            tipo_demonstracao,
            ordem_exibicao
        ),

    CONSTRAINT ck_core_contas_unidade
        CHECK (
            unidade IN (
                'BRL_MILLIONS',
                'RATIO'
            )
        ),

    CONSTRAINT ck_core_contas_ordem
        CHECK (ordem_exibicao > 0)
);

CREATE TABLE IF NOT EXISTS core.periodos (
    id BIGINT GENERATED ALWAYS AS IDENTITY
        PRIMARY KEY,

    ano SMALLINT NOT NULL,
    trimestre SMALLINT NOT NULL,
    periodo VARCHAR(10) NOT NULL,

    CONSTRAINT uq_core_periodos_ano_trimestre
        UNIQUE (ano, trimestre),

    CONSTRAINT uq_core_periodos_periodo
        UNIQUE (periodo),

    CONSTRAINT ck_core_periodos_ano
        CHECK (ano BETWEEN 2000 AND 2099),

    CONSTRAINT ck_core_periodos_trimestre
        CHECK (trimestre BETWEEN 1 AND 4),

    CONSTRAINT ck_core_periodos_formato
        CHECK (periodo ~ '^[1-4]Q[0-9]{2}$')
);

CREATE TABLE IF NOT EXISTS core.importacoes (
    id BIGINT GENERATED ALWAYS AS IDENTITY
        PRIMARY KEY,

    empresa_id BIGINT NOT NULL,

    tipo_demonstracao VARCHAR(100) NOT NULL,
    arquivo_origem VARCHAR(255) NOT NULL,
    aba_origem VARCHAR(100) NOT NULL,

    importado_em TIMESTAMP WITH TIME ZONE
        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_core_importacoes_empresa
        FOREIGN KEY (empresa_id)
        REFERENCES core.empresas (id)
        ON DELETE RESTRICT,

    CONSTRAINT uq_core_importacoes_origem
        UNIQUE (
            empresa_id,
            tipo_demonstracao,
            arquivo_origem,
            aba_origem
        )
);

CREATE TABLE IF NOT EXISTS core.resultados_financeiros (
    id BIGINT GENERATED ALWAYS AS IDENTITY
        PRIMARY KEY,

    empresa_id BIGINT NOT NULL,
    conta_financeira_id BIGINT NOT NULL,
    periodo_id BIGINT NOT NULL,
    importacao_id BIGINT NOT NULL,

    valor NUMERIC(20, 6) NOT NULL,

    criado_em TIMESTAMP WITH TIME ZONE
        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_core_resultados_empresa
        FOREIGN KEY (empresa_id)
        REFERENCES core.empresas (id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_core_resultados_conta
        FOREIGN KEY (conta_financeira_id)
        REFERENCES core.contas_financeiras (id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_core_resultados_periodo
        FOREIGN KEY (periodo_id)
        REFERENCES core.periodos (id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_core_resultados_importacao
        FOREIGN KEY (importacao_id)
        REFERENCES core.importacoes (id)
        ON DELETE RESTRICT,

    CONSTRAINT uq_core_resultados_chave
        UNIQUE (
            empresa_id,
            conta_financeira_id,
            periodo_id
        )
);
COMMIT;
