import type {
    Empresa,
    ItemDre,
    KpiTrimestral,
} from "../types/financeiro";


const API_BASE_URL = (
    import.meta.env.VITE_API_URL
    ?? "http://127.0.0.1:8000/api/v1"
).replace(/\/$/, "");


async function buscarJson<T>(
    caminho: string,
): Promise<T> {
    const resposta = await fetch(
        `${API_BASE_URL}${caminho}`,
        {
            headers: {
                Accept: "application/json",
            },
        },
    );

    if (!resposta.ok) {
        let mensagem = (
            `Erro ${resposta.status} ao consultar a API.`
        );

        try {
            const corpo = await resposta.json();

            if (corpo.detail) {
                mensagem = corpo.detail;
            }
        } catch {
            // Mantém a mensagem padrão.
        }

        throw new Error(mensagem);
    }

    return resposta.json() as Promise<T>;
}


export function listarEmpresas():
    Promise<Empresa[]> {
    return buscarJson<Empresa[]>(
        "/empresas",
    );
}


export function buscarKpi(
    ticker: string,
    periodo: string,
): Promise<KpiTrimestral> {
    const tickerSeguro = encodeURIComponent(
        ticker
    );

    const periodoSeguro = encodeURIComponent(
        periodo
    );

    return buscarJson<KpiTrimestral>(
        `/empresas/${tickerSeguro}/kpis`
        + `?periodo=${periodoSeguro}`,
    );
}


export function listarHistoricoKpis(
    ticker: string,
): Promise<KpiTrimestral[]> {
    const tickerSeguro = encodeURIComponent(
        ticker
    );

    return buscarJson<KpiTrimestral[]>(
        `/empresas/${tickerSeguro}`
        + "/kpis/historico",
    );
}


export function listarDre(
    ticker: string,
    periodo: string,
): Promise<ItemDre[]> {
    const tickerSeguro = encodeURIComponent(
        ticker
    );

    const periodoSeguro = encodeURIComponent(
        periodo
    );

    return buscarJson<ItemDre[]>(
        `/empresas/${tickerSeguro}/dre`
        + `?periodo=${periodoSeguro}`,
    );
}