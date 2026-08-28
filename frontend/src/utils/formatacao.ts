export function formatarMilhoes(
  valor: number,
): string {
  const valorFormatado = (
    new Intl.NumberFormat(
      "pt-BR",
      {
        style: "currency",
        currency: "BRL",
        minimumFractionDigits: 1,
        maximumFractionDigits: 1,
      },
    )
    .format(valor)
  );

  return `${valorFormatado} mi`;
}


export function formatarPercentual(
  valor: number,
): string {
  return new Intl.NumberFormat(
    "pt-BR",
    {
      style: "percent",
      minimumFractionDigits: 1,
      maximumFractionDigits: 1,
    },
  ).format(valor);
}
export function formatarPeriodo(
  periodo: string,
): string {
  const correspondencia = (
    /^([1-4])Q([0-9]{2})$/.exec(periodo)
  );

  if (!correspondencia) {
    return periodo;
  }

  const trimestre = Number(
    correspondencia[1]
  );

  const ano = (
    2000
    + Number(correspondencia[2])
  );

  return (
    `${trimestre}º Trimestre ${ano}`
  );
}