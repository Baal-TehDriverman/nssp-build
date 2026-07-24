import { useState, useEffect } from 'react'
import { 
  LayoutDashboard, 
  Cpu, 
  Brain, 
  Users, 
  GitBranch, 
  Scale, 
  Image, 
  Gamepad2, 
  Key, 
  Globe, 
  Settings, 
  Terminal,
  Menu,
  X,
  ChevronLeft,
  ChevronRight,
  Zap,
  Database,
  Shield,
  Network,
  Music,
  Video,
  FileText,
  Search,
  RefreshCw,
  Settings as SettingsIcon,
  Power,
  Bell,
  Moon,
  Sun
} from 'lucide-react'
import { cn } from './lib/utils'
import SystemPanel from './panels/SystemPanel'
import AIPanel from './panels/AIPanel'
import AgentPanel from './panels/AgentPanel'
import DevPanel from './panels/DevPanel'
import LegalPanel from './panels/LegalPanel'
import MediaPanel from './panels/MediaPanel'
import GamePanel from './panels/GamePanel'
import CryptoPanel from './panels/CryptoPanel'
import NetworkPanel from './panels/NetworkPanel'
import ConfigPanel from './panels/ConfigPanel'
import TerminalPanel from './panels/TerminalPanel'

const PANELS = [
  { id: 'sys', label: 'SYS', icon: LayoutDashboard, component: SystemPanel, color: 'text-accent-tertiary' },
  { id: 'ai', label: 'AI', icon: Brain, component: AIPanel, color: 'text-accent-primary' },
  { id: 'agt', label: 'AGT', icon: Users, component: AgentPanel, color: 'text-accent-secondary' },
  { id: 'dev', label: 'DEV', icon: GitBranch, component: DevPanel, color: 'text-green-400' },
  { id: 'lgl', label: 'LGL', icon: Scale, component: LegalPanel, color: 'text-amber-400' },
  { id: 'med', label: 'MED', icon: Image, component: MediaPanel, color: 'text-pink-400' },
  { id: 'gam', label: 'GAM', icon: Gamepad2, component: GamePanel, color: 'text-orange-400' },
  { id: 'cry', label: 'CRY', icon: Key, component: CryptoPanel, color: 'text-yellow-400' },
  { id: 'net', label: 'NET', icon: Globe, component: NetworkPanel, color: 'text-cyan-400' },
  { id: 'cfg', label: 'CFG', icon: Settings, component: ConfigPanel, color: 'text-gray-400' },
  { id: 'term', label: 'TERM', icon: Terminal, component: TerminalPanel, color: 'text-green-300' },
]

