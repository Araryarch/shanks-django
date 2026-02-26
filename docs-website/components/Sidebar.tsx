'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

interface NavItem {
  title: string;
  href: string;
  items?: NavItem[];
}

const navigation: { section: string; items: NavItem[] }[] = [
  {
    section: 'Getting Started',
    items: [
      { title: 'Introduction', href: '/docs/getting-started' },
      { title: 'Installation', href: '/docs/installation' },
    ],
  },
  {
    section: 'CLI',
    items: [
      { title: 'Overview', href: '/docs/cli' },
      { title: 'shanks new', href: '/docs/cli/new' },
      { title: 'shanks create', href: '/docs/cli/create' },
      { title: 'shanks generate', href: '/docs/cli/generate' },
      { title: 'shanks run', href: '/docs/cli/run' },
    ],
  },
  {
    section: 'Routing',
    items: [
      { title: 'Overview', href: '/docs/routing' },
      { title: 'Basic Routes', href: '/docs/routing/basic' },
      { title: 'Route Groups', href: '/docs/routing/groups' },
      { title: 'Dynamic Routes', href: '/docs/routing/dynamic' },
      { title: 'HTTP Methods', href: '/docs/routing/methods' },
    ],
  },
  {
    section: 'Middleware',
    items: [
      { title: 'Overview', href: '/docs/middleware' },
      { title: 'Built-in', href: '/docs/middleware/builtin' },
      { title: 'Custom', href: '/docs/middleware/custom' },
      { title: 'CORS', href: '/docs/middleware/cors' },
    ],
  },
  {
    section: 'Authentication',
    items: [
      { title: 'Overview', href: '/docs/authentication' },
      { title: 'JWT Auth', href: '/docs/authentication/jwt' },
      { title: 'Session Auth', href: '/docs/authentication/session' },
      { title: 'Middleware', href: '/docs/authentication/middleware' },
    ],
  },
  {
    section: 'Caching',
    items: [
      { title: 'Overview', href: '/docs/caching' },
      { title: 'Auto Cache', href: '/docs/caching/auto' },
      { title: 'Manual Cache', href: '/docs/caching/manual' },
      { title: 'Invalidation', href: '/docs/caching/invalidation' },
    ],
  },
  {
    section: 'Database (SORM)',
    items: [
      { title: 'Overview', href: '/docs/sorm' },
      { title: 'Setup', href: '/docs/sorm/database' },
      { title: 'Migrations', href: '/docs/sorm/migrations' },
      { title: 'Admin Panel', href: '/docs/sorm/admin' },
    ],
  },
  {
    section: 'ORM Queries',
    items: [
      { title: 'Overview', href: '/docs/orm' },
      { title: 'Models', href: '/docs/orm/models' },
      { title: 'Queries', href: '/docs/orm/queries' },
      { title: 'Relationships', href: '/docs/orm/relationships' },
    ],
  },
  {
    section: 'Configuration',
    items: [
      { title: 'Overview', href: '/docs/configuration' },
      { title: 'Environment', href: '/docs/configuration/env' },
      { title: 'Database', href: '/docs/configuration/database' },
      { title: 'Settings', href: '/docs/configuration/settings' },
    ],
  },
  {
    section: 'Advanced',
    items: [
      { title: 'Swagger / OpenAPI', href: '/docs/swagger' },
    ],
  },
  {
    section: 'Deployment',
    items: [
      { title: 'Overview', href: '/docs/deployment' },
      { title: 'Generate Django', href: '/docs/deployment/generate' },
      { title: 'Heroku', href: '/docs/deployment/heroku' },
      { title: 'Railway', href: '/docs/deployment/railway' },
      { title: 'Docker', href: '/docs/deployment/docker' },
    ],
  },
  {
    section: 'Examples',
    items: [
      { title: 'Overview', href: '/docs/examples' },
      { title: 'Blog API', href: '/docs/examples/blog' },
      { title: 'E-commerce', href: '/docs/examples/ecommerce' },
      { title: 'Real-time Chat', href: '/docs/examples/chat' },
    ],
  },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="sticky top-14 h-[calc(100vh-3.5rem)] w-52 lg:w-60 shrink-0 overflow-y-auto pb-12 hidden md:block border-r border-white/8 pr-5">
      <div className="pt-8 space-y-6">
        {navigation.map((group) => (
          <div key={group.section}>
            {/* Section label */}
            <p className="mb-2 px-2 text-[10px] font-bold uppercase tracking-[0.12em] text-rose-500/60 select-none">
              {group.section}
            </p>
            <ul className="space-y-0.5">
              {group.items.map((item) => {
                const isActive = pathname === item.href;
                return (
                  <li key={item.href}>
                    <Link
                      href={item.href}
                      className={`flex items-center gap-2 px-3 py-1.5 text-[13px] rounded-lg transition-all duration-150 ${
                        isActive
                          ? 'bg-gradient-to-r from-rose-600/20 to-red-600/10 text-rose-300 font-semibold border border-rose-500/20'
                          : 'text-white/40 hover:text-white/80 hover:bg-white/5 font-normal'
                      }`}
                    >
                      {isActive && (
                        <span className="w-1 h-1 rounded-full bg-rose-400 shrink-0" />
                      )}
                      {item.title}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
      </div>
    </aside>
  );
}
