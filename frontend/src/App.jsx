import { useState, useEffect, useRef } from 'react'
import './index.css'
import { uploadFile, pollStatus } from './api/client'
import UploadCard from './components/UploadCard'
import ProgressStepper from './components/ProgressStepper'
import DownloadCard from './components/DownloadCard'
import VideoPlayer from './components/VideoPlayer'
import aotImg from './assets/aot.jpg'
import narutoImg from './assets/naruto.jpg'

const POLL_INTERVAL = 1500 // ms

export default function App() {
  const [jobId, setJobId] = useState(null)
  const [step, setStep] = useState(null)      // null = idle
  const [message, setMessage] = useState('')
  const [showPlayer, setShowPlayer] = useState(false)
  const pollRef = useRef(null)

  async function handleUpload(file) {
    setStep('uploading')
    setMessage('Sending file to server…')
    try {
      const job = await uploadFile(file)
      setJobId(job.job_id)
      setStep(job.step)
      setMessage(job.message)
    } catch (err) {
      setStep('error')
      setMessage(err?.response?.data?.detail || err.message)
    }
  }

  // Poll until done or error
  useEffect(() => {
    if (!jobId || step === 'done' || step === 'error' || step === null) return

    pollRef.current = setInterval(async () => {
      try {
        const status = await pollStatus(jobId)
        setStep(status.step)
        setMessage(status.message)
        if (status.step === 'done' || status.step === 'error') {
          clearInterval(pollRef.current)
        }
      } catch {
        // transient error — keep polling
      }
    }, POLL_INTERVAL)

    return () => clearInterval(pollRef.current)
  }, [jobId, step])

  function reset() {
    setJobId(null)
    setStep(null)
    setMessage('')
    setShowPlayer(false)
  }

  const idle = step === null
  const processing = step && step !== 'done' && step !== 'error'
  const done = step === 'done'

  return (
    <div className="min-h-screen bg-[#0a0805] text-amber-50">
      <div className="max-w-2xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-10">
          <div className="flex items-center justify-center gap-3 mb-3">
            <div className="h-px w-20 bg-gradient-to-r from-transparent to-orange-700"></div>
            <span className="text-orange-600 text-xs tracking-[0.3em] select-none">⚔ 進撃のヘブライ語 ⚔</span>
            <div className="h-px w-20 bg-gradient-to-l from-transparent to-orange-700"></div>
          </div>
          <h1 className="text-5xl font-bold mb-1 anime-glow title-flicker">
            <span className="text-orange-400">Anime</span>
            <span className="text-red-500">-Hebrew</span>
            <span className="text-amber-200"> AI</span>
          </h1>
          <p className="text-orange-800 text-xs tracking-widest mt-1 select-none">ATTACK ON NARUTO · 疾風伝ヘブライ語</p>
          <p className="text-amber-700/80 text-sm mt-4">
            Upload a video or audio — get Hebrew subtitles in seconds
          </p>
        </div>

        {/* Anime banner */}
        <div className="flex gap-3 mb-10 rounded-2xl overflow-hidden" style={{height: '200px'}}>
          <div className="relative flex-1 overflow-hidden rounded-xl">
            <img src={aotImg} alt="Attack on Titan" className="w-full h-full object-cover object-center" />
            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />
            <div className="absolute bottom-0 left-0 right-0 p-3 text-center">
              <p className="text-xs text-red-400 tracking-widest font-bold select-none">進撃の巨人</p>
              <p className="text-white text-sm font-bold select-none">ATTACK ON TITAN</p>
            </div>
          </div>
          <div className="relative flex-1 overflow-hidden rounded-xl">
            <img src={narutoImg} alt="Naruto Shippuden" className="w-full h-full object-cover object-center" />
            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />
            <div className="absolute bottom-0 left-0 right-0 p-3 text-center">
              <p className="text-xs text-orange-400 tracking-widest font-bold select-none">疾風伝</p>
              <p className="text-white text-sm font-bold select-none">NARUTO SHIPPUDEN</p>
            </div>
          </div>
        </div>

        {/* Upload area */}
        {(idle || processing) && (
          <UploadCard onUpload={handleUpload} disabled={processing} />
        )}

        {/* Progress */}
        {processing && (
          <ProgressStepper step={step} message={message} />
        )}

        {/* Error */}
        {step === 'error' && (
          <div className="mt-6 p-4 bg-red-950/40 border border-red-800 rounded-xl text-red-300 text-sm card-glow">
            <strong>⚠ Error:</strong> {message}
            <button onClick={reset} className="ml-4 underline text-orange-400 hover:text-orange-200">Try again</button>
          </div>
        )}

        {/* Done */}
        {done && <DownloadCard jobId={jobId} onReset={reset} />}

        {/* Video player toggle */}
        {(idle || done) && (
          <div className="mt-6 text-center">
            <button
              onClick={() => setShowPlayer(v => !v)}
              className="text-sm text-orange-500 hover:text-orange-300 underline transition-colors"
            >
              {showPlayer ? 'Hide' : 'Open'} video player
            </button>
          </div>
        )}

        {showPlayer && <VideoPlayer />}
      </div>
    </div>
  )
}
