const CMS=process.env.CMS_BASE_URL??"http://localhost:8000";
export async function GET(){const response=await fetch(`${CMS}/api/v1/sitemap.xml`,{next:{revalidate:300}});return new Response(await response.text(),{status:response.status,headers:{"content-type":"application/xml","cache-control":"public, s-maxage=300, stale-while-revalidate=600"}});}
