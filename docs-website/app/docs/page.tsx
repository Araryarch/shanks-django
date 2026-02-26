import Link from 'next/link';
import { ArrowRight, Zap, Code2, Shield, Rocket, BookOpen, Database, Terminal, Layers } from 'lucide-react';
import { BashBlock } from '@/components/BashBlock';

const features = [
  {
    icon: <Code2 className="h-5 w-5" />,
    label: 'Routing',
    title: 'Express.js-like Routing',
    description: 'Define routes with simple decorators. Group routes by domain. No urls.py, no boilerplate.',
    href: '/docs/routing',
    color: 'text-rose-400',
    bg: 'bg-rose-500/10',
    border: 'border-rose-500/20',
  },
  {
    icon: <Zap className="h-5 w-5" />,
    label: 'Performance',
    title: '10× Faster with Caching',
    description: 'Automatic GET request caching with zero config. Smart invalidation built in.',
    href: '/docs/caching',
    color: 'text-orange-400',
    bg: 'bg-orange-500/10',
    border: 'border-orange-500/20',
  },
  {
    icon: <Database className="h-5 w-5" />,
    label: 'ORM',
    title: 'Prisma-like ORM',
    description: 'Intuitive query syntax: find_many(), find_unique(), create(). Type-hints friendly.',
    href: '/docs/orm',
    color: 'text-pink-400',
    bg: 'bg-pink-500/10',
    border: 'border-pink-500/20',
  },
  {
    icon: <Shield className="h-5 w-5" />,
    label: 'Auth',
    title: 'Built-in Authentication',
    description: 'JWT and session auth ready out of the box. Secure by default, extensible by design.',
    href: '/docs/authentication',
    color: 'text-red-400',
    bg: 'bg-red-500/10',
    border: 'border-red-500/20',
  },
];

const quickLinks = [
  { icon: <Terminal className="h-4 w-4" />, title: 'CLI Reference', desc: 'Generate CRUD, auth & more', href: '/docs/cli', color: 'text-rose-400', bg: 'bg-rose-500/10' },
  { icon: <Layers className="h-4 w-4" />, title: 'SORM / Migrations', desc: 'Database & schema management', href: '/docs/sorm', color: 'text-orange-400', bg: 'bg-orange-500/10' },
  { icon: <Rocket className="h-4 w-4" />, title: 'Deployment', desc: 'Heroku, Railway, Docker', href: '/docs/deployment', color: 'text-pink-400', bg: 'bg-pink-500/10' },
  { icon: <BookOpen className="h-4 w-4" />, title: 'Examples', desc: 'Blog, e-commerce, chat', href: '/docs/examples', color: 'text-red-400', bg: 'bg-red-500/10' },
];

export default function DocsHome() {
  return (
    <div className="pb-20">

      {/* Hero */}
      <div className="mb-12 pt-4">
        {/* Version badge */}
        <div className="inline-flex items-center gap-2 text-[11px] font-bold text-rose-400 bg-rose-500/10 border border-rose-500/20 rounded-full px-3 py-1.5 mb-6 uppercase tracking-widest select-none">
          <span className="relative flex h-1.5 w-1.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-500 opacity-75" />
            <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-rose-500" />
          </span>
          Documentation — v1.0
        </div>

        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-5 leading-tight">
          <span className="bg-gradient-to-br from-white via-rose-100 to-rose-200 bg-clip-text text-transparent">
            Welcome to Shanks
          </span>
        </h1>
        <p className="text-base text-white/50 max-w-lg leading-relaxed mb-8">
          The modern Python framework that brings Express.js-style ergonomics 
          to Django. Fast, typed, and delightful to use.
        </p>
        <div className="flex flex-wrap gap-3">
          <Link
            href="/docs/getting-started"
            className="inline-flex items-center gap-2 px-5 py-2.5 text-sm font-bold text-white bg-gradient-to-r from-rose-600 to-red-500 hover:from-rose-500 hover:to-red-400 rounded-lg transition-all duration-200 shadow-xl shadow-rose-700/30 hover:-translate-y-px group"
          >
            Get started
            <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
          </Link>
          <Link
            href="/docs/cli"
            className="inline-flex items-center gap-2 px-5 py-2.5 text-sm font-semibold text-white/60 hover:text-white bg-white/5 hover:bg-white/10 rounded-lg transition-all duration-200 border border-white/10 hover:border-white/20"
          >
            CLI Reference
          </Link>
        </div>
      </div>

      {/* Quick install terminal */}
      <div className="mb-12">
        <BashBlock code={`$ pip install shanks-django
$ shanks new my_api && cd my_api
$ shanks run`} />
      </div>

      {/* Feature cards */}
      <p className="text-[10px] font-bold uppercase tracking-[0.12em] text-rose-500/60 mb-4">Core Features</p>
      <div className="grid sm:grid-cols-2 gap-4 mb-12">
        {features.map((f) => (
          <Link
            key={f.href}
            href={f.href}
            className={`group relative flex flex-col gap-3 p-5 rounded-xl border ${f.border} bg-white/3 hover:bg-white/5 transition-all duration-200 hover:-translate-y-0.5 overflow-hidden`}
          >
            {/* Top gradient line */}
            <div className={`absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent ${f.color.replace('text-', 'via-')} to-transparent opacity-40 group-hover:opacity-100 transition-opacity`} />
            <div className="flex items-center gap-3">
              <span className={`p-2 rounded-lg ${f.bg} ${f.color}`}>
                {f.icon}
              </span>
              <span className="text-[10px] font-bold uppercase tracking-widest text-white/30">
                {f.label}
              </span>
            </div>
            <div>
              <h3 className={`font-semibold text-[15px] text-white/90 mb-1.5 group-hover:${f.color} transition-colors`}>
                {f.title}
              </h3>
              <p className="text-sm text-white/40 leading-relaxed">
                {f.description}
              </p>
            </div>
            <div className={`mt-auto flex items-center gap-1 text-xs font-semibold text-white/30 group-hover:${f.color} transition-colors`}>
              Explore <ArrowRight className="w-3 h-3 group-hover:translate-x-0.5 transition-transform" />
            </div>
          </Link>
        ))}
      </div>

      {/* Quick links */}
      <p className="text-[10px] font-bold uppercase tracking-[0.12em] text-rose-500/60 mb-4">Explore More</p>
      <div className="grid sm:grid-cols-2 gap-3">
        {quickLinks.map((q) => (
          <Link
            key={q.href}
            href={q.href}
            className="group flex items-center gap-4 p-4 rounded-xl border border-white/8 bg-white/3 hover:bg-white/5 hover:border-white/15 transition-all duration-200"
          >
            <span className={`p-2 rounded-lg ${q.bg} ${q.color} shrink-0`}>
              {q.icon}
            </span>
            <div>
              <p className="text-sm font-semibold text-white/80">{q.title}</p>
              <p className="text-xs text-white/35">{q.desc}</p>
            </div>
            <ArrowRight className="w-4 h-4 text-white/20 group-hover:text-rose-400 ml-auto transition-colors group-hover:translate-x-0.5 transition-transform" />
          </Link>
        ))}
      </div>
    </div>
  );
}
