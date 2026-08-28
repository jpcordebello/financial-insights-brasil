import {
    useEffect,
    useState,
} from "react";

import { listarDre } from "../api/financialApi";

import type {
    ItemDre,
} from "../types/financeiro";


interface EstadoDre {
    chave: string;
    dados: ItemDre[];
    erro: string | null;
}


const ESTADO_INICIAL: EstadoDre = {
    chave: "",
    dados: [],
    erro: null,
};


export function useDre(
    ticker: string,
    periodo: string,
) {
    const [
        estado,
        setEstado,
    ] = useState<EstadoDre>(
        ESTADO_INICIAL,
    );

    const chaveAtual = periodo
        ? `${ticker}:${periodo}`
        : "";

    useEffect(() => {
        if (!periodo) {
            return;
        }

        let componenteAtivo = true;

        listarDre(ticker, periodo)
            .then((dados) => {
                if (componenteAtivo) {
                    setEstado({
                        chave: `${ticker}:${periodo}`,
                        dados,
                        erro: null,
                    });
                }
            })
            .catch((erroRecebido: unknown) => {
                if (!componenteAtivo) {
                    return;
                }

                const mensagem = (
                    erroRecebido instanceof Error
                )
                    ? erroRecebido.message
                    : "Erro desconhecido ao carregar a DRE.";

                setEstado({
                    chave: `${ticker}:${periodo}`,
                    dados: [],
                    erro: mensagem,
                });
            });

        return () => {
            componenteAtivo = false;
        };
    }, [ticker, periodo]);

    const respostaAtual = (
        estado.chave === chaveAtual
    );

    return {
        dre: respostaAtual
            ? estado.dados
            : [],

        carregando: (
            Boolean(chaveAtual)
            && !respostaAtual
        ),

        erro: respostaAtual
            ? estado.erro
            : null,
    };
}