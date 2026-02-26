import { AlertCircle, CheckCircle, Info, AlertTriangle } from 'lucide-react';

interface CalloutProps {
  type?: 'info' | 'warning' | 'error' | 'success';
  title?: string;
  children: React.ReactNode;
}

export function Callout({ type = 'info', title, children }: CalloutProps) {
  const styles = {
    info: {
      container: { backgroundColor: 'rgba(137, 180, 250, 0.1)', borderColor: 'var(--ctp-blue)' },
      icon: <Info className="h-5 w-5" style={{ color: 'var(--ctp-blue)' }} />,
      title: { color: 'var(--ctp-blue)' },
      text: { color: 'var(--ctp-text)' },
    },
    warning: {
      container: { backgroundColor: 'rgba(249, 226, 175, 0.1)', borderColor: 'var(--ctp-yellow)' },
      icon: <AlertTriangle className="h-5 w-5" style={{ color: 'var(--ctp-yellow)' }} />,
      title: { color: 'var(--ctp-yellow)' },
      text: { color: 'var(--ctp-text)' },
    },
    error: {
      container: { backgroundColor: 'rgba(243, 139, 168, 0.1)', borderColor: 'var(--ctp-red)' },
      icon: <AlertCircle className="h-5 w-5" style={{ color: 'var(--ctp-red)' }} />,
      title: { color: 'var(--ctp-red)' },
      text: { color: 'var(--ctp-text)' },
    },
    success: {
      container: { backgroundColor: 'rgba(166, 227, 161, 0.1)', borderColor: 'var(--ctp-green)' },
      icon: <CheckCircle className="h-5 w-5" style={{ color: 'var(--ctp-green)' }} />,
      title: { color: 'var(--ctp-green)' },
      text: { color: 'var(--ctp-text)' },
    },
  };

  const style = styles[type];

  return (
    <div className="my-6 flex gap-3 rounded-lg border p-4" style={style.container}>
      <div className="flex-shrink-0">{style.icon}</div>
      <div className="flex-1">
        {title && <div className="mb-1 font-semibold" style={style.title}>{title}</div>}
        <div className="text-sm" style={style.text}>{children}</div>
      </div>
    </div>
  );
}
