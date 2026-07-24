import { useState, useEffect } from 'react'
import { 
  Brain, 
  Zap, 
  Settings, 
  RefreshCw, 
  TrendingUp, 
  BarChart3, 
  List,
  Loader2,
  Circle,
  Target,
  Trophy,
  Flame,
  Clock,
  Mic,
  Video,
  Image
} from 'lucide-react'
import { cn } from '../../lib/utils'

interface ModelInfo {
  name: string
  provider: string
  status: 'loaded' | 'loading' | 'error' | 'unloaded'
  vram: number // in MB
  ram: number // in MB
  tokensPerSecond: number
  contextSize: number
  quantization: string
  lastUsed: string
}

interface InferenceStats {
  totalRequests: number
  avgLatency: number
  tokensPerSecond: number
  errorRate: number
}

const AIPanel = () => {
  const [models, setModels] = useState<ModelInfo[]>([])
  const [stats, setStats] = useState<InferenceStats>({
    totalRequests: 0,
    avgLatency: 0,
    tokensPerSecond: 0,
    errorRate: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate fetching model stats from Lilith Gateway
    const fetchData = async () => {
      try {
        // In a real app, this would be: const response = await fetchAPI('/api/v1/models')
        // For demo, we use mock data
        setModels([
          {
            name: 'nemotron-3-ultra-550b-a12b',
            provider: 'nvidia-nim',
            status: 'loaded',
            vram: 24000,
            ram: 0,
            tokensPerSecond: 85,
            contextSize: 32768,
            quantization: 'AWQ-4bit',
            lastUpdated: new Date(Date.now() - 5 * 60 * 1000).toISOString()
          },
          {
            name: 'cosmos-3-quantized',
            provider: 'ollama',
            status: 'loaded',
            vram: 8000,
            ram: 4096,
            tokensPerSecond: 45,
            contextSize: 8192,
            quantization: 'Q4_K_M',
            lastUpdated: new Date(Date.now() - 2 * 60 * 1000).toISOString()
          },
          {
            name: 'qwen3-coder',
            provider: 'ollama',
            status: 'loading',
            vram: 6000,
            ram: 0,
            tokensPerSecond: 0,
            contextSize: 32768,
            quantization: 'Q5_K_S',
            lastUpdated: new Date(Date.now() - 30 * 1000).toISOString()
          },
          {
            name: 'llama-3-70b',
            provider: 'vllm',
            status: 'unloaded',
            vram: 0,
            ram: 0,
            tokensPerSecond: 0,
            contextSize: 0,
            quantization: 'none',
            lastUpdated: 'Never'
          }
        ])
        setStats({
          totalRequests: 12450,
          avgLatency: 320,
          tokensPerSecond: 65.5,
          errorRate: 0.2
        })
      } catch (err) {
        console.error('Failed to fetch AI stats:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-border-primary pb-4">
        <div className="flex items-center gap-3">
          <Brain className="w-6 h-6 text-accent-primary" />
          <h2 className="font-mono text-xl font-bold text-fg-primary">AI Model Management</h2>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <button className="px-3 py-1 glass rounded hover:bg-bg-tertiary transition-colors text-xs">
            <RefreshCw className="w-4 h-4" /> Refresh
          </button>
          <button className="px-3 py-1 glass rounded hover:bg-bg-tertiary transition-colors text-xs">
            <Settings className="w-4 h-4" /> Settings
          </button>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="glass p-4 rounded-lg border border-border-primary">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div className="text-center">
            <div className="text-fg-muted">Total Requests</div>
            <div className="text-fg-primary font-mono">{stats.totalRequests.toLocaleString()}</div>
          </div>
          <div className="text-center">
            <div className="text-fg-muted">Avg Latency</div>
            <div className="text-fg-primary font-mono">{stats.avgLatency}ms</div>
          </div>
          <div className="text-center">
            <div className="text-fg-muted">Tokens/sec</div>
            <div className="text-fg-primary font-mono">{stats.tokensPerSecond.toFixed(1)}</div>
          </div>
          <div className="text-center">
            <div className="text-fg-muted">Error Rate</div>
            <div className="text-fg-primary font-mono">{stats.errorRate.toFixed(1)}%</div>
          </div>
        </div>
      </div>

      {/* Models List */}
      <div className="glass p-4 rounded-lg border border-border-primary">
        <h3 className="font-mono text-lg text-fg-primary mb-4">Loaded Models</h3>
        {loading ? (
          <div className="text-center py-8">
            <Loader2 className="w-8 h-8 mx-auto mb-2 text-accent-secondary animate-spin" />
            <p className="text-fg-muted">Loading model status...</p>
          </div>
        ) : (
          <div className="space-y-3">
            {models.map((model, index) => (
              <div key={index} className="p-3 rounded-lg border border-border-primary/50 hover:border-accent-primary/50 transition-colors">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3 w-full">
                    <div className="w-8 h-8 flex-shrink-0">
                      <div className={cn(
                        'flex h-full w-full items-center justify-center rounded-full',
                        model.status === 'loaded' ? 'bg-success/20 text-success' :
                        model.status === 'loading' ? 'bg-warning/20 text-warning' :
                        model.status === 'error' ? 'bg-error/20 text-error' : 'bg-bg-tertiary'
                      )}>
                        {model.status === 'loading' && (
                          <Loader2 className="w-4 h-4 stroke-current" />
                        )}
                        {model.status === 'loaded' && (
                          <Zap className="w-4 h-4" />
                        )}
                        {model.status === 'error' && (
                          <Circle className="w-4 h-4" />
                        )}
                        {model.status === 'unloaded' && (
                          <Circle className="w-4 h-4" />
                        )}
                      </div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex justify-between w-full">
                        <h4 className="font-mono text-fg-primary truncate max-w-xs">{model.name}</h4>
                        <span className="text-xs text-fg-muted">{model.quantization}</span>
                      </div>
                      <div className="flex flex-wrap gap-2 mt-1 text-xs">
                        <span className="bg-bg-tertiary/50 px-2 py-0.5 rounded">{model.provider}</span>
                        <span className="bg-bg-tertiary/50 px-2 py-0.5 rounded">{model.status}</span>
                        <span className="bg-bg-tertiary/50 px-2 py-0.5 rounded">{model.contextSize.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')} ctx</span>
                      </div>
                    </div>
                    <div className="w-24 text-right font-mono text-sm">
                      <div className="flex items-center gap-1">
                        <Chip className="w-3 h-3" />
                        <span className="text-fg-muted">{model.vram}MB VRAM</span>
                      </div>
                      <div className="flex items-center gap-1 mt-1">
                        <Mic className="w-3 h-3" />
                        <span className="text-fg-muted">{model.ram}MB RAM</span>
                      </div>
                    </div>
                  </div>
                  <div className="text-right space-y-1">
                    <div className="text-xs font-mono">{model.tokensPerSecond.toFixed(1)} tok/s</div>
                    <div className="text-xs text-fg-muted">
                      {new Date(model.lastUpdated).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                    </div>
                  </div>
                </div>
                <div className="mt-2 w-full bg-bg-primary rounded-full h-1.5 overflow-hidden">
                  <div 
                    className="h-full rounded-full transition-all duration-500"
                    style={{ 
                      width: Math.min(model.vram / 24000 * 100, 100) + '%',
                      background: model.vram > 20000 ? 'var(--error)' : model.vram > 10000 ? 'var(--warning)' : 'var(--success)'
                    }}
                  />
                </div>
                <p className="text-xs text-fg-muted mt-1">VRAM Usage</p>
              </div>
            ))}
          </div>
        </div>

      {/* Inference Benchmark */}
      <div className="glass p-4 rounded-lg border border-border-primary">
        <h3 className="font-mono text-lg text-fg-primary mb-4 flex items-center gap-2">
          <BarChart3 className="w-5 h-5 text-accent-secondary" />
          Inference Benchmark
        </h3>
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <div className="text-fg-muted text-sm">Prompt Processing Speed</div>
              <div className="flex items-center gap-2">
                <div className="w-20 h-4 bg-bg-primary rounded-full overflow-hidden">
                  <div className="h-full bg-accent-secondary rounded" style={{ width: '75%' }} />
                </div>
                <span className="font-mono text-sm">75 tok/s</span>
              </div>
            </div>
            <div>
              <div className="text-fg-muted text-sm">Token Generation Speed</div>
              <div className="flex items-center gap-2">
                <div className="w-20 h-4 bg-bg-primary rounded-full overflow-hidden">
                  <div className="h-full bg-accent-primary rounded" style={{ width: '85%' }} />
                </div>
                <span className="font-mono text-sm">85 tok/s</span>
              </div>
            </div>
          </div>
          <div className="flex items-center justify-between border-t border-border-primary pt-4">
            <span className="text-fg-muted text-sm">Context Utilization</span>
            <div className="flex-1 ml-4">
              <div className="w-full h-4 bg-bg-primary rounded-full overflow-hidden">
                <div className="h-full bg-accent-tertiary rounded" style={{ width: '60%' }} />
              </div>
              <span className="font-mono text-sm ml-2">19660 / 32768 tokens</span>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="glass p-4 rounded-lg border border-border-primary">
        <h3 className="font-mono text-lg text-fg-primary mb-4 flex items-center gap-2">
          <Target className="w-5 h-5 text-accent-secondary" />
          Quick Actions
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          <button className="w-full px-4 py-2 glass rounded-lg hover:bg-bg-tertiary transition-colors flex items-center gap-2 text-sm font-mono">
            <Flame className="w-4 h-4" />
            Warm Up Model
          </button>
          <button className="w-full px-4 py-2 glass rounded-lg hover:bg-bg-tertiary transition-colors flex items-center gap-2 text-sm font-mono">
            <Clock className="w-4 h-4" />
            Benchmark
          </button>
          <button className="w-full px-4 py-2 glass rounded-lg hover:bg-bg-tertiary transition-colors flex items-center gap-2 text-sm font-mono">
            <Mic className="w-4 h-4" />
            Voice Chat
          </button>
          <button className="w-full px-4 py-2 glass rounded-lg hover:bg-bg-tertiary transition-colors flex items-center gap-2 text-sm font-mono">
            <Video className="w-4 h-4" />
            Video Gen
          </button>
          <button className="w-full px-4 py-2 glass rounded-lg hover:bg-bg-tertiary transition-colors flex items-center gap-2 text-sm font-mono">
            <Image className="w-4 h-4" />
            Image Gen
          </button>
          <button className="w-full px-4 py-2 glass rounded-lg hover:bg-bg-tertiary transition-colors flex items-center gap-2 text-sm font-mono">
            <Trophy className="w-4 h-4" />
            Load Cosmos 3
          </button>
        </div>
      </div>
    </div>
  )
}

export default AIPanel