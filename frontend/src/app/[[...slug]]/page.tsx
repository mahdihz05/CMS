import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { CardGrid, ContentBlocks } from "@/components/content-blocks";
import { getPage, mediaUrl } from "@/lib/cms";
import { formatPersianDate, formatToman } from "@/lib/format";

type Props={params:Promise<{slug?:string[]}>};
async function load(params:Props["params"]){const {slug=[]}=await params;try{return await getPage(slug.join("/"));}catch{notFound();}}
export async function generateMetadata({params}:Props):Promise<Metadata>{const page=await load(params);const og=page.metadata.openGraph;return {title:page.metadata.title,description:page.metadata.description,alternates:{canonical:page.metadata.canonical},robots:page.metadata.robots,openGraph:{title:og.title,description:og.description,images:og.image?[{url:mediaUrl(og.image.url),width:og.image.width,height:og.image.height,alt:og.image.alt}]:[]}};}

export default async function CmsPage({params}:Props){
  const page=await load(params);const startsWithHero=page.blocks[0]?.type==="hero";
  return <main id="content">
    {page.product?<section className="container product-header">{page.product.image&&<Image src={mediaUrl(page.product.image.url)} width={page.product.image.width} height={page.product.image.height} alt={page.product.image.alt} priority/>}<div><div className="eyebrow">{page.product.category}</div><h1>{page.title}</h1><p className="lede">{page.product.shortDescription}</p><p className="price">{formatToman(page.product.discountPriceToman??page.product.priceToman)}</p>{page.product.discountPriceToman&&<del>{formatToman(page.product.priceToman)}</del>}<p className={`stock ${page.product.available?"in-stock":"out-of-stock"}`}>{page.product.available?"موجود در فروشگاه":"در حال حاضر ناموجود"}</p><Link className="button" href="/contact/">درخواست راهنمایی خرید</Link></div></section>:!startsWithHero&&<header className="container section"><h1>{page.title}</h1>{page.article&&<><p className="lede">{page.article.excerpt}</p><time dateTime={page.article.date}>{formatPersianDate(page.article.date)} · {page.article.author}</time></>}</header>}
    <ContentBlocks blocks={page.blocks} products={page.products} posts={page.posts}/>
    {page.products&&page.products.length>0&&<section className="container section"><CardGrid cards={page.products}/></section>}
    {page.posts&&page.posts.length>0&&<section className="container section"><CardGrid cards={page.posts}/></section>}
    {page.form&&<section className="container section"><form className="contact-form" action="/api/contact" method="post"><input type="hidden" name="pageId" value={page.form.pageId}/>{page.form.fields.map((field)=><p key={field.name}><label>{field.label}{field.required&&<span aria-hidden="true"> *</span>}{field.type==="multiline"?<textarea name={field.name} required={field.required} rows={6}/>:<input name={field.name} type={field.type==="email"?"email":"text"} required={field.required}/>}</label></p>)}<button className="button" type="submit">ارسال پیام</button></form></section>}
    <script type="application/ld+json" dangerouslySetInnerHTML={{__html:JSON.stringify(page.schemas).replace(/</g,"\\u003c")}}/>
  </main>;
}