function Sidebar({ isOpen, onToggle, activePanel, setActivePanel }) {
  return (
    <aside className={cn(
      'fixed left-0 top-0 z-50 h-full glass-strong transition-all duration-300',
      isOpen ? 'w-64' : 'w-16'
    )}>
      <div className="flex flex-col h-full">
        {/* Logo */}
        <div className="flex items-center justify-between h-16 px-4 border-b border-border-primary">
          <div className="flex items-center gap-3">
            <span className="text-2xl font-mono text-accent-primary">🜏</span>
            {isOpen && <span className="font-bold text-lg text-fg-primary">LILITH</span>}
          </div>
          <button 
            onClick={onToggle}
            className="p-2 rounded hover:bg-bg-tertiary transition-colors"
            aria-label={isOpen ? 'Collapse sidebar' : 'Expand sidebar'}
          >
            {isOpen ? <ChevronLeft className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />}
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 py-4 px-2 overflow-y-auto">
          <ul className="space-y-1">
            {PANELS.map((panel) => {
              const Icon = panel.icon
              const isActive = activePanel === panel.id
              return (
                <li key={panel.id}>
                  <button
                    onClick={() => setActivePanel(panel.id)}
                    className={cn(
                      'w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200',
                      'group relative overflow-hidden',
                      isActive 
                        ? 'glass-strong glow-accent text-accent-primary' 
                        : 'text-fg-secondary hover:text-fg-primary hover:bg-bg-tertiary',
                      !important'
                    )}
                    title={panel.label}
                  >
                    <Icon className={cn('w-5 h-5 flex-shrink-0', panel.color)} />
                    {isOpen && <span className="font-mono text-sm">{panel.label}</span>}
                    {isActive && !isOpen && (
                      <span className="absolute left-full top-1/2 -translate-y-1/2 ml-2 px-2 py-1 bg-bg-tertiary rounded text-xs font-mono whitespace-nowrap">
                        {panel.label}
                      </span>
                    )}
                  </button>
                </li>
              )
            })}
          </ul>
        </nav>

        {/* Bottom status */}
        <div className="p-4 border-t border-border-primary">
          {isOpen && (
            <div className="space-y-2 text-xs">
              <div className="flex items-center gap-2 text-fg-muted">
                <span className="w-2 h-2 rounded-full bg-success" />
                <span>System Online</span>
              </div>
              <div className="flex items-center gap-2 text-fg-muted">
                <Zap className="w-4 h-4 text-accent-primary" />
                <span>NVIDIA RTX 3060</span>
              </div>
              <div className="flex items-center gap-2 text-fg-muted">
                <Database className="w-4 h-4 text-accent-secondary" />
                <span>NGD Connected</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </aside>
  )
}

function Header({ activePanel }) {
  const panel = PANELS.find(p => p.id === activePanel)
  const Icon = panel?.icon

  return (
    <header className="h-14 glass border-b border-border-primary flex items-center justify-between px-6">
      <div className="flex items-center gap-4">
        {panel && (
          <div className="flex items-center gap-3">
            <Icon className={cn('w-6 h-6', panel.color)} />
            <h1 className="font-mono text-xl font-bold text-fg-primary">{panel.label}</h1>
          </div>
        )}
      </div>
      
      <div className="flex items-center gap-4">
        <div className="hidden md:flex items-center gap-2 px-3 py-1.5 glass rounded-lg text-xs font-mono text-fg-secondary">
          <span className="w-1.5 h-1.5 rounded-full bg-success animate-pulse" />
          <span>LIVE</span>
        </div>
        
        <button className="p-2 rounded hover:bg-bg-tertiary transition-colors" title="Notifications">
          <Bell className="w-5 h-5" />
        </button>
        <button className="p-2 rounded hover:bg-bg-tertiary transition-colors" title="Theme">
          <Moon className="w-5 h-5" />
        </button>
        <button className="p-2 rounded hover:bg-bg-tertiary transition-colors text-error" title="Power">
          <Power className="w-5 h-5" />
        </button>
      </div>
    </header>
  )
}

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [activePanel, setActivePanel] = useState('sys')
  const [terminalOpen, setTerminalOpen] = useState(false)

  const PanelComponent = PANELS.find(p => p.id === activePanel)?.component || SystemPanel

  return (
    <div className="min-h-screen bg-bg-primary flex">
      <Sidebar 
        isOpen={sidebarOpen} 
        onToggle={() => setSidebarOpen(!sidebarOpen)}
        activePanel={activePanel}
        setActivePanel={setActivePanel}
      />
      
      <div className={cn(
        'flex-1 flex flex-col transition-all duration-300',
        sidebarOpen ? 'ml-64' : 'ml-16'
      )}>
        <Header activePanel={activePanel} />
        
        <main className="flex-1 p-6 overflow-auto">
          <PanelComponent />
        </main>
      </div>

      {/* Floating terminal toggle */}
      <button
        onClick={() => setTerminalOpen(!terminalOpen)}
        className={cn(
          'fixed bottom-6 right-6 z-40 p-3 rounded-xl glass-strong glow-accent transition-all',
          'hover:scale-105'
        )}
        title="Toggle Terminal"
      >
        <Terminal className="w-6 h-6 text-accent-primary" />
      </button>

      {terminalOpen && (
        <div className="fixed bottom-6 right-6 z-50 w-96 h-96 glass-strong rounded-xl overflow-hidden">
          <TerminalPanel isFloating onClose={() => setTerminalOpen(false)} />
        </div>
      )}
    </div>
  )
}