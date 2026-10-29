import { NavLink, Link } from 'react-router-dom'
import { Activity, LayoutDashboard, Users, ClipboardList, FilePlus2, ListTodo, ChartNoAxesCombined, HeartPulse, Search, Bell, ChevronRight, CircleHelp } from 'lucide-react'
import type { ReactNode } from 'react'

const nav = [
  {to:'/',label:'Dashboard',icon:LayoutDashboard},
  {to:'/queue',label:'Care coordination queue',icon:Users},
  {to:'/intake',label:'Discharge intake',icon:FilePlus2},
  {to:'/tasks',label:'Tasks & follow-ups',icon:ListTodo},
  {to:'/outcomes',label:'Outcomes',icon:ChartNoAxesCombined},
]
export function Shell({children}:{children:ReactNode}){
 return <div className="app-shell"><aside className="sidebar"><Link to="/" className="brand"><span className="brand-mark"><HeartPulse size={23}/></span><span><b>Stepwise Care</b><small>AI care coordination</small></span></Link><div className="workspace-label">WORKSPACE</div><nav>{nav.map(({to,label,icon:Icon})=><NavLink end={to==='/'} key={to} to={to} className={({isActive})=>`nav-link ${isActive?'active':''}`}><Icon size={18}/><span>{label}</span>{label==='Care coordination queue'&&<span className="nav-count">7</span>}</NavLink>)}</nav><div className="sidebar-bottom"><div className="help-card"><CircleHelp size={18}/><div><b>Need a hand?</b><small>View the coordinator guide</small></div><ChevronRight size={15}/></div><div className="user-card"><div className="avatar">SC</div><div><b>Sarah Chen</b><small>Care coordinator</small></div><span className="online-dot"/></div></div></aside><main className="main-area"><header className="topbar"><div className="breadcrumb">Workspace <ChevronRight size={14}/> <b>Care coordination</b></div><div className="top-actions"><span className="environment"><span/> Demo environment</span><button className="icon-button" aria-label="Notifications"><Bell size={18}/><i/></button><div className="avatar small">SC</div></div></header><div className="page-content">{children}</div><footer className="footer"><span><Activity size={14}/> Stepwise Care <span className="footer-sep">•</span> Demo workspace</span><span>Human review required for all AI-generated care plans</span></footer></main></div>
}
export function PageHeading({eyebrow,title,subtitle,action}:{eyebrow?:string;title:string;subtitle?:string;action?:ReactNode}){
 return <div className="page-heading"><div>{eyebrow&&<div className="eyebrow">{eyebrow}</div>}<h1>{title}</h1>{subtitle&&<p>{subtitle}</p>}</div>{action&&<div className="heading-action">{action}</div>}</div>
}
export function RiskBadge({risk}:{risk:string}){return <span className={`badge risk-${risk.toLowerCase()}`}><span/> {risk} risk</span>}
export function StatusBadge({status}:{status:string}){return <span className={`status-badge status-${status.toLowerCase().replaceAll(' ','-')}`}>{status}</span>}
export function SectionTitle({title,subtitle,action}:{title:string;subtitle?:string;action?:ReactNode}){return <div className="section-title"><div><h2>{title}</h2>{subtitle&&<p>{subtitle}</p>}</div>{action}</div>}
export function SearchBox({value,onChange,placeholder='Search patients...'}:{value:string;onChange:(v:string)=>void;placeholder?:string}){return <label className="search-box"><Search size={17}/><input value={value} onChange={e=>onChange(e.target.value)} placeholder={placeholder}/></label>}
