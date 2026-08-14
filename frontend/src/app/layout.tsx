import type { Metadata } from "next";
import Link from "next/link";
import { getNavigation, getSiteSettings } from "@/lib/cms";
import "./globals.css";

export const metadata: Metadata = { title: { default: "ویژنا | فروشگاه تخصصی عینک", template: "%s" }, description: "عینک آفتابی، فریم طبی، بلوکات و ورزشی ویژنا" };

export default async function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  const [navigation, settings] = await Promise.all([getNavigation(), getSiteSettings()]);
  return <html lang="fa" dir="rtl"><body>
    <a className="skip-link" href="#content">رفتن به محتوای اصلی</a>
    <header className="site-header"><div className="container header-inner"><Link className="brand" href="/" aria-label={`خانه ${settings.siteName}`}>{settings.siteName}</Link><nav aria-label="فهرست اصلی"><ul>{(navigation.header ?? []).map((item) => <li key={`${item.label}-${item.url}`}><Link href={item.url}>{item.label}</Link></li>)}</ul></nav></div></header>
    {children}
    <footer className="site-footer"><div className="container footer-grid"><div><div className="brand">{settings.siteName}</div><p>{settings.address}</p><p><a href={`tel:${settings.phone}`}>{settings.phone}</a></p><a href={`mailto:${settings.email}`}>{settings.email}</a></div><nav aria-label="فهرست پایین سایت"><ul>{(navigation.footer ?? []).map((item) => <li key={`${item.label}-${item.url}`}><Link href={item.url}>{item.label}</Link></li>)}</ul></nav></div></footer>
  </body></html>;
}
