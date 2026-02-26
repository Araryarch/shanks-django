'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Github, BookOpen } from 'lucide-react'

export function Header() {
  const pathname = usePathname()
  const isDocsPage = pathname.startsWith('/docs')

  return (
    <header className="sticky top-0 z-50 h-14 w-full border-b border-white/8 bg-black/40 backdrop-blur-xl">
      {/* Gradient line at the top of header */}
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-rose-500/50 to-transparent" />
      
      <div className="max-w-7xl mx-auto h-full px-4 sm:px-6 flex items-center justify-between gap-4">

        {/* Logo */}
        <Link href="/" className="flex items-center shrink-0 group">
          <span className="text-[16px] font-black tracking-tight text-white group-hover:text-rose-300 transition-colors duration-200">
            SHANKS
          </span>
          <span className="text-[16px] font-black text-rose-500 group-hover:text-rose-400 transition-colors duration-200">.</span>
        </Link>

        {/* Center pill nav */}
        <nav className="hidden md:flex items-center gap-1 px-1.5 py-1.5 rounded-full bg-white/5 border border-white/10">
          <Link
            href="/"
            className={`px-4 py-1.5 text-xs font-semibold rounded-full transition-all duration-200 ${
              pathname === '/'
                ? 'bg-gradient-to-r from-rose-600 to-red-500 text-white shadow-md shadow-rose-700/30'
                : 'text-white/50 hover:text-white'
            }`}
          >
            Home
          </Link>
          <Link
            href="/docs"
            className={`px-4 py-1.5 text-xs font-semibold rounded-full transition-all duration-200 ${
              isDocsPage
                ? 'bg-gradient-to-r from-rose-600 to-red-500 text-white shadow-md shadow-rose-700/30'
                : 'text-white/50 hover:text-white'
            }`}
          >
            Docs
          </Link>
        </nav>

        {/* Right side */}
        <div className="flex items-center gap-2.5">
          <a
            href="https://github.com/Araryarch/shanks-django"
            target="_blank"
            rel="noopener noreferrer"
            className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-white/50 hover:text-white border border-white/10 hover:border-white/20 rounded-full bg-white/3 hover:bg-white/8 transition-all duration-200"
          >
            <Github className="w-3.5 h-3.5" />
            GitHub
          </a>
          <Link
            href="/docs/getting-started"
            className="inline-flex items-center gap-1.5 px-4 py-2 text-xs font-bold text-white bg-gradient-to-r from-rose-600 to-red-500 hover:from-rose-500 hover:to-red-400 rounded-full transition-all duration-200 shadow-lg shadow-rose-700/30"
          >
            <BookOpen className="w-3.5 h-3.5" />
            Get started
          </Link>
        </div>
      </div>
    </header>
  )
}
