import Image from "next/image";
import Link from "next/link";
import { mediaUrl } from "@/lib/cms";
import { formatPersianDate, formatToman } from "@/lib/format";
import type { Block, Card, ImageData } from "@/lib/types";

function CmsImage({ value, priority=false }:{value:ImageData;priority?:boolean}) { return value?<Image src={mediaUrl(value.url)} width={value.width} height={value.height} alt={value.alt} priority={priority} sizes="(max-width: 760px) 100vw, 50vw"/>:null; }
function Cards({cards}:{cards:Card[]}) { return <div className="grid">{cards.map((card)=><article className="card" key={card.id}><CmsImage value={card.image??null}/><div className="card-body">{card.category&&<span className="card-category">{card.category}</span>}<h3><Link href={card.url}>{card.title}</Link></h3><p>{card.excerpt??card.description}</p>{card.date&&<time dateTime={card.date}>{formatPersianDate(card.date)}</time>}{card.priceToman&&<p className="price">{formatToman(card.priceToman)}</p>}</div></article>)}</div>; }

export function ContentBlocks({blocks,products=[],posts=[]}:{blocks:Block[];products?:Card[];posts?:Card[]}) {
  return <>{blocks.map((block)=>{ const value=block.value as Record<string,unknown>;
    if(block.type==="hero") return <section className="hero" key={block.id}><div className="container hero-layout"><div className="hero-inner">{Boolean(value.eyebrow)&&<div className="eyebrow">{String(value.eyebrow)}</div>}<h1>{String(value.heading)}</h1><p className="lede">{String(value.text??"")}</p>{Boolean(value.cta_page)&&<Link className="button" href={(value.cta_page as {url:string}).url}>{String(value.cta_label)}</Link>}</div>{Boolean(value.image)&&<CmsImage value={value.image as ImageData} priority/>}</div></section>;
    if(block.type==="rich_text") return <section className="section" key={block.id}><div className="container rich-text" dangerouslySetInnerHTML={{__html:String(block.value)}}/></section>;
    if(block.type==="features") return <section className="section" key={block.id}><div className="container features">{(block.value as Array<{title:string;text:string}>).map((item)=><div className="feature" key={item.title}><h3>{item.title}</h3><p>{item.text}</p></div>)}</div></section>;
    if(block.type==="testimonials") return <section className="section" key={block.id}><div className="container grid">{(block.value as Array<{quote:string;author:string}>).map((item)=><blockquote className="quote" key={item.author}>“{item.quote}”<footer>— {item.author}</footer></blockquote>)}</div></section>;
    if(block.type==="image_text") return <section className="section" key={block.id}><div className="container image-text"><CmsImage value={value.image as ImageData}/><div><h2>{String(value.heading)}</h2><div dangerouslySetInnerHTML={{__html:String(value.text)}}/></div></div></section>;
    if(block.type==="product_grid") return <section className="section" key={block.id}><div className="container"><h2>{String(value.heading||"محصولات ویژه")}</h2><Cards cards={(value.pages as Card[])??products}/></div></section>;
    if(block.type==="category_grid") return <section className="section" key={block.id}><div className="container"><h2>{String(value.heading||"دسته‌بندی‌ها")}</h2><div className="grid">{(value.categories as Array<{id:number;name:string;description:string;image:ImageData}>).map((item)=><article className="card" key={item.id}><CmsImage value={item.image}/><div className="card-body"><h3>{item.name}</h3><p>{item.description}</p></div></article>)}</div></div></section>;
    if(block.type==="blog_grid") return <section className="section" key={block.id}><div className="container"><h2>{String(value.heading||"راهنماها")}</h2><Cards cards={(value.pages as Card[])??posts}/></div></section>;
    if(block.type==="cta") return <section className="section" key={block.id}><div className="container"><h2>{String(value.heading)}</h2><p>{String(value.text??"")}</p>{Boolean(value.page)&&<Link className="button" href={(value.page as {url:string}).url}>{String(value.label)}</Link>}</div></section>;
    return null;
  })}</>;
}
export function CardGrid({cards}:{cards:Card[]}) { return <Cards cards={cards}/>; }
