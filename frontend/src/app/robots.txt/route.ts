const CMS=process.env.CMS_BASE_URL??"http://localhost:8000";
export async function GET(){const response=await fetch(`${CMS}/api/v1/robots.txt`,{next:{revalidate:300}});return new Response(await response.text(),{status:response.status,headers:{"content-type":"text/plain","cache-control":"public, s-maxage=300"}});}
