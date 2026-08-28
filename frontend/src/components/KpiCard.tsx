import "./KpiCard.css";


type KpiCardProps = {
    titulo: string;
    valor: string;
    legenda: string;
};


function KpiCard({
    titulo,
    valor,
    legenda,
}: KpiCardProps) {
    return (
        <article className="kpi-card">
            <p className="kpi-card__titulo">
                {titulo}
            </p>

            <strong className="kpi-card__valor">
                {valor}
            </strong>

            <p className="kpi-card__legenda">
                {legenda}
            </p>
        </article>
    );
}


export default KpiCard;