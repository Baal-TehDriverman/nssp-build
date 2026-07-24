import { cn } from '../lib/utils'
import { 
  Cpu, Memory, HardDrive, Wifi, Thermometer, 
  Activity, TrendingUp, AlertTriangle, CheckCircle,
  Zap, Database, Server, Cloud
} from 'lucide-react'

interface MetricCardProps {
  title: string
  value: string
  unit?: string
  icon: React.ReactNode
  trend?: number
  status?: 'ok' | 'warn' | 'critical'
  color: string
}

function MetricCard({ title, value, unit, icon, trend, status, color }: MetricCardProps) {
  return (
    <div className="glass p-5 rounded-xl border border-border-primary">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-mono text-fg-muted uppercase tracking-wide">{title}</p>
          <div className="flex items-baseline gap-1 mt-1">
            <span className="text-3xl font-bold text-fg-primary">{value}</span>
            {unit && <span className="text-fg-muted">{unit}</span>}
          </div>
          {trend !== undefined && (
            <p className={cn('text-xs font-mono mt-1', trend >= 0 ? 'text-success' : 'text-error')}>
              {trend >= 0 ? '▲' : '▼'} {Math.abs(trend).toFixed(1)}%
            </p>
          )}
        </div>
        <div className={cn('p-2 rounded-lg', color)}>
          {icon}
        </div>
      </div>
      <div className="mt-4 h-1 bg-bg-primary rounded-full overflow-hidden">
        <div 
          className={cn('h-full transition-all duration-500', 
            status === 'critical' ? 'bg-error' : 
            status === 'warn' ? 'bg-warning' : 'bg-success')}
          style={{ width: `${Math.min(100, Math.max(0, parseFloat(value)))}%` }}
        />
      </div>
    </div>
  )
}

