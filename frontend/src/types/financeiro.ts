export type Empresa = {
    id: number;
    nome: string;
    ticker: string | null;
    setor: string | null;
};


export type KpiTrimestral = {
    empresa_id: number;
    empresa: string;
    ticker: string;
    setor: string | null;

    ano: number;
    trimestre: number;
    periodo: string;

    receita_liquida: number;
    margem_bruta: number;

    ebitda: number;
    margem_ebitda: number;

    lucro_liquido: number;
    margem_liquida: number;
};


export interface ItemDre {
    empresa: string;
    ticker: string;
    periodo: string;

    codigo_conta: string;
    conta: string;
    conta_en: string | null;

    unidade: "BRL_MILLIONS" | "RATIO";
    ordem_exibicao: number;
    valor: number;
}