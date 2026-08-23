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
  const [name, setName] = useState('')
  const [goal, setGoal] = useState('')
  const [profileSaved, setProfileSaved] = useState(false)

  useEffect(() => {
    const stored = localStorage.getItem('neuroprep_scores')
    if (stored) {
      try {
        setHistory(JSON.parse(stored))
      } catch {
        setHistory([])
      }
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
      if (secondsLeft <= 0 && timerActive) {
        setTimerActive(false)
        submitDrill()
      }
      return
    }
    const id = window.setInterval(() => setSecondsLeft((s) => s - 1), 1000)
    return () => window.clearInterval(id)
  }, [timerActive, secondsLeft])

  const saveScore = (score: number, total: number) => {
    const entry: ScoreEntry = {
      date: new Date().toISOString().split('T')[0],
      score,
      total,
    }
    const next = [entry, ...history].slice(0, 20)
    setHistory(next)
    localStorage.setItem('neuroprep_scores', JSON.stringify(next))
  }

  const saveProfile = () => {
    localStorage.setItem('neuroprep_profile', JSON.stringify({ name, goal }))
    setProfileSaved(true)
  }

  const startDrill = async () => {
    setDrillLoading(true)
    setSubmitted(false)
    setSelected({})
    setScore(0)
    setSecondsLeft(0)
    setTimerActive(false)
    try {
      const res = await fetch(`${import.meta.env.VITE_API_BASE || 'http://localhost:8001'}/csat/drill`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic, count }),
      })
      const data = await res.json()
      setDrill(data)
      setSecondsLeft(Math.max(60, data.length * 30))
      setTimerActive(true)
    } catch (e) {
      console.error(e)
    } finally {
      setDrillLoading(false)
    }
  }

  const choose = (id: number, opt: string) => {
    if (submitted) return
    setSelected((prev) => ({ ...prev, [id]: opt }))
  }

  const submitDrill = () => {
    let s = 0
    drill.forEach((q) => {
      if (selected[q.id] === q.answer) s += 1
    })
    setScore(s)
    setSubmitted(true)
    saveScore(s, drill.length)
  }

  const generateEthics = async () => {
    setEthicsLoading(true)
    try {
      const res = await fetch(`${import.meta.env.VITE_API_BASE || 'http://localhost:8001'}/ethics/template`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: 'General ethics' }),
      })
      const data = await res.json()
      setEthics(data)
    } catch (e) {
      console.error(e)
    } finally {
      setEthicsLoading(false)
    }
  }

  const mapHeadline = async () => {
    setCurrentAffairsLoading(true)
    try {
      const res = await fetch(`${import.meta.env.VITE_API_BASE || 'http://localhost:8001'}/current-affairs/map`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ headline }),
      })
      const data = await res.json()
      setCurrentAffairs(data)
    } catch (e) {
      console.error(e)
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
            </div>
            {history.length > 0 && (
              <div className="mt-6">
                <h3 className="font-medium">Recent Drills</h3>
                <ul className="mt-2 list-disc pl-5 text-gray-700">
                  {history.slice(0, 5).map((entry, idx) => (
                    <li key={idx}>{entry.date}: {entry.score}/{entry.total}</li>
                  ))}
                </ul>
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
            {drill.length > 0 && (
              <div className="mt-4 space-y-3">
                {drill.map((q) => (
                  <div key={q.id} className="rounded border p-3">
                    <p className="font-medium">{q.prompt}</p>
                    <ul className="mt-2 list-disc pl-5 text-gray-700">
                      {q.options.map((opt) => (
                        <li key={opt}>
                          <button onClick={() => choose(q.id, opt)} className={selected[q.id] === opt ? 'font-semibold' : ''}>
                            {opt}
                          </button>
                        </li>
                      ))}
                    </ul>
                    {submitted && (
                      <div className="mt-2 text-sm text-gray-600">
                        <p>Answer: {q.answer}</p>
                        <p>{q.explanation}</p>
                      </div>
                    )}
                  </div>
                ))}
                {!submitted ? (
                  <button onClick={submitDrill} className="rounded bg-gray-900 px-4 py-2 text-white">Submit</button>
                ) : (
                  <p className="font-medium">Score: {score} / {drill.length}</p>
                )}
              </div>
            )}
          </section>
        )}
        {tab === 'ethics' && (
          <section>
            <h2 className="text-lg font-medium">Ethics Template</h2>
            <p className="mt-2 text-gray-600">Generate answer skeletons fast.</p>
            <button onClick={generateEthics} className="mt-4 rounded bg-gray-900 px-4 py-2 text-white">
              {ethicsLoading ? 'Loading...' : 'Generate Template'}
            </button>
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
