import {
    useEffect,
    useState,
} from "react";

import {
    listarHistoricoKpis,
} from "../api/financialApi";
import type {
    KpiTrimestral,
} from "../types/financeiro";


export function useHistoricoKpis(
    ticker: string,
) {
    const [historico, setHistorico] = (
        useState<KpiTrimestral[]>([])
    );

    const [carregando, setCarregando] = (
        useState(true)
    );

    const [erro, setErro] = (
        useState<string | null>(null)
    );

    useEffect(() => {
        let componenteAtivo = true;

        async function carregarHistorico() {
            try {
                setCarregando(true);
                setErro(null);

                const dados = (
                    await listarHistoricoKpis(ticker)
                );

                if (componenteAtivo) {
                    setHistorico(dados);
                }
            } catch (erroEncontrado) {
                if (!componenteAtivo) {
                    return;
                }

                const mensagem = (
                    erroEncontrado instanceof Error
                        ? erroEncontrado.message
                        : "Não foi possível carregar o histórico."
                );

                setErro(mensagem);
            } finally {
                if (componenteAtivo) {
                    setCarregando(false);
                }
            }
        }

        carregarHistorico();

        return () => {
            componenteAtivo = false;
        };
    }, [ticker]);

    return {
        historico,
        carregando,
        erro,
    };
}