import { CodeBlock } from './CodeBlock';
import { Callout } from './Callout';

interface DocPageProps {
  title: string;
  description: string;
  children: React.ReactNode;
}

export function DocPage({ title, description, children }: DocPageProps) {
  return (
    <div className="prose max-w-none">
      <h1>{title}</h1>
      <p className="lead">{description}</p>
      {children}
    </div>
  );
}

export { CodeBlock, Callout };
