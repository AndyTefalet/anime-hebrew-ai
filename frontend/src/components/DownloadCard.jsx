import { downloadUrl } from '../api/client'

export default function DownloadCard({ jobId, onReset }) {
  return (
    <div className="mt-8 p-8 bg-[#130f08] border border-orange-900/60 rounded-2xl text-center card-glow">
      <div className="text-5xl mb-4 select-none">🌀</div>
      <div className="flex items-center justify-center gap-2 mb-1">
        <div className="h-px w-10 bg-gradient-to-r from-transparent to-orange-700"></div>
        <span className="text-xs text-orange-700 tracking-widest select-none">任務完了</span>
        <div className="h-px w-10 bg-gradient-to-l from-transparent to-orange-700"></div>
      </div>
      <h2 className="text-xl font-bold text-orange-300 mb-2">Mission Complete!</h2>
      <p className="text-amber-800 mb-6 text-sm">Your Hebrew subtitles are ready.</p>
      <div className="flex gap-3 justify-center flex-wrap">
        <a
          href={downloadUrl(jobId)}
          download="hebrew_subtitles.srt"
          className="px-6 py-3 bg-gradient-to-r from-orange-700 to-red-700 hover:from-orange-500 hover:to-red-600 text-white rounded-xl font-medium transition-all duration-200 shadow-lg shadow-orange-950/50"
        >
          Download .srt
        </a>
        <button
          onClick={onReset}
          className="px-6 py-3 bg-[#1e1610] hover:bg-[#2a1f10] border border-orange-900/50 text-amber-300 rounded-xl font-medium transition-colors"
        >
          Translate Another
        </button>
      </div>
    </div>
  )
}
