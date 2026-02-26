import Link from 'next/link'
import { Header } from '@/components/Header'
import { CodeBlock } from '@/components/CodeBlock'
import {
  ArrowRight, Zap, Database,
  Code2, Cpu, Boxes, Layers
} from 'lucide-react'

const features = [
  {
    icon: <Code2 className="w-5 h-5" />,
    title: "Express-style Routing",
    description: "Define routes with clean decorators. Group by domain. Zero urls.py.",
    color: "text-rose-400",
    bg: "bg-rose-500/10",
    border: "border-rose-500/20",
    glow: "group-hover:shadow-rose-500/20",
  },
  {
    icon: <Zap className="w-5 h-5" />,
    title: "10× Auto Caching",
    description: "Smart GET caching with zero configuration. Instant speed boost.",
    color: "text-orange-400",
    bg: "bg-orange-500/10",
    border: "border-orange-500/20",
    glow: "group-hover:shadow-orange-500/20",
  },
  {
    icon: <Database className="w-5 h-5" />,
    title: "Prisma-like ORM",
    description: "find_many(), find_unique(), create() — clean, typed, modern.",
    color: "text-pink-400",
    bg: "bg-pink-500/10",
    border: "border-pink-500/20",
    glow: "group-hover:shadow-pink-500/20",
  },
  {
    icon: <Cpu className="w-5 h-5" />,
    title: "CLI Generator",
    description: "Scaffold CRUD, auth, and entire modules with one command.",
    color: "text-rose-300",
    bg: "bg-rose-400/10",
    border: "border-rose-400/20",
    glow: "group-hover:shadow-rose-400/20",
  },
  {
    icon: <Layers className="w-5 h-5" />,
    title: "Go-like Architecture",
    description: "Organize code by domain, not by Django's rigid app structure.",
    color: "text-red-400",
    bg: "bg-red-500/10",
    border: "border-red-500/20",
    glow: "group-hover:shadow-red-500/20",
  },
  {
    icon: <Boxes className="w-5 h-5" />,
    title: "Familiar Middleware",
    description: "req, res, next pattern. Easy to read and compose.",
    color: "text-orange-300",
    bg: "bg-orange-400/10",
    border: "border-orange-400/20",
    glow: "group-hover:shadow-orange-400/20",
  },
]