export default function SystemPanel() {
  // In real implementation, these would come from WebSocket/System API
  const metrics = [
    { title: 'CPU Usage', value: '34', unit: '%', icon: <Cpu className="w-6 h-6" />, trend: -2.1, status: 'ok', color: 'bg-accent-tertiary/20 text-accent-tertiary' },
    { title: 'GPU Usage', value: '67', unit: '%', icon: <Zap className="w-6 h-6" />, trend: 5.3, status: 'ok', color: 'bg-accent-primary/20 text-accent-primary' },
    { title: 'GPU Memory', value: '8.2', unit: '/ 12 GB', icon: <Memory className="w-6 h-6" />, trend: 1.2, status: 'ok', color: 'bg-accent-primary/20 text-accent-primary' },
    { title: 'RAM Usage', value: '42', unit: '%', icon: <Database className="w-6 h-6" />, trend: -0.5, status: 'ok', color: 'bg-accent-secondary/20 text-accent-secondary' },
    { title: 'Disk Usage', value: '58', unit: '%', icon: <HardDrive className="w-6 h-6" />, trend: 0.1, status: 'ok', color: 'bg-amber-500/20 text-amber-500' },
    { title: 'GPU Temp', value: '62', unit: '°C', icon: <Thermometer className="w-6 h-6" />, trend: 2.0, status: 'ok', color: 'bg-warning/20 text-warning' },
    { title: 'Network RX', value: '1.2', unit: 'MB/s', icon: <Wifi className="w-6 h-6" />, trend: 10, status: 'ok', color: 'bg-cyan-500/20 text-cyan-500' },
    { title: 'Network TX', value: '0.4', unit: 'MB/s', icon: <Server className="w-6 h-6" />, trend: -5, status: 'ok', color: 'bg-cyan-500/20 text-cyan-500' },
  ]

  const services = [
    { name: 'Lilith Gateway', status: 'running', port: 8080, pid: 12451 },
    { name: 'Ollama', status: 'running', port: 11434, pid: 12389 },
    { name: 'vLLM/NIM', status: 'running', port: 8000, pid: 12523 },
    { name: 'ComfyUI', status: 'running', port: 8188, pid: 12601 },
    { name: 'Hermes Gateway', status: 'running', port: 8642, pid: 12402 },
    { name: 'NGD', status: 'running', port: 7687, pid: 12345 },
    { name: 'MSN Router', status: 'running', port: 8081, pid: 12367 },
    { name: 'Lilith Council', status: 'running', port: 8082, pid: 12389 },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold font-mono text-fg-primary">System Overview</h2>
          <p className="text-fg-muted text-sm">Real-time hardware and service monitoring</p>
        </div>
        <div className="flex items-center gap-3">
          <span className="px-3 py-1 glass rounded-lg text-xs font-mono text-success flex items-center gap-1">
            <span className="w-1.5 h-1.5 rounded-full bg-success animate-pulse" />
            LIVE
          </span>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-8 gap-4">
        {metrics.map((m, i) => (
          <MetricCard key={i} {...m} />
        ))}
      </div>

      {/* Detailed Sections */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* GPU Details */}
        <div className="glass p-6 rounded-xl border border-border-primary">
          <h3 className="font-mono text-lg text-fg-primary mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-accent-primary" />
            NVIDIA RTX 3060 (12GB)
          </h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-fg-secondary">GPU Utilization</span>
                <span className="text-fg-primary font-mono">67%</span>
              </div>
              <div className="h-2 bg-bg-primary rounded-full overflow-hidden">
                <div className="h-full bg-accent-primary rounded-full" style={{ width: '67%' }} />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-fg-secondary">Memory Used</span>
                <span className="text-fg-primary font-mono">8.2 / 12 GB (68%)</span>
              </div>
              <div className="h-2 bg-bg-primary rounded-full overflow-hidden">
                <div className="h-full bg-accent-primary rounded-full" style={{ width: '68%' }} />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-fg-muted">Temperature</p>
                <p className="text-fg-primary font-mono text-xl">62°C</p>
              </div>
              <div>
                <p className="text-fg-muted">Power Draw</p>
                <p className="text-fg-primary font-mono text-xl">145W / 170W</p>
              </div>
              <div>
                <p className="text-fg-muted">SM Clock</p>
                <p className="text-fg-primary font-mono text-xl">1785 MHz</p>
              </div>
              <div>
                <p className="text-fg-muted">Memory Clock</p>
                <p className="text-fg-primary font-mono text-xl">875 MHz</p>
              </div>
            </div>
            <div className="grid grid-cols-3 gap-4 text-sm pt-4 border-t border-border-primary">
              <div>
                <p className="text-fg-muted">Processes</p>
                <p className="text-fg-primary font-mono">12</p>
              </div>
              <div>
                <p className="text-fg-muted">Fan Speed</p>
                <p className="text-fg-primary font-mono">52%</p>
              </div>
              <div>
                <p className="text-fg-muted">Driver</p>
                <p className="text-fg-primary font-mono">560.xx</p>
              </div>
            </div>
          </div>
        </div>

        {/* Storage & Filesystems */}
        <div className="glass p-6 rounded-xl border border-border-primary">
          <h3 className="font-mono text-lg text-fg-primary mb-4 flex items-center gap-2">
            <HardDrive className="w-5 h-5 text-accent-secondary" />
            Btrfs Filesystems (nvme0n1p3)
          </h3>
          <div className="space-y-3">
            {[
              { name: '@ (root)', used: '45G', total: '467G', pct: 10, mount: '/' },
              { name: '@home', used: '120G', total: '467G', pct: 26, mount: '/home' },
              { name: '@lilith', used: '12G', total: '467G', pct: 3, mount: '🜏 Lilith/ONE FUCKING DASHBOARD' },
              { name: '@opt', used: '35G', total: '467G', pct: 7, mount: '/opt' },
              { name: '@srv', used: '8G', total: '467G', pct: 2, mount: '/srv' },
              { name: '@var_log', used: '2G', total: '467G', pct: 1, mount: '/var/log' },
              { name: '@var_cache', used: '5G', total: '467G', pct: 1, mount: '/var/cache' },
              { name: '@snapshots', used: '28G', total: '467G', pct: 6, mount: '/.snapshots' },
            ].map((fs, i) => (
              <div key={i} className="space-y-1">
                <div className="flex justify-between text-sm">
                  <span className="text-fg-secondary font-mono">{fs.name}</span>
                  <span className="text-fg-primary">{fs.used} / {fs.total}</span>
                </div>
                <div className="h-1.5 bg-bg-primary rounded-full overflow-hidden">
                  <div 
                    className="h-full rounded-full transition-all duration-500"
                    style={{ 
                      width: `${fs.pct}%`,
                      background: fs.pct > 80 ? 'var(--error)' : fs.pct > 60 ? 'var(--warning)' : 'var(--success)'
                    }}
                  />
                </div>
                <p className="text-xs text-fg-muted font-mono">{fs.mount}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Services Status */}
      <div className="glass p-6 rounded-xl border border-border-primary">
        <h3 className="font-mono text-lg text-fg-primary mb-4 flex items-center gap-2">
          <Activity className="w-5 h-5 text-accent-tertiary" />
          Core Services
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-fg-muted border-b border-border-primary">
                <th className="pb-2 font-mono">Service</th>
                <th className="pb-2 font-mono">Status</th>
                <th className="pb-2 font-mono">Port</th>
                <th className="pb-2 font-mono">PID</th>
                <th className="pb-2 font-mono">Uptime</th>
                <th className="pb-2 font-mono">CPU %</th>
                <th className="pb-2 font-mono">Memory</th>
              </tr>
            </thead>
            <tbody>
              {services.map((svc, i) => (
                <tr key={i} className="border-b border-border-primary/50 hover:bg-bg-tertiary/50">
                  <td className="py-3 font-mono text-fg-secondary">{svc.name}</td>
                  <td className="py-3">
                    <span className={cn(
                      'px-2 py-0.5 rounded text-xs font-mono',
                      svc.status === 'running' ? 'bg-success/20 text-success' : 'bg-error/20 text-error'
                    )}>
                      {svc.status}
                    </span>
                  </td>
                  <td className="py-3 font-mono text-fg-muted">{svc.port}</td>
                  <td className="py-3 font-mono text-fg-muted">{svc.pid}</td>
                  <td className="py-3 font-mono text-fg-muted">2h 34m</td>
                  <td className="py-3 font-mono text-fg-muted">{Math.random() * 5 + 0.5 | 0}%</td>
                  <td className="py-3 font-mono text-fg-muted">{(Math.random() * 500 + 100) | 0} MB</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="flex flex-wrap gap-3">
        {[
          { label: 'Refresh', icon: RefreshCw },
          { label: 'GPU Reset', icon: Zap },
          { label: 'Clear Cache', icon: HardDrive },
          { label: 'Snapshot', icon: Database },
          { label: 'Reboot', icon: AlertTriangle },
        ].map((action, i) => (
          <button key={i} className="px-4 py-2 glass rounded-lg border border-border-primary hover:border-accent-primary hover:text-accent-primary transition-all flex items-center gap-2 text-sm font-mono">
            <action.icon className="w-4 h-4" />
            {action.label}
          </button>
        ))}
      </div>
    </div>
  )
}