import {
    Bar,
    CartesianGrid,
    ComposedChart,
    Legend,
    Line,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from "recharts";

import type {
    KpiTrimestral,
} from "../types/financeiro";

import {
    formatarMilhoes,
    formatarPeriodo,
} from "../utils/formatacao";


interface EvolucaoChartProps {
    historico: KpiTrimestral[];
    carregando: boolean;
    erro: string | null;
}


function formatarPeriodoCurto(
    periodo: string,
): string {
    return periodo.replace("Q", "T");
}


export function EvolucaoChart({
    historico,
    carregando,
    erro,
}: EvolucaoChartProps) {
    if (carregando) {
        return (
            <p aria-live="polite">
                Carregando histórico...
            </p>
        );
    }

    if (erro) {
        return (
            <p role="alert">
                Não foi possível carregar o histórico.
            </p>
        );
    }

    if (historico.length === 0) {
        return (
            <p>
                Nenhum histórico disponível.
            </p>
        );
    }

    return (
        <ResponsiveContainer
            width="100%"
            height={300}
        >
            <ComposedChart
                data={historico}
                margin={{
                    top: 16,
                    right: 8,
                    bottom: 0,
                    left: 0,
                }}
                accessibilityLayer
            >
                <CartesianGrid
                    strokeDasharray="3 3"
                    vertical={false}
                />

                <XAxis
                    dataKey="periodo"
                    tickFormatter={formatarPeriodoCurto}
                    tickLine={false}
                    axisLine={false}
                    minTickGap={16}
                />

                <YAxis
                    yAxisId="receita"
                    tickFormatter={(valor) => (
                        `${valor / 1000} bi`
                    )}
                    tickLine={false}
                    axisLine={false}
                />

                <YAxis
                    yAxisId="resultados"
                    orientation="right"
                    tickFormatter={(valor) => (
                        `${valor} mi`
                    )}
                    tickLine={false}
                    axisLine={false}
                />

                <Tooltip
                    labelFormatter={(periodo) => (
                        formatarPeriodo(String(periodo))
                    )}
                    formatter={(valor) => (
                        formatarMilhoes(Number(valor))
                    )}
                />

                <Legend />

                <Bar
                    yAxisId="receita"
                    dataKey="receita_liquida"
                    name="Receita líquida"
                    fill="var(--color-primary)"
                    radius={[4, 4, 0, 0]}
                />

                <Line
                    yAxisId="resultados"
                    type="monotone"
                    dataKey="ebitda"
                    name="EBITDA"
                    stroke="var(--color-positive)"
                    strokeWidth={2}
                    dot={false}
                />

                <Line
                    yAxisId="resultados"
                    type="monotone"
                    dataKey="lucro_liquido"
                    name="Lucro líquido"
                    stroke="var(--color-negative)"
                    strokeWidth={2}
                    dot={false}
                />
            </ComposedChart>
        </ResponsiveContainer>
    );
}