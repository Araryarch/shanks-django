import { Sidebar } from '@/components/Sidebar';
import { Header } from '@/components/Header';

export default function DocsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-[#0a0608] text-white antialiased">
      {/* Subtle red mesh glow for docs */}
      <div className="fixed inset-0 -z-10 pointer-events-none">
        <div className="absolute top-0 right-[5%] w-[500px] h-[500px] bg-rose-700/12 rounded-full blur-[130px]" />
        <div className="absolute bottom-[10%] left-[5%] w-[400px] h-[400px] bg-red-800/10 rounded-full blur-[120px]" />
      </div>

      <Header />

      <div className="max-w-7xl mx-auto flex px-4 sm:px-6">
        <Sidebar />
        <main className="flex-1 min-w-0 py-10 md:pl-12 lg:pl-16 max-w-4xl">
          {children}
        </main>
      </div>
    </div>
  );
}
