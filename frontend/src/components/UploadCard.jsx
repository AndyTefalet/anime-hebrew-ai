import { useRef, useState } from 'react'

const ACCEPTED = '.mp4,.mkv,.avi,.mov,.webm,.mp3,.wav,.m4a,.ogg,.flac,.aac'

export default function UploadCard({ onUpload, disabled }) {
  const inputRef = useRef(null)
  const [dragging, setDragging] = useState(false)

  function handleFiles(files) {
    if (files.length && !disabled) onUpload(files[0])
  }

  function onDrop(e) {
    e.preventDefault()
    setDragging(false)
    handleFiles(e.dataTransfer.files)
  }

  return (
    <div
      className={`relative border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all duration-200
        ${dragging
          ? 'border-orange-400 bg-orange-950/30 card-glow-drag'
          : 'border-orange-900 hover:border-orange-600 bg-[#130f08] card-glow'}
        ${disabled ? 'opacity-50 pointer-events-none' : ''}
      `}
      onClick={() => inputRef.current?.click()}
      onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
      onDragLeave={() => setDragging(false)}
      onDrop={onDrop}
    >
      <input
        ref={inputRef}
        type="file"
        accept={ACCEPTED}
        className="hidden"
        onChange={(e) => handleFiles(e.target.files)}
      />
      <div className="text-5xl mb-4 select-none">⚔️</div>
      <p className="text-lg font-semibold text-amber-100">Drop your video or audio here</p>
      <p className="text-xs text-orange-700 tracking-widest mt-1 select-none">「動画を選べ」</p>
      <p className="text-sm text-amber-800 mt-1">MP4, MKV, MOV, MP3, WAV and more</p>
      <button
        className="mt-6 px-6 py-2 bg-gradient-to-r from-orange-700 to-red-700 hover:from-orange-500 hover:to-red-600 text-white rounded-xl font-medium transition-all duration-200 shadow-lg shadow-orange-950/50"
        onClick={(e) => { e.stopPropagation(); inputRef.current?.click() }}
      >
        Choose File
      </button>
    </div>
  )
}
