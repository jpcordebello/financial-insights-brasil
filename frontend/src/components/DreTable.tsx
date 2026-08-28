import type {
    ItemDre,
} from "../types/financeiro";

import {
    formatarMilhoes,
    formatarPercentual,
} from "../utils/formatacao";


interface DreTableProps {
    itens: ItemDre[];
    carregando: boolean;
    erro: string | null;
}


const CODIGOS_RESUMO = [
    "RECEITA_LIQUIDA",
    "LUCRO_BRUTO",
    "MARGEM_BRUTA",
    "EBITDA",
    "MARGEM_EBITDA",
    "EBIT",
    "RESULTADO_FINANCEIRO",
    "LUCRO_LIQUIDO",
    "MARGEM_LIQUIDA",
];


function formatarValor(
    item: ItemDre,
): string {
    if (item.unidade === "RATIO") {
        return formatarPercentual(item.valor);
    }

    return formatarMilhoes(item.valor);
}


export function DreTable({
    itens,
    carregando,
    erro,
}: DreTableProps) {
    if (carregando) {
        return (
            <p aria-live="polite">
                Carregando DRE...
            </p>
        );
    }

    if (erro) {
        return (
            <p role="alert">
                Não foi possível carregar a DRE.
            </p>
        );
    }

    const itensResumo = itens
        .filter((item) => (
            CODIGOS_RESUMO.includes(
                item.codigo_conta,
            )
        ))
        .sort((
            primeiroItem,
            segundoItem,
        ) => (
            primeiroItem.ordem_exibicao
            - segundoItem.ordem_exibicao
        ));

    if (itensResumo.length === 0) {
        return (
            <p>
                Nenhum dado disponível para o período.
            </p>
        );
    }

    return (
        <div className="dre-table-wrapper">
            <table className="dre-table">
                <thead>
                    <tr>
                        <th>Conta</th>
                        <th>Valor</th>
                    </tr>
                </thead>

                <tbody>
                    {itensResumo.map((item) => (
                        <tr key={item.codigo_conta}>
                            <td>{item.conta}</td>

                            <td>
                                {formatarValor(item)}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}