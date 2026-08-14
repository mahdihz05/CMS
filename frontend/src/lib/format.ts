export function formatToman(value:string|number){
  return `${new Intl.NumberFormat("fa-IR",{maximumFractionDigits:0}).format(Number(value))} تومان`;
}

export function formatPersianDate(value:string){
  return new Intl.DateTimeFormat("fa-IR-u-ca-persian",{year:"numeric",month:"long",day:"numeric"}).format(new Date(value));
}
