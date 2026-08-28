import {
    useState,
} from "react";

import KpiCard from "../components/KpiCard";
import {
    useHistoricoKpis,
} from "../hooks/useHistoricoKpis";
import {
    formatarMilhoes,
    formatarPercentual,
    formatarPeriodo,
} from "../utils/formatacao";
import { EvolucaoChart } from "../components/EvolucaoChart";
import "./DashboardPage.css";
import { DreTable } from "../components/DreTable";
import { useDre } from "../hooks/useDre";

function DashboardPage() {
    const [periodoSelecionado, setPeriodoSelecionado] = (
        useState("")
    );

    const {
        historico,
        carregando,
        erro,
    } = useHistoricoKpis("AZZA3");

    const ultimoKpi = (
        historico.length > 0
            ? historico[historico.length - 1]
            : null
    );

    const kpi = (
        historico.find(
            (item) => (
                item.periodo === periodoSelecionado
            ),
        )
        ?? ultimoKpi
    );

    const periodoAtivo = (
        periodoSelecionado
        || kpi?.periodo
        || ""
    );

    const {
        dre,
        carregando: carregandoDre,
        erro: erroDre,
    } = useDre("AZZA3", periodoAtivo);

    const periodosDisponiveis = (
        [...historico].reverse()
    );

    const valorInicial = (
        carregando
            ? "Carregando..."
            : "—"
    );

    const indicadores = [
        {
            titulo: "Receita líquida",
            valor: (
                kpi
                    ? formatarMilhoes(
                        kpi.receita_liquida
                    )
                    : valorInicial
            ),
            legenda: "Valores em R$ milhões",
        },
        {
            titulo: "EBITDA",
            valor: (
                kpi
                    ? formatarMilhoes(kpi.ebitda)
                    : valorInicial
            ),
            legenda: "Resultado operacional",
        },
        {
            titulo: "Lucro líquido",
            valor: (
                kpi
                    ? formatarMilhoes(
                        kpi.lucro_liquido
                    )
                    : valorInicial
            ),
            legenda: "Valores em R$ milhões",
        },
        {
            titulo: "Margem EBITDA",
            valor: (
                kpi
                    ? formatarPercentual(
                        kpi.margem_ebitda
                    )
                    : valorInicial
            ),
            legenda: "Percentual sobre a receita",
        },
    ];

    return (
        <div className="dashboard">
            <header className="dashboard__header">
                <div>
                    <span className="dashboard__eyebrow">
                        Financial Insights Brasil
                    </span>

                    <h1 className="dashboard__title">
                        {kpi?.empresa ?? "Azzas 2154"}
                    </h1>

                    <p className="dashboard__subtitle">
                        {kpi?.ticker ?? "AZZA3"}
                        {" · "}
                        {kpi?.setor ?? "Consumo Cíclico"}
                    </p>
                </div>

                <div className="dashboard__filters">
                    <label className="dashboard__field">
                        Empresa

                        <select value="AZZA3" disabled>
                            <option value="AZZA3">
                                Azzas 2154
                            </option>
                        </select>
                    </label>

                    <label className="dashboard__field">
                        Período

                        <select
                            value={periodoAtivo}
                            disabled={
                                carregando
                                || periodosDisponiveis.length === 0
                            }
                            onChange={(evento) => {
                                setPeriodoSelecionado(
                                    evento.target.value
                                );
                            }}
                        >
                            {periodosDisponiveis.length === 0 && (
                                <option value="">
                                    {carregando
                                        ? "Carregando..."
                                        : "Sem períodos"}
                                </option>
                            )}

                            {periodosDisponiveis.map(
                                (item) => (
                                    <option
                                        key={item.periodo}
                                        value={item.periodo}
                                    >
                                        {formatarPeriodo(item.periodo)}
                                    </option>
                                ),
                            )}
                        </select>
                    </label>
                </div>
            </header>

            {erro && (
                <div
                    className="dashboard__error"
                    role="alert"
                >
                    {erro}
                </div>
            )}

            <section
                className="dashboard__kpis"
                aria-label="Indicadores financeiros"
            >
                {indicadores.map(
                    (indicador) => (
                        <KpiCard
                            key={indicador.titulo}
                            titulo={indicador.titulo}
                            valor={indicador.valor}
                            legenda={indicador.legenda}
                        />
                    ),
                )}
            </section>

            <section className="dashboard__content">
                <article className="dashboard__panel">
                    <header className="dashboard__panel-header">
                        <div>
                            <h2>Evolução trimestral</h2>
                            <p>
                                Receita, EBITDA e lucro líquido
                            </p>
                        </div>
                    </header>

                    <div className="dashboard__placeholder">
                        <div className="dashboard__chart-content">
                            <EvolucaoChart
                                historico={historico}
                                carregando={carregando}
                                erro={erro}
                            />
                        </div>
                    </div>
                </article>

                <article className="dashboard__panel">
                    <header className="dashboard__panel-header">
                        <div>
                            <h2>DRE resumida</h2>
                            <p>
                                Contas de {
                                    periodoAtivo
                                        ? formatarPeriodo(periodoAtivo)
                                        : "—"
                                }
                            </p>
                        </div>
                    </header>

                    <div className="dashboard__dre-content">
                        <DreTable
                            itens={dre}
                            carregando={carregandoDre}
                            erro={erroDre}
                        />
                    </div>
                </article>
            </section>

            <footer className="dashboard__footer">
                Dados públicos da Azzas 2154.
                Projeto independente para estudo e portfólio.
            </footer>
        </div>
    );
}


export default DashboardPage;