import {NextRequest,NextResponse} from "next/server";
const CMS=process.env.CMS_BASE_URL??"http://localhost:8000";
export async function proxy(request:NextRequest){try{const response=await fetch(`${CMS}/api/v1/redirects/resolve/?path=${encodeURIComponent(request.nextUrl.pathname)}`);if(response.ok){const {data}=await response.json();if(data)return NextResponse.redirect(new URL(data.url,request.url),data.status);}}catch{}return NextResponse.next();}
export const config={matcher:["/((?!_next|favicon.ico|sitemap.xml|robots.txt).*)"]};
