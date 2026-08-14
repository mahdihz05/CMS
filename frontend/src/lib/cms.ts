import type { MenuItem, PageData } from "./types";
const CMS = process.env.CMS_BASE_URL ?? "http://localhost:8000";
const revalidate = Number(process.env.API_REVALIDATE_SECONDS ?? 60);
async function api<T>(path:string):Promise<T> { const response=await fetch(`${CMS}/api/v1${path}`,{next:{revalidate},headers:{Accept:"application/json"}}); if(!response.ok) throw new Error(`CMS request failed (${response.status}) for ${path}`); return (await response.json()).data as T; }
export async function getPage(path:string){ return api<PageData>(`/pages/resolve/?path=${encodeURIComponent(path)}`); }
export async function getNavigation(){ try{return await api<Record<string,MenuItem[]>>("/navigation/");}catch{return {};} }
export async function getSiteSettings(){ try{return await api<{siteName:string;phone:string;email:string;address:string;locale:string;direction:"rtl";currency:{code:string;label:string;schemaCode:string;schemaMultiplier:number}}>("/site-settings/");}catch{return {siteName:"ویژنا",phone:"",email:"",address:"",locale:"fa-IR",direction:"rtl" as const,currency:{code:"IRT",label:"تومان",schemaCode:"IRR",schemaMultiplier:10}};} }
export function mediaUrl(url:string){ return url.startsWith("http")?url:`${CMS}${url}`; }
