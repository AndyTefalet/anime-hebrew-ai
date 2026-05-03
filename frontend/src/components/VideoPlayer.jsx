import { useRef, useState } from 'react'

export default function VideoPlayer() {
  const videoRef = useRef(null)
  const [videoUrl, setVideoUrl] = useState(null)
  const [srtUrl, setSrtUrl] = useState(null)

  function handleVideo(e) {
    const file = e.target.files[0]
    if (file) setVideoUrl(URL.createObjectURL(file))
  }

  function handleSrt(e) {
    const file = e.target.files[0]
    if (file) setSrtUrl(URL.createObjectURL(file))
  }

  return (
    <div className="mt-8 p-6 bg-gray-900/60 border border-gray-700 rounded-2xl">
      <h2 className="text-lg font-semibold text-gray-200 mb-4">Watch with Subtitles</h2>
      <div className="flex gap-4 mb-4 flex-wrap">
        <label className="flex-1 min-w-40">
          <span className="block text-xs text-gray-400 mb-1">Video file (MP4, MKV…)</span>
          <input type="file" accept="video/*" onChange={handleVideo}
            className="w-full text-sm text-gray-400 file:mr-3 file:py-1 file:px-3 file:rounded-lg file:border-0 file:bg-gray-700 file:text-gray-200 hover:file:bg-gray-600 cursor-pointer" />
        </label>
        <label className="flex-1 min-w-40">
          <span className="block text-xs text-gray-400 mb-1">Subtitle file (.srt)</span>
          <input type="file" accept=".srt,.vtt" onChange={handleSrt}
            className="w-full text-sm text-gray-400 file:mr-3 file:py-1 file:px-3 file:rounded-lg file:border-0 file:bg-gray-700 file:text-gray-200 hover:file:bg-gray-600 cursor-pointer" />
        </label>
      </div>

      {videoUrl ? (
        <video
          ref={videoRef}
          controls
          className="w-full rounded-xl bg-black"
          src={videoUrl}
          crossOrigin="anonymous"
        >
          {srtUrl && <track kind="subtitles" src={srtUrl} srcLang="he" label="Hebrew" default />}
        </video>
      ) : (
        <div className="h-40 flex items-center justify-center bg-black/40 rounded-xl text-gray-600 text-sm">
          Load a video to preview
        </div>
      )}
    </div>
  )
}
