import { useState, useEffect } from 'react'

type Tab = 'home' | 'csat' | 'ethics' | 'current-affairs'

interface CurrentAffairsResponse {
  gs_mapping: string
  answer_outline: string[]
  keywords: string[]
}

interface DrillItem {
  id: number
  topic: string
  prompt: string
  options: string[]
  answer: string
  explanation: string
}

interface EthicsTemplate {
  intro: string
  body_points: string[]
  conclusion: string
}

interface ScoreEntry {
  date: string
  score: number
  total: number
}

const TOPICS = ['General', 'Number System', 'Time Speed Distance', 'Percentages', 'Ratio', 'Averages']

function App() {
  const [tab, setTab] = useState<Tab>('home')
  const [drill, setDrill] = useState<DrillItem[]>([])
  const [drillLoading, setDrillLoading] = useState(false)
  const [selected, setSelected] = useState<Record<number, string>>({})
  const [submitted, setSubmitted] = useState(false)
  const [score, setScore] = useState(0)
  const [ethicsQuestion, setEthicsQuestion] = useState('')
  const [ethics, setEthics] = useState<EthicsTemplate | null>(null)
  const [ethicsLoading, setEthicsLoading] = useState(false)
  const [history, setHistory] = useState<ScoreEntry[]>([])
  const [topic, setTopic] = useState('General')
  const [count, setCount] = useState(3)
  const [secondsLeft, setSecondsLeft] = useState(0)
  const [timerActive, setTimerActive] = useState(false)
  const [headline, setHeadline] = useState('')
  const [currentAffairs, setCurrentAffairs] = useState<CurrentAffairsResponse | null>(null)
  const [currentAffairsLoading, setCurrentAffairsLoading] = useState(false)
  const [currentAffairsError, setCurrentAffairsError] = useState('')
  const [name, setName] = useState('')
  const [goal, setGoal] = useState('')
  const [profileSaved, setProfileSaved] = useState(false)
  const [homeError, setHomeError] = useState('')
  const [csatError, setCsatError] = useState('')
  const [ethicsError, setEthicsError] = useState('')
  const [submittedOnce, setSubmittedOnce] = useState(false)
  const [topicStats, setTopicStats] = useState<Record<string, {total:number, correct:number}>>({})

  useEffect(() => {
    const stored = localStorage.getItem('neuroprep_topic_stats')
    if (stored) {
      try { setTopicStats(JSON.parse(stored)) } catch { setTopicStats({}) }
    }
    const scores = localStorage.getItem('neuroprep_scores')
    if (scores) {
      try { setHistory(JSON.parse(scores)) } catch { setHistory([]) }
    }
    const profile = localStorage.getItem('neuroprep_profile')
    if (profile) {
      try {
        const data = JSON.parse(profile)
        setName(data.name || '')
        setGoal(data.goal || '')
        setProfileSaved(true)
      } catch {
        setProfileSaved(false)
      }
    }
  }, [])

  useEffect(() => {
    if (!timerActive || secondsLeft <= 0) {
      if (secondsLeft <= 0 && timerActive && drill.length > 0 && !autoSubmittedRef.current) {
        autoSubmittedRef.current = true
        setTimerActive(false)
        submitDrill()
      }
      if (secondsLeft <= 0) {
        setTimerActive(false)
      }
      return
    }
    const id = window.setInterval(() => setSecondsLeft((s) => s - 1), 1000)
    return () => window.clearInterval(id)
  }, [timerActive, secondsLeft, drill.length])

  const saveScore = (score: number, total: number) => {
    const entry: ScoreEntry = {
      date: new Date().toISOString().split('T')[0],
      score,
      total,
    }
    const next = [entry, ...history].slice(0, 20)
    setHistory(next)
    localStorage.setItem('neuroprep_scores', JSON.stringify(next))
    setTopicStats((prev) => {
      const updated = { ...prev }
      if (topic && topic !== 'General') {
        const current = updated[topic] || { total: 0, correct: 0 }
        updated[topic] = {
          total: current.total + total,
          correct: current.correct + score,
        }
      }
      localStorage.setItem('neuroprep_topic_stats', JSON.stringify(updated))
      return updated
    })
  }

  const saveProfile = () => {
    localStorage.setItem('neuroprep_profile', JSON.stringify({ name, goal }))
    setProfileSaved(true)
  }

  const startDrill = async () => {
    autoSubmittedRef.current = false
    setDrillLoading(true)
    setSubmitted(false)
    setSelected({})
    setScore(0)
    setSecondsLeft(0)
    setTimerActive(false)
    setCsatError('')
    try {
      const res = await fetch(`${import.meta.env.VITE_API_BASE || 'http://localhost:8001'}/csat/drill`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic, count }),
      })
      if (!res.ok) throw new Error(`Drill failed: ${res.status}`)
      const data = await res.json()
      if (!Array.isArray(data) || data.length === 0) throw new Error('No questions returned.')
      setDrill(data)
      setSecondsLeft(Math.max(60, data.length * 30))
      setTimerActive(true)
    } catch (e: any) {
      setCsatError(e?.message || 'Failed to load drill.')
      setDrill([])
    } finally {
      setDrillLoading(false)
    }
  }

  const choose = (id: number, opt: string) => {
    if (submitted) return
    setSelected((prev) => ({ ...prev, [id]: opt }))
  }

  const submitDrill = () => {
    if (!drill.length) return
    let s = 0
    drill.forEach((q) => {
      if (selected[q.id] === q.answer) s += 1
    })
    setScore(s)
    setSubmitted(true)
    setSubmittedOnce(true)
    saveScore(s, drill.length)
  }

  const generateEthics = async () => {
    setEthicsLoading(true)
    setEthicsError('')
    try {
      const res = await fetch(`${import.meta.env.VITE_API_BASE || 'http://localhost:8001'}/ethics/template`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: ethicsQuestion || 'General ethics' }),
      })
      if (!res.ok) throw new Error(`Template failed: ${res.status}`)
      const data = await res.json()
      setEthics(data)
    } catch (e: any) {
      setEthicsError(e?.message || 'Failed to load template.')
    } finally {
      setEthicsLoading(false)
    }
  }

  const mapHeadline = async () => {
    setCurrentAffairsLoading(true)
    setCurrentAffairsError('')
    try {
      const res = await fetch(`${import.meta.env.VITE_API_BASE || 'http://localhost:8001'}/current-affairs/map`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ headline }),
      })
      if (!res.ok) throw new Error(`Mapping failed: ${res.status}`)
      const data = await res.json()
      setCurrentAffairs(data)
    } catch (e: any) {
      setCurrentAffairsError(e?.message || 'Failed to map headline.')
      setCurrentAffairs(null)
    } finally {
      setCurrentAffairsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <header className="border-b">
        <div className="max-w-3xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-semibold">NeuroPrep</h1>
          <nav className="space-x-2">
            <button onClick={() => setTab('home')} className={tab === 'home' ? 'font-medium' : ''}>Home</button>
            <button onClick={() => setTab('csat')} className={tab === 'csat' ? 'font-medium' : ''}>CSAT</button>
            <button onClick={() => setTab('ethics')} className={tab === 'ethics' ? 'font-medium' : ''}>Ethics</button>
            <button onClick={() => setTab('current-affairs')} className={tab === 'current-affairs' ? 'font-medium' : ''}>Current Affairs</button>
          </nav>
        </div>
      </header>
      <main className="max-w-3xl mx-auto px-4 py-6">
        {tab === 'home' && (
          <section>
            <h2 className="text-lg font-medium">Dashboard</h2>
            <p className="mt-2 text-gray-600">Track your daily prep targets and momentum.</p>
            <div className="mt-4 space-y-2">
              <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Your name" className="w-full rounded border p-2" />
              <input value={goal} onChange={(e) => setGoal(e.target.value)} placeholder="Prep goal" className="w-full rounded border p-2" />
              <button onClick={saveProfile} className="rounded bg-gray-900 px-4 py-2 text-white">Save Profile</button>
              {profileSaved && <p className="text-sm text-gray-500">Profile saved locally.</p>}
              {homeError && <p className="text-sm text-red-600">{homeError}</p>}
            </div>
            {history.length > 0 && (
              <div className="mt-6 space-y-3">
                <div className="flex items-center gap-4 text-sm text-gray-700">
                  <span>Streak: {history.filter((entry, idx, arr) => idx === 0 || entry.date !== arr[idx - 1].date).length} days</span>
                  <span>Best: {Math.max(...history.map((entry) => entry.score / entry.total)) * 100 | 0}%</span>
                </div>
                <div>
                  <h3 className="font-medium">Recent Drills</h3>
                  <ul className="mt-2 list-disc pl-5 text-gray-700">
                    {history.slice(0, 5).map((entry, idx) => (
                      <li key={idx}>{entry.date}: {entry.score}/{entry.total}</li>
                    ))}
                  </ul>
                </div>
                {(() => {
                  const entries = Object.entries(topicStats).map(([topic, stat]) => ({ topic, total: stat.total, correct: stat.correct, accuracy: stat.total ? stat.correct / stat.total : 0 }))
                  const weak = entries.filter(e => e.accuracy < 0.7).sort((a, b) => a.accuracy - b.accuracy).slice(0, 3)
                  const strong = entries.filter(e => e.accuracy >= 0.7).sort((a, b) => b.accuracy - a.accuracy).slice(0, 3)
                  return (
                    <div className="mt-4 space-y-2">
                      <h3 className="font-medium">Topic Performance</h3>
                      {weak.length === 0 && strong.length === 0 && <p className="text-sm text-gray-500">Complete a topic drill to see weak/strong areas.</p>}
                      {weak.length > 0 && (
                        <div className="rounded border border-red-200 bg-red-50 p-2">
                          <p className="text-sm font-medium text-red-700">Weak areas</p>
                          <ul className="mt-1 list-disc pl-5 text-gray-700">
                            {weak.map((item) => (
                              <li key={item.topic}>
                                <span>{item.topic}: {Math.round(item.accuracy * 100)}% ({item.correct}/{item.total})</span>
                                <button onClick={() => { setTopic(item.topic); setTab('csat'); }} className="ml-2 rounded border px-2 py-1 text-xs">Practice</button>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                      {strong.length > 0 && (
                        <div className="rounded border border-green-200 bg-green-50 p-2">
                          <p className="text-sm font-medium text-green-700">Strong areas</p>
                          <ul className="mt-1 list-disc pl-5 text-gray-700">
                            {strong.map((item) => (
                              <li key={item.topic}>{item.topic}: {Math.round(item.accuracy * 100)}% ({item.correct}/{item.total})</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  )
                })()}
              </div>
            )}
          </section>
        )}
        {tab === 'csat' && (
          <section>
            <h2 className="text-lg font-medium">CSAT Drill</h2>
            <p className="mt-2 text-gray-600">Practice adaptive CSAT questions here.</p>
            <select value={topic} onChange={(e) => setTopic(e.target.value)} className="mt-4 rounded border p-2">
              {TOPICS.map((t) => (
                <option key={t} value={t}>{t}</option>
              ))}
            </select>
            <input
              type="number"
              min={1}
              max={15}
              value={count}
              onChange={(e) => setCount(Number(e.target.value))}
              className="mt-4 ml-2 w-16 rounded border p-2"
            />
            {timerActive && (
              <p className="mt-2 text-sm text-gray-600">Time left: {secondsLeft}s</p>
            )}
            <button onClick={startDrill} className="mt-4 ml-2 rounded bg-gray-900 px-4 py-2 text-white">
              {drillLoading ? 'Loading...' : 'Start Drill'}
            </button>
            {(() => {
              const entries = Object.entries(topicStats).map(([topic, stat]) => ({ topic, total: stat.total, correct: stat.correct, accuracy: stat.total ? stat.correct / stat.total : 0 }))
              const weak = entries.filter(e => e.accuracy < 0.7).sort((a, b) => a.accuracy - b.accuracy).slice(0, 3)
              if (weak.length === 0) return null
              return (
                <div className="mt-4 rounded border border-red-200 bg-red-50 p-3">
                  <p className="text-sm font-medium text-red-700">Suggested focus</p>
                  <ul className="mt-1 list-disc pl-5 text-gray-700">
                    {weak.map((item) => (
                      <li key={item.topic}>
                        <span>{item.topic}: {Math.round(item.accuracy * 100)}% — practice this topic</span>
                        <button onClick={() => { setTopic(item.topic); setTab('csat'); }} className="ml-2 rounded border px-2 py-1 text-xs">Practice</button>
                      </li>
                    ))}
                  </ul>
                </div>
              )
            })()}
            {drill.length > 0 ? (
              <div className="mt-4 space-y-3">
                {drill.map((q) => (
                  <div key={q.id} className="rounded border p-3">
                    <p className="font-medium">{q.prompt}</p>
                    <ul className="mt-2 list-disc pl-5 text-gray-700">
                      {q.options.map((opt) => {
                        let className = selected[q.id] === opt ? 'font-semibold' : ''
                        if (submitted) {
                          if (opt === q.answer) className = 'font-semibold text-green-700'
                          else if (selected[q.id] === opt && opt !== q.answer) className = 'font-semibold text-red-700'
                        }
                        return (
                          <li key={opt}>
                            <button onClick={() => !submitted && choose(q.id, opt)} className={className} disabled={submitted}>
                              {opt}
                            </button>
                          </li>
                        )
                      })}
                    </ul>
                    {submitted && (
                      <div className="mt-2 text-sm text-gray-600">
                        <p>
                          Result:{' '}
                          <span className={selected[q.id] === q.answer ? 'text-green-700' : 'text-red-700'}>
                            {selected[q.id] === q.answer ? 'Correct' : 'Wrong'}
                          </span>
                        </p>
                        <p>Answer: {q.answer}</p>
                        <p>{q.explanation}</p>
                      </div>
                    )}
                  </div>
                ))}
                {!submitted ? (
                  <button onClick={submitDrill} className="rounded bg-gray-900 px-4 py-2 text-white">Submit</button>
                ) : (
                  <div>
                    <p className="font-medium">Score: {score} / {drill.length}</p>
                    <button onClick={() => setTab('home')} className="mt-2 rounded border px-3 py-1 text-sm">View analytics on dashboard</button>
                  </div>
                )}
                {submittedOnce && !submitted && drill.length > 0 && (
                  <p className="text-sm text-gray-500">Timer ended. Submit to see score.</p>
                )}
                {csatError && <p className="text-sm text-red-600">{csatError}</p>}
              </div>
            ) : (
              <p className="mt-4 text-sm text-gray-500">Start a drill to see questions here.</p>
            )}
          </section>
        )}
        {tab === 'ethics' && (
          <section>
            <h2 className="text-lg font-medium">Ethics Template</h2>
            <p className="mt-2 text-gray-600">Generate answer skeletons fast.</p>
            <input
              value={ethicsQuestion}
              onChange={(e) => setEthicsQuestion(e.target.value)}
              placeholder="Ethics question or topic"
              className="mt-4 w-full rounded border p-2"
            />
            <button onClick={generateEthics} className="mt-2 rounded bg-gray-900 px-4 py-2 text-white">
              {ethicsLoading ? 'Loading...' : 'Generate Template'}
            </button>
            {ethicsError && <p className="mt-2 text-sm text-red-600">{ethicsError}</p>}
            {ethics && (
              <div className="mt-4 space-y-2">
                <p className="font-medium">Intro</p>
                <p className="text-gray-700">{ethics.intro}</p>
                <p className="font-medium">Body</p>
                <ul className="list-disc pl-5 text-gray-700">
                  {ethics.body_points.map((point, idx) => (
                    <li key={idx}>{point}</li>
                  ))}
                </ul>
                <p className="font-medium">Conclusion</p>
                <p className="text-gray-700">{ethics.conclusion}</p>
              </div>
            )}
          </section>
        )}
        {tab === 'current-affairs' && (
          <section>
            <h2 className="text-lg font-medium">Current Affairs Mapper</h2>
            <p className="mt-2 text-gray-600">Turn a headline into a GS answer outline.</p>
            <input
              value={headline}
              onChange={(e) => setHeadline(e.target.value)}
              placeholder="Enter headline"
              className="mt-4 w-full rounded border p-2"
            />
            <button onClick={mapHeadline} className="mt-2 rounded bg-gray-900 px-4 py-2 text-white">
              {currentAffairsLoading ? 'Loading...' : 'Map Headline'}
            </button>
            {currentAffairsError && <p className="mt-2 text-sm text-red-600">{currentAffairsError}</p>}
            {currentAffairs && (
              <div className="mt-4 space-y-2">
                <p className="font-medium">GS Mapping</p>
                <p className="text-gray-700">{currentAffairs.gs_mapping}</p>
                <p className="font-medium">Outline</p>
                <ul className="list-disc pl-5 text-gray-700">
                  {currentAffairs.answer_outline.map((point, idx) => (
                    <li key={idx}>{point}</li>
                  ))}
                </ul>
                <p className="font-medium">Keywords</p>
                <p className="text-gray-700">{currentAffairs.keywords.join(', ')}</p>
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  )
}

export default App