export default function Home() {
  return (
    <div className="min-h-screen bg-[#0a0608] text-white antialiased overflow-x-hidden">

      {/* ── Mesh gradient background ─────────────── */}
      <div className="fixed inset-0 -z-10 pointer-events-none">
        {/* Primary red orb */}
        <div className="absolute top-[-20%] left-[10%] w-[700px] h-[700px] bg-rose-600/25 rounded-full blur-[140px]" />
        {/* Secondary warm orb */}
        <div className="absolute top-[30%] right-[-10%] w-[500px] h-[500px] bg-orange-600/15 rounded-full blur-[120px]" />
        {/* Bottom crimson orb */}
        <div className="absolute bottom-[-10%] left-[30%] w-[600px] h-[600px] bg-red-700/20 rounded-full blur-[130px]" />
        {/* Subtle grid */}
        <div
          className="absolute inset-0 opacity-[0.04]"
          style={{
            backgroundImage: 'radial-gradient(circle, #f87171 1px, transparent 1px)',
            backgroundSize: '32px 32px',
          }}
        />
        {/* Noise vignette */}
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-[#0a0608]/80" />
      </div>

      <Header />

      <main>
        {/* ── Hero ────────────────────────────────── */}
        <section className="max-w-5xl mx-auto px-6 pt-28 pb-16 text-center">

          {/* Badge */}
          <div className="inline-flex items-center gap-2 text-xs font-semibold text-rose-300 bg-rose-500/10 border border-rose-500/25 rounded-full px-4 py-2 mb-10 select-none backdrop-blur-sm">
            <span className="relative flex h-1.5 w-1.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-rose-400" />
            </span>
            Now in beta · v1.0.0-beta
          </div>

          {/* Headline */}
          <h1 className="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-black tracking-tight leading-[1.0] mb-8">
            <span className="bg-gradient-to-br from-white via-rose-100 to-rose-200 bg-clip-text text-transparent">
              Express.js
            </span>
            <br />
            <span className="bg-gradient-to-r from-rose-400 via-red-400 to-orange-400 bg-clip-text text-transparent">
              ergonomics
            </span>
            <br />
            <span className="text-white/50 text-4xl sm:text-5xl md:text-6xl font-bold">
              for Django.
            </span>
          </h1>

          <p className="text-base md:text-lg text-white/50 max-w-xl mx-auto leading-relaxed mb-10">
            No{' '}
            <code className="text-rose-400 font-mono text-[0.9em] bg-rose-500/10 px-1.5 py-0.5 rounded border border-rose-500/20">
              urls.py
            </code>
            . No boilerplate. Clean routing, auto-caching, Prisma-like ORM, and powerful CLI.{' '}
            <span className="text-white font-semibold">10× faster</span> out of the box.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
            <Link
              href="/docs/getting-started"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-4 text-sm font-bold text-white bg-gradient-to-r from-rose-600 to-red-500 hover:from-rose-500 hover:to-red-400 rounded-xl transition-all duration-200 shadow-2xl shadow-rose-700/40 hover:shadow-rose-600/50 hover:-translate-y-0.5 group"
            >
              Start building
              <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
            </Link>
            <Link
              href="/docs"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-4 text-sm font-semibold text-white/70 hover:text-white bg-white/5 hover:bg-white/10 rounded-xl transition-all duration-200 border border-white/10 hover:border-white/20 backdrop-blur-sm"
            >
              Read the docs
            </Link>
          </div>
        </section>

        {/* ── Code block ──────────────────────────── */}
        <section className="max-w-3xl mx-auto px-6 pb-28">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-rose-600/20 to-orange-600/20 rounded-3xl blur-2xl scale-95" />
            <div className="relative">
              <CodeBlock
                filename="internal/routes/__init__.py"
                language="python"
                code={`from shanks import App, auto_cache

app = App()
app.use(auto_cache)  # 10x faster 🚀

@app.get("api/posts")
def list_posts(req):
    return { "posts": [] }`}
              />
            </div>
          </div>
        </section>

        {/* ── Features ────────────────────────────── */}
        <section className="max-w-5xl mx-auto px-6 pb-32">
          {/* Section header */}
          <div className="text-center mb-14">
            <p className="text-xs font-semibold uppercase tracking-widest text-rose-400/60 mb-3">Features</p>
            <h2 className="text-3xl md:text-4xl lg:text-5xl font-black tracking-tight mb-4">
              <span className="bg-gradient-to-r from-white to-white/60 bg-clip-text text-transparent">
                Everything you need.
              </span>
            </h2>
            <p className="text-white/40 text-base max-w-md mx-auto">
              Built for speed, clarity, and developer happiness.
            </p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {features.map((f, i) => (
              <div
                key={i}
                className={`group relative p-6 rounded-2xl border ${f.border} bg-white/3 hover:bg-white/5 backdrop-blur-sm transition-all duration-300 hover:-translate-y-1 hover:shadow-xl ${f.glow} overflow-hidden`}
              >
                {/* Gradient top line */}
                <div className={`absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent ${f.color.replace('text-', 'via-')} to-transparent opacity-50 group-hover:opacity-100 transition-opacity`} />
                <span className={`inline-flex p-2.5 rounded-xl ${f.bg} ${f.color} mb-4 group-hover:scale-110 transition-transform duration-300`}>
                  {f.icon}
                </span>
                <h3 className="font-bold text-[15px] text-white/90 mb-2">{f.title}</h3>
                <p className="text-sm text-white/40 leading-relaxed">{f.description}</p>
              </div>
            ))}
          </div>
        </section>

        {/* ── CTA banner ───────────────────────────── */}
        <section className="max-w-5xl mx-auto px-6 pb-28">
          <div className="relative rounded-3xl overflow-hidden p-10 md:p-14 text-center">
            <div className="absolute inset-0 bg-gradient-to-br from-rose-600/30 via-red-600/20 to-orange-600/15" />
            <div className="absolute inset-0 border border-rose-500/20 rounded-3xl" />
            <div className="absolute top-0 left-1/4 right-1/4 h-px bg-gradient-to-r from-transparent via-rose-400/50 to-transparent" />
            <div className="relative z-10">
              <h2 className="text-3xl md:text-4xl font-black mb-4">
                <span className="bg-gradient-to-r from-rose-300 to-orange-300 bg-clip-text text-transparent">
                  Ready to build faster?
                </span>
              </h2>
              <p className="text-white/50 mb-8 max-w-sm mx-auto">
                Get started in seconds. Install with pip and create your first API.
              </p>
              <Link
                href="/docs/getting-started"
                className="inline-flex items-center gap-2 px-8 py-4 text-sm font-bold text-white bg-gradient-to-r from-rose-600 to-red-500 hover:from-rose-500 hover:to-red-400 rounded-xl transition-all duration-200 shadow-2xl shadow-rose-700/50 hover:-translate-y-0.5 group"
              >
                Get started free
                <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
              </Link>
            </div>
          </div>
        </section>
      </main>

      {/* ── Footer ──────────────────────────────── */}
      <footer className="border-t border-white/8">
        <div className="max-w-5xl mx-auto px-6 py-10 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm">
          <span className="font-black tracking-tight text-white">
            SHANKS<span className="text-rose-500">.</span>
          </span>
          <p className="text-white/30 text-center">
            MIT License · Built with ❤ for Django developers
          </p>
          <div className="flex gap-5 text-white/40">
            <Link href="/docs" className="hover:text-white transition-colors">Docs</Link>
            <a href="https://github.com/Araryarch/shanks-django" className="hover:text-white transition-colors">GitHub</a>
          </div>
        </div>
      </footer>
    </div>
  )
}
