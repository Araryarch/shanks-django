import { H1, Lead, Card } from '@/components/Typography'

export default function DocsPage() {
  return (
    <div>
      <H1>Documentation</H1>
      <Lead>Everything you need to know about Shanks Django.</Lead>
      
      <div className="space-y-3">
        <Card
          href="/docs/getting-started"
          badge="START HERE"
          title="Getting Started"
          description="Learn the basics and create your first Shanks app"
        />
        
        <Card
          href="/docs/routing"
          badge="CORE"
          title="Routing"
          description="Simple routing with grouping like Gin/Express"
        />
        
        <Card
          href="/docs/orm"
          badge="DATABASE"
          title="ORM"
          description="Prisma-like ORM syntax for Django models"
        />
      </div>
    </div>
  )
}
